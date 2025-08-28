from netmiko import ConnectHandler

def main():
    last_octet = 1
    while last_octet <= 3:
        ip = f"10.254.0.{last_octet}"
        conn = ConnectHandler(ip=ip, device_type="cisco_ios", username="cisco", password="cisco")
        hostname = conn.send_command("show run | i hostname")
        print(hostname)
        print("-"*20)
        last_octet += 1

if __name__ == "__main__":
    main()
