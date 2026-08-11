# social-content

A video editor you talk to. Point it at a clip you filmed on your phone and it cuts the
dead air, keeps the best take of each line, burns captions in your colors, builds a
cover image, and writes the caption three ways for Instagram, TikTok and YouTube.

Runs inside Claude Desktop's Cowork. You will not type a single command.

## Get it

1. Click the green **Code** button above, then **Download ZIP**.
2. Unzip onto your Desktop and rename the folder to `social-content`. GitHub adds
   `-main` to the name and you do not want that.
3. Open Claude Desktop, click Cowork, point it at the folder.
4. Open `PROMPTS.md` and paste the first prompt.

Full instructions are in [SETUP.md](SETUP.md). Read that one, not this one.

Do not bother asking Cowork to clone this for you. Its sandbox reaches Anthropic, pypi
and npm, and nothing else, so the browser download is the way in.

## What is in here

| | |
|---|---|
| `SETUP.md` | Start here. The whole thing in plain language |
| `PROMPTS.md` | The two things you copy and paste |
| `BRAND.md` | Your colors, font, cover line and voice. Fill it once |
| `RULES.md` | Corrections you have made. This is the part that matters |
| `PROCEDURE.md` | The editing steps. For the model, not for you |
| `tools/` | The scripts that do the cutting, captions and cover |

## Why the rules file matters more than the code

The scripts here are maybe four hundred lines. The useful part is `RULES.md`, which is a
list of mistakes that each cost an evening to find. ASS subtitle colors are BGR and not
RGB, so reading one as RGB inverts the whole palette. iPhone footage reports itself as
landscape and lies. Speech recognition pads the last word of a phrase well past where
the audio stops, so filtering on end time silently drops it.

None of that is guessable. It only exists because someone got it wrong, worked out why,
and wrote it down. Add your own as you go and the tool stops repeating itself.

## Requirements

Claude Desktop with Cowork. Optionally an ElevenLabs account for sharper word timings,
free for about 30 minutes of audio a month. There is a local option that costs nothing
and needs no account.
