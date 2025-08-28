"""Use a connection info dictionary and argument unpacking."""
from netmiko import ConnectHandler

def main():
    csr1kv1 = {
        "ip": "10.254.0.1",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "port": 22,
    }
    conn = ConnectHandler(**csr1kv1)
    print(conn.send_command("show run"))

if __name__ == "__main__":
    main()
