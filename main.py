import requests

base_url = "https://monitoringapi.solaredge.com/v2"

headers = {
    'X-Account-Key': "2qJoXFz8OGWqsXoXHCRkZ0GrhudZBV2HgAQSqIye7dw=",
    'X-API-Key': "OSvay4Laaldn/85Sb/HqJ8GUz/jMbSEmkVing2GRz1Y="
}

## Get all sites under my account
sites = requests.get(f"{base_url}/sites", headers=headers).json()

for site in sites:
    site_id = site["siteId"]
    params = {
        'from': '2022-01-01T00:00:00.00Z',
        'to': '2023-01-01T00:00:00.00Z'
    }
    site_overview = requests.get(f"{base_url}/sites/{site_id}/overview", params=params, headers=headers).json()
    print(f"2022 annual consumption for site id {site_id}: {site_overview['production']['total']}")

    params = {
        'types': 'INVERTER'
    }
    site_inverters = requests.get(f"{base_url}/sites/{site_id}/devices", params=params, headers=headers).json()

    for inverter in site_inverters:
        sn = inverter['serialNumber']
        params = {
            'from': '2022-01-01T00:00:00.00Z',
            'to': '2022-01-02T00:00:00.00Z',
            'resolution': 'HOUR'
        }
        avg_voltage = requests.get(f"{base_url}/sites/{site_id}/inverters/{sn}/voltage", params=params, headers=headers).json()

