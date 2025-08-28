import requests
import pandas as pd
requests.packages.urllib3.disable_warnings()

def main():
    dash = "-" * 80
    conn_info = pd.read_csv("restconf_conn_info.csv")
    for _, row in conn_info.iterrows():
        ip = row["ip"]
        username = row["username"]
        password = row["password"]
        uri = f"https://{ip}:443/restconf/"
        r = requests.get(uri, auth=(username, password), verify=False)
        print(r.content)
        print(dash)

if __name__ == "__main__":
    main()
