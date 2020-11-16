# Data Discovery APIs

The following snippet is an example of how to use the Data Discovery and Metadata Query API. This will include Authentication with the client credentials flow.

## Discovery API
This api will allow you to discover what labels and sensors where captured during the specified datetime range for a site. 

```json
{
    "sensors": [
        {
            "sensor": "color_bottom",
            "count": 16991
        },
        {
            "sensor": "color_top",
            "count": 17011
        }
    ],
    "labels": [
        {
            "label": "aisle_05L",
            "count": 58
        },
        {
            "label": "aisle_05T",
            "count": 60
        },
        {
            "label": "aisle_05R",
            "count": 38
        }
    ]
}
``` 



## Metadata Query API
This api will return any metadata for a given site, datetime range, sensors and labels. Each metadata object will have a temporary link to it's corresponding image.

### Query Params

* startDate -> ISO8601 DateTime
* endDate -> ISO8601 DateTime
* siteName -> Name of Store

```json
[
    {
        "name": "<imageName>",
        "date": "2020-07-29T17:16:03.409Z",
        "sensor": "color_top",
        "siteName": "<siteName>",
        "pose": {
            "x": -53.4742,
            "y": -19.0307,
            "theta": 1.6658
        },
        "labels": [
            "aisle_05L"
        ],
        "distance": 6888,
        "hash": "69ac405300b83f2730880acb48ddb42536209cacc25d01923a07de315ffa69b6eebec661b64951f36adc03b45e8bb928351eb4b569fccc714d6a50e854c0dcaf",
        "size": 1190558,
        "meta": {
            "created": "2020-07-31T16:39:57.323Z",
            "updated": "2020-07-31T16:39:57.323Z"
        },
        "href": "<signedLinkToDownload>"
    },
    {
        "name": "<imageName>",
        "date": "2020-07-29T17:16:02.904Z",
        "sensor": "color_top",
        "siteName": "<siteName>",
        "pose": {
            "x": -53.4671,
            "y": -19.1784,
            "theta": 1.6912
        },
        "labels": [
            "aisle_05L"
        ],
        "distance": 6192,
        "hash": "a7e6e08d558099e2bb76958826c3f8a81f800106711d2d4f242da3c43784f479aca7fed1daefbefa830cc500001439be9bcf3ca730ee1520d3799590cfd84471",
        "size": 1185698,
        "meta": {
            "created": "2020-07-31T16:39:57.323Z",
            "updated": "2020-07-31T16:39:57.323Z"
        },
        "href": "<signedLinkToDownload>"
    },
    {
        "name": "<imageName>",
        "date": "2020-07-29T17:16:02.407Z",
        "sensor": "color_top",
        "siteName": "<siteName>",
        "pose": {
            "x": -53.4538,
            "y": -19.3341,
            "theta": 1.7116
        },
        "labels": [
            "aisle_05L"
        ],
        "distance": 5080,
        "hash": "c6948ba1b2c52931f96bc1e541810db6d7e79f298e1e9563fff9493422fac0be98c523e5d4fc95a03267b916a73314f52873447ba1016fbec3b1d7d88e840886",
        "size": 1174531,
        "meta": {
            "created": "2020-07-31T16:39:57.323Z",
            "updated": "2020-07-31T16:39:57.323Z"
        },
        "href": "<signedLinkToDownload>"
    }
]
```

### Query Parameters

* startDate -> ISO8601 DateTime
* endDate -> ISO8601 DateTime
* siteName -> Name of Store

#### Optional Filters
* sensors -> comma separated list of sensors listed in discovery or well-known
* labels -> comma separated list of strings of labels listed in discovery or well-known

## Requirements

- Python 3.6+
- pip packages: requests
- environment variables - will be provided.
    - PARTNER_CLIENT_ID
    - PARTNER_CLIENT_SECRET
    - AUTH_URL

### Setup environment

The sample uses environment variables to run pass credentials. This may differ depending on OS. Linux and MAC are documented here.

```shell script
export PARTNER_CLIENT_ID=<ClientId>
export PARTNER_CLIENT_SECRET=<ClientSecret>
export AUTH_URL=https://dev-483595.okta.com/oauth2/default/v1/token
```

## Usage

```shell script
python data-discovery.py --discovery --start-date 2020-01-07T07:57:13.000Z --end-date 2020-01-07T07:57:14.000Z --site <SiteName> --scope partner
```

### Pick resource
- discovery -> Sample will pull data from discovery resource.
- query -> Sample will pull data from metadata query resource.

### Filters
- start-date and end-date -> specify a date range.
- site -> specify the site you’d like to download or inspect

#### Optional Filters
- labels -> comma list of strings of labels listed in discovery or well-known
- sensors -> comma separated list of strings of labels listed in discovery or well-known

#### Optional flags
- scope -> Oauth scope for client.