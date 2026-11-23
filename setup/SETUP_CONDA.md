# Setup with conda (Windows, macOS, Linux)

**In short: install conda, create one environment for the course, and select it as the kernel in VS Code.**

You prefer `uv`? Use [SETUP_UV.md](SETUP_UV.md) instead. You only need one of the two.

| Step | What you do | Once or every time? |
|---|---|---|
| 1 | Install conda | once |
| 2 | Get the course repo | once |
| 3 | Create the environment `amlta-2026` | once |
| 4 | Create the `.env` file with your settings | once |
| 5 | Set up VS Code and select the kernel | once per notebook |

---

## Step 1: Install conda

| System | What to install | Official manual |
|---|---|---|
| Windows | **Anaconda Distribution** (graphical installer) | [Windows installer for Anaconda Distribution](https://www.anaconda.com/docs/getting-started/anaconda/install/windows-gui-install) |
| macOS | **Miniconda** (terminal installer) | [macOS terminal installer for Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install/mac-cli-install) |
| Linux | **Miniconda** | [Linux installer for Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install) |

Not sure which one fits? See the overview: [Installing Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) and [Installing Anaconda Distribution](https://www.anaconda.com/docs/getting-started/anaconda/install).

### Windows

1. Download the installer from [anaconda.com/download](https://www.anaconda.com/download).
2. Run the `.exe` file and keep the default settings ("Just Me").
3. Open **Anaconda Prompt** from the Start menu. All `conda` commands below go there.

Prefer the smaller Miniconda on Windows? That works the same: [Windows installer for Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install/windows-gui-install).

### macOS

Open the **Terminal** and run:

```bash
# Apple Silicon (M1, M2, ...)
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash ~/Miniconda3-latest-MacOSX-arm64.sh

# older Macs with an Intel processor instead:
# curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
# bash ~/Miniconda3-latest-MacOSX-x86_64.sh
```

* Answer `yes` to the license and to the question whether conda should be initialized.
* Then close the Terminal and open a new one (or run `source ~/.zshrc`).

### Linux

```bash
# x86_64 (most computers)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ~/Miniconda3-latest-Linux-x86_64.sh

# ARM computers instead:
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
# bash ~/Miniconda3-latest-Linux-aarch64.sh
```

* Answer `yes` to the license and to the question whether conda should be initialized.
* Then close the terminal and open a new one (or run `source ~/.bashrc`).

### Check

```bash
conda --version
```

You see a version number? Good. You see `conda: command not found`? Open a new terminal. Still not found? See the troubleshooting section at the end of the [macOS](https://www.anaconda.com/docs/getting-started/miniconda/install/mac-cli-install) or [Linux](https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install) manual.

---

## Step 2: Get the course repo

With [Git](https://git-scm.com/downloads):

```bash
git clone https://github.com/olivermueller/amlta-2026.git
cd amlta-2026
```

Without Git: on [github.com/olivermueller/amlta-2026](https://github.com/olivermueller/amlta-2026), click **Code** → **Download ZIP** and unpack it.

---

## Step 3: Create the environment

```bash
conda create -n amlta-2026 python=3.12
conda activate amlta-2026
pip install ipykernel jupyter python-dotenv
```

* `conda create` makes a separate Python 3.12 just for this course. Your other projects stay untouched.
* `conda activate` switches to it. Your prompt now starts with `(amlta-2026)`.
* `ipykernel` lets VS Code and Jupyter use the environment as a **kernel**.
* The notebooks install everything else themselves, with `%pip install` in their first cells.

**conda asks you to accept the Terms of Service?** Since 2025, conda asks once per channel before it uses Anaconda's default channels. Read the question and answer it. Details: [Managing Terms of Service on the command line](https://www.anaconda.com/docs/getting-started/tos-plugin).

**Every time you open a new terminal**, run `conda activate amlta-2026` again. VS Code does this for you once you have selected the kernel (Step 5).

Optional, for Jupyter in the browser: register the environment as a kernel under a readable name.

```bash
python -m ipykernel install --user --name amlta-2026 --display-name "Python 3.12 (amlta-2026)"
```

More commands: [Managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), [conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html), [Installing kernels](https://ipython.readthedocs.io/en/stable/install/kernel_install.html).

---

## Step 4: Create the `.env` file

From Session 4 on, `setup_model()` in the notebooks reads its settings from a file called `.env` in the repo folder: where the model runs, keys, addresses, and model names. `.env.example` has one block per provider; the providers are explained in `Session_04/4.03`.

```bash
# macOS / Linux
cp .env.example .env

# Windows (Anaconda Prompt)
copy .env.example .env
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
| [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (Microsoft) | finds your conda environments |
| [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) (Microsoft) | opens and runs `.ipynb` notebooks |

### Open the repo and select the kernel

1. **File** → **Open Folder...** → choose the `amlta-2026` folder (the one that contains `Session_01`, `Session_02`, ...).
2. Open a notebook, for example `Session_04/4.03 - Prompting with the OpenAI-Compatible API.ipynb`.
3. Click **Select Kernel** in the top right corner of the notebook.
4. Choose **Python Environments...** → **amlta-2026**.
5. Run the first cell with `Shift+Enter`. VS Code asks to install `ipykernel`? Click **Install**.

Check that the notebook uses the right Python:

```python
import sys
print(sys.executable)  # the path should contain "amlta-2026"
```

**`amlta-2026` is not in the list?**

* Press `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) and run **Developer: Reload Window**.
* Or run **Python: Select Interpreter** and pick `amlta-2026` there first.
* Still missing? Choose **Select Another Kernel...** → **Jupyter Kernel...** (works after the optional `ipykernel install` from Step 3).

Official manuals: [Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks), [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments), [Getting started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial).

---

## Quick reference

| What | Command |
|---|---|
| activate the environment | `conda activate amlta-2026` |
| leave it | `conda deactivate` |
| list all environments | `conda env list` |
| install a package | `pip install <package>` (inside the activated environment) |
| delete the environment and start over | `conda remove -n amlta-2026 --all` |
