#!/usr/bin/env python3
from distros import distros, print_side_by_side, RST, LBLU, GRE, WHI
import os
import subprocess
from pathlib import Path
import re
import psutil
import shutil

def vga_gpus():
    out = subprocess.check_output(["lspci", "-mm"], text=True).splitlines()
    for line in out:
        if "VGA" not in line:
            continue
        fields = line.split('"')[1::2]
        vendor = re.sub(r"\s*\[.*?\]", "", fields[1])
        yield f"{fields[2]}"

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

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return f"{int(hh)}:{int(mm):02}:{int(ss):02}"


os_release = parse_os_release()

logo = distros[os_release.get("ID", "linux")]

username = os.environ.get("USER", "unknown")
hostname = "unknown"
if Path("/etc/hostname").exists():
    hostname = Path("/etc/hostname").read_text().strip()
username_hostname = f"{LBLU}{username}{WHI}@{LBLU}{hostname}"
user_host_len = len(username) + len(hostname) + 1

arch = subprocess.check_output(["uname", "-m"], text=True).strip() or "unknown_arch"
distro = f"{LBLU}OS{WHI}: {os_release.get("PRETTY_NAME", "Unknown")} {arch}"
kernel_ver = subprocess.check_output(["uname", "-sr"], text=True).strip() or "unknown_kernel"
kernel = f"{LBLU}Kernel{WHI}: {kernel_ver}"

package_texts = []
if shutil.which("pacman"):
    pacman_pkg_count = subprocess.check_output("pacman -Q | wc -l", shell=True, text=True).strip()
    package_texts.append(f"{LBLU}Packages (pacman){WHI}: {pacman_pkg_count}")
if shutil.which("dpkg"):
    output = subprocess.check_output(["dpkg", "-l"], text=True)
    dpkg_count = count = sum(1 for line in output.splitlines() if line.startswith("ii"))
    package_texts.append(f"{LBLU}Packages (dpkg){WHI}: {dpkg_count}")
if shutil.which("flatpak"):
    flatpak_system = subprocess.check_output("flatpak list --system | wc -l", shell=True, text=True).strip()
    flatpak_user = subprocess.check_output("flatpak list --user | wc -l", shell=True, text=True).strip()
    package_texts.append(f"{LBLU}Packages (flatpak system){WHI}: {flatpak_system}")
    package_texts.append(f"{LBLU}Packages (flatpak user){WHI}: {flatpak_user}")

cpu_info = Path("/proc/cpuinfo").read_text().splitlines()
cpu = "Unknown cpu"
for line in cpu_info:
    if line.startswith("model name"):
        cpu = line.replace(":", "").removeprefix("model name").strip()

cpu_text = f"{LBLU}Cpu{WHI}: {cpu}"

gpus = vga_gpus()
gpu_texts = []
for gpu in gpus:
    gpu_texts.append(f"{LBLU}Gpu{WHI}: {gpu}")

ram_info = psutil.virtual_memory()
ram_used = ram_info.used / (1024 ** 3)
ram_total = ram_info.total / (1024 ** 3)
ram = f"{LBLU}Ram{WHI}: {ram_used:.1f} GiB / {ram_total:.1f} GiB"

swap_info = psutil.swap_memory()
swap_used = swap_info.used / (1024 ** 3)
swap_total = swap_info.total / (1024 ** 3)
swap = f"{LBLU}Swap{WHI}: {swap_used:.1f} GiB / {swap_total:.1f} GiB"

disk_info = psutil.disk_usage("/")
disk_used = disk_info.used / (1024 ** 3)
disk_total = disk_info.total / (1024 ** 3)
disk = f"{LBLU}Disk{WHI}: {disk_used:.1f} GiB / {disk_total:.1f} GiB"

network_info = psutil.net_if_addrs()
network_texts = []
for network in network_info.keys():
    if network.startswith("wlan") or network.startswith("enp"):
        network_texts.append(f"{LBLU}Local ({network}){WHI}: {network_info[network][0].address}")

batt = psutil.sensors_battery()
batt_text = ""
if batt:
    status = "Discharging"
    if batt.power_plugged:
        status = "Charging" if batt.percent < 100 else "Fully charged"
    batt_text = f"{LBLU}Battery ({status}){WHI}: {secs2hours(batt.secsleft)} {batt.percent}%"

info = [
    "",    
    "",
    "",
    username_hostname,
    LBLU + "-" * user_host_len,
    distro,
    kernel,
    *package_texts,
    cpu_text,
    *gpu_texts,
    ram,
    swap,
    disk,
    *network_texts,
    batt_text
]

for i in range(25 - len(info)):
    info.append("")

print_side_by_side(logo, info, gap=5)
