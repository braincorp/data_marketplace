import argparse
import json
import os
import traceback
from datetime import datetime

import pytz
import requests
from requests.auth import HTTPBasicAuth
from clint.textui import progress
import concurrent.futures

class DiscoveryRepository:
    token_payload = {
        'grant_type': 'client_credentials',
        'scope': 'customer',
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
    }

    def __init__(self):
        self.token = None

    def hydrate_token(self):
        res = requests.post(os.environ['AUTH_URL'], headers=self.headers, data=self.token_payload,
                            auth=HTTPBasicAuth(os.environ['PARTNER_CLIENT_ID'], os.environ['PARTNER_CLIENT_SECRET']))
        res.raise_for_status()
        self.token = res.json()['access_token']

    def query(self, site, start_date, end_date, labels=None, limit=None, sensors=None):
        print('running metadata query')
        url = f'https://shelfscanninginsights.azurewebsites.net/v1/site-images'
        params = {'siteName': site, 'startDate': start_date, 'endDate': end_date}
        headers = {'Authorization': f'Bearer {self.token}'}
        if limit:
            params['limit'] = limit

        if labels:
            params['labels'] = labels

        if sensors:
            params['sensors'] = sensors

        res = requests.get(url, params=params, headers=headers)
        res.raise_for_status()
        return res.json()

    def discovery(self, site, start_date, end_date):
        print('running discovery query')
        print('site', site)
        print('start date', start_date)
        print('end date', end_date)
        url = f'https://shelfscanninginsights.azurewebsites.net/v1/sites-images-discovery'
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'siteName': site, 'startDate': start_date, 'endDate': end_date}
        res = requests.get(url, params=params, headers=headers)
        res.raise_for_status()
        return json.dumps(res.json(), indent=4)

s = requests.Session()
# requests.adapters.DEFAULT_RETRIES = 5

def download(name, url):
    """
    Downloads file to current directory.
    :param name: Name of the file
    :param url: The locator of the file.
    :return: None
    """
    with s.get(url, stream=True) as r:
        r.raise_for_status()
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='discover, list and download data')
    parser.add_argument('--start-date', type=str, required=True, default='1970-01-01T00:00:00.000Z', help='start date')
    parser.add_argument('--end-date', type=str, required=True,
                        default=datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
                        help='end date')
    parser.add_argument('--list', type=bool, default=False, nargs='?', const=True,
                        help='list data satisfying criterion')
    parser.add_argument('--download', type=bool, default=False, nargs='?', const=True,
                        help='download to current directory')
    parser.add_argument('--site', type=str, default=None, required=True, help='site name')
    parser.add_argument('--labels', type=str, default=None, help='CSV of labels')
    parser.add_argument('--limit', type=str, default=None, help='limit of dataset')
    parser.add_argument('--sensors', type=str, default=None, help='CSV of sensor names')
    parser.add_argument('--discovery', type=bool, default=False, nargs='?', const=True,
                        help='discover data based on site and date range.')
    parser.add_argument('--query', type=bool, default=False, nargs='?', const=True,
                        help='query data based on site, data range, labels and sensors')
    parser.add_argument('--scope', type=str, default='partner', help='dataset type filtered or unfiltered')

    args = parser.parse_args()

    r = DiscoveryRepository()
    if args.scope:
        r.token_payload['scope'] = args.scope
    r.hydrate_token()

    if args.discovery:
        print(r.discovery(args.site, args.start_date, args.end_date))
    elif args.query:
        image_meta = r.query(args.site, args.start_date, args.end_date, args.labels, args.limit, args.sensors)
        count = len(image_meta)
        serialized_meta = json.dumps(image_meta, indent=4)
        if args.download:
            print("requested download")
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(download, datum['name'], datum['href']) for datum in image_meta if len(datum['labels']) != 0}
                for future in progress.bar(concurrent.futures.as_completed(futures), expected_size=len(futures)):
                    try:
                        future.result()
                    except Exception:
                        print("can't download image, may be missing labels")
                        traceback.print_exc()
                        raise

            with open('image_metadata.json', 'w') as meta_json:
                meta_json.write(serialized_meta)

        print(serialized_meta)
        print("count", count)
    else:
        raise ValueError("no selection made --discovery or --query")
