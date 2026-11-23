# Setup with uv (Windows, macOS, Linux)

**In short: install uv, create a virtual environment `.venv` in the repo folder, and select it as the kernel in VS Code.**

[uv](https://docs.astral.sh/uv/) is a fast tool for Python versions, virtual environments, and packages. You prefer conda? Use [SETUP_CONDA.md](SETUP_CONDA.md) instead. You only need one of the two.

| Step | What you do | Once or every time? |
|---|---|---|
| 1 | Install uv | once |
| 2 | Get the course repo | once |
| 3 | Create the virtual environment `.venv` | once |
| 4 | Create the `.env` file with your settings | once |
| 5 | Set up VS Code and select the kernel | once per notebook |

---

## Step 1: Install uv

**macOS and Linux** (Terminal):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows** (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Other ways, for example with Homebrew (`brew install uv`) or WinGet (`winget install --id=astral-sh.uv -e`): [Installing uv](https://docs.astral.sh/uv/getting-started/installation/).

Close the terminal, open a new one, and check:

```bash
uv --version
```

---

## Step 2: Get the course repo

With [Git](https://git-scm.com/downloads):

```bash
git clone https://github.com/olivermueller/amlta-2026.git
cd amlta-2026
```

Without Git: on [github.com/olivermueller/amlta-2026](https://github.com/olivermueller/amlta-2026), click **Code** → **Download ZIP** and unpack it.

---

## Step 3: Create the virtual environment

Inside the `amlta-2026` folder:

```bash
uv venv --seed --python 3.12
```

* This creates the folder `.venv` with its own Python 3.12. No Python 3.12 on your computer? uv downloads it for you ([Python versions in uv](https://docs.astral.sh/uv/concepts/python-versions/)).
* **Don't forget `--seed`.** It puts `pip` into the environment. Without it, the `%pip install` cells in the notebooks fail with `No module named pip` ([uv and Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)).

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate
```

Your prompt now starts with `(amlta-2026)` or `(.venv)`.

**Windows says that running scripts is disabled?** Run this once in PowerShell, then activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Install the basics:

```bash
uv pip install ipykernel jupyter python-dotenv
```

* `ipykernel` lets VS Code and Jupyter use the environment as a **kernel**.
* The notebooks install everything else themselves, with `%pip install` in their first cells.

**Every time you open a new terminal**, activate the environment again. VS Code does this for you once you have selected the kernel (Step 5).

Optional, for Jupyter in the browser: register the environment as a kernel under a readable name.

```bash
python -m ipykernel install --user --name amlta-2026 --display-name "Python 3.12 (amlta-2026)"
```

More: [Using Python environments with uv](https://docs.astral.sh/uv/pip/environments/), [Installing kernels](https://ipython.readthedocs.io/en/stable/install/kernel_install.html).

---

## Step 4: Create the `.env` file

From Session 4 on, `setup_model()` in the notebooks reads its settings from a file called `.env` in the repo folder: where the model runs, keys, addresses, and model names. `.env.example` has one block per provider; the providers are explained in `Session_04/4.03`.

```bash
# macOS / Linux
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
```

Open `.env` and fill in the block of the provider you use (no quotes, no spaces). Ollama needs no key; download the model once in a terminal: `ollama pull qwen3.5:9b` (or `qwen3.5:4b`, `qwen3.5:2b`). For the university's AI-Gateway, see [SETUP_AI_GATEWAY.md](SETUP_AI_GATEWAY.md).

**Never commit or share `.env`.** It is listed in `.gitignore`, so Git ignores it. Background: [python-dotenv](https://pypi.org/project/python-dotenv/).

---

## Step 5: VS Code and the kernel

### Install VS Code and two extensions (once)

1. Install VS Code: [code.visualstudio.com/download](https://code.visualstudio.com/download).
2. Open VS Code, click the **Extensions** icon on the left (or press `Ctrl+Shift+X`, Mac: `Cmd+Shift+X`), and install:

| Extension | What it does |
|---|---|
| [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (Microsoft) | finds the `.venv` in your folder |
| [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) (Microsoft) | opens and runs `.ipynb` notebooks |

### Open the repo and select the kernel

1. **File** → **Open Folder...** → choose the `amlta-2026` folder (the one that contains `.venv`, `Session_01`, `Session_02`, ...). **Open this folder, not a session folder**, otherwise VS Code does not find `.venv`.
2. Open a notebook, for example `Session_04/4.03 - Prompting with the OpenAI-Compatible API.ipynb`.
3. Click **Select Kernel** in the top right corner of the notebook.
4. Choose **Python Environments...** → **.venv** (marked as recommended).
5. Run the first cell with `Shift+Enter`. VS Code asks to install `ipykernel`? Click **Install**.

Check that the notebook uses the right Python:

```python
import sys
print(sys.executable)  # the path should end in .venv/bin/python (Windows: .venv\Scripts\python.exe)
```

**`.venv` is not in the list?**

* Press `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) and run **Developer: Reload Window**.
* Or run **Python: Select Interpreter** → **Enter interpreter path...** and choose `.venv/bin/python` (Windows: `.venv\Scripts\python.exe`).
* Still missing? Choose **Select Another Kernel...** → **Jupyter Kernel...** (works after the optional `ipykernel install` from Step 3).

Official manuals: [Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks), [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments), [Using Jupyter from VS Code with uv](https://docs.astral.sh/uv/guides/integration/jupyter/).

---

## Quick reference

| What | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| activate the environment | `source .venv/bin/activate` | `.venv\Scripts\activate` |
| leave it | `deactivate` | `deactivate` |
| install a package | `uv pip install <package>` | `uv pip install <package>` |
| delete the environment and start over | `rm -rf .venv` | `Remove-Item -Recurse -Force .venv` |
