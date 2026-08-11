# social-content

A video editor you talk to. Point it at a clip you filmed on your phone and it cuts the
dead air, keeps the best take of each line, burns captions in your colors, builds a
cover image, and writes the caption three ways for Instagram, TikTok and YouTube.

It runs inside Claude Desktop's Cowork. You will not type a single command.

## What you need

Claude Desktop, with Cowork. That is the only thing you have to have.

Optionally an ElevenLabs account, which is free and asks for no card. It transcribes
more accurately, so the cuts land cleaner. Setup asks which you want, and the built-in
option needs no account at all, so you can skip this and decide later.

## Get started

**1. Download it.** Click the green **Code** button above, then **Download ZIP**.

**2. Unzip it onto your Desktop** and rename the folder to `social-content`. GitHub adds
`-main` to the end and you do not want that.

**3. Open Claude Desktop, click Cowork, and point it at that folder.**

**4. Paste this in:**

```
This folder is a video toolkit. Read SETUP.md and .claude/skills/create-social-
content/SKILL.md, then set me up. Ask me one question at a time and wait for my
answer. I am not technical and I will not be running commands, so if something
is broken, tell me what it means for me rather than what the error said.

First, check the folder over. Confirm you can see the create-social-content
skill, and confirm ffmpeg is here and can burn subtitles. Say plainly if
anything is missing.

Second, my brand. Ask whether I already have a brand guide or want you to build
one from my website. If I give you a website, search for it first and then read
it, pull out my colors and my typeface, show me what you found, and let me
correct it before you save anything. Then ask me for the fixed line that goes on
every cover image, and how I sound when I write. Put all of it in BRAND.md.

Third, transcription. Ask which I want and give me the tradeoff plainly:
ElevenLabs is more accurate and the account is free for about 30 minutes of
footage a month, local is free forever but needs a 430 MB download. Walk me
through the steps for whichever I pick, then check it actually worked before you
tell me it did. Save my answer in SETTINGS.md.

When that is all done, explain how this works from here: what I type to start a
video, where I put the clip, and what I get back at the end. Then offer to make
my first project right now.
```

That is the only thing you have to copy. It checks the folder, asks three or four
questions, and then offers to make your first video on the spot.

From then on you type `/create-social-content` and it takes it from there.

Do not bother asking Cowork to clone this for you. Its sandbox reaches Anthropic, pypi
and npm, and nothing else, so the download above is the way in.

## What comes out

Every project gets its own dated folder, and three files land in it:

- `reel.mp4`, the video with captions burned in
- `cover.png`, for the profile grid. You upload this by hand when you post, otherwise
  the platform picks its own frame and it always picks a badly timed one
- `captions.txt`, the caption written for Instagram, TikTok and YouTube

## What is in here

| | |
|---|---|
| `SETUP.md` | The full guide. Everything on this page plus what to do when it goes wrong |
| `BRAND.md` | Your colors, font, cover line and voice. Filled in once during setup |
| `RULES.md` | Corrections you have made. This is the part that matters |
| `PROCEDURE.md` | The editing steps. Written for the model, not for you |
| `tools/` | The scripts that do the cutting, the captions and the cover |

## Why the rules file matters more than the code

The scripts here come to a few hundred lines. The useful part is `RULES.md`, a list of
mistakes that each cost an evening to find. ASS subtitle colors are BGR rather than RGB,
so reading one as RGB inverts the whole palette. iPhone footage reports itself as
landscape and lies. Speech recognition pads the last word of a phrase well past where
the audio stops, so filtering on end time silently drops it.

None of that is guessable. It exists because someone got it wrong, worked out why, and
wrote it down. Add your own as you go and the tool stops repeating itself.
