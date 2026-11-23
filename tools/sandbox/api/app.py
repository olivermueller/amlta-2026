"""Course sandbox: runs untrusted Python code (for example code an LLM wrote) in a fresh container per request.

POST /run  {"code": "...", "files": {"shop.db": "<base64>"}, "timeout": 10}
           with the header  Authorization: Bearer <SANDBOX_KEY>
returns    {"stdout": "...", "stderr": "...", "exit_code": 0, "timed_out": false}

Every run gets its own container: no network, read-only file system, a small writable /work (in memory),
limits for memory, CPU, processes and time, an unprivileged user, and no Linux capabilities.
The container is deleted after the run, so even `rm -rf` only destroys the throwaway container.
"""
import base64
import binascii
import hmac
import json
import os
import re
import subprocess
import threading
import uuid

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

SANDBOX_KEY = os.environ.get("SANDBOX_KEY", "")
RUNNER_IMAGE = os.getenv("RUNNER_IMAGE", "course-sandbox-runner:latest")
SANDBOX_RUNTIME = os.getenv("SANDBOX_RUNTIME", "")  # optional, e.g. "runsc" for gVisor (stronger isolation)
MAX_PARALLEL = int(os.getenv("MAX_PARALLEL", "4"))  # containers at the same time; the others wait
MEMORY = os.getenv("SANDBOX_MEMORY", "256m")
CPUS = os.getenv("SANDBOX_CPUS", "0.5")
MAX_TIMEOUT = 30  # seconds
MAX_FILES_BYTES = 5 * 1024 * 1024
MAX_OUTPUT = 20_000  # characters of stdout and of stderr
FILE_NAME = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")  # no folders, no "..": files land in /work only

if len(SANDBOX_KEY) < 16:
    raise RuntimeError("Set SANDBOX_KEY (at least 16 characters).")

slots = threading.BoundedSemaphore(MAX_PARALLEL)
app = FastAPI(title="Course sandbox")


class RunRequest(BaseModel):
    code: str = Field(max_length=100_000)
    files: dict[str, str] = Field(default_factory=dict, description="file name -> content in base64; lands in /work")
    timeout: int = Field(10, ge=1, le=MAX_TIMEOUT)


class RunResult(BaseModel):
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool


def check_key(authorization):
    if not hmac.compare_digest(authorization.encode(), f"Bearer {SANDBOX_KEY}".encode()):
        raise HTTPException(status_code=401, detail="wrong or missing key")


def check_files(files):
    size = 0
    for name, content in files.items():
        if not FILE_NAME.match(name) or name in (".", "..", "main.py"):
            raise HTTPException(status_code=400, detail=f"file name not allowed: {name!r}")
        try:
            size += len(base64.b64decode(content, validate=True))
        except (binascii.Error, ValueError):
            raise HTTPException(status_code=400, detail=f"file {name!r} is not valid base64")
    if size > MAX_FILES_BYTES:
        raise HTTPException(status_code=400, detail="files too large (5 MB at most)")


def docker_command(name):
    command = [
        "docker", "run", "--rm", "-i", "--name", name,
        "--network", "none",  # no internet, no other containers
        "--read-only",  # the image cannot be changed ...
        "--tmpfs", "/work:rw,nosuid,nodev,size=64m,mode=1777",  # ... only /work, in memory
        "--tmpfs", "/tmp:rw,nosuid,nodev,size=16m,mode=1777",
        "--memory", MEMORY, "--memory-swap", MEMORY,
        "--cpus", CPUS,
        "--pids-limit", "64",  # no fork bombs
        "--user", "65534:65534",  # nobody
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
    ]
    if SANDBOX_RUNTIME:
        command += ["--runtime", SANDBOX_RUNTIME]
    return command + [RUNNER_IMAGE]


def cut(data):
    text = (data or b"").decode("utf-8", errors="replace")
    return text if len(text) <= MAX_OUTPUT else text[:MAX_OUTPUT] + f"\n... ({len(text) - MAX_OUTPUT} more characters)"


def execute(request):
    name = f"sandbox-{uuid.uuid4().hex[:12]}"
    job = json.dumps({"code": request.code, "files": request.files, "timeout": request.timeout}).encode()
    try:
        # the runner stops the code after `timeout` seconds; the extra seconds are for starting the container
        done = subprocess.run(docker_command(name), input=job, capture_output=True, timeout=request.timeout + 15)
    except subprocess.TimeoutExpired as expired:
        subprocess.run(["docker", "kill", name], capture_output=True)
        return RunResult(stdout=cut(expired.stdout), stderr=cut(expired.stderr), exit_code=None, timed_out=True)
    return RunResult(stdout=cut(done.stdout), stderr=cut(done.stderr), exit_code=done.returncode,
                     timed_out=done.returncode == 124)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/run", response_model=RunResult)
def run(request: RunRequest, authorization: str = Header(default="")):
    check_key(authorization)
    check_files(request.files)
    if not slots.acquire(timeout=60):
        raise HTTPException(status_code=503, detail="the sandbox is busy, try again in a moment")
    try:
        return execute(request)
    finally:
        slots.release()
