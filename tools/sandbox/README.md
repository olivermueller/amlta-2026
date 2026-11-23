# Course Sandbox

Runs untrusted Python code (for example code an LLM wrote in 6.04) on a server, in a **fresh container per request**.

| Protection | How |
|---|---|
| no internet | `--network none` |
| the image cannot be changed | `--read-only`; only `/work` (64 MB, in memory) is writable |
| no root | user `nobody`, all Linux capabilities dropped, `no-new-privileges` |
| limits | 256 MB memory, half a CPU, 64 processes, at most 30 seconds |
| nothing stays | the container is deleted after the run, so even `rm -rf` only destroys the throwaway container |
| access | only with the key (`Authorization: Bearer <SANDBOX_KEY>`) |

## The API

```
POST /run   {"code": "print(2 + 2)", "files": {"shop.db": "<base64>"}, "timeout": 10}
→           {"stdout": "4\n", "stderr": "", "exit_code": 0, "timed_out": false}
GET  /health
```

Files land in `/work`, next to the code (`main.py`). From Python:

```python
import base64, os, requests

def run_in_sandbox(code, files=(), timeout=10):
    payload = {"code": code, "timeout": timeout,
               "files": {os.path.basename(f): base64.b64encode(open(f, "rb").read()).decode() for f in files}}
    response = requests.post(os.environ["SANDBOX_URL"] + "/run", json=payload, timeout=60,
                             headers={"Authorization": "Bearer " + os.environ["SANDBOX_KEY"]})
    response.raise_for_status()
    return response.json()
```

## Deploy with Coolify

1. New resource → Docker Compose, pointing at this folder (`tools/sandbox/docker-compose.yml`).
2. Environment variable `SANDBOX_KEY`: a long random key, for example from `openssl rand -hex 32`.
   Optional: `MAX_PARALLEL` (default 4 containers at the same time).
3. Domain for the service `api`, port `8000` (Coolify writes the Traefik labels; your own labels work as well).
4. Deploy. The service `runner` only builds the image for the code and exits right away; that is expected.

Test: `curl https://<your-domain>/health` gives `{"ok":true}`.

**Good to know**

* The API container gets the Docker socket of the host to start the sandbox containers. The untrusted code never sees it, but whoever controls the API controls Docker on the host: keep the key secret and the API image small.
* Stronger isolation: install [gVisor](https://gvisor.dev/docs/user_guide/install/) on the server and set `SANDBOX_RUNTIME=runsc`. Then the code does not even talk to the kernel of the host directly.
* More packages for the code (pandas, ...): add them in `runner/Dockerfile`.

## Test on your computer

```bash
cd tools/sandbox
SANDBOX_KEY=$(openssl rand -hex 32) docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
# → http://127.0.0.1:8765
```
