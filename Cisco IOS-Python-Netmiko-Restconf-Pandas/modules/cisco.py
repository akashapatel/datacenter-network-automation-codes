from netmiko import ConnectHandler
import pandas as pd
import requests
import json

class CiscoIOS:
    def __init__(self, ip, port=22, username=None, password=None, device_type="cisco_ios"):
        self.conn = ConnectHandler(ip=ip, port=port, username=username, password=password, device_type=device_type)
        self.hostname = self.conn.send_command("show run | include hostname").split()[-1]

    def get_interface_names(self):
        ip_int_br = self.conn.send_command("show ip int br", use_textfsm=True)
        df = pd.DataFrame(ip_int_br)
        return df["intf"].to_list()

    def get_run_cfg(self):
        return self.conn.send_command("show run")

    def get_IOS_version(self):
        rommon = self.conn.send_command("show version | include ROM")
        version = self.conn.send_command("show version | include Version")
        return {"hostname": self.hostname, "rommon": rommon.strip(), "version": version.strip()}

class CiscoRestconf:
    def __init__(self, ip, username, password, port=443):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = str(port)

    def get_interface_info(self, data_type="json"):
        url_base = f"https://{self.ip}:{self.port}"
        dn = "/restconf/data/Cisco-IOS-XE-native:native/interface/"
        headers = {"Accept": "application/yang-data+" + data_type}
        r = requests.get(url_base + dn, headers=headers, auth=(self.username, self.password), verify=False)
        if data_type == "json":
            return r.json()
        return r.content

    def get_interface_ips(self, interface_info, data_type="json"):
        return json.dumps(interface_info, indent=4)
