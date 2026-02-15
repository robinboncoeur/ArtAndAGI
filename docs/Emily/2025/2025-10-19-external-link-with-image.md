---
title: "External link with image"
date: 2025-10-19
---

# External link with image

**Robyn:**

Hi Emily. Please give me a stable diffusion prompt, just the positive, it should be natural language, just a beautiful woman's face, hyper-realistic, with expressive eyes.

**Emily:**

A hyper-realistic close-up portrait of a beautiful adult woman, head and shoulders, centered, expressive eyes with bright catchlights, gentle natural smile, minimal makeup, soft diffused daylight, finely detailed skin texture and subtle freckles, smooth even complexion, balanced facial symmetry, shallow depth of field with creamy background bokeh, shot on an 85mm prime, elegant editorial beauty photography.

**Robyn:**

Hi Emily. I'm pretty sure you've told me this, but I forgot: how do I ceate an external link in html using an image?

**Emily:**

You wrap the `<img>` in an `<a>` tag. Here’s the clean, accessible version:

```html
<a href="https://example.com" target="_blank" rel="noopener noreferrer" title="Open example.com">
  <img src="/path/to/image.jpg"
       alt="Descriptive text of the image"
       width="600" height="400"
       loading="lazy">
</a>
```

Quick notes:
- `target="_blank"` opens in a new tab.
- `rel="noopener noreferrer"` is a security/perf best practice when using `_blank`.
- Always include a meaningful `alt` for accessibility.
- `loading="lazy"` defers image load until needed; keep or drop as you prefer.
- Make it responsive with CSS:

```css
a img { max-width: 100%; height: auto; display: block; }
```

(If you ever want the Markdown shorthand: `[![alt text](/path/to/image.jpg)](https://example.com)`.)

**Robyn:**

Ideal. Thanks, Emily.

**Emily:**

Anytime! If you want variants (same-tab, download link, captioned figure, or a responsive `<picture>` setup), just say the word.

**Robyn:**

Hi Emily. I have a CSS question for you: please give me a very simple <style> </style> thingie I can insert on a page where I want two small (384 x 384 px) videos to play side by side, in my MkDocs file. The videos need to be in an <iframe src=... container.

**Emily:**

Here’s a drop-in snippet you can paste right into your MkDocs page:

```html
<style>
  /* two 384×384 iframes side by side */
  .video-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;
  }
  .video-row iframe {
    width: 384px;
    height: 384px;
    border: 0;
    border-radius: 8px; /* optional */
  }
  /* Stack on narrow screens */
  @media (max-width: 820px) {
    .video-row { flex-direction: column; align-items: center; }
  }
</style>

<div class="video-row">
  <iframe
    src="YOUR_VIDEO_URL_1"
    title="Video 1"
    loading="lazy"
    allow="autoplay; fullscreen; picture-in-picture"
    allowfullscreen>
  </iframe>

  <iframe
    src="YOUR_VIDEO_URL_2"
    title="Video 2"
    loading="lazy"
    allow="autoplay; fullscreen; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>
```

Swap in your iframe `src` URLs. This keeps each player exactly 384×384 on desktop, centers them with a gap, and stacks them on small screens.

**Robyn:**

Elegant. Thank you!

**Emily:**

You’re very welcome!  
Tiny optional tweak: if you ever want them to scale down on narrow pages, swap the fixed size rule for:

```css
.video-row iframe { aspect-ratio: 1 / 1; width: min(384px, 100%); height: auto; }
```

Same look, but gracefully responsive.
