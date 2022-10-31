from meraki_subnets import check, check_api_key_set, connect_to_dashboard_api, get_orgs, get_org
import pytest

# Mock the dashboard api for testing
class DashboardAPI:
    def __init__(self):
        self.organizations = Organizations()
        self.administered = ""
        self.appliance = ""
        self.batch = ""
        self.camera = ""
        self.cellularGateway = ""
        self.devices = ""
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
    