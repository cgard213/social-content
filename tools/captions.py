#!/usr/bin/env python3
"""Build the caption file.

    python3 tools/captions.py --emphasis "every call,forty seconds,free"

Reads work/words.json, work/edl.json (if there was a cut) and BRAND.md, and writes
work/captions.ass.

Do not hand-write the ASS. The timing here is the part that took the longest to get
right, and none of it is guessable:

  - Words are selected by start time, never by end time. Speech recognition pads the
    last token of a phrase well past where the audio actually stops, so filtering on
    `end <= range_end` silently drops the final word of every trimmed segment.
  - Cues seed at three words and then grow until they clear a minimum on-screen time.
    Two-word cues technically fit the speech and are unreadable.
  - Each cue is held until the next one begins rather than ending on its own last word.
    That single change is what stops the flicker between cues.
  - ASS colors are BGR. Feed it RGB and the whole palette inverts, which reads as a
    styling bug rather than a color-order bug and costs an afternoon.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# The toolkit root, the social-content folder. BRAND.md and RULES.md live here and are
# shared by every project. Each project is a subfolder with its own raw/ work/ out/.
ROOT = Path(__file__).resolve().parent.parent

MIN_CUE = 0.833   # Netflix/BBC floor for a readable cue
SEED_WORDS = 3
MAX_WORDS = 7
DEFAULTS = {
    "light": "#F0EDE4",
    "dark": "#1D263A",
    "accent": "#2E58BC",
    "highlight": "#C0C657",
    "font": "Geist Black",
    "size": "84",
    "tracking": "-3.2",
    "padding": "32",
    "margin_lr": "80",
    "margin_v": "280",
}


def ass_color(hex_str):
    """#RRGGBB -> &H00BBGGRR. ASS is BGR."""
    h = hex_str.strip().lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def read_brand(path):
    brand = dict(DEFAULTS)
    if not path.exists():
        return brand
    text = path.read_text()

    for role in ("light", "dark", "accent", "highlight"):
        m = re.search(rf"^\|\s*{role}\s*\|\s*`?(#[0-9A-Fa-f]{{6}})`?", text, re.M)
        if m:
            brand[role] = m.group(1)

    m = re.search(r"\*\*Font:\*\*\s*`?([^`\n]+?)`?\s*$", text, re.M)
    if m:
        brand["font"] = m.group(1).strip()

    for key, label in (
        ("size", "Size"),
        ("tracking", "Tracking"),
    ):
        m = re.search(rf"\*\*{label}:\*\*\s*(-?[\d.]+)", text)
        if m:
            brand[key] = m.group(1)

    for key, label in (
        ("padding", "Plate padding"),
        ("margin_lr", r"Margin left / right"),
        ("margin_v", "Margin from bottom"),
    ):
        m = re.search(rf"\|\s*{label}\s*\|\s*(-?[\d.]+)\s*\|", text)
        if m:
            brand[key] = m.group(1)

    return brand


def map_to_cut(words, edl):
    """Move word timings from the source timeline onto the cut timeline."""
    if not edl:
        return list(words)

    out, offset = [], 0.0
    for rng in edl.get("ranges", []):
        start, end = float(rng["start"]), float(rng["end"])
        for w in words:
            # Select on start only. End timings are padded by the recognizer.
            if start <= w["start"] < end:
                out.append(
                    {
                        "text": w["text"],
                        "start": w["start"] - start + offset,
                        "end": min(w["end"], end) - start + offset,
                    }
                )
        offset += end - start
    return out


def norm(text):
    return re.sub(r"[^\w']", "", text.lower())


def find_spans(words, emphasis):
    """Locate each emphasis phrase in the word list as an inclusive index range."""
    flat = [norm(w["text"]) for w in words]
    spans = set()
    for phrase in emphasis:
        toks = [norm(t) for t in phrase.strip().split() if norm(t)]
        if not toks:
            continue
        n = len(toks)
        for i in range(len(flat) - n + 1):
            if flat[i : i + n] == toks:
                spans.add((i, i + n - 1))
    return sorted(spans)


def build_cues(words, emphasis):
    spans = find_spans(words, emphasis)

    def span_covering(idx):
        for a, b in spans:
            if a <= idx <= b:
                return (a, b)
        return None

    # Pass one: index ranges, half open.
    bounds, i = [], 0
    while i < len(words):
        j = min(i + SEED_WORDS, len(words))
        # Grow until the cue is on screen long enough to read.
        while (
            j < len(words)
            and (j - i) < MAX_WORDS
            and (words[j - 1]["end"] - words[i]["start"]) < MIN_CUE
        ):
            j += 1
        # Never end a cue in the middle of an emphasis phrase. Splitting one across
        # two cues means neither cue matches and the highlight silently disappears.
        covering = span_covering(j - 1)
        if covering and covering[1] >= j:
            j = min(covering[1] + 1, len(words))
        bounds.append([i, j])
        i = j

    # Pass two: no cue is left holding a single word.
    k = 1
    while k < len(bounds):
        if bounds[k][1] - bounds[k][0] < 2:
            bounds[k - 1][1] = bounds[k][1]
            bounds.pop(k)
        else:
            k += 1

    cues = []
    for a, b in bounds:
        chunk = words[a:b]
        hit = next((s for s in spans if s[0] >= a and s[1] < b), None)
        cues.append(
            {
                "start": chunk[0]["start"],
                "end": chunk[-1]["end"],
                "words": [w["text"] for w in chunk],
                "emphasis": (hit[0] - a, hit[1] - a) if hit else None,
            }
        )

    # Hold each cue until the next one starts. This is what kills the flicker.
    for k, cue in enumerate(cues):
        if k + 1 < len(cues):
            cue["end"] = max(cue["end"], cues[k + 1]["start"] - 0.083)
        else:
            cue["end"] += 0.35
    return cues


def stamp(t):
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def render(cues, brand):
    light = ass_color(brand["light"])
    accent = ass_color(brand["accent"])
    highlight = ass_color(brand["highlight"])
    font, size = brand["font"], brand["size"]
    track, pad = brand["tracking"], brand["padding"]
    mlr, mv = brand["margin_lr"], brand["margin_v"]

    def style(name, fill, plate):
        return (
            f"Style: {name},{font},{size},{fill},{highlight},{plate},{plate},"
            f"0,0,0,0,100,100,{track},0,4,{pad},0,2,{mlr},{mlr},{mv},1"
        )

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,"
        "BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,"
        "BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        style("Default", accent, light),
        style("Accent", light, accent),
        "",
        "[Events]",
        # MarginV must be in this Format line or libass leaks a stray comma into the text.
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]

    for cue in cues:
        name = "Accent" if cue["emphasis"] else "Default"
        base = light if name == "Accent" else accent
        parts = list(cue["words"])
        if cue["emphasis"]:
            a, b = cue["emphasis"]
            parts[a] = f"{{\\1c{highlight}}}{parts[a]}"
            parts[b] = f"{parts[b]}{{\\1c{base}}}"
        text = " ".join(parts)
        # Hard spaces so the plate has breathing room at both ends.
        lines.append(
            f"Dialogue: 0,{stamp(cue['start'])},{stamp(cue['end'])},{name},,0,0,0,,"
            f"\\h{text}\\h"
        )

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emphasis", default="", help="comma separated words to highlight")
    ap.add_argument("--project", default=".", help="the project folder")
    ap.add_argument("--words")
    ap.add_argument("--edl")
    ap.add_argument("--brand", default=str(ROOT / "BRAND.md"))
    ap.add_argument("--out")
    args = ap.parse_args()

    work = Path(args.project) / "work"
    args.words = args.words or str(work / "words.json")
    args.edl = args.edl or str(work / "edl.json")
    args.out = args.out or str(work / "captions.ass")

    words_path = Path(args.words)
    if not words_path.exists():
        print(f"No transcript at {words_path}. Run step 3 first.", file=sys.stderr)
        return 1

    words = json.loads(words_path.read_text())["words"]
    edl_path = Path(args.edl)
    edl = json.loads(edl_path.read_text()) if edl_path.exists() else None

    cues = build_cues(map_to_cut(words, edl), args.emphasis.split(","))
    if not cues:
        print("No cues built. Check that the transcript overlaps the edl ranges.",
              file=sys.stderr)
        return 1

    brand = read_brand(Path(args.brand))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(cues, brand))

    marked = sum(1 for c in cues if c["emphasis"])
    print(f"{len(cues)} cues ({marked} emphasized) -> {out}")
    if not marked and args.emphasis.strip():
        print("None of the emphasis words matched the transcript. Check the spelling "
              "against what was actually said.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
