# Procedure

Read this file, `RULES.md`, and `BRAND.md` before doing anything. `RULES.md` outranks
this file on any conflict, because it holds corrections the operator has already made.

**Run everything from inside the project folder**, the dated one the skill created.
Paths below are relative to it: the clip is in `raw/`, intermediates go in `work/`, the
finished file goes in `out/`. Shared things live one level up, so `../tools/`,
`../fonts/`, `../BRAND.md`.

Never move, rename, or delete anything in `raw/`. That is the operator's footage and
there may not be another copy.

Stop once, at step 5, and show the operator the cut before spending time on captions
and the final encode. That is the only checkpoint. Do not stop at the others.

---

## 0. Preflight

Run these and report anything missing before starting:

```bash
ffmpeg -version | head -1
ffmpeg -filters | grep -w subtitles
ls ../tools/whisper-small.en 2>/dev/null
ls ../fonts/*.ttf 2>/dev/null
```

- No `subtitles` filter means libass is not compiled in and captions cannot be burned.
  Stop and say so. Do not substitute `drawtext`, it will not match the design.
- The transcription check depends on what `../SETTINGS.md` says they chose. For
  ElevenLabs, confirm you have a `transcribe_audio` tool; if you do not, they have not
  restarted Claude Desktop since installing it, which is nearly always the reason. For
  local, confirm `../tools/whisper-small.en/model.bin` exists; if it does not, they have
  not dropped the downloaded model in yet. You cannot fetch it from in here, the weights
  come from Hugging Face and this environment reaches Anthropic, pypi and npm only. Do
  not try, and do not offer to. Point them at `../SETUP.md` and stop.
- No TTF in `../fonts/` means captions fall back to whatever fontconfig finds. Check
  with `fc-list | head`. If that is also empty, stop and ask for a font file.

## 1. Normalize the source

iPhone vertical footage reports 1920x1080 with a rotation flag. Raw dimensions lie. Do
not read them and decide the video is landscape. Normalize once, then trust the result:

```bash
ffmpeg -y -i raw/<CLIP> \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -metadata:s:v:0 rotate=0 \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
  -c:a aac -ar 48000 -movflags +faststart work/source.mp4
```

Confirm the result with `ffprobe` before continuing. It must be 1080x1920 with no
rotation side data.

If the source is HLG or PQ (`color_transfer` is `arib-std-b67` or `smpte2084`) the grade
will read washed out and there is nothing in this environment that fixes it well. Say so
plainly, finish the reel anyway, and tell the operator to turn HDR off in Camera settings
before the next shoot.

## 2. Extract audio

```bash
ffmpeg -y -i work/source.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le work/audio.wav
```

Small mono wav, not the video file. Both transcription paths want this.

## 3. Transcribe

Use whichever path `../SETTINGS.md` records. If it says nothing, prefer the
`transcribe_audio` tool when you have it and fall back to the local model.

**ElevenLabs**: call `transcribe_audio` with the project's `work/audio.wav` and tell it
to write to the same `work/` folder. Its word boundaries are measured rather than
inferred, which is the whole reason to pay for it.

**Local**:

```bash
python3 ../tools/transcribe.py work/audio.wav
```

First run installs `faster-whisper` from pip, which takes a minute or two. Both paths
write `work/words.json` in the same shape:

```json
{"text": "full transcript", "words": [{"text": "so", "start": 1.24, "end": 1.39}]}
```

## 4. Choose the takes

Read `work/words.json`. The operator films one long take and restarts whenever they flub
a line, so the same sentence appears several times. Your job is to keep the best attempt
of each and drop everything else.

- Prefer the last clean attempt. People deliver better on the fourth try than the first.
- Cut the restarts, the false starts, the throat clearing, and the silence between takes.
- Snap every cut point to a word boundary from the words array. Never cut mid-word.
- Leave about 120 ms of air before the first word of a range and after the last. Cutting
  tight to the waveform sounds clipped.

Write `work/edl.json`:

```json
{"source": "work/source.mp4",
 "ranges": [{"start": 12.40, "end": 18.95, "beat": "hook"}]}
```

## 5. Cut, then stop

For each range, with `DUR` computed as `end - start`:

```bash
ffmpeg -y -i work/source.mp4 -ss <START> -to <END> \
  -af "afade=t=in:st=0:d=0.02,afade=t=out:st=<DUR-0.02>:d=0.02" \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
  -c:a aac -ar 48000 -ac 2 work/seg_<NN>.mp4
```

`-ss` goes after `-i`. Before `-i` it seeks by keyframe and your cut points drift.

Concat with the demuxer, then normalize loudness in one pass:

```bash
printf "file 'seg_%02d.mp4'\n" $(seq 0 <N>) > work/concat.txt
ffmpeg -y -f concat -safe 0 -i work/concat.txt -c copy work/joined.mp4
ffmpeg -y -i work/joined.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v copy -c:a aac -b:a 192k work/base.mp4
```

**Stop here.** Report the duration, the number of cuts, and the running transcript of
what survived. Ask whether the cut is right. Wait for an answer before continuing.

## 6. Captions

Pick 4 to 6 emphasis words yourself: the claim, any number, and the call to action. Do
not ask which words. Then:

```bash
python3 ../tools/captions.py --project . --emphasis "word one,word two,word three"
```

It reads `work/words.json`, `work/edl.json` and `../BRAND.md`, and writes
`work/captions.ass`. Do not hand-write the ASS file. The timing rules in that script are
the difference between captions that read and captions that flicker.

## 7. Burn

```bash
ffmpeg -y -i work/base.mp4 -vf "subtitles=work/captions.ass:fontsdir=../fonts" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a copy -movflags +faststart out/reel.mp4
```

Check the ffmpeg log for the `fontselect` line. If it resolved to a font you did not
expect, the font name in `BRAND.md` does not match what the TTF actually registers, and
the captions are rendering in the wrong weight.

## 8. Check the result

```bash
ffprobe -v error -show_entries stream=width,height,codec_type -of csv out/reel.mp4
ffmpeg -i out/reel.mp4 -af volumedetect -f null - 2>&1 | grep mean_volume
```

Dimensions must be 1080x1920. Both a video and an audio stream must be present. Mean
volume must not be `-inf`, which would mean the audio was dropped somewhere.

Pull one still from a moment where the caption sits over the brightest part of the
frame, and look at it. Captions that read fine over a dark shirt disappear over a
window.

## 9. Social captions

Write `out/captions.txt` from the finished cut. Read the Voice section of `../BRAND.md`
first and write in that voice, not yours.

```
INSTAGRAM
<three or four short lines, then the call to action>
<3 to 5 hashtags, never more>

TIKTOK
<same length, same call to action, no hashtag wall>

YOUTUBE
Title: <plain language, under 70 characters or it truncates>
<two or three lines>
```

Rules that hold for all three:

- Short. The caption is not the piece, the video is. If it runs to more than one
  paragraph of setup it is already too long, and a caption nobody finishes never reaches
  the call to action.
- The call to action uses whatever word they actually said on camera. Never invent a
  keyword afterwards.
- Never use a number that is not in the video, and drop any number in the video that has
  no source behind it.
- The YouTube title is a search surface, so a plain description of the symptom beats a
  clever line. Reusing the cover's second line is good, the two reinforce each other.

## 10. Cover image

Nothing ships without this. The platform picks its own frame otherwise and it always
picks a bad one, and on a profile grid the cover is the only thing selling the video.

Propose the variable line yourself, drawn from what the video is actually about, and
show it to the operator before rendering. The fixed line comes from `../BRAND.md` and
does not change between videos.

```bash
python3 ../tools/cover.py --project . --line "the line this video is about"
```

Pass `--at <seconds>` to pick a different frame. Aim for the first few seconds, before
they lean into the camera, with eyes to the lens.

Then look at `work/cover_gridcrop.png`, not `out/cover.png`. The grid crop is what
people actually see, it loses the top and bottom 285 pixels, and a card that reads
perfectly at full height can lose a line in it. If the card is clipped or fights the
face, move the frame with `--at` before anything else.

## 11. Report

Tell the operator where the three files are, `out/reel.mp4`, `out/cover.png` and
`out/captions.txt`, plus the duration and how many takes were dropped. Mention anything
you had to work around. If you worked around the same thing twice, say so and offer to
add it to `RULES.md`.

The cover has to be uploaded by hand when they post. Say so, because nothing about the
file makes that obvious.
