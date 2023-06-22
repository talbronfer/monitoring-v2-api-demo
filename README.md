---
stoplight-id: e9nwvc91l1jf5
---

# Getting Started with Monitoring API

In this article, we'll show you how to make your first API calls to the SolarEdge Monitoring V2 API. If you're transitioning from Monitoring API V1, be sure to also read our migration guide.

In the SolarEdge Monitoring API, we can differentiate between 3 hierarchies of data:

- Fleet level
- Site level
- Device level 

In this tutorial, we'll demonstrate each hierarchy level. We will be providing code examples in Python, using the `requests` library. If you'd like to follow along, make sure to have a Python development environment and IDE set up.

The code detailed in this tutorial can also be found in this GitHub repository.
## Authorization

SolarEdge Monitoring API supports two types of authorization methods. Some of the API endpoints support both methods, while some only support API Key based authorization. Refer to each endpoint's documentation to learn more.

- **API Key** - ideal if your SolarEdge account owns the SolarEdge site, either directly or via account association. This will suit most solar installers' use case.
- **SolarEdge Connect (OAuth)** - if you don't currently have access to the SolarEdge sites in question, and you'd like the System Owner to approve your account to access their data. 

*June 2022 Update: SolarEdge Connect will be available in Q4 2023. At this point, only API Key authorization is supported.*

### Getting your API Keys

Your SolarEdge account manager will provide you with two separate API keys. Each request you make to the Monitoring API needs to have both of these keys as **HTTP headers**.

Name | Description | Header Name
---------|----------|---------
 Account Key | Identifies your SolarEdge account. Shared between users in the same account. | X-Account-Key
 User Key | Identifies the specific SolarEdge user used to access the API. | X-API-Key

Remember to store both tokens/keys in a secure location. Never store them in a public location, such as a network share drive or client-side code (JavaScript).

## Bootstrappping your project
1. Make sure that you have the `requests` library installed on your machine. Install using `pip install requests`.
2. Create a file in which we'll place the code, such as `main.py`.
2. At the top of your file, import the `requests` library:
```python
import requests
```

## Fleet Level: Site List endpoint

First, we'll configure our `headers` dictionary so that it includes the API keys, and save the API's base url:

```python
base_url = "https://monitoringapi.solaredge.com/v2/monitoring"

headers = {
    'X-Account-Key': "ACCOUNT_KEY",
    'X-API-Key': "API_KEY"
}

```

Now, we'll make a request to the [`Site List`](https://se-api.stoplight.io/docs/monitoring/833cd5efe90d0-site-list) endpoint (`/sites`) which will return all sites owned or associated to our account.

```python
sites = requests.get(f"{base_url}/sites", headers=headers).json()
```

Here's what you could expect as a result. Obviously, your API call will return different results.

```json
[
  {
    "siteId": 222881711,
    "name": "Doe, Jane JJ81234",
    "peakPower": 8.502,
    "installationDate": "2013-12-23T07:00:00Z",
    "location": {
      "address": "223 Martin Luther King Dr.",
      "city": "Los Angeles",
      "state": "California",
      "zip": "90001",
      "country": "United States"
    },
    "activationStatus": "ACTIVE",
    "note": ""
  },
  {
    "siteId": 434232993,
    "name": "Smith, Mike UU221123",
    "peakPower": 9.99,
    "installationDate": "2021-11-03T07:00:00Z",
    "location": {
      "address": "892 Main St.",
      "city": "Los Angeles",
      "state": "California",
      "zip": "90001",
      "country": "United States"
    },
    "activationStatus": "ACTIVE",
    "note": "Ownership transfer to testuser@gmail.com"
  }
]
```

## Site Level: Overview endpoint

Starting from Site List could be useful when starting to build an API integration, because it gives us SolarEdge site IDs to work with. We can now start diving deeper into the API and get **site level data**. 

Let's say we want to get the *annual solar production for 2022* for each of the sites in our fleet. Let's continue right where we stopped:

```python
for site in sites:
    site_id = site["siteId"]
    params = {
        'from': '2022-01-01T00:00:00.00Z',
        'to': '2023-01-01T00:00:00.00Z'
    }
    site_overview = requests.get(f"{base_url}/sites/{site_id}/overview", params=params, headers=headers).json()
    print(f"2022 annual consumption for site id {site_id}: {site_overview['production']['total']}")
```

The above code iterates over all sites, and calls the [`Site Overview`](https://se-api.stoplight.io/docs/monitoring/bc101de319142-site-overview) endpoint, providing a time range of `01/01/2022 00:00` until `01/01/2023 00:00`:

```json
{
    "siteId": 1148616,
    "production": {
        "total": 17994812,
        "unit": "WH",
        "toSelfConsumption": null,
        "toStorage": 1974019.6,
        "toGrid": null
    },
    "consumption": {
        "total": 15884045,
        "unit": "WH",
        "fromPv": null,
        "fromStorage": null,
        "fromGrid": null
    },
    "performance": {
        "specificYield": 1405.8447,
        "performanceRatio": null
    }
}
```
## Device Level: Inverter Voltage

Sometimes site-level endpoints are not sufficient for our use case: we might want to collect specific measurements from each inverter, or access an RGM meter explicitly rather than using aggregated site data. To do this, we can use the device level endpoints. Let's say we wanted to extract the *1 hour average voltage* for every inverter in the site. To achieve this, we can use the [`Inverter Voltage`](https://se-api.stoplight.io/docs/monitoring/30f0aa1d645cc-inverter-voltage) endpoint.

Device level endpoints require both the Site ID and the device's Serial Number to be provided as URL parameters. To determine a device's SN, we can use the [`Site Inventory`](https://se-api.stoplight.io/docs/monitoring/30abc1f8b9210-site-inventory) endpoint: 

```python
    params = {
        'types': 'INVERTER'
    }
    site_inverters = requests.get(f"{base_url}/sites/{site_id}/devices", params=params, headers=headers).json()
```
The result of this call will look something like this:

```json
[
    {
        "type": "INVERTER",
        "serialNumber": "7F16E777-F1",
        "manufacturer": "SolarEdge",
        "model": "SE7600",
        "createdAt": "2019-06-11T16:07:59-07:00",
        "connectedTo": null,
        "active": true,
        "communicationType": "ETHERNET"
    },
    {
        "type": "INVERTER",
        "serialNumber": "731CD555-E9",
        "manufacturer": "SolarEdge",
        "model": "SE5000",
        "createdAt": "2019-06-11T16:40:19-07:00",
        "connectedTo": null,
        "active": true,
        "communicationType": "RS485"
    }
]
```

Now that we have the inverters' serial numbers, we can make the call to the `Inverter Voltage` endpoint:

```python
    for inverter in site_inverters:
        sn = inverter.serialNumber
        params = {
            'from': '2022-01-01T00:00:00.00Z',
            'to': '2022-01-02T00:00:00.00Z',
            'resolution': 'HOUR'
        }
        avg_voltage = requests.get(f"{base_url}/sites/{site_id}/inverters/{sn}/voltage", params=params, headers=headers).json()
```

This is the response you can expect:

```json
{
    "period": {
        "from": "2022-01-01T00:00:00-08:00",
        "to": "2022-01-02T00:00:00-08:00"
    },
    "unit": "VOLT",
    "resolution": "HOUR",
    "values": [
        {
            "timestamp": "2022-01-01T00:00:00-08:00",
            "value": 246.3737
        },
        {
            "timestamp": "2022-01-01T01:00:00-08:00",
            "value": 246.52864
        },
        ...
    ]
}
```

