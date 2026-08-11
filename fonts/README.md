# Fonts

Drop your caption font's TTF files in this folder, then name the font in `BRAND.md`.

The name in `BRAND.md` has to match what the file calls itself internally, which is not
always what the filename suggests. A file called `Geist-Black.ttf` often registers as
family `Geist Black` with a regular subfamily, so asking for `Geist` in bold quietly
gets you Geist Bold instead. Everything then looks slightly wrong in a way that is hard
to point at.

You do not have to work this out yourself. Ask Cowork:

> Check the font files in fonts/ and tell me exactly what to put as the font name in
> BRAND.md.

If this folder is empty, captions still render, using whatever font the system can find.
It just will not be yours.
