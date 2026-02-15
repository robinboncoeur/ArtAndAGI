---
title: "Fix 1:1 video ratio"
date: 2025-10-11
---

# Fix 1:1 video ratio

**Robyn:**

Hi Emily. I have a video on Cloudflare with a 1:1 aspect ratio. This code:

<div style="position:relative;padding-top:56.25%">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>

seems to show the video in 9:16 (height:width) aspect ratio. How do I get it to display in 1:1, please?

**Emily:**

Hey Robyn! Your wrapper is forcing a 16:9 box — `padding-top:56.25%` is the classic 16:9 hack (0.5625 = 9/16). For a square, make the container 1:1.

Quick fix (keep your current pattern):
```html
<div style="position:relative;padding-top:100%">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>
```

Modern (cleaner) approach using `aspect-ratio`:
```html
<div style="aspect-ratio:1/1;width:100%;max-width:640px;">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:0;width:100%;height:100%;"></iframe>
</div>
```

Either way, the player will letterbox if the video isn’t exactly square, but since yours is 1:1 it’ll fill perfectly.

**Robyn:**

You're a legend, Emily... thank you!

**Emily:**

Anytime, Robyn! 🙌

Tiny pro tip for polish:
```html
<div class="cf-player">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen></iframe>
</div>

<style>
  .cf-player{
    aspect-ratio:1/1;
    width:100%;
    max-width:480px;     /* cap size if you like */
    margin:auto;         /* center it */
  }
  .cf-player iframe{
    width:100%;
    height:100%;
    border:0;
  }

  /* Fallback for very old browsers:
  .cf-player{position:relative;padding-top:100%}
  .cf-player iframe{position:absolute;inset:0}
  */
</style>
```

That’ll keep it perfectly square, responsive, and nicely centered.

**Robyn:**

I'll give that a go, thanks!

**Emily:**

Awesome—have fun! Two tiny polish tweaks you might like:

1) add lazy-loading + a11y title  
2) make the iframe a block element (removes the little baseline gap some browsers add)

```html
<div class="cf-player">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe"
    title="Cloudflare Stream video"
    allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
    allowfullscreen
    loading="lazy"></iframe>
</div>

<style>
  .cf-player{
    aspect-ratio:1/1;
    width:100%;
    max-width:480px;
    margin:auto;
    background:#111;          /* pleasant placeholder while loading */
    border-radius:12px;
    overflow:hidden;
  }
  .cf-player iframe{
    display:block;
    width:100%;
    height:100%;
    border:0;
  }
</style>
```

If it still looks too tall anywhere, check for a parent element enforcing its own aspect ratio or fixed height—happy to peek if you paste that container’s CSS.

**Robyn:**

Hi Emily. I'm on a Macbook Pro. All of a sudden, my background on YouTube defaults to light, no matter how often I set it to either device setting (my Mac background is dark) or dark. The problem appears to be only YouTube: OpenAI (this site) respects my settings. So, it's YouTube only. Is there some setting I can change, please, to keep the YouTube background consistently dark? I have already cleared cache.

**Emily:**

Got you, Robyn. YouTube’s theme can be stored per-account (server-side) or per-browser via cookies/local storage. If that storage gets blocked/cleared—or you’re switching Google profiles—it snaps back to light. Here’s a tight fix list that usually nails it:

1) Set it to “Dark” (not “Use device theme”)
- On YouTube, click your avatar → Appearance → pick Dark (explicitly).  
- Refresh the page. If you switch Google accounts/channels, set it for each one.

2) Reset YouTube’s site data (cache isn’t enough)
- **Chrome**: YouTube tab → click the lock icon → Site settings → “Delete data”.  
  Or Settings → Privacy & security → Site settings → “View permissions and data stored across sites” → search “youtube” → Remove.  
- **Safari**: Settings → Privacy → Manage Website Data… → search “youtube” (and “google”) → Remove.

Then go back to YouTube and set Appearance → Dark again.

3) Make sure nothing auto-clears cookies/site data
- **Chrome**: Settings → Privacy & security → Cookies and other site data → ensure “Clear cookies and site data when you close all windows” is **off**.  
  In “Customised behaviours”, add **[*.]youtube.com** and **[*.]google.com** to “Sites that can always use cookies”.
- If you use extensions (uBlock, Privacy Badger, Cookie AutoDelete, etc.), whitelist YouTube so it doesn’t wipe its storage.

4) Quick isolation test
- Open an **Incognito** (or Safari Private) window with **extensions disabled**. Sign into YouTube, set Dark.  
  - If it sticks there, an extension or per-site cookie rule in your normal profile is the culprit.

5) Chrome flags (edge case)
- In the address bar: `chrome://flags` → search “Auto Dark Mode for Web Contents”. Set to **Default** or **Disabled** (conflicts can cause odd theme behaviour). Relaunch.

If it’s still reverting after those, tell me your browser (Chrome/Safari/Firefox) and whether you’re signed in or using multiple Google profiles—I’ll tailor exact clicks.

**Robyn:**

That worked, Emily. Thank you. It was driving me crazy! I'm going to save this conversation as this isn't the first time I've run into this. Thanks so much.

**Emily:**

Yay—glad we tamed it! 🎉

I put a tiny one-pager together so you don’t have to hunt next time:
[Download the cheat sheet](sandbox:/mnt/data/yt-dark-mode-mac-cheatsheet.md)

If it pops up again and the sheet doesn’t fix it, ping me with your browser + any extensions you’re running and I’ll zero in.

**Robyn:**

Thanks - got it saved in my project.tightbytes.com site, where I store all this stuff (well, most of the time)...

**Emily:**

Love it. 💾

If you want to turn fixes like this into tidy, reusable pages in your MkDocs site, here’s a tiny template you can paste and adapt for each “gotcha”:

```markdown
# YouTube Dark Theme Won’t Stick

!!! success "TL;DR"
    Set **Appearance → Dark** (not “Use device theme”), clear **YouTube site data**, and make sure nothing is auto-clearing cookies.

??? tip "Why this happens"
    YouTube stores theme per Google profile and in site storage. If cookies/local storage get wiped or you switch profiles, it reverts.

=== "Chrome"
- YouTube → avatar → **Appearance → Dark**
- URL bar lock → **Site settings → Delete data**
- Settings → Privacy & security → **Cookies** → ensure “Clear cookies on close” **Off**; whitelist `youtube.com`

=== "Safari"
- YouTube → avatar → **Appearance → Dark**
- Settings → **Privacy → Manage Website Data…** → remove `youtube.com` / `google.com`

=== "Firefox"
- YouTube → avatar → **Appearance → Dark**
- Settings → Privacy & Security → **Cookies and Site Data → Manage Data…** → remove `youtube.com`

??? bug "Still not sticking?"
- Try a Private/Incognito window with extensions disabled.  
- In Chrome, check `chrome://flags` → **Auto Dark Mode for Web Contents** = Default/Disabled.
```

(Uses Material’s **admonitions**, **details**, and **tabs**—which you likely already have enabled. If you want, I can tune it to your exact `mkdocs.yml` setup.)

Need a similar sheet for Cloudflare Stream embeds or anything else? I’ll whip one up.
