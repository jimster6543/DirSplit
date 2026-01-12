import os
import sys
import shutil
from pathlib import Path

def split_directory(folder_path, files_per_folder):
    folder_path = Path(folder_path)

    if not folder_path.is_dir():
        print(f"[SKIP] Not a directory: {folder_path}")
        return

    files = [f for f in folder_path.iterdir() if f.is_file()]

    if not files:
        print(f"[INFO] No files in {folder_path}")
        return

    files.sort(key=lambda x: x.name.lower())

    digits = len(str((len(files) - 1) // files_per_folder + 1))

    for index, file in enumerate(files):
        folder_index = index // files_per_folder + 1
        subfolder_name = str(folder_index).zfill(digits)
        target_dir = folder_path / subfolder_name
        target_dir.mkdir(exist_ok=True)

        shutil.move(str(file), target_dir / file.name)

    print(f"[DONE] {folder_path} → {files_per_folder} files per folder")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python dirsplit.py <folder> <files_per_folder>")
        print("  python dirsplit.py <textfile>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    files_per_folder = None
    if len(sys.argv) >= 3:
        files_per_folder = int(sys.argv[2])

    if files_per_folder is not None and files_per_folder <= 0:
        print("Files per folder must be greater than zero.")
        sys.exit(1)

    if input_path.is_file():
        with open(input_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            try:
                folder, per_folder = line.rsplit("|", 1)
                split_directory(folder.strip(), int(per_folder))
            except ValueError:
                print(f"[SKIP] Invalid line format: {line}")
    else:
        split_directory(input_path, files_per_folder)


if __name__ == "__main__":
    main()
