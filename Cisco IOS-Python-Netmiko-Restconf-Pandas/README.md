# Network Automation Snippets (Netmiko & RESTCONF)

This repo is a collection of small, self-contained Python scripts  
Each script shows off a different pattern or use case — from connecting to Cisco devices with Netmiko,  
to pulling data over RESTCONF, to parsing outputs with regex and pandas.

The goal is to make it easy to learn, copy, and extend these building blocks into your own projects.

---

## 📂 What’s Inside

The repo is organized by theme so you don’t get lost:

- **`netmiko/`** → All the connection basics: loops over IPs, auth retries, dict unpacking, etc.  
- **`parsing/`** → Helpers for cleaning and validating data (IPs, MACs, regex examples).  
- **`restconf/`** → Working RESTCONF calls using `requests`, including JSON and XML examples.  
- **`modules/`** → Reusable classes you can import into your own scripts (CiscoIOS, CiscoRestconf).  
- **`pandas/`** → Examples of reading inventories from CSV and saving structured results.  
- **`cli/`** → Command-line interface example with `argparse`.  
- **`filesystem/`** → Saving device outputs into per-router folders.  
- **`oop/`** → Object-oriented patterns like inheritance.  

Each script is complete and runnable on its own (unless it explicitly imports a helper).

---

## 🔗 How the Pieces Fit Together

Most of the scripts stand alone, but a few lean on helpers:

- **`modules/`**:  
  - `cisco.py`, `cisco_ios_full.py`, `cisco_restconf.py` don’t depend on anything else in this repo — they’re drop-in utilities you can reuse anywhere.  

- **`pandas/pandas_example_router_versions.py`**:  
  - Reads `router_info.csv` and imports `modules/cisco.py` to connect to devices and grab versions.  
  - Creates `hostname_version.csv` as output.  

- **`netmiko/show_ip_int_br_for_loop.py`**:  
  - Uses a small helper `routers.py` (kept in the same folder) to demonstrate looping with imported credentials.  

- **`parsing/mac_formatting_example.py`**:  
  - Calls a local helper `change_mac_notation.py` to reformat MAC addresses.  

- **`restconf/restconf_loop_conn_info.py`**:  
  - Reads device info from `restconf_conn_info.csv` before making API calls.  

Everything else — like the while-loops, auth retries, RESTCONF GETs — is completely self-contained.

---

## Getting Started

Set up your Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
You might also want ntc-templates
if you plan to use use_textfsm=True with Netmiko.

▶️ Running Some Examples
Grab interface status from 3 devices:


python netmiko/show_ip_int_br_loop_int.py
Collect hostname + version from CSV inventory:


python pandas/pandas_example_router_versions.py
RESTCONF JSON call:


python restconf/restconf_get_json.py
Reformat MAC addresses:


python parsing/mac_formatting_example.py


 Notes
Demo IPs are set to 10.254.0.x with cisco/cisco creds — change them for your environment.

Some scripts use TextFSM parsing; you’ll need templates installed if you want structured data.

Be careful: these really will connect to devices if you run them unmodified.

 Where to Start
If you’re just exploring:

Start with basic Netmiko loops (netmiko/show_ip_int_br_list.py).

Check out regex parsing (parsing/extract_ips_from_interfaces.py).

Try CSV + pandas workflows in the pandas/ folder.

Move up to RESTCONF examples for API-style access.

Then dive into the modules/ classes to see how you’d structure real reusable code.

✅ Next Steps
Some ideas to extend this repo:

Add a .env file for credentials and load them with python-dotenv.

Expand CSV inventories into YAML for more flexibility.

Add a Makefile or invoke tasks for “one-liner” demos.

Wrap with pytest tests for the parsing utilities.
