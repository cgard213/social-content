# Rules

Things that were learned the hard way. This file outranks `PROCEDURE.md`.

Add a line whenever you correct the tool on something you will care about again. One
line, stated as an instruction, with the reason if the reason is not obvious. Do not add
a rule the first time something goes wrong. Add it the second time, when you know it was
a pattern and not a one-off.

Delete rules that stop being true. A file full of stale rules is worse than a short one.

## Seeded

These came from a few hundred reels and are true regardless of what you are making.

- Cut points snap to word boundaries from `words.json`. Never mid-word, no exceptions.
- Keep the last clean attempt of a line, not the first. Delivery improves with each try.
- Leave 120 ms of air at both ends of a range. Frame-tight cuts sound clipped.
- `-ss` goes after `-i`. Before it, seeking is keyframe-accurate only and cuts drift.
- Never trust raw `ffprobe` dimensions on phone footage. Normalize first, measure after.
- Captions come from `tools/captions.py`. Hand-written ASS has been rebuilt three times.
- ASS colors are BGR, not RGB. Reading one as RGB inverts the whole palette.
- Under `BorderStyle 4`, the `Outline` number is plate padding, not stroke width.
- Hold each caption cue until the next one starts. Ending at the last word is what makes
  captions flicker.
- Every word on screen needs high contrast against whatever is behind it. When unsure,
  put a solid plate behind it. Check it over the brightest frame, not the average one.
- Re-check audio after every step that touches video. It gets dropped silently.
- Fade times in a trimmed segment are in SOURCE time, not segment time. Writing them
  from zero silences the whole segment and the file looks perfectly normal.
- Audio checks test for quiet, not for `-inf`. A silenced track reads as -91 dB and
  sails past a check that only looks for `-inf`.
- A QC still with no caption usually means you landed in the two-frame gap between
  cues, not that the burn failed. Nudge the timestamp before investigating.
- Judge the cover by `work/cover_gridcrop.png`, never by the full-height file. The grid
  loses the top and bottom 285 pixels and that is where covers get ruined.
- Pull the cover frame from the cut before captions are burned. A frame with a caption
  plate on it gives you two pieces of type fighting each other.
- Social captions run three or four short lines on every platform, including Instagram.
  A caption nobody finishes never reaches the call to action.
- Never put a number in a caption that is not in the video.

## Yours

Add below this line.
