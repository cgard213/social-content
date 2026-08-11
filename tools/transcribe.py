#!/usr/bin/env python3
"""Local transcription. Runs inside Cowork's VM, no network, no account.

    python3 tools/transcribe.py work/audio.wav

Writes work/words.json:

    {"text": "...", "words": [{"text": "so", "start": 1.24, "end": 1.39}], "source": "local"}

Installs faster-whisper from pypi on first run, which is allowed by the VM's network
allowlist. The model weights are not, which is why they were downloaded ahead of time
by tools/get-model.py and live in tools/whisper-small.en.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "tools" / "whisper-small.en"


def ensure_faster_whisper():
    try:
        from faster_whisper import WhisperModel  # noqa: F401
        return
    except ImportError:
        pass
    print("Installing faster-whisper (first run only) ...", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", "faster-whisper"],
        check=True,
    )


def main():
    if len(sys.argv) < 2:
        print("usage: transcribe.py <audio.wav> [out.json]", file=sys.stderr)
        return 2

    audio = Path(sys.argv[1])
    # Defaults next to the audio, which is the project's own work/ folder.
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else audio.parent / "words.json"

    if not audio.exists():
        print(f"No such file: {audio}", file=sys.stderr)
        return 1

    if not (MODEL / "model.bin").exists():
        print(
            f"Model missing at {MODEL}.\n"
            "Run this from a terminal on the host machine, once:\n"
            "    python3 tools/get-model.py",
            file=sys.stderr,
        )
        return 1

    ensure_faster_whisper()
    from faster_whisper import WhisperModel

    # local_files_only stops it reaching for Hugging Face, which is blocked in here and
    # fails with an error that points at the wrong problem.
    model = WhisperModel(
        str(MODEL), device="cpu", compute_type="int8", local_files_only=True
    )

    segments, info = model.transcribe(
        str(audio), word_timestamps=True, vad_filter=True, beam_size=5
    )

    words, parts = [], []
    for seg in segments:
        parts.append(seg.text)
        for w in seg.words or []:
            text = w.word.strip()
            if text:
                words.append(
                    {"text": text, "start": round(w.start, 3), "end": round(w.end, 3)}
                )

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "text": " ".join(p.strip() for p in parts).strip(),
                "words": words,
                "source": "local",
                "duration": round(info.duration, 2),
            },
            indent=1,
        )
    )

    print(f"{len(words)} words over {info.duration:.1f}s -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
