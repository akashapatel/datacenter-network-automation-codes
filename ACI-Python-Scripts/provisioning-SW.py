import csv
import argparse
import getpass
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.infra import AccPortP, NodeP, RsAccPortP, NodeBlk, RsAccBaseGrp, MaintGrp
from cobra.model.fabric import NodeIdentP, ProtPol, ProtAcc
from cobra.model.fv import Tenant, Ap, AEPg, RsPathAtt
from cobra.model.l3ext import IntersiteNodeP, IntersiteIpP

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Clone ACI Switch Node Configuration")
parser.add_argument("--apic-url", required=True, help="APIC URL (e.g., https://<APIC-IP>)")
parser.add_argument("--username", required=True, help="APIC Username")
parser.add_argument("--csv-file", required=True, help="Path to the configuration CSV file")
args = parser.parse_args()

# Secure password input
password = getpass.getpass(prompt="Enter APIC password: ")

# Login to APIC
login_session = LoginSession(args.apic_url, args.username, password)
mo_dir = MoDirectory(login_session)
mo_dir.login()

# Read the CSV file
with open(args.csv_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        source_node_id = row['SourceNodeID']
        source_switch_name = row['SourceSwitchName']
        new_node_id = row['NewNodeID']
        new_switch_name = row['NewSwitchName']
        maintenance_group = row['MaintenanceGroup']
        management_ip = row['ManagementIP']
        subnet_mask = row['SubnetMask']
        gateway = row['Gateway']
        source_vpc = row['SourceVPC']
        destination_vpc = row['DestinationVPC']
        source_epg = row['SourceEPG']
        destination_epg = row['DestinationEPG']

        infra = mo_dir.lookupByDn("uni/infra")

        # Step 1: Copy Interface Profile
        source_interface_profile_dn = f"uni/infra/accportprof-{source_switch_name}"
        source_interface_profile = mo_dir.lookupByDn(source_interface_profile_dn)
        if source_interface_profile:
            new_interface_profile = AccPortP(infra, new_switch_name)
            for child in source_interface_profile.children:
                if isinstance(child, RsAccBaseGrp):
                    RsAccBaseGrp(new_interface_profile, tDn=child.tDn)

        # Step 2: Copy Switch Profile
        source_switch_profile_dn = f"uni/infra/nprof-{source_switch_name}"
        source_switch_profile = mo_dir.lookupByDn(source_switch_profile_dn)
        if source_switch_profile:
            new_switch_profile = NodeP(infra, new_switch_name)
            NodeBlk(new_switch_profile, f"block-{new_node_id}", from_=new_node_id, to_=new_node_id)
            RsAccPortP(new_switch_profile, tDn=f"uni/infra/accportprof-{new_switch_name}")
            MaintGrp(new_switch_profile, name=maintenance_group)

        # Step 3: Configure Management IP
        fabric_node = NodeIdentP(infra, id=new_node_id, name=new_switch_name)
        intersite_node = IntersiteNodeP(fabric_node, id=new_node_id)
        IntersiteIpP(intersite_node, addr=management_ip, mask=subnet_mask, gw=gateway)

        # Step 4: Setup VPC Pair
        source_vpc_ids = source_vpc.split("-")
        destination_vpc_ids = destination_vpc.split("-")
        vpc_prot_pol = ProtPol(infra, name=f"vpc-{destination_vpc}")
        ProtAcc(vpc_prot_pol, nodeId1=destination_vpc_ids[0], nodeId2=destination_vpc_ids[1])

        # Step 5: Copy EPG Binding
        tenant = mo_dir.lookupByDn("uni/tn-common")  # Adjust tenant as needed
        app_profile = tenant.Aps["default"]         # Adjust application profile as needed
        source_epg_obj = app_profile.aEPgs[source_epg]
        dest_epg_obj = app_profile.aEPgs[destination_epg]
        for binding in source_epg_obj.children:
            if isinstance(binding, RsPathAtt):
                RsPathAtt(dest_epg_obj, tDn=binding.tDn, encap=binding.encap)

        print(f"Processed Source Node: {source_node_id}, New Node: {new_node_id}")

# Commit Changes
config_request = ConfigRequest()
config_request.addMo(infra)
mo_dir.commit(config_request)

print("Configuration applied successfully.")
