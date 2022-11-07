# Meraki Appliance Subnet Updater

A simple program to re-configure the subnet and appliance ip assigned dynamically when a new appliance is created from a template network.

e.g.

network id = 12345678

## Appliance subnets/vlans conversion

|vlan_id|subnet          |appliance_ip  |
| ---   | ---            | ---          | 
|10     |192.168.159.0/24| 192.168.159.1|
|20     |192.168.129.0/24| 192.168.129.6|
|30     |192.168.165.0/24| 192.168.165.1|

These dynamically assigned subnets/ips would be converted to the below:

|vlan_id|subnet          |appliance_ip  |
| ---   | ---            | ---          | 
|10     |192.168.10.0/24| 192.168.10.1  |
|20     |192.168.20.0/24| 192.168.20.1  |
|30     |192.168.30.0/24| 192.168.30.1  |

## Process

The program works as follows:

1. Read information from CSV file devices.csv

```
serial,vlan,subnet
Q2RN-ZDH8-W3RU,1,10.10.10.1/24
Q2RN-ZDH8-W3RU,123,10.11.11.5/24
```

This file needs to contain the serial no. of the appliance to be modified, the currently assigned vlan and the new appliance ip.

> Note:  
> The subnet/appliance ip are derived based on the desired appliance ip (10.10.10.1/24) in the above example.  subnet = 10.10.10.0/24, appliance ip = 10.10.10.1.
> Entering 10.10.10.0/24 or 10.10.10.255/24 would be invalid.

> Additionally the subnet defined in the csv must be a valid subnet of the supernet defined in the Meraki template network. 10.10.0.0/16  or 10.0.0.0/8 would be valid for this example. 172.16.0.0/16 would not be.

2. An valid Meraki API key is used to connect to the dashboard api. This needs to be set as the environment variable MERAKI_DASHBOARD_API_KEY

This can be set by creating a .env file with the below contents if desired:

MERAKI_DASHBOARD_API_KEY=1234ntntntyf90

3. The appliance networkId is retrieved using the serial number in the csv.
4. The existing subnet information is saved into a file in the current directory backup.json, in case the networks need to be restored later. The restore process is detailed below.
5. The subnets will be overwritten based on the information in the csv.

> Note:
   > Only unique prefixes can be updated. If the template network is set to "same" then the  update will fail.



## Restore Process

In the event that the original subnets need to be restored the csv would need to be updated with the old subnet information. This information can be found in the backup.json
