"""Validate and execute all offline notebook cells; heavy optional examples are opt-in."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

for path in sorted(Path("notebooks").glob("*.ipynb")):
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    NotebookClient(notebook, timeout=180, kernel_name="python3",
                   resources={"metadata": {"path": str(Path.cwd())}}).execute()
    print(f"Executed {path}")
