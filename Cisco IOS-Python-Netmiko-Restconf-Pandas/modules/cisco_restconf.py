import requests
import json
requests.packages.urllib3.disable_warnings()

class CiscoRestconf:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.auth = (username, password)
        self.port = str(port)

    def get_request(self, headers, dn):
        url_base = f"https://{self.ip}:{self.port}/restconf"
        uri = url_base + dn
        try:
            r = requests.get(uri, headers=headers, auth=self.auth, verify=False)
            r.raise_for_status()
        except requests.ConnectionError:
            return f"Failed to Connect, check IP and port.\n{url_base}"
        except requests.HTTPError as err:
            return f"HTTP Error raised, see error message.\n{err}"
        else:
            return r

    def get_interface_info(self, data_type="json"):
        dn = "/data/Cisco-IOS-XE-native:native/interface"
        headers = {"Accept": "application/yang-data+" + data_type}
        return self.get_request(headers, dn)

    def get_interface_ips(self, interface_info, data_type="json"):
        if hasattr(interface_info, "json"):
            data = interface_info.json()
        else:
            data = interface_info
        return json.dumps(data, indent=4)

if __name__ == "__main__":
    ip = "10.254.0.1"
    csr = CiscoRestconf(ip, 443, "cisco", "cisco")
    print(csr.get_interface_info())
