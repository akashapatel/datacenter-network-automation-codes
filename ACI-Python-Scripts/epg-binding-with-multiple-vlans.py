import argparse
import csv
from getpass import getpass
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant, Ap, AEPg
from cobra.model.infra import RsPathAtt

def bind_epgs_to_vpc(apic_url, username, csv_file):
    # Get the password securely
    password = getpass("Enter APIC password: ")

    # Login to APIC
    session = LoginSession(apic_url, username, password)
    md = MoDirectory(session)
    md.login()

    try:
        # Read the CSV file
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            bindings = [row for row in reader if row]  # Skip empty rows

        if not bindings:
            print("No data found in the CSV file.")
            return

        for row in bindings:
            if len(row) < 4:
                print(f"Invalid row format: {row}. Expected: tenant, app_profile, epg, interface_path")
                continue

            tenant_name, app_profile_name, epg_name, path = map(str.strip, row)

            # Locate tenant, application profile, and EPG
            tenant_dn = f"uni/tn-{tenant_name}"
            tenant = md.lookupByDn(tenant_dn)
            if not tenant:
                print(f"Tenant {tenant_name} not found.")
                continue

            app_profile = md.lookupByDn(f"{tenant_dn}/ap-{app_profile_name}")
            if not app_profile:
                print(f"Application Profile {app_profile_name} not found under Tenant {tenant_name}.")
                continue

            epg = md.lookupByDn(f"{tenant_dn}/ap-{app_profile_name}/epg-{epg_name}")
            if not epg:
                print(f"EPG {epg_name} not found under Application Profile {app_profile_name}.")
                continue

            # Bind EPG to the VPC interface path
            rs_path = RsPathAtt(epg, tDn=path, encap="unknown")  # Encapsulation is optional if not specific
            print(f"Binding EPG {epg_name} to VPC {path} in Tenant {tenant_name}, Application Profile {app_profile_name}.")

        # Commit the configuration
        config_request = ConfigRequest()
        config_request.addMo(tenant)
        md.commit(config_request)

        print("EPGs successfully bound to VPC interfaces.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        md.logout()

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Bind multiple EPGs to a VPC in Cisco ACI using the Cobra SDK.")
    parser.add_argument("--apic", required=True, help="APIC URL (e.g., https://<APIC_IP>)")
    parser.add_argument("--username", required=True, help="APIC username")
    parser.add_argument("--csv", required=True, help="Path to CSV file with binding details")

    args = parser.parse_args()

    # Call the function with parsed arguments
    bind_epgs_to_vpc(
        apic_url=args.apic,
        username=args.username,
        csv_file=args.csv,
    )
