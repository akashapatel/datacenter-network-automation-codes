import requests
requests.packages.urllib3.disable_warnings()

def get_interface_info(to_terminal=False):
    api_root = "https://10.254.0.1:443/restconf"
    dn = "/data/Cisco-IOS-XE-native:native/interface/"
    r = requests.get(api_root + dn, auth=("cisco", "cisco"), verify=False)
    if to_terminal:
        print(r.content.decode("utf-8"))
    else:
        return r.content

if __name__ == "__main__":
    get_interface_info(to_terminal=True)
