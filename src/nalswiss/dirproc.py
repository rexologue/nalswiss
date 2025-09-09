from __future__ import annotations
import os
import fnmatch
from pathlib import Path
from argparse import ArgumentParser
import chardet

EXT_BLACKLIST = {".ipynb", ".pyc", ".csv", ".pth", ".parquet"}
DIR_BLACKLIST_NAMES = {".git", ".vscode", "__pycache__"}


def detect_encoding(file_path: str) -> str:
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result.get("encoding") or "latin1"


def normalize_path(path: str, root_dir: str) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = Path(root_dir) / p
    return str(p.resolve())


def should_exclude(full_path: str, relative_path: str, root_dir: str, exclude_dirs: list[str], exclude_files: list[str], exclude_patterns: list[str]) -> bool:
    p = Path(full_path)

    # basic dir blacklist by *names* anywhere in the path
    if any(part in DIR_BLACKLIST_NAMES for part in p.parts):
        return True

    # exact path excludes (normalized)
    rel_norm = normalize_path(relative_path, root_dir)
    if p.is_dir() and rel_norm in exclude_dirs:
        return True
    if p.is_file() and rel_norm in exclude_files:
        return True

    # glob/substring patterns against the POSIX path string
    posix_str = p.as_posix()
    for pat in exclude_patterns:
        if pat in posix_str or fnmatch.fnmatch(posix_str, pat):
            return True

    # extensions blacklist for files
    if p.is_file() and p.suffix in EXT_BLACKLIST:
        return True

    return False


def process_directory(root_dir: str, current_dir: str = "", output_file: str | None = None, recursive: bool = True, exclude_dirs: list[str] | None = None, exclude_files: list[str] | None = None, exclude_patterns: list[str] | None = None) -> None:
    exclude_dirs = exclude_dirs or []
    exclude_files = exclude_files or []
    exclude_patterns = exclude_patterns or []

    out = open(output_file, "a", encoding="utf-8") if output_file else None

    base = os.path.join(root_dir, current_dir)
    try:
        items = os.listdir(base)
    except FileNotFoundError:
        print(f"Path not found: {base}")
        if out:
            out.close()
        return

    for item in items:
        full_path = os.path.join(base, item)
        relative_path = os.path.join(current_dir, item)
        p = Path(full_path)

        if should_exclude(full_path, relative_path, root_dir, exclude_dirs, exclude_files, exclude_patterns):
            continue

        if p.is_dir():
            if recursive:
                process_directory(root_dir, relative_path, output_file, recursive, exclude_dirs, exclude_files, exclude_patterns)
        elif p.is_file():
            result = f"File: {relative_path}\n\n"
            try:
                encoding = detect_encoding(full_path)
                with open(full_path, "r", encoding=encoding, errors="replace") as f:
                    content = f.read()
                result += f"Content:\n{content}\n\n"
            except Exception as e:
                result += f"Error reading file {relative_path}: {e}\n\n"

            if out:
                out.write(result)
            else:
                print(result)

    if out:
        out.close()


def cli() -> None:
    parser = ArgumentParser(description="Process a directory and optionally save output to a file.")
    parser.add_argument("root_dir", type=str, help="The root directory to start processing.")
    parser.add_argument("--output-file", type=str, default=None, help="Optional output file to save results.")
    parser.add_argument("-nR", "--non-recursive", action="store_true", help="Disable recursion")
    parser.add_argument("--exclude-dirs", nargs='*', default=[], help="Exact paths (relative to root) to exclude (dirs)")
    parser.add_argument("--exclude-files", nargs='*', default=[], help="Exact paths (relative to root) to exclude (files)")
    parser.add_argument("--exclude-pattern", nargs='*', default=[], help="Exclude if path contains or matches glob pattern(s)")

    args = parser.parse_args()

    root_dir = str(Path(args.root_dir).resolve())
    exclude_dirs = [normalize_path(d, root_dir) for d in args.exclude_dirs]
    exclude_files = [normalize_path(f, root_dir) for f in args.exclude_files]

    process_directory(
        root_dir,
        output_file=args.output_file,
        recursive=not args.non_recursive,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        exclude_patterns=args.exclude_pattern,
    )

