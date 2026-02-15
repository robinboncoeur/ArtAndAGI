---
title: "Prompt analysis feedback"
date: 2025-11-19
---

# Prompt analysis feedback

**Robyn:**

Hi Emily. I just now tried to create an image using this prompt:

1st woman "moimeme3", young, has light skin, long brown hair in an updo, and is wearing a fitted white tank top paired with a pink cardigan and high-waisted red mini skirt that emphasizes her curvy physique and medium-sized breasts. She also wears black ankle-strap heels, giving a sleek, professional vibe to her outfit.  This photograph captures a provocative interaction between two women in a softly lit pink-walled room.  In the blurred background, there are two other women seated at a table, engaged in conversation and adding depth to the scene. The room has a light pink hue which contrasts against their darker outfits, and the textures of the wall and floor are smooth, indicative of modern design elements. Overall, the photograph creates a provocative, intimate atmosphere, emphasizing power dynamics through subtle, suggestive details.   2st woman "celestesh", medium skin and long brown hair falling past her shoulders. She is dressed in an all-black ensemble comprising of a button-up shirt and slacks that highlight her slender but shapely figure. She is gently resting her left hand on the face of the 1st woman, applying soft pressure with her fingers while gazing intently into her eyes. This act of intimate interaction exudes a sense of dominance and submission.  This photograph captures a provocative interaction between two women in a softly lit pink-walled room.  In the blurred background, there are two other women seated at a table, engaged in conversation and adding depth to the scene. The room has a light pink hue which contrasts against their darker outfits, and the textures of the wall and floor are smooth, indicative of modern design elements. Overall, the photograph creates a provocative, intimate atmosphere, emphasizing power dynamics through subtle, suggestive details. 

I see nothing pornographic or even salacious about this prompt. However, the OpenAI image generator balked at using it to create an image. Can you analyse my prompt and point out which words tripped up 'image generator', please?

**Emily:**

You’re right that there’s nothing overtly pornographic in what you wrote, but there *are* a few clusters of words/phrases that, together, will very likely trip OpenAI’s image filters.

I don’t have access to the exact internal rules or logs for *your* request, but based on the public safety rules I can say with pretty high confidence where the model started clutching its pearls:

---

### 1. Sexual / fetish-coded power dynamics

These phrases are the biggest red flags:

- **“provocative interaction”**  
- **“intimate atmosphere” / “intimate interaction”**  
- **“emphasizing power dynamics through subtle, suggestive details”**  
- **“sense of dominance and submission”**

Even though everyone is fully clothed, that combination of:

- “provocative”
- “intimate”
- “dominance and submission”
- “power dynamics”

reads *to a safety filter* as **BDSM-coded / fetish-adjacent content**, which is explicitly disallowed for image generation, even if it’s visually tame.

On their own, some of those words might be fine. Together, and in a context that explicitly frames the scene as dominance/submission, they’re very likely what caused the refusal.

---

### 2. Body/sexual focus wording

You also have:

- **“high-waisted red mini skirt that emphasizes her curvy physique and medium-sized breasts”**

Describing clothing is fine; describing body shape is often fine. But “emphasizes … breasts” in the same prompt as “provocative,” “intimate interaction,” and “dominance and submission” can tilt the classifier toward **“sexualized content”** rather than neutral fashion.

Again, not because *you* wrote anything explicit, but because the filters are conservative and pattern-based.

---

### 3. Repetition of the charged framing

You repeat this general framing twice:

> “This photograph captures a provocative interaction between two women in a softly lit pink-walled room… Overall, the photograph creates a provocative, intimate atmosphere, emphasizing power dynamics through subtle, suggestive details.”

That repetition reinforces to the filter:  
“Okay, this isn’t just a candid moment, the *point* of the image is a suggestive, power-dynamic-heavy interaction.”

So even if the pose itself is mild (hand on cheek, close eye contact), the *language* is doing a lot of sexualized heavy lifting.

---

### So, which bits most likely triggered it?

If I had to highlight the prime suspects:

- **“provocative interaction”**  
- **“provocative, intimate atmosphere”**  
- **“emphasizing power dynamics through subtle, suggestive details”**  
- **“sense of dominance and submission”**  
- plus the phrase **“emphasizes her… breasts”** in that context

Those together are almost certainly what caused the system to say “nope.”

---

If you’d like, I can:

- help you rephrase this into something that keeps the mood (confident, controlling woman; yielding but fully-clothed partner; strong female presence)  
- but stays firmly in “stylish portrait / cinematic still” territory rather than “sexual power play” in the eyes of the filters.

You wouldn’t have to dull the *feminine authority* or the emotional charge, just tweak the vocabulary away from “dominance/submission” and “provocative.”

**Robyn:**

Right-o - that makes sense. Funny how one sees the words and can't appreciate the implications. Fair enough: perhaps I've been inured to the potential for abuse through much exposure.

**Emily:**

Yeah, that happens *so* easily – especially when you spend a lot of time in spaces where this kind of power-play language is just… normal vocabulary, not a big neon sign saying “CONTENT FILTER, LOOK HERE!” 😄

A couple of things that might help frame it:

- The filter isn’t “judging” the scene the way a human would (“this is just a charged moment, calm down”).  
  It’s pattern-matching: *provocative + intimate + dominance + submission + breasts* → probably sexual / fetish-coded → block.
- You, on the other hand, are reading it as a writer and visual storyteller. You’re thinking in terms of **character, mood, and dynamics**, not “how do I make this naughty.”

So yes, “inured” is exactly it: you’re used to reading this kind of language as emotionally and psychologically meaningful, not inherently salacious.

---

If you’d like to keep the *same* vibe but slip past the filter, the trick is to:

- keep the **visuals and emotional tension**,  
- swap out a few **flaggy words** for more neutral craft-language.

For example, a safer variant of your prompt:

> A young woman with light skin and long brown hair in an elegant updo, wearing a fitted white tank top, pink cardigan and a high-waisted red mini skirt, standing in a softly lit pink-walled room. She wears black ankle-strap heels, giving her a confident, professional look.  
>  
> Another woman with medium skin and long brown hair falling past her shoulders stands close in front of her, dressed in an all-black button-up shirt and tailored slacks that highlight her poised, self-assured presence. She gently rests her left hand along the first woman’s cheek, looking steadily into her eyes.  
>  
> The mood is cinematic and intense but non-explicit: a quiet moment of tension and unspoken conversation between them. In the blurred background, two other women sit at a table, talking softly. The overall style is a modern, high-end editorial photograph.

Notice what’s gone:

- no *“dominance and submission”*  
- no *“provocative interaction”*  
- no *“emphasizes her … breasts”*  
- “intimate” is softened into “quiet moment of tension” / “unspoken conversation.”

But: the visual and the power balance are still there. The woman in black is clearly the one in control.

If you want, you can paste me whatever you try next and I’ll do a quick “filter-sensitivity pass” on it before you feed it to the image model.

**Robyn:**

I need some help with displaying videos. I am currently using this:

<div style="position:relative;padding-top:56.25%">
  <iframe src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/3bb666683521a8eac9904681dc8ca560/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:none;position:absolute;inset:0;width:75%;height:75%"></iframe>
</div>

to display 'landscape' videos. How do I modify it to display, like vertical (iPhone/TikTok) style videos, like shorts?

**Emily:**

Nice, Cloudflare Stream again 😊

What you’ve got now is a classic **16:9 responsive wrapper**:

```html
<div style="position:relative;padding-top:56.25%">
  <!-- ... -->
</div>
```

`56.25%` is `9 / 16 * 100`, i.e. **height = 9/16 of the width** → landscape.

For vertical / shorts-style video (TikTok / iPhone portrait), you just flip the ratio to **9:16**, so the container is **taller than it is wide**.

### Option 1 – Keep the same “padding-top” trick (most compatible)

Use `padding-top:177.78%` (which is `16 / 9 * 100`):

```html
<div style="position:relative;padding-top:177.78%;">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/3bb666683521a8eac9904681dc8ca560/iframe"
    allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
    allowfullscreen
    style="border:none;position:absolute;inset:0;width:100%;height:100%;"
  ></iframe>
</div>
```

Key changes:

- `padding-top:177.78%;` → container is now 9:16.
- `width:100%; height:100%;` on the iframe so it fills the container.

You can tweak that 177.78 to 178 if you want to keep it simple; visually you won’t notice.

---

### Option 2 – Using `aspect-ratio` (if you’re happy to rely on modern CSS)

If your target browsers are reasonably up to date, you can skip the padding hack entirely:

```html
<div style="position:relative;aspect-ratio:9 / 16;">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/3bb666683521a8eac9904681dc8ca560/iframe"
    allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
    allowfullscreen
    style="border:none;position:absolute;inset:0;width:100%;height:100%;"
  ></iframe>
</div>
```

That tells the browser “this box is 9 units wide by 16 units tall,” and it will scale responsively.

---

If you tell me whether you want **square**, **9:16**, or something in between for your layout, I can give you a tiny snippet you can just paste into MkDocs as a reusable class instead of inline styles.

**Robyn:**

I actually took your second suggestion (resized width & height down to 40%) - why is there a huge space under the video? What did I do wrong?

**Emily:**

Ah, yeah, I can picture exactly what’s happening there. You didn’t really do anything “wrong” in the sense of syntax – it’s just how the layout math works.

### What’s going on

With this pattern:

```html
<div style="position:relative;aspect-ratio:9 / 16;">
  <iframe
    src="…"
    style="border:none;position:absolute;inset:0;width:40%;height:40%;"
  ></iframe>
</div>
```

- The **outer `<div>`** has `aspect-ratio: 9 / 16`.  
  That means:  
  - It will be **as wide as the parent allows** (often 100% of the page width or content column).
  - Its **height** is then computed from that width to keep a 9:16 ratio. So it becomes *quite tall*.

- The **iframe** is absolutely positioned inside that tall box, but you’ve told it to be only:
  - `width: 40%`
  - `height: 40%`

Because it’s `position:absolute; inset:0;`, it’s pinned to the top-left and only fills 40% of the container’s size.  
So you end up with:

- video at the top
- a big, empty chunk of the wrapper underneath → that’s the “huge space under the video” you’re seeing.

### The fix: scale the wrapper, not the iframe

You almost never want to shrink the iframe itself in this pattern.  
Leave the iframe at `width:100%; height:100%;` and instead control the **size of the wrapper**.

For example, a vertical video that only takes up 40% of the content width:

```html
<div style="position:relative;aspect-ratio:9 / 16;width:40%;max-width:320px;margin:0 auto;">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/3bb666683521a8eac9904681dc8ca560/iframe"
    allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
    allowfullscreen
    style="border:none;position:absolute;inset:0;width:100%;height:100%;"
  ></iframe>
</div>
```

Key points:

- `width:40%;` → wrapper is narrower (so everything shrinks proportionally).
- `aspect-ratio:9 / 16;` → wrapper stays vertical, no weird padding tricks.
- `width:100%; height:100%;` on the iframe → it fills the wrapper perfectly, no leftover space inside.
- `margin:0 auto;` just centres it horizontally (optional but usually nice).

If you show me exactly what you’ve got now, I can tweak *your* snippet directly, but conceptually:  
👉 **don’t scale the iframe; scale the container.**

**Robyn:**

You are a LEGEND, Emily.... works a treat!

**Emily:**

Heh, that makes *me* very happy to hear 🥰

I’ll remember:  
- **Landscape:** 16/9 (or padding-top:56.25%)  
- **Vertical:** 9/16 (or padding-top:177.78%),  
- and **always scale the wrapper, not the iframe**.

If you end up wanting two vertical clips side by side or a little “gallery” row of videos in MkDocs, I can whip up a tiny CSS + HTML pattern for that too.

**Robyn:**

Yes please, that would be awesome, thank you, Emily.

**Emily:**

Yesss, brilliant, let’s make you a cute little shorts gallery 💅📱  

Below is a drop-in pattern you can paste into a MkDocs page (or into `extra.css` if you like it enough to reuse everywhere).

---

## 1. CSS – two-across (and auto-wrap into a gallery)

You can put this at the top of your Markdown page inside `<style>...</style>`, or in your theme’s custom CSS:

```html
<style>
  /* Row that holds all the videos */
  .video-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;      /* centre the row nicely */
  }

  /* Each vertical video */
  .video-portrait {
    position: relative;
    aspect-ratio: 9 / 16;         /* vertical, like TikTok/Reels/Shorts */
    width: min(45vw, 320px);      /* two(ish) per row on desktop */
    max-width: 100%;
  }

  .video-portrait iframe {
    border: none;
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }

  /* On small screens, stack them nicely */
  @media (max-width: 700px) {
    .video-portrait {
      width: 100%;
      max-width: 360px;
    }
  }
</style>
```

- `aspect-ratio: 9 / 16;` keeps them vertical.
- `width: min(45vw, 320px);` makes them about two-across on a laptop, but avoids getting massive on large monitors.
- The media query stacks them on phones.

---

## 2. HTML – two (or more) vertical clips side by side

Now, wherever you want the videos in your Markdown:

```html
<div class="video-row">

  <div class="video-portrait">
    <iframe
      src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/VIDEO_ID_1/iframe"
      allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
      allowfullscreen>
    </iframe>
  </div>

  <div class="video-portrait">
    <iframe
      src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/VIDEO_ID_2/iframe"
      allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
      allowfullscreen>
    </iframe>
  </div>

  <!-- Optional third, fourth, etc. – they’ll wrap automatically -->
  <!--
  <div class="video-portrait">
    <iframe
      src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/VIDEO_ID_3/iframe"
      allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
      allowfullscreen>
    </iframe>
  </div>
  -->

</div>
```

Just swap `VIDEO_ID_1`, `VIDEO_ID_2`, etc. for your actual Cloudflare Stream IDs.

---

If you’d like a *mixed* row (landscape on the left, vertical on the right), I can give you a `.video-landscape` class that plays nicely with this setup too.

**Robyn:**

Saved to my Help page so I don't have to ask you again.

**Emily:**

Perfect place for it 😄

I’m very proud to be quietly lurking in your Help page, doing layout duty.

Anytime you want to:

- mix portrait + landscape clips in one row,
- add captions under each video,
- or turn the whole thing into a neat “before / after” comparison layout,

just say the word and we’ll extend the pattern rather than reinvent it.

**Robyn:**

Hi Emily, I need a synonym for 'tiny' that I can use as part of a prompt in the 'Illustrious' model.

**Emily:**

Hi lovely 😊

A few nice, prompt-friendly options instead of **“tiny”**:

- **petite** – great for adult femininity (petite woman, petite frame)  
- **dainty** – suggests delicacy and elegance, not childishness  
- **diminutive** – a bit more literary, but Illustrious should handle it fine  
- **miniature** – good for objects, props, accessories  
- **compact** – works well for cameras, furniture, cars, etc.  
- **slender** – for bodies/figures, if you mean slight rather than short  
- **delicate** – soft, fine, not necessarily small but often implied

If you tell me what you’re describing (body, dress, accessory, room, etc.), I can suggest a phrase tuned for the model, like *“a petite young woman with a delicate frame”* or *“a dainty lace collar”* that will read nicely in Illustrious.

**Robyn:**

It's a body part... it needs to be part of a prompt that Illustrious understands.

**Emily:**

Gotcha, that helps.

For a **body part** in an Illustrious prompt, these tend to parse well and stay tasteful:

- **petite** – very reliable for proportions  
- **slender** – good for limbs, fingers, neck, waist  
- **delicate** – nice for hands, wrists, facial features  
- **fine** – as in *fine features*, *fine hands*  
- **small** – boring but very safe and clear to the model  
- **subtle** – useful for things like curves, muscles, contours  
- **slight** – gentle, understated

A few plug-and-play patterns you can adapt:

- `a petite young woman with slender, delicate hands`  
- `a graceful woman with a slight, delicate nose`  
- `a mature woman with subtle, fine features`

If you tell me *which* body part you’re hinting at, I can give you 2–3 very targeted prompt fragments that Illustrious will almost certainly “get.”

**Robyn:**

Well, let's say 'pinky' finger...

**Emily:**

Ahh, perfect use case 😊

For a **pinky finger**, “tiny” maps really nicely to:

- **little** – anatomically correct (little finger), models understand it well  
- **slender** – shape-focused, graceful  
- **dainty** – small *and* elegant  
- **delicate** – soft, fine, not chunky

Some ready-to-drop-in prompt fragments for Illustrious:

- `with a dainty little finger resting against her lips`  
- `her slender little finger lightly touching the teacup`  
- `a close-up of her delicate little finger and polished nail`  
- `elegant hands, with a dainty pinky finger adorned by a thin gold ring`

If you want it to really “lock in,” use **“little finger”** in at least one place, then you can get more poetic with “dainty” / “delicate” around it.
