#!/usr/bin/env python3

import os, sys
import meraki
import logging

def check():
    return True

def main():
    check_api_key_set('MERAKI_DASHBOARD_API_KEY')
    dashboard = connect_to_dashboard_api(meraki)
    orgs = get_orgs(dashboard)


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

if __name__ == "__main__":
    main()