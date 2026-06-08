#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
INCLUDE = [
    'lpg_project',
    'requirements.txt',
    '.env.example',
    '.gitignore',
    'README-lpg.md',
]
EXCLUDE_DIRS = {'.venv', '__pycache__', 'staticfiles', '.git'}
EXCLUDE_FILES = {'db.sqlite3'}


def should_exclude(path: Path) -> bool:
    if path.name in EXCLUDE_DIRS or path.name in EXCLUDE_FILES:
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def add_path_to_zip(zip_file: ZipFile, src: Path, base: Path):
    if should_exclude(src):
        return
    if src.is_dir():
        for child in sorted(src.iterdir()):
            add_path_to_zip(zip_file, child, base)
    else:
        arcname = src.relative_to(base)
        zip_file.write(src, arcname)
        print(f"Added {arcname}")


def build_zip(output: Path):
    with ZipFile(output, 'w', compression=ZIP_DEFLATED) as zipf:
        for item in INCLUDE:
            src = ROOT / item
            if not src.exists():
                print(f"Warning: ignored missing path {src}")
                continue
            add_path_to_zip(zipf, src, ROOT)
    print(f"Created ZIP archive: {output}")


def build_rar(output: Path):
    rar_exe = shutil.which('rar') or shutil.which('rar.exe')
    if not rar_exe:
        raise RuntimeError('rar executable not found in PATH. Install rar or use zip format.')
    command = [rar_exe, 'a', str(output)]
    command.extend([str(ROOT / item) for item in INCLUDE if (ROOT / item).exists()])
    print('Running:', ' '.join(command))
    subprocess.run(command, check=True)
    print(f"Created RAR archive: {output}")


def main():
    parser = argparse.ArgumentParser(description='Create a deployment package for PythonAnywhere.')
    parser.add_argument('--output', '-o', default='deploy_package.zip', help='Output archive path')
    parser.add_argument('--format', '-f', choices=['zip', 'rar'], default='zip', help='Archive format')
    args = parser.parse_args()

    output = ROOT / args.output
    if output.exists():
        output.unlink()

    if args.format == 'zip':
        build_zip(output)
    else:
        build_rar(output)

    print('Deployment package ready.')


if __name__ == '__main__':
    main()
