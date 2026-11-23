"""Runs inside the throwaway sandbox container: reads the job from stdin, writes the files to /work, runs the code."""
import base64
import json
import os
import subprocess
import sys

job = json.load(sys.stdin)
os.chdir("/work")
for name, content in job.get("files", {}).items():
    with open(name, "wb") as file:
        file.write(base64.b64decode(content))
with open("main.py", "w", encoding="utf-8") as file:
    file.write(job["code"])

timeout = job.get("timeout", 10)
try:
    finished = subprocess.run([sys.executable, "main.py"], stdin=subprocess.DEVNULL, timeout=timeout)
    if finished.returncode < 0:  # stopped by a signal; 9 (SIGKILL) is almost always the memory limit
        signal = -finished.returncode
        print(f"The code was stopped by signal {signal}" + (" (probably the memory limit)." if signal == 9 else "."),
              file=sys.stderr)
        sys.exit(128 + signal)
    sys.exit(finished.returncode)
except subprocess.TimeoutExpired:
    print(f"Timeout: the code ran longer than {timeout} seconds and was stopped.", file=sys.stderr)
    sys.exit(124)
