import argparse
import csv
from getpass import getpass
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import RsPathAtt
import urllib3
import logging
#logging.basicConfig(level=logging.DEBUG)

urllib3.disable_warnings()

# Function to establish a connection to APIC
def connect_to_apic(apic_url, username, password):
    session = LoginSession(apic_url, username, password)
    md = MoDirectory(session)
    md.login()
    return md


# Main function to process the CSV and delete bindings
def remove_epg_bindings(md, csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            tenant = row['tenant']
            app_profile = row['app profile']
            epg_name = row['epg']
            node = row['node']
            port_type = row['port type']
            port = row["port"]
            path= f"topology/pod-1/{port_type}-{node}/pathep-[{port}]"
            print(path)
            # Construct the EPG DN and RsPathAtt DN
            epg_dn = f"uni/tn-{tenant}/ap-{app_profile}/epg-{epg_name}"
            binding_dn = f"{epg_dn}/rspathAtt-[{path}]"

            print(f"Processing: Tenant={tenant}, App Profile={app_profile}, EPG={epg_name}, Path={path}")

            # Lookup the binding directly
            binding = md.lookupByDn(binding_dn)
            if binding:
                print(f"Binding found: {binding.dn}")
                binding.delete()  # Mark for deletion

                # Commit the changes
                config_request = ConfigRequest()
                config_request.addMo(binding)
                md.commit(config_request)
                print(f"Binding {binding.dn} successfully deleted.")
            else:
                print(f"No binding found for {binding_dn}.")


# Argument parser setup
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove EPG bindings to VPCs in Cisco ACI")
    parser.add_argument('-u', '--apic-url', required=True, help='APIC URL (e.g., https://apic.example.com)')
    parser.add_argument('-l', '--username', required=True, help='APIC username')
    parser.add_argument('-c', '--csv-file', required=True, help='Path to the CSV file containing EPG bindings')

    args = parser.parse_args()
    password = getpass("Enter APIC password: ")

    # Connect to APIC and process the CSV file
    try:
        md = connect_to_apic(args.apic_url, args.username, password)
        remove_epg_bindings(md, args.csv_file)
    except Exception as e:
        print(f"Error: {e}")
