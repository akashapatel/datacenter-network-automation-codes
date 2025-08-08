import argparse
import requests
import json
import re
import csv
import time
from getpass import getpass
import logging

requests.packages.urllib3.disable_warnings()

# Get token for REST API
def get_token(apic_url, username, password):
    url = f"{apic_url}/api/aaaLogin.json"
    payload = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()['imdata'][0]['aaaLogin']['attributes']['token']
    else:
        raise Exception("Failed to get token")

def getvpc(apic_url, token, nodeid, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/mo/uni/fabric/protpol.json?query-target=subtree&target-subtree-class=fabricExplicitGEp&query-target-filter=not(wcard(fabricExplicitGEp.dn,"__ui_"))&target-subtree-class=fabricNodePEp,fabricRsVpcInstPol&query-target-filter=wcard(fabricNodePEp.dn,"nodepep-{nodeid}")'

    try:
        response = requests.get(url, headers=headers, verify=False)
        vpc_data = json.loads(response.content)
        vpc_value = vpc_data['imdata'][0]['fabricNodePEp']['attributes']['dn']
        vpc_pattern = r'expgep-([A-Za-z0-9-]+)/nodepep'
        vpc_match = re.search(vpc_pattern, vpc_value)
        if vpc_match:
            extracted_value = vpc_match.group(1)
            if vlog:
                logging.info(f'{url} \n {vpc_data}')
            return(extracted_value)
        else:
            print(f"No VPC found for {nodeid}")

    except Exception as e:
        print(f"No VPC found for {nodeid}")

def getname(apic_url, token, nodeid, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/mo/topology/pod-1/node-{nodeid}.json?query-target=children&target-subtree-class=topSystem'

    try:
        response = requests.get(url, headers=headers, verify=False)
        name_data = json.loads(response.content)
        name_value = name_data['imdata'][0]['topSystem']['attributes']['name']
        if vlog:
            logging.info(f'{url} \n {name_data}')
        return(name_value)

    except Exception as e:
        print(f"An error occurred: {e}")

def decomswitch(apic_url, token, nodeid):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/class/fabricRsOosPath.json?query-target-filter=wcard(fabricRsOosPath.dn,"paths-{nodeid}")'

    try:
        response = requests.get(url, headers=headers, verify=False)
        return(response.content)

    except Exception as e:
        print("Failed to decom")
        print(f"An error occurred: {e}")

def decom_switch1(apic_url, token, nodeid, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f"{apic_url}/api/node/mo/uni/fabric/outofsvc.json"
    payload = {'fabricRsDecommissionNode': {'attributes': {
        'tDn': f'topology/pod-1/node-{nodeid}',
        'status': 'created,modified','removeFromController': 'true','debug': 'false'},'children': []}}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url}{json.dumps(payload)} \n {response.content}')
    except Exception as e:
        print("Failed to decom")
        print(f"An error occurred: {e}")

def decom_switch2(apic_url, token, nodeid):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f"{apic_url}/api/node/mo/uni/fabric/outofsvc/rsdecommissionNode-[topology/pod-1/node-{nodeid}].json"
    payload = {'fabricRsDecommissionNode': {'attributes': {
        'dn': f'uni/fabric/outofsvc/rsdecommissionNode-[topology/pod-1/node-{nodeid}]',
        'status': 'deleted'},'children': []}}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    except Exception as e:
        print("Failed to decom")
        print(f"An error occurred: {e}")

def deintsearch(apic_url, token, nodeid, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/class/fabricRsOosPath.json?query-target-filter=wcard(fabricRsOosPath.dn,"paths-{nodeid}")'

    try:
        response = requests.get(url, headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} \n {response.content}')
        return(response.content)

    except Exception as e:
        print("Failed to decom")
        print(f"An error occurred: {e}")

def extract_dns(obj):
    dns_list = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "dn":
                dns_list.append(value)
            else:
                dns_list.extend(extract_dns(value))
    elif isinstance(obj, list):
        for item in obj:
            dns_list.extend(extract_dns(item))
    return dns_list


def removeinterfaces(dn_list):
    output = {
        "fabricOOServicePol": {
            "attributes": {"dn": "uni/fabric/outofsvc","status": "modified"},"children": []}}

    for dn in dn_list:
        child_entry = {
            "fabricRsOosPath": {
                "attributes": {
                    "dn": dn,
                    "status": "deleted"},"children": []}}
        output["fabricOOServicePol"]["children"].append(child_entry)
    return(output)

def removedecomports(apic_url, token, nodedata, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f"{apic_url}/api/node/mo/uni/fabric/outofsvc.json"

    payload = nodedata

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} {json.dumps(payload)} \n {response}')

    except Exception as e:
        print("Failed to remove ports")
        print(f"An error occurred: {e}")

def removeug(apic_url, token, nodeid, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    if int(nodeid) % 2 == 0:
        ug_side = "SideB"
    else:
        ug_side = "SideA"
    url = f'{apic_url}/api/node/mo/uni/fabric/maintgrp-UTC-Whitespace-{ug_side}-UG.json'
    payload = {
        'maintMaintGrp': {'attributes': {'dn': f'uni/fabric/maintgrp-UTC-Whitespace-{ug_side}-UG','status':
        'modified'},'children': [{'fabricNodeBlk': {'attributes': {
        'dn': f'uni/fabric/maintgrp-UTC-Whitespace-{ug_side}-UG/nodeblk-blk{nodeid}-{nodeid}',
        'status': 'deleted'},'children': []}}]}}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} {json.dumps(payload)} \n {response.content}')
        return(response.content)

    except Exception as e:
        print("Failed to remove from UG")
        print(f"An error occurred: {e}")

def removestaticnodeaddress(apic_url, token, nodeid, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/mo/uni/tn-mgmt/mgmtp-default/inb-inb_mgmt-EPG/rsinBStNode-[topology/pod-1/node-{nodeid}].json'
    payload = {'mgmtRsInBStNode':{'attributes':{'dn':f'uni/tn-mgmt/mgmtp-default/inb-inb_mgmt-EPG/rsinBStNode-[topology/pod-1/node-{nodeid}]','status':'deleted'},'children':[]}}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} {json.dumps(payload)} \n {response.content}')
        return(response.content)

    except Exception as e:
        print("Failed to decom")
        print(f"An error occurred: {e}")

def removeleafprofile(apic_url, token, switchname, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/mo/uni/infra.json'
    payload = {'infraInfra': {'attributes': {'dn': 'uni/infra','status': 'modified'},
    'children': [{'infraNodeP': {'attributes': {
            'dn': f'uni/infra/nprof-{switchname}-SwitchProfile',
            'status': 'deleted'},'children': []}}]}}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} {json.dumps(payload)} \n {response.content}')
        return(response.content)

    except Exception as e:
        print("Failed to remove from UG")
        print(f"An error occurred: {e}")

def removeleafintprofile(apic_url, token, switchname, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/mo/uni/infra.json'
    payload = {'infraInfra': {'attributes': {'dn': 'uni/infra','status': 'modified'},
    'children': [{'infraAccPortP': {'attributes': {
            'dn': f'uni/infra/accportprof-{switchname}-IntPol',
            'status': 'deleted'},'children': []}}]}}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} {json.dumps(payload)} \n {response.content}')
        return(response.content)

    except Exception as e:
        print("Failed to remove from UG")
        print(f"An error occurred: {e}")

def removevpc(apic_url, token, vpcname, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f'{apic_url}/api/node/mo/uni/fabric/protpol.json'
    payload = {'fabricProtPol': {
    'attributes': {'dn': 'uni/fabric/protpol','status': 'modified'},
      'children': [{'fabricExplicitGEp': {'attributes': {
            'dn': f'uni/fabric/protpol/expgep-{vpcname}',
            'status': 'deleted'},'children': []}}]}}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} {json.dumps(payload)} \n {response.content}')
        return(response.content)

    except Exception as e:
        print("Failed to remove from UG")
        print(f"An error occurred: {e}")

def get_fvRsPathAtt(apic_url, token, nodeid, vlog):
    url = f"{apic_url}/api/node/class/fvRsPathAtt.json?query-target-filter=wcard(fvRsPathAtt.dn,\"paths-{nodeid}\")"
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} \n {response.json()}')
        return response.json()
    except Exception as e:
        print("Failed to get fvRsPathAtt information")
        print(f"An error occurred: {e}")

def get_fvRsPathAtt_prot(apic_url, token, nodeid, vlog):
    url = f"{apic_url}/api/node/class/fvRsPathAtt.json?query-target-filter=wcard(fvRsPathAtt.dn,\"protpaths-{nodeid}\")"
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} \n {response.json()}')
        return response.json()
    except Exception as e:
        print("Failed to get fvRsPathAtt information")
        print(f"An error occurred: {e}")

def parse_tDn(tDn):
    match = re.match(r'topology/pod-(\d+)/(paths|protpaths)-(\d+-?\d*)/pathep-\[([^\]]+)\]', tDn)
    if match:
        pod, path_type, node, interface = match.groups()
        return pod, path_type, node, interface
    return None, None, None, None

def convert_to_list(data):
    result_list = []
    for item in data['imdata']:
        attributes = item['fvRsPathAtt']['attributes']
        dn, encap, mode, tDn, instrImedcy = attributes['dn'], attributes['encap'], attributes['mode'], attributes['tDn'], attributes['instrImedcy']
        dn_parts = re.match(r'uni/tn-(.*?)/ap-(.*?)/epg-(.*?)/rspathAtt-\[.*', dn)
        tenant, app_profile, epg = dn_parts.groups()
        pod, path_type, node, interface = parse_tDn(tDn)
        if pod and path_type and node and interface:
            result_list.append([tenant, app_profile, epg, encap, mode, node, interface, path_type, instrImedcy])
    return result_list

def decom_switch_epg(apic_url, token, tenant, app_profile, epg, node, interface, path_type, vlog):
    headers = {
        'Cookie': f'APIC-cookie={token}',
        'Content-Type': 'application/json'
    }
    url = f"{apic_url}/api/node/mo/uni/tn-{tenant}/ap-{app_profile}/epg-{epg}.json"
    payload = {'fvAEPg': {'attributes': {'dn': f'uni/tn-{tenant}/ap-{app_profile}/epg-{epg}','status': 'modified'},
    'children': [{'fvRsPathAtt': {'attributes': {
    'dn': f'uni/tn-{tenant}/ap-{app_profile}/epg-{epg}/rspathAtt-[topology/pod-1/{path_type}-{node}/pathep-[{interface}]]',
    'status': 'deleted'},'children': []}}]}}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if vlog:
            logging.info(f'{url} {json.dumps(payload)} \n {response.content}')
    except Exception as e:
        print("Failed to decom EPG")
        print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description="Script to decommission ACI switches.")
    parser.add_argument('-i', '--host', help='Specify APIC IP address.')
    parser.add_argument('-u', '--user', help='Specify username.')
    parser.add_argument('-p', '--password', help='Specify password (will prompt if not provided).')
    parser.add_argument('-f', '--file', help='Specify CSV filename')
    parser.add_argument('-v', '--verbose', action='store_true', help='Set verbose logging')
    args = parser.parse_args()
    host = args.host or input("Please Enter the IP Address or Hostname of the APIC > ")
    user = args.user or input("Please Enter Your User ID > ")
    password = args.password or getpass("Please Enter Your Password > ")
    filename = args.file or input("Please Enter CSV filename > ")
    if args.verbose:
        print("Verbose logging enabled")
        vlog = True
    else:
        print("Verbose logging disabled")
        vlog = False
    apic_url = f'https://{host}'
    timestr = time.strftime("%Y%m%d-%H%M%S")
    logging.basicConfig(
        filename=f"{filename}-{timestr}.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )

    with open(filename, mode='r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            nodeid, switchname = row['NodeID'], row['SwitchName']
            try:
                # Get token for each node in case stepping through slow.
                token = get_token(apic_url, user, password)
                vpcname = getvpc(apic_url, token, nodeid, vlog)
                # Found if node is offline the APIC doesn't report switchname so this is commented out
                # switchname = getname(apic_url, token, nodeid, vlog)
                print(f"Node ID: {nodeid}, Switch Name: {switchname}")
                logging.info(f"Node ID: {nodeid}, Switch Name: {switchname}")
                proceed = input(f'Press \'s\' to step through or \'y\' to delete node {nodeid} - {switchname} > ').casefold()
                if proceed == 'y' or proceed == 's':
                    decom_switch1(apic_url, token, nodeid, vlog)
                    print(f"Removed node {nodeid}")
                    logging.info(f"Removed node {nodeid}")
                    if proceed == 's':
                        input(f'Press any key to remove ports for {nodeid} >')
                    int_search = deintsearch(apic_url, token, nodeid, vlog)
                    downint = int_search.decode('utf-8')
                    intdata = json.loads(downint)
                    intdata2 = extract_dns(intdata)
                    port_info = removeinterfaces(intdata2)
                    removedecomports(apic_url, token, port_info, vlog)
                    print(f"Removed ports for {nodeid}")
                    logging.info(f"Removed ports for {nodeid}")
                    if proceed == 's':
                        input(f'Press any key to remove {nodeid} from Upgrade Group >')
                    removeug(apic_url, token, nodeid, vlog)
                    print(f"Removed {nodeid} from Upgrade Group")
                    logging.info(f"Removed {nodeid} from Upgrade Group")
                    if proceed == 's':
                        input(f'Press any key to remove static node address for {nodeid} >')
                    removestaticnodeaddress(apic_url, token, nodeid, vlog)
                    print(f"Removed static node address for {nodeid}")
                    logging.info(f"Removed static node address for {nodeid}")
                    if proceed == 's':
                        input(f'Press any key to remove leaf profile \"{switchname}-SwitchProfile\" for {switchname} >')
                    removeleafprofile(apic_url, token, switchname, vlog)
                    print(f"Removed leaf profile for {switchname}")
                    logging.info(f"Removed leaf profile \"{switchname}-SwitchProfile\" for {switchname}")
                    if proceed == 's':
                        input(f'Press any key to remove \"{switchname}-IntPol\" interface profile for {switchname} >')
                    removeleafintprofile(apic_url, token, switchname, vlog)
                    print(f"Removed leaf interface profile for {switchname}")
                    logging.info(f"Removed leaf interface profile \"{switchname}-IntPol\" for {switchname}")
                    if proceed == 's':
                        input(f'Press any key to remove VPC {vpcname} >')
                    if vpcname != None:
                        removevpc(apic_url, token, vpcname, vlog)
                        print(f"Removed VPC {vpcname}")
                        logging.info(f"Removed VPC {vpcname}")
                    else:
                        print(f"No VPC listed for {nodeid} - {switchname}")
                        logging.info(f"No VPC listed for {nodeid} - {switchname}")
                    if proceed == 's':
                        input(f'Press any key to remove {nodeid} from EPG >')
                    fvRsPathAtt_info = get_fvRsPathAtt(apic_url, token, nodeid, vlog)
                    listtofile = convert_to_list(fvRsPathAtt_info)
                    for x in listtofile:
                        tenant, app_profile, epg, encap, mode, node, interface, path_type, instrImedcy = x
                        decom_switch_epg(apic_url, token, tenant, app_profile, epg, node, interface, path_type, vlog)
                    print(f"Removed {nodeid} from EPG")
                    logging.info(f"Removed {nodeid} from EPG")
                else:
                    print(f'Node {nodeid} - {switchname} not removed.')
                    logging.info(f'Node {nodeid} - {switchname} not removed.')

            except Exception as e:
                print(f"An error occurred: {e}")
                logging.info(f"FAILED - An error occurred: {e}")


if __name__ == "__main__":
    main()
