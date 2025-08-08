import argparse
import csv
import getpass
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.infra import AccPortP, HPortS, RsAccBaseGrp, NodeP, RsAccPortP
import urllib3
urllib3.disable_warnings()

def copy_children(source_obj, target_obj):
    """
    Recursively copies all child objects from a source object to a target object.

    :param source_obj: The source Managed Object (MO).
    :param target_obj: The target Managed Object (MO).
    """
    for child in source_obj.children:
        child_class = child.__class__
        new_child = child_class(target_obj)
        # Copy properties
        for prop_meta in child.meta.props:
            prop_name = prop_meta.name
            if hasattr(child, prop_name):
                setattr(new_child, prop_name, getattr(child, prop_name))
        # Recursively copy child objects
        copy_children(child, new_child)


def copy_interface_profile(mo_dir, infra, source_profile_name, target_profile_name):
    """
    Copies an Interface Profile and its Interface Selectors.

    :param mo_dir: MoDirectory object for APIC.
    :param infra: The root infra Managed Object.
    :param source_profile_name: Name of the source Interface Profile.
    :param target_profile_name: Name of the target Interface Profile.
    """
    # Get the source Interface Profile
    source_profile_dn = f"uni/infra/accportprof-{source_profile_name}"
    source_profile = mo_dir.lookupByDn(source_profile_dn)

    if not source_profile:
        raise ValueError(f"Source Interface Profile '{source_profile_name}' not found.")

    # Create the target Interface Profile without setting 'name', 'rn', 'type'
    target_profile = AccPortP(infra, target_profile_name)  # APIC automatically handles 'name' and 'rn'
    print(f"Copying Interface Profile: {source_profile_name} to {target_profile_name}")

    # Fetch Interface Selectors directly
    selectors = mo_dir.lookupByClass("infraHPortS", parentDn=source_profile_dn)
    print(f"Found {len(selectors)} Interface Selectors under '{source_profile_name}':")

    for selector in selectors:
        print(f"Copying Interface Selector: {selector.name}")

        # Copy the 'type' from the source selector, it is mandatory to pass it during object creation
        new_selector = HPortS(target_profile, selector.name, type=selector.type)  # Use the 'type' directly

        # Copy properties of HPortS, excluding 'dn', 'rn', 'name', 'type', 'creator', 'modTs', 'extMngdBy', 'lcOwn', 'monPolDn'
        for prop in selector.meta.props:
            prop_name = prop.name
            # Skip createOnly and admin implicit properties (e.g., 'creator', 'modTs', 'extMngdBy', 'lcOwn', 'monPolDn')
            if prop_name not in ['dn', 'rn', 'name', 'type', 'creator', 'modTs', 'extMngdBy', 'lcOwn',
                                 'monPolDn'] and hasattr(selector, prop_name):
                setattr(new_selector, prop_name, getattr(selector, prop_name))

        # Copy children of HPortS (e.g., infra.RsAccBaseGrp)
        for child in selector.children:
            if isinstance(child, RsAccBaseGrp):
                print(f"Copying RsAccBaseGrp for Selector: {selector.name}")
                new_binding = RsAccBaseGrp(new_selector, child.tDn)
                # Copy properties of RsAccBaseGrp
                for prop in child.meta.props:
                    prop_name = prop.name
                    # Skip createOnly and admin implicit properties (e.g., 'creator', 'modTs', 'extMngdBy', 'lcOwn', 'monPolDn')
                    if prop_name not in ['dn', 'rn', 'name', 'type', 'creator', 'modTs', 'extMngdBy', 'lcOwn',
                                         'monPolDn'] and hasattr(child, prop_name):
                        setattr(new_binding, prop_name, getattr(child, prop_name))

    print(f"Interface Profile '{source_profile_name}' successfully copied to '{target_profile_name}'.")


def copy_interface_profile(mo_dir, infra, source_profile_name, target_profile_name):
    """
    Copies an Interface Profile and its Interface Selectors.

    :param mo_dir: MoDirectory object for APIC.
    :param infra: The root infra Managed Object.
    :param source_profile_name: Name of the source Interface Profile.
    :param target_profile_name: Name of the target Interface Profile.
    """
    # Get the source Interface Profile
    source_profile_dn = f"uni/infra/accportprof-{source_profile_name}"
    source_profile = mo_dir.lookupByDn(source_profile_dn)

    if not source_profile:
        raise ValueError(f"Source Interface Profile '{source_profile_name}' not found.")

    # Create the target Interface Profile without setting 'name', 'rn', 'type'
    target_profile = AccPortP(infra, target_profile_name)  # APIC automatically handles 'name' and 'rn'
    print(f"Copying Interface Profile: {source_profile_name} to {target_profile_name}")

    # Fetch Interface Selectors directly
    selectors = mo_dir.lookupByClass("infraHPortS", parentDn=source_profile_dn)
    print(f"Found {len(selectors)} Interface Selectors under '{source_profile_name}':")

    for selector in selectors:
        print(f"Copying Interface Selector: {selector.name}")

        # Copy the 'type' from the source selector, it is mandatory to pass it during object creation
        new_selector = HPortS(target_profile, selector.name, type=selector.type)  # Use the 'type' directly

        # Copy properties of HPortS, excluding 'dn', 'rn', 'name', 'type', 'creator', 'modTs', 'extMngdBy', 'lcOwn', 'monPolDn', 'uid'
        for prop in selector.meta.props:
            prop_name = prop.name
            # Skip createOnly and admin implicit properties (e.g., 'creator', 'modTs', 'extMngdBy', 'lcOwn', 'monPolDn', 'uid')
            if prop_name not in ['dn', 'rn', 'name', 'type', 'creator', 'modTs', 'extMngdBy', 'lcOwn', 'monPolDn',
                                 'uid'] and hasattr(selector, prop_name):
                setattr(new_selector, prop_name, getattr(selector, prop_name))

        # Copy children of HPortS (e.g., infra.RsAccBaseGrp)
        for child in selector.children:
            if isinstance(child, RsAccBaseGrp):
                print(f"Copying RsAccBaseGrp for Selector: {selector.name}")
                new_binding = RsAccBaseGrp(new_selector, child.tDn)
                # Copy properties of RsAccBaseGrp
                for prop in child.meta.props:
                    prop_name = prop.name
                    # Skip createOnly and admin implicit properties (e.g., 'creator', 'modTs', 'extMngdBy', 'lcOwn', 'monPolDn', 'uid')
                    if prop_name not in ['dn', 'rn', 'name', 'type', 'creator', 'modTs', 'extMngdBy', 'lcOwn',
                                         'monPolDn', 'uid'] and hasattr(child, prop_name):
                        setattr(new_binding, prop_name, getattr(child, prop_name))

    print(f"Interface Profile '{source_profile_name}' successfully copied to '{target_profile_name}'.")


def copy_switch_profile(mo_dir, infra, source_switch_name, target_switch_name, target_interface_profile_name):
    """
    Copies a Switch Profile and links it to the target Interface Profile.

    :param mo_dir: MoDirectory object for APIC.
    :param infra: The root infra Managed Object.
    :param source_switch_name: Name of the source Switch Profile.
    :param target_switch_name: Name of the target Switch Profile.
    :param target_interface_profile_name: Name of the target Interface Profile.
    """
    source_switch_dn = f"uni/infra/nprof-{source_switch_name}"
    source_switch = mo_dir.lookupByDn(source_switch_dn)

    if not source_switch:
        raise ValueError(f"Source Switch Profile '{source_switch_name}' not found.")

    target_switch = NodeP(infra, target_switch_name)
    RsAccPortP(target_switch, tDn=f"uni/infra/accportprof-{target_interface_profile_name}")

    copy_children(source_switch, target_switch)

    print(f"Switch Profile '{source_switch_name}' copied to '{target_switch_name}'.")


def main(apic_url, username, password, csv_file):
    """
    Main function to copy profiles based on the CSV input.

    :param apic_url: APIC URL.
    :param username: APIC username.
    :param password: APIC password.
    :param csv_file: Path to the CSV file.
    """
    # Login to APIC
    login_session = LoginSession(apic_url, username, password)
    mo_dir = MoDirectory(login_session)
    mo_dir.login()

    # Lookup Infra MO
    infra = mo_dir.lookupByDn("uni/infra")

    # Read CSV and process
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            source_interface_profile = row['SourceInterfaceProfile']
            target_interface_profile = row['TargetInterfaceProfile']
            source_switch_profile = row['SourceSwitchProfile']
            target_switch_profile = row['TargetSwitchProfile']

            # Step 1: Copy Interface Profile
            copy_interface_profile(
                mo_dir, infra, source_interface_profile, target_interface_profile
            )

            # Step 2: Copy Switch Profile
            copy_switch_profile(
                mo_dir, infra, source_switch_profile, target_switch_profile, target_interface_profile
            )

    # Commit changes
    config_request = ConfigRequest()
    config_request.addMo(infra)
    mo_dir.commit(config_request)

    print("All profiles copied successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy Interface and Switch Profiles in Cisco ACI using Cobra SDK.")
    parser.add_argument("--apic-url", required=True, help="APIC URL (e.g., https://<APIC-IP>)")
    parser.add_argument("--username", required=True, help="APIC username")
    parser.add_argument("--csv-file", required=True, help="Path to the CSV file")
    args = parser.parse_args()

    # Get password securely Imp
    apic_password = getpass.getpass(prompt="Enter APIC password: ")

    # Debugging print statements
    print(f"Arguments: APIC URL={args.apic_url}, Username={args.username}, CSV File={args.csv_file}")
    print(f"Password is captured: {'Yes' if apic_password else 'No'}")

    try:
        main(args.apic_url, args.username, apic_password, args.csv_file)
    except Exception as e:
        print(f"Error while running the script: {e}")