#!/usr/bin/env python3
from meraki_subnets import check_api_key_set, get_devices_from_file, update_appliance_subnet
import meraki, os

def update_appliance_subnets_from_csv(dashboard, devices_filename='data.csv', supernet=None):
    devices = get_devices_from_file(devices_filename, supernet=supernet, reformat=False)
    for device in devices:
        sub = {
            "applianceIp": device.get('applianceIp'),
            "subnet": device.get('subnet')
            }
        network_id = device.get('networkId')
        vlan = device.get('id')
        update_appliance_subnet(dashboard, network_id, vlan, **sub)


if __name__ == '__main__':
    check_api_key_set('MERAKI_DASHBOARD_API_KEY')
    dashboard = meraki.DashboardAPI()
    org_id = os.environ.get('MERAKI_ORG_ID')
    update_appliance_subnets_from_csv(dashboard)

