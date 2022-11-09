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

These dynamically assigned subnets/ips would be coverted to the below:

|vlan_id|subnet          |appliance_ip  |
| ---   | ---            | ---          | 
|10     |192.168.10.0/24| 192.168.10.1  |
|20     |192.168.20.0/24| 192.168.20.1  |
|30     |192.168.30.0/24| 192.168.30.1  |

## Install

 - Install python 3.10
 - Install pipenv `pip install --user pipenv`
 - Add `.env` file with info detailed below
 - Run `pipenv shell` to install dependencies

## Usage

1. Create `.env` file in root of repository.

    - A valid Meraki API key is used to connect to the dashboard api. This needs to be set as the environment variable MERAKI_DASHBOARD_API_KEY

    This can be set by creating a .env file with the below contents if desired:

    `MERAKI_DASHBOARD_API_KEY=1234ntntntyf90`

    - The organisation id also needs to be set in .env:

    `MERAKI_ORG_ID=548548`

2. `python subnet_updater.py -h`


## Process

The program works as follows:

1. The existing subnet information is retrieved from the API and saved into a file in the current directory devices.csv.

site,networkId,id,subnet,applianceIp
API TEST,L_714946440845072076,1,10.129.215.160/27,10.129.215.161
API TEST,L_714946440845072076,2,10.129.82.64/27,10.129.82.65
API TEST,L_714946440845072076,3,10.129.25.224/27,10.129.25.225
API TEST,L_714946440845072076,4,10.129.8.64/27,10.129.8.65

note:
    The subnet defined in the csv must be a valid subnet of the supernet defined in the Meraki template network. 10.10.0.0/16  or 10.0.0.0/8 would be valid for this example. 172.16.0.0/16 would not be.

2. The csv need to be modified with the desired subnet information.
3. The subnets are overwritten based on the information in the csv.

note:
    Only unique prefixes can be updated. If the template network is set to "same" then the  update will fail.

## Pipenv Path issues

`pip install --user pipenv`

https://pipenv.pypa.io/en/latest/install/

This does a user installation to prevent breaking any system-wide packages. If pipenv isn’t available in your shell after installation, you’ll need to add the user base’s binary directory to your PATH.

On Linux and macOS you can find the user base binary directory by running python -m site --user-base and adding bin to the end. For example, this will typically print ~/.local (with ~ expanded to the absolute path to your home directory) so you’ll need to add ~/.local/bin to your PATH. You can set your PATH permanently by modifying ~/.profile.

On Windows you can find the user base binary directory by running python -m site --user-site and replacing site-packages with Scripts. For example, this could return C:\Users\Username\AppData\Roaming\Python36\site-packages so you would need to set your PATH to include C:\Users\Username\AppData\Roaming\Python36\Scripts. You can set your user PATH permanently in the Control Panel. You may need to log out for the PATH changes to take effect.

For more information, see the user installs documentation.