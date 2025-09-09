# nalswiss

Small, portable CLI utilities packaged for easy install on any machine via `pipx` or `uv tool`.

## Installation

### Using pipx from a Release (preferred)
1. Download or copy the direct URL of the wheel from your repo Releases, e.g. `https://your.git.host/you/nalswiss/releases/download/v0.1.0/nalswiss-0.1.0-py3-none-any.whl`.
2. Install (one line):
   
   `pipx install https://your.git.host/you/nalswiss/releases/download/v0.1.0/nalswiss-0.1.0-py3-none-any.whl`

3. (Optional) With integrity pinning (replace HASH):
   
   `pipx install "https://your.git.host/you/nalswiss/releases/download/v0.1.0/nalswiss-0.1.0-py3-none-any.whl#sha256=<HASH>"`

4. Upgrade to a newer release: just run install again with the new wheel URL — pipx will replace the existing installation.
   
   `pipx install https://your.git.host/you/nalswiss/releases/download/v0.1.1/nalswiss-0.1.1-py3-none-any.whl`

> Requires Python 3.10–3.12 available on the system.

#### How to build a wheel locally (for making a Release)
- Build: `poetry build`
- Get SHA256: `sha256sum dist/nalswiss-0.1.0-py3-none-any.whl`
- Upload the wheel (`.whl`) to your Release assets.

---

## Commands

### `treex`
Show a directory tree with excludes.

Examples:
- `treex --path .`
- `treex --path . --exclude __pycache__ .git`
- `treex --path . --exclude-pattern *.egg-info __pycache__`

### `gdrive-dl`
Download a Google Drive file or folder by ID (auto-detects; `--force-folder` to force folder mode).

Examples:
- `gdrive-dl -i 1AbCdEfGhIjKlMn -o ./downloads`
- `gdrive-dl -i 1FolderIdXYZ -o ./my-folder --force-folder`

### `dirproc`
Traverse a directory (recursively by default), concatenating text files into stdout or `--output-file` with encoding auto-detection.

Examples:
- `dirproc ./repo-root --output-file out.txt`
- `dirproc ./repo-root --exclude-dirs data large --exclude-files README.md --exclude-pattern *.csv *.parquet`
- `dirproc ./repo-root -nR`

## Aliases (optional)
- `alias tree='treex'`
- `alias gdl='gdrive-dl'`
- `alias dp='dirproc'`

## License
MIT
