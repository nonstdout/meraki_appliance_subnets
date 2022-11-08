from meraki_subnets import check_api_key_set, connect_to_dashboard_api, get_config_template, get_orgs, get_org, load_from_csv, save_subnet_info, update_appliance_subnet, valid_ip, valid_vlan_id
from meraki_subnets import get_appliance_network_id, get_appliance_subnets, create_appliance_subnets, restore_appliance_subnets, get_devices_from_file, clean_data, valid_serial
import os, json
import pytest

# Mock the dashboard api for testing
class DashboardAPI:
    def __init__(self):
        self.organizations = Organizations()
        self.administered = ""
        self.appliance = Appliance()
        self.batch = ""
        self.camera = ""
        self.cellularGateway = ""
        self.devices = Devices()
        self.insight = ""
        self.networks = ""
        self.sensor = "" 
        self.sm = "" 
        self.switch = ""
        self.wireless = ""

class Meraki:
    def __init__(self):
        pass
    
    def DashboardAPI(self):
        return DashboardAPI()

class Organizations:
    def __init__(self):
        self.orgs = [{'id': '541362', 'name': 'test_org', }]
    
    def getOrganizations(self):
        return self.orgs
    
    def getOrganizationConfigTemplates(self, org_id):
        return [{'id': 'N_671599294431643613', 'name': 'London-Access-Layer', 'productTypes': ['switch', 'appliance'], 'timeZone': 'America/Los_Angeles'}, {'id': 'N_671599294431643780', 'name': 'London Firewall', 'productTypes': ['appliance'], 'timeZone': 'America/Los_Angeles'}, {'id': 'N_671599294431643781', 'name': 'London-Wifi', 'productTypes': ['wireless'], 'timeZone': 'America/Los_Angeles'}]

class Devices:
    def __init__(self):
        self.devices = [{'lat': 51.517, 'lng': -0.07834, 'address': 'EC2M 4YN', 'serial': 'Q2QN-Q6B7-LUZ9', 'mac': 'e0:55:3d:17:44:d5', 'wan1Ip': '109.231.220.56', 'wan2Ip': None, 'url': 'https://n193.meraki.com/Natilik-Showcase/n/yLlFYdbd/manage/nodes/new_list/246656701777109', 'networkId': 'N_671599294431629896', 'tags': [], 'name': 'DC-MX65-01', 'model': 'MX65', 'firmware': 'wired-17-10-2', 'floorPlanId': None}]
    
    def getDevice(self, serial):
        return [device for device in self.devices if serial == device['serial']][0]

class Appliance:
    def __init__(self):
        self.appliance_vlans = {'N_671599294431629896':[{'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [{'start': '192.168.2.200', 'end': '192.168.2.210', 'comment': 'ESXi,ISE,AD '}], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431631089', 'ipv6': {'enabled': False}}, {'id': 503, 'networkId': 'N_671599294431629896', 'name': 'DMZ', 'applianceIp': '192.168.3.1', 'subnet': '192.168.3.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759058', 'ipv6': {'enabled': False}}, {'id': 508, 'networkId': 'N_671599294431629896', 'name': 'VOICE', 'applianceIp': '192.168.8.1', 'subnet': '192.168.8.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759055', 'ipv6': {'enabled': False}}, {'id': 509, 'networkId': 'N_671599294431629896', 'name': 'GUEST', 'applianceIp': '192.168.9.1', 'subnet': '192.168.9.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759056', 'ipv6': {'enabled': False}}, {'id': 510, 'networkId': 'N_671599294431629896', 'name': 'CORP-WIFI', 'applianceIp': '192.168.10.1', 'subnet': '192.168.10.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759057', 'ipv6': {'enabled': False}}, {'id': 514, 'networkId': 'N_671599294431629896', 'name': 'SHOWCASE_MGMT', 'applianceIp': '192.168.0.1', 'subnet': '192.168.0.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759054', 'ipv6': {'enabled': False}}]}
    def getNetworkApplianceVlans(self, network_id):
        return self.appliance_vlans.get(network_id)

    def createNetworkApplianceVlan(self, network_id, _id, name, **kwargs):
        sub = {
            'id': _id, 
            'networkId': network_id, 
            'name': name, 
            'applianceIp': kwargs['applianceIp'], 
            'subnet': kwargs['subnet'],
            'reservedIpRanges': [],
            'dnsNameservers': 'upstream_dns',
            'dhcpHandling': 'Run a DHCP server', 
            'dhcpLeaseTime': '1 day', 
            'dhcpBootOptionsEnabled': False, 
            'dhcpOptions': [], 
            'interfaceId': '671599294431631089'
            }


        if kwargs.get('ipv6'):
            sub['ipv6'] = kwargs['ipv6']

        if not self.appliance_vlans.get(network_id):
            self.appliance_vlans[network_id] = []
        self.appliance_vlans.get(network_id).append(sub)
        return sub
    
    def updateNetworkApplianceVlan(self, network_id, vlan_id, **kwargs):
        sub = {
            'networkId': network_id, 
            'vlanId': vlan_id,
            'applianceIp': kwargs['applianceIp'], 
            'subnet': kwargs['subnet'],
            'reservedIpRanges': [],
            'dnsNameservers': 'upstream_dns',
            'dhcpHandling': 'Run a DHCP server', 
            'dhcpLeaseTime': '1 day', 
            'dhcpBootOptionsEnabled': False, 
            'dhcpOptions': [], 
            'interfaceId': '671599294431631089'
            }


        if kwargs.get('ipv6'):
            sub['ipv6'] = kwargs['ipv6']

        if not self.appliance_vlans.get(network_id):
            self.appliance_vlans[network_id] = []
        self.appliance_vlans.get(network_id).append(sub)
        return sub



mock_dash_object = Meraki()


def test_empty_api_key_fails():
    """not having env var set should raise sys.exit()"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_api_key_set('123test_Key')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "API Key not set as environment variable"

def test_connect_to_dashboard_api(): # Refactor to just test we get back a dashboardAPI with the correct keys
    """test setting up connection to dashboard api"""
    assert connect_to_dashboard_api(mock_dash_object).organizations.getOrganizations() == [{'id': '541362', 'name': 'test_org', }]

def test_orgs():
    dashboard = mock_dash_object.DashboardAPI()
    assert get_orgs(dashboard) == [{'id': '541362', 'name': 'test_org'}]

def test_get_org():
    dashboard = mock_dash_object.DashboardAPI()
    assert get_org(dashboard, None) == None
    assert get_org(dashboard, 123456) == None
    assert get_org(dashboard, 'test_org123') == None
    assert get_org(dashboard, 541362) == {'id': '541362', 'name': 'test_org'}
    assert get_org(dashboard, '541362') == {'id': '541362', 'name': 'test_org'}
    assert get_org(dashboard, 'test_org') == {'id': '541362', 'name': 'test_org'}
    assert get_org(dashboard, 'tEst_OrG') == {'id': '541362', 'name': 'test_org'}

def test_get_appliance_network_id():
    dashboard = mock_dash_object.DashboardAPI()
    assert get_appliance_network_id(dashboard, "Q2QN-Q6B7-LUZ9") == 'N_671599294431629896'
    assert get_appliance_network_id(dashboard, "Q123-Q6B7-2131") == None

def test_get_appliance_subnets():
    dashboard = mock_dash_object.DashboardAPI()
    assert get_appliance_subnets(dashboard, 'N_671599294431629896', save=False) == [{'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [{'start': '192.168.2.200', 'end': '192.168.2.210', 'comment': 'ESXi,ISE,AD '}], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431631089', 'ipv6': {'enabled': False}}, {'id': 503, 'networkId': 'N_671599294431629896', 'name': 'DMZ', 'applianceIp': '192.168.3.1', 'subnet': '192.168.3.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759058', 'ipv6': {'enabled': False}}, {'id': 508, 'networkId': 'N_671599294431629896', 'name': 'VOICE', 'applianceIp': '192.168.8.1', 'subnet': '192.168.8.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759055', 'ipv6': {'enabled': False}}, {'id': 509, 'networkId': 'N_671599294431629896', 'name': 'GUEST', 'applianceIp': '192.168.9.1', 'subnet': '192.168.9.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759056', 'ipv6': {'enabled': False}}, {'id': 510, 'networkId': 'N_671599294431629896', 'name': 'CORP-WIFI', 'applianceIp': '192.168.10.1', 'subnet': '192.168.10.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759057', 'ipv6': {'enabled': False}}, {'id': 514, 'networkId': 'N_671599294431629896', 'name': 'SHOWCASE_MGMT', 'applianceIp': '192.168.0.1', 'subnet': '192.168.0.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759054', 'ipv6': {'enabled': False}}]
    assert get_appliance_subnets(dashboard, 'N_671599294431629896') == [{'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [{'start': '192.168.2.200', 'end': '192.168.2.210', 'comment': 'ESXi,ISE,AD '}], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431631089', 'ipv6': {'enabled': False}}, {'id': 503, 'networkId': 'N_671599294431629896', 'name': 'DMZ', 'applianceIp': '192.168.3.1', 'subnet': '192.168.3.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759058', 'ipv6': {'enabled': False}}, {'id': 508, 'networkId': 'N_671599294431629896', 'name': 'VOICE', 'applianceIp': '192.168.8.1', 'subnet': '192.168.8.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759055', 'ipv6': {'enabled': False}}, {'id': 509, 'networkId': 'N_671599294431629896', 'name': 'GUEST', 'applianceIp': '192.168.9.1', 'subnet': '192.168.9.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759056', 'ipv6': {'enabled': False}}, {'id': 510, 'networkId': 'N_671599294431629896', 'name': 'CORP-WIFI', 'applianceIp': '192.168.10.1', 'subnet': '192.168.10.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759057', 'ipv6': {'enabled': False}}, {'id': 514, 'networkId': 'N_671599294431629896', 'name': 'SHOWCASE_MGMT', 'applianceIp': '192.168.0.1', 'subnet': '192.168.0.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759054', 'ipv6': {'enabled': False}}]
    assert get_appliance_subnets(dashboard, 'N_123456789111119812') == None
    assert get_appliance_subnets(dashboard, '') == None
    assert get_appliance_subnets(dashboard, '', save=False) == None
    # assert get_appliance_subnets(dashboard, 'N_671599294431629896') == "called save"
    # assert get_appliance_subnets(dashboard, '', save=False) == "didn't call save"
    
def test_save_subnet_info():
    test_backup_file = "test_backup.json"
    subnets = [{'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24'}]
    if os.path.exists(test_backup_file):
        os.remove(test_backup_file)
    assert not os.path.exists(test_backup_file)
    save_subnet_info(subnets, 'N_671599294431629896', test_backup_file)
    assert os.path.exists(test_backup_file)
    with open(test_backup_file, "r") as f:
            existing_subs = json.load(f)
    assert existing_subs == {'N_671599294431629896':[{'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24'}]}
    os.remove(test_backup_file)

def test_create_appliance_subnets():
    mock_dash_object = Meraki()
    dashboard = mock_dash_object.DashboardAPI()
    assert get_appliance_subnets(dashboard, 'N_671599294431629896', save=False) == [{'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [{'start': '192.168.2.200', 'end': '192.168.2.210', 'comment': 'ESXi,ISE,AD '}], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431631089', 'ipv6': {'enabled': False}}, {'id': 503, 'networkId': 'N_671599294431629896', 'name': 'DMZ', 'applianceIp': '192.168.3.1', 'subnet': '192.168.3.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759058', 'ipv6': {'enabled': False}}, {'id': 508, 'networkId': 'N_671599294431629896', 'name': 'VOICE', 'applianceIp': '192.168.8.1', 'subnet': '192.168.8.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759055', 'ipv6': {'enabled': False}}, {'id': 509, 'networkId': 'N_671599294431629896', 'name': 'GUEST', 'applianceIp': '192.168.9.1', 'subnet': '192.168.9.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759056', 'ipv6': {'enabled': False}}, {'id': 510, 'networkId': 'N_671599294431629896', 'name': 'CORP-WIFI', 'applianceIp': '192.168.10.1', 'subnet': '192.168.10.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759057', 'ipv6': {'enabled': False}}, {'id': 514, 'networkId': 'N_671599294431629896', 'name': 'SHOWCASE_MGMT', 'applianceIp': '192.168.0.1', 'subnet': '192.168.0.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759054', 'ipv6': {'enabled': False}}]
    sub_to_add = {
        "id": "666",
        "name": "TERSSTT",
        "subnet": "10.10.10.0/24",
        "applianceIp": "10.10.10.1"
    }

    assert create_appliance_subnets(dashboard, 'N_671599294431629896', **sub_to_add) == {
            'id': "666", 
            'networkId': 'N_671599294431629896', 
            'name': 'TERSSTT', 
            'applianceIp': '10.10.10.1', 
            'subnet': '10.10.10.0/24', 
            'reservedIpRanges': [], 
            'dnsNameservers': 'upstream_dns', 
            'dhcpHandling': 'Run a DHCP server', 
            'dhcpLeaseTime': '1 day', 
            'dhcpBootOptionsEnabled': False, 
            'dhcpOptions': [], 
            'interfaceId': '671599294431631089',
        }
    assert get_appliance_subnets(dashboard, 'N_671599294431629896', save=False) == [
        {'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [{'start': '192.168.2.200', 'end': '192.168.2.210', 'comment': 'ESXi,ISE,AD '}], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431631089', 'ipv6': {'enabled': False}}, 
        {'id': 503, 'networkId': 'N_671599294431629896', 'name': 'DMZ', 'applianceIp': '192.168.3.1', 'subnet': '192.168.3.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759058', 'ipv6': {'enabled': False}}, 
        {'id': 508, 'networkId': 'N_671599294431629896', 'name': 'VOICE', 'applianceIp': '192.168.8.1', 'subnet': '192.168.8.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759055', 'ipv6': {'enabled': False}}, 
        {'id': 509, 'networkId': 'N_671599294431629896', 'name': 'GUEST', 'applianceIp': '192.168.9.1', 'subnet': '192.168.9.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759056', 'ipv6': {'enabled': False}}, 
        {'id': 510, 'networkId': 'N_671599294431629896', 'name': 'CORP-WIFI', 'applianceIp': '192.168.10.1', 'subnet': '192.168.10.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759057', 'ipv6': {'enabled': False}}, 
        {'id': 514, 'networkId': 'N_671599294431629896', 'name': 'SHOWCASE_MGMT', 'applianceIp': '192.168.0.1', 'subnet': '192.168.0.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759054', 'ipv6': {'enabled': False}},
        {
            'id': '666', 
            'networkId': 'N_671599294431629896', 
            'name': 'TERSSTT', 
            'applianceIp': '10.10.10.1', 
            'subnet': '10.10.10.0/24', 
            'reservedIpRanges': [], 
            'dnsNameservers': 'upstream_dns', 
            'dhcpHandling': 'Run a DHCP server', 
            'dhcpLeaseTime': '1 day', 
            'dhcpBootOptionsEnabled': False, 
            'dhcpOptions': [], 
            'interfaceId': '671599294431631089'
        }]
    
def test_restore_appliance_subnets():
    mock_dash_object = Meraki()
    dashboard = mock_dash_object.DashboardAPI()
    test_backup_file = "test_backup.json"
    if os.path.exists(test_backup_file):
        os.remove(test_backup_file)
    assert not os.path.exists(test_backup_file)
    subs = {"N_671599294431629894": [
    {
      "id": 500,
      "networkId": "N_671599294431629894",
      "name": "SHOWCASEMGMT",
      "applianceIp": "192.168.0.254",
      "subnet": "192.168.0.0/24",
      'reservedIpRanges': [], 
      'dnsNameservers': 'upstream_dns',
      'dhcpHandling': 'Do not respond to DHCP requests',
      'interfaceId': '671599294431631089'
    },
    {
      "id": 504,
      "networkId": "N_671599294431629894",
      "name": "inside",
      "applianceIp": "192.168.4.254",
      "subnet": "192.168.4.0/24",
      'reservedIpRanges': [], 
      'dnsNameservers': 'upstream_dns',
      'dhcpHandling': 'Do not respond to DHCP requests',
      'interfaceId': '671599294431631089'
    },
    {
      "id": 506,
      "networkId": "N_671599294431629894",
      "name": "outside",
      "applianceIp": "192.168.6.254",
      "subnet": "192.168.6.0/24",
      'reservedIpRanges': [], 
      'dnsNameservers': 'upstream_dns',
      'dhcpHandling': 'Do not respond to DHCP requests',
      'interfaceId': '671599294431631089'
    }
    ]
    }

    with open(test_backup_file, "w") as f:
        f.write(json.dumps(subs))
    mock_dash_object.DashboardAPI().appliance.appliance_vlans = {}
    restore_appliance_subnets(dashboard, 'N_671599294431629894', test_backup_file)
    assert get_appliance_subnets(dashboard, 'N_671599294431629894', save=False) == [
        {'id': 500, 'networkId': 'N_671599294431629894', 'name': 'SHOWCASEMGMT', 
        'applianceIp': '192.168.0.254', 'subnet': '192.168.0.0/24', 
        'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 
        'dhcpHandling': 'Run a DHCP server', 
        'dhcpLeaseTime': '1 day', 
        'dhcpBootOptionsEnabled': False, 
        'dhcpOptions': [], 
        'interfaceId': '671599294431631089'},
        {'id': 504, 'networkId': 'N_671599294431629894', 'name': 'inside', 
        'applianceIp': '192.168.4.254', 'subnet': '192.168.4.0/24', 
        'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 
        'dhcpHandling': 'Run a DHCP server', 
        'dhcpLeaseTime': '1 day', 
        'dhcpBootOptionsEnabled': False, 
        'dhcpOptions': [], 
        'interfaceId': '671599294431631089'}, 
        {'id': 506, 'networkId': 'N_671599294431629894', 
        'name': 'outside', 'applianceIp': '192.168.6.254', 
        'subnet': '192.168.6.0/24', 'reservedIpRanges': [], 
        'dnsNameservers': 'upstream_dns', 
        'dhcpHandling': 'Run a DHCP server', 
        'dhcpLeaseTime': '1 day', 
        'dhcpBootOptionsEnabled': False, 
        'dhcpOptions': [], 
        'interfaceId': '671599294431631089'}]
    os.remove(test_backup_file)

def test_load_from_csv():
    devices_file = 'test_devices.csv'
    if os.path.exists(devices_file):
        os.remove(devices_file)
    with open(devices_file, 'w') as f:
        f.write("serial,vlan,subnet\nQ2RN-ZDH8-W3RU,10,192.168.10.1/24\nQ2RN-ZDH8-W3RU,20,192.168.20.1/24\nQ2RN-ZDH8-W2RU,20,192.168.20.1/24\nQ2RN-ZDH8-W2RU,10,192.168.10.1/24\nQ2RN-ZDH8-W3RU,30,192.168.30.1/24\nQ2RN-ZDH8-W3RU,40,192.168.40.1/24\nQ2RN-ZDH8-W1RU,10,192.168.10.1/24\nQ2RN-ZDH8-W1RU,40,192.168.40.1/24")
    with open(devices_file, 'r') as f:
        assert load_from_csv(f) == {'Q2RN-ZDH8-W3RU': {'subnets': {('40', '192.168.40.1/24'), ('10', '192.168.10.1/24'), ('20', '192.168.20.1/24'), ('30', '192.168.30.1/24')}}, 'Q2RN-ZDH8-W2RU': {'subnets': {('10', '192.168.10.1/24'), ('20', '192.168.20.1/24')}}, 'Q2RN-ZDH8-W1RU': {'subnets': {('40', '192.168.40.1/24'), ('10', '192.168.10.1/24')}}}
    os.remove(devices_file)

def test_get_devices_from_file():
    devices_file = 'test_devices.csv'
    with pytest.raises(FileNotFoundError) as excinfo:
        get_devices_from_file(devices_file)
        assert "Please create devices.csv file" in excinfo
    if os.path.exists(devices_file):
        os.remove(devices_file)
    with open(devices_file, 'w') as f:
        f.write("serial,vlan,subnet\nQ2RN-ZDH8-W3RU,10,192.168.10.1/24\nQ2RN-ZDH8-W3RU,20,192.168.20.1/24\nQ2RN-ZDH8-W2RU,20,192.168.20.1/24\nQ2RN-ZDH8-W2RU,10,192.168.10.1/24\nQ2RN-ZDH8-W3RU,30,192.168.30.1/24\nQ2RN-ZDH8-W3RU,40,192.168.40.1/24\nQ2RN-ZDH8-W1RU,10,192.168.10.1/24\nQ2RN-ZDH8-W1RU,40,192.168.40.1/24")
    assert get_devices_from_file(devices_file) == {'Q2RN-ZDH8-W3RU': {'subnets': {('40', '192.168.40.1/24'), ('10', '192.168.10.1/24'), ('20', '192.168.20.1/24'), ('30', '192.168.30.1/24')}}, 'Q2RN-ZDH8-W2RU': {'subnets': {('10', '192.168.10.1/24'), ('20', '192.168.20.1/24')}}, 'Q2RN-ZDH8-W1RU': {'subnets': {('40', '192.168.40.1/24'), ('10', '192.168.10.1/24')}}}
    os.remove(devices_file)

def test_update_appliance_subnet():
    mock_dash_object = Meraki()
    dashboard = mock_dash_object.DashboardAPI()
    sub_to_update = {
        "id": "666",
        "subnet": "11.11.11.0/24",
        "applianceIp": "11.11.11.1"
    }
    assert update_appliance_subnet(dashboard, 'N_671599294431629894', 666, **sub_to_update) == {'networkId': 'N_671599294431629894', 'vlanId': 666, 'applianceIp': '11.11.11.1', 'subnet': '11.11.11.0/24', 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431631089'}

def test_clean_data():
    spaces_data = [
        {"serial": "Q2RN-ZDH8-W3RU ", "vlan": " 1", "subnet": "  10. 10.1 0.1/24 "},
        {"serial": " Q2RN- ZD H8-W3RU ", "vlan": "12 3 ", "subnet": "10.11.11.5/24  "},
    ]
    assert clean_data(spaces_data) == [
        {"serial": "Q2RN-ZDH8-W3RU", "vlan": "1", "subnet": "10.10.10.1/24"},
        {"serial": "Q2RN-ZDH8-W3RU", "vlan": "123", "subnet": "10.11.11.5/24"},
    ]

    ints_data = [
        {"serial": " Q2RN-ZDH8-W3RU ", "vlan": 1, "subnet": "  10.10.10.1/24 "},
        {"serial": " Q2RN-ZDH8-W3RU ", "vlan": 123, "subnet": "10.11.11.5/24"},
    ]
    assert clean_data(ints_data) == [
        {"serial": "Q2RN-ZDH8-W3RU", "vlan": "1", "subnet": "10.10.10.1/24"},
        {"serial": "Q2RN-ZDH8-W3RU", "vlan": "123", "subnet": "10.11.11.5/24"},
    ]

def test_validate_serial():
    good_serials = ["1234-2234-1111", "Q2RN-ZDH8-W3RU"] 
    bad_serials = ["Q-QWFP-AART", "QSTF_123W_STFW", "QWFP-STFF-£2ST", "QWFP-QRP2-f2WF", ""]
    for serial in good_serials:
        assert valid_serial(serial)
    for serial in bad_serials:
        assert not valid_serial(serial)

def test_validate_vlan_id():
    good_ids = [1234, 100, 200, "300", "5", 1, 3967]
    bad_ids = ["nine", 0, "4095", 3968, -13, ""]
    for vlan_id in good_ids:
        assert valid_vlan_id(vlan_id)
    for vlan_id in bad_ids:
        assert not valid_vlan_id(vlan_id)

def test_validate_ip():
    good_ips = [("10.0.1.1/24", "10.0.0.0/16"), ("192.168.0.1/22", "192.168.0.0/16"), ("10.0.0.1/8", "10.0.0.0/8"), ("172.16.2.254/24", "172.16.0.0/22")]
    bad_ips = [("127.0.0.1/24","127.0.0.0/24"),("224.0.0.1/24", "224.0.0.0/24"),("0.1.1.1/1", "1.1.1.1/24"), ("592.168.0.1/22", "2.2.2.2"), ("10.1.1000.1/8","1.2.3.4/21"), ("172..16.2.254/24","1.2.3.4/21")]
    for ip, supernet in good_ips:
        assert valid_ip(ip, supernet)
    for ip, supernet in bad_ips:
        assert not valid_ip(ip, supernet)

def test_get_config_templates():
    org_id = "548548"
    mock_dash_object = Meraki()
    dashboard = mock_dash_object.DashboardAPI()
    assert get_config_template(dashboard, org_id, product_types=["appliance"]) == [{'id': 'N_671599294431643613', 'name': 'London-Access-Layer', 'productTypes': ['switch', 'appliance'], 'timeZone': 'America/Los_Angeles'}, {'id': 'N_671599294431643780', 'name': 'London Firewall', 'productTypes': ['appliance'], 'timeZone': 'America/Los_Angeles'}]
    assert get_config_template(dashboard, org_id, product_types=["appliance"]) == [{'id': 'N_671599294431643613', 'name': 'London-Access-Layer', 'productTypes': ['switch', 'appliance'], 'timeZone': 'America/Los_Angeles'}, {'id': 'N_671599294431643780', 'name': 'London Firewall', 'productTypes': ['appliance'], 'timeZone': 'America/Los_Angeles'}]
    assert get_config_template(dashboard, org_id, product_types=["appliance", "switch"]) == [{'id': 'N_671599294431643613', 'name': 'London-Access-Layer', 'productTypes': ['switch', 'appliance'], 'timeZone': 'America/Los_Angeles'},{'id': 'N_671599294431643780', 'name': 'London Firewall', 'productTypes': ['appliance'], 'timeZone': 'America/Los_Angeles'}]