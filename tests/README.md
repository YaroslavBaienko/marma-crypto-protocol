# Production test suite — environment notes

Run with the project venv and **without** prepending an older dist-packages path:

```
~/.venvs/knowledge-os/bin/python -m pytest tests -q
```

The suite requires:
- `pymupdf >= 1.28.2` — text extraction changed between 1.25.x and 1.28.x; the sealed
  whitepapers were canonicalised with 1.28.x, so an older PyMuPDF makes the PAdES whitepaper
  audit fail with a false "document text was modified" verdict;
- `numpy`, `pycairo`, `python-docx`, `pypdf`, `pytest` (see `requirements-dev.txt`).

Do **not** run with `PYTHONPATH=/usr/lib/python3/dist-packages` prepended: it shadows the
venv's PyMuPDF with the older system copy and reproduces the false PAdES failure. If system
packages are needed in the venv, add them as a fallback path in a `.pth` file instead
(appended after site-packages, so venv packages win).

Expected: `40 passed`.
