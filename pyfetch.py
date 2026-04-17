#!/usr/bin/env python3
from distros import distros, print_side_by_side, colors, RST
import os
import subprocess
from pathlib import Path
import re
import psutil
import socket
import shutil
import tomllib

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

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

os_release = parse_os_release()

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return f"{int(hh)}h {int(mm):02}m {int(ss):02}s"

def add_colors(module_text):
    result = module_text
    for color in colors.keys():
        result = result.replace(f"${color}$", colors[color])
    return result

def module_len(module_text):
    return len(ansi_escape.sub("", module_text))

def module_empty(module):
    count = module.get("count", "15")
    return ["" for i in range(int(count))]

def module_username_hostname(module): #format="$lightblue$%username%$white$@$lightblue$%hostname%"):
    username = os.environ.get("USER", "unknown")
    hostname = "unknown"
    if Path("/etc/hostname").exists():
        hostname = Path("/etc/hostname").read_text().strip()

    format = module.get("format", "$lightblue$%username%$white$@$lightblue$%hostname%")

    module_text = format.replace("%username%", username).replace("%hostname%", hostname)
    module_text = add_colors(module_text)
    return module_text

def module_divider(module):#format="-", count="15"):
    format = module.get("format", "-")
    count = module.get("count", "15")

    try:
        count_int = int(count)
        return add_colors(format) * count_int
    except ValueError:
        return "Incorrect count for divider"        

def module_os(module): #format="$lightblue$OS$white$: %os% %arch%"):
    format = module.get("format", "$lightblue$OS$white$: %os% %arch%")

    if not os_release:
        return add_colors(format).replace("%os%", "Unknown")

    arch = subprocess.check_output(["uname", "-m"], text="True").strip() or "unknown_arch"

    return add_colors(format).replace("%os%", os_release.get("PRETTY_NAME", "Unknown")).replace("%arch%", arch)

def module_kernel(module):#format="$lightblue$Kernel$white$: %kernel%"):
    format = module.get("format", "$lightblue$Kernel$white$: %kernel%")

    kernel = subprocess.check_output(["uname", "-sr"], text=True).strip() or "unknown_kernel"

    return add_colors(format).replace("%kernel%", kernel)

def module_packages(module):#pkgman="pacman", format="$lightblue$Packages (pacman)$white$: %pkgcount%"):
    pkgman = module.get("pkgman", "pacman")
    format = module.get("format", "$lightblue$Packages (pacman)$white$: %pkgcount%")

    if not shutil.which(pkgman.split("_")[0]):
        return add_colors(format).replace("%pkgcount%", "unknown")

    if pkgman == "pacman":
        #pacman_pkg_count = subprocess.check_output("pacman -Q | wc -l", shell=True, text=True).strip()
        pacman_pkg_count = str(len(list(Path("/var/lib/pacman/local/").iterdir())) - 1)
        return add_colors(format).replace("%pkgcount%", pacman_pkg_count)
    elif pkgman == "dpkg":
        output = subprocess.check_output(["dpkg", "-l"], text=True)
        dpkg_count = count = sum(1 for line in output.splitlines() if line.startswith("ii"))
        return add_colors(format).replace("%pkgcount%", dpkg_count)
    elif pkgman == "flatpak_system":
        #flatpak_system = subprocess.check_output("flatpak list --system | wc -l", shell=True, text=True).strip()
        app = len(list(Path("/var/lib/flatpak/app/").iterdir())) if Path("/var/lib/flatpak/app/").exists() else 0
        runtime = len(list(Path("/var/lib/flatpak/runtime/").iterdir())) if Path("/var/lib/flatpak/runtime/").exists() else 0
        flatpak_system = str(app + runtime)
        return add_colors(format).replace("%pkgcount%", flatpak_system)
    elif pkgman == "flatpak_user":
        #flatpak_user = subprocess.check_output("flatpak list --user | wc -l", shell=True, text=True).strip()        
        app = len(list((Path.home() / Path(".local/share/flatpak/app/")).iterdir())) if (Path.home() / Path(".local/share/flatpak/app/")).exists() else 0
        runtime = len(list((Path.home() / Path(".local/share/flatpak/runtime/")).iterdir())) if (Path.home() / Path(".local/share/flatpak/runtime/")).exists() else 0
        flatpak_user = str(app + runtime)
        return add_colors(format).replace("%pkgcount%", flatpak_user)
    else:
        return add_colors(format).replace("%pkgcount%", "unknown_pkgman")

def module_cpu(module):#format="$lightblue$CPU$white$: %cpu%"):
    format = module.get("format", "$lightblue$CPU$white$: %cpu%")

    cpu_info = Path("/proc/cpuinfo").read_text().splitlines()
    cpu = "Unknown cpu"
    for line in cpu_info:
        if line.startswith("model name"):
            cpu = line.replace(":", "").removeprefix("model name").strip()

    return add_colors(format).replace("%cpu%", cpu)

def module_gpus(module):#format="$lightblue$GPU$white$: %gpu%"):
    format = module.get("format", "$lightblue$GPU$white$: %gpu%")

    gpus = vga_gpus()
    module_texts = []
    for gpu in gpus:
        module_texts.append(add_colors(format).replace("%gpu%", gpu))

    return module_texts

def module_ram(module):#format="$lightblue$RAM$white$: %ram_used% GiB / %ram_total% GiB"):
    format = module.get("format", "$lightblue$RAM$white$: %ram_used% GiB / %ram_total% GiB")

    ram_info = psutil.virtual_memory()
    ram_used = ram_info.used / (1024 ** 3)
    ram_total = ram_info.total / (1024 ** 3)

    return add_colors(format).replace("%ram_used%", f"{ram_used:.1f}").replace("%ram_total%", f"{ram_total:.1f}")

def module_swap(module):#format="$lightblue$Swap$white$: %swap_used% GiB / %swap_total% GiB"):
    format = module.get("format", "$lightblue$Swap$white$: %swap_used% GiB / %swap_total% GiB")

    swap_info = psutil.swap_memory()
    swap_used = swap_info.used / (1024 ** 3)
    swap_total = swap_info.total / (1024 ** 3)

    return add_colors(format).replace("%swap_used%", f"{swap_used:.1f}").replace("%swap_total%", f"{swap_total:.1f}")

def module_disk(module):#root="/", format="$lightblue$Disk$white$: %disk_used% GiB / %disk_total% GiB"):
    root = module.get("root", "/")
    format = module.get("format", "$lightblue$Disk$white$: %disk_used% GiB / %disk_total% GiB")

    disk_info = psutil.disk_usage(root)
    disk_used = disk_info.used / (1024 ** 3)
    disk_total = disk_info.total / (1024 ** 3)

    return add_colors(format).replace("%disk_used%", f"{disk_used:.1f}").replace("%disk_total%", f"{disk_total:.1f}")

def module_network(module):#interface="wlan0", format="$lightblue$Network (%interface%)$white$: %ipv4%"):
    interface = module.get("interface", "wlan0")
    format = module.get("format", "$lightblue$Network (%interface%)$white$: %ipv4%")

    net_info = psutil.net_if_addrs()
    interface_info = net_info.get(interface, None)
    if not interface_info:
        return "No interface named: " + interface

    ipv4 = ""
    ipv6 = ""
    for addr in interface_info:
        if hasattr(addr, "family") and addr.family == socket.AF_INET:
            ipv4 = addr.address
        elif hasattr(addr, "family") and addr.family == socket.AF_INET6:
            ipv6 = addr.address

    return add_colors(format).replace("%ipv4%", ipv4).replace("%ipv6%", ipv6).replace("%interface%", interface)

def module_battery(module):#charging="Charging", discharging="Discharging", fullycharged="Fully Charged", unlimited="Unlimited", format="$lightblue$Battery (%status%)$white$: %left% %percent%%"):
    charging = module.get("charging", "Charging")
    discharging = module.get("discharging", "Discharging")
    fullycharged = module.get("fullycharged", "Fully Charged")
    unlimited = module.get("unlimited", "Unlimited")
    format = module.get("format", "$lightblue$Battery (%status%)$white$: %left% %percent%%")

    battery = psutil.sensors_battery()
    if not battery:
        return "No battery"

    percent = battery.percent
    status = discharging
    if battery.power_plugged:
        status = charging if percent < 100 else fullycharged

    return add_colors(format).replace("%status%", status).replace("%left%", secs2hours(battery.secsleft) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else unlimited).replace("%percent%", f"{percent:.1f}")

def main():
    config = {
        "pyfetch": 
        {
            "logo": "default"
        },
        "info":
        {
            "modules":
            [
                { "type": "empty", "count": 3 },
                { "type": "username_hostname", "format": "$lightblue$%username%$white$@$lightblue$%hostname%" },
                { "type": "divider", "format": "-", "count": "15" },
                { "type": "os", "format": "$lightblue$OS$white$: %os% %arch%" },
                { "type": "kernel", "format": "$lightblue$Kernel$white$ %kernel%" },
                { "type": "packages", "pkgman": "pacman", "format": "$lightblue$Packages (pacman)$white$: %pkgcount%" },
                { "type": "cpu", "format": "$lightblue$CPU$white$: %cpu%" },
                { "type": "gpus", "format": "$lightblue$GPU$white$: %gpu%" },
                { "type": "ram", "format": "$lightblue$RAM$white$: %ram_used% GiB / %ram_total% GiB" },
                { "type": "swap", "format": "$lightblue$Swap$white$: %swap_used% GiB / %swap_total% GiB" },
                { "type": "disk", "root": "/", "format": "$lightblue$Disk$white$: %disk_used% GiB / %disk_total% GiB"},
                { "type": "network", "interface": "wlan0", "format": "$lightblue$Network (%interface%)$white$: %ipv4%" },
                { "type": "battery", "charging": "Charging", "discharging": "Discharging", "fullycharged": "Fully Charged", "unlimited": "Unlimited", "format": "$lightblue$Battery (%status%)$white$: %left% %percent%%" }
            ]
        }
    }

    config_path = Path.home() / Path(".config/pyfetch/config.toml")
    if config_path.exists:
        config = tomllib.loads(config_path.read_text())

    info_modules = []

    if config["pyfetch"]["logo"] == "default":
        logo = distros.get(os_release.get("ID", "linux"), "linux")
    else:
        logo = distros.get(config["pyfetch"]["logo"], "linux")

    for module in config["info"]["modules"]:
        match module["type"]:
            case "empty":
                for empty in module_empty(module):
                    info_modules.append(empty)
            case "username_hostname":
                info_modules.append(module_username_hostname(module))
            case "divider":
                info_modules.append(module_divider(module))
            case "os":
                info_modules.append(module_os(module))
            case "kernel":
                info_modules.append(module_kernel(module))
            case "packages":
                info_modules.append(module_packages(module))
            case "cpu":
                info_modules.append(module_cpu(module))
            case "gpus":
                for gpu in module_gpus(module):
                    info_modules.append(gpu)
            case "ram":
                info_modules.append(module_ram(module))
            case "swap":
                info_modules.append(module_swap(module))
            case "disk":
                info_modules.append(module_disk(module))
            case "network":
                info_modules.append(module_network(module))
            case "battery":
                info_modules.append(module_battery(module))

    if len(info_modules) < 25:
        for empty in module_empty({"type": "empty", "count": str(25 - len(info_modules))}):
            info_modules.append(empty)

    print_side_by_side(logo, info_modules, gap=5)

if __name__ == "__main__":
    main()
