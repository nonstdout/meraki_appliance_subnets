#!/usr/bin/env python3

import os, sys
from unittest import result
import meraki
import logging

def check():
    return True

def main():
    check_api_key_set('MERAKI_DASHBOARD_API_KEY')
    dashboard = connect_to_dashboard_api(meraki)
    orgs = get_orgs(dashboard)
    print(get_org(dashboard, ''))


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


if __name__ == "__main__":
    main()