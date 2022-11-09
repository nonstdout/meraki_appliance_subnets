#!/usr/bin/env python3
import csv
import os, sys
import meraki
import ipaddress
import re


def main():
    print("Run subnet_updater.py instead")


def check_api_key_set(key):
    # print("Retrieving MERAKI_DASHBOARD_API_KEY from env vars")
    if not os.environ.get(key):
        sys.exit("API Key not set as environment variable")

def connect_to_dashboard_api(api):
    return api.DashboardAPI()

def get_devices_from_file(filename, reformat=True, supernet=None):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Missing {filename}")
    file_type = filename.split(".")[1]
    with open(filename, 'r') as f:   
        file_types = {
            "csv": load_from_csv(f, reformat, supernet)
        }
        return file_types[file_type]

def load_from_csv(_file, reformat=True, supernet=None):
    data = list(csv.DictReader(_file))
    processed_data = clean_data(data)
    validate_data(processed_data, supernet)
    if reformat:
        return reformat_data(processed_data)
    return processed_data

def validate_data(data, supernet=None):
    for item in data:
        if item.get('serial'):
            valid_serial(item.get('serial'))
        if item.get('vlan'):
            valid_vlan_id(item.get('vlan'))
        if supernet:
            valid_ip(item.get('subnet'), supernet) 
        else:
            # Supernet is validated by the API
            pass
            # print("Can't validate ip address is valid without supernet information")
        #### need to add query to get the template supernet

def get_appliance_supernet(dashboard, org_id, vlan_id, product_types=['appliance', "switch", "wireless"]):
    template_ids = [template.get('id') for template in get_config_template(dashboard, org_id, product_types)]
    api = meraki.DashboardAPI()

    return [api.appliance.getNetworkApplianceVlan(template_id, vlan_id) for template_id in template_ids]



def reformat_data(data):
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


def valid_serial(string):
    # e.g Q2RN-ZDH8-W3RU
    serial_no = "[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}"
    return re.search(serial_no, string)

def valid_vlan_id(string):
    # range 1 -> 3967
    try:
        vlan_id = int(string)
        if not 3968 > vlan_id > 0 :
            return False
        return True
    except ValueError as e:
        return False

def valid_ip(ip, supernet):
    host_bit = int(ip.split(".")[3].split("/")[0])
    network_addr = ".".join(ip.split(".")[:3]) + ".0/" + ip.split("/")[1]
    try:
        net = ipaddress.ip_network(network_addr)
        supnet = ipaddress.ip_network(supernet)
        appliance_ip = net.network_address + host_bit
        appliance_ip2 = ipaddress.ip_address(appliance_ip)
        if net.is_link_local or net.is_loopback or net.is_multicast:
            return False
        if net.is_private and net.subnet_of(supnet) and net.version == 4:
            return True
        if appliance_ip2 != net.broadcast_address and appliance_ip2 != net.network_address:
            return True
        else:
            return False
        
    except Exception as e:
        print(e)
        return False
    

def clean_data(data):
    # Remove any spaces, cast ints to string, upper case
    output = []
    for item in data:
        thing = {}
        for k, v in item.items():
            thing[k] = "".join(str(v).split(" ")).upper()
        output.append(thing)
    return output

def update_appliance_subnet(dashboard, network_id, vlan_id, **kwargs):
    sub = kwargs
    app = dashboard.appliance
    try:
        return app.updateNetworkApplianceVlan(network_id, vlan_id, **sub)
    except Exception as e:
        print(e)

def get_config_template(dashboard, org_id, product_types=['appliance', "switch", "wireless"]):
    product_types = set(product_types)
    try:
        templates = dashboard.organizations.getOrganizationConfigTemplates(org_id)

        return [template for template in templates if set(product_types).issubset(set(template.get("productTypes"))) or set(product_types).issuperset(set(template.get("productTypes")))]

    except Exception as e:
        print(e)

def save_data_to_csv(data, filename="devices.csv", headers=["site","networkId", "id", "subnet", "applianceIp"]):
    memo = {}
    try:
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            for row in data:
                network = row.get('networkId')
                if network in memo:
                    site_name = memo[network]
                else:
                    site_name = meraki.DashboardAPI().networks.getNetwork(network).get('name')
                    memo[network] = site_name
                row['site'] = site_name
                writer.writerow(row)
            print("saved data to csv")
    except Exception as e:
        print("failed to save data to csv")
        print(e)

if __name__ == "__main__":
    main()