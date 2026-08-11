#!/usr/bin/env python3
"""Fetch the transcription model into the folder. For whoever is packaging this up.

    python3 tools/get-model.py

Run it once on a machine with internet, then hand out the folder with the model already
inside. People using the tool never run this, or anything else in a terminal.

It creates tools/.venv, installs huggingface_hub into it, and pulls the CTranslate2
build of Whisper small.en into tools/whisper-small.en (about 250 MB).

This cannot happen inside Cowork. Its network allowlist covers Anthropic, pypi and npm,
so faster-whisper installs fine in there but the weights, which come from Hugging Face,
do not. Hence shipping them in the folder.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = "Systran/faster-whisper-small.en"
DEST = ROOT / "whisper-small.en"
VENV = ROOT / ".venv"
VENV_PY = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    if DEST.exists() and any(DEST.glob("model.bin")):
        print(f"Model already here: {DEST}")
        return 0

    if not VENV_PY.exists():
        print("Creating tools/.venv ...")
        run(sys.executable, "-m", "venv", VENV)

    print("Installing huggingface_hub ...")
    run(VENV_PY, "-m", "pip", "install", "--quiet", "--upgrade", "pip")
    run(VENV_PY, "-m", "pip", "install", "--quiet", "huggingface_hub")

    print(f"Downloading {REPO} (about 250 MB, this takes a few minutes) ...")
    code = (
        "from huggingface_hub import snapshot_download;"
        f"p=snapshot_download({REPO!r}, local_dir={str(DEST)!r});"
        "print(p)"
    )
    run(VENV_PY, "-c", code)

    if not (DEST / "model.bin").exists():
        print("Download finished but model.bin is missing. Something went wrong.")
        return 1

    size = sum(f.stat().st_size for f in DEST.rglob("*") if f.is_file())
    print(f"\nDone. {DEST} ({size / 1e6:.0f} MB)")
    print("You can close the terminal. Everything else happens in Cowork.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as e:
        print(f"\nFailed: {' '.join(str(c) for c in e.cmd)}")
        sys.exit(1)
