# Datasets API Example Script

The following snippet is an example of how to use the Datasets API. This will include Authentication with the client credentials flow, list out available datasets and the option to download these datasets.

## Requirements

- Python 3.6+
- pip packages: pytz, python-dateutil, requests, clint, PrettyTable
- environment variables - will be provided.
    - PARTNER_CLIENT_ID
    - PARTNER_CLIENT_SECRET
    - AUTH_URL


## Setup

There is a simple setup required to run the sample.

### Requirements installation

A requirements file has been provided to manage requirements.

```shell script
pip install -r requirements.txt
```

### Setup environment

The sample uses environment variables to run pass credentials. This may differ depending on OS. Linux and MAC are documented here

```shell script
export PARTNER_CLIENT_ID=<ClientId>
export PARTNER_CLIENT_SECRET=<ClientSecret>
export AUTH_URL=https://dev-483595.okta.com/oauth2/default/v1/token
```

## Usage

```shell script
python samples/datasets.py --list --download --start-date 2020-01-07T07:57:13.000Z --end-date 2020-01-07T07:57:14.000Z --site <SiteName>
```

- start_date and end_date - specify a date range. Optional
- site - specify the site you’d like to download or inspect. Optional
- list - displays datasets that meet specified criteria in a table view
- download - downloads all datasets that match criteria
- type - switches between the filtered and unfiltered dataset routes. Excepted values are `filtered`, `unfiltered`. Default value is `unfiltered`
