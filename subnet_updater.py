#!/usr/bin/env python3
from meraki_subnets import check_api_key_set, get_config_template, save_data_to_csv, update_appliance_subnets_from_csv
import meraki, os
import argparse

def save_current_subnets():
    appliance_templates = get_config_template(dashboard, org_id, ['appliance'])
    appliance_networks = [dashboard.organizations.getOrganizationNetworks(org_id, configTemplateId=template['id']) for template in appliance_templates][0]
    appliance_vlans = [dashboard.appliance.getNetworkApplianceVlans(network['id']) for network in appliance_networks][0]
    save_data_to_csv(appliance_vlans)

def update_subnets():
    update_appliance_subnets_from_csv(dashboard)

if __name__ == '__main__':
    check_api_key_set('MERAKI_DASHBOARD_API_KEY')


    my_parser = argparse.ArgumentParser(prog='Meraki subnet updater', 
                                            description='Configure options', 
                                                epilog='Running without options will save current subnets')
    # Add the arguments
    my_parser.add_argument('-u','--update', dest='update', action='store_true',
                           help="Update subnets with info from csv file")
    # Execute the parse_args() method
    args = my_parser.parse_args()
    update = args.update
    dashboard = meraki.DashboardAPI()
    org_id = os.environ.get('MERAKI_ORG_ID')
    if update:
        update_subnets()
    else:
        save_current_subnets()

    