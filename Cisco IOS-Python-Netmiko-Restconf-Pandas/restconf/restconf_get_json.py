import requests
requests.packages.urllib3.disable_warnings()

def main():
    dn = "/restconf/data/Cisco-IOS-XE-native:native/interface/"
    headers = {"Accept": "application/yang-data+json"}
    r = requests.get("https://10.254.0.1:443/" + dn, headers=headers, auth=("cisco","cisco"), verify=False)
    print(r.json())

if __name__ == "__main__":
    main()
