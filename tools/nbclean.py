"""Git clean filter for notebooks: strip outputs and local kernel settings before committing.

Reads a notebook from stdin and writes the cleaned notebook to stdout. Your local copy
keeps its outputs; only what git stores is cleaned. Enabled for Sessions 01-03 via
.gitattributes. Activate it once per clone:

    git config filter.nbclean.clean "python3 tools/nbclean.py"
"""
import json
import sys

raw = sys.stdin.read()
try:
    nb = json.loads(raw)
except json.JSONDecodeError:
    sys.stdout.write(raw)  # not valid JSON (e.g., merge conflict): leave untouched
    sys.exit(0)

for cell in nb.get("cells", []):
    if cell.get("cell_type") == "code":
        cell["outputs"] = []
        cell["execution_count"] = None

meta = nb.setdefault("metadata", {})
meta.pop("widgets", None)
meta["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
meta["language_info"] = {"name": "python"}

sys.stdout.write(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
