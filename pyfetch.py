from distros import distros, print_side_by_side
from colorama import Fore, Style
import os
from pathlib import Path

def parse_os_release(path="/etc/os-release"):
    data = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            data[key] = value
    return data

os_release = parse_os_release()

logo = distros[os_release.get("ID", "linux")]

username = os.environ.get("USER", "unknown")
hostname = "unknown"
if Path("/etc/hostname").exists():
    hostname = Path("/etc/hostname").read_text().strip()
username_hostname = f"{Style.RESET_ALL}{username}{Fore.GREEN}@{Style.RESET_ALL}{hostname}"
user_host_len = len(username) + len(hostname) + 1

info = [
    "",    
    "",
    "",
    username_hostname,
    Style.RESET_ALL + "-" * user_host_len,
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",    
]

print_side_by_side(logo, info, gap=5)
