---
name: create-social-content
description: Start a social video project. Sets up the brand guide and transcription on first run, then creates a named project folder, takes the operator's raw footage, and cuts it into a finished captioned vertical reel. Use when the operator says /create-social-content, "new reel", "new social project", "start a video", or drops footage and asks for a cut.
---

# Create social content

One session, start to finish: set up if this is the first time, make a project folder,
wait for footage, then cut the reel.

Everything lives under the `social-content` folder. Shared files sit at the top,
`BRAND.md`, `RULES.md`, `PROCEDURE.md`, `SETTINGS.md` and `tools/`, and each project
gets its own subfolder.

Ask one question at a time. Wait for the answer before asking the next. The operator is
not technical and will not be running commands, so never hand them one. If something is
broken, say what it means for them, not what the error said.

---

## Step 1. First run only

Skip this whole step if `SETTINGS.md` exists and `BRAND.md` has been filled in. Go
straight to step 2.

### 1a. The brand guide

Ask:

> Do you have a brand guide I should follow, or should I build one from your website?

**If they have one**, take it however it arrives, a pasted block of text, a file they
drop in the folder, a description in their own words. Pull out what `BRAND.md` needs:
four colors, a caption font, and how the captions should sit. Ask about anything the
source does not cover. Write `BRAND.md`.

**If they give a website**, do this and nothing else:

1. Run a **web search** for the domain first. A direct fetch of a URL they typed will
   usually be refused, because this environment only permits fetching URLs that came
   back from a search. Searching first is what makes the fetch work.
2. Fetch the result and read the page.
3. Pull the four colors and the typeface from what you find. Note the voice too, whether
   it is plain or playful, what it calls its customers, what it never says.
4. Write `BRAND.md` using the existing table structure. Keep the four role names exactly
   as they are, `light`, `dark`, `accent`, `highlight`, because `tools/captions.py`
   looks them up by name.
5. Show them the four colors and the font and ask whether that looks right before moving
   on. Sites often carry colors that are nothing to do with the brand.

If the fetch fails even after searching, do not keep retrying. Ask them for their colors
in plain words instead, "what are your two main colors," and work from that.

**Then two more questions**, once the colors are settled, still one at a time.

First, the fixed cover line. Explain it before you ask: every cover carries two lines,
the top one never changes and the bottom one is about that video, and the repetition is
what makes someone recognize their videos in a feed. Ask what the top line should say.
Propose two or three options from what you learned about them. Write it into `BRAND.md`
as the `Fixed line`.

Second, voice. Ask what they sound like and what they would never say, in their own
words. If you read their website you already have most of this, so show them what you
inferred and ask whether it is right rather than making them start from nothing. Write
it into the Voice section. That section is what the social captions get written from.

### 1b. Transcription

Ask, exactly like this:

> How should I transcribe your audio?
>
> **ElevenLabs** (more accurate, cuts land cleaner. Free for about 30 minutes of footage
> a month, then roughly 22 cents an hour)
>
> **Local** (free forever, nothing leaves your machine, word timings are a little
> looser. One 430 MB download to set up)

Then follow whichever they pick, using the steps in `SETUP.md`. Both are a download and
a couple of clicks. Neither needs a terminal. Read them the steps and wait until they
say it is done.

Verify before you believe them:

- **ElevenLabs**: check whether you have a `transcribe_audio` tool. If not, they have
  not restarted Claude Desktop yet. That is almost always the answer.
- **Local**: check that `tools/whisper-small.en/model.bin` exists.

Write `SETTINGS.md` with what they chose:

```markdown
# Settings

- Transcription: elevenlabs | local
- Set up on: <date>
```

They can switch later by asking. Set up the other one, change the line.

## Step 2. Name the project

Ask:

> What should I call this one?

Turn their answer into a lowercase folder name with dashes instead of spaces. Prefix it
with today's date as `mm-dd`, so "missed calls teardown" becomes `08-11_missed-calls`.
The date prefix keeps the folder sorted by when it was made, which is the order people
actually look for things in.

Create it inside `social-content` with three empty folders:

```
<mm-dd_name>/
  raw/     their footage goes here
  work/    intermediates, ignore it
  out/     the finished reel
```

## Step 3. Wait for footage

Tell them, with the real path filled in:

> Made it. Drop your video into
> **social-content/<mm-dd_name>/raw/** and tell me when it is in there.

Then stop. Do not guess at a file, do not look elsewhere on the machine, do not offer to
find something. Wait.

Two things worth saying while they are dropping it in, but only if this is one of their
first few projects:

- Turn HDR video off on the phone before the next shoot. Settings, Camera, Record Video,
  HDR off. It washes out once any other software touches it and nothing here can undo it.
- Film one long take and just say the line again when it goes wrong. Every attempt gets
  read and the best one is kept.

## Step 4. Cut the reel

Read `PROCEDURE.md`, `RULES.md` and `BRAND.md`, then run the procedure with the project
folder as the working directory. `RULES.md` outranks `PROCEDURE.md` wherever they
disagree, because it holds corrections the operator has already made.

Stop once, at step 5 of the procedure, and show them the cut before spending time on
captions. That is the only checkpoint.

Three files come out of it, all in the project's `out/`: the reel, a cover image, and a
text file of captions for Instagram, TikTok and YouTube. Do not stop after the video.
The last two steps of the procedure are what make it postable.

## Step 5. Close the loop

When it is done, say where the three files are and how long the reel runs. Remind them
the cover has to be uploaded by hand at posting time, since nothing about the file makes
that obvious. Then ask:

> Anything about that you would want done differently next time?

If they name something, write it into `RULES.md` as an instruction with the reason,
one or two lines. If they say no, leave the file alone. A rules file that fills up with
one-offs stops being worth reading.

---

## Rules for running this

- One question at a time. Never a list of four.
- Never print a terminal command for them to run. If a command is needed, you run it.
- Never move, rename or delete anything in a project's `raw/`. That is their footage and
  there may not be another copy.
- Search before fetching any URL. A direct fetch of a typed address gets refused here.
- If `BRAND.md` and what they just asked for disagree, do what they asked and ask
  whether to update `BRAND.md`.
