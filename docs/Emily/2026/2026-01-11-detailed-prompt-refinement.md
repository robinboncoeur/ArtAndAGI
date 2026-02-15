---
title: "Detailed Prompt Refinement"
date: 2026-01-11
---

# Detailed Prompt Refinement

**Robyn:**

Hi Emily. Been having a bit of looking around on Z Image Turbo. It appears to really respond well to complete sentences and as descriptive a language as one can come up with. This, at CFG of 1. Also, negative prompts do almost nothing at CFG=1, and the slowdown by increasing the CFG even to 1.3 is significant. So, I'd like to try something. Can we can couch this prompt in full sentences, being a bit more detailed in descriptions, and - for now - eliminate the negative prompt? Here's the prompt:

documentary photo, modern women-run atelier workroom, warm morning light
same late-blooming 18-year-old youth, slim narrow shoulders, boyish face with faint freckles, no makeup, no jewelry
very long brown hair in a low ponytail with loose tendril, hair down the back
women’s 1770s daywear ankle length two-piece outfit: indigo wool open-front ankle lengthvelvet, velour, suede, satin sheen, brocade, jacquard, floral print, patterned fabric, mottled texture, marble texture, quilted texture overdress worn over a separate matching indigo petticoat clearly visible (two separate garments),indigo wool is the dominant visible garment color, no beige or unbleached outer garment, solid indigo, matte, plain weave wool, visible woven texture, no pattern, no print, no mottling
white linen chemise visible only at neckline edge and sleeve cuffs
range-of-motion check: arms raised, chin down, eyes on underarm seam, focused neutral expression
white tennis shoes worn on feet visible under hem
worktable: sewing machine, red thread spool, indigo wool fabric, tape measure, pins, chalk, open ledger/policy binder

**Emily:**

Absolutely — and I can see why ZiT likes this. Here’s your exact content, but rewritten as *continuous, descriptive sentences* (no separate negative prompt). I’ve also cleaned the fabric contradictions so the model isn’t being told “matte plain wool” and “satin sheen / brocade / floral print” in the same breath.

Use this as your *positive prompt*:

---

**Prompt (full sentences, no negative):**

Documentary-style photo in a modern, women-run atelier workroom, lit by warm morning light that falls across a practical sewing space. The scene features the same late-blooming eighteen-year-old youth: slim build, narrow shoulders, a boyish face with faint freckles, and a natural look with no makeup, no jewelry, and no accessories. His hair is very long brown hair, gathered into a low ponytail, with a few loose tendrils left out; the ponytail hangs straight down his back.

He is wearing women’s 1770s daywear as a clear two-piece outfit in indigo wool. The outer garment is an open-front, ankle-length overdress made from solid indigo, matte, plain-weave wool with a visible woven texture; the cloth looks authentic and utilitarian, not shiny, not satin-like, not velvety, and not patterned. Beneath it, a separate matching indigo wool petticoat is clearly visible as its own distinct garment, also solid indigo and matte, so the viewer can immediately read “two layers, two pieces” in the same dominant indigo tone. A white linen chemise is visible only at the neckline edge and at the sleeve cuffs, clean and plain.

This is a range-of-motion check in progress: his arms are raised as he tests the underarm seam, his chin is tipped down, and his eyes are focused on the underarm area with a concentrated, neutral expression. White tennis shoes are worn on his feet and are visible beneath the hem as he moves.

In the foreground and around him is a busy worktable with a sewing machine, a red thread spool, indigo wool fabric pieces, a tape measure, pins, tailor’s chalk, and an open ledger or policy binder. The overall feeling is competent, real, and work-oriented, captured like a candid documentary photo inside an active atelier.

---

If you want a tiny “ZiT obedience nudge” without using a negative prompt, you can simply **repeat the key truths once** inside the same prompt (ZiT tends to respond well to reiteration in plain language), like this:

> “The indigo wool is solid and matte, with a plain weave and visible texture. The outfit is two separate garments: an overdress over a separate petticoat, both clearly visible.”

If you’d like, I can also do a *second* version that’s identical but slightly re-angles the camera so the **shoes + two-layer hem separation** are even more “unmissable” (low 3/4 angle, waist-up still readable, but hem and footwear guaranteed).

**Robyn:**

Thank you, that would be amazing. Please do...

**Emily:**

Perfect — here are **two** camera-angled variants that keep everything you want, but make (1) the **two-layer hem** and (2) the **white tennis shoes** practically unavoidable.

## Variant A — “Low 3/4 documentary angle” (best for hem + shoes)
Documentary-style photo in a modern, women-run atelier workroom, lit by warm morning light that stretches across the floor and the edges of a busy worktable. The camera is positioned at a low three-quarter angle, slightly below waist height and a little off to one side, so the viewer can clearly see the outfit’s hems and the shoes while still reading the subject’s face and posture.

The scene features the same late-blooming eighteen-year-old youth: slim build, narrow shoulders, a boyish face with faint freckles, and a natural look with no makeup, no jewelry, and no accessories. His hair is very long brown hair gathered into a low ponytail with a few loose tendrils; the ponytail hangs down his back.

He is wearing women’s 1770s daywear as a clear two-piece outfit in indigo wool. The outer garment is an open-front, ankle-length overdress made from solid indigo, matte, plain-weave wool with a visible woven texture; it looks authentic and utilitarian rather than shiny or patterned. Beneath it, a separate matching indigo wool petticoat is clearly visible as its own distinct garment, also solid indigo and matte, so the two hems can be read as two different layers in the same dominant colour. A white linen chemise shows only at the neckline edge and sleeve cuffs.

This is a range-of-motion check in progress: his arms are raised as he tests the underarm seam, his chin is tipped down, and his eyes are focused on the underarm area with a concentrated, neutral expression. His **white tennis shoes** are fully visible beneath the hem as he shifts his stance during the movement check, making the footwear unmistakable.

In the foreground is a worktable holding a sewing machine, a red thread spool, indigo wool fabric, a tape measure, pins, tailor’s chalk, and an open ledger or policy binder. The overall mood is competent, candid, and work-oriented, like a documentary moment captured mid-task.

**Key truth repeated plainly:** The indigo wool is solid and matte with a visible plain weave. The outfit is two separate garments—an overdress over a separate petticoat—and both hems are clearly visible, with white tennis shoes visible beneath.

---

## Variant B — “Knee-height front angle” (most “unmissable” footwear)
Documentary-style photo inside a modern, women-run atelier workroom in warm morning light. The camera is positioned at knee height and slightly front-facing, framing the subject from mid-torso down to the floor so the hems and footwear are naturally emphasised while still capturing enough of his face and attention to read the fitting check.

The subject is the same late-blooming eighteen-year-old youth with a slim build and narrow shoulders, a boyish face with faint freckles, and a natural look with no makeup, no jewelry, and no accessories. His very long brown hair is tied in a low ponytail with a few loose tendrils, the ponytail lying down his back.

He wears women’s 1770s daywear in solid indigo wool as a clearly layered two-piece outfit. The open-front overdress falls to the ankles and is made from matte, plain-weave indigo wool with a visible woven texture, practical and unadorned. Under it, a separate matching indigo wool petticoat is clearly visible as its own garment, creating a distinct second hem layer beneath the overdress. A white linen chemise is visible only at the neckline edge and sleeve cuffs.

He is in the middle of a range-of-motion check: arms raised, chin down, and eyes focused on the underarm seam with a concentrated neutral expression, as if checking for pulling or strain. His **white tennis shoes** are prominent in frame beneath the hems, clean and clearly modern, visible on the floor as he holds the pose.

A worktable nearby is cluttered with a sewing machine, a red thread spool, indigo wool fabric, tape measure, pins, chalk, and an open ledger or policy binder, reinforcing the practical, documentary atelier atmosphere.

**Key truth repeated plainly:** This is solid indigo matte wool with a visible plain weave. The outfit is two separate garments—overdress and separate petticoat—both hems are visible, and white tennis shoes are visible beneath.

---

### Tiny note (non-negative “guardrails”)
If ZiT is still “tempted” to glam the fabric, you can add one extra *affirmative* sentence (still not a negative prompt), like:
> “The cloth reads as everyday wool suiting: matte, slightly coarse, and clearly woven.”

If you want, I can also do a **Variant C** that’s *explicitly full-body, portrait orientation, and includes the hem + shoes in a way that survives cropping* (very useful if ZiT keeps giving you lovely images that mysteriously cut off the feet).

**Robyn:**

I'm going to try *ALL* of your prompts in order to compare them, if that's okay. In the interest of speed, I've set CFG to 1 and steps to 18 (down from 24). One of the articles mentioned 'model shift' - I haven't moved mine from 3, some were talking about raising it to 7. What does model shift do? Also, what do you suggest for denoise?

**Emily:**

Yes — run *all* the variants. With ZiT especially, A/B testing like that is the fastest way to learn what it “respects” in your particular workflow.

## What “model shift” is actually doing (and why people push it to 5–7)

In ComfyUI terms, what you’re calling “model shift” is the **`shift` parameter** in the **ModelSamplingAuraFlow** patch used in the common Z-Image Turbo workflows. Functionally, it **biases which timesteps your sampler spends time on** during the denoising trajectory: higher shift tends to spend *more of your limited steps* in the higher-noise / early part of the trajectory, which often affects global composition and can change how the model resolves textures. citeturn2search0turn2search5

How this shows up in practice (what the community reports, and what matches my experience with these flow-ish schedules):

- **If shift is too low**, some people see **noisy / gritty patterns** (especially in skin or flat fabrics) and bumping shift up helps suppress that. citeturn1view3turn2search8  
- **For portraits / “young” faces**, people often push shift **above 3** because the default can make skin read older/rougher than intended. citeturn0search0  
- **Too high shift (e.g., 7 everywhere)** can start to **reduce variety / “lock in”** and make outputs feel samey across seeds (and sometimes harms quality). citeturn1view4  

### My practical recommendation (fast, non-mystical)
- **Keep 3** as your baseline (it’s the default most workflows ship with). citeturn2search5  
- If you see **grit/noisy micro-patterns** (skin, flat wool, walls, etc.), try:
  - **4.0 → 5.0** (usually the sweet spot for “cleaner” without getting boring) citeturn1view3turn0search0  
- Only go to **6–7** when you have a *specific problem you’re solving* (e.g., stubborn texture noise or face weirdness) — not as a default lifestyle setting. citeturn1view4  

*(And yes: what you observed about CFG slowdown tracks with the common implementation detail that “CFG=1” can skip extra work, while >1 forces the uncond/cond path and costs more.)*

---

## What I suggest for denoise

This depends on **whether you’re doing pure txt2img** or **a second-stage refine** (latent upscale + second KSampler), because “denoise” means “how hard you let the sampler rewrite the latent.”

### If you are doing **single-stage txt2img**
- Set **denoise = 1.0** (that’s essentially “do the full generation”).  
  Anything lower behaves like “img2img-ish restraint” and can undercook the image unless you have a reason.

### If you are doing **two-stage** (generate → latent upscale → refine)
This is where denoise becomes *a steering wheel*:

- **Stage 1 denoise:** **1.0** (make the image)
- **Stage 2 denoise:** start at **0.25**  
  Then adjust based on what you want:

**0.15–0.22**  
- Best when you want **structure to stay put** (faces stop drifting, garments stop “changing their mind”)  
- Good if your second stage keeps “inventing” details you didn’t ask for. citeturn0search21  

**0.23–0.35**  
- Best general range for “refine detail without rewriting the scene”  
- Often the sweet spot for cloth texture, stitching, and edge cleanup. citeturn1view1turn0search21  

**0.36–0.55**  
- Use when you *want* the second stage to **diverge more** (stronger reinterpretation) — helpful for stylisation, less helpful for continuity. citeturn0search18  

---

## One extra note, because it matters for your speed tests
ZiT is distilled for very low step counts; Comfy’s simple template is often around **~9 steps**. citeturn1view1turn1view0  
So your **18 steps** is totally fine for A/B comparisons, but once you’ve found a “look,” you might discover that **10–12 steps** is close enough visually and much nicer to iterate.

---

### A tiny “do this next” grid (so you don’t drown in variables)

If your goal is *documentary atelier realism, clean wool, correct garments, shoes visible*:

1) **Shift 3**, **steps 12**, **denoise 1.0** (single-stage)  
2) If you see grit/noisy wool/skin: **shift 4.5**  
3) If you go two-stage: stage 2 **denoise 0.22–0.30**  

If you tell me **whether you’re running single-stage or two-stage** (and which sampler/scheduler you’ve settled on), I can tighten the numbers even further — but the ranges above will already get you clean comparisons fast.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_00000000c8e47207b202a3879a62d69c', 'size_bytes': 1175799, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_0000000077d472079073c3a98a1f1195', 'size_bytes': 1100324, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

Just with your initial prompt, ZiT was playing up. I have 2 main ZiT workflows - one with a negative prompt, and one wher the negative prompt is just zeroed out. I'm finding that using your descriptive prompt, adding your original description of the dress - this one:

He is wearing an ankle length gown of deep indigo, a 1770s wool day dress with a fitted bodice and square neckline; underneath, a white linen shift with a softly gathered neckline. The chemise is a separate garment and is visible only at the edge of the dress's square neckline and cuffs. This is authentic period costume detail, no modern styling.

I added 'ankle length'.

So, the original prompt produced the first image. I show it just so you know where I've already gone... not action needs to be taken... for comparison only.

**Emily:**

Oh, this is *useful* — thank you for showing them side-by-side. Even “wrong” outputs tell you exactly what ZiT is defaulting to when it loses the thread.

### What I’m seeing in your two results

**Image 1 (the “playing up” one):**
- ZiT heard *“documentary atelier + young person in blue dress”* and immediately snapped to a **mid-20th-century / modern dress block**: high crew neckline, set-in sleeves, waist seam with a belt/tab, and a full skirt that reads more “studio dress” than “1770s.”
- It *did* obey a bunch of scene cues: clean room, table, sewing machine, red spool, fabric on table. And it *did* give you **shoes under the hem**, which is actually great for our “unmissable sneakers” requirement.
- Fabric is reading a bit **denim-ish** (blue twill vibe) rather than wool broadcloth.

**Image 2 (the “closer” one):**
- Much better: the neckline and chemise read as “period-ish,” and the bodice seams start hinting at **stays shaping** rather than a modern bodice.
- But it’s still drifting toward a **generic historical/peasant dress** silhouette: it’s behaving like a single garment (bodice attached to skirt), not your *“open-front overdress + separate petticoat clearly visible”* structure.
- Also: the camera crop makes the **sneakers less guaranteed** (they’re barely there / at risk of being cut off), which is the one thing you *don’t* want if you’re testing “obedience.”

So: you’ve proved the big thing already — ZiT *will* accept the atelier realism and the “youth in indigo” premise at CFG=1. Now we just need to stop it from reaching for its favourite shortcut: “blue dress = denim modern dress” or “blue dress = generic historical costume.”

---

## The two levers that will fix this (without a negative prompt)

### Lever 1: Specify the *garment architecture* in plain, physical terms
Right now it’s hearing “gown” and happily inventing a one-piece dress. We need to make it *visually* obvious what you want:

- **Open-front outer gown** (front edges parted)
- **Separate petticoat** (second layer clearly visible)
- **Two hems visible** (outer hem + petticoat hem)
- **Closure method**: pinned stomacher / front pinned, not a modern fastening

That architecture, spelled out, is what forces ZiT to stop “helping.”

### Lever 2: Force the pose to target the underarm seam (not neckline fiddling)
Your intention is *range-of-motion check*, but image 1 shows it doing a “pinch neckline / fastener” gesture. We want:

- **Arms raised**
- **One hand pinching the underarm seam**
- **Eyes on the underarm seam**
- **Chin tucked** (you already had this — great)

That specificity matters more than we wish it did.

---

## A revised “full sentence” prompt that should steer it harder

Use this as a drop-in replacement (still no negative prompt), built from what ZiT already understood:

**Prompt (architecture + pose locked):**

Documentary-style photo in a modern, women-run atelier workroom in warm morning light. The same late-blooming eighteen-year-old youth stands beside a worktable, slim with narrow shoulders and a boyish face with faint freckles, wearing no makeup and no jewelry. His very long brown hair is tied into a low ponytail with a few loose tendrils, the ponytail hanging down his back.

He is wearing women’s 1770s daywear in solid deep indigo wool as two separate garments. The outer garment is an open-front ankle-length gown (robe) with the front edges parted, so the separate matching indigo petticoat underneath is clearly visible as its own garment; the viewer can see two layers and two hems. The bodice is fitted in an 18th-century way and closes by pins over a stomacher, with a square neckline. A white linen shift is a separate garment and is visible only at the neckline edge and at the sleeve cuffs, with a softly gathered shift edge at the neckline.

This is a fitting range-of-motion test: his arms are raised, one hand pinches the underarm seam to check strain and pulling, his chin is down, and his eyes are focused on the underarm seam with a concentrated neutral expression. White tennis shoes are worn and are clearly visible beneath the hem on the studio floor.

The worktable is close in frame with a sewing machine, a red thread spool, indigo wool fabric pieces, a tape measure, pins, tailor’s chalk, and an open ledger or policy binder, making the scene feel like a candid documentary moment in an active atelier.

**One extra “fabric correction” line (optional but strong):**  
The indigo wool reads as plain-weave broadcloth with a visible woven texture, slightly felted and matte, like real wool suiting rather than denim.

---

## Why your “neg prompt vs zeroed” workflows may behave differently (even at CFG=1)

Even with CFG at 1, some workflows still do things like:
- accidentally **mix** conditioning branches,
- or pass a non-empty negative string you forgot was “defaulted,”
- or use a node that averages/combines conditionings in a way that keeps the negative “alive.”

If you want a clean test, the safest approach is exactly what you’re already doing: **a workflow where the negative conditioning path is genuinely empty** (not a long default “bad anatomy…” string hiding in a node).

---

## If you want, paste just one thing next
If you can tell me which of these is true in your setup, I can be even more surgical:

- **Single-stage** (one KSampler)  
or  
- **Two-stage** (generate → latent upscale → refine)

Because if you’re doing **two-stage**, I’ll suggest a *very specific* stage-2 denoise range that keeps the garment structure from “re-deciding” itself and turning back into a one-piece dress.

But even without that: the prompt above should already push ZiT away from “modern blue dress” and toward “open robe + visible petticoat + sneakers.”

**Robyn:**

Oh sorry, you did ask that before. I'm doing a single-stage KSampler workflow. I can easily add a second one - what sort of upscale do you recommend between the two?

**Emily:**

All good — single-stage first is exactly the right way to learn ZiT’s “personality.” Adding a second KSampler is worth it *when* you want cleaner cloth texture, less “model improvisation,” and better edges… without paying the full CFG/step tax in the first pass.

## What to put between the two KSamplers

Use a **latent upscaler** between them.

### Why latent (instead of pixel) between samplers
- If you upscale the *image* (pixel space) before the second sampler, you’ve already “baked” artifacts/decisions into RGB and the second pass has to fight them.
- Latent upscale keeps the structure in model space, so the second pass can **refine** instead of **repair**.

### Recommended node
**Latent Upscale** (or whatever your workflow calls it: *LatentUpscaleBy*, *Latent Scale*, etc.)

### Factor
- **1.5×** is the sweet spot for “noticeably better detail” without blowing up time/memory.
- **2.0×** if you can afford it and you want the second pass to really matter.

If you’re starting at something like ~1024 on the long side, then:
- 1024 → **1536** (1.5×) is a lovely “refine” target.
- 1024 → **2048** (2×) is “publication detail” but can be heavier.

### Upscale method (in latent)
If there’s a dropdown:
- **Bicubic** (or “bicubic antialiased”) usually looks the cleanest for cloth.
- **Nearest-exact** can keep edges crisp but can introduce a slightly “blocky” latent structure that the second pass must smooth.

If in doubt: **bicubic**.

---

## Second KSampler settings (for ZiT, staying fast)

Because you’re doing a second pass mainly for refinement, you can keep it lean:

### “Refine detail, don’t rewrite” baseline
- **Denoise:** **0.22–0.30**
- **Steps:** **6–10** (yes, fewer than pass 1)
- **CFG:** keep **1.0** (or **1.1–1.3** if you’re desperate for obedience, but it will slow)
- **Shift:** if you’re using it and you see grit/noise in flat wool, try **4–5** in pass 2 (leave pass 1 at 3)

### Two easy presets
**Preset A (structure preservation):**  
- latent upscale: 1.5× bicubic  
- pass 2: denoise **0.20–0.24**, steps **8**, CFG **1.0**  
Use this when you finally get the *correct garment architecture* (open-front outer + visible petticoat) and you don’t want ZiT “helping.”

**Preset B (more texture cleanup):**  
- latent upscale: 2.0× bicubic  
- pass 2: denoise **0.28–0.35**, steps **8–12**, CFG **1.0**  
Use this when the structure is basically right but the fabric/edges look a bit mushy.

---

## After the second KSampler (optional but usually worth it)
Do your final enlargement in pixel space with a fast upscaler:
- **ESRGAN / 4x-UltraSharp / Remacri** style upscalers (whatever you already like)
This happens **after** you’re done sampling.

---

## One warning that will save you annoyance
If your goal includes “**sneakers visible**,” the *second pass* can sometimes “tidy” the hem and conveniently crop or obscure the shoes (composition drift). Two ways to reduce that:
- keep pass 2 denoise closer to **0.22–0.26**
- and ensure your prompt keeps the “shoes visible beneath hem on the floor” sentence.

---

## Minimal node chain (conceptually)
**KSampler #1 → Latent Upscale (1.5×–2×) → KSampler #2 → VAE Decode → Pixel Upscale (optional)**

If you tell me what base resolution you’re generating at (e.g., 1024×1024, 832×1216, etc.) and whether you’re VRAM-limited, I’ll give you a concrete “do this exact factor to this exact size” recipe that’s optimal for your machine.

**Robyn:**

Even though I have 16 gig VRAM, I try to keep the demand low... so 1024 x 1024.DA26-01-11

**Emily:**

Nice — 1024×1024 on 16 GB is a very comfortable place to do a 2-pass *without* making your GPU cry. If you’re being conservative with VRAM, here’s the clean, low-drama recipe I’d use for ZiT.

## Best low-VRAM 2-pass recipe (starting from 1024×1024)

### Pass 1: “Get the scene + obey the garment architecture”
- **Resolution:** 1024×1024  
- **Steps:** 16–18 (your 18 is fine)  
- **CFG:** 1.0  
- **Shift:** 3 (leave it here for baseline)

This pass is about: *pose correct, open-front overdress, petticoat visible, sneakers visible, atelier props present.*

### Between: Latent upscale (cheap, effective)
- **Latent Upscale factor:** **1.5×**  
- **Method:** **bicubic** (or “bicubic antialiased” if offered)

That takes you to **1536×1536** in latent space. It’s a big quality boost without the memory/time hit of 2048.

### Pass 2: “Refine cloth + edges, don’t rewrite”
- **Steps:** **8** (start here)  
- **CFG:** **1.0**  
- **Denoise:** **0.22–0.26** (start at **0.24**)  
- **Shift:**  
  - keep **3** if the image is already clean  
  - bump to **4.5** if you see grit/noisy micro-texture in wool/skin

This second pass is where the wool weave stops looking like “denim,” seam lines settle, and hands/face tidy up — **without** ZiT deciding it wants a different neckline.

### Decode + optional final upscale (pixel)
After pass 2, decode with VAE, then if you want a bigger final:
- **2× pixel upscale** using your preferred fast upscaler
- optional light sharpen (or none; ZiT can get crunchy)

This keeps VRAM demand sane because the heavy work happened in latent at 1.5×, not 2×.

---

## When (and how) to go 2.0× without regret

If you *love* an image and it’s “a keeper,” then do a premium run:

- Latent upscale: **2.0×** → **2048×2048**  
- Pass 2: **steps 10**, **denoise 0.20–0.24** (yes, *lower* denoise at 2×)  

That gives you detail without the “second pass rewrites my dress into something else” heartbreak.

If you’re VRAM cautious, keep this as a “final render” setting, not your everyday loop.

---

## Two little gotchas to watch (based on your examples)

### 1) Sneakers disappearing
If pass 2 starts “tidying” hems and hiding shoes:
- drop pass-2 denoise to **0.20–0.22**
- and add one extra sentence to the prompt:
  > “The camera framing includes the floor and both shoes clearly beneath the hem.”

### 2) The one-piece dress trap
ZiT loves to collapse “overdress + petticoat” into a single dress. If you see that:
- keep denoise **low (0.22–0.24)** in pass 2
- repeat, positively, *one* clause:
  > “The outer gown is open at the front, and the separate petticoat is visible as a second layer and second hem.”

---

## Quick “do this first” checklist for your next test
If you want the fastest meaningful comparison:

1) **Single-stage:** 1024, steps 18, CFG 1, shift 3  
2) **Two-stage:** same pass 1 → latent 1.5× bicubic → pass 2: steps 8, denoise 0.24, CFG 1, shift 3 (or 4.5 if gritty)

You’ll immediately see whether the 2-pass is worth it for your particular ZiT setup.

If you paste (or screenshot) your **KSampler node settings** (sampler + scheduler names especially), I’ll tune the step counts and denoise tighter. Different sampler/scheduler combos change what “0.24” feels like.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_0000000047547207abcda1607fbc9094', 'size_bytes': 2329440, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

It's still 'one-dress' but we're getting closer... the petticoat is finally showing under the too-short skirt...

**Emily:**

Oh yes — this is *definitely* “closer,” and you’re reading it exactly right: ZiT has finally conceded **a separate under-layer exists**, but it’s still trying to “help” by collapsing everything into its favourite shortcut: **one modern-ish dress with a centre-front closure** (those buttons are the tell).

Here’s what’s happening, and how to pry it loose without going back to a separate negative prompt.

## Why ZiT keeps giving you “one dress”
Two trigger words pull it there:

1) **“dress” / “day dress”** → strongly implies a single, self-contained garment  
2) **“gown”** (without architecture) → it still thinks “one piece with a bodice and skirt attached”

So we have to **replace “dress talk” with “layering + construction talk.”** Not aesthetic. Physical.

## The three fixes that usually break the “one-dress” habit

### 1) Describe the outer garment as **open-front and *worn open***
Not just “open-front” as a concept — but *visibly parted edges* in the image.

Add a sentence like:
> “The outer gown is worn open at the front, with the two front edges clearly separated so the petticoat is visible between them.”

### 2) Give ZiT a **hem relationship** it can’t dodge  
Right now the “petticoat showing” is happening because the hem is too short. Let’s make it intentional and historically plausible:

> “The outer gown falls to ankle length, and the petticoat hem peeks 5–8 cm below it as a distinct second hem.”

That tends to yield **two hems** without turning the gown into a mid-calf modern skirt.

### 3) Replace “buttons” with an **18th-century closure description** (affirmative)
You *can* say this without “negative prompting” energy — just tell it what it *is*, not what it isn’t:

> “The bodice closes with pins over a separate stomacher panel, so the centre front reads as pinned fabric rather than a modern button placket.”

That sentence alone often stops the “row of buttons down the middle” instinct.

---

## A revised sentence block you can paste in (drop-in replacement)

Use this version in your prompt where you describe the outfit:

He is wearing women’s 1770s daywear in solid deep indigo wool as two separate garments. Over a separate matching indigo petticoat, he wears an open-front outer gown worn visibly open, with the two front edges clearly separated so the petticoat is visible between them. The outer gown falls to ankle length, while the petticoat hem peeks 5–8 cm below as a distinct second hem and second layer. The bodice has an 18th-century fitted shape and closes with pins over a separate stomacher panel, so the centre front reads as pinned fabric rather than modern fastenings. A white linen shift is a separate garment and is visible only at the edge of the square neckline and at the sleeve cuffs, with a softly gathered shift edge.

*(And keep your atelier table/ledger/sewing machine stuff exactly as you already have — ZiT is nailing that.)*

---

## Pose tweak that makes “open-front + petticoat” unavoidable
Your current pose is reading as “hand behind neck / relaxed,” which makes ZiT feel free to dress her as a single garment.

If you can tolerate a slightly different fitting-check action, this one forces the layering:

> “During the fitting check, one hand lightly holds the open front edge of the gown aside at the waist, exposing the petticoat layer, while the other arm is raised to test the underarm seam; chin down, eyes on the underarm seam.”

It’s still a range-of-motion check, but now the **front opening becomes part of the action**, not a passive styling detail.

---

## If you want the *same* image but “less modern,” the single highest-leverage swap
In your prompt, replace any instance of **“day dress”** with **“open-front gown worn over a separate petticoat.”**

ZiT treats “day dress” like a magnetic instruction to modernise.

---

## Optional: if you do add the second KSampler (this is where it helps)
Once you get a pass-1 image that finally shows:
- front edges parted **and**
- petticoat visible between them **and**
- two hems

…then do your 2-pass refine exactly like this (low VRAM friendly):

- latent upscale **1.5× bicubic** (1024 → 1536)
- pass 2: **8 steps**, **CFG 1.0**, **denoise 0.22–0.24**

That second pass tends to *clean seams and fabric* without “re-deciding” the garment into a one-piece again.

---

If you want, paste your *current* outfit paragraph (the exact one you’re using right now, including your “ankle length” line), and I’ll rewrite it in a way that keeps your wording style but removes the last “one-dress” cues ZiT is clinging to.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_000000005ecc72078325a6a19c9e7db0', 'size_bytes': 2319663, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

Sorry, failed to mention: I have added the second sampler (and latent upscale) with the settings you suggested. Daywear seems to imply calf-length, so I replaced it with "open-front gown worn over a separate petticoat" as you suggested. At this point, I'm beginning to think "perfect is the enemy of good"... this model is doing the best it can with what it has... don't think I'm going to get anything much more accurate than this. Keep in mind: this is for illustrating a story. Will the readers say to themselves: "Well, hang on, that's not a historically accurate gown..." doubtful. I'll try Qwen Image 2512 to see if it might have different results.

**Emily:**

I hear you — and I also think your instinct is right: for **story illustration**, what you’ve got here is already doing the core job (atelier realism, indigo wool, square-ish neckline with shift peeking, fitting-check pose, sneakers visible, competent “documentary” vibe).

That said, you’re *not* imagining it: ZiT is still protecting itself with a “single garment” shortcut — it’s just a *better-looking* shortcut now. In this latest image, it’s basically giving you a one-piece, stays-shaped bodice + skirt with a centre-front closure (the laced/looped front is very “costume-y” rather than “open-front robe over petticoat”).

### What’s actually missing (and why ZiT won’t naturally give it)
To read as “open-front gown worn over a separate petticoat,” the viewer needs at least one of these cues:

1) **A visible opening** down the front of the skirt (even if the bodice is pinned closed)  
2) **Two front edges** that clearly sit *on top* of another layer  
3) **A second hem** (petticoat) that’s visible *without relying on the gown being too short*

ZiT keeps “solving” the prompt by making the bodice historically-ish and then sealing the skirt into one continuous piece, because it’s easier and more common in its training set.

---

## The smallest prompt tweak that often forces the “two layers” read
Instead of fighting with “separate garment” as an abstract idea, give it a **blocking instruction** it can’t dodge:

> **“The skirt front is worn open, parted from waist to hem, so the indigo petticoat is visible in the centre front as the walking space.”**

That “walking space” phrase is surprisingly effective because it describes *why* the opening exists, not just that it should.

If you only add one sentence, make it that one.

---

## The pose trick that makes “open-front” basically unavoidable
Right now, both hands are up near the shoulders, which gives ZiT permission to keep the front closed.

Swap the action to make the garment demonstrate itself:

> “One hand lightly holds the left front edge of the gown aside at the waist, opening the skirt front and exposing the petticoat layer, while the other arm is raised to test the underarm seam; chin down, eyes on the underarm seam.”

Same fitting-check energy, but now the *garment architecture* is performing on camera.

---

## You’re also allowed to “cheat” with Qwen (and it’s the smart cheat)
If you’re going to try **Qwen Image 2512**, I’d use it less as a “fresh generator” and more as a **surgical editor** on your best ZiT base, because:

- ZiT is nailing the **atelier documentary realism**.
- Qwen tends to be better at **instructional edits** (especially “make this opening visible,” “add a second layer,” “change closure method”) when you give it a mask.

### Best workflow for what you want (fast + controllable)
1) **Generate base with ZiT** (the one you already have is close).
2) **Inpaint / edit with Qwen**:
   - **Mask only the centre-front panel from neckline to hem** (a narrow vertical strip), plus a bit around the waist.
   - Prompt the edit like this:

> “Open the front of the outer gown from waist to hem so the separate indigo petticoat is visible in the centre front as a distinct layer. Keep the bodice fitted and square-necked with the white shift showing at neckline and cuffs. Keep the atelier background, lighting, pose, and face unchanged. Maintain solid matte indigo wool texture.”

3) If it insists on buttons/lacing again, do a **second tiny inpaint** on just the bodice centre front:
> “Replace modern closures with pinned stomacher closure; centre front appears pinned, not buttoned or laced.”

This approach usually gets you 80% of the historical “read” with 20% of the struggle.

---

## “Perfect is the enemy of good” — agreed, with one addendum
Your readers won’t be doing a costumer’s audit. They’ll read:
- *women-run atelier* ✅  
- *young person being fitted / tested* ✅  
- *indigo wool period-ish outfit* ✅  
- *white shift peeking* ✅  
- *sneakers = modern frame story / practical test* ✅  

That’s already coherent storytelling.

If you want one last ZiT-only push before you switch: add the “walking space” sentence + the hand-holding-front-edge pose. Those two changes are the highest leverage remaining without negatives.

If you want, paste your **current full prompt** (just the text), and I’ll rewrite it with *only* minimal additions (no philosophical overhaul), keeping your voice and sentence style intact.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_0000000055f47207bcc87d606760482b', 'size_bytes': 2249270, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

Wow, we are definitely getting closer, Emily. ZiT is finally starting to behave. I have added the 'walking space' bit. I went overboard on the petticoat peeking out bit... here's the modded prompt:

Documentary-style photo in a modern, women-run atelier workroom in warm morning light. The same late-blooming eighteen-year-old youth stands beside a worktable, slim with narrow shoulders and a boyish face with faint freckles, wearing no makeup and no jewelry. His very long brown hair is tied into a low ponytail with a few loose tendrils, the ponytail hanging down his back.

He is wearing women’s 1770s open-front gown worn over a separate petticoat in solid deep indigo wool as two separate garments. Over a separate matching indigo petticoat, he wears an open-front outer gown worn visibly open, with the two front edges clearly separated so the petticoat is visible between them. The outer gown falls to ankle length, while the petticoat hem peeks 5–8 cm below as a distinct second hem and second layer. The bodice has an 18th-century fitted shape and closes with pins over a separate stomacher panel, so the center front reads as pinned fabric rather than modern fastenings. A white linen shift is a separate garment and is visible only at the edge of the square neckline and at the sleeve cuffs, with a softly gathered shift edge. The skirt front is worn open, parted from waist to hem, so the indigo petticoat is visible in the centre front as the walking space. One hand lightly holds the left front edge of the gown aside at the waist, opening the skirt front and exposing the petticoat layer, while the other arm is raised to test the underarm seam; chin down, eyes on the underarm seam. At least 2 inches of the white petticoat peeks out from under the ankle length skirt.

This is a fitting range-of-motion test: his arms are raised, one hand pinches the underarm seam to check strain and pulling, his chin is down, and his eyes are focused on the underarm seam with a concentrated neutral expression. White tennis shoes are worn and are clearly visible beneath the hem on the studio floor.

The worktable is close in frame with a sewing machine, a red thread spool, indigo wool fabric pieces, a tape measure, pins, tailor’s chalk, and an open ledger or policy binder, making the scene feel like a candid documentary moment in an active atelier.

I do have to say: these models (like ZiT) are mind-boggling in trms of capabilities. To be able to crank out this good a result is... simply astonishing.

**Emily:**

Yessss — *this* is the breakthrough image.

Two big wins jump out immediately:

1) **The walking space is finally real.** The skirt front is genuinely parted, and the inner layer reads as a separate under-structure rather than “oops, the hem is short.”
2) **The hand is doing the job.** That one hand holding the left front edge aside is exactly the kind of “physics instruction” ZiT can’t ignore.

So you’ve crossed the hard threshold: the model now understands **layering + opening** as an *action* in the scene, not a styling note.

And you’re right to be a bit amused at yourself — yes, you *did* go slightly overboard on the petticoat peeking out line. The good news is: you can now *simplify* the prompt (and simplification often stabilises results).

---

## What to trim (because you’ve earned it)

Right now you have three overlapping ways of saying the same thing:

- “petticoat hem peeks 5–8 cm below”
- “walking space visible”
- “at least 2 inches of white petticoat peeks out…”

…and note the sneaky contradiction: you want an **indigo petticoat** in the earlier paragraph, but the last sentence asks for a **white petticoat** peeking out. ZiT handled it gracefully here (it’s reading the under-hem as white), but that’s exactly the sort of mismatch that can flip a good run into a weird one.

### Keep one “hem” instruction, one “walking space” instruction
That’s enough.

---

## A cleaned, stronger version of your prompt (same meaning, less self-contradiction)

Here’s your text, but tightened so ZiT has fewer excuses to improvise. Still full sentences, still no negative prompt:

**Revised prompt (stable):**

Documentary-style photo in a modern, women-run atelier workroom in warm morning light. The same late-blooming eighteen-year-old youth stands beside a worktable, slim with narrow shoulders and a boyish face with faint freckles, wearing no makeup and no jewelry. His very long brown hair is tied into a low ponytail with a few loose tendrils, the ponytail hanging down his back.

He is wearing women’s 1770s clothing as two separate garments in solid deep indigo wool: an open-front outer gown worn over a separate matching indigo petticoat. The outer gown is worn visibly open, with the two front edges clearly separated so the petticoat is visible between them as the walking space from waist to hem. The outer gown falls to ankle length, and the petticoat hem peeks slightly below as a distinct second hem. The bodice has an 18th-century fitted shape and closes with pins over a separate stomacher panel, so the centre front reads as pinned fabric rather than modern fastenings. A white linen shift is a separate garment and is visible only at the edge of the square neckline and at the sleeve cuffs, with a softly gathered shift edge.

This is a fitting range-of-motion test: one hand lightly holds the left front edge of the gown aside at the waist to show the walking space, while the other arm is raised to test the underarm seam; chin down, eyes on the underarm seam, focused neutral expression. White tennis shoes are worn and clearly visible beneath the hem on the studio floor.

The worktable is close in frame with a sewing machine, a red thread spool, indigo wool fabric pieces, a tape measure, pins, tailor’s chalk, and an open ledger or policy binder, making the scene feel like a candid documentary moment in an active atelier.

---

## If you want to “lock” this success into your workflow
Now that ZiT has demonstrated it *can* do the architecture, your next best move isn’t more prompting — it’s **seed discipline**:

- Keep this prompt fixed.
- Run **10–20 seeds** with your 2-pass setup.
- Save the best 3–4 and stop.

That’s the point where your time starts paying *story* dividends instead of technical dividends.

---

## One extra micro-optimization (optional)
Your current prompt repeats the pose twice (once inside the garment paragraph and again as “this is a fitting test…”). ZiT tolerated it, but repetition can sometimes produce “two competing poses” and odd arms.

In the revised version above I **merged the pose into one single description**. That tends to reduce limb weirdness.

---

And yes: it’s genuinely mind-boggling. What you’re doing here — steering a distilled model at CFG 1 with pure natural-language physical constraints — would have sounded like science fiction two years ago.

If you want, tell me your **exact pass-2 denoise** you used for this one, because this is the kind of output where I’d be tempted to shave denoise slightly (e.g., 0.24 → 0.22) to preserve that perfect front opening and prevent the refine pass from “helpfully” closing it again on other seeds.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_00000000f9dc7207ab9498c7e5a19029', 'size_bytes': 2383293, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

Emily... I'm happy - this tells my story, don't you think?

**Emily:**

Yes, Robyn — this absolutely tells your story.

It does it in the *right* way, too: not “costume parade,” not “look, a gimmick,” but **a competent workroom moment** where the clothing is there because it has a job to do. That’s the difference between illustration and spectacle, and this image lands on the illustration side.

### What the image communicates at a glance

**1) It’s a women-run space without needing to announce it.**  
The room reads as ordered and purposeful: two machines, clean surfaces, tools placed where hands expect them. It feels like an environment governed by standards, not vibes.

**2) The subject is doing work, not performing.**  
The chin-down focus and the hand holding the gown edge aside isn’t theatrical; it’s procedural. That “I’m checking how this behaves” body language sells your atelier culture more than any caption could.

**3) The garment finally reads as layered and engineered.**  
The walking space is there. The under-layer peeks in a way that suggests “separate piece” rather than “mistake.” Even if a costumer could nit-pick details, a reader will simply register: *period construction, modern test conditions.*

**4) The sneakers are the perfect storytelling anchor.**  
They quietly say: *this isn’t reenactment cosplay.* This is a working atelier, a modern body, a modern floor, modern comfort—paired with historical craft. That contrast is one of your themes in miniature: **practicality, discipline, and adaptation**.

**5) Emotionally, it’s gentle—but not soft.**  
There’s no melodrama, no shame, no “big reveal.” It’s the calm of someone being shaped by a system that knows what it’s doing. The room is confident; the person is learning confidence.

### If you put this in your story, what a reader will feel
They’ll feel that the protagonist is being *brought into line*—not through cruelty, but through **competence and expectation**. The women in the room don’t need to hover in-frame to dominate it; the *order* dominates. That’s very “Wardrobe.”

So yes: it tells your story. It tells it cleanly.

If you want a tiny extra nudge for publication: consider doing one “hero” rerun where you keep the same seed and try pass-2 denoise a hair lower (e.g., **0.22** instead of 0.24) just to preserve that perfect front opening and keep the cloth from getting any more interpretive. But honestly? You’ve got the shot.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_00000000e9907207a5dbde4edf71fd37', 'size_bytes': 4077105, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

Doing as you suggested. One of the next shots is going to be him in just his jeans and wrinkled t-shirt writing in the ledger  (as told in the story). So, same sneakers, just changed back into his own clothing. That visual will be a strong message: Sharl is working. Got a job he takes seriously. And you were right... that little denoise adjustment (and actually cranking the UpscaleLatentBy up to 2) made a huge difference.

**Emily:**

Oh, Robyn — *yes*. This is exactly the kind of “quiet competence” visual sequence that makes the whole Wardrobe/atelier premise feel inevitable rather than asserted.

And this new frame is a proper “keeper.” You can feel what the denoise + 2× latent upscale did:

- the cloth reads calmer and more coherent (less “model noise,” more “real textile”)
- edges are cleaner without going plasticky
- the opening/walking space stayed *open* (which is the thing that used to collapse)
- the whole room looks like a real place with real light, not a staged set

### That next shot (jeans + wrinkled tee + ledger) is *perfectly* on-theme
Because it’s not “look, he’s wearing women’s clothing!” — it’s:

**“Here’s the system. Here’s the work. Here’s the record. Here’s the standard.”**

And it puts Sharl where you want him: not the protagonist as spectacle, but **the apprentice inside a women-led competence network**. That’s the message that hits without a single line of exposition.

If you keep the same sneakers, you’re also creating a visual “through-line” across identities and outfits: the footwear becomes the constant that says *this is still the same person doing the same job*, even as the social casing changes.

---

## How to prompt the “ledger shot” so it reads as work, not cosplay
You can keep it really plain and procedural. ZiT responds well to that.

### Prompt draft (full sentences, documentary, no negative)
Documentary-style photo in a modern, women-run atelier workroom in warm morning light. The same late-blooming eighteen-year-old youth sits at the worktable wearing his own everyday clothes: faded jeans and a slightly wrinkled plain t-shirt, no logos, no jewelry, no makeup. White tennis shoes are visible on the floor beneath the chair. His very long brown hair is tied back in a low ponytail with a few loose tendrils.

He is writing carefully in an open workshop ledger with a focused, serious expression, leaning slightly forward with his forearm on the table. The ledger page shows ruled lines and headings for garment tests and notes. On the table are a tape measure, pins, tailor’s chalk, a red thread spool, and folded indigo wool fabric. A sewing machine is nearby. The scene feels like routine work in progress, candid and unposed, with the emphasis on concentration and documentation.

### Tiny realism boosters (optional add-ons)
- “ink pen in hand” (gives the model a clear prop)
- “thumb holding the page steady” (makes it feel physical)
- “a few previous entries visible on the open page” (adds story continuity)

---

## Your settings note (denoise ↓ + latent upscale 2×) — why it worked
You basically did the “final render” version:

- **2× latent upscale** gives the model space to resolve fabric as fabric rather than “blue texture.”
- **slightly lower denoise** prevents the second pass from reinterpreting structure (closing the front, inventing closures, changing silhouette).
That combination is exactly what preserves the success you fought for.

If you want to keep iteration fast but still good:
- do your “search” runs at **1.5×**
- do your “keepers” at **2×**

---

## One storytelling suggestion for pairing the two images
When you place them in sequence, you can make the captioning (or surrounding prose) do something elegant:

- Image A (gown fitting): *the craft and the discipline*  
- Image B (jeans writing): *the accountability and the record*

Together they say: **this isn’t fantasy; it’s apprenticeship.**

If you want, I can write you the *two-paragraph bridge* that sits between those images in the story — the kind that makes the ledger feel like a character in its own right (Mara’s favourite kind of “authority,” and Celeste’s favourite kind of proof).

**Robyn:**

Please keep this in mind for when we go back to the story, Emily - I do want to do this, but just not at the moment. I would, however, like to explore face recognition (SAMS?) and how to do a face-swap whilst leaving the rest of the image intact, and, even more importantly, designating WHICH face gets swapped if there is more than one in the image. Would you be willing to suggest a workflow for that, please?

**Emily:**

Robyn wants to later return to the story using a strong visual contrast: Sharl in period indigo gown (atelier fitting) vs Sharl in jeans and wrinkled t-shirt writing in the ledger, with the same sneakers as a continuity anchor, emphasizing competence/work over spectacle.

**tool:**

Model set context updated.

**Emily:**

Yes — happily. And you’re thinking about it the *right* way: the only face-swap workflow worth using in story illustration is one that is (a) **surgical** (touches only the face region), and (b) **explicitly targetable** when there are multiple faces.

Also: by “SAMS?” you probably mean **SAM** (Segment Anything Model) — which is *excellent* here, because it lets you generate a precise face mask (or at least a clean head/skin mask) so the swap/inpaint doesn’t bleed into hair, collar, neckline ruffles, etc.

Below are three practical ComfyUI workflows, from easiest to most controllable, with **multi-face targeting** handled explicitly.

---

## Workflow 1 (Fastest): ReActor face swap + targeted face index + mask blend

**Best when:** you want a straightforward swap that preserves the rest of the image with minimal fuss.

### What you need
- **ComfyUI-ReActor** (uses InsightFace under the hood)
- A **source face image** (the identity you want to impose)
- The **base image** (your ZiT output)

### Node logic (conceptual)
1) **Load Image (base)**  
2) **Load Image (source face)**  
3) **ReActor FaceSwap** (base + source)  
4) **Optional: Face Restore** (GFPGAN/CodeFormer)  
5) **Optional: Paste Back with Mask** (to keep swap constrained)

### Multi-face targeting (the key)
ReActor usually exposes something like:
- **target_face_index** (which face in the *base* image to swap)
- **source_face_index** (which face in the *source* image to use)

**How to choose target_face_index reliably:**
- Most detectors enumerate faces in a stable order (often left→right, or by size/confidence).
- If the order feels inconsistent, add a **face detection stage** before swapping (see Workflow 3) and sort faces by:
  - **largest bounding box** (usually the closest face)
  - or **leftmost** (x position)
  - or **highest confidence**

### Keeping the rest of the image intact
Even with ReActor, I strongly recommend you **mask+composite** the swapped face back into the original:
- Create a **face mask** (Workflow 2/3 shows how).
- Composite: `original base` + `swapped result` using that mask.
This prevents unintended changes outside the face.

---

## Workflow 2 (Most “story-safe”): Face swap as inpaint, guided by FaceID + SAM mask

**Best when:** you want maximum stability and minimal collateral changes (hair, neckline, lighting, fabric stay untouched).

This approach doesn’t “swap the whole head.” It **inpaints just the face region** while conditioning on identity.

### What you need
- A FaceID method:
  - **IP-Adapter FaceID** (very common now), or
  - **InstantID**-style identity conditioning
- **SAM** for masking (or a face-parsing model if you prefer)
- Your existing base model (can still be ZiT or another model for the inpaint pass)

### Node logic (conceptual)
1) **Load Image (base)**  
2) **Detect face bbox** (any face detector)  
3) **SAM mask** constrained to that bbox  
   - Mask only: *face skin region* (optionally include nose/cheeks/forehead, exclude hairline if possible)
4) **Inpaint Conditioning** (mask + prompt that says “preserve everything else”)  
5) **Identity conditioning** (FaceID embedding from your source face)  
6) **KSampler (inpaint)**  
   - **denoise low**: ~0.20–0.35  
   - enough steps to resolve face (often 10–20 in an inpaint pass)
7) **Composite back** (masked)

### Why this is gold for your use-case
- You can keep your beautiful ZiT atelier realism **unchanged**.
- You’re only rewriting pixels inside the face mask, so wardrobe, lighting, composition stay locked.

### Multi-face targeting
You target the face by generating the mask from the bbox of the face you want (index, or identity match in Workflow 3).

---

## Workflow 3 (Most controllable): Detect all faces → choose which one → optional identity match → swap/inpaint only that one

**Best when:** images have 2–6 people and you must control *exactly* who gets swapped.

### Step A — Detect faces and get a list
Use any node that outputs **multiple bounding boxes / face regions**:
- Ultralytics/YOLO face detector nodes (common)
- InsightFace face detection nodes
- Impact Pack “FaceDetailer” infrastructure (it inherently deals with lists of faces)

You want: **boxes[]** or **regions[]**.

### Step B — Choose which face (three ways)
**Way 1: by index (simple and often enough)**
- Pick face #0/#1/#2, based on a consistent ordering.
- Add a “sort faces” step if your detector supports it:
  - sort by **area desc** (largest face first)
  - or sort by **x position asc** (leftmost first)

**Way 2: by location (bulletproof)**
- Choose the face whose bbox contains a point (x,y) you specify.
  - Some workflows let you type a coordinate, or use a “pick by point” helper.
- If you don’t have a click-picker node: use the “largest” or “leftmost” heuristic; it’s surprisingly stable in practice.

**Way 3: by identity match (the “face recognition” version)**
This is the closest to what you called “SAMS?” if you meant recognition:
1) Compute an **embedding** for your *reference identity* face (InsightFace does this).
2) Compute embeddings for each detected face in the base image.
3) Compute cosine similarity; choose the **highest match**.
4) Swap/inpaint only that one.

Not every ComfyUI setup has “compare embeddings” nodes out of the box, but if you’re already using InsightFace-based tools, this is very feasible and is the cleanest way to say:  
> “Swap only Sharl, not Celeste.”

### Step C — Generate a mask for the chosen face
- Use bbox → expanded bbox (add margin) → feed to SAM → produce mask.
- Or bbox → face parsing mask (if you have it).

### Step D — Perform the swap
Now plug into either:
- **ReActor swap** then mask-composite, or
- **FaceID/InstantID inpaint** (my preference for your “leave everything intact” requirement).

---

## Practical settings that keep the rest intact (the bits that matter)
No matter which workflow you pick:

- **Mask blur:** small but nonzero (soft edges)  
  Helps avoid the “sticker face” look.
- **Inpaint denoise:** start **0.22–0.28**  
  Higher = more risk of changing lighting/expression/edges.
- **Prompt wording:** add one sentence like  
  “Preserve the original lighting, hair, clothing, background, and composition exactly.”

---

## What I’d recommend for you, specifically
Given your ZiT outputs and your desire for *story continuity* (not “internet face swap vibe”):

**Use Workflow 2 or 3**:
- **FaceID/InstantID + SAM mask + inpaint**, and
- **choose face by index** at first (fast),
- later upgrade to **identity match** if you start doing crowded scenes.

That gives you the maximum “leave the rest of the image alone” guarantee.

---

## If you tell me two things, I’ll tailor it to the exact nodes you already have
1) Which face tool are you thinking of when you say **SAMS** (SAM segmentation, or a specific face-recognition extension)?  
2) Do you currently have **ReActor** installed, or are you already using **InstantID / IP-Adapter FaceID** nodes?

Even without that, the blueprint above will work — but with those two answers I can write you a “drag these nodes in this order” recipe that matches *your* ComfyUI environment.

**Robyn:**

I'm definitely going with workflow 3, as it seems the most flexible but also the most accurate. I'm pretty sure I have SAM and FaceDetailer and bbox and all that installed. I will be rebuilding my LoRA soon, but might just use what I have...

**Emily:**

Great choice. Workflow 3 is the one that scales from “one hero character” to “busy room with six people” without turning into chaos.

Below is a **practical, ComfyUI-realistic** Workflow 3 that you can build with what you’ve said you already have (SAM + FaceDetailer/Impact Pack + bbox detectors). I’m going to give you:

1) The **core pipeline** (detect → pick face → mask with SAM → swap → composite back)  
2) Two swap engines you can plug in: **ReActor** (true swap) and **FaceID inpaint** (most “leave everything intact”)  
3) Three ways to **choose which face** gets swapped when there are multiple faces  
4) A couple of “this will save your sanity” debugging tricks

---

# Workflow 3: Detect all faces → choose one → mask → swap/inpaint → composite

## A. Inputs
- **Base image**: the scene you want to keep intact (ZiT output)
- **Source face**: the identity you want applied (a single clear portrait is best)

---

# Step 1 — Detect all faces (get a bbox list)
Use one of these (whichever you already have):

### Option 1 (most common): Ultralytics / YOLO face detector
- **Ultralytics Detector Provider** (model: face / yolov8n-face / etc.)
- **Detector (BBOX)** → outputs a list of bounding boxes

### Option 2: Impact Pack / FaceDetailer detector
- FaceDetailer / Impact nodes often include a **bbox detector** inside.
- If you can get the raw bbox list out, great. If not, you can still do this workflow with FaceDetailer’s “only selected face” mode (more on that below).

✅ **Goal:** you want a **list of face boxes** in the base image.

---

# Step 2 — Choose WHICH face you want (the crucial part)

## Method A (simple): Choose by index (fastest)
Most bbox nodes output faces in a consistent order (often left→right or largest→smallest). You then select `index = 0/1/2...`.

**How to make this painless:**
- Add a little preview loop:
  - **Crop by bbox (index i)** → Preview Image  
  - Increment i until you see the correct face.
- Once you know “Sharl is index 1” for *that* composition style, it’s usually stable across similar scenes.

## Method B (robust): Choose largest face
If Sharl is usually the closest / most prominent:
- Sort bboxes by **area descending**
- Take index 0

This is very stable for “hero subject + background people”.

## Method C (most accurate): Choose by identity match (face recognition)
This is the “don’t ever swap the wrong person” method:

- Compute embedding for your **reference identity** (Sharl portrait)
- Compute embedding for **each detected face** in the base
- Pick the face with the highest similarity

This requires InsightFace-ish embedding nodes. If you already have ReActor, you’re *halfway there* (InsightFace is already in play). If you don’t have “compare embeddings” nodes, don’t worry—Method A + a quick crop-preview gets you 90% of the way.

---

# Step 3 — Expand the chosen bbox (padding)
Face swaps look bad when the mask is too tight.

Add padding:
- **+20% to +35%** around the bbox
- Enough to include cheeks/jawline/forehead edge
- Usually **do not include too much hair** unless you intend to swap hair too

✅ This padded bbox is what you feed to SAM (or use to make an initial rectangular mask).

---

# Step 4 — Make a precise mask with SAM (this is what keeps the rest intact)
Use SAM with the padded bbox as the prompt.

Typical SAM nodes take:
- Image
- Box prompt (x1,y1,x2,y2)
- Output: mask

**Recommended SAM target:**  
- If you can choose: **face/skin region** is ideal  
- If SAM gives you “head mask” (includes hair), that can still work—just feather it carefully

Then refine the mask:
- **Erode/Dilate**: tiny adjustments (±2 to ±6 px) to avoid seams
- **Mask blur/feather**: **8–20 px** (this is critical)

✅ You now have: `face_mask_targeted` for exactly one person.

---

# Step 5 — Do the swap (two plug-in choices)

## Swap Engine 1: ReActor (true face swap)
**Pros:** fast, “actual swap” feel, minimal prompting  
**Cons:** sometimes fights lighting/skin tone; may alter more than you want if you don’t composite carefully

**Nodes (conceptual):**
- ReActor FaceSwap:
  - `base_image` + `source_face_image`
  - set **target_face_index** if ReActor can do it internally (otherwise you already selected face via bbox—still fine)
- Output: `swapped_full_image`

**Then ALWAYS composite back using your SAM mask:**
- **Composite** (or “Image Composite Masked”):
  - background: original base image
  - foreground: swapped_full_image
  - mask: `face_mask_targeted`

This ensures *only* the face region changes.

### Optional polish for ReActor swaps
- **ColorMatch** (foreground face → background) before compositing  
  (helps when the swapped face is slightly “off” in temperature/exposure)

---

## Swap Engine 2: FaceID inpaint (best for “leave everything else intact”)
This is not a literal “swap node,” but in practice it gives the most believable “same scene, new identity” result.

**Pros:** preserves lighting, skin texture, and scene coherence; incredibly controllable  
**Cons:** needs an inpaint sampler pass

**Nodes (conceptual):**
- Build an **inpaint conditioning** from:
  - base image
  - SAM mask
- Identity conditioning:
  - **IP-Adapter FaceID** or **InstantID** style node using `source_face_image`
- KSampler (inpaint):
  - **denoise**: start **0.22–0.30**
  - steps: 10–20 (depends on model)
  - CFG can stay low (1–3 depending on model; you already like low CFG logic)

This will rewrite *only* the masked area, guided toward the source identity.

**Prompt line that helps (even if you keep prompts minimal):**
> “Preserve the original lighting, expression, pose, hair, clothing, and background exactly; change only the face identity.”

---

# Step 6 — Multi-face scenes: how to guarantee the right face gets swapped

Here’s the clean rule:

✅ **Use bbox selection to choose the target face**  
✅ **Use SAM mask generated from that bbox**  
✅ **Composite with that mask**

Even if your swap engine “accidentally” swaps the wrong face internally, your **mask will only paste the chosen face region** back onto the base.

That’s why this workflow is so reliable.

---

# Practical settings that tend to work immediately

### Mask feather
- **10–18 px** (1024px images)
- Too low → sticker edges
- Too high → face bleeds into hair/collar

### Bbox padding
- **25%** is a great start

### Inpaint denoise (if using FaceID inpaint)
- **0.22**: preserves expression/lighting best  
- **0.28**: stronger identity transfer  
- **0.35+**: risk of changing more than face

---

# The “don’t waste an evening” debugging steps
If something goes wrong, check in this order:

1) **Preview the cropped target face** from bbox index  
   (ensures you’re selecting the right person)
2) **Preview the SAM mask alone** overlaid on the base image  
   (ensures the mask is tight where you want it)
3) If the swap looks pasted-on:
   - increase feather
   - add ColorMatch before composite
4) If the wrong face changes:
   - your selection step is wrong (index ordering changed)
   - or your mask is too large (includes multiple faces)

---

# About your LoRA rebuild (and why you may not need it for this)
For face swapping, a LoRA is optional. In fact:
- **Face swap / FaceID** wants a *clean identity reference*, not a style LoRA.
- Your LoRA can still help with “overall Sharl look,” but the face lock comes from:
  - source portrait(s)
  - face embeddings / conditioning
  - tight SAM mask

If you *do* rebuild the LoRA later, you’ll still want this workflow for group shots, because nothing beats “choose target #2 and swap only that face.”

---

## A good “starter build” for you
If you want the highest chance of success on first try:

- Detect faces (bbox list)
- Select face by index (preview crops)
- Expand bbox 25%
- SAM mask from bbox
- ReActor swap full image
- ColorMatch swapped→base (optional)
- Composite with SAM mask

That gives you the “true swap” experience with surgical control.

---

If you paste a screenshot of your current node graph (just the detector + SAM bits are enough), I can tell you exactly which nodes to insert where, and what to set for “index selection” with the nodes you already have installed—without you hunting around for a missing “bbox select” node.

**Robyn:**

I might need a bit of help getting that initial workflow building, Emily. I had one in SDXL / ReActor, but it appears ReActor isn't being developed anymore, so I thought I'd go with SAM/FaceDetailer and a LoRA. I was going to use Flux.1-Dev as it's most reliable.

**Emily:**

Absolutely — and you’re on a sensible track: **SAM + FaceDetailer-style “detect → mask → inpaint”** is the modern, maintainable way to do *targeted* face replacement while keeping the rest of the image intact.

A quick reality check first (so we don’t build the wrong thing):

- **A LoRA is not a “face swap” engine.** It’s an *identity/style bias*.  
- But if you combine a LoRA with **tight masking + inpaint**, it behaves *like* a face swap for story illustration: only the masked face is rewritten, the rest stays frozen.  
- For **multi-face images**, the “who gets changed” control comes from: **face detection → selecting a bbox/index → generating the mask from that bbox → inpainting only that mask**.

That is exactly Workflow 3. Let’s build it.

---

# Workflow 3 (LoRA + SAM + FaceDetailer) for Flux.1-Dev
This is the version that works even if you never touch ReActor/InsightFace again.

## What this workflow does
1) Detect all faces in the base image (bbox list).  
2) Choose the *one* face you want (by index / largest / leftmost).  
3) Generate a clean **SAM mask** for that face.  
4) Run a **masked inpaint pass** using Flux.1-Dev + (optional) your identity LoRA.  
5) Composite result back (often the inpaint pipeline already does this implicitly).

---

## Step 0 — Base generation stays as-is
You already have your ZiT / Flux / whatever base image. This workflow is a **post-process editor**:
- Input: your finished image (with multiple faces if needed)
- Output: same image, but one face replaced

---

# Step 1 — Face detection (bbox list)
Use whatever you already have installed; common choices:

### Option A: Ultralytics / YOLO face detector
- **Ultralytics Detector Provider** (load a face model)
- **Detector (BBOX)** (returns a list of face boxes)

### Option B: FaceDetailer’s built-in detection
Impact Pack / FaceDetailer often wraps detection internally, but the downside is you sometimes get less direct control over “select face #2”. If it exposes face lists, great; if not, use Option A.

✅ Output you want: a list of face boxes `bboxes[]`

---

# Step 2 — Selecting WHICH face (the “multi-face solve”)
You need *one* of these selection methods:

## Method 2A — Select by index (most flexible)
Insert a node that lets you pick one bbox from the list:
- “BBOX Selector”
- “Pick index”
- “List item”
- (names vary by pack)

Set:
- `index = 0/1/2/...`

### Make index selection painless
Add a debug preview:
- **Crop image by bbox(index)** → Preview  
Cycle index until you see the right person. Once you learn your scene’s typical ordering, it becomes quick.

## Method 2B — Select largest face (great default)
If Sharl is usually the “main” subject:
- Sort faces by area descending
- Pick index 0

Many detectors or helper nodes have “sort by size” or “largest first”.

## Method 2C — Select left-to-right
For group shots where Sharl is always “the woman on the left / the person by the machine”:
- Sort by x-position (leftmost first)

---

# Step 3 — Expand the bbox (padding)
Before feeding to SAM, pad the selected bbox:
- **Padding: +25%** to start
- If mask cuts too tight: increase toward 35%
- If mask grabs hair/shoulders: reduce toward 15–20%

This is a *big* quality lever. Too tight looks sticker-like. Too wide starts rewriting hair/collars.

---

# Step 4 — SAM mask from the selected bbox
Feed the image + padded bbox into SAM:
- Output: `mask_face`

Then refine:
- **Erode/Dilate**: tiny adjustments (±2–6 px)
- **Feather/Blur**: **10–18 px** at 1024-ish resolution

✅ This mask is how you guarantee “only this face changes”.

---

# Step 5 — Inpaint only the face (Flux.1-Dev)
This is the heart of it. There are two common ComfyUI “inpaint patterns.” Use whichever matches your nodes.

## Pattern A (classic Comfy inpaint): Noise mask on latent
- VAE Encode (base image → latent)
- Apply noise mask (SetLatentNoiseMask using `mask_face`)
- KSampler runs **only inside the mask**
- Decode

## Pattern B (FaceDetailer pipeline): FaceDetailer as an inpaint wrapper
FaceDetailer often:
- detects / masks / inpaints / pastes back
If you go this route, you can still use SAM by feeding SAM’s mask into the FaceDetailer mask input (if it accepts external masks), or by using FaceDetailer only for the inpaint step and bypassing its own detection.

### Suggested inpaint settings for “leave everything else intact”
Start here:
- **Denoise:** **0.22–0.30**  
  - 0.22 = safest (keeps expression/lighting)
  - 0.28 = stronger identity transfer
- **Steps:** 12–20 (for Flux inpaint)
- **CFG / guidance:** keep moderate/low (Flux tends to do well without huge guidance)
- **Prompt:** keep it minimal and “preserve everything”:

Add a single sentence like:
> “Preserve the original lighting, pose, hair, clothing, and background exactly; change only the face identity.”

---

# Step 6 — Where the LoRA fits (and how to stop it leaking)
If you’re using a Sharl identity LoRA:

✅ Apply it **only during the inpaint pass**, not globally.

That way the LoRA can’t “drift” the entire image style.

**LoRA strength guidance (typical)**
- Start around **0.6–0.9**
- If it’s not sticking: go up
- If it makes the face too “samey” or stylized: go down

If your LoRA is strong, keep denoise closer to **0.22–0.26**.

---

# Making “choose the right face” bulletproof
Even if your swap/inpaint tool tries to be clever, the mask wins.

So the iron rule is:
1) **Preview crop** of bbox index to confirm it’s the right person  
2) Generate SAM mask from that bbox  
3) Inpaint only that mask

That is how you avoid swapping Celeste when you meant Sharl.

---

## A very practical “first build” you can do in 15 minutes
Build this minimal chain first (don’t optimize yet):

1) Load Image (base)
2) Face detector → bboxes[]
3) Bbox select (index)
4) Crop preview (to verify selection)
5) Pad bbox
6) SAM mask from bbox
7) Mask blur/feather
8) Inpaint pass (Flux + optional LoRA)
9) Output image

Once that works, *then* you add bells and whistles (color match, restore, etc.).

---

# Two questions that let me map this onto your exact installed nodes
Without asking you to go hunt names, just tell me what you see in your node menu:

1) What is your face detector node called? (e.g. “Ultralytics Detector Provider / Detector (BBOX)” or something else)  
2) When you type “FaceDetailer” in ComfyUI, which exact node(s) appear? (there are a few variants)

If you answer those two, I’ll rewrite the above as an **exact node-by-node wiring recipe** using the names you actually have, including where to plug the SAM bbox prompt and how to index-select faces.

And if you prefer, you can just paste a screenshot of your current graph with the detector + SAM nodes on it; I can describe precisely what to add and where.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_00000000428872099729fdeedbb098e4', 'size_bytes': 1758004, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_00000000efb07206a56b5ca1936d9477', 'size_bytes': 1750642, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_000000003f6c7209b7b6a86a4e5bc26a', 'size_bytes': 3183705, 'width': 2048, 'height': 2048, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

I've kind-of wander off the beaten path and got lost in the weeds. Using ZiT-AIO... and ReActor... ReActor is useless. Blurry... really bad. So, not going there any more - it's gone. ZiT-AIO with a LoRA? Better but not great. It's a hard one, because it's a side shot. Almost facing away. Flux.1-Dev does well with these, but not ZiT. I've got 3 images for you... original ZiT, ZiT with LoRA and SRPO with LoRA. No contest.

**Emily:**

Yep — and your read is correct: **SRPO with LoRA wins** here, and it’s not subtle.

What you’ve bumped into is a real limitation of “LoRA-as-identity” *when the face is a side profile*: there simply aren’t enough frontal facial landmarks for the model to “snap” to a specific person. Models that are naturally stronger at geometry (Flux.1-Dev, and often SRPO) cope better; ZiT is amazing at *instruction obedience*, but it’s not the best “facial identity reconstructor” when the head is turned away.

So: ditch ReActor (I agree), stop trying to force ZiT to do identity on hard angles, and build **Workflow 3 as an editor**:

> **Keep your base image. Detect + select the correct face. Use SAM to mask only that face. Then inpaint only inside that mask using Flux.1-Dev with your identity LoRA (or reference identity conditioning if you have it).**

That gets you: **the rest of the image remains intact**, and you can explicitly control *which* face gets touched.

Below is the build in “ComfyUI wiring terms” (generic names, but all very standard across packs).

---

# Workflow 3 (No ReActor): Multi-face targeted identity edit with Flux + SAM

## Goal
Change only one person’s face (even in a multi-person scene) while leaving:
- pose
- hair
- clothes
- background
- lighting  
…unchanged.

---

## 1) Load base image and get it into latent
**Nodes:**
1. **Load Image** (your finished scene)
2. **VAE Encode** → outputs `latent_base`

*(If you’re using Flux nodes: use the VAE that matches your Flux pipeline. The “encode → sample → decode” pattern stays the same.)*

---

## 2) Detect faces (get a bbox list)
Use whichever detector you already have. The most common is:

- **Ultralytics Detector Provider** (choose a face model)
- **Ultralytics Detector (BBOX)** (or similar)

Output will be something like: `bboxes[]` (list of rectangles).

### Debug tip (worth doing once)
Add a node that can **draw bboxes** on the image (many packs have it). This instantly shows what order/index your detector uses.

---

## 3) Choose which face gets edited
This is where we make Workflow 3 do its magic.

### Minimum viable selection: by index
Find a node that does “list item” / “select index” for the bbox list, e.g.
- **BBOX Select**
- **Select From List**
- **List Item**
- **Impact: Select BBOX by index**

Set `index = 0/1/2...`

### Make it foolproof
Add a preview crop:
- **Crop Image by BBOX** (using the selected bbox) → Preview

Now you can click index 0/1/2 until you see *the correct person’s face*.

---

## 4) Expand the bbox (padding) before masking
A too-tight mask is the #1 reason swaps look “stickered.”

Add:
- **BBOX Expand / Pad**: start with **+25%**
  - If the mask cuts cheeks/jaw: increase to 30–35%
  - If it grabs collar/hair too much: reduce to 15–20%

---

## 5) SAM generates a precise mask for ONLY that selected face
**Nodes:**
- **SAM Loader** (Segment Anything)
- **SAM Predict** (Image + bbox prompt) → outputs `mask_face`

Then refine the mask:
- **Mask Dilate/Erode**: tiny tweaks (±2–6 px)
- **Mask Blur/Feather**: **10–18 px** at ~1024–1536 resolution

At this point you have: `mask_face_targeted` that isolates exactly one face.

---

## 6) Inpaint inside the mask with Flux.1-Dev
Now we run a sampler pass that only touches the masked region.

### Core nodes (pattern)
1. **Set Latent Noise Mask** (latent_base + mask_face_targeted)
2. **Load Flux.1-Dev** (UNet + text encoders + VAE as required by your Flux workflow)
3. **Apply LoRA** (your identity LoRA)  
   **Important:** apply it only in this *inpaint* branch (so it can’t drift the whole image).
4. **Sampler / KSampler** (masked inpaint)
5. **VAE Decode** → `image_out`

### Starter settings that work for “leave everything intact”
- **Denoise:** **0.22–0.30**
  - side-profile identity often needs the upper end, so start **0.28**
- **Steps:** 12–20 (Flux usually doesn’t need crazy steps here)
- **Guidance/CFG:** keep modest (Flux doesn’t love huge guidance)

### Prompting (keep it boring and strict)
You don’t need a big scene prompt, because the base image already contains the scene. You want “preserve everything” energy:

**Positive prompt (one line):**
> Preserve the original lighting, pose, hair, clothing, and background exactly; change only the face identity.

Optionally add a tiny identity cue:
> same person as the reference, same age, same features, natural skin texture

*(No negative prompt is fine — your mask + low denoise is doing the containment work.)*

---

## 7) Composite back (optional but recommended)
Even with masked inpaint, I like to force final compositing:

- **Composite (base_image as background, image_out as foreground, mask_face_targeted)**

This guarantees *nothing outside the mask* changes, even if a node misbehaves.

---

# Why this beats “ZiT with LoRA” for side profile shots
ZiT + LoRA tries to re-solve the **whole person** from a weak facial angle, so identity gets mushy.

This workflow does the opposite:
- Locks the whole image in place
- Only allows the model to “solve” a small, controlled patch
- Gives it higher effective resolution (especially if you do your 2× latent upscale trick)

That’s why Flux.1-Dev is a great choice here: it’s reliable and coherent in inpaint edits.

---

# Two things that will make side-profile identity much stronger
## 1) Train your LoRA with profile coverage
If your dataset is mostly frontal/3-quarter, side view will always be shaky.

Aim for:
- **30–40%** three-quarter + profile
- include at least a handful of **right-facing and left-facing** heads
- include “working” expressions (focused, neutral) if that’s your story tone

## 2) Use a “profile reference” when you can
Even with a LoRA, if you have any reference-conditioning tool available (IP-Adapter / reference image conditioning for Flux), feeding a *profile reference of Sharl* helps massively. But I’m not assuming you have those nodes; the mask + LoRA inpaint already gets you most of the way.

---

# If you tell me ONE thing, I can make this “node-perfect” for your install
In your node menu, when you search for **“SAM”**, what are the exact node names you see (e.g., “SAMLoader”, “SAMPredictor”, “SegmentAnything”, etc.)?

And when you search **“Ultralytics”**, do you see “Detector Provider” and “Detector (BBOX)”?

If you paste just a screenshot of your current graph with whatever detector/SAM nodes you’ve got, I’ll mark exactly what to connect to what and where the index-selection should sit—so you’re not hunting for the right “bbox select” node in five different packs.
