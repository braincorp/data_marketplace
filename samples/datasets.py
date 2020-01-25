"""
Lists and Downloads datasets from the AI Marketplace Dataset API.

Supports filtering from a data range and a specified site.

requires python3.6+, pytz, python-dateutil, requests, clint, PrettyTable
"""

import requests
import os
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import dateutil.parser
import pytz
import time
import argparse
from clint.textui import progress


envs = {
    'local': 'http://localhost:4000',
    'azure': 'https://shelfscanninginsights.azurewebsites.net'
}

token_payload = {
    'grant_type': 'client_credentials',
    'scope': 'partner',
}
headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json',
}

token = None


def hydrate_token():
    global headers
    global token_payload

    res = requests.post(os.environ['AUTH_URL'], headers=headers, data=token_payload, auth=HTTPBasicAuth(os.environ['PARTNER_CLIENT_ID'], os.environ['PARTNER_CLIENT_SECRET']))
    res.raise_for_status()
    global token
    token = res.json()['access_token']


def download(name, url):
    """
    Downloads file to current directory.
    :param name: Name of the file
    :param url: The locator of the file.
    :return: None
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_length = int(r.headers.get('content-length'))
        with open(name, 'wb') as f:
            for chunk in progress.bar(r.iter_content(chunk_size=8192), expected_size=(total_length/8192) + 1):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)


def table(datasets):
    """
    prints a formatted table of the returned datasets.
    :param datasets:
    :return: None
    """
    from prettytable import PrettyTable

    t = PrettyTable()
    t.field_names = ["File", "Date", "Site"]
    for d in datasets:
        t.add_row([d['meta']['name'], d['date'], d['location']])

    print(t)


def main(opts):
    start_date = opts['start_date']
    end_date = opts['end_date']
    site = opts['site_name']
    list_available = opts['list_available']
    download_available = opts['download_available']
    type = opts['type']


    hydrate_token()

    params = {}
    if site:
        params['location'] = site

    if type == 'filtered':
        resource = 'datasets'
    elif type == 'unfiltered':
        resource = 'datasets-unfiltered'
    else:
        raise ValueError('unsupported type')

    res = requests.get(f'https://shelfscanninginsights.azurewebsites.net/v1/{resource}', params=params, headers={'Authorization': f'Bearer {token}'})
    res.raise_for_status()

    datasets = list(filter(lambda d: dateutil.parser.parse(d['date']) >= start_date and dateutil.parser.parse(d['date']) <= end_date, res.json()))
    if list_available:
        table(datasets)

    if download_available:
        for dataset in datasets:
            dataset_name = os.path.basename(dataset['meta']['name'])
            print('downloading dataset:', dataset_name)
            try:
                download(dataset_name, dataset['href'])
            except Exception as e:
                print(e)
                print('retrying dataset:', dataset_name)
                time.sleep(10)
                download(dataset_name, dataset['href'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='list and download datasets')
    parser.add_argument('--start-date', type=str, default='1970-01-01T00:00:00.000Z', help='start date')
    parser.add_argument('--end-date', type=str, default=datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(), help='end date')
    parser.add_argument('--list', type=bool, default=False, nargs='?', const=True, help='list datasets satisfying criterion')
    parser.add_argument('--download', type=bool, default=False, nargs='?', const=True, help='download to current directory')
    parser.add_argument('--site', type=str, default=None, help='download to current directory')
    parser.add_argument('--type', type=str, default='unfiltered', help='dataset type filtered or unfiltered')

    args = parser.parse_args()

    start = dateutil.parser.parse(args.start_date)
    end = dateutil.parser.parse(args.end_date)

    if start >= end:
        raise ValueError('start date is greater then end date')

    if not args.download and not args.list:
        raise ValueError('please select and option, --list,--download')

    supported_types = ['filtered', 'unfiltered']

    if args.type not in supported_types:
        raise ValueError(f'invalid type parameter, {args.type} not {",".join(supported_types)}')

    opt = {
        'start_date': start,
        'end_date': end,
        'site_name': args.site,
        'list_available': args.list,
        'download_available': args.download,
        'type': args.type,
    }

    main(opt)
