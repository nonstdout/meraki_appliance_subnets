from meraki_subnets import check, check_api_key_set, connect_to_dashboard_api, get_orgs, get_org, save_subnet_info
from meraki_subnets import get_appliance_network_id, get_appliance_subnets, create_appliance_subnets
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
        api = DashboardAPI()
        return api

class Organizations:
    def __init__(self):
        self.orgs = [{'id': '541362', 'name': 'test_org', }]
    
    def getOrganizations(self):
        return self.orgs

class Devices:
    def __init__(self):
        self.devices = [{'lat': 51.517, 'lng': -0.07834, 'address': 'EC2M 4YN', 'serial': 'Q2QN-Q6B7-LUZ9', 'mac': 'e0:55:3d:17:44:d5', 'wan1Ip': '109.231.220.56', 'wan2Ip': None, 'url': 'https://n193.meraki.com/Natilik-Showcase/n/yLlFYdbd/manage/nodes/new_list/246656701777109', 'networkId': 'N_671599294431629896', 'tags': [], 'name': 'DC-MX65-01', 'model': 'MX65', 'firmware': 'wired-17-10-2', 'floorPlanId': None}]
    
    def getDevice(self, serial):
        return [device for device in self.devices if serial == device['serial']][0]

class Appliance:
    def __init__(self):
        self.appliance_vlans = [{'id': 502, 'networkId': 'N_671599294431629896', 'name': 'Inside - Showcase devices', 'applianceIp': '192.168.2.1', 'subnet': '192.168.2.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [{'start': '192.168.2.200', 'end': '192.168.2.210', 'comment': 'ESXi,ISE,AD '}], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431631089', 'ipv6': {'enabled': False}}, {'id': 503, 'networkId': 'N_671599294431629896', 'name': 'DMZ', 'applianceIp': '192.168.3.1', 'subnet': '192.168.3.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759058', 'ipv6': {'enabled': False}}, {'id': 508, 'networkId': 'N_671599294431629896', 'name': 'VOICE', 'applianceIp': '192.168.8.1', 'subnet': '192.168.8.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759055', 'ipv6': {'enabled': False}}, {'id': 509, 'networkId': 'N_671599294431629896', 'name': 'GUEST', 'applianceIp': '192.168.9.1', 'subnet': '192.168.9.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759056', 'ipv6': {'enabled': False}}, {'id': 510, 'networkId': 'N_671599294431629896', 'name': 'CORP-WIFI', 'applianceIp': '192.168.10.1', 'subnet': '192.168.10.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759057', 'ipv6': {'enabled': False}}, {'id': 514, 'networkId': 'N_671599294431629896', 'name': 'SHOWCASE_MGMT', 'applianceIp': '192.168.0.1', 'subnet': '192.168.0.0/24', 'fixedIpAssignments': {}, 'reservedIpRanges': [], 'dnsNameservers': 'upstream_dns', 'dhcpHandling': 'Run a DHCP server', 'dhcpLeaseTime': '1 day', 'dhcpBootOptionsEnabled': False, 'dhcpOptions': [], 'interfaceId': '671599294431759054', 'ipv6': {'enabled': False}}]
    def getNetworkApplianceVlans(self, network_id):
        if network_id == 'N_671599294431629896':
            return self.appliance_vlans
        return None

    def createNetworkApplianceVlan(self, network_id, _id, name, **kwargs):
        sub = {
            'id': _id, 
            'networkId': network_id, 
            'name': name, 
            'applianceIp': kwargs['applianceIp'], 
            'subnet': kwargs['subnet'],
            'fixedIpAssignments': {}, 
            'reservedIpRanges': [], 
            'dnsNameservers': 'upstream_dns', 
            'dhcpHandling': 'Run a DHCP server', 
            'dhcpLeaseTime': '1 day', 
            'dhcpBootOptionsEnabled': False, 
            'dhcpOptions': [], 
            'interfaceId': '671599294431631089', 
            'ipv6': {'enabled': False}
        }
        self.appliance_vlans.append(sub)
        return sub






mock_dash_object = Meraki()


def test():
    assert "hello" == "hello"

def test_meraki_subnet():
    assert check() == True

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
            'fixedIpAssignments': {}, 
            'reservedIpRanges': [], 
            'dnsNameservers': 'upstream_dns', 
            'dhcpHandling': 'Run a DHCP server', 
            'dhcpLeaseTime': '1 day', 
            'dhcpBootOptionsEnabled': False, 
            'dhcpOptions': [], 
            'interfaceId': '671599294431631089', 
            'ipv6': {'enabled': False}
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
            'fixedIpAssignments': {}, 
            'reservedIpRanges': [], 
            'dnsNameservers': 'upstream_dns', 
            'dhcpHandling': 'Run a DHCP server', 
            'dhcpLeaseTime': '1 day', 
            'dhcpBootOptionsEnabled': False, 
            'dhcpOptions': [], 
            'interfaceId': '671599294431631089', 
            'ipv6': {'enabled': False}
        }]