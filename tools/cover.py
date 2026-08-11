#!/usr/bin/env python3
"""Build the cover image.

    python3 ../tools/cover.py --project . --line "You are answering half your calls"

Pulls a frame from the cut, lays the brand card over it, and writes out/cover.png at
1080x1920. Also writes work/cover_gridcrop.png, which is what the profile grid will
actually show. Look at that one before calling the cover done.

Why the grid crop matters: the file is 1080x1920, but a profile grid re-crops it to
3:4. The dependable band is the centred 1080x1350, so the top 285 pixels and the bottom
285 are gone. A card that looks perfectly placed at full height can lose its first line
in the grid, which is the only place the cover has to work.

The frame comes from the clean cut, before captions are burned. A frame with a caption
plate already on it gives you a cover with two competing pieces of type.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from captions import ass_color, read_brand  # noqa: E402

GRID_CROP = "crop=1080:1350:0:285"


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:3])} ... failed:\n{proc.stderr[-600:]}")
    return proc


def build_ass(brand, fixed, variable, out):
    dark = ass_color(brand["dark"])
    light = ass_color(brand["light"])
    accent = ass_color(brand["accent"])
    font = brand["font"]

    # Sits inside the safe band with room to spare. 420 is far enough down that the
    # grid crop cannot eat the first line, and high enough to clear a face at centre.
    x, y = 90, 420

    text = fixed.replace("\n", " ").strip()
    body = f"{text}\\N{{\\1c{accent}}}{variable.strip()}"

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
        f"Style: Cover,{font},92,{dark},{accent},{light},{light},"
        f"0,0,0,0,100,100,{brand['tracking']},0,4,40,0,7,90,90,90,1",
        "",
        "[Events]",
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
        f"Dialogue: 0,0:00:00.00,0:00:10.00,Cover,,0,0,0,,{{\\pos({x},{y})}}{body}",
    ]
    out.write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--line", required=True, help="the line this video is about")
    ap.add_argument("--fixed", help="the recurring line above it, defaults to BRAND.md")
    ap.add_argument("--at", default="2.0", help="seconds into the cut to grab the frame")
    ap.add_argument("--source", help="defaults to the project's work/base.mp4")
    ap.add_argument("--brand", default=str(ROOT / "BRAND.md"))
    ap.add_argument("--out")
    args = ap.parse_args()

    proj = Path(args.project)
    work = proj / "work"
    work.mkdir(parents=True, exist_ok=True)

    source = Path(args.source) if args.source else work / "base.mp4"
    if not source.exists():
        print(f"No cut at {source}. Build the reel first.", file=sys.stderr)
        return 1

    out = Path(args.out) if args.out else proj / "out" / "cover.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    brand = read_brand(Path(args.brand))
    fixed = args.fixed
    if not fixed:
        m = re.search(r"^-\s*\*\*Fixed line:\*\*\s*(.+)$", Path(args.brand).read_text(), re.M)
        fixed = m.group(1).strip() if m else ""
    if not fixed:
        print("No fixed line in BRAND.md and none passed. Using the variable line "
              "alone.", file=sys.stderr)

    frame = work / "cover_frame.png"
    # Output seeking. -ss before -i would drop the subtitles filter later and is
    # keyframe-accurate only, which is the wrong frame more often than not.
    run(["ffmpeg", "-y", "-v", "error", "-i", str(source), "-ss", args.at,
         "-frames:v", "1", str(frame)])

    ass = work / "cover.ass"
    build_ass(brand, fixed, args.line, ass)

    fonts = ROOT / "fonts"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(frame),
         "-vf", f"subtitles={ass}:fontsdir={fonts}", "-frames:v", "1", str(out)])

    grid = work / "cover_gridcrop.png"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-vf", GRID_CROP,
         "-frames:v", "1", str(grid)])

    print(f"{out}\n{grid}  <- this is what the profile grid shows, look at it")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
