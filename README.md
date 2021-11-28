# Utilization

The `utilization.py` script reports on the utilization of several
resources on a Linux system.

It comes with:

* Crontab entry
* Elasticsearch mapping
* Logrotate entry
* Kibana Dashboard

The cron job writes to /var/log/utilization.log which Logrotate manages and Filebeat ships to Elasticsearch.

Test the script by running it:

```
$ /usr/local/bin/utilization.py
{"@timestamp": "2021-01-03T10:38:53.350801", "utilization.set.name": "system",...
```

## Configuration

Configure Elastic Filebeat to pick up the log:

```
filebeat.inputs:
- type: log
  enabled: true
  json.keys_under_root: true
  json.add_error_key: true
  index: "utilization-%{+yyyy.MM}"
  paths:
    - /var/log/utilization.log
```

Tell logrotate to manage the log:

```
$ cat /etc/logrotate.d/utilization 
/var/log/utilization.log {
  weekly
  rotate 12
  compress
  delaycompress
  missingok
  notifempty
  create 644 ubuntu ubuntu
}
```

Add it to a user's crontab:

```
$ crontab -l
* * * * * /usr/local/bin/utilization.py >> /var/log/utilization.log 2>&1
```

Or the system crontab:

```
$ cat /etc/crontab
* * * * * root /usr/local/bin/utilization.py >> /var/log/utilization.log 2>&1
```

## Example Output

```
{
  "@timestamp": "2021-01-03T10:38:53.350801",
  "utilization.set.name": "system",
  "utilization.bios.vendor": "Google",
  "utilization.bios.version": "Google",
  "utilization.bios.release-date": "01/01/2011",
  "utilization.system.manufacturer": "Google",
  "utilization.system.product-name": "Google Compute Engine",
  "utilization.system.version": "Not Specified",
  "utilization.system.serial-number": "GoogleCloud-EEA4B63CC8AA2E63B76CBB6E240954A1",
  "utilization.system.uuid": "eea4b63c-c8aa-2e63-b76c-bb6e240954a1",
  "utilization.baseboard.manufacturer": "Google",
  "utilization.baseboard.product-name": "Google Compute Engine",
  "utilization.baseboard.version": "Not Specified",
  "utilization.baseboard.serial-number": "Board-GoogleCloud-EEA4B63CC8AA2E63B76CBB6E240954A1",
  "utilization.baseboard.asset-tag": "EEA4B63C-C8AA-2E63-B76C-BB6E240954A1",
  "utilization.chassis.manufacturer": "Google",
  "utilization.chassis.type": "Other",
  "utilization.chassis.version": "Not Specified",
  "utilization.chassis.serial-number": "Not Specified",
  "utilization.chassis.asset-tag": "Not Specified",
  "utilization.processor.family": "Other\nOther\nOther\nOther",
  "utilization.processor.manufacturer": "Google\nGoogle\nGoogle\nGoogle",
  "utilization.processor.version": "Not Specified\nNot Specified\nNot Specified\nNot Specified",
  "utilization.processor.frequency": "2000 MHz\n2000 MHz\n2000 MHz\n2000 MHz",
  "utilization.cpu.architecture": "x86_64",
  "utilization.cpu.op-modes": "32-bit, 64-bit",
  "utilization.cpu.byte-order": "Little Endian",
  "utilization.cpu.vcpus": 4,
  "utilization.cpu.hyperthreaded": true,
  "utilization.cpu.cores-per-socket": 2,
  "utilization.cpu.sockets": 1,
  "utilization.cpu.total-cores": 2,
  "utilization.cpu.vendor-id": "GenuineIntel",
  "utilization.cpu.family": 6,
  "utilization.cpu.model": 63,
  "utilization.cpu.model-name": "Intel(R) Xeon(R) CPU @ 2.30GHz",
  "utilization.cpu.stepping": 0,
  "utilization.cpu.mhz": 2300,
  "utilization.cpu.bogomips": 4600,
  "utilization.cpu.hypervisor-vendor": "KVM",
  "utilization.cpu.virtualization-type": "full",
  "utilization.cpu.flags": [
    "fpu",
    "vme",
    "de",
    "pse",
    "tsc",
    "msr",
    "pae",
    "mce",
    "cx8",
    "apic",
    "sep",
    "mtrr",
    "pge",
    "mca",
    "cmov",
    "pat",
    "pse36",
    "clflush",
    "mmx",
    "fxsr",
    "sse",
    "sse2",
    "ss",
    "ht",
    "syscall",
    "nx",
    "pdpe1gb",
    "rdtscp",
    "lm",
    "constant_tsc",
    "rep_good",
    "nopl",
    "xtopology",
    "nonstop_tsc",
    "cpuid",
    "tsc_known_freq",
    "pni",
    "pclmulqdq",
    "ssse3",
    "fma",
    "cx16",
    "pcid",
    "sse4_1",
    "sse4_2",
    "x2apic",
    "movbe",
    "popcnt",
    "aes",
    "xsave",
    "avx",
    "f16c",
    "rdrand",
    "hypervisor",
    "lahf_lm",
    "abm",
    "invpcid_single",
    "pti",
    "ssbd",
    "ibrs",
    "ibpb",
    "stibp",
    "fsgsbase",
    "tsc_adjust",
    "bmi1",
    "avx2",
    "smep",
    "bmi2",
    "erms",
    "invpcid",
    "xsaveopt",
    "arat",
    "md_clear",
    "arch_capabilities"
  ],
  "utilization.memory.total-kb": [
    16397316
  ],
  "utilization.memory.free-kb": [
    256764
  ],
  "utilization.memory.available-kb": [
    14042636
  ],
  "utilization.memory.cached-kb": [
    13418604
  ],
  "utilization.memory.active-kb": [
    6355800
  ],
  "utilization.memory.inactive-kb": [
    9002108
  ],
  "utilization.memory.swap-total-kb": [
    0
  ],
  "utilization.memory.swap-free-kb": [
    0
  ],
  "utilization.memory.total-gb": [
    16.397
  ],
  "utilization.memory.free-gb": [
    0.257
  ],
  "utilization.memory.available-gb": [
    14.043
  ],
  "utilization.memory.cached-gb": [
    13.419
  ],
  "utilization.memory.active-gb": [
    6.356
  ],
  "utilization.memory.inactive-gb": [
    9.002
  ],
  "utilization.memory.swap-total-gb": [
    0
  ],
  "utilization.memory.swap-free-gb": [
    0
  ],
  "utilization.loadavg.1m": [
    0.18
  ],
  "utilization.loadavg.5m": [
    0.59
  ],
  "utilization.loadavg.15m": [
    0.7
  ],
  "utilization.loadavg.processes.running": [
    1
  ],
  "utilization.loadavg.processes.total": [
    328
  ],
  "utilization.cpu.usr-pct": 0.01,
  "utilization.cpu.nice-pct": 0,
  "utilization.cpu.sys-pct": 0,
  "utilization.cpu.iowait-pct": 0,
  "utilization.cpu.irq-pct": 0,
  "utilization.cpu.soft-pct": 0,
  "utilization.cpu.steal-pct": 0,
  "utilization.cpu.guest-pct": 0,
  "utilization.cpu.gnice-pct": 0,
  "utilization.cpu.idle-pct": 0.98,
  "utilization.summary.cpu-used-pct": [
    0.02
  ],
  "utilization.summary.cpu-free-pct": [
    0.98
  ],
  "utilization.summary.memory-used-pct": [
    0.39
  ],
  "utilization.summary.memory-free-pct": [
    0.61
  ],
  "utilization.summary.system-used-pct": [
    0.21
  ],
  "utilization.summary.system-free-pct": [
    0.79
  ]
}
```
