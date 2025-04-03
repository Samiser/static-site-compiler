import shutil
from pathlib import Path


def copy_files(source_dir: Path, dest_dir: Path):
    try:
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        print(f"Copied files from {source_dir} to {dest_dir}")
    except FileNotFoundError:
        print(f"Source directory {source_dir} does not exist.")
    except Exception as e:
        print(f"Error copying files: {e}")


def write_index_html(out_path: Path, output: str):
    outfile = out_path / "index.html"

    with outfile.open(mode="w") as f:
        _: int = f.write(output)
        print(f"Blog compiled and written to {outfile}")
