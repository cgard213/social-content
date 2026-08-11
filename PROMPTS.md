# Prompts

Two things to copy and paste. After that you use the skill and never come back here.

Paste them into Cowork with this folder open. Cowork is the tab in Claude Desktop that
can see your files. Not a normal Claude chat, and not a terminal.

---

## 1. Set up

Once, the very first time.

```
This folder is a video toolkit. Read SETUP.md, then get me set up.

Confirm the create-social-content skill is available to you. If it is not, read
.claude/skills/create-social-content/SKILL.md yourself and follow it directly
when I ask for a new project.

Check that ffmpeg is here and that it can burn subtitles, and tell me in plain
language whether anything is missing. Assume I will not be fixing it myself.

Then walk me through the two setup questions from the skill, one at a time: my
brand guide, and which transcription I want. Do not ask them both at once.

Finish by telling me the one thing I type to start a video.
```

---

## 2. Start a video

Every time after that.

```
/create-social-content
```

If typing that does nothing, say this instead and it will work the same way:

```
Start a new social content project.
```

The skill takes it from there. It asks what to call the project, makes the folder, and
tells you where to drop your video. Then it cuts it.

---

## When it gets something wrong

Tell it what you wanted, then:

```
Add that to RULES.md so it does not happen again.
```

Wait until the same thing has annoyed you twice. Once is bad luck, twice is a pattern,
and a rules file full of one-offs stops being worth reading.

Fill in the complaint however it comes out of your head. "You cut me off mid-sentence at
the end, I wanted the last word to breathe" is a perfectly good rule. It does not have
to sound technical.
