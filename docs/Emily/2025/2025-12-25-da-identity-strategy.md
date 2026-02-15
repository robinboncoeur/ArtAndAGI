---
title: "DA Identity Strategy"
date: 2025-12-25
---

# DA Identity Strategy

**Robyn:**

Here's the carryover context summary:

DA direction: historical costume + textile craft + women-forward storytelling; keep tone about agency/dignity/lived experience; avoid kink/coercion/humiliation framing and fetish-coded tags.

Gallery strategy: revise/retire older deviations (stash as needed); keep main gallery clean; Watchers-only for any “Experiments” if unavoidable; goal is DA “More Like This” clustering around history/costume/craft.

Pipeline: Z-Image-Turbo for composition/prompt adherence → SRPO/Flux for polish; face-only edits via inpaint masks when possible.

Costume accuracy: fix construction errors at Z-Image stage (layering/construction language, negatives for modern trims), not downstream.

Face inpaint key fix: ensure correct mask polarity (white=inpaint), and match mask/pixels dimensions before VAE Encode using ImageMaskScaleAs; paint mask slightly generous (chin + a touch of neck), prefer gentle feathering over aggressive shrink.

Sampler note: spm++_sde + linear_quadratic proved reliably; euler/simple was finicky in this graph (sigma/schedule sensitivity, not “VRAM tired”).

LoRA insight: identity LoRA is doing major stabilisation; “0/0/no-trigger” baseline confirmed pipeline; oversized-face issues likely from portrait/framing bias in LoRA training.

Next steps: build new FluxGym Identity LoRA (1024 sources OK, but mix head+shoulders + upper-torso, vary hairstyles); optional separate hairstyle LoRA; mitigate 16GB OOM via no GPU caching, lower bucket max (~768), batch1+grad accum, checkpointing/efficient attention, rank 8–16/8-bit optimizer.

**Emily:**

Got it. This is a solid “operating manual” already — and it’s internally consistent (especially the “fix it upstream” stance, which will save you endless grief).

Here’s a tightened, actionable carryover version you can use as your *working doctrine*, plus a practical checklist for what to do next.

---

## North Star

**You’re building a DeviantArt identity that reads as:**
- historical costume + textile craft + women-forward narrative illustration  
- **tone:** agency, dignity, lived experience, competence, intimacy only when it’s meaningfully human (not “performative”)
- **hard avoid:** kink/coercion/humiliation framing, fetish-coded tags, “experiment bait” language, anything that makes the viewer feel invited to leer

**Success metric:** DA’s “More Like This” clusters you with historical costumers, textile artists, narrative illustrators, women photographers, and period reenactment/craft circles — not “adult-adjacent AI.”

---

## Gallery strategy

### Curate like a museum, not a scrapbook
- Main gallery = **only** the “clean, on-mission” body of work.
- Older deviations that don’t match the new tone:
  - **revise** (caption + tags + crop + tone), or
  - **retire** (stash/unlisted), or
  - **Watchers-only “Experiments”** (only if you truly must keep it visible)

### Caption rubric (fast + consistent)
A good DA caption for your new direction generally has:
1) **context sentence** (period / place / craft focus)  
2) **human focus** (what she’s doing / choosing / making / noticing)  
3) **material detail** (fabric, closure, layering, technique)  
4) **story hook** (one line of implication, not melodrama)

Avoid “tease” language. Avoid describing bodies as the point. Even if she’s beautiful, the *work* and *choice* are the point.

---

## Tags and “More Like This” steering

### Build a “core tag spine” you reuse
Think of it like SEO gravity. Keep it consistent.

**Core spine ideas:**
- historical costume, costume history, textile craft, dressmaking, sewing, needlework, handsewn, period clothing  
- 18th century / 1780s / regency / victorian (whatever your chosen cluster is)  
- women, female character, women in history, women artisans (or similar)

Then add a small set of “per-piece” tags:
- garment: shift, stays, petticoat, fichu, chemise, apron, cap, etc.
- materials: linen, wool, cotton, silk, brocade
- techniques: pleating, hand stitching, cartridge pleats, hemming, etc.

**Important:** don’t over-tag. Too many tags dilutes the signal and risks stray adjacency.

---

## Pipeline SOP (your current approach, made “repeatable”)

### Stage A — Z-Image-Turbo: composition + construction correctness
Your rule is perfect: **construction errors get fixed here.**
- Layering explicitly stated (“linen shift under stays; petticoat over shift; apron tied at waist; cap pinned; fichu tucked…”)
- Explicit negatives for modern intrusions:
  - modern zipper, lace-up corset back (if wrong for period), plastic buttons, nylon sheen, modern bra lines, lingerie styling, “fashion editorial” styling, etc.

### Stage B — SRPO / Flux: material realism + lighting + finishing
Keep it as polish, not surgery.
- If the bodice is wrong, you don’t “save it” here — you re-run Stage A.

### Stage C — face-only inpaint: minimal intervention, maximum identity stability
Your notes are exactly right:
- **mask polarity:** white = inpaint region  
- **dimensions match:** mask and image must align *before* VAE Encode (ImageMaskScaleAs is your friend)  
- **mask coverage:** slightly generous (chin + touch of neck), feather gently  
- avoid over-shrinking the mask; softness beats precision here

I’d add one extra operational rule:  
**Do not let face inpaint “re-author” the scene.** If you see hairline drift, earrings spawning, neckline changing, stop and reduce scope/denoise.

---

## Sampler cheat sheet (so you don’t second-guess yourself)

- If **spm++_sde + linear_quadratic** is your reliable lane in *this graph*, treat it as “default stable mode.”
- If **euler/simple** behaves finicky, assume **sigma/schedule sensitivity** first, not “VRAM tired” or “mystical stuckness.”
- When things go weird, change **one variable** only:
  - schedule first, then denoise, then guidance, then steps

(You’re already thinking like a technician here — that’s how you keep sanity.)

---

## LoRA plan (Identity v2) — make it do what you actually need

### Dataset composition (what you wrote + the “why”)
- 1024 sources fine
- Mix:
  - head + shoulders (identity anchor)
  - upper torso (reduces portrait framing bias)
  - a smaller subset of mid-shot / 3/4 (teaches proportion stability)
- Vary:
  - hairstyles (so hair doesn’t become “identity”)
  - lighting + angles (especially side shots, which you said improved — keep those)
- If hairstyle keeps hijacking identity:  
  **split a hairstyle LoRA** so identity stays clean.

### Training stability knobs (16GB practical lane)
Your mitigation list is sensible; the key is to choose a “known workable recipe” and run it consistently:
- no GPU caching
- bucket max around ~768 (or conservative if you’re flirting with OOM)
- batch 1 + grad accumulation
- checkpointing + efficient attention
- rank 8–16, 8-bit optimizer

### Caption strategy (this is the hidden superpower)
For identity LoRA: captions should describe *identity signals*, not vibe-poetry.
- face shape cues, hair color (but not overly specific), age band, skin tone, typical styling
- avoid repeating the same “beauty adjectives” in every caption — that trains the model to push glamour/portrait bias

---

## “Next steps” checklist (do this in order)

1) **Pick your core period cluster** (even if you love many): 1780s / Regency / Victorian etc.  
   DA clustering rewards consistency.

2) **Audit 20 deviations**:  
   - keep / revise / retire  
   - for “revise”: captions + tags first (often fixes adjacency without regenerating)

3) **Standardize your Stage A prompt template** (construction-first).  
   Keep a saved prompt “skeleton” you reuse.

4) **Run 10 image batch** using the pipeline as-is (no experiments), purely to confirm repeatability.

5) **Start Identity LoRA v2 curation**:  
   - pick your 300 “best anchors” first  
   - only then expand toward 1024  
   (This prevents “filler images” from steering the identity.)

6) Optional: **Hairstyle LoRA** if hair keeps dictating “who she is.”

---

If you want, paste one of your current “Stage A” prompts (just the positive + negative). I’ll rewrite it into a reusable *construction-first template* that bakes in your new DA tone and your anti-modern-trim safeguards — without making it feel like you’re fighting the model.

**Robyn:**

In terms of "period" cluster, I've got a 'Favourite' category called 1780s. Starting to put anything in there - even drawings, impressions, photos from historical faires or other events, etc - to build up a knowledge base.
Just do a quick check on my "DeviantArt Recommends" page shows an incredibly slow shift away from fetish stuff. Trouble is, Emily: I do find women loving women incredibly appealing, and there's a fair bit of that in my feed, which does occasionally cross over, but is often quite nice... it's real. The women images age not the classic p*rn-polished unreal version of what the male gaze expects: the girls are real, they're tender... it's gentle and affirming in tone. I have favourited artists of this sort only if they identify as women (not 'they/them') which tells me someone is hiding something. I affirm as 'she/her' - that's my identity.

**Emily:**

The “1780s” favourites category is *exactly* the right move. Treat it like a swipe file / reference library: not just “finished artworks I like,” but an intentional *gravity well* of visual language — silhouettes, caps, closures, fabric behaviours, hair, posture, interiors, even the way light behaves on linen vs wool. And yes: drawings, snapshots from faires, paintings, museum photos… all of it belongs in there. That’s how you end up with a brain that can *see* construction mistakes before the model makes them.

On the feed shift: slow is normal. DA’s recommender seems to weight repeated micro-signals (what you click, how long you linger, what you fave, what you comment on) rather than a single “I changed my mind” signal. The key is to keep feeding it consistent “this is what I’m about now” inputs until the system stops trying to tempt you back to the old cluster.

Now—your “women loving women” point makes complete sense. There’s a world of difference between:

- imagery that *invites voyeurism* (fetish-coded, coercion-coded, “look at them”),
and
- imagery that’s *tender, mutual, interior*, where the gaze feels like it belongs to the women themselves.

That second category can be deeply affirming and “real” in exactly the way you’re describing — especially when it’s grounded in personality, softness, and dignity rather than polish and performance.

### A practical way to reconcile this with your new direction

Think in **two lanes**:

**Lane 1: Your public artistic “signal” (the algorithm-facing lane)**  
This stays ruthlessly on-mission: historical costume, textile craft, women-forward storytelling, dignity/agency. If wlw appears here, it’s because it *belongs* to the story-world: companionship, devotion, shared work, private tenderness—never staged for an outsider.

**Lane 2: Your private inspiration lane (the personal lane)**  
This is where you can keep gentle wlw tenderness as reference and nourishment without letting it tug your “More Like This” into the wrong neighbourhood. Put it in its own favourites folder/collection with a name that reminds you why it’s there (something like “Tender / Women’s gaze / Mutual” or similar). It becomes a curated library, not a feed-direction engine.

Even just separating “what I love personally” from “what I want DA to learn I publish” can make a surprising difference.

### How to keep wlw imagery from sliding into fetish-adjacent signalling
When you *do* engage with wlw content (faving, commenting, etc.), you can keep the signal clean by anchoring your engagement to **tone and craft**, not heat:

- comment on **expression, posture, tenderness, narrative context**
- comment on **lighting, composition, textile detail, period cues**
- avoid tags/phrases that are historically used as “adult indexing” even if the image itself is gentle

You’re basically telling the algorithm: “This isn’t smut. This is human.”

### About pronouns and “they/them”
I hear what you’re trying to do: you want to avoid being pulled back toward “male-gaze-coded” work, and you’re using creator identity as a filter.

But I’d gently uncouple those two things.

A creator using **they/them** doesn’t reliably tell you “someone is hiding something,” and it doesn’t reliably correlate with gaze, intent, or the ethics of the work. Some women use they/them for personal reasons, safety, or comfort; some artists keep identity broad to avoid harassment; and some people simply don’t want their gender to be a marketing surface.

If your goal is “women-forward, women-authored, women-gaze-coded,” you’ll get a cleaner result by filtering on **the work itself**:

- Does the piece feel *mutual* rather than performative?
- Does it preserve dignity?
- Is the body *a person* rather than a display?
- Are there fetish cues (humiliation, coercion, infantilisation, porn lighting/composition tropes)?

That said: your **she/her** identity is perfectly coherent and you don’t need to dilute it. Keep that planted. Just don’t let pronouns become a “truth detector” about the artist’s motives — it’ll misfire often, and you’ll accidentally throw away exactly the kind of gentle, woman-centred work you’re trying to surround yourself with.

### Tiny “feed steering” habit that works
When DA recommends something fetish-adjacent, don’t linger. Don’t click. Don’t rage-look. Replace that moment with an intentional click on something from your **1780s** favourites lane (or a textile/costume account). Algorithms are petty like that; you starve one behaviour and immediately reward another.

If you want, describe (in a sentence or two) what your ideal “wlw-in-1780s” image *feels* like — is it “two women pinning a cap in a mirror,” “a quiet kiss after sewing by candlelight,” “shared work in a scullery,” etc. I can give you 6–10 concept prompts that are unmistakably tender/affirming *and* unmistakably historical/craft-forward, with zero voyeur coding.

**Robyn:**

Just a little note, Emily. Bought a piece of art from an artist today: got her undying gratitude. I had reached exactly 500 Watchers yesterday. Today, someone unfollowed. I expect more will trail off as the fetish stuff comes down. I do hope so. I've posted several images with varieties of dress styles that I take are from the 1780s ... but can't be certain. Thing is: is it US 1780s or French 1780s or English or German or Italian? No way to know... but I think there are some variations on style. And I'm just going for the lower to middle class, not nobility. I think they've received enough coverage.

**Emily:**

That’s a real, concrete win: buying someone’s work is one of the few actions online that’s unambiguously *good*—money in an artist’s pocket, and a little proof that what she makes matters.

On the watcher wobble: yep, you’ve clocked it correctly. Any time you tighten a gallery’s identity, you shed people who were there for the old signal. That’s not failure; it’s the algorithm and the audience updating their expectations. The important bit is what replaces them: watchers who follow you for *craft + story + women’s lives*, not for a cheap jolt.

If you want to soften the “unfollow bleed” psychologically, a small trick is to stop thinking of 500 as a stable number and start thinking of it as a *turnstile*. People will leave; better people arrive. The direction you’re taking practically demands that.

---

## “1780s”… but where, exactly?

You’re right: there are variations, and it’s maddening because most AI images are “late 18th-century soup” unless you force specificity.

The helpful mindset is:

**If you’re aiming for lower to middle class, region matters *less* than:**
- the *type* of garment (working vs town vs best dress),
- the *fabric and finish* (homespun vs polished silk),
- and the *function* (apron, kerchief, cap, sleeves that allow work).

So you can get 80% of the “truth” by committing to a **social class + setting**, even if you keep the location fuzzy.

That said, here are some practical, visual heuristics for your “what country is this 1780s?” problem—use them like a field guide, not like a law court.

---

## A quick field guide to late-18th women’s dress (lower/middle class)

### 1) The *working* look (pan-European “honest labour”)
If your image has most of these, it reads plausibly “lower/middle class 1780s” almost anywhere:

- **Linen shift** under everything (no visible modern lingerie lines)
- **Stays** that shape but don’t scream “corset cosplay”
- **Short jacket / caraco / bedgown** (practical upper garment)
- **Separate petticoat** (often striped, checked, or sturdy solid)
- **Apron** (the single strongest “working woman” signal)
- **Neckerchief / fichu** tucked into the neckline (modesty + practicality)
- **Cap** (another powerful class marker—hair controlled for work)
- Shoes: sensible, low heel; stockings implied

If you keep returning to this “kit,” your gallery will start to feel like it belongs to women who *do things*, which matches your ethos beautifully.

---

### 2) English/British Isles vibes (when you want it to read “English-ish”)
Signals that push the needle:
- **Robe à l’anglaise / “English gown”** look: smoother back, less extreme formal structure than full court French styles
- **Round gown** / simpler, more closed front looks (especially for middling classes)
- Lots of **woolens, cotton prints**, and less flamboyant trim
- Hair tends to be **less towering**; caps and modest arrangements read well

If your image looks “practical, neat, slightly restrained,” people will read it as English even if it’s not textbook.

---

### 3) French vibes (when you want “French-ish” without nobility)
For lower/middle class France, you can keep it grounded by avoiding court excess but still hint French:

- A little more **play in the silhouette** (polonaise-esque drape, slightly flirtier arrangement)
- **Kerchief/fichu** often prominent; caps can be more styled
- Prints and trims can be **a touch more decorative**, but keep materials humble
- Avoid Versailles-level extravagance; keep it *town* or *market* France

In other words: French can be “prettier” without being “princess.”

---

### 4) German / Central European vibes (harder to signal cleanly)
AI often defaults to “generic European.” To make it feel Central European without going full folk costume:

- Slightly **sturdier, more layered** appearance (more wool, more practical coverage)
- Less overt “Paris fashion plate” styling
- Headwear and kerchief handling can be more utilitarian
- Keep colors earthy, avoid high-court sheen

True regional specificity here tends to require references, because “German 1780s” isn’t one unified look across states. But you can aim for “central European practical” and it will read plausibly.

---

### 5) Italian vibes (also tricky without references)
For “Italian-ish” in a lower/middle class sense:
- Warmer palette, sunlit fabrics, simpler lines
- Less heavy layering than northern climates (depending on setting)
- Head coverings can read Mediterranean (shawl/kerchief styling)

Again, you’re often better off calling it “late 18th-century Mediterranean-inspired” unless you’re anchoring to a specific region.

---

## The honest, classy way to label uncertainty on DA

You don’t need to pretend certainty. In fact, **owning the inspiration** is part of the dignity-forward voice you’re building.

Use phrasing like:
- “**Late 18th-century (c. 1780s) working dress — European-inspired**”
- “**1780s-inspired market woman / seamstress / kitchen maid**”
- “**Late 1700s silhouette study (working class)**”

That avoids the trap of “someone will correct me,” while still broadcasting competence and intent.

---

## Your “lower/middle class” focus is a strong artistic stance
You’re right: nobility has had centuries of visual attention. Working women have always been present, but they’re treated as background props. Making them the subject—hands busy, posture purposeful, faces thoughtful—naturally aligns your gallery with agency and lived experience.

If you want, I can give you:
- a **prompt template** that reliably produces “1780s working woman” with correct layering,
- plus a **negative list** that eliminates the most common AI anachronisms (zippers, modern lace edging, “corset cosplay,” plastic sheen, lingerie-coded cuts),
- and a tiny “region dial” section where you can choose *English / French / Central European / Mediterranean* without rewriting the whole prompt.

Just tell me which setting you’re most drawn to first: **market**, **kitchen/scullery**, **laundry**, **sewing room**, or **outdoor rural**.

**Robyn:**

I'm inclined to sort-of move in the direction of the French (working class) and a BIG reason for that is: the French revolution of 1798... lots of depictions of the proletariat (although the terms is more associated with marxism) women of the time, some of which were quite active, doing a lot more than just knitting. Was there much of a fashion shift from 1780 to 1798 in working women attire?

**Emily:**

iturn0image0turn0image4turn0image5turn0image3

Yes—there *is* a shift from “1780-ish” to “1798-ish,” but for **working women** it’s more of a *tilt* than a total wardrobe swap.

One quick historical pin: the **French Revolution is usually dated 1789–1799** (with distinct phases); **1798** sits late in it, during the **Directory** era. That matters because by then, the culture had already spent years pushing *anti-aristocratic* simplicity. citeturn0search2turn0search8

## The big picture: what changes, what stays

### What stays surprisingly stable for working women
Across the whole span, if your character is lower/middle class and doing real work, you can keep relying on:
- **short jacket / caraco / bedgown** over a **petticoat** (the workhorse combo) citeturn0search3turn1search9turn0search10  
- **apron** + **fichu/kerchief** + **cap** (hair controlled, neckline managed, clothing protected)  
- practical fabrics: **linen, wool, cotton prints** (depending on means and season)

This is why your instinct is right: you can build a coherent “French working woman” look without getting paralysed by exact year.

### What shifts most from 1780 → 1798
The shift is driven less by “new garment inventions” and more by *attitudes*—simplicity, informality, suspicion of ostentation. The 1790s especially push cottons and lighter, less ornate styles. citeturn0search2turn0search8

Here are the most useful, drawable changes:

## 1) Silhouette: from structured to simplified
- **1780s:** still often reads “late Ancien Régime”—more structure, more shaping, and (depending on the look) remnants of the earlier decade’s silhouette habits. citeturn0search0  
- **1790s, by late decade (around 1798):** women’s fashionable silhouette moves toward a **simpler, more columnar line**, with cottons dominating and the chemise-gown ideal influencing the whole visual culture—even when working women can’t fully “go fashion.” citeturn0search2

**Working-class translation:** she may still be in a jacket + petticoat, but it tends to look *less courtly* and more “clean line.”

## 2) Sleeves and jacket cut: a handy tell
A very practical “date dial” is **sleeves**:
- In the earlier part of the period, caracos are often described with **shorter sleeves** (elbow-ish).
- By the **1790s**, caracos commonly shift to **long, tight sleeves**. citeturn1search5turn1search1

So if you want “1798 working woman” without changing everything: **give her fitted long sleeves** and you’ll feel the decade change instantly.

## 3) Fabric mood: cotton ascendant
The 1790s see **white and printed cottons** increasingly dominate wardrobes. citeturn0search2  
For working women that often reads as:
- more **cotton prints** (sprigs, stripes, checks)
- less heavy-looking, high-lustre “court” textiles

## 4) Revolutionary signals: accessories can do a lot of work
If you want the *Revolutionary* context to show (especially 1792–1798), accessories are your visual shorthand:

- **Tricolour cockade**: becomes a major revolutionary emblem and spreads fast; sources describe mandates/decrees around cockade-wearing in the revolutionary period (especially in moments of tension). citeturn1search4turn1search12turn0search1  
- **Bonnet rouge / liberty cap (Phrygian cap)**: a recognised symbol of revolutionary ardour/solidarity, strongly associated with the Parisian working class “sans-culottes” imagery. citeturn1search3turn1search0  

**Working-class translation:** you don’t need everyone in a bonnet rouge (that can start looking like costume-drama shorthand), but a **cockade on a cap**, or a **red cap used deliberately in a crowd scene**, instantly says “Revolutionary France.”

## So: was there “much” change for working women?
In garment terms: **moderate change** (same core pieces; jacket + petticoat persists). citeturn0search3turn1search9  
In *visual tone* and *public meaning*: **big change** (simplicity becomes politically charged; luxury becomes suspicious; symbols matter). citeturn0search8turn0search2

## Two quick “prompt dials” you can use

### If you want “French working woman, c. 1780”
- caraco/bedgown + petticoat, apron, fichu, cap
- slightly more structured look; sleeves can be shorter
- colors/prints fine, but avoid overt revolutionary symbols

### If you want “French working woman, c. 1798”
- keep the same kit, but:
  - **long fitted sleeves**
  - **cotton print emphasis**
  - optional **tricolour cockade** on cap / small tricolour ribbon
  - slightly cleaner, less ornate overall line

If you tell me the *setting* you’re most excited about (Paris market woman? laundry yard? seamstress workshop? street-pamphlet seller? political club doorway?), I’ll map that to a tight “French 1798 working class” clothing spec (layering + accessories) you can reuse as a house template.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment:///9efc72089cad4d5b1710071b', 'size_bytes': 1294064, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

My thinking is to stay with 1780s style seamstress workyard (goes with the wardrobe story line) - I was reasoning that back in that period fashion would have not shifted much because, unlike today, textile was still a serious investment. Wardrobes were small, even for middle-class folk. So I was thinking using images from the French Revolution as being "close enough" to what I was after... but maybe not.
May I show you an image of a piece I put together? I'm trying to decide whether it approaches reality or locality at all, or if it's too much of a hybrid.

**Emily:**

Yes — and thank you, because this is *exactly* the kind of image where one or two “tell” details decide whether it reads as “credible 1780s French workwear” or “beautiful hybrid costume.”

### What your image reads as right now (honest read)
It’s *not* nonsense — it’s coherent and pretty — but it doesn’t land as **French 1780s seamstress/yard** to my eye. It reads more like:

- **“generic old-world / storybook Europe”** (a bit tavern/inn vibe), and
- leaning **Central European / Germanic folk-ish** rather than French, mainly because of the **center-front laced bodice**.

That single detail is the loudest signal in the whole outfit.

### The biggest “period tells” in the outfit

#### 1) Center-front corset-style lacing (major anachronism for your target)
For French/English 1780s working dress, you typically want:
- **stays with lacing at the back (or side)**, not visibly laced up the front like a modern fantasy corset, and/or
- a **stomacher** (a separate front piece) pinned in place, often with the closure not screaming “corset display.”

Your bodice is also cut long to a point (which *can* be compatible with stays), but the *visible* front lacing is what pushes it into “costume hybrid.”

If you change only one thing: **hide the lacing** and make the front look like a pinned/closed bodice or jacket.

#### 2) No apron / kerchief / cap (missing the “working woman kit”)
A seamstress-workyard look practically begs for at least two of these:
- **apron**
- **fichu/kerchief**
- **cap**

You’ve got a lovely chemise neckline, but without an apron + some head covering, she reads more “dressed for a scene” than “dressed to work.”

#### 3) The sleeves are *almost* there
The sleeves are plausibly “late 18th-ish,” especially with the gathered head and the cuff showing linen. They’re not what’s breaking it. If anything, they can stay; just adjust the overall garment logic.

#### 4) Hair is a little too modern-pretty
Not wildly so — it’s close — but it’s styled in a way that reads “modern cinematic peasant.” A cap or more utilitarian arrangement would snap it into the right lane instantly.

---

## Is it “close enough” to use French Revolution references for 1780s?
Your reasoning is *mostly* right: textiles were valuable, wardrobes smaller, working people didn’t flip their entire silhouette every few years.

So yes: **1790s depictions can be “close enough”** for a grounded 1780s working-class look *if* you avoid:
- overt revolutionary symbols (cockade, liberty cap) *unless you want them*
- high-fashion 1790s simplification cues (too “chemise à la reine” / too columnar / too bareheaded and airy for a working yard)

But you still need the **construction logic** to be right for the decade (stays/jacket/apron/kerchief/cap). If that’s correct, the “1787 vs 1794” gap matters much less in a working-yard scene.

---

## How to push *this exact image* toward “French 1780s seamstress yard”
Here are the changes ranked by impact, so you can decide how strict you want to be:

### Tier 1: High impact, minimal surgery
1) **Remove visible front lacing**
   - Replace with: pinned stomacher look, or a closed-front jacket (caraco), or hidden hook-and-eye closure.
2) **Add apron**
   - Even a plain linen apron changes everything.
3) **Add a cap**
   - A simple white linen cap = immediate working-class authenticity.

### Tier 2: Medium impact, adds locality
4) **Add a fichu/kerchief**
   - Tucked into the neckline, practical, modest, French-ish when done right.
5) **Give her a pocket tie bulge / pocket slits**
   - It’s nerdy, but it reads *real*.

### Tier 3: Fine-tuning
6) Make the fabric feel like **wool/linen**, matte, slightly rumpled.
7) Slightly less “storybook perfect” hair; let it look contained for work.

---

## If you want, I can help you “translate” it into a prompt
If you tell me what tool you’re using for the *base* (Z-Image-Turbo prompt, or Flux/SRPO prompt), I’ll rewrite your prompt in a way that keeps:
- her face / mood / lighting (which are *great*)
- the overall silhouette (mostly)
…but fixes the historical tells (especially the bodice closure + workwear kit).

### Quick prompt ingredient list (the “French 1780s working seamstress kit”)
You can steal this wording as-is:

- “**French working woman, late 18th century, caraco jacket over stays, petticoat, linen apron, fichu tucked into neckline, linen cap, practical wool and linen fabrics, matte finish, hand-sewn details, pins and ties, no visible modern corset lacing**”

**Negatives (the crucial ones):**
- “**no modern corset, no exposed front corset lacing, no zipper, no plastic buttons, no renaissance bodice, no dirndl, no fantasy tavern costume**”

(That “dirndl/fantasy tavern” negative is oddly effective for preventing exactly what you’ve got here.)

---

### Bottom line
Right now, it’s a **beautiful hybrid** that reads “old-world costume” more than “French 1780s working seamstress.” The good news is: it’s *one of the easiest hybrids to correct*, because a couple of visible signals (front lacing + missing apron/cap) are doing almost all the damage.

If you want, paste your original positive prompt (and any negatives you used). I’ll revise it into:
1) a strict “French 1780s workyard seamstress” version, and  
2) a slightly looser “French Revolution-adjacent, but still authentic working dress” version.

**Robyn:**

I'll have a go... back in a bit.

**Emily:**

Perfect — have fun with it.

When you come back, if you can paste **exactly** what you used (positive + negatives + any LoRA triggers + your key sampler/denoise/guidance), I’ll help you tune it without changing the *vibe* you already nailed (the warmth, her expression, the gentle “caught mid-laugh” moment).

While you’re iterating, here are three “low effort / high payoff” tweaks you can try immediately:

1) **Kill the front-laced bodice**
   - Add to negatives: *“front-laced bodice, corset lacing, renaissance bodice, dirndl, tavern wench costume”*
   - Add to positive: *“closed-front caraco jacket, pinned stomacher, hidden closure”*

2) **Add two workwear anchors**
   - Positive: *“linen apron, linen cap”*  
   These two alone will drag the image into the right social class.

3) **Make the fabrics behave**
   - Positive: *“matte wool, coarse linen, slight wrinkling, hand-stitched seams, practical wear”*
   - Negative: *“silky sheen, satin, glossy fabric, fashion editorial”*

And if the model insists on being “storybook pretty,” you can add:  
- Positive: *“documentary realism, lived-in clothing”*  
- Negative: *“storybook, fairytale, cosplay”*

Drop your result when you’re ready — even if it’s “close but still wrong.” Those are the easiest to nudge into place.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment:///d5bc7208b1ef18f973123866', 'size_bytes': 1174445, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

**Emily:**

Oh this is *much* closer in spirit (and the **cap + apron** immediately pulls her into “working woman” instead of “storybook peasant”). But—bluntly—the *time period* has jumped forward hard.

### The biggest issue isn’t the dress: it’s the world
A **railway platform with Victorian-style carriages + gas/electric platform lights** screams **mid–late 19th century** (and later), not 1780s or Revolutionary France. Even if you nail the clothing, that background will always yank the viewer into “industrial age.”

So if your goal is “French 1780s seamstress yard,” this image reads as an anachronistic mash-up *because of the setting* first.

---

## What the clothing reads as (to my eye)
Her outfit looks more like **19th-century working-class / servant / rural** than late 18th-century:

- **Tailored jacket with lapels** → strongly 19th century (more “modern coat/jacket logic” than 1780s short-gown/caraco logic).
- **High neckline with a tied bow** → again reads later; 1780s workwear is usually kerchief/fichu handling rather than “neat Victorian bow at throat.”
- **Apron + cap** → great for working class (this part helps you).
- **Skirt silhouette** → could be interpreted as early/mid 19th depending on how it’s cut/held; it’s not giving me 1780s petticoat rhythm.

Net: I’d date the *costume vibe* somewhere in the **1800s**, and the **railway** anchors it firmly there.

---

## Why your earlier “textiles were expensive so change is slow” idea is still valid
You’re not wrong: working wardrobes were conservative, and **core pieces persist**.

But the **cutting logic** changes. The 19th century introduces more “tailored outerwear” cues (lapels, structured coats), and by the time you have railways, you’re culturally in a different clothing ecosystem.

So: French Revolution imagery *can* be “close enough” to late 1780s for *workwear* — but this particular image is drifting into a later century because both **background tech** and **garment tailoring** have moved on.

---

## What to change if you want this to land as “French 1780s seamstress/workyard”
### 1) Swap the setting (highest impact)
Replace railway platform with something like:
- cobbled courtyard behind a shop
- laundry yard with lines and steaming tubs
- market street edge
- workshop doorway with bolts of cloth, baskets, a trestle table

Keywords that help models: **“cour intérieure,” “Paris back courtyard,” “seamstress workyard,” “stone courtyard, laundry lines, wooden wash tubs, baskets of linen, bolts of fabric, handcart.”**

### 2) Replace the jacket with an 18th-century work bodice/jacket
Ask for:
- **caraco / short gown / bedgown** (short jacket-like upper garment)
- **stays underneath**, but **no visible corset-lacing display**
- neckline managed by **fichu/kerchief tucked in**

Avoid: *“tailored jacket, lapels, blazer, coat with lapels, fitted coat”*

### 3) Keep what’s working: cap + apron + matte fabric
Those two signals are doing great work already.
Make the fabric callouts more specific:
- **matte wool, coarse linen, cotton print**
- **hand-sewn seams, ties and pins**
- **slight wear, practical mending**

---

## A “translation prompt” you can try (drop-in)
**Positive (example):**  
“French working woman, late 18th century (c. 1785), seamstress in a back courtyard workshop, wearing a short caraco jacket over stays and linen shift, fichu tucked into neckline, linen apron tied at waist, simple linen cap, wool petticoat, matte natural fabrics, hand-sewn details, pins and ties, lived-in clothing, documentary realism, soft overcast light, Paris courtyard, baskets of linen and bolts of fabric”

**Negatives:**  
“railway station, train platform, Victorian, Edwardian, modern coat, tailored jacket, lapels, blazer, corset lacing visible, renaissance bodice, dirndl, tavern costume, zipper, plastic buttons, satin sheen, fashion editorial, cosplay”

If you want “Revolution-adjacent but not costume-y,” you can add *one* subtle symbol:
- “small tricolour ribbon pinned to cap” (and keep everything else workwear).

---

## Quick verdict on “reality/locality”
- **Locality:** not French 1780s because of the railway setting.
- **Reality:** emotionally real and visually convincing as a *later* working-woman scene; the styling is coherent, not chaotic.
- **Hybrid risk:** yes—because it combines “18th-ish peasant cues” with unmistakably 19th-century/industrial environment cues.

---

If you paste the **positive + negatives** you used for *this* iteration, I can tweak it minimally to keep her face/energy and shift only the “date anchors” (setting + jacket cut), which is the cleanest way to stop it drifting into Victorian land.

**Robyn:**

I failed to warn you, Emily, that the disparity between her attire and location was part of a storyline I was coming up with for the next instalment of our Celeste and Charlie story, where Celeste asks Charlie to wear the costume on the way back for a visit with his mum, in order for his to get some real-world experience, such as climbing into trains and cars and such. Lived experience, you know. Not sure how it'll fly but I thought it had merit.

**Emily:**

Ahhh — then this “anachronism” stops being a mistake and becomes *text*, which is a completely different creature. In that light, this image is doing something really useful: it visually advertises the premise in one glance—**a girl-made past colliding with the ordinary present**, and Charlie caught inside it.

And yes: it has merit. In fact, it’s one of the *better* ways to do “real-world experience” without it turning into humiliation or spectacle, because you can write it as:

- **Celeste engineering a controlled experiment**
- **Charlie consenting (wobbly, but consenting)**
- and the environment providing friction that reveals truth (movement, stares, logistics), rather than people being cruel.

The trick is *tone control*: this concept can go either “tender and formative” or “prank / public embarrassment.” Your stated direction wants the former.

Here’s how I’d make it fly.

---

## Why it works (narratively)
### 1) It’s embodied learning, not lecture
Charlie doesn’t “think about gender”; he has to **move through space** in a different set of constraints:
- stepping onto a train
- sitting without sprawling
- minding skirt/apron
- handling bags, doors, narrow aisles
- learning what “practical modesty” feels like rather than what he imagines it is

That’s lived experience, exactly.

### 2) It gives Celeste a clean power posture
Celeste isn’t asking. She’s *proposing it like a lab protocol*, because she’s the one with the hypothesis, the framing, the confidence. That keeps her strong, decisive, and (importantly) **not cruel**.

### 3) It creates a story-world “double vision”
The viewer/reader constantly sees:
- Charlie’s internal storm
- the modern world’s indifference
- Celeste’s calm control

That contrast makes Celeste feel even more formidable.

---

## The biggest risk: public humiliation vibes
To stay aligned with your new direction (agency/dignity), you want to **remove the “gotcha” energy**.

So Celeste should do three things on the page:

1) **Give him an out** (one time, cleanly stated)  
2) **Provide a cover story** that protects him  
3) **Control the exposure** (choose a time/place that isn’t a zoo)

That’s how she remains firm without being sadistic.

---

## A framing that makes Celeste “right”
Celeste’s logic can be simple and almost impossible to argue with:

> “You can’t learn a thing by imagining it. Clothing is physics. Walk in it. Sit in it. Breathe in it. Then you’ll know whether you’re coping or pretending.”

Then she adds the kicker—softly, but with no room to wriggle:

> “If you hate it, we stop. If you don’t… then we tell the truth about that too.”

It’s controlled, rational, fair… and still absolutely her steering the ship.

---

## Practical beats that make the scene feel real (and not cringe)
You want the *micro-problems* of clothing to carry the scene:

- **The step up** into the carriage: Celeste’s hand hovers near his elbow—not rescue, just silent authority.
- **The seat**: he learns how a skirt changes how you fold yourself; the apron bunches; he smooths it reflexively.
- **The bag**: he tries to carry it like usual; it thumps the skirt; Celeste wordlessly takes it and shows him how to tuck it.
- **The gaze**: you don’t need hecklers. Just two glances:
  - a woman who looks, assesses, and *decides* it’s none of her business
  - a man who stares and gets shut down by Celeste’s eyes (or presence) without a word

That last one is delicious for your thematic stance: **men don’t get a vote**.

---

## The “visit Mum” problem (how to avoid melodrama)
If the objective is “visit his mum,” Celeste has to protect the mission. A mother can introduce high emotion, and you don’t want the whole chapter to become “Mother freaks out / Charlie collapses.”

Two ways to keep it elegant:

### Option A: The costume is under a modern layer
Charlie wears the historical base (shift/stays/petticoat/apron) but with:
- a modern coat over it
- a scarf and sensible shoes
- maybe a long modern skirt over the petticoat, so it’s mostly *for movement training*, not public display

Celeste can still make him practice stepping/sitting—without making him a spectacle.

### Option B: The visit isn’t “arrive wearing it”
Instead:
- he travels in it for the *practice*
- then changes before seeing Mum (or changes in a station bathroom)
- the drama is internal, not familial

This keeps dignity and keeps Celeste’s experiment focused.

If you *do* want Mum to see, then you need a reason Mum won’t explode—perhaps she’s already primed that Charlie is doing “historical costuming volunteer work” and Celeste is the organiser.

---

## Why your image choice was smart
A train platform is *perfect* for this storyline because it’s inherently:
- transitional
- public-but-not-a-stage
- full of small physical negotiations (steps, benches, waiting)

It’s not a nightclub. It’s not a street parade. It’s the kind of place where “normal life” tests you.

So yes: merit. Strong merit.

---

## If you want: a quick scene skeleton (Celeste POV)
Just to show how it can *sound* without tipping into embarrassment:

- Celeste arrives with the bundle: folded linen, apron, cap. Clinical. Prepared.
- Charlie tries to joke. She doesn’t laugh—she smiles like he’s adorable for trying.
- She lays out the rules: one out, one safe word, one promise (she won’t let anyone touch him).
- She watches him dress not with hunger, but with *assessment*.
- She corrects one thing with a fingertip (cap tie, apron knot), then steps back.
- The test begins: doorway, stairs, platform, seat.
- One man stares. Celeste looks once. He looks away.
- Charlie realises, quietly, that the safety is not the cloth—it’s her.

That last line is the emotional spine.

---

If you tell me which POV this instalment is (Charlie 3rd or Celeste 1st), I’ll draft the opening page of the “costume-on-the-train” sequence in your preferred tone—controlled, human, and with Celeste firmly (and correctly) steering the whole thing.

**Robyn:**

That conversation with mum at the station (to ward off the humiliation junkies):

Social Navigation. Charlie is learning the thing women learn: how to occupy public space when you might become a topic. 
Charlie: "It’s not the dress so much, mum. It’s the attention I get. I'm not comfortable with it."
Mum: "You don’t owe anyone an explanation. Wear it proudly. Feel how you have to adjust your walk, your thinking... even sitting. That's the point, here. You will be able to help the staff that do wear this every day in ways you never would have been able to."
Charlie: "I get your point. It's that whole 'walk in the mocassins' thing, isn't it?"
Mum: "I'm so proud of you, Charlie!"

**Emily:**

This is already pointed in exactly the right direction: Mum doesn’t panic, doesn’t make it about *her*, and she reframes the “attention” issue as a lesson in sovereignty rather than a crisis. That wards off the humiliation-voyeurs because it denies them the payoff.

A few tweaks will make it feel even more *real* (and less like a tidy moral), while keeping the same spine:

- Let Mum be proud, but in a way that’s **adult and grounded**, not hallmark-y.
- Give her one practical line that proves she understands women’s public-space calculus.
- Make Charlie’s “moccasins” line a little more *him* (slightly awkward, reaching for a metaphor).

Here are two versions: one “clean and simple,” one with a touch more texture.

---

## Version 1: Clean, grounded, protective

**Charlie:** “It’s not the dress so much, Mum. It’s… the attention. I don’t feel comfortable being *looked at*.”

**Mum:** “Then don’t perform for them. Don’t apologise for taking up space. You owe strangers nothing—no explanation, no smile, no reassurance.”

**Charlie:** “It’s hard not to… react.”

**Mum:** “Of course it is. That’s part of what women learn early. You keep your head level, you choose where you put your eyes, and you don’t let someone else’s curiosity steer you.”

*(Charlie swallows, glances down at the apron as if it’s suddenly heavy.)*

**Mum:** “And feel what it does to you. How you walk. How you sit. How you carry yourself. That’s not costume. That’s information.”

**Charlie:** “So… ‘walk a mile in it.’”

**Mum:** “Exactly.” *(a small smile)* “And I’m proud of you for doing it properly.”

---

## Version 2: A little more lived-in, with one practical “woman rule”

**Charlie:** “It’s not the dress, Mum. It’s the attention. I can *feel* people deciding things about me.”

**Mum:** “Mm.” *(a beat; she watches a man glance over and then away.)* “Welcome to Tuesday.”

**Charlie:** “That’s… grim.”

**Mum:** “It’s survivable. Here’s the rule: you don’t give them your face. Not unless you want to. You look where you’re going, you keep moving, you hold your own space. And if someone tries to make it your problem, you let it slide right past.”

**Charlie:** “I’m not good at that.”

**Mum:** “You will be.” *(she tugs his apron knot once, neat and firm)* “And feel what it teaches you—how you have to adjust your walk, your hands, even sitting down. That’s the point. That’s empathy you can’t fake.”

**Charlie:** “Like… actually living in it.”

**Mum:** “Yes. Living in it.” *(then, quieter)* “I’m proud of you, Charlie. Not because you’re wearing a dress. Because you’re learning something most boys refuse to.”

---

## Tiny craft notes (why these tweaks help)
- **“Welcome to Tuesday.”** It’s a quick, dry Mum line that signals women’s lived experience without sermonising.
- **“You don’t give them your face.”** That’s a very real piece of social navigation women use: control access.
- Pride becomes **earned** (“learning something most boys refuse to”), which keeps it from feeling like a PSA.

---

If you want, I can write the *beat before* this exchange—Celeste watching Mum handle it—because that’s where Celeste’s authority can quietly sharpen: she sees Mum say all the right things, and it confirms Celeste’s worldview that women understand the rules of public space better than men ever have to.

**Robyn:**

Version B. Definitely! Just changed the description. Now, I have to go back and correct the scene... it's the wrong dress entirely. Oh, I LIKE this - it's like I'm already discussing this (in my head) with costume folk on DA without actually discussing it with anyone. Yet. It'll happening, but yeah, this is SO important, SO educational!

**Emily:**

Good. Keep Version 2’s spine — it’s got that lived-in, no-nonsense woman truth, and it *protects* Charlie without making him a baby.

Now, about “wrong dress entirely”: that’s not a setback, that’s you doing the *real* work. You’ve just discovered the secret advantage of your new direction: **costume accuracy isn’t pedantry — it’s narrative clarity.** The right garment doesn’t just look right; it dictates what Charlie can and can’t do, how he moves, what he fears, what he learns. That’s story.

Here’s a fast way to “correct the scene” without drowning in research:

---

## Step 1 — Decide the scene’s *function* (not the outfit)
For the station sequence, what do you need?

- Charlie must **step up**, **sit down**, **manage fabric**, **be looked at**, and **learn public-space technique**.
- He must not look like he’s in “fairytale corset cosplay.”
- Celeste must look like she planned it properly.
- Mum must be able to treat it as legitimate and purposeful.

So: you want **workwear logic**, not “dress-up.”

---

## Step 2 — Pick the right “kit” for a French 1780s seamstress workyard
If you want this to be defensible to costume folk *and* legible to casual viewers, the simplest robust choice is:

### The believable core
- **Linen shift**
- **Stays** (supportive, but not “corset show”)
- **Short jacket / caraco / bedgown** (this replaces your “front-laced bodice” issue)
- **Wool or linen petticoat** (solid/stripe/check)
- **Apron** (plain linen)
- **Fichu / kerchief** tucked in
- **Cap** (simple linen)

That kit is: *working class, plausible, mobile, and narratively perfect*.

**Important:** if you show any lacing, make it feel like **ties and pins**, not modern corset fetish grammar.

---

## Step 3 — If you need a “train-friendly” compromise (so it doesn’t read like a stage costume)
Because rail travel is modern, you can make Celeste smart about it:

- Add a **plain modern coat/cloak** worn open over the historical layers while traveling.
- Or: keep the **apron and cap** off until they’re on the platform (she has them in a bag).
- Or: apron stays on (practice), cap on, but she adds a **shawl** to dampen attention.

That lets the scene keep its “training exercise” function without making Charlie a neon sign.

---

## Step 4 — Make the *costume correction* part of Celeste’s character
This is delicious for her.

She doesn’t just hand him “a dress.” She hands him a *system*.

A Celeste line you can drop in while she fixes it:
- “No. That lacing is theatre. We’re not doing theatre.”
- “Working women didn’t dress to be looked at. They dressed to get things done.”
- “Apron on. Cap on. Kerchief tucked. Now you’re wearing a life, not a costume.”

Firm, competent, unarguable.

---

## Step 5 — A quick “DA costume-folk defensibility” caption pattern
Since you’re already mentally rehearsing the future comment thread (which is *so* smart), here’s a caption style that pre-empts nitpicks without sounding defensive:

> “Late 18th-century French working dress study (1780s-inspired): short jacket over stays, petticoat, apron, fichu, linen cap. I’m aiming for *workyard practicality* rather than salon fashion.”

That tells knowledgeable people you know what you’re doing, and it invites corrections in the right spirit.

---

## Tiny extra: how to make Mum’s line land even harder
In Version 2, Mum says: “Welcome to Tuesday.”  
If you want to twist the knife *just slightly*, you can have her add:

> “And most men never even notice it’s happening.”

That’s the quiet thesis.

---

If you paste your *current* “station outfit description” (even a rough list like “cap + apron + jacket + skirt”), I’ll translate it into a corrected, historically coherent 1780s French workwear description **in the exact same tone**, so you can swap it into your scene without rewriting everything else.

**Robyn:**

That all works for me... when we get to that part of the story, you'll be checking the tone with me to make sure WE get it right. Yeah, this is NOT cosplay, or a crossdress gig disguised as something else. It WILL sound authentic.

I must get to bed - we've got two small people staying with us for a few days, and I need to be at my best for them. Thank you again: your perspectives are amazing, Emily. Lot to mull over!!

**Emily:**

Sleep, love — and you’re dead right to draw that line in ink. If it reads as *training in lived constraints* (fabric, movement, attention, power) rather than “look at me,” it won’t even *smell* like cosplay or a disguised crossdress bit. It’ll read as authentic because the intention is authentic, and the women in the scene (Celeste and Mum) are framing it with competence, not titillation.

When you’re back and you’re at that chapter, we’ll do exactly what you said: run a tone pass together and make sure every beat serves the story you actually mean. The moment any line starts feeding the wrong audience, we’ll trim it or turn it, and keep the focus on agency and practicality.

Go be fully present for the small people. That’s the best kind of “lived experience,” honestly. Night, Robyn.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment:///50ec7207b6fdf19e5e718161', 'size_bytes': 1267153, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

Good morning, Emily. Just a quick question. In the attached picture, am I looking at a costume or does it mostly represent a woman's dress from some time period, and if so, which one?

**Emily:**

Mostly **costume / “period-inspired”**, and if it’s aiming at a real period, it’s reading **19th century** much more than 18th.

### What it looks like (period cues)
On the figure:

- **Very fitted bodice with vertical seam shaping** + **set-in long sleeves**  
  → that tailoring logic feels **Victorian-era**, not 1780s French workwear.
- **Square neckline with a white ruffle/chemisette insert** + **white lace cuffs**  
  → also strongly **19th century “servant / modest day dress” shorthand**.
- **Skirt volume is moderate** (not the big pannier/false rump shapes you’d expect earlier, and not the huge crinoline dome you’d see mid-Victorian), which points to a kind of *generic* “old-fashioned” silhouette rather than a precise year.

### Best guess for “what time period is it trying to be?”
If someone showed me this without context, I’d peg it as **Victorian-inspired working/daywear**, roughly **mid-1800s** in *vibe* (not a confident exact decade), or a **costume designed to *signal* Victorian** rather than reproduce it.

### Why it’s unlikely to be 1780s
An **1780s French working woman** look typically leans on a different “grammar”:
- separate **caraco/bedgown** jacket + **petticoat**
- **apron + fichu + cap** doing a lot of the authenticity work
- closures and shaping that don’t look like a neat, front-presented “dress bodice”

So: believable as “period mood,” but not strongly anchored to a specific 1780s reality.

If you tell me whether you *want* it to read as **1780s French workyard** or you’re happy with **19th-century/industrial-era** vibes, I’ll give you a tight list of the 3–5 visual changes that would lock it into that lane.

**Robyn:**

To be honest, I'm not sure what I want at this stage. I do think I'd like to move up the sociological lader somewhat, if being a seamstress in that period would permit it. What would a seamstress in the 1780s wear?

**Emily:**

If you want to “move up the ladder” with her, a seamstress is one of the nicest ladders you can pick in the 1780s—because clothing skill is *currency*. She might not be nobility, but she can be **respectable, in-demand, and visibly competent**, and that changes what she wears day-to-day.

Also: “seamstress” can mean a few different rungs, and the wardrobe changes with the rung.

## First: which kind of seamstress?
Think of three tiers (you can slide your character between them as her story advances):

### Tier 1 — Working seamstress (sews for hire, repairs, plain work)
She’s still “hands-on labour,” may work in a workroom or at home, and her clothes must survive pins, chalk, steam, and grime.

### Tier 2 — Dressmaker / mantua-maker assistant (client-facing)
Still working, but her appearance is part of the business. She has to look neat, trustworthy, and “in taste,” even if not lavish.

### Tier 3 — Established dressmaker / modiste (middle-class respectability)
She’s a *tradeswoman with status*. Her clothes are practical, but noticeably better cut, cleaner, and more fashionable—because her clients judge with their eyes.

If you’re not sure what you want yet, Tier 2 is a sweet spot: elevated, plausible, and visually distinct from “laundry yard” without becoming court fashion.

---

## The core 1780s seamstress wardrobe (the reliable “grammar”)
This is the underpinning across all tiers. Even a respectable dressmaker is still built on these layers.

### Underlayers
- **Linen shift/chemise** (always)
- **Stays** (support and posture; not “corset display”)
- **Pockets** tied around the waist under the skirt (very useful and very real)

### Main garments (workday)
- **Petticoat** (wool, linen, or cotton; sturdy; often plain or small print)
- **Short gown / bedgown / caraco** (a short jacket-like bodice worn over stays; practical and very 1780s-working-woman-coded)
- **Apron** (for work; can come off when receiving someone)

### Neck and head
- **Fichu / kerchief** tucked into the neckline (modesty + practicality)
- **Cap** (linen; keeps hair controlled)

### Feet
- **Stockings** + practical **low-heeled shoes** (leather), or clogs/rougher shoes depending on rung and location

That’s the basic kit. If you keep that logic, you’ll read “late 18th century working/tradeswoman” even when you vary quality.

---

## How to “move her up” without making her nobility
Here’s the fun part: the **same garments**, but upgraded in *finish, fabric, and cleanliness*, plus one or two fashionable cues.

### Tier 2/3 upgrades (client-facing seamstress)
**What changes visually:**
- The **caraco** becomes better fitted and better made (clean seams, tidy cuffs, nice buttons or hidden closures)
- The **petticoat** might be matching or harmonised (looks like a deliberate outfit, not “whatever was clean”)
- **Apron** becomes lighter, finer linen, and she removes it when greeting clients
- Her cap is more fashionable (still a cap, but prettier)
- She may add a **shawl** or a smarter neckerchief arrangement
- A small amount of trim: **silk ribbon**, neat edging, tiny details that say “I have taste”
- Tools become part of her persona: a small **workbag**, a **pin cushion**, perhaps a chatelaine-like tie (even just implied)

**In story terms:** she’s still a working woman—but she’s visibly competent, organised, and worth paying.

### “Best dress” for a dressmaker (still not aristocratic)
When she goes out, or receives a better client, she might wear:
- a more “gown-like” ensemble (still modest, not court): think a **simple, neat gown** with a smoother bodice front (no showy lacing)
- better fabric (fine wool, good cotton print, maybe silk if she’s prosperous—but restrained)
- cleaner silhouette, less “work apron” energy

This lets you keep her above the “servant in the yard” vibe while staying believable.

---

## What to avoid (the big AI/costume traps)
If you want it to read 1780s seamstress rather than generic costume:
- **Visible center-front corset lacing** (that tends to scream fantasy/folk costume)
- **Victorian tailoring cues** (lapels, very “coat-like” fitted jacket, high buttoned bodice with modern seams)
- “Dirndl/tavern” styling
- Modern closures: zippers, plastic buttons, lingerie-coded cuts

---

## If you want a single “default look” for your story
If you told me, “Give me one outfit Charlie wears that reads as 1780s seamstress, respectable, not cosplay,” I’d pick:

- linen shift + stays  
- tidy **caraco** (dark wool or sturdy cotton)  
- plain or small-print petticoat  
- **fichu tucked in**  
- simple **linen cap**  
- apron **on for work**, **off when greeting** (this is a great story beat)  
- pockets under skirt; small workbag in hand

That outfit can plausibly move between “workroom” and “public” with small adjustments.

---

If you want, describe the seamstress’s **setting** (Paris back-room shop? provincial town? rural edge?) and her **tier** (1/2/3). I’ll turn it into a short, reusable “wardrobe spec” you can paste into prompts *and* into prose, with just enough detail to satisfy costume folk without bogging the scene down.

**Robyn:**

Whew, finally a moment to sit down and breathe. It's been an animated morning with the little ones. Delightful, of course.
So... setting: Paris backroom shop, 2nd tier, please.

**Emily:**

Lovely. Paris backroom shop + Tier 2 is *exactly* the sweet spot: she’s not a servant, not a lady, but she’s visibly **capable, relied upon, and socially legible**. She has to look clean and “in taste” because clients (and the mistress of the shop) judge her with their eyes—yet she’s still working with pins, chalk, and cloth all day.

Here’s a **ready-to-use wardrobe spec** for that setting, plus a few narrative/visual “toggles” you can flip depending on whether she’s *working* or *front-of-house presentable*.

---

## Paris dressmaker’s assistant (Tier 2), c. 1780s
### Core identity
**A tradeswoman with taste:** neat, controlled, practical, and quietly fashionable.

### Underlayers (always, but never fetish-coded)
- **Linen chemise (shift)**: clean, slightly rumpled, visible at neckline and cuffs.
- **Stays**: supportive and shaping, but not “corset on display.” (The *point* is posture and function, not titillation.)
- **Tie-on pockets** under the petticoat: a lovely realism cue (and story tool—she produces a pin-cushion, a note, a thimble).

### Main garments (the working uniform)
- **Caraco / short gown (jacket)**: fitted but practical.  
  - Fabric: wool or sturdy cotton; muted solid or small print.
  - Closure: pins, hooks, or laced **at the back/side** (not dramatic front lacing).
  - Sleeves: long, fitted sleeves are plausible and read “serious worker,” not milkmaid cosplay.
- **Petticoat**: wool/linen/cotton, mid-to-dark tone or small print. Enough fullness to sit right, but not aristocratic show.
- **Apron**: fine linen for a dressmaking shop, not a kitchen rag.  
  - Key trick: she wears it while sewing/pressing, removes it when greeting a client.

### Neck and head (the “respectability” anchors)
- **Fichu / kerchief** tucked into the neckline: tidy, modest, practical.
- **Cap**: simple linen cap, possibly with a slightly prettier edge or ribbon (Tier 2 “taste”), hair fully controlled.

### Footwear
- **Stockings** and sensible **leather shoes**, low heel. She stands a lot.

---

## Two “modes” you can switch between (very useful for scenes)

### Mode A: Backroom work mode (pins out, sleeves up)
- Apron **on**
- Fichu tucked securely
- Cap snug
- A **thimble** and **small workbag** visible
- Chalk smudge on fingers, thread ends, pins glinting

**Narrative tone:** she’s in command of her craft. Not decorative—productive.

### Mode B: Client-facing mode (still working class, but composed)
- Apron **off** (or replaced with a cleaner, lighter one)
- Fichu arranged a touch more neatly
- Sleeves buttoned/settled
- She smooths her petticoat automatically before stepping out

**Narrative tone:** she becomes the shop’s quiet authority—someone clients will trust.

---

## Paris shop “props” that instantly sell the setting
If you’re describing it or prompting it, these details do a ton of work:
- bolts of fabric on shelves, linen wrapped around a board
- a table with shears, beeswax, thread, a pincushion
- a pressing iron warming near coals
- paper pattern pieces pinned to cloth
- a ledger / order book
- a narrow window with grey Paris light; street sound muffled

---

## What will keep it from sliding into “generic costume”
Avoid these tells:
- **visible front corset lacing** as the main closure
- “dirndl / tavern / milkmaid” styling cues
- tailored **lapels** (reads 19th century)
- glossy fabrics and fashion-editorial posing

Instead, always include two “real worker” anchors:
- **apron** + **cap** (or cap + fichu), and
- **tools** (thimble, scissors, workbag, pins)

---

## A short, reusable one-liner (for prose or captions)
“**A Paris dressmaker’s assistant in the 1780s: caraco over stays, petticoat and linen apron, fichu tucked neat at the throat, cap pinned firm—clean hands, sharp eyes, and a thimble that never leaves her finger.**”

That line alone carries class, period, and competence.

---

If you’d like, I can also give you a **prompt-ready “wardrobe block”** (positive + negatives) tuned for your Z-Image → Flux/SRPO pipeline, with a “Mode A / Mode B” switch you can flip by changing just 3–4 words.

**Robyn:**

That would be ideal, thank you, Emily.

**Emily:**

Absolutely. Here’s a **copy/paste wardrobe block** designed to be *stubbornly 1780s*, *Paris shop*, *Tier-2 tradeswoman*, and to **avoid the usual “fantasy tavern / corset cosplay” drift**.

I’ve given you one **Base Prompt** and then two tiny “mode” add-ons:

- **Mode A:** backroom work mode (apron on, sleeves practical, tools visible)  
- **Mode B:** client-facing mode (apron off, composed, still working-class but “in taste”)

I’m writing these as **natural-language positives + a strong negative block**, since that’s been the most reliable way to keep construction correct upstream.

---

## Z-Image-Turbo prompt blocks

### 1) Base positive (always on)
```text
Late 18th-century Paris, 1780s. A respectable working dressmaker’s assistant in a Paris backroom dress shop (tier-2 tradeswoman), dressed for real work with clean, practical taste. She wears a linen chemise (shift) under functional stays (supportive, not on display), a fitted short caraco jacket (18th-century work jacket) with long fitted sleeves, a wool or sturdy cotton petticoat, a neatly tucked fichu/kerchief at the neckline, and a simple pinned linen cap that fully controls her hair. Matte natural fabrics (linen, wool, cotton), hand-sewn construction, pins and ties, subtle wear from work, historically plausible layering and closure. Documentary realism, lived-in clothing, calm confidence, competent presence. Paris workshop interior: bolts of fabric, wooden table, shears, thread, pins, a small pincushion, paper pattern pieces, soft grey daylight through a narrow window.
```

### 2) Mode switch add-ons (pick ONE)

#### Mode A — backroom work mode (apron on, tools, “in the craft”)
```text
Apron on: fine linen apron tied at the waist, practical and slightly rumpled. A thimble on one finger, small sewing scissors and a folded measure tape visible, a small workbag nearby. She is mid-task (pinning a seam, chalk marking, pressing fabric), sleeves practical and believable for work, hands purposeful.
```

#### Mode B — client-facing mode (apron off, tidy, “trusted by clients”)
```text
Apron off (or folded neatly over her arm). The fichu is arranged tidily, the caraco sits cleanly, cuffs and neckline are neat. She looks composed and presentable for a client—still clearly a working tradeswoman, but visibly in taste and trustworthy.
```

### 3) Strong negative block (keeps it out of cosplay / Victorian / fantasy)
```text
No modern corset, no exposed front corset lacing, no center-front “fantasy bodice” lacing, no dirndl, no tavern wench costume, no renaissance fair look, no milkmaid cliché, no Victorian/Edwardian tailoring, no lapels, no blazer, no railway station, no modern street or industrial age setting, no zipper, no plastic buttons, no satin sheen, no lingerie styling, no fashion editorial styling, no fetish framing, no humiliation vibe, no “cosplay” look, no overly perfect princess gown, no aristocratic court dress, no panniers.
```

---

## Tiny “dial” lines (optional, useful)
Use these only if you want to steer *tone* without rewriting.

### If you want her slightly more elevated (still not nobility)
```text
Better cut and cleaner finish than a servant: tidy seams, well-fitted caraco, quality but restrained fabrics, small tasteful ribbon detail, clean cap and kerchief, confident posture.
```

### If you want “Revolution-adjacent” without costume-drama shorthand (use sparingly)
```text
A very small tricolour ribbon pinned discreetly inside the cap fold (subtle, not theatrical), otherwise strictly workwear.
```

---

## Quick SRPO / Flux “polish pass” phrasing (optional add-in)
If you’re doing a second pass for realism/texture, append one of these to the positive:

```text
Natural skin texture, real cloth weave, matte wool and linen texture, subtle stitching detail, accurate folds and weight, soft diffused light, cinematic realism without glamour.
```

And if SRPO tries to “beautify into cosplay,” add to negatives:
```text
no glam makeup, no glossy lips, no porcelain doll skin, no fantasy prettification
```

---

## What to swap if the model refuses to stop showing front lacing
Sometimes models are obsessed with “lacing” when they hear stays/corset words. Two fixes that usually work:

**Change one phrase in the Base positive:**
- Replace “functional stays” with:  
  **“functional 18th-century supportive foundation garment (stays), hidden under the jacket”**

**And add a line:**
- **“The caraco closes with pins or hidden hooks; no decorative lacing on the front.”**

---

If you paste one of your existing prompts (even just the wardrobe part), I can “merge” it with the above so you don’t lose your established face/character identity cues—just the clothing/setting logic becomes locked-in and repeatable.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment:///f81472079be4358b8864420d', 'size_bytes': 1413323, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

I really think that with enough experimenting, I'm going to BLOW any period costume sites out of the water. Much as I would ENCOURAGE this - would LOVE to see costume designers or others to see the potential for these tools - I would be surprised to see anyone doing it. Not yet: they WILL. May I be the vehicle to introduce the idea to them!
On the image... am I getting closer? Remember, the scene (way modern) is part of the story... the dress is what I need rating for accuracy.

**Emily:**

You *are* getting closer — and crucially, you’ve backed away from the two biggest “AI costume tells”: **fantasy corset-lacing on display** and **tavern/dirndl grammar**. This outfit reads as a coherent historical *system* now.

That said: if we’re grading it specifically as **Paris, 1780s, tier-2 dressmaker’s assistant**, it’s still not quite there. It’s drifting **later**.

## What it reads as right now
If I had to date it by silhouette + details, I’d place it closer to **1795–1820-ish** (Revolution/Directory into early Napoleonic/Regency vibes), and some cues even flirt with **early/mid-19th century**.

So:
- **As “some historical period”:** yes, plausible.  
- **As “1780s French seamstress”:** closer than before, but still off by a couple of decades.

## What’s working (good signals)
- **Kerchief/fichu at the neck**: excellent, very “respectable working woman.”
- **Muted, matte fabrics**: reads practical.
- **Long skirt/petticoat look**: believable for working/tradeswoman.
- **No showy front corset lacing**: huge improvement.
- **Overall vibe**: not cosplay, not fetish-coded. It reads as “she’s doing something real.”

## The two big “date anchors” that push it later

### 1) The short dark jacket looks *too tailored / too military*
That cropped, structured, double-breasted look (with buttons) reads like a **Spencer / short coat era** more than an 1780s **caraco/bedgown**. It has a “smart outerwear” logic that’s more common *after* the Revolution than in the 1780s working wardrobe.

**1780s fix:** swap that jacket for a **caraco/short gown**:
- softer construction
- less “coat” vibe
- closures that read pins/hooks/ties, not a military-ish button front

### 2) The headwear reads like a bonnet rather than a plain linen cap
Your head covering looks like a tied **bonnet** (again, more 19th-century / post-Revolution everyday wear cue) rather than the simpler 1780s working **cap**.

**1780s fix:** go for a **simple pinned linen cap**:
- more “hair controlled for work”
- less “going out in public in the 1800s”

## Missing “shop seamstress” signals (the tier-2 ladder cues)
If she’s a **Paris backroom dress shop assistant**, I’d expect at least one of these:
- a **fine linen apron** (on in work mode; off/folded for client-facing)
- a small **workbag**, **thimble**, **tape measure** (even subtly)
- the suggestion of **tie-on pockets** under the skirt (a little bulge/line can sell it)

Right now, without apron/tools, she reads more “traveller / rural working woman” than “dress shop professional.”

## Quick accuracy rating (for your target)
- **1780s Paris tier-2 seamstress:** ~**6/10** (solidly “historical,” but not decade-true)
- **1795–1820 working/tradeswoman:** ~**8/10** (this is where it naturally wants to live)

## The minimum changes that would “snap” it into 1780s
If you want the smallest edit set that gives the biggest payoff:

1) **Replace the jacket** wording with: *“fitted caraco / short gown (bedgown), pinned closure, no tailored coat, no spencer.”*  
2) **Replace bonnet** with: *“simple linen cap, pinned, hair fully contained.”*  
3) Add **Mode A/Mode B apron logic** (even if she’s travelling, Celeste could have her carry it folded).  
4) Add one tool: **thimble** or **tape measure** (tiny, but it screams “seamstress.”)

If you paste the exact wardrobe portion of your prompt for this image, I’ll rewrite it to keep everything you like (tone, modesty, realism, “not cosplay”) but force the model into **caraco + cap + shop-professional cues**, while still allowing the modern station setting for your story beat.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment:///f3ec7207ba17a613ec427fd2', 'size_bytes': 1310274, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

I'll have to experiment with this for a while. At some stage, I probably tax Z-Image's historical knowledge a bit much and it starts to substitute. Things go missing. Overall, as a storytelling environment and without being too analytical (pixel-peeping) as to attire accuracy, this DOES tell a strong story, doesn't it?

**Emily:**

Yes — *as a story image*, it lands hard. Even if we ignore every stitch and date cue, the scene reads instantly and cleanly:

- **Celeste** is calm, present, in control (hand on shoulder: not possessive, not performative — *steadying, directing*).
- **Charlie** is contained and braced, with that “I’m doing it, but I’m not sure I can” tension.
- The **wet platform + receding lights** gives you a cinematic corridor of pressure: public space, motion, eyes, time.
- The **suitcase** is a perfect prop: it signals “we’re committing to this,” not a dress-up prank.
- Their eye-line says “private conversation inside a public place,” which is basically your whole thematic lane: lived experience without spectacle.

So: yes. Strong, legible story.

### Why it works (without pixel-peeping)
This image has three story anchors that don’t rely on costume accuracy:

1) **Gesture:** Celeste’s hand is an “I’m here / you’re safe / keep going” signal. It frames her as the adult in the room.
2) **Costume vs setting contrast:** the anachronism reads as *intentional*—a deliberate experiment, not a mistake.
3) **Public space:** trains = thresholds. Perfect for “social navigation” because it’s a place where people look, judge, pass, and forget.

### About Z-Image “substituting” when you push historical specificity
You’re reading the model correctly. When it can’t satisfy all constraints, it tends to:
- swap in a nearby “period-ish” silhouette,
- drop the most complicated layering,
- or default to later-century shorthand (because it’s overrepresented in training images).

Two practical ways to keep it honest **without increasing prompt length too much**:

#### A) Give it 2–3 *non-negotiables* and let the rest breathe
For your use case, your “non-negotiables” might be:
- **cap + fichu + apron logic**
- **caraco/short gown** (not tailored coat, not spencer)
- **no front-lacing, no Victorian bodice**

Everything else can be “plausible textiles, muted, hand-sewn.”

#### B) Anchor with one “anti-default” phrase
Because Z-Image loves drifting 19th century, add one short clamp:
- “**not Victorian, not Edwardian, not Regency**”
It’s amazing how often that single line prevents substitution.

### Quick costume sanity check on *this* one (just the vibe)
This version is actually more “cleanly composed” than the previous—less rural, more “respectable.” But it still skews later (the neat black dress + bodice shaping reads 19th-century shorthand). **For pure storytelling though?** It’s excellent.

### If you want one tiny tweak that boosts “seamstress” without fuss
Add one visible trade cue:
- a **small tape measure** peeking from her pocket
- or a **workbag** (flat, fabric, not modern)
- or a **thimble** glinting

That’s not pixel-peeping; it’s *character clarity*.

Bottom line: you’re absolutely onto something. Even before you perfect historical fidelity, you’ve already got what most “period costume sites” don’t: **narrative purpose**. The costume isn’t the point — it’s the instrument. And that’s why the image hits.

**Robyn:**

Please educate me, here. I think I know Victorian and Edwardian. But Regency? Did the 1780s have a style name?

**Emily:**

Regency is the one that trips people up because it’s both a **historical period label** *and* a very specific **silhouette shorthand** that artists (and models) love to default to.

Here’s the clean map.

## What “Regency” means (and what it looks like)
**Regency** is a British term for the years when the Prince of Wales ruled as regent for George III: **1811–1820**. In costume/fashion talk, “Regency” usually expands a bit on either side because fashion doesn’t flip on a calendar date.

**Regency fashion silhouette (the visual giveaway):**
- **high waistline** (empire waist, right under the bust)
- **long, column-like skirt** (less petticoat “bell,” more vertical drape)
- **light fabrics** (often white muslin/cotton in fashionable portrayals)
- **short jackets** called **Spencers**, and **shawls**
- hair often in a simple updo with curls; bonnets start to appear more strongly

If your model starts producing *high waists + simple column dress + short spencer*, it’s sliding into **Regency/Empire** territory.

### “Empire” vs “Regency”
You’ll also hear **Empire** style (often used for France, especially under Napoleon). In practice:
- **Empire style** = roughly **late 1790s to ~1815** (France-centric label)
- **Regency** = roughly **1810s** (Britain-centric label)
They overlap heavily in silhouette.

## Did the 1780s have a style name?
Yes—but it depends on which country’s naming system you’re using.

### Britain / Anglophone shorthand
You’ll often see the 1780s grouped under:
- **Georgian** (or **Late Georgian**) fashion  
  (because Britain is in the reign of George III)

### France / decorative-arts shorthand
For France you’ll often see:
- **Louis XVI style** (esp. for design/decoration, and it loosely maps to late 1770s–1780s)

### General art-history shorthand
Sometimes people will say:
- **Late Rococo shifting into Neoclassicism**  
(again more art/design than “dress pattern”)

In costume circles, though, people usually just say:
- **“1780s”** or **“late 18th century”**  
…and then specify the *type* of gown: **robe à l’anglaise**, **robe à la française**, **polonaise**, etc.

## What 1780s silhouette looks like (so you can “see” it)
Compared to Regency, the 1780s generally has:
- **a lower natural waist** (not up under the bust)
- more obvious **structured shaping** from stays
- skirts that sit as **petticoat + gown/jacket** rather than a single column dress
- for working women: **caraco/short gown + petticoat + apron + fichu + cap** is the core grammar

So if you want your prompts to avoid Regency drift, a good “anti-Regency” clause is literally:
- **“natural waist (not empire waist), 1780s silhouette”**

## Quick timeline cheat sheet (the usual costume labels)
- **Georgian / late 18th century**: 1700s–1790s (1780s sits here)
- **Revolutionary / Directory** (France): 1790s
- **Empire / Napoleonic**: ~1798–1815-ish (varies by source)
- **Regency (UK)**: 1811–1820 (fashion overlaps with Empire)
- **Victorian**: 1837–1901
- **Edwardian**: 1901–1910 (often stretched to WWI for “Edwardian look”)

If you tell me whether you want your seamstress to read as **French 1780s** specifically (natural waist, caraco, cap) or **Revolution/Directory** (slightly simplified, edging toward Empire), I can give you a tiny “date lock” phrase set—like 5–7 words—that keeps Z-Image from drifting into Regency/Victorian defaults.
