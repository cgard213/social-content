# Start here

This folder is a video editor. You talk to it, it cuts your footage.

Tell it to start a project, drop a clip in, and it transcribes what you said, keeps the
cleanest take of each line, cuts the dead air, burns captions in your colors, and writes
a finished vertical MP4.

You will not type a single command. Every project you make gets its own folder in here,
so a month from now you can still find the raw file that went with a reel.

## What you need

Claude Desktop, with Cowork. That is the whole list.

## Setup

1. Open the Google Drive folder you were sent and download `social-content.zip`.
2. Unzip it onto your Desktop. Keep the folder named `social-content`.
3. Open Claude Desktop, click Cowork, point it at that folder.
4. Open `PROMPTS.md`, copy the first prompt, paste it in.

It checks the folder over and then asks you a few questions about your brand and how you
want your audio transcribed. Everything below is what it will ask, if you would rather
read ahead.

One thing that will not work, in case you try it: asking Cowork to download the project
for you. It can only reach a short list of approved addresses and Google Drive is not
one of them. The browser download above is the way in.

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
Free for about 30 minutes of footage a month, then roughly 22 cents an hour.

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

1. In the same Drive folder, download `whisper-small.en.zip`. It is about 300 MB, so
   Drive will warn that it cannot scan it for viruses. Click download anyway.
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
