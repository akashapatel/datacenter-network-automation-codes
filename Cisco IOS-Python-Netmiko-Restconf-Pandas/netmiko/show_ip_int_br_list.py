"""Use a list of IPs and aggregate results."""
from netmiko import ConnectHandler

USERNAME = "cisco"
PASSWORD = "cisco"
DEVICE_TYPE = "cisco_ios"
PORT = 22
IP_LIST = ["10.254.0.1", "10.254.0.2", "10.254.0.3"]

def main():
    results = []
    for ip in IP_LIST:
        conn = ConnectHandler(ip=ip, device_type=DEVICE_TYPE,
                              username=USERNAME, password=PASSWORD, port=PORT)
        results.append(conn.send_command("show ip interface brief"))
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
