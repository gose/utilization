#!/usr/bin/env python3

import datetime
import json
import subprocess

entry = {}

def addStr(key, cmd):
    val = subprocess.getoutput(cmd).strip()
    if val != '':
        entry[key] = val

def addStrArr(key, cmd):
    val = subprocess.getoutput(cmd).strip()
    if val != '':
        entry[key] = val.split()

def addInt(key, cmd):
    val = subprocess.getoutput(cmd).strip()
    try:
        entry[key] = int(val)
    except:
        return None

def addFlt(key, cmd):
    val = subprocess.getoutput(cmd).strip()
    try:
        entry[key] = round(float(val), 3)
    except:
        return None

# timestamp
entry['@timestamp'] = datetime.datetime.utcnow().isoformat()

# set
entry['utilization.set.name'] = "system"

# power
power = subprocess.getoutput("/usr/local/bin/pyhs100 --ip 192.168.192.3 emeter 2>&1 | grep voltage")
if power != "":
    power = power.replace("'", "\"")
    power = power.replace("0:", "\"0\":")
    power = power.replace("1:", "\"1\":")
    power = power.replace("2:", "\"2\":")
    power = power.replace("3:", "\"3\":")
    power = power.replace("4:", "\"4\":")
    power = power.replace("5:", "\"5\":")
    power_json = json.loads(power)
    entry['utilization.power.volts'] = power_json["3"]["voltage_mv"] / 1000.0
    entry['utilization.power.amps'] = power_json["3"]["current_ma"] / 1000.0
    entry['utilization.power.watts'] = power_json["3"]["power_mw"] / 1000.0

# dmidecode
addStr('utilization.bios.vendor', 'sudo dmidecode -s bios-vendor')
addStr('utilization.bios.version', 'sudo dmidecode -s bios-version')
addStr('utilization.bios.release-date', 'sudo dmidecode -s bios-release-date')
addStr('utilization.system.manufacturer', 'sudo dmidecode -s system-manufacturer')
addStr('utilization.system.product-name', 'sudo dmidecode -s system-product-name')
addStr('utilization.system.version', 'sudo dmidecode -s system-version')
addStr('utilization.system.serial-number', 'sudo dmidecode -s system-serial-number')
addStr('utilization.system.uuid', 'sudo dmidecode -s system-uuid')
addStr('utilization.baseboard.manufacturer', 'sudo dmidecode -s baseboard-manufacturer')
addStr('utilization.baseboard.product-name', 'sudo dmidecode -s baseboard-product-name')
addStr('utilization.baseboard.version', 'sudo dmidecode -s baseboard-version')
addStr('utilization.baseboard.serial-number', 'sudo dmidecode -s baseboard-serial-number')
addStr('utilization.baseboard.asset-tag', 'sudo dmidecode -s baseboard-asset-tag')
addStr('utilization.chassis.manufacturer', 'sudo dmidecode -s chassis-manufacturer')
addStr('utilization.chassis.type', 'sudo dmidecode -s chassis-type')
addStr('utilization.chassis.version', 'sudo dmidecode -s chassis-version')
addStr('utilization.chassis.serial-number', 'sudo dmidecode -s chassis-serial-number')
addStr('utilization.chassis.asset-tag', 'sudo dmidecode -s chassis-asset-tag')
addStr('utilization.processor.family', 'sudo dmidecode -s processor-family')
addStr('utilization.processor.manufacturer', 'sudo dmidecode -s processor-manufacturer')
addStr('utilization.processor.version', 'sudo dmidecode -s processor-version')
addStr('utilization.processor.frequency', 'sudo dmidecode -s processor-frequency')

# lscpu
addStr('utilization.cpu.architecture', "lscpu | grep Arch | awk -F ' +' '{print $2}'")
addStr('utilization.cpu.op-modes', "lscpu | grep op-mode | awk -F '  +' '{print $2}'")
addStr('utilization.cpu.byte-order', "lscpu | grep Byte | awk -F '  +' '{print $2}'")
addInt('utilization.cpu.vcpus', "lscpu | grep ^CPU\(s\): | awk -F '  +' '{print $2}'")
addStr('utilization.cpu.on-line', "lscpu | grep On-line | awk -F '  ' '{print $2}'")
addInt('utilization.cpu.threads-per-core', "lscpu | grep Thread | awk -F '  ' '{print $2}'")

# (custom lscpu entry)
entry['utilization.cpu.hyperthreaded'] = False
tpc = subprocess.getoutput("lscpu | grep Thread | awk -F '  ' '{print $2}'").strip()
if int(tpc) > 1:
    entry['utilization.cpu.hyperthreaded'] = True

cores_per_socket = subprocess.getoutput("lscpu | grep Core\(s\) | awk -F '  +' '{print $2}'")
sockets_per_core = subprocess.getoutput("lscpu | grep Socket | awk -F '  +' '{print $2}'")
entry['utilization.cpu.cores-per-socket'] = int(cores_per_socket)
entry['utilization.cpu.sockets'] = int(sockets_per_core)
entry['utilization.cpu.total-cores'] = int(cores_per_socket) * int(sockets_per_core)

addStr('utilization.cpu.vendor-id', "lscpu | grep 'Vendor' | awk -F '  +' '{print $2}'")
addInt('utilization.cpu.family', "lscpu | grep 'family:' | awk -F '  +' '{print $2}'")
addInt('utilization.cpu.model', "lscpu | grep 'Model:' | awk -F '  +' '{print $2}'")
addStr('utilization.cpu.model-name', "lscpu | grep 'Model name:' | awk -F '  +' '{print $2}'")
addInt('utilization.cpu.stepping', "lscpu | grep 'Stepping:' | awk -F '  +' '{print $2}'")
addFlt('utilization.cpu.mhz', "lscpu | grep 'CPU MHz:' | awk -F '  +' '{print $2}'")
addFlt('utilization.cpu.max-mhz', "lscpu | grep 'CPU max' | awk -F '  +' '{print $2}'")
addFlt('utilization.cpu.min-mhz', "lscpu | grep 'CPU min' | awk -F '  +' '{print $2}'")
addFlt('utilization.cpu.bogomips', "lscpu | grep 'BogoMIPS' | awk -F '  +' '{print $2}'")
addStr('utilization.cpu.virtualization', "lscpu | grep Virtualization: | awk -F '  +' '{print $2}'")
addStr('utilization.cpu.hypervisor-vendor', "lscpu | grep Hypervisor | awk -F '  +' '{print $2}'")
addStr('utilization.cpu.virtualization-type', "lscpu | grep 'lization type:' | awk -F '  +' '{print $2}'")
addInt('utilization.cpu.l1d-cache-kb', "lscpu | awk -F '  +' '/L1d/ {gsub(/K/, "", $2); print $2}'")
addInt('utilization.cpu.l1i-cache-kb', "lscpu | awk -F '  +' '/L1i/ {gsub(/K/, "", $2); print $2}'")
addInt('utilization.cpu.l2-cache-kb', "lscpu | awk -F '  +' '/L2/ {gsub(/K/, "", $2); print $2}'")
addInt('utilization.cpu.l3-cache-kb', "lscpu | awk -F '  +' '/L3/ {gsub(/K/, "", $2); print $2}'")
addStrArr('utilization.cpu.flags', "lscpu | grep Flags: | awk -F '  +' '{print $2}'")

# sensors (from lm-sensors package) example: +32.0°C
# processor 1
sensors = subprocess.getoutput("sensors 2>&1 | grep 'Package id 0:'").strip()
if sensors != "":
    package = subprocess.getoutput("sensors | awk -F '  +' '/^Package id 0:/ {print $2}'")
    package = package.replace('°C', '')
    entry['utilization.temperature.package-id-0-c'] = float(package),
    entry['utilization.temperature.package-id-0-f'] = round(float(package) * 1.8 + 32, 3),
# processor 2
sensors = subprocess.getoutput("sensors 2>&1 | grep 'Package id 1:'").strip()
if sensors != "":
    package = subprocess.getoutput("sensors | awk -F '  +' '/^Package id 1:/ {print $2}'")
    package = package.replace('°C', '')
    entry['utilization.temperature.package-id-1-c'] = float(package),
    entry['utilization.temperature.package-id-1-f'] = round(float(package) * 1.8 + 32, 3),

# cat /proc/meminfo
memory_total_kb = subprocess.getoutput("awk '/^MemTotal:/ {print $2}' /proc/meminfo")
memory_free_kb = subprocess.getoutput("awk '/^MemFree:/ {print $2}' /proc/meminfo")
memory_available_kb = subprocess.getoutput("awk '/^MemAvailable:/ {print $2}' /proc/meminfo")
memory_cached_kb = subprocess.getoutput("awk '/^Cached:/ {print $2}' /proc/meminfo")
memory_active_kb = subprocess.getoutput("awk '/^Active:/ {print $2}' /proc/meminfo")
memory_inactive_kb = subprocess.getoutput("awk '/^Inactive:/ {print $2}' /proc/meminfo")
memory_swap_total_kb = subprocess.getoutput("awk '/^SwapTotal:/ {print $2}' /proc/meminfo")
memory_swap_free_kb = subprocess.getoutput("awk '/^SwapFree:/ {print $2}' /proc/meminfo")

entry["utilization.memory.total-kb"] = int(memory_total_kb),
entry["utilization.memory.free-kb"] = int(memory_free_kb),
entry["utilization.memory.available-kb"] = int(memory_available_kb),
entry["utilization.memory.cached-kb"] = int(memory_cached_kb),
entry["utilization.memory.active-kb"] = int(memory_active_kb),
entry["utilization.memory.inactive-kb"] = int(memory_inactive_kb),
entry["utilization.memory.swap-total-kb"] = int(memory_swap_total_kb),
entry["utilization.memory.swap-free-kb"] = int(memory_swap_free_kb),

entry["utilization.memory.total-gb"] = round(float(memory_total_kb) / 1000 / 1000, 3),
entry["utilization.memory.free-gb"] = round(float(memory_free_kb) / 1000 / 1000, 3),
entry["utilization.memory.available-gb"] = round(float(memory_available_kb) / 1000 / 1000, 3),
entry["utilization.memory.cached-gb"] = round(float(memory_cached_kb) / 1000 / 1000, 3),
entry["utilization.memory.active-gb"] = round(float(memory_active_kb) / 1000 / 1000, 3),
entry["utilization.memory.inactive-gb"] = round(float(memory_inactive_kb) / 1000 / 1000, 3),
entry["utilization.memory.swap-total-gb"] = round(float(memory_swap_total_kb) / 1000 / 1000, 3),
entry["utilization.memory.swap-free-gb"] = round(float(memory_swap_free_kb) / 1000 / 1000, 3),

# cat /proc/loadavg
loadavg = subprocess.getoutput("cat /proc/loadavg").split()
loadavg_1m = loadavg[0]
loadavg_5m = loadavg[1]
loadavg_15m = loadavg[2]
processes_running = loadavg[3].split("/")[0]
processes_total = loadavg[3].split("/")[1]
entry['utilization.loadavg.1m'] = float(loadavg_1m),
entry['utilization.loadavg.5m'] = float(loadavg_5m),
entry['utilization.loadavg.15m'] = float(loadavg_15m),
entry['utilization.loadavg.processes.running'] = int(processes_running),
entry['utilization.loadavg.processes.total'] = int(processes_total),

# mpstat
mpstat = subprocess.getoutput("mpstat | grep all").split()
cpu_usr_pct = round(float(mpstat[3]) / 100, 2)
cpu_nice_pct = round(float(mpstat[4]) / 100, 2)
cpu_sys_pct = round(float(mpstat[5]) / 100, 2)
cpu_iowait_pct = round(float(mpstat[6]) / 100, 2)
cpu_irq_pct = round(float(mpstat[7]) / 100, 2)
cpu_soft_pct = round(float(mpstat[8]) / 100, 2)
cpu_steal_pct = round(float(mpstat[9]) / 100, 2)
cpu_guest_pct = round(float(mpstat[10]) / 100, 2)
cpu_gnice_pct = round(float(mpstat[11]) / 100, 2)
cpu_idle_pct = round(float(mpstat[12]) / 100, 2)
entry['utilization.cpu.usr-pct'] = cpu_usr_pct
entry['utilization.cpu.nice-pct'] = cpu_nice_pct
entry['utilization.cpu.sys-pct'] = cpu_sys_pct
entry['utilization.cpu.iowait-pct'] = cpu_iowait_pct
entry['utilization.cpu.irq-pct'] = cpu_irq_pct
entry['utilization.cpu.soft-pct'] = cpu_soft_pct
entry['utilization.cpu.steal-pct'] = cpu_steal_pct
entry['utilization.cpu.guest-pct'] = cpu_guest_pct
entry['utilization.cpu.gnice-pct'] = cpu_gnice_pct
entry['utilization.cpu.idle-pct'] = cpu_idle_pct

# Summary
cpu_free_pct = cpu_idle_pct
cpu_used_pct = round(1 - cpu_free_pct, 2)
memory_used_pct = round(float(memory_active_kb) / float(memory_total_kb), 2)
memory_free_pct = 1 - memory_used_pct
system_used_pct = round((memory_used_pct + cpu_used_pct) / 2, 2)
system_free_pct = 1 - system_used_pct

entry['utilization.summary.cpu-used-pct'] = cpu_used_pct,
entry['utilization.summary.cpu-free-pct'] = cpu_free_pct,
entry['utilization.summary.memory-used-pct'] = memory_used_pct,
entry['utilization.summary.memory-free-pct'] = memory_free_pct,
entry['utilization.summary.system-used-pct'] = system_used_pct,
entry['utilization.summary.system-free-pct'] = system_free_pct,

print(json.dumps(entry))
