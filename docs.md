# `system` Module Documentation

The `system` module provides a set of utility functions for interacting with the operating system, executing shell commands securely, retrieving system information, and performing package installations. It is designed for temporary, isolated command execution with automatic cleanup.

---

## Overview

```python
import shlex
import os
import ipaddress
import requests
import uuid
import psutil
from typing import Optional
```

**Global Variables:**
- `string = str()` – Empty string type alias (unused in core logic).
- `id = uuid.uuid4()` – Unique identifier for the current session/run.
- `parts = psutil.disk_partitions()` – List of mounted disk partitions.
- `usage = psutil.disk_usage("./")` – Disk usage statistics for current directory.
- `uid = str(id)` – String version of the UUID used as a unique temporary directory name.

---

## Functions

### `run(cmd: str = "True", parts: str = None, usage: str = None) -> None`

**Purpose:** Execute a shell command via a temporary bash script with full isolation and cleanup.

**Parameters:**
- `cmd` (str): Shell command to execute. Default: `"True"` (no-op).
- `parts`, `usage` (str): Legacy parameters (ignored).

**Behavior:**
1. Creates a unique directory: `./{uid}/`
2. Writes the command into `cache.sh`
3. Makes it executable
4. Runs the script
5. Deletes the entire directory afterward

**Example:**
```python
run("ls -la")
run("echo 'Hello World!'")
```

> **Security Note:** Uses `shlex.quote()` to prevent injection when writing commands.

---

### `getoutput(label: str = "True", parts: Optional[str] = None, usage: Optional[str] = None) -> str`

**Purpose:** Execute a shell command and **capture both stdout and stderr** as a string.

**Returns:** `str` – Combined output, stripped of whitespace.

**Raises:**
- `ValueError` if global `id` is `None`

**Process:**
1. Ensures unique directory exists
2. Writes `label` as a bash script
3. Executes and redirects all output to `output.txt`
4. Reads and returns the result
5. Cleans up everything

**Example:**
```python
output = getoutput("uname -a")
print(output)  # e.g., "Linux hostname 5.15.0-56-generic ..."

output = getoutput("pwd && ls")
```

> Ideal for capturing command results programmatically.

---

### `py(cmd: str)`

**Purpose:** Execute **Python code** via a temporary `.py` file.

> **Warning:** Not recommended — use direct Python execution instead.

**Behavior:** Same lifecycle as `run()`, but writes to `cache.py` and runs with `python`.

**Example:**
```python
py("print('Hello from temp Python!')")
py("import sys; print(sys.version)")
```

---

### `install(manager: str, pkg: str)`

**Purpose:** Install a package using a system package manager **with `sudo`**.

**Supported Syntax:** `manager install pkg`

**Examples:**
```python
install("apt", "vim")        # Debian/Ubuntu
install("yum", "htop")       # CentOS/RHEL
install("pacman", "-S", "neofetch")  # Arch (note: may need adjustment)
```

> **Requires `sudo` privileges without password prompt.**

**Security Warning:** High privilege escalation risk.

---

### `ip() -> ipaddress.ip_address`

**Purpose:** Retrieve your **public IP address** using `https://ifconfig.me`

**Returns:** `ipaddress.IPv4Address` or `IPv6Address` object

**Example:**
```python
public_ip = ip()
print(public_ip)                    # 203.0.113.42
print(type(public_ip))              # <class 'ipaddress.IPv4Address'>
print(public_ip.version)            # 4
```

> Uses `requests.get()` — requires internet access.

---

## Global State & Lifecycle

- Each module load generates a **new UUID** (`id`, `uid`)
- All functions use the **same `uid`** for isolation
- Temporary directories: `./{uid}/`
- All files and directories are **deleted after use**

---

## Best Practices & Warnings

| Practice | Recommendation |
|--------|----------------|
| **Command Injection** | Always let `run()`/`getoutput()` handle quoting via `shlex.quote()` |
| **Privilege Escalation** | `install()` uses `sudo` — only use in trusted environments |
| **Error Handling** | Wrap calls in `try/except` — `getoutput()` may return empty on failure |
| **Performance** | Avoid in loops — filesystem overhead per call |
| **Python Execution** | Prefer native Python over `py()` |

---

## Example Usage

```python
# Show system info
print(getoutput("hostname"))
print(getoutput("df -h"))

# Get public IP
print(f"Your IP: {ip()}")

# List partitions
for p in parts:
    print(p.device, p.mountpoint)

# Install a tool (requires sudo)
# install("apt", "curl")

# Run one-off command
run("touch hello.txt")
```

---

## Dependencies

```bash
pip install psutil requests
```

Or via system:
```python
install("apt", "python3-psutil, python3-requests")
```

---

## Version

- **Author:** Custom Utility Module
- **Python:** 3.6+
- **Status:** Functional, not for production without review

---

> **Use Responsibly** — This module executes arbitrary system commands and uses `sudo` (for some commands).

--- 

**Module Name:** `system`  
**Namespace-safe UUID isolation**  
**Zero persistent state**