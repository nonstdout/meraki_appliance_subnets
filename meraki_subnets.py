#!/usr/bin/env python3

import csv
import os, sys
import meraki
from meraki.exceptions import APIError
import logging
import json
import ipaddress



backup_filename = "backup.json"
devices_filename = "devices.csv"


def main():
    check_api_key_set('MERAKI_DASHBOARD_API_KEY')
    dashboard = connect_to_dashboard_api(meraki)
    update_appliance_subnets_from_csv(dashboard)


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
    appliances = set(["MX65", "MX65W"])
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
        print(appliance_subnets)
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

def create_appliance_subnets(dashboard, network_id, **kwargs):
    app = dashboard.appliance
    _id = kwargs['id']
    name = kwargs['name']

    sub = kwargs
    sub.pop('id')
    sub.pop('name')
    try:
        return app.createNetworkApplianceVlan(network_id, _id, name, **sub)
    except Exception as e:
        print(e)

def restore_appliance_subnets(dashboard, network_id, backup_filename=backup_filename):
    try:
        with open(backup_filename, "r") as f:
            data = json.load(f)
            subnets = data.get(network_id)
    except Exception as e:
        print(e)
    else:
        for sub in subnets:
            sub.pop('networkId')
            create_appliance_subnets(dashboard, network_id, **sub)

def get_devices_from_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("Please create devices.csv file")
    file_type = filename.split(".")[1]
    with open(filename, 'r') as f:   
        file_types = {
            "csv": load_from_csv(f)
        }
        return file_types[file_type]

def load_from_csv(_file):
    data = list(csv.DictReader(_file))
    output = {}
    # reformat the data from csv into a nice nested format
    for i in range(len(data)): 
        device = data[i]
        if device.get('serial') not in output:
            serial, vlan, subnet = device.values()
            output[serial] = {"subnets": set([(vlan, subnet)]) }
        for j in range(i+1,len(data)):
            device2 = data[j]
            serial2, vlan2, subnet2 = device2.values()
            if serial == serial2:
                output[serial]['subnets'].add((vlan2, subnet2))

    return output

def update_appliance_subnet(dashboard, network_id, vlan_id, **kwargs):
    sub = kwargs
    app = dashboard.appliance
    try:
        return app.updateNetworkApplianceVlan(network_id, vlan_id, **sub)
    except Exception as e:
        print(e)

def update_appliance_subnets_from_csv(dashboard):
    devices = get_devices_from_file(devices_filename)
    for serial, device in devices.items():
        network_id = get_appliance_network_id(dashboard, serial)
        
        #save subnets to "backup.json"
        get_appliance_subnets(dashboard, network_id)

        subnets = device.get('subnets')
        for subnet in subnets:
            vlan, ip = subnet
            host_bit = int(ip.split(".")[3].split("/")[0])
            network_addr = ".".join(ip.split(".")[:3]) + ".0/" + ip.split("/")[1]
            net = ipaddress.ip_network(network_addr)
            appliance_ip = net.network_address + host_bit
            sub = {
                "applianceIp": str(appliance_ip),
                "subnet": str(net)
            }
            print(update_appliance_subnet(dashboard, network_id, vlan, **sub))
        
    # Need to check if the subnets are set to "unique"



if __name__ == "__main__":
    main()