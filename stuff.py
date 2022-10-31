
# Mock the dashboard api for testing
class DashboardAPI:
    def __init__(self):
        # self.organizations = ""
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

class Organizations:
    
    def __init__(self):
        self.orgs = [{'id': '541362', 'name': 'test_org', }]
    
    def getOrganizations(self):
        return self.orgs


meraki = Meraki()
meraki.DashboardAPI = DashboardAPI()
orgs = Organizations()
meraki.DashboardAPI.organizations = orgs
mock_dash_object = meraki