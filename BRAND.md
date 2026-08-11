# Brand

Fill this in once and every project uses it. The tool reads it every run and does not
improvise around it. The values below are what it ships with, so it works before you
touch anything.

You do not have to fill it in by hand. On first run the skill offers to read your
website and write this file for you. Check what it comes back with either way, because
sites carry plenty of colors that have nothing to do with the brand.

## Colors

Four, and only four. More than four and the captions stop looking like a system.

| Role | Hex | Used for |
|---|---|---|
| light | `#F0EDE4` | caption plate, light text |
| dark | `#1D263A` | dark text, plates behind type |
| accent | `#2E58BC` | the alternating caption plate |
| highlight | `#C0C657` | the emphasis word, and nothing else |

Change the hex values, keep the four roles. `tools/captions.py` parses this table by
role name and converts to the BGR that ASS wants.

## Type

- **Font:** `Geist Black`
- **Fallback:** `DejaVu Sans`

Drop the TTF in `fonts/`. The name above has to match what the file actually registers
as, which is not always what the filename says. A file called `Geist-Black.ttf` may
register its family as `Geist Black` with a regular subfamily, so asking for `Geist` in
bold gets you Geist Bold instead and everything looks slightly wrong in a way that is
hard to name. Check the `fontselect` line in the ffmpeg output.

- **Size:** 84
- **Tracking:** -3.2 (ASS wants absolute pixels here, not em)
- **Case:** sentence case

Sentence case is deliberate. Uppercase flattens the rise and fall of the letters, which
is most of what makes type recognizable at a glance on a phone.

## Caption layout

| Setting | Value |
|---|---|
| Plate padding | 32 |
| Shadow | 0 |
| Margin left / right | 80 |
| Margin from bottom | 280 |
| Border style | 4 |

280 from the bottom clears the Instagram interface. Lower and the caption sits under the
username on a repost.

## How the captions read

Two styles alternate on a fully opaque plate. Default is accent text on light. Accent is
light text on accent. A cue flips to the second style when it contains one of your
emphasis words, and that word itself goes highlight color inside the cue.

The alternation is the entire look. One style on its own reads flat.

## Cover

Every video gets a cover image, because the platform picks a frame on its own otherwise
and it always picks a bad one. On a profile grid there is no sound and no motion, so the
cover is the only thing selling the video.

Two lines on one card. The first never changes, the second is about this video:

- **Fixed line:** You do not need AI:

Change that line to yours and then leave it alone. The repetition is what makes someone
recognize your videos in a feed before they read a word.

## Voice

Used for the social captions the tool writes at the end. Fill in whatever is true.

- **You sound like:** plain and specific, peer to peer, no hype
- **You never say:** words your customers would not use out loud
- **Your call to action:** what you want them to comment or click
