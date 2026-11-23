"""Entry for make.fun news-image-20261123.

Copies the entry image beside this file to the output directory.
Standard library only, no network.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

if not SRC.is_file():
    raise SystemExit(f"missing entry image: {SRC}")
if SRC.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("entry.png is not a PNG file")
OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, OUT_DIR / "entry.png")
print("wrote", OUT_DIR / "entry.png")
