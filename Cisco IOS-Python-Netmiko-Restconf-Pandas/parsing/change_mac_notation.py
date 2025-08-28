import re

def change_notation(mac: str, sep: str = ":") -> str:
    mac = mac.lower().replace(".", "")
    mac = re.sub(r"[^0-9a-f]", "", mac)
    if len(mac) != 12:
        raise ValueError("MAC should have 12 hex digits after cleaning")
    return sep.join(mac[i:i+2] for i in range(0,12,2))
