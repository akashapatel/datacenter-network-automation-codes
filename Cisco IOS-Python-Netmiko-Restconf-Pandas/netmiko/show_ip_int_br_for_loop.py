"""Split comma-separated IP string and loop. Also demonstrates helper module."""
from netmiko import ConnectHandler
import routers

def main():
    ip_string = "10.254.0.1,10.254.0.2,10.254.0.3"
    for ip in ip_string.split(","):
        conn = ConnectHandler(ip=ip, username="cisco", password="cisco", device_type="cisco_ios")
        print(conn.send_command("show ip int brief"))
        print("_"*80)

    print("\n--- Alternative using routers module ---")
    for router in routers.creds:
        print(routers.get_ip_int_br(**router))
        print("_"*80)

if __name__ == "__main__":
    main()
