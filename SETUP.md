# Start here

This folder is a video editor. You talk to it, it cuts your footage.

Tell it to start a project, drop a clip in, and it transcribes what you said, keeps the
cleanest take of each line, cuts the dead air, burns captions in your colors, and writes
a finished vertical MP4.

You will not type a single command. Every project you make gets its own folder in here,
so a month from now you can still find the raw file that went with a reel.

## What you need

Claude Desktop, with Cowork. That is the only thing you have to have.

Optionally, an ElevenLabs account. It is free, it takes about a minute, and no card is
involved. It transcribes your audio more accurately than the built-in option, which
means the cuts land cleaner. Setup asks you which one you want and there is a local
option that needs no account at all, so you can skip this and decide later.

## Setup

**1. Get the folder.** Go to **github.com/cgard213/social-content**, click the green
**Code** button, then **Download ZIP**.

**2. Unzip it onto your Desktop** and rename the folder to `social-content`. GitHub adds
`-main` to the end of the name and you do not want that.

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

That is the last thing you have to copy. It checks the folder, asks you three or four
questions, and then offers to make your first video on the spot.

The rest of this page is what it is going to ask, in case you would rather read ahead
than think on the spot.

One thing that will not work, in case you try it: asking Cowork to download the project
for you. It can only reach a short list of approved addresses and GitHub is not one of
them. The browser download in step 1 is the way in.

## Question one: your brand

Captions come out in your colors and your font, so it needs to know them.

If you have a brand guide, hand it over however it exists. Paste the text, drop the PDF
in this folder, or just describe it. If you do not have one, give it your website
address and it will read the site and write you a simple one. Check what it comes back
with. Websites carry all sorts of colors that have nothing to do with the brand.

It also asks for two things a website cannot tell it. One is the fixed line that sits on
every cover image, the top line that never changes. The other is how you sound, which is
what your social captions get written from.

All of it lands in `BRAND.md` and you can edit that file whenever you want.

## Question two: how to transcribe

It has to turn your audio into words with timings before it can cut anything. Two ways,
and you can switch later by asking.

### ElevenLabs, the accurate one

Better word timings, so cuts land cleaner and captions sit tighter against the audio.
The account is free and asks for no card. It covers about 30 minutes of footage a month,
and only if you go past that does it cost anything, at roughly 22 cents an hour.

1. Go to elevenlabs.io and make a free account.
2. Click your profile, then API keys, and copy the key.
3. Back here, double-click `elevenlabs-stt.mcpb`. Claude Desktop opens an install
   window and asks for two things: paste the key, and pick this folder.
4. Quit Claude Desktop and open it again. It will not work until you do, and this is
   the step everyone skips.

The 30 free minutes go faster than you think, because every restart and every flubbed
line is still audio you paid to transcribe.

### Local, the free one

Runs on your own machine. Nothing leaves it, no account, no card, free for good. Word
timings are a little looser than ElevenLabs, which mostly shows up as a cut landing a
hair early or late.

1. On the same GitHub page, click **Releases** in the right-hand column, then download
   `whisper-small.en.zip`. It is about 430 MB and will take a few minutes.
2. Unzip it.
3. Drag the `whisper-small.en` folder into the `tools` folder in here.

That is it. Nothing to sign up for and nothing to restart.

Not sure? Take ElevenLabs. There is nothing to download, the free tier covers more
footage than most people shoot in a month, and you will not be asked for a card until
you go past it. Local is there for when you would rather nothing left your machine at
all, and you can switch by asking.

## Making a video

Type `/create-social-content`, or just say "start a new social content project."

It asks what to call it, makes a folder for it, and tells you where to put your video.
Drop the clip in, say it is there, and it goes. It stops once to show you the cut before
it spends time on captions, so you get a say before the slow part.

Three things come out, in that project's `out` folder:

- `reel.mp4`, the finished video with captions burned in
- `cover.png`, the image for the profile grid. You upload this by hand when you post,
  otherwise the platform picks its own frame and it always picks a bad one
- `captions.txt`, the caption written three ways, for Instagram, TikTok and YouTube

## Two things worth doing before you film

Turn off HDR video on your phone. Settings, Camera, Record Video, HDR off. Apple's HDR
looks terrific in Photos and then washes out the moment any other software touches it.
Nothing in this folder can fix that afterwards. It has to happen before the shot.

Then film one long take, and when you flub a line, just say it again. Do not stop
recording. Every attempt gets read and the best one is kept, so a restart costs you
eight seconds instead of a second session. You will also deliver the fourth attempt
better than the first, which is most of why this works.

## When it gets something wrong

Tell it what you wanted and ask it to add that to `RULES.md`.

That file is the point of the whole thing. It starts nearly empty and fills up with the
specific things you care about, which is how the tool stops making the same mistake
twice. After five or six videos it will be doing things you no longer have to ask for.
