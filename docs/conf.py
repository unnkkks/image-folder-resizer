from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

project = "image-folder-resizer"
author = "Ksenia Martynycheva"
release = "0.1.0"
extensions = [
    "myst_parser",
    "autoapi.extension",
    "sphinx_click",
    "sphinx.ext.napoleon",
]
autoapi_dirs = ["../src/resizer"]
autoapi_options = ["members", "undoc-members", "show-inheritance", "show-module-summary"]
html_theme = "furo"
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
