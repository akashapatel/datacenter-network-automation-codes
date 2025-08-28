import pandas as pd
from modules import cisco

def main():
    df = pd.read_csv("router_info.csv")
    router_list, version_list = [], []
    for _, row in df.iterrows():
        router = cisco.CiscoIOS(row["ip"], username=row["username"], password=row["password"],
                                port=row["port"], device_type=row["device_type"])
        version_data = router.get_IOS_version()
        router_list.append(version_data["hostname"])
        version_list.append(f"{version_data['rommon']} {version_data['version']}")
    out_df = pd.DataFrame({"hostname": router_list, "version": version_list})
    out_df.to_csv("hostname_version.csv", index=False)
    print(out_df)

if __name__ == "__main__":
    main()
