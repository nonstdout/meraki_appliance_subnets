#!/usr/bin/env python3

import os, sys
import meraki
from meraki.exceptions import APIError
import logging
import json

backup_filename = "backup.json"

def check():
    return True

def main():
    check_api_key_set('MERAKI_DASHBOARD_API_KEY')
    dashboard = connect_to_dashboard_api(meraki)
    # orgs = get_orgs(dashboard)
    # print(get_org(dashboard, ''))
    print(get_appliance_subnets(dashboard, 'N_671599294431629896'))


def check_api_key_set(key):
    logging.info("Retrieving MERAKI_DASHBOARD_API_KEY from env vars")
    if not os.environ.get(key):
        sys.exit("API Key not set as environment variable")

def connect_to_dashboard_api(api):
    api = api.DashboardAPI()
    return api

def get_orgs(dashboard):
    orgs = dashboard.organizations.getOrganizations()
    return orgs

def get_org(dashboard, org_name_or_id):
    orgs = dashboard.organizations.getOrganizations()
    if not org_name_or_id:
        return None
    try:
        org_id = int(org_name_or_id)
        try:
            return [org for org in orgs if org.get('id') == str(org_id)][0]
        except IndexError as e:
            return None

    except ValueError as e:
        print("Orgid not a number")
        print(e)
        org_name = org_name_or_id.lower()
        try:
            return [org for org in orgs if org.get('name') == org_name.lower()][0]
        except IndexError as e:
            return None

def get_appliance_network_id(dashboard, serial):
    appliances = set(["MX65"])
    try:
        device = dashboard.devices.getDevice(serial)
        if device.get("model") in appliances:
            return device.get("networkId")
        logging.info("Device: " +  device.get("name") + "is not an appliance!")
        return None
    except APIError as e:
        logging.info(e)
        return None
    except IndexError as e:
        logging.info(e)
        return None

def get_appliance_subnets(dashboard, network_id, save=True):
    try:
        appliance_subnets = dashboard.appliance.getNetworkApplianceVlans(network_id)
        if save:
            save_subnet_info(appliance_subnets, network_id, backup_filename)
        return appliance_subnets
    except APIError as e:
        logging.info(e)
        return None

def save_subnet_info(appliance_subnets, network_id, backup_filename):
    if not os.path.exists(backup_filename):
        with open(backup_filename, "w") as f:
            f.write(json.dumps({}))

    try:
        with open(backup_filename, "r") as f:
            existing_subs = json.load(f)
        
        with open(backup_filename, "w") as f:
            existing_subs[network_id] = appliance_subnets
            f.write(json.dumps(existing_subs, indent=2))
    except Exception as e:
        logging.INFO(e)

if __name__ == "__main__":
    main()