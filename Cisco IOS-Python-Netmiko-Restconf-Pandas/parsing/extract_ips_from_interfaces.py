import re
from netmiko import ConnectHandler

def main():
    conn = ConnectHandler(ip="10.254.0.1", device_type="cisco_ios", username="cisco", password="cisco", port=22)
    output = conn.send_command("show ip int br")

    lines = output.splitlines()
    regex = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")
    ips = []
    for line in lines:
        m = regex.search(line)
        if m:
            ips.append(m.group(1))
    print(",".join(ips))

if __name__ == "__main__":
    main()
