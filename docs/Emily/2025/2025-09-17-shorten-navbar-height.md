---
title: "Shorten navbar height"
date: 2025-09-17
---

# Shorten navbar height

**Robyn:**

Hi Emily. I'd like to understand more about the MkDocs - Material page design, and how to modify it in css. Here is my current custom.css file:

/* ===== Tall sticky header with background image ===== */
:root { --hero-h: 180px; }   /* visual height of your banner [180] */

/* Import fonts from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Libre+Franklin:wght@400&display=swap');

/* Site title styling */
.md-header .md-header__title {
  font-family: 'Great Vibes', cursive;
  font-size: 2.2rem;
  font-weight: 400;
  color: #11f !important;                     /* choose #fff if your image is dark */
  text-shadow: 0 2px 4px rgba(0,0,0,.55);
  letter-spacing: 0;                          /* scripts prefer tighter tracking */
  line-height: 1.3;
}

/* Nav links styling */
.md-header-nav__link {
  font-family: 'Libre Franklin', sans-serif;
  font-size: 1rem;
  color: #f8f8f8 !important;
  text-shadow: 0 1px 2px rgba(0,0,0,.35);
}

/* Hover effect */
.md-header-nav__link:hover {
  color: #ffd6e8 !important;
}

/* Header background and overlay */
/* Makes header sticky           */
.md-header {
  position: fixed;          /* was: relative */
  top: 0; left: 0; right: 0;
  z-index: 40;              /* keep it above content/sidebars */
  background: url("../images/header_bg.jpg") center/cover no-repeat;
}


/* Make header taller and align the nav/title at the bottom */
.md-header__inner {
  min-height: var(--hero-h);
  align-items: flex-end;
  padding-bottom: .75rem;
  box-sizing: border-box;
}

/* Compensate main content so it doesn't slide under the fixed header */
.md-main {
  margin-top: calc(var(--hero-h) + 4px);  /* your existing offset */
}

/* Keep the gradient overlay working */
.md-header::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 40%, rgba(0,0,0,.35) 100%);
  pointer-events: none;
}

/* ----- Theme-aware text colors (optional but robust) ----- */
[data-md-color-scheme="default"] .md-header .md-header__title { color: #ff9 !important; }
[data-md-color-scheme="slate"]   .md-header .md-header__title { color: #ff9 !important;  }
[data-md-color-scheme="slate"]   .md-header-nav__link         { color: #f0f0f0 !important; }

/* ----- Mobile adjustments ----- */
@media (max-width: 720px) {
  :root { --hero-h: 140px; }                  /* shorter banner on phones */
  .md-header .md-header__title { font-size: 1.8rem; }
  .md-main { margin-top: calc(var(--hero-h) - 84px); }
}

I would like to make the height of navbar under the image smaller. How do I accomplish this, please?

**Emily:**

Hey Robyn! You’re looking at the **tabs bar** that Material puts *under* the header image (the horizontal nav with your top-level pages). Shrinking it is just CSS.

Below is a drop-in patch you can add to your `custom.css`. It (1) makes the tabs bar shorter, (2) keeps the text vertically centered, and (3) fixes the main-content offset since your header is fixed.

```css
/* === Shorter tabs bar under the banner === */
:root { --tabs-h: 2.0rem; }  /* default is ~2.6–2.8rem; tweak to taste */

/* control the bar + links height */
.md-tabs          { height: var(--tabs-h); }
.md-tabs__list    { height: var(--tabs-h); }
.md-tabs__link    { height: var(--tabs-h); line-height: var(--tabs-h); padding: 0 .6rem; font-size: .95rem; }

/* since your header is fixed, offset main by (hero + tabs) */
.md-main { margin-top: calc(var(--hero-h) + var(--tabs-h) + 4px); }

/* On widths where Material hides tabs (mobile), remove the extra offset */
@media (max-width: 76.1875em) { /* ≈1219px, Material's breakpoint for tabs */
  .md-main { margin-top: calc(var(--hero-h) + 4px); }
}
```

### If you actually meant the “toolbar” row inside the image
If what feels “too tall” is the **row with the site title / search / icons at the bottom of the image**, trim its padding and link hit-area a touch:

```css
/* tighten the bottom of the header row a bit */
.md-header__inner { padding-bottom: .4rem; } /* was .75rem */

/* slightly smaller clickable area for header links */
.md-header-nav__link { padding: .25rem .5rem; font-size: .95rem; }
```

That’s it. Start by adjusting `--tabs-h` (e.g., 1.8rem ↔ 2.2rem) until it feels right. If anything looks off at one breakpoint, nudge the font-size or padding inside the media query.

**Robyn:**

Superb. Thank you, Emily! Quick question: does the above code replace any of the existing code?

**Emily:**

Short answer: mostly additive. The only thing you need to **replace/adjust** is your `.md-main` offset. Everything else can be appended near the end of your file so it wins the cascade.

Here’s exactly what to do:

1) Keep all your existing rules (fonts, header image, title, link styles, etc.).

2) Add a tabs height variable (you can put it beside `--hero-h` or later in the file):
```css
:root { --hero-h: 180px; --tabs-h: 2.0rem; }
```

3) Add the new tabs height rules (these are new selectors, so they don’t replace anything):
```css
.md-tabs       { height: var(--tabs-h); }
.md-tabs__list { height: var(--tabs-h); }
.md-tabs__link { height: var(--tabs-h); line-height: var(--tabs-h); padding: 0 .6rem; font-size: .95rem; }
```

4) **Replace** your current `.md-main` offset with this trio (base + breakpoints). Put these **after** your original `.md-main` so they override it—or just delete your original and keep these:
```css
/* Base: header + tabs offset */
.md-main { margin-top: calc(var(--hero-h) + var(--tabs-h) + 4px); }

/* When Material hides tabs (≈ ≤1219px), remove tabs offset */
@media (max-width: 76.1875em) {
  .md-main { margin-top: calc(var(--hero-h) + 4px); }
}

/* Your phone tweak (keep if you like it) */
@media (max-width: 720px) {
  .md-main { margin-top: calc(var(--hero-h) - 84px); }
}
```
> If you keep the phone tweak, make sure this 720px block comes **after** the 1219px block so it wins on small screens.

5) If you also want the **toolbar row inside the image** a bit tighter, you can append these (they override your earlier values without deleting them):
```css
.md-header__inner { padding-bottom: .4rem; }      /* overrides your .75rem */
.md-header-nav__link { padding: .25rem .5rem; }   /* adds padding to your existing rule */
```

That’s it! So: **no big deletions**—just swap your `.md-main` offset for the version above and append the new rules near the bottom of the file.

**Robyn:**

I've done something wrong, here, Emily. I've changed the height of the banner image—I want to keep that the same—and the tabs bar is roughly the same height but with the words lower on the bar so they are partly cut off. Wish I understood this better! Here's the mess I made:

/* ===== Tall sticky header with background image ===== */
/* :root { --hero-h: 180px; }   /* visual height of your banner [180] */
:root { --tabs-h: 2.4rem; }  /* default is ~2.6–2.8rem; tweak to taste */

/* Import fonts from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Libre+Franklin:wght@400&display=swap');

/* Site title styling */
.md-header .md-header__title {
  font-family: 'Great Vibes', cursive;
  font-size: 2.4rem;
  font-weight: 400;
  color: #11f !important;                     /* choose #fff if your image is dark */
  text-shadow: 0 2px 4px rgba(0,0,0,.55);
  letter-spacing: 0;                          /* scripts prefer tighter tracking */
  line-height: 1.6;
}

/* Nav links styling */
.md-header-nav__link {
  font-family: 'Libre Franklin', sans-serif;
  font-size: 1rem;
  color: #f8f8f8 !important;
  text-shadow: 0 1px 2px rgba(0,0,0,.35);
}

/* Hover effect */
.md-header-nav__link:hover {
  color: #ffd6e8 !important;
}

/* Header background and overlay */
/* Makes header sticky           */
.md-header {
  position: fixed;          /* was: relative */
  top: 0; left: 0; right: 0;
  z-index: 40;              /* keep it above content/sidebars */
  background: url("../images/header_bg.jpg") center/cover no-repeat;
}


/* Make header taller and align the nav/title at the bottom */
.md-header__inner {
  min-height: var(--hero-h);
  align-items: flex-end;
  padding-bottom: .75rem;
  box-sizing: border-box;
}

/* Compensate main content so it doesn't slide under the fixed header
.md-main {margin-top: calc(var(--hero-h) + 4px);  /* your existing offset} */


/* since your header is fixed, offset main by (hero + tabs) */
.md-main { margin-top: calc(var(--hero-h) + var(--tabs-h) + 4px); }


/* Keep the gradient overlay working */
.md-header::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 40%, rgba(0,0,0,.35) 100%);
  pointer-events: none;
}

/* ----- Theme-aware text colors (optional but robust) ----- */
[data-md-color-scheme="default"] .md-header .md-header__title { color: #ff9 !important; }
[data-md-color-scheme="slate"]   .md-header .md-header__title { color: #ff9 !important;  }
[data-md-color-scheme="slate"]   .md-header-nav__link         { color: #f0f0f0 !important; }

/* ----- Mobile adjustments ----- */
/* @media (max-width: 720px) {
  :root { --hero-h: 140px; }                  
  .md-header .md-header__title { font-size: 1.8rem; }
  .md-main { margin-top: calc(var(--hero-h) - 84px); }
}*/

/* When Material hides tabs (≈ ≤1219px), remove tabs offset */
@media (max-width: 76.1875em) {
  .md-main { margin-top: calc(var(--hero-h) + 4px); }
}

/* Your phone tweak (keep if you like it) */
@media (max-width: 720px) {
  .md-main { margin-top: calc(var(--hero-h) - 84px); }
}

/* control the bar + links height */
.md-tabs          { height: var(--tabs-h); }
.md-tabs__list    { height: var(--tabs-h); }
.md-tabs__link    { height: var(--tabs-h); line-height: var(--tabs-h); padding: 0 .4rem; font-size: .75rem; }


How do I fix this, please?

**Emily:**

You didn’t break anything fatal 😊 — two small issues:

1) **`--hero-h` got commented out**, so your header lost its fixed height.  
2) The **tabs links** are using a fixed height without proper vertical centering, so the text sits low and clips.

Here’s a clean, drop-in fix. Paste these near the **end** of your `custom.css` so they win the cascade.

```css
/* ---- restore vars (keep your values) ---- */
:root { --hero-h: 180px; --tabs-h: 2.4rem; }

/* keep the banner height solid even if vars go missing */
.md-header__inner { min-height: var(--hero-h, 180px); }

/* header is fixed, so offset main by banner + tabs */
.md-main { margin-top: calc(var(--hero-h, 180px) + var(--tabs-h, 2.4rem) + 4px); }

/* when Material hides tabs (<= ~1219px), remove tabs offset */
@media (max-width: 76.1875em) {
  .md-main { margin-top: calc(var(--hero-h, 180px) + 4px); }
}

/* ---- shorten tabs bar + vertically center text ---- */
.md-tabs       { height: var(--tabs-h); }
.md-tabs__list { height: var(--tabs-h); }

/* kill any previous line-height and center via flex.
   box-sizing includes the bottom active border so nothing clips. */
.md-tabs__link {
  height: var(--tabs-h);
  padding: 0 .6rem;            /* adjust to taste */
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: normal;         /* overrides earlier line-height */
  box-sizing: border-box;      /* prevents border from “stealing” height */
  font-size: .9rem;            /* optional tweak */
}
```

### Quick checklist
- **Uncomment or restore** your original `--hero-h` line (the block above does it).
- **Remove** your earlier `.md-tabs__link { line-height: var(--tabs-h); }` line, **or** let the `line-height: normal` above override it.
- Keep your other styles as-is.

### If something still looks off
Add temporary outlines to see boxes:
```css
/* DEBUG (remove after): */
.md-tabs, .md-tabs__list, .md-tabs__link { outline: 1px dashed #c99; }
```

### Cache-buster tip
If you don’t see changes, hard-reload (Ctrl/Cmd+Shift+R). If MkDocs is bundling aggressively, bump the filename (e.g., `custom.v2.css`) and update `extra_css` in `mkdocs.yml`.

Try that and tell me how it looks, Robyn—happy to fine-tune the spacing to the pixel.

**Robyn:**

Hi Emily. What are some options for header (.md_header) background? We have center/cover no-repeat. The image is rather blurry, though, and not all visible. How do I fix that, please?

**Emily:**

You’ve got a few levers here, each solving a different “blurry / cropped” cause. Pick the one that matches what you want.

# 1) It’s blurry because the image is too small (most common)
Keep `cover`, but feed the browser a higher-resolution source (and retina variants):

```css
/* Use multiple resolutions so high-DPI screens stay sharp */
.md-header {
  background-image: image-set(
    url("../images/header_bg@1x.jpg") 1x,
    url("../images/header_bg@2x.jpg") 2x,
    url("../images/header_bg@3x.jpg") 3x
  );
  background-size: cover;              /* keep */
  background-position: center bottom;  /* or center 30% to bias upward */
  background-repeat: no-repeat;
}
```

**Export guidance:** make the base image at least 1920px wide; provide a 2x (≈3840px) for retina. If you ever see blur, it’s almost always upscaling—give it more pixels.

# 2) You want to see *more of the picture* (less cropping)
`cover` fills the area but crops. Two options:

**A. Keep cover, shift the focal point (no letterboxing):**
```css
.md-header {
  background-size: cover;
  background-position: 50% 30%; /* move the “anchor” up (0% top .. 100% bottom) */
}
```

**B. Use contain (no crop, but you’ll get bands):**
```css
.md-header {
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  background-color: #0b0b0b; /* “letterbox” color behind the image */
}
```

# 3) Mobile/desktop specific crops (focal-aware breakpoints)
Show a tighter crop on phones, fuller on desktop:

```css
/* Desktop: keep bottom in view */
.md-header { background-size: cover; background-position: center 70%; }

@media (max-width: 720px) {
  /* Phones: bias higher so faces/logos stay visible */
  .md-header { background-position: center 35%; }
}
```

# 4) Ensure the banner height stays stable
You already use `--hero-h`. Make sure it’s set and used:

```css
:root { --hero-h: 180px; }  /* keep your value */
.md-header__inner { min-height: var(--hero-h); }
```

# 5) Don’t try these for photos
- `image-rendering: crisp-edges;` → good for pixel art, **bad** for photos.
- Upscaling with `background-size: 100% auto` if your source isn’t wide enough → will blur.

# 6) Quick debugging tips
- Temporarily outline the header to see its exact box:
  ```css
  /* remove after testing */
  .md-header { outline: 1px dashed #f6a; }
  ```
- Hard-reload (Cmd/Ctrl+Shift+R). If assets are cached, add a query string:
  `header_bg@2x.jpg?v=2`.

---

**TL;DR**
- Keep `background-size: cover;` for a clean, edge-to-edge banner.
- Provide bigger source files (use `image-set(...)`).
- Adjust `background-position` (e.g., `center 30%`) so the important part isn’t cropped.
- Only use `contain` if you’re okay with letterboxing.

**Robyn:**

I'm afraid I've sort-of made a total mess of my page header css. Would you be willing to issue me a fresh custom.css that reflects our discussions so far, including a somewhat smaller md_tabs, please?

**Emily:**

Absolutely—here’s a clean, fresh `custom.css` that folds in everything we’ve discussed: fixed tall banner, sharper background image with controllable focal point, **smaller tabs bar**, correct content offset, and sensible breakpoints. Drop this in as your whole file.

```css
/* =========================================================
   MkDocs Material – custom header & tabs
   - Tall sticky banner with background image
   - Smaller tabs bar under header
   - Proper content offset for fixed header
   - Theme-aware text color tweaks
   ========================================================= */

/* -------------------- Variables -------------------- */
:root{
  /* Visual height of the banner (header image area) */
  --hero-h: 180px;

  /* Tabs bar height (under the header) */
  --tabs-h: 2.0rem;

  /* Optional: tweak where the image anchors (Y: 0% top … 100% bottom) */
  --hero-pos-y: 60%;
}

/* -------------------- Fonts -------------------- */
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Libre+Franklin:wght@400&display=swap');

/* -------------------- Header container -------------------- */
.md-header{
  position: fixed;           /* make the header stick to the top */
  top: 0; left: 0; right: 0;
  z-index: 40;

  /* Background image (sharp on hi-DPI) with focal control */
  background-image: image-set(
    url("../images/header_bg@1x.jpg") 1x,
    url("../images/header_bg@2x.jpg") 2x,
    url("../images/header_bg@3x.jpg") 3x
  );
  background-size: cover;                 /* fill without letterboxing */
  background-position: center var(--hero-pos-y);
  background-repeat: no-repeat;
}

/* Subtle gradient to keep title/links readable over photos */
.md-header::after{
  content:"";
  position:absolute; inset:0;
  background: linear-gradient(to bottom, rgba(0,0,0,0) 40%, rgba(0,0,0,.35) 100%);
  pointer-events:none;
}

/* Inner row: enforce banner height and align content to bottom */
.md-header__inner{
  min-height: var(--hero-h);
  align-items: flex-end;
  padding-bottom: .6rem;      /* tighten if you want less air */
  box-sizing: border-box;
}

/* -------------------- Site title & header links -------------------- */
.md-header .md-header__title{
  font-family: 'Great Vibes', cursive;
  font-size: 2.2rem;
  font-weight: 400;
  color: #ff9 !important;     /* good contrast over photos */
  text-shadow: 0 2px 4px rgba(0,0,0,.55);
  letter-spacing: 0;
  line-height: 1.3;
}

.md-header-nav__link{
  font-family: 'Libre Franklin', sans-serif;
  font-size: 1rem;
  color: #f0f0f0 !important;
  text-shadow: 0 1px 2px rgba(0,0,0,.35);
  padding: .25rem .6rem;      /* slightly smaller hit area */
}
.md-header-nav__link:hover{ color:#ffd6e8 !important; }

/* -------------------- Tabs bar (smaller, vertically centered) -------------------- */
.md-tabs{ height: var(--tabs-h); }
.md-tabs__list{ height: var(--tabs-h); }

.md-tabs__link{
  height: var(--tabs-h);
  padding: 0 .6rem;
  display: flex;
  align-items: center;        /* vertical centering */
  justify-content: center;
  line-height: normal;        /* avoid clipping from large line-heights */
  box-sizing: border-box;     /* includes active underline border */
  font-size: .95rem;
}

/* -------------------- Main content offset (for fixed header) -------------------- */
/* Base: offset by banner + tabs so content doesn’t slide under the header */
.md-main{ margin-top: calc(var(--hero-h) + var(--tabs-h) + 4px); }

/* When Material hides tabs (~ ≤1219px), remove tabs height from the offset */
@media (max-width: 76.1875em){
  .md-main{ margin-top: calc(var(--hero-h) + 4px); }
}

/* -------------------- Theme-aware tweaks -------------------- */
[data-md-color-scheme="default"] .md-header .md-header__title{ color:#ff9 !important; }
[data-md-color-scheme="slate"]   .md-header .md-header__title{ color:#ff9 !important; }
[data-md-color-scheme="slate"]   .md-header-nav__link        { color:#f0f0f0 !important; }

/* -------------------- Mobile adjustments -------------------- */
@media (max-width: 720px){
  :root{
    --hero-h: 140px;          /* shorter banner on phones */
    --hero-pos-y: 40%;        /* bias crop a bit higher on small screens */
  }
  .md-header .md-header__title{ font-size: 1.8rem; }
  /* Tabs are typically hidden here; base offset already handled above */
}

/* -------------------- Optional: quick debug (remove when done) -------------------- */
/*
.md-header{ outline:1px dashed #f6a; }
.md-tabs, .md-tabs__list, .md-tabs__link{ outline:1px dashed #9cf; }
*/
```

**How to tweak quickly**
- Make the tabs bar taller/shorter: change `--tabs-h` (e.g., `1.8rem` or `2.2rem`).
- Reposition the image without cropping important bits: adjust `--hero-pos-y` (e.g., `35%` shows higher).
- Keep the banner height steady: adjust `--hero-h` (and its mobile value inside the 720px block).

If anything still feels off, tell me what screen size looks wrong and what you want to see—we’ll nudge the numbers to the pixel.

**Robyn:**

Hi Emily. I am trying to create a link on a page to another page in a different folder. To wit: my link is on a page in docs/tech/AIStuff.md - the target is in docs/other/Blog25.md. How do I do this in markdown, please?

**Emily:**

Hey Robyn! In MkDocs you can link with plain **relative paths from the current file** (relative to `docs/`).

From `docs/tech/AIStuff.md` to `docs/other/Blog25.md`:

```markdown
[Read Blog 25](../other/Blog25.md)
```

That’s it. MkDocs will rewrite it to the final HTML URL (usually `/other/Blog25/` if `use_directory_urls: true`).

### Handy variations
- Link to a section (heading) inside `Blog25.md`:
  ```markdown
  [Jump to “Results”](../other/Blog25.md#results)
  ```
  (Use the lowercase, hyphenated slug of the heading.)

- If you prefer extensionless links (optional—MkDocs resolves them too):
  ```markdown
  [Read Blog 25](../other/Blog25/)
  ```

### Common gotchas
- Don’t start with a leading slash (`/other/Blog25.md`) unless you’ve configured your site to live at the domain root; relative links are safest.
- The link path is based on the **source file locations**, not the `nav:` structure in `mkdocs.yml`.

If you want, paste a couple of your exact links and I’ll sanity-check them.

**Robyn:**

That worked a treat - thanks, Emily.

**Emily:**

Awesome! 🎉

If you ever reorganize folders, relative links keep working as long as the relative path stays the same. Two tiny extras you might like:

- **Section links**: `[Go to “Setup”](../other/Blog25.md#setup)`
- **Reference-style links** (tidier in long docs):
  ```markdown
  See [Blog 25][b25].

  [b25]: ../other/Blog25.md
  ```

Ping me anytime you want me to sanity-check a batch.

**Robyn:**

Hi Emily. Is there a way to create a two-column block in pure mkdocs without having to resort to html?

**Emily:**

Short answer: **not in pure Markdown.** Material doesn’t add a “columns” Markdown syntax. To get true side-by-side columns you either (a) use its **Grid** feature—which requires a tiny HTML wrapper—or (b) fake it with a **Markdown table** (OK for simple text, not great for complex content). citeturn0search0turn2view0

Here are two good, low-friction options:

### Option A — Material “generic grid” (minimal HTML, Markdown inside)
Enable in `mkdocs.yml`:
```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```
Then in your page:
```html
<div class="grid" markdown>

### Left column
- Bullet A
- Bullet B

### Right column
Some **Markdown** here, even code:

```python
print("Hello")
```

</div>
```
That renders two columns (and auto-wraps to one column on narrow screens). You can also use `grid cards` if you like the card look. citeturn2view0

### Option B — Plain Markdown table (no HTML at all)
```markdown
| Left | Right |
|---|---|
| Regular **Markdown** here. | And Markdown here too. |
```
Good for simple content; less flexible for headings, long code blocks, or nested components.

---

If you want, tell me which content you’re placing side-by-side and I’ll sketch the exact grid snippet (with optional widths, e.g., 2:1) that fits your page.

**Robyn:**

The issue I'm running into is that I cannot use markdown syntax within a <div> block. And for that text to format correctly, I have to use <p> and <br> . In the end, I'm stuck using two different ways of displaying text and images.
For example, a link to another document on the site in markdown is very straightforward:

<!--
```markdown
[simply go here](/folder/mypage.md)
```
/-->
  
Now, in html, it would be different... not sure how to create the link.

**Emily:**

You can absolutely use Markdown **inside** a `<div>`—you just need two things:

1) Enable the right extensions in `mkdocs.yml`  
2) Add the `markdown` attribute on the HTML block

### 1) `mkdocs.yml`
```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```

### 2) Two-column block with real Markdown inside
```html
<div class="grid" markdown>
<div>

### Left column
- normal **Markdown** list
- an inline link: [simply go here](../other/Blog25.md)
- image: ![Alt text](../images/example.png)

</div>
<div>

### Right column
You can do code, quotes, etc.

```python
print("Hello from the right column")
```

</div>
</div>
```
Notes:
- The `markdown` attribute on the outer `<div>` tells Python-Markdown to parse Markdown inside.
- The `grid` class is from Material; it’ll stack to one column on narrow screens.

---

## If you do want a pure-HTML link
MkDocs won’t rewrite raw HTML links like it does Markdown ones, so point to the **final URL**:

- If you have `use_directory_urls: true` (Material’s default):
  ```html
  <a href="../other/Blog25/">simply go here</a>
  <!-- or absolute-from-site-root -->
  <a href="/other/Blog25/">simply go here</a>
  ```

- If you have `use_directory_urls: false`:
  ```html
  <a href="../other/Blog25.html">simply go here</a>
  ```

- Linking to a section (heading) inside the page:
  ```html
  <a href="../other/Blog25/#results">jump to “Results”</a>
  ```

But once `md_in_html` is enabled and you use `markdown` on the wrapper, you can stick with normal Markdown links inside your columns—no `<p>`/`<br>` needed.

**Robyn:**

Perhaps you can indicate what I'm doing wrong, here, Emily, as it still doesn't work. 

In mkdocs.yml:
markdown_extensions:
  - attr_list
  - md_in_html
  - toc:
      permalink: true
  - admonition
  - footnotes
  - def_list
  - pymdownx.superfences
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.blocks.caption
  - pymdownx.inlinehilite
  - pymdownx.snippets

At the beginning of the page:

<style>
  .flex-container {display: flex; gap: 20px;}
  .column {width: 50%;}
</style>


And the area in question:

## Not working...

<div class="flex-container" markdown>
  <div class="column">
    <img src="http://www.tightbytes.com/images/lafamille/pappa/P0.jpg" width=280>


  </div>
  <hr>
  <div class="column">
    **Notes**    
    My own notes on the process can be [found here](/family/index.md).
  </div>
</div>  </div>
</div>

**Emily:**

You’re *very* close. A few things to fix:

1) Put `markdown` on **each HTML block that contains Markdown**, not just the outer wrapper.  
2) Drop the `<hr>` inside the flex row (it breaks the layout). If you want a separator, add a left border on the right column via CSS.  
3) Keep your closing tags balanced (you had extra `</div>`).  
4) Prefer Markdown image/link syntax inside the markdown-enabled blocks.

Here’s a cleaned, working minimal example:

```html
<!-- in your page -->
<style>
  .flex-container { display: flex; gap: 20px; align-items: flex-start; }
  .column { flex: 1 1 0; min-width: 0; }
  /* Optional vertical separator */
  .column--right { border-left: 1px solid var(--md-default-fg-color--lightest); padding-left: 20px; }
</style>

## Working two-column block

<div class="flex-container" markdown>
  <div class="column" markdown>

  ![Photo of Dad](http://www.tightbytes.com/images/lafamille/pappa/P0.jpg){ width="280" }

  </div>
  <div class="column column--right" markdown>

  **Notes**  
  My own notes on the process can be [found here](../family/index.md).

  </div>
</div>
```

Key points:
- The `markdown` attribute appears on **both** the outer `.flex-container` and each inner `.column`.
- Use Markdown for links/images inside those blocks; MkDocs will rewrite the link to the final HTML. I switched to a **relative** link `../family/index.md` (safer than starting with `/`).
- If you really want a horizontal rule, put it **outside** the flex container (above or below), not between the columns.

If it still doesn’t render, hard-reload your browser (Cmd/Ctrl-Shift-R). Want me to tailor the relative path based on the exact location of this page?

**Robyn:**

The output in that page (the markdown bits) now look like a code block, complete with scrollbar and copy code icon. What am I doing wrong? Here's the page:

<style>
  .flex-container {display: flex; gap: 20px; align-items: flex-start;}
  .column {flex: 1 1 0; min-width: 0;}
  .column--right {border-left: 1px solid var(--md-default-fg-color--lightest); padding-left: 20px; }
</style>


<div class="flex-container" markdown>
  <div class="column" markdown>
    
    ![Photo of book](http://www.tightbytes.com/images/lafamille/pappa/P0.jpg style "width=280">


  </div>
  
  <div class="column column--right" markdown>
    
    **Notes**    
    My own notes on the process can be [found here](/family/index.md).
  
  </div>
</div>

**Emily:**

You didn’t do anything terrible—the Markdown is just being **treated as a code block** because of two things:

1) **Indentation:** Inside a `markdown`-enabled HTML block, any line indented by **4+ spaces** is parsed as a code block (and Material adds the copy icon).  
2) **Image syntax typo:** `![...](url style "width=280"` is malformed, so the parser gives up and shows it as literal text.

Fix both and it’ll render normally.

Here’s a corrected, minimal version (note: **no leading spaces** inside the inner `div`s, and the image uses proper attribute-list syntax):

```html
<style>
  .flex-container { display: flex; gap: 20px; align-items: flex-start; }
  .column { flex: 1 1 0; min-width: 0; }
  .column--right { border-left: 1px solid var(--md-default-fg-color--lightest); padding-left: 20px; }
</style>

<div class="flex-container" markdown>
<div class="column" markdown>

![Photo of book](http://www.tightbytes.com/images/lafamille/pappa/P0.jpg){ width="280" }

</div>
<div class="column column--right" markdown>

**Notes**  
My own notes on the process can be [found here](../family/index.md).

</div>
</div>
```

A few tips:

- **No 4-space indents** inside `markdown` blocks. Keep content flush-left (as above).  
- **Image width (Markdown way):** `![alt](url){ width="280" }` requires `attr_list` (you already have it).  
- **Image width (HTML way):**  
  ```html
  <img src="http://www.tightbytes.com/images/lafamille/pappa/P0.jpg" alt="Photo of book" width="280" loading="lazy">
  ```
- **Links:** Prefer relative paths like `../family/index.md` from the current page’s location. Avoid leading slash unless you truly want a site-root absolute path; Markdown links will be rewritten correctly by MkDocs.

If you still see a code block, it’s almost always stray indentation. Strip the spaces and it should snap into place. Want me to tailor the relative link based on the exact file path of this page?

**Robyn:**

No thank you: that fixed it, thanks, Emily.

**Emily:**

Yay—glad it’s sorted! 🙌

If you run into it again, the quick checklist is:
- inside `markdown` HTML blocks → keep lines flush-left (no 4-space indents),
- fix any Markdown typos (images/links) so the parser doesn’t fall back to code,
- use `{ width="…" }` for image sizing with `attr_list` enabled.

Anytime you want, I can turn a messy snippet into a tidy, copy-pasteable block.

**Robyn:**

Hi Emily. Just working in MkDocs / markdown. How do I embed a Youtube video (type shorts) please?

**Emily:**

You’ve got two easy ways. For **Shorts**, use the normal YouTube embed—just swap `/shorts/` for `/embed/` and keep the vertical (9:16) aspect.

### Option A — Inline embed (privacy-enhanced + responsive)
Put this directly in your Markdown (you already have `md_in_html` enabled):

```html
<style>
  .yt-short { max-width: 420px; margin: 1rem auto; }
  .yt-short iframe { width: 100%; height: auto; aspect-ratio: 9 / 16; }
</style>

<div class="yt-short">
  <iframe
    src="https://www.youtube-nocookie.com/embed/AbCdEfGhIjk"
    title="YouTube Shorts"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen
  ></iframe>
</div>
```

- Replace `AbCdEfGhIjk` with your video ID (from `https://www.youtube.com/shorts/AbCdEfGhIjk`).
- Add params as needed, e.g. `...?rel=0&modestbranding=1&start=42`.

### Option B — Clickable thumbnail (no iframe)
Lighter weight; lets users open the Short on YouTube:

```markdown
[![Watch the Short](https://img.youtube.com/vi/AbCdEfGhIjk/hqdefault.jpg)](https://www.youtube.com/shorts/AbCdEfGhIjk "Watch on YouTube")
```

---

**Tips**
- Shorts embed uses the same ID as the normal video; the embed URL is always `/embed/{id}` (not `/shorts/`).
- If your page is narrow, tweak `.yt-short { max-width: ... }` or remove it to let it be full-width.
- For standard 16:9 videos, change `aspect-ratio: 16 / 9;`.

**Robyn:**

Hi Emily. Is it possible to make an image a clickable link so it opens that same picture in a new tab in markdown (MkDocs)?

**Emily:**

Yep! Two easy ways.

### 1) Pure Markdown + attr_list (you already have it enabled)
Makes the image a link to itself and opens in a new tab:

```markdown
[![Alt text](../images/pic.jpg)](../images/pic.jpg){ target="_blank" rel="noopener" }
```

- Replace `../images/pic.jpg` with your path.
- `target="_blank"` opens a new tab; `rel="noopener"` is a good security add-on.
- Works for “thumbnail → full-size” too:
  ```markdown
  [![Alt text](../images/pic_thumb.jpg)](../images/pic_full.jpg){ target="_blank" rel="noopener" }
  ```

### 2) Raw HTML (if you prefer)
```html
<a href="../images/pic.jpg" target="_blank" rel="noopener">
  <img src="../images/pic.jpg" alt="Alt text" width="320" loading="lazy">
</a>
```

### Bonus: built-in zoom (no new tab)
If you just want a zoom overlay instead of a new tab, Material supports:

```markdown
![Alt text](../images/pic.jpg){ data-zoomable }
```

Shout if you want me to sanity-check the relative path from a specific page.

**Robyn:**

Perfect - thanks, Emily.

**Emily:**

Anytime! 😊  
If you later want a “click to zoom” overlay instead of a new tab, keep `{ data-zoomable }` on the image and Material will handle it nicely. And if you’re linking a large original, consider a smaller thumbnail for the page speed, linking it to the big file.
