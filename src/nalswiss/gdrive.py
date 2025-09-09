from __future__ import annotations
import argparse
import gdown


def try_download_file(url: str, output: str) -> bool:
    res = gdown.download(url=url, output=output, quiet=False)
    return res is not None


def try_download_folder(file_id: str, output: str) -> bool:
    # use_cookies False -> fewer surprises on headless boxes
    gdown.download_folder(id=file_id, output=output, quiet=False, use_cookies=False)
    return True


def cli() -> None:
    parser = argparse.ArgumentParser(description="Download a Google Drive file or folder by ID.")
    parser.add_argument("-i", "--id", type=str, required=True, help="ID of file/folder on Google Drive")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to save downloaded data")
    parser.add_argument("--force-folder", action="store_true", help="Force folder mode (skip file attempt)")
    args = parser.parse_args()

    if args.force_folder:
        try_download_folder(args.id, args.output)
        return

    url = f"https://drive.google.com/uc?id={args.id}"

    try:
        if not try_download_file(url, args.output):
            print("Not a file, trying as folder...")
            try_download_folder(args.id, args.output)
    except Exception as e:
        print(f"Error: {e}")
