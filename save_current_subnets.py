#!/usr/bin/env python3
from meraki_subnets import check_api_key_set, get_config_template, save_data_to_csv
import meraki, os


if __name__ == '__main__':
    check_api_key_set('MERAKI_DASHBOARD_API_KEY')
    dashboard = meraki.DashboardAPI()
    org_id = os.environ.get('MERAKI_ORG_ID')
    appliance_templates = get_config_template(dashboard, org_id, ['appliance'])
    appliance_networks = [dashboard.organizations.getOrganizationNetworks(org_id, configTemplateId=template['id']) for template in appliance_templates][0]
    appliance_vlans = [dashboard.appliance.getNetworkApplianceVlans(network['id']) for network in appliance_networks][0]
    save_data_to_csv(appliance_vlans)


