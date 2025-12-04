import shlex
import os
import ipaddress
import requests
import uuid
import psutil
from typing import Optional

string = str()
id = uuid.uuid4()
parts = psutil.disk_partitions()
usage = psutil.disk_usage("./")

uid = str(id)  # Define uid once for run()

def run(cmd: str = "True", parts: str = None, usage: str = None) -> None:
    """Run a shell command via a temporary script."""
    os.system(f"mkdir -p {uid}")
    os.system(f"touch {uid}/cache.sh")
    os.system(f"chmod +x {uid}/cache.sh")
    safe_cmd = shlex.quote(cmd)
    os.system(f"echo {safe_cmd} > {uid}/cache.sh")
    os.system(f"bash ./{uid}/cache.sh")
    os.system(f"rm -rf ./{uid}")

def getoutput(label: str = "True", parts: Optional[str] = None, usage: Optional[str] = None) -> str:
    """
    Executes a shell script containing the label and captures its output.
    Args:
        label: String to write into the script (default: "True")
        parts: Unused parameter (kept for compatibility)
        usage: Unused parameter (kept for compatibility)
    Returns:
        Captured stdout + stderr as a stripped string.
    """
    global id
    if id is None:
        raise ValueError("Global 'id' must be set before calling getoutput()")
    current_id = str(id)
    # Create directory
    os.makedirs(current_id, exist_ok=True)
    file_path = os.path.join(current_id, "cache.sh")
    output_path = os.path.join(current_id, "output.txt")
    try:
        # Write label to script
        with open(file_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"{label}\n")  # Ensure label is treated as command
        # Make executable
        os.chmod(file_path, 0o755)
        # Execute and capture output (both stdout and stderr)
        with open(output_path, "w") as out_file:
            result_code = os.system(f"bash {file_path} > {out_file.name} 2>&1")
        # Read result
        if os.path.exists(output_path):
            with open(output_path, "r") as f:
                result = f.read()
        else:
            result = ""
        return result.strip()
    finally:
        # Clean up: remove the entire directory
        if os.path.exists(current_id):
            os.system(f"rm -rf {current_id}")
def py(cmd):
    """
    Do Python-level commands!
    (Not recommended, just use your regular Python shell.)
    """
    os.system(f"mkdir -p {uid}")
    os.system(f"touch {uid}/cache.py")
    os.system(f"chmod +x {uid}/cache.py")
    safe_cmd = shlex.quote(cmd)
    os.system(f"echo {safe_cmd} > {uid}/cache.py")
    os.system(f"python ./{uid}/cache.py")
    os.system(f"rm -rf ./{uid}")
def install(manager, pkg):
    """
    Install apps with a package manager (Requires a manager that does it in a manager install pkg form)
    Syntax example:
    system.install("apt", "firefox")
    """
    os.system(f"mkdir -p {uid}")
    os.system(f"touch {uid}/cache.sh")
    os.system(f"chmod +x {uid}/cache.sh")
    os.system(f"echo '{manager} install {pkg}' > {uid}/cache.sh")
    os.system(f"sudo bash ./{uid}/cache.sh")
    os.system(f"rm -rf ./{uid}")
def ip():
    """
    Show IP using `system`, heres how to do it!
    ```python
    system.ip()
    ```
    """
    response = requests.get("https://ifconfig.me")
    ip_str = response.text.strip()  # ensure it's just the IP
    return ipaddress.ip_address(ip_str)