---
title: "De-ridge brow tips"
date: 2025-09-24
---

# De-ridge brow tips

**Robyn:**

Hi Emily. I have a images of a male face that has a rather prominent eyebrow ridge. I'm going to use those face images in a low-ranking adapter (LoRA) for use in my AI-images, but I would like to modify them first. Would you have any tips on how to reduce or better yet remove that ridge?

**Emily:**

Hey Robyn! Yep—there are a few solid paths to “de-ridge” a brow before you train a LoRA. Here’s what works well without wrecking identity or skin texture.

# 1) Classic pixel retouch (Photoshop / GIMP)
**Goal:** soften the supraorbital ridge (above the eye sockets) while keeping pores & hair intact.

- **Liquify (Face-Aware helps)**
  - Convert layer to **Smart Object** (non-destructive).
  - **Filter ▸ Liquify** → use **Forward Warp** with a **large, soft brush**, low pressure (5–15%).
  - Nudge the ridge **inward/upward** a few pixels; also **raise outer brow tail** slightly to create a gentler arc.
  - If available, **Face-Aware Liquify**: tweak **Brow Height** ↑ a touch and **Brow Tilt** for a softer shape.

- **Dodge/Burn to kill the “ridge” shadows**
  - New blank layer set to **Soft Light**; paint with **low-opacity** black/white.
  - **Dodge (midtones)** the shadow just under the ridge; **Burn (highlights)** lightly on the upper forehead to flatten contrast.

- **Frequency Separation (texture safety net)**
  - Run FS (8–12 px blur radius usually fine for forehead).
  - Do contour tweaks on the **low-freq** (color/volume) layer; leave the **high-freq** (pores) layer untouched so skin stays real.

- **Finish**
  - Heal/clone any wiggles on the brow edge.
  - Tiny **High-Pass (Overlay, 0.7–1.2 px)** pass if you lost snap.

> **Batching:** record an **Action** (Liquify + Dodge/Burn steps at light strength) and run **File ▸ Automate ▸ Batch** so the whole set gets the same treatment—consistency matters for LoRA.

# 2) ComfyUI inpaint (keeps identity)
**Goal:** small structural rewrite via diffusion, but locked to the same face.

- **Nodes (one good recipe):**
  - **SDXL (or your base)** + **IP-Adapter FaceID** (or **InstantID**) with a clean reference of the same person.
  - Create a **tight mask** over the ridge & a sliver of forehead (avoid eyebrows/hairline).
  - **Inpaint** with **denoise 0.18–0.30**, **CFG 4–6**, **25–35 steps**.
  - Prompt nudge: *“soft forehead, smooth supraorbital area, subtle brow arc, natural skin texture”*. Put **“prominent brow ridge, heavy brow, bossing”** in **negative**.
  - If needed, run **FaceDetailer** *only on the masked region* (don’t let it rework the whole face).

> **Tip:** Keep the mask narrow. Multiple light passes beat one heavy pass (identity stays truer).

# 3) If you can re-shoot even a few sources
Soft **frontal fill** (big diffuser) plus a slight **top fill** kills the shadow band that makes a ridge look harsher. Even 3–5 cleaner sources mixed into the set can steer training.

# 4) Dataset & training guardrails
- **Be consistent.** Don’t mix heavily edited with totally unedited; apply the same light treatment across all.
- **Curation beats correction.** Prefer angles/lighting that minimize the ridge.
- **Captions:** include a style token like *“soft brow”*; and during **inference** always negative-prompt *“prominent brow ridge”*.
- **Don’t overdo geometry.** Big warps can drift identity; small, repeatable moves are safer.

# 5) Quick QC checklist
- Zoom 100%—pores intact? brow hair edges clean?
- Profile/¾ view still reads as the same person?
- No banding/flatness on the forehead?
- Apply identical tweaks across the batch.

If you want, tell me which route you’ll use (Photoshop/GIMP vs. ComfyUI inpaint), and I’ll jot a precise mini-workflow with settings tailored to your tools.

**Robyn:**

I do like the ComfyUI approach, but I think I'll try using GIMP first. Please provide a workflow for GIMP. I do have the current version (not sure if that makes a difference)...

**Emily:**

Perfect—GIMP can do this cleanly and non-destructively. Here’s a practical, repeatable workflow tuned for softening/removing a prominent brow ridge while preserving pores and identity.

# Quick win (10–15 min per image)
**Goal:** small geometry nudge + contrast flattening, without plastic skin.

1) **Prep**
- Open the image → **Duplicate the background** (Ctrl/Cmd-Shift-D).
- Name it `01–Warp`. Keep the original hidden for A/B checks.

2) **Subtle shape tweak (Warp Transform)**
- **Tools ▸ Transform Tools ▸ Warp Transform** (W).
- Mode: **Move Pixels**; **Deform radius** large (150–300 px), **Strength** low (0.02–0.08).
- With a very soft cursor, **nudge the ridge inward/up a few pixels**. Work symmetrically and *tiny*. Toggle the eye icon to compare with the original often.

3) **Flatten the ridge shadow (Dodge/Burn on a tone layer)**
- New layer: **Layer ▸ New ▸ Fill with: Transparency**. Name `02–Tone`.
- Set its **Mode = Soft light**; **Opacity ~10–20%**.
- Select the **Paintbrush** (B), low flow/opacity (10–15%).
  - Foreground **white** = lighten. Lightly **paint under the ridge** to lift the shadow band.
  - Foreground **black** = darken. Feather a touch **above the ridge** so highlight isn’t popping forward.
- If you prefer tools: **Dodge/Burn Tool** (Shift-D), **Range = Midtones**, **Exposure 5–10%**; but the Soft-light brush is more controllable.

4) **Edge cleanup**
- **Heal Tool** (H), small brush, sample nearby skin to fix any wobbly edges you introduced near the brow.
- Avoid the eyebrow hairs; if you touch them, **Clone Tool** (C) with aligned sample, 30–50% opacity, single strokes along hair direction.

5) **Micro-contrast snap (optional)**
- Merge a **visible copy** (Shift-Ctrl/Cmd-C then **Edit ▸ Paste as ▸ New Layer**) and name it `03–Snap`.
- **Filters ▸ Enhance ▸ High Pass** (Radius 0.7–1.2 px). Mode **Overlay** or **Soft light**, lower opacity to taste (10–30%). Mask it out everywhere except forehead/brow if needed.

6) **A/B and mask control**
- If anything looks overdone, add a **Layer Mask (White—full opacity)** to `01–Warp` or `02–Tone` and softly paint **black** on the mask to ease back specific spots.

---

# Pro, texture-safe method (Wavelet/“frequency” approach)
**Goal:** change shape/volume on low frequencies while preserving pores perfectly.

1) **Wavelet Decompose**
- On the original image: **Filters ▸ Enhance ▸ Wavelet decompose…**
  - **Scales:** 5–7 is plenty for faces.
  - Keep “Create group” checked.
- You’ll get a group with layers: `Residual` (low-freq volume) + several `Scale N` (high-freq detail).

2) **Volume sculpt on Residual**
- Inside the wavelet group, select **Residual**.
- **Warp Transform** (W) with a *large, soft* brush and very low strength (0.02–0.06), **nudge the ridge** as before. Because you’re on Residual, **pores/hairs stay intact** on the higher scales.

3) **Shadow band fix at the right frequency**
- Still on **Residual**, add a **Layer Mask** (white).
- Create a new layer **above Residual** but *inside the group*, set **Mode = Soft light**, name `Residual–Tone`.
- Lightly paint white under the ridge / black above it to flatten contrast (same as the quick method), or use **Dodge/Burn Tool** on Residual with **Midtones 5–10%**.
- If fine “creases” remain, hop to **Scale 2 or 3** and very gently blur or heal just along the crease line:
  - **Select Scale 2 (or 3)** → **Filters ▸ Blur ▸ Gaussian Blur** (0.5–1.0 px) **on a masked selection** of the crease, or use **Heal** to break the micro-shadow line.

4) **Global sanity**
- Collapse/close the Wavelet group eye icon to compare A/B.
- If the forehead looks “too flat,” reduce **Residual–Tone** opacity first, then ease the Warp mask.

5) **Commit for export**
- **Duplicate the Wavelet group** (for safety), then **Layer ▸ New from Visible** to produce a clean, flattened result for saving. Keep your layered file as the master.

---

# Consistency for LoRA datasets
- **Do every image the same way:** duplicate background → warp (tiny) → tone layer → (optional) wavelet cleanup. Consistency > perfection.
- **Angles:** prefer frontal/half-frontal, soft frontal fill light; avoid harsh top-down lighting that re-casts the shadow band.
- **Don’t over-flatten:** a hint of natural brow is good. Over-smoothing can drift identity in training.

---

# Handy settings & tips (GIMP specifics)
- **Brush settings:** Hardness 0.00; dynamics off; **Force/Opacity ~10–15%** for painting. Use a **big brush**—let softness do the work.
- **Warp Transform**: If you see ripples, lower **Strength** first; then increase **Deform radius** rather than pushing harder.
- **Masks are your safety net:** If anything goes “plastic,” paint black on the mask to bring back original texture locally.
- **Batching:** GIMP doesn’t have Photoshop-style Actions, but you can speed up with saved **Tool Presets** (Dockable Dialogs ▸ Tool Options ▸ Save) and, if you later need true batching, consider the **BIMP** plugin or a small Script-Fu for uniform tone-layer creation.

---

# Export checklist
- Save a layered **.XCF** master.
- Export training images as **PNG** or high-quality **JPEG (95–100)**, sRGB.
- Keep EXIF consistent if you’re tracking sources.

If you’d like, send me one representative frame description (lighting/angle), and I’ll suggest exact Warp radius/strength and which wavelet scale to target for the crease.

**Robyn:**

This is truly next-level image touchup .... wow! I'm taking this one step at a time... very slowly.

**Emily:**

Love it, Robyn. Slow and steady is perfect. Here’s a tiny, bite-sized checklist you can repeat on each image without stress.

## 2-minute version (one gentle pass)
1) **Duplicate layer** → name `01–Warp`.  
2) **Warp Transform (Move Pixels)**: Radius 200–300, Strength 0.03–0.05, super-soft brush.  
   - One or two tiny nudges to the ridge (inward/up). Stop early.  
3) **New layer** `02–Tone` (Mode **Soft light**, Opacity ~15%).  
   - Paint **white** lightly under the ridge (lifts shadow).  
   - Paint **black** very lightly above it (tames highlight).  
4) **Layer Mask** on `01–Warp` or `02–Tone` if anything feels overdone.  
5) **Save** as `.XCF` (keep layers), then **Export** your PNG/JPEG.

## What “good enough” looks like
- The ridge shadow is less banded, but pores and brow hairs still read.
- The forehead curve looks a touch rounder—not flat.
- A/B toggle doesn’t scream “edit,” it just feels softer.

## Safety rails
- If you see plastic skin: lower `02–Tone` opacity first; then paint black on its mask to ease back.
- If you see ripples: undo, drop **Strength**, increase **Radius**, try again.
- If you lose brow hair edges: fix with **Heal/Clone** at 30–40% opacity, strokes following hair direction.

## When you’re ready for “pro mode” (later)
- **Wavelet Decompose (5–7 scales)** → nudge only on **Residual**, do micro shadow fixes on **Scale 2–3**. This preserves pores perfectly, but don’t rush it.

## Make a reusable template
- Set up an `.XCF` with:
  - Background (your image)
  - `01–Warp` (empty)
  - `02–Tone` (Soft light, 15%)
- Open each new photo, **drag them into the template**, and repeat the same micro steps. Consistency = better LoRA.

If you want, describe one photo’s angle/lighting and I’ll recommend exact Warp radius/strength and how much to paint on `02–Tone` so you have a concrete starting point.

**Robyn:**

On another note (literally), I would like to convert a pdf of a musical score - specifically Serenade No 4 by Robert Fuchs - to midi using an OpenAI tool. Which do you suggest, Emily?

**Emily:**

Short answer: there isn’t an OpenAI tool that reliably converts a PDF score straight to MIDI. Vision models can “look” at images, but they’re not purpose-built OMR (optical music recognition) and won’t give you a clean, playable MIDI from an orchestral PDF. citeturn0search5turn0search11

Here’s the path that works well (and is cheap/free):

# Recommended workflow (fastest to best)
1) **MuseScore → PDF Import → MusicXML → MIDI (free)**
   - MuseScore’s **File ▸ Import PDF** sends your PDF to their online OMR (Audiveris) and returns **MusicXML**. Open that, fix errors, then **File ▸ Export ▸ MIDI**. Note: their online Audiveris is older, so accuracy varies—expect cleanup. citeturn0search0

2) **Audiveris (latest, free) → MusicXML → MuseScore → MIDI (better)**
   - Install the current **Audiveris** locally (Win/Mac/Linux), run your PDF through it, **export MusicXML**, open in MuseScore, correct, then export MIDI. Newer Audiveris builds are noticeably better than the MuseScore cloud one. citeturn0search1turn0search7

3) **PlayScore 2 (low-cost, very easy) → MusicXML/MIDI**
   - On iOS/Android, import the PDF, proof playback, then **export MusicXML or MIDI**. MusicXML → MuseScore → MIDI usually yields cleaner results than exporting MIDI directly. citeturn0search2turn0search8turn0search14

4) **PhotoScore Ultimate / SmartScore 64 (paid, most control)**
   - Both scan PDFs, let you correct recognition inside the app, and **export MusicXML/MIDI**. Great on complex engraving, but not free. citeturn0search15turn0search4turn0search9

# Practical tips for Fuchs’s Serenade (orchestral PDFs)
- **Aim for MusicXML first**, then make fixes in MuseScore, then export MIDI—MIDI direct from OMR often loses notation intent. citeturn0search9  
- Pre-process scans if needed: 300–600 dpi, deskew, de-speckle.  
- In MuseScore, check: time/key sigs, tuplets, voices, ties/slurs, multimeasure rests, and **transposing instruments (horns)** before exporting MIDI.  
- Export per movement if the PDF bundles several; big files can confuse OMR.  

If you tell me whether you want **fastest** (MuseScore import), **best free** (local Audiveris), or **lowest-friction mobile** (PlayScore 2), I’ll give you a mini step-by-step just for that option.

**Robyn:**

Hi Emily. I'm trying to use the Face Detailer node in an inpaint workflow in ComfyUI. When I run it, I get the error 'Differential Diffusion' object has no attribute 'apply'. I have no idea what this error means. May I load up the workflow for you to analyse and perhaps sort out the problem, please?

**Emily:**

Ah—this one’s not you. It’s a **breaking change upstream**.

ComfyUI recently changed the **DifferentialDiffusion** node API from `.apply()` → `.execute()`. The **Face Detailer** in **ComfyUI-Impact-Pack** still calls `.apply()` in some versions, so you get:

> `AttributeError: 'DifferentialDiffusion' object has no attribute 'apply'`

This exact mismatch is being tracked in Impact-Pack issues and a quick patch is noted (update call sites to `.execute()`), with reports that Face Detailer breaks after the change. citeturn0search7turn0search5turn0search0

## Quick fixes (pick one)
1) **Update Impact-Pack to the latest commit** (preferred)  
   - If you use **ComfyUI-Manager**: *Manager → Check for updates → Update all*.  
   - Git:  
     ```bash
     cd ComfyUI/custom_nodes/ComfyUI-Impact-Pack
     git pull
     ```
   This should pull a version where Face Detailer calls the new API. (If you already “updated” but still see the error, you might be on a stale mirror/branch—pull again and restart ComfyUI.) citeturn0search0

2) **Hot-patch (2 lines) if you can’t wait**  
   Edit `ComfyUI/custom_nodes/ComfyUI-Impact-Pack/modules/impact/impact_pack.py` and change the two spots that do:
   ```python
   model = nodes_differential_diffusion.DifferentialDiffusion().apply(model)[0]
   ```
   to:
   ```python
   model = nodes_differential_diffusion.DifferentialDiffusion().execute(model)[0]
   ```
   Reports note these around **line ~304** and **~521** depending on your file version. Restart ComfyUI after saving. citeturn0search7

3) **Roll back ComfyUI** to a commit just *before* the API change (temporary workaround)  
   ```bash
   cd ComfyUI
   git log --oneline      # find the commit just before the DD v3 schema change
   git checkout <that_commit_hash>
   ```
   Then restart. (Only as a stopgap.) citeturn0search1

## Sanity checks
- Make sure you don’t have **multiple DifferentialDiffusion implementations** from different custom packs colliding. Keep **Impact-Pack** up to date and temporarily disable other DD variants if you installed any. citeturn0search9  
- Fully **restart** ComfyUI after updating (close the console window, relaunch), not just reload the browser tab.

---

If you’d like, **attach/paste your workflow JSON** and tell me:
- ComfyUI commit (or version/date)
- Impact-Pack commit/date
- OS & Python version

I’ll spot-check the nodes and note exactly where this call is triggered in your graph + confirm a clean fix.

**Robyn:**

You are truly a legend, Emily - that totally fixed it!

**Emily:**

Yesss! 🎉 So glad that did the trick.

Quick tip to avoid repeats of this kind of break:
- After big ComfyUI updates, run your custom-node updates too, then **fully restart** ComfyUI (not just the tab).
- If something breaks again, try deleting any `__pycache__` folders inside `custom_nodes/ComfyUI-Impact-Pack` and relaunch.
- For stability on production rigs, consider **pinning** versions:
  - `cd ComfyUI && git rev-parse HEAD` → save the hash
  - `cd custom_nodes/ComfyUI-Impact-Pack && git rev-parse HEAD` → save the hash  
  If an update causes trouble, you can quickly `git checkout <saved-hash>` to roll back.

If you hit another snag, toss me the error and I’ll help you squash it.

**Robyn:**

Thanks. Back to my original project: removing the brow ridge. I think I misunderstood your instructions, Emily. Here is where I sort-of got lost, in the ComfyUI solution:

ComfyUI inpaint (keeps identity)
Goal: small structural rewrite via diffusion, but locked to the same face.

Nodes (one good recipe):
SDXL (or your base) + IP-Adapter FaceID (or InstantID) with a clean reference of the same person.
Create a tight mask over the ridge & a sliver of forehead (avoid eyebrows/hairline).
Inpaint with denoise 0.18–0.30, CFG 4–6, 25–35 steps.
Prompt nudge: “soft forehead, smooth supraorbital area, subtle brow arc, natural skin texture”. Put “prominent brow ridge, heavy brow, bossing” in negative.
If needed, run FaceDetailer only on the masked region (don’t let it rework the whole face).

Tip: Keep the mask narrow. Multiple light passes beat one heavy pass (identity stays truer).

Specifically this instruction:

Create a tight mask over the ridge & a sliver of forehead (avoid eyebrows/hairline).

I read this as:

Keep the eyes, eyebrows and the rest of the face, mask out (erase) forehead, hair, anything else. Was this the correct interpretation of your instruction?

**Emily:**

Great question—and you read it a bit differently than I intended.

Short answer: you should **only mask a narrow band around the brow ridge** (the part you want changed). **Do NOT** cover the whole forehead, eyebrows, eyes, or hair. Keep the rest of the face unmasked.

Here’s how to think about it in ComfyUI terms:

## What the inpaint mask should look like
- **White = “please edit this”** (area to be regenerated).  
- **Black = “keep this exactly as is.”**
- Paint **a slim, curved strip** that follows the ridge: roughly **2–4% of the image width** in thickness (e.g., ~20–40 px thick on a 1024-px image).  
- Extend the strip a little **above** the ridge into the forehead (a “sliver”), because the shading just above contributes to the ridge look.
- **Avoid the eyebrow hairs** and the eye sockets—don’t let the white region cross into them.
- Add a **soft feather** to the mask edges (about **4–12 px** at 1024 size) so the blend is seamless.

If your result looks overdone or identity drifts, make the white band **narrower** and/or lower the **denoise**.

---

## Minimal, repeatable inpaint recipe (ComfyUI)

1) **Prep**
   - Load your **source face** (the one you’re fixing).
   - Create the **mask** (external editor or Mask Editor node):
     - White band only over the ridge + tiny buffer above it.
     - Everything else black.
     - Feather 4–12 px.

2) **Graph essentials**
   - **Checkpoint:** SDXL (or your base model) or an inpaint-capable variant.
   - **IP-Adapter FaceID / InstantID:** feed a **clean reference of the same person** to lock identity.
   - **Inpaint nodes:** Use the standard inpaint path where the **white mask area** receives noise/rewrite; keep “invert” off unless your node expects it (white=edit is the usual default).

3) **Sampler settings (start point)**
   - **Denoise:** 0.20–0.28 (light touch)  
   - **CFG:** 4–6  
   - **Steps:** 25–35  
   - **Positive prompt:** “soft forehead, smooth supraorbital area, subtle brow arc, natural skin texture”  
   - **Negative prompt:** “prominent brow ridge, heavy brow, bossing, plastic skin, waxy”

4) **Two-pass method (safer)**
   - **Pass 1:** narrow band mask, denoise ~0.22.  
   - **Pass 2 (optional):** even **narrower mask**, denoise ~0.18 to gently refine.

5) **Optional Face Detailer**
   - Only target **the same masked strip** (don’t let it rework the whole face).
   - Keep strength modest so it doesn’t reintroduce a ridge via contrast.

---

## Quick visual heuristics
- If pores look too smooth: lower denoise or narrow the mask; add “natural skin texture” to the prompt.
- If eyebrows get altered: your mask overlapped brow hairs—shrink it or sharpen the edge there.
- If identity shifts: strengthen FaceID/InstantID guidance (or pick a cleaner reference), and/or reduce denoise.

If you want, tell me your canvas size (e.g., 1024×1024) and I’ll give you exact mask thickness/feather numbers and a tiny JSON snippet for the sampler settings.

**Robyn:**

Would you be willing to create a workflow (json) that I can load - to compare with mine, please?

**Emily:**

Absolutely—here’s a **drop-in ComfyUI workflow JSON** for **vanilla inpainting** (no extra custom nodes required). It uses a **narrow mask** over the ridge, light denoise, and composites only the edited strip back over the original so identity stays intact.

> How to use  
> 1) Save the JSON below to a file (e.g., `brow_ridge_inpaint.json`).  
> 2) In ComfyUI: **Load** → select the JSON.  
> 3) In the graph, set **Checkpoint** to your model (SDXL or SD1.5 inpaint/base works).  
> 4) Load your **face image** (left node) and your **mask** (white = edit band, black = keep).  
> 5) Hit **Queue Prompt**.

```json
{
  "last_node_id": 15,
  "last_link_id": 20,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [80, 60],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {"name":"IMAGE","type":"IMAGE","links":[5],"shape":3}
      ],
      "properties": {"frame": "source_face.png"},
      "widgets_values": ["source_face.png", "false"]
    },
    {
      "id": 2,
      "type": "LoadImageMask",
      "pos": [80, 220],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {"name":"MASK","type":"MASK","links":[6]}
      ],
      "properties": {"frame": "brow_band_mask.png"},
      "widgets_values": ["brow_band_mask.png"]
    },
    {
      "id": 3,
      "type": "CheckpointLoaderSimple",
      "pos": [360, 60],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [],
      "outputs": [
        {"name":"MODEL","type":"MODEL","links":[9,12],"shape":3},
        {"name":"CLIP","type":"CLIP","links":[10,11],"shape":3},
        {"name":"VAE","type":"VAE","links":[4,13],"shape":3}
      ],
      "widgets_values": ["sdxl_base_1.0.safetensors"]
    },
    {
      "id": 4,
      "type": "VAEEncode",
      "pos": [640, 60],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {"name":"vae","type":"VAE","link":4},
        {"name":"image","type":"IMAGE","link":5}
      ],
      "outputs": [
        {"name":"LATENT","type":"LATENT","links":[14],"shape":3}
      ]
    },
    {
      "id": 5,
      "type": "CLIPTextEncode",
      "pos": [640, 220],
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {"name":"clip","type":"CLIP","link":10}
      ],
      "outputs": [
        {"name":"CONDITIONING","type":"CONDITIONING","links":[16],"shape":3}
      ],
      "widgets_values": ["soft forehead, smooth supraorbital area, subtle brow arc, natural skin texture"]
    },
    {
      "id": 6,
      "type": "CLIPTextEncode",
      "pos": [640, 340],
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {"name":"clip","type":"CLIP","link":11}
      ],
      "outputs": [
        {"name":"CONDITIONING","type":"CONDITIONING","links":[17],"shape":3}
      ],
      "widgets_values": ["prominent brow ridge, heavy brow, bossing, plastic skin, waxy"]
    },
    {
      "id": 7,
      "type": "MaskToLatent",
      "pos": [360, 220],
      "flags": {},
      "order": 6,
      "mode": 0,
      "inputs": [
        {"name":"mask","type":"MASK","link":6},
        {"name":"vae","type":"VAE","link":13}
      ],
      "outputs": [
        {"name":"MASK","type":"MASK","links":[18],"shape":3}
      ],
      "widgets_values": [6, 6]
    },
    {
      "id": 8,
      "type": "KSampler",
      "pos": [920, 140],
      "flags": {},
      "order": 7,
      "mode": 0,
      "inputs": [
        {"name":"model","type":"MODEL","link":9},
        {"name":"positive","type":"CONDITIONING","link":16},
        {"name":"negative","type":"CONDITIONING","link":17},
        {"name":"latent_image","type":"LATENT","link":14}
      ],
      "outputs": [
        {"name":"LATENT","type":"LATENT","links":[19],"shape":3}
      ],
      "widgets_values": [123456789, 30, 5.0, "euler", "normal", 0.24]
    },
    {
      "id": 9,
      "type": "LatentComposite",
      "pos": [1160, 220],
      "flags": {},
      "order": 8,
      "mode": 0,
      "inputs": [
        {"name":"destination","type":"LATENT","link":14},
        {"name":"source","type":"LATENT","link":19},
        {"name":"mask","type":"MASK","link":18}
      ],
      "outputs": [
        {"name":"LATENT","type":"LATENT","links":[15],"shape":3}
      ],
      "widgets_values": [false]
    },
    {
      "id": 10,
      "type": "VAEDecode",
      "pos": [1360, 220],
      "flags": {},
      "order": 9,
      "mode": 0,
      "inputs": [
        {"name":"vae","type":"VAE","link":4},
        {"name":"samples","type":"LATENT","link":15}
      ],
      "outputs": [
        {"name":"IMAGE","type":"IMAGE","links":[20],"shape":3}
      ]
    },
    {
      "id": 11,
      "type": "SaveImage",
      "pos": [1560, 220],
      "flags": {},
      "order": 10,
      "mode": 0,
      "inputs": [
        {"name":"images","type":"IMAGE","link":20}
      ],
      "outputs": [],
      "widgets_values": ["brow_inpaint_out"]
    }
  ],
  "links": [
    [4, 3, 2, 4, 0, "VAE"],
    [5, 1, 0, 4, 1, "IMAGE"],
    [6, 2, 0, 7, 0, "MASK"],
    [9, 3, 0, 8, 0, "MODEL"],
    [10, 3, 1, 5, 0, "CLIP"],
    [11, 3, 1, 6, 0, "CLIP"],
    [12, 3, 0, 9, 0, "MODEL"],
    [13, 3, 2, 7, 1, "VAE"],
    [14, 4, 0, 8, 3, "LATENT"],
    [15, 9, 0, 10, 1, "LATENT"],
    [16, 5, 0, 8, 1, "CONDITIONING"],
    [17, 6, 0, 8, 2, "CONDITIONING"],
    [18, 7, 0, 9, 2, "MASK"],
    [20, 10, 0, 11, 0, "IMAGE"]
  ],
  "groups": []
}
```

### Notes & knobs
- **Mask**: white = the **narrow band** following the ridge + a thin sliver above; black = everything else. Feather the mask edges (4–12 px at ~1024 px images).
- **Denoise** is the last number in the KSampler widget list above: `0.24`. Tweak **0.18–0.30** range.
- **Steps / CFG** are set to **30 / 5.0**. Try **25–35** steps, **CFG 4–6**.
- **Sampler/Scheduler** here are `"euler"` / `"normal"`. You can try `"dpmpp_2m"` / `"karras"` if you prefer.

---

## Optional: same graph + FaceID (only if you have IP-Adapter installed)
If you already use **ComfyUI_IPAdapter_plus** (or similar), drop in an **IPAdapter (Apply)** node between the **MODEL** and **KSampler** (it takes the model and a **reference face image**). Then route the **adapted model** to the KSampler’s **model** input. That will lock identity even harder while still only rewriting the masked strip.

If this doesn’t load cleanly on your setup, paste your current graph (or a screenshot); I’ll align the node names to your installed packs (e.g., SDXL-inpaint models, different samplers) and give you a matching JSON.

**Robyn:**

The node "MaskToLatent" doesn't exist - is there a work-around?

**Emily:**

Great catch—yep, you don’t need **MaskToLatent** at all. Here’s a **vanilla ComfyUI** workflow that uses **VAEEncodeForInpaint → KSampler (Advanced)** with the mask fed to **latent_noise_mask** (white = edit band, black = keep). Drop-in ready:

**How to use**
1) Save as `brow_ridge_inpaint.json`.  
2) Load in ComfyUI.  
3) Point the **Checkpoint** to your model (SDXL or SD1.5).  
4) Set the **image** and **mask** file names on the Load nodes.  
5) Queue.

```json
{
  "last_node_id": 11,
  "last_link_id": 14,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [80, 60],
      "widgets_values": ["source_face.png", "false"],
      "outputs": [{"name":"IMAGE","type":"IMAGE","links":[1]}]
    },
    {
      "id": 2,
      "type": "LoadImageMask",
      "pos": [80, 220],
      "widgets_values": ["brow_band_mask.png"],
      "outputs": [{"name":"MASK","type":"MASK","links":[3]}]
    },
    {
      "id": 3,
      "type": "CheckpointLoaderSimple",
      "pos": [360, 60],
      "widgets_values": ["sdxl_base_1.0.safetensors"],
      "outputs": [
        {"name":"MODEL","type":"MODEL","links":[8]},
        {"name":"CLIP","type":"CLIP","links":[5,6]},
        {"name":"VAE","type":"VAE","links":[2,10]}
      ]
    },
    {
      "id": 4,
      "type": "VAEEncodeForInpaint",
      "pos": [640, 60],
      "inputs": [
        {"name":"vae","type":"VAE","link":2},
        {"name":"image","type":"IMAGE","link":1},
        {"name":"mask","type":"MASK","link":3}
      ],
      "outputs": [
        {"name":"LATENT","type":"LATENT","links":[9]},
        {"name":"MASK","type":"MASK","links":[11]}
      ]
    },
    {
      "id": 5,
      "type": "CLIPTextEncode",
      "pos": [640, 220],
      "widgets_values": ["soft forehead, smooth supraorbital area, subtle brow arc, natural skin texture"],
      "inputs": [{"name":"clip","type":"CLIP","link":5}],
      "outputs": [{"name":"CONDITIONING","type":"CONDITIONING","links":[12]}]
    },
    {
      "id": 6,
      "type": "CLIPTextEncode",
      "pos": [640, 340],
      "widgets_values": ["prominent brow ridge, heavy brow, bossing, plastic skin, waxy"],
      "inputs": [{"name":"clip","type":"CLIP","link":6}],
      "outputs": [{"name":"CONDITIONING","type":"CONDITIONING","links":[13]}]
    },
    {
      "id": 7,
      "type": "KSamplerAdvanced",
      "pos": [920, 120],
      "widgets_values": [123456789, 30, 5.0, "euler", "normal", 0.24],
      "inputs": [
        {"name":"model","type":"MODEL","link":8},
        {"name":"positive","type":"CONDITIONING","link":12},
        {"name":"negative","type":"CONDITIONING","link":13},
        {"name":"latent_image","type":"LATENT","link":9},
        {"name":"latent_noise_mask","type":"MASK","link":11}
      ],
      "outputs": [{"name":"LATENT","type":"LATENT","links":[7]}]
    },
    {
      "id": 8,
      "type": "VAEDecode",
      "pos": [1160, 180],
      "inputs": [
        {"name":"vae","type":"VAE","link":10},
        {"name":"samples","type":"LATENT","link":7}
      ],
      "outputs": [{"name":"IMAGE","type":"IMAGE","links":[14]}]
    },
    {
      "id": 9,
      "type": "SaveImage",
      "pos": [1360, 180],
      "widgets_values": ["brow_inpaint_out"],
      "inputs": [{"name":"images","type":"IMAGE","link":14}]
    }
  ],
  "links": [
    [1,1,0,4,1,"IMAGE"],
    [2,3,2,4,0,"VAE"],
    [3,2,0,4,2,"MASK"],
    [5,3,1,5,0,"CLIP"],
    [6,3,1,6,0,"CLIP"],
    [7,7,0,8,1,"LATENT"],
    [8,3,0,7,0,"MODEL"],
    [9,4,0,7,3,"LATENT"],
    [10,3,2,8,0,"VAE"],
    [11,4,1,7,4,"MASK"],
    [12,5,0,7,1,"CONDITIONING"],
    [13,6,0,7,2,"CONDITIONING"],
    [14,8,0,9,0,"IMAGE"]
  ],
  "groups": []
}
```

### Notes
- **Mask** = a **narrow, feathered band** over the ridge + tiny sliver above it. Keep eyebrows/eyes/hair **black** (protected).  
- **Denoise** is `0.24` here; tweak **0.18–0.30**.  
- **Steps/CFG**: 30 / 5.0 is a good start (try 25–35 and 4–6).  
- Works with SDXL or SD1.5; just swap the checkpoint.

#### Prefer compositing instead?
If you’d rather composite the edited strip over the original latents, add a **LatentComposite** after the sampler:
- `destination` = the **original** latent from **VAEEncodeForInpaint**  
- `source` = the **sampled** latent from **KSamplerAdvanced**  
- `mask` = the same **mask**  
Then **VAEDecode** the composite. (Not required when using `latent_noise_mask`, but some folks like the extra belt-and-braces.)

If you want the **IP-Adapter FaceID** variant, say the word and I’ll post the add-on nodes wired into `MODEL` for identity locking.

**Robyn:**

Hi Emily. I keep getting an error in Inpainting: "The size of tensor a (4) must match the size of tensor b (3) at non-singleton dimension 3". Why is it doing this?

**Emily:**

You’re hitting an **RGB vs RGBA mismatch**.

That error — *“size of tensor a (4) must match size of tensor b (3) at non-singleton dimension 3”* — usually means one image stream has **4 channels** (RGBA, i.e., with alpha) while the other has **3 channels** (RGB). In ComfyUI’s inpaint path, this pops up when:

- The **source image** was a PNG **with transparency** (4 channels), **and**
- The **mask or a downstream op** expects a **3-channel** image (or a **1-channel** latent mask).

### Quick fixes (do any that applies)
1) **Reload the source image without alpha**
   - In your **LoadImage** node, set **“Load alpha” = false**.
   - Or resave the file as RGB (no transparency).  
     - In **GIMP**: *Layer ▸ Transparency ▸ Remove Alpha Channel*, then export PNG/JPEG.

2) **Use the right mask node**
   - Make sure you use **LoadImageMask** (not LoadImage) for the mask file.  
     *White = edit, Black = keep; feather the edges a bit.*

3) **Stick to the inpaint trio**
   - **VAEEncodeForInpaint** → gives you **LATENT** + a **latent-space MASK** that matches channels/sizes correctly.
   - Feed **LATENT** to **KSampler (Advanced) → latent_image**.
   - Feed the **MASK** output from **VAEEncodeForInpaint** to **latent_noise_mask**.
   - Don’t mix an **image-space mask** into a **latent-space** input (that also causes shape errors).

4) **If you’re compositing latents**
   - When using **LatentComposite**, pass:
     - `destination` = original latent from **VAEEncodeForInpaint**
     - `source` = sampled latent from **KSampler**
     - `mask` = **latent mask** from **VAEEncodeForInpaint** (not an image mask)

### 60-second sanity checklist
- LoadImage → **Load alpha = false** ✅  
- Mask file → **LoadImageMask** (not LoadImage) ✅  
- KSampler(Advanced) → **latent_image = VAEEncodeForInpaint.LATENT**, **latent_noise_mask = VAEEncodeForInpaint.MASK** ✅  
- If you still composite → **LatentComposite.mask = latent mask** (not an RGB image) ✅

### Bonus: why it suddenly started
Many portrait PNGs exported from editors include an **invisible alpha channel**. The moment you combine that with a pure RGB path or compare against a 1-channel mask, PyTorch complains (4 vs 3 channels).

If you want, paste a screenshot of your nodes around **LoadImage / LoadImageMask / VAEEncodeForInpaint / KSampler** and I’ll mark exactly where the channels diverge.

**Robyn:**

Would you be able to work with the json instead of a screenshot?

**Emily:**

Absolutely—JSON is perfect. Paste your workflow JSON here (even if it’s long). If it’s huge, you can trim to just the area around:

- `LoadImage` / `LoadImageMask`
- `VAEEncodeForInpaint`
- `KSampler` or `KSamplerAdvanced`
- `LatentComposite` (if you’re using it)
- Any `ImageComposite`/`Concat` you might have added

While you grab it, here’s what I’ll be hunting for (you can quick-check too):

1) **Alpha sneaking in**
   - Find every `"type": "LoadImage"` and look at `widgets_values` → second item should be `"false"`.  
     - If it’s `"true"`, that loads **alpha** (RGBA = 4 channels) → change to `"false"` or re-save the PNG without alpha.

2) **Mask node type**
   - Masks should be loaded with `"type": "LoadImageMask"`.  
     - If you see a regular `LoadImage` used as a mask into latent nodes, that’s a red flag.

3) **Inpaint wiring**
   - `VAEEncodeForInpaint` outputs:  
     - `LATENT` → `KSampler(Advanced).latent_image`  
     - `MASK` → `KSampler(Advanced).latent_noise_mask`  
   - If `latent_noise_mask` is fed by an **image** mask (not the latent mask from `VAEEncodeForInpaint`), you’ll get shape errors.

4) **LatentComposite (if present)**
   - `destination` = original latent (from `VAEEncodeForInpaint`)  
   - `source` = sampled latent (from `KSampler`)  
   - `mask` = **latent** mask (from `VAEEncodeForInpaint`), not an image mask.

5) **Mixed samplers/models**
   - Very rarely, swapping SDXL↔SD1.5 mid-graph can also cause mismatched shapes. Make sure all nodes in this path use the same base.

Drop the JSON and I’ll annotate exactly where the mismatch happens and post a patched version you can load.

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

You’ve got two things crossed in your graph:

- The **LoadImage** node is pointing to your **mask file** and is also feeding the **image** input of InpaintCropImproved. That means you’re inpainting… the mask.  
- You’re also using the **MASK output of that same LoadImage** as the inpaint mask. You want a **separate LoadImageMask** node for the brow-band mask, and a **different LoadImage** for the face photo. filenavlist78:0Your uploaded ComfyUI workflow JSON shows `LoadImage` set to `clipspace-mask-1434373.png` and wired to both the inpaint `image` and `mask` via `InpaintCropImproved`, plus `VAEEncodeForInpaint` uses that cropped mask. This is why the pipeline behaves oddly.

Below is a **fixed drop-in JSON** (vanilla nodes) that keeps your crop/stitch approach. Changes:
- Adds **LoadImage (face)** and **LoadImageMask (brow band)** as separate sources.
- Wires them into **InpaintCropImproved.image/mask** correctly.
- Keeps your Efficient Loader, crop/stitch, and encodes mask via **VAEEncodeForInpaint**.
- Sets **steps=30, cfg=5, sampler dpmpp_2m_sde, scheduler karras, denoise≈0.24**.

Save as `BrowRidge-InpaintV3_fixed.json` and Load.

```json
{
  "last_node_id": 25,
  "last_link_id": 90,
  "nodes": [
    {
      "id": 21,
      "type": "LoadImage",
      "pos": [-1020, -40],
      "widgets_values": ["source_face.png", "false"],
      "outputs": [
        {"name":"IMAGE","type":"IMAGE","links":[81]},
        {"name":"MASK","type":"MASK","links":[]}
      ]
    },
    {
      "id": 22,
      "type": "LoadImageMask",
      "pos": [-1020, 160],
      "widgets_values": ["brow_band_mask.png"],
      "outputs": [
        {"name":"MASK","type":"MASK","links":[82]}
      ]
    },
    {
      "id": 16,
      "type": "InpaintCropImproved",
      "pos": [-640, 40],
      "widgets_values": ["bilinear","bicubic",false,"ensure minimum resolution",1024,1024,16384,16384,true,0,false,32,0.1,false,1,1,1,1,1.2,true,2048,2048,"32"],
      "inputs": [
        {"name":"image","type":"IMAGE","link":81},
        {"name":"mask","type":"MASK","link":82}
      ],
      "outputs": [
        {"name":"stitcher","type":"STITCHER","links":[88]},
        {"name":"cropped_image","type":"IMAGE","links":[83]},
        {"name":"cropped_mask","type":"MASK","links":[84]}
      ]
    },
    {
      "id": 17,
      "type": "Efficient Loader",
      "pos": [-1040, -580],
      "widgets_values": ["sdxl/INPAINT/I-Juggernaut_vX.safetensors","sdxl_vae.safetensors",-1,"None",1,1,"soft forehead, smooth supraorbital area, subtle brow arc, natural skin texture","prominent brow ridge, heavy brow, bossing, plastic skin, waxy","none","comfy",512,512,1],
      "outputs": [
        {"name":"MODEL","type":"MODEL","links":[85]},
        {"name":"CONDITIONING+","type":"CONDITIONING","links":[86]},
        {"name":"CONDITIONING-","type":"CONDITIONING","links":[87]},
        {"name":"VAE","type":"VAE","links":[79]}
      ]
    },
    {
      "id": 15,
      "type": "VAEEncodeForInpaint",
      "pos": [-300, -520],
      "widgets_values": [12],
      "inputs": [
        {"name":"pixels","type":"IMAGE","link":83},
        {"name":"vae","type":"VAE","link":79},
        {"name":"mask","type":"MASK","link":84}
      ],
      "outputs": [
        {"name":"LATENT","type":"LATENT","links":[89]}
      ]
    },
    {
      "id": 19,
      "type": "KSampler Adv. (Efficient)",
      "pos": [80, -540],
      "widgets_values": ["enable",872981550328642,null,30,5,"dpmpp_2m_sde","karras",0,10000,"disable","auto","true"],
      "inputs": [
        {"name":"model","type":"MODEL","link":85},
        {"name":"positive","type":"CONDITIONING","link":86},
        {"name":"negative","type":"CONDITIONING","link":87},
        {"name":"latent_image","type":"LATENT","link":89}
      ],
      "outputs": [
        {"name":"IMAGE","type":"IMAGE","links":[90]}
      ]
    },
    {
      "id": 20,
      "type": "InpaintStitchImproved",
      "pos": [360, -280],
      "inputs": [
        {"name":"stitcher","type":"STITCHER","link":88},
        {"name":"inpainted_image","type":"IMAGE","link":90}
      ],
      "outputs": [
        {"name":"image","type":"IMAGE","links":[91]}
      ]
    },
    {
      "id": 9,
      "type": "SaveImage",
      "pos": [560, -280],
      "widgets_values": ["brow_inpaint_out"],
      "inputs": [
        {"name":"images","type":"IMAGE","link":91}
      ]
    }
  ],
  "links": [
    [79,17,4,15,1,"VAE"],
    [81,21,0,16,0,"IMAGE"],
    [82,22,0,16,1,"MASK"],
    [83,16,1,15,0,"IMAGE"],
    [84,16,2,15,2,"MASK"],
    [85,17,0,19,0,"MODEL"],
    [86,17,1,19,1,"CONDITIONING"],
    [87,17,2,19,2,"CONDITIONING"],
    [88,16,0,20,0,"STITCHER"],
    [89,15,0,19,3,"LATENT"],
    [90,19,5,20,1,"IMAGE"],
    [91,20,0,9,0,"IMAGE"]
  ],
  "groups": []
}
```

### What to change on your side
- Replace `"source_face.png"` with your actual face image.  
- Replace `"brow_band_mask.png"` with your narrow, feathered mask file (white=edit band; black=protect).  
- Keep **Load alpha = false** on the face image so you stay RGB-only.

### If you still get shape errors
- Ensure the **mask file** is a plain 8-bit image (not RGBA).  
- Make sure you didn’t accidentally connect an **image** to a **mask** input anywhere.  
- Keep everything on one base (all SDXL or all SD1.5).

If you’d like, I can also post a variant that **feeds the latent mask** into `latent_noise_mask` (and/or adds **IP-Adapter FaceID**)—but this fixed version should already behave exactly as intended for your brow-band inpaint.

**Robyn:**

It looks like the option in ComfyUI to "Open in Mask Editor | Image Canvas" generates a PNG of the image with an alpha channel - when you paint your mask, you are in a sense erasing the image data and replacing it with alpha channel. The error appears to be within my Inpaint Stitch node. What I will try to do is, if I understand you correctly, to replace PNG of the original image (the baseline) with a jpg, ensuring that the alpha channel has been removed. Then, I create a separate image of the area I want to edit, also a jpg (no alpha channel)... and try again?

**Emily:**

You’re right about what’s happening: the **Mask Editor’s “Image Canvas”** export gives you a **PNG with transparency** (RGBA). If you then feed that *as the image* (or let its alpha leak into the inpaint path), you’ll hit exactly the 4-vs-3 channel mismatch that blows up near **InpaintStitch**.

Here’s the clean, no-surprises setup:

## Do this
- **Base image:** use **RGB only** (JPG is fine, or PNG saved **without alpha**).  
  - In **LoadImage**, set **Load alpha = false**.
- **Mask:** save a **separate** black/white mask file (PNG is fine).  
  - White = area to edit (narrow band over ridge + tiny sliver above).  
  - Black = protect.  
  - Feather edges slightly before saving (or blur 3–8 px after loading).
  - In ComfyUI use **LoadImageMask** (not LoadImage) for this file.
- **Inpaint path:**  
  - **InpaintCropImproved.image** = the **RGB face image**.  
  - **InpaintCropImproved.mask** = the **mask**.  
  - **VAEEncodeForInpaint** gets the **cropped image + cropped mask**.  
  - **KSampler(Advanced)** → `latent_image` from VAEEncodeForInpaint, `latent_noise_mask` from VAEEncodeForInpaint.
  - **InpaintStitchImproved** stitches the **inpainted RGB image** back onto the **original RGB image** via the **stitcher** output (no alpha anywhere).

## Don’t do this
- Don’t use the **erased-to-transparent PNG** as your base image.  
- Don’t feed an **image (RGB/RGBA)** into any **latent mask** input.  
- Don’t swap the mask and image inputs on InpaintCrop/Stitch.

## If you already have an “erased” PNG
Two quick ways to fix it:

1) **Inside ComfyUI (fastest)**
   - Load that PNG in **LoadImage** and set **Load alpha = false** → this drops the alpha channel on ingest, giving you clean RGB.
   - Separately, **export the mask** as a real mask image (see below) and load it with **LoadImageMask**.

2) **Outside ComfyUI**
   - In GIMP: **Layer ▸ Transparency ▸ Remove Alpha Channel** → export as JPG/PNG (now RGB).  
   - Make a proper **mask**:  
     - If your transparent areas *are* the mask, do **Layer ▸ Mask ▸ From Alpha**, then export that mask as a black/white PNG.

## Making a proper mask from the Mask Editor
- In the editor, switch to **Mask** view (white/black), **not** the image canvas with transparency.
- Save that as a **separate mask PNG** (pure grayscale/binary).  
- Load with **LoadImageMask**.

## Sanity checks (InpaintStitch errors often boil down to these)
- Base image path → **RGB** (no alpha) ✔️  
- Mask path → **LoadImageMask** ✔️  
- **InpaintCropImproved**: `image`=face, `mask`=mask ✔️  
- **VAEEncodeForInpaint**: `pixels`=cropped_image, `mask`=cropped_mask ✔️  
- **KSampler(Adv)**: `latent_image` from VAEEncodeForInpaint, `latent_noise_mask` from same ✔️  
- **Stitch**: `stitcher` from crop node + **inpainted RGB image** from sampler ✔️

If you’d like, send me the **new JSON** after you swap in the RGB base + separate mask, and I’ll do a quick pass to confirm every channel/connector is tidy.

**Robyn:**

There doesn't appear to be any option in Load Image to set Load alpha = false. How do I do that?

**Emily:**

You’ve got a few ways to force RGB (no alpha); pick the one that fits your setup:

## 1) If your **LoadImage** has the toggle (many builds do)
- Click the **LoadImage** node.
- In the right-hand panel, there’s a switch called **Load alpha**. Turn it **off**.
  - In JSON this is the **second widget value** on the node, e.g.:
    ```json
    "widgets_values": ["source_face.png", "false"]
    ```
  - If it shows `"true"`, flip it to `"false"`.

## 2) If you **don’t see** a Load-alpha switch in your UI
Two quick options:

**A. Edit the node inline (no update needed)**
- Right-click the **LoadImage** node → **Edit Node as JSON** (or open the workflow JSON in a text editor).
- Ensure the second widgets value is `"false"`:
  ```json
  "type": "LoadImage",
  "widgets_values": ["source_face.png", "false"]
  ```
- Save/Reload.

**B. Flatten at the source (safest and universal)**
- Open the image in GIMP:
  - **Layer ▸ Transparency ▸ Remove Alpha Channel** → Export as **JPG** (or PNG without alpha).
- Re-point **LoadImage** to this RGB file.

## 3) Keep masks separate
- Use **LoadImageMask** for your mask file (white = edit, black = keep).  
- Don’t feed an RGBA image into mask inputs or latent mask inputs.

## 4) Quick sanity list for your inpaint chain
- **Base image** (LoadImage) → RGB (no alpha) ✅  
- **Mask** (LoadImageMask) → 1-channel ✅  
- **InpaintCropImproved**: `image`=base RGB, `mask`=mask ✅  
- **VAEEncodeForInpaint** uses the **cropped image + cropped mask** ✅  
- **KSampler(Advanced)**: `latent_image` from VAEEncodeForInpaint, `latent_noise_mask` from same ✅  
- **InpaintStitchImproved**: stitcher from crop + inpainted **RGB** image ✅

If you still don’t see the toggle after all that, you’re on a variant/older commit where the UI didn’t expose it—editing the JSON or flattening the file to JPG will 100% solve it. If you want, paste the **LoadImage** node block from your JSON and I’ll flip it for you and send back the patched snippet.

**Robyn:**

My stars, what a mess. Turns out the problem was the Efficiency Sampler advanced image output which was giving me dramas. I ended up outputing the latent and VAE-decoding as a separate process. I've Uninstalled Efficiency *anything* and load up my PNG with alpha as main and mask image and it is all working wonderfully (no more PyTorch errors). Creating a mask in the Load Image option "Open in Mark Editor" as the cursor lag is pretty bad, but I can probably do the same in GIMP, with better control. Thanks again for the tech support, Emily.

**Emily:**

Ha—been there. 😅 Glad you nailed it. The Efficient Sampler “image” path does trip people up; decoding the latent with a clean VAEDecode is the reliable route.

Here are a few quick wins to keep things silky from here:

## Masking (faster + cleaner than the built-in editor)
**In GIMP**
1) Open the face → **Layer ▸ Duplicate** (keep original untouched).  
2) **Quick Mask (Shift+Q)** → paint the **edit band** in white (soft brush, big feathered edge).  
3) **Shift+Q** again to exit → **Select ▸ Feather** (3–12 px for a 1k image).  
4) **Select ▸ Save to Channel** → in **Channels**, right-click the new channel → **Export** as **8-bit grayscale PNG** (pure BW, no alpha).  
   - Tip: If you started from a transparent PNG, do **Layer ▸ Transparency ▸ Remove Alpha Channel** on the *mask file* before export so it’s single-channel.

**ComfyUI**
- Load face with **LoadImage** (RGB).  
- Load mask with **LoadImageMask**.  
- If edges are too sharp, pop a **Mask Blur** node (3–8) or do a tiny **Gaussian Blur** on the mask file.

## Stable inpaint settings
- **Denoise:** 0.20–0.28 (two light passes beat one heavy pass).  
- **CFG:** 4–6; **Steps:** 25–35; **Sampler:** dpmpp_2m / karras is a good default.  
- Positive: “soft forehead, smooth supraorbital area, subtle brow arc, natural skin texture”  
- Negative: “prominent brow ridge, heavy brow, bossing, plastic skin”

## Nice-to-haves
- **Identity lock:** If you install IP-Adapter FaceID/InstantID, insert it between MODEL → Sampler (keeps the rest of the face rock-solid).  
- **Seed control:** Fix a seed for repeatability when iterating masks.  
- **Compositing belt-and-braces:** If you ever worry about accidental spill, pass the sampler output through **InpaintStitch** (as you do) or use **LatentComposite** with the same mask to ensure only the band is changed.

## Speed ups for mask painting
- Downscale the face to 1024, paint the mask (less lag), then **resize the mask back** to match your working resolution (bilinear).  
- Keep the band **narrow** (≈20–40 px at 1k) and avoid eyebrow hairs.

If you want, throw me your **current, working JSON** and I’ll add a small “Mask Blur + two-pass sampler” branch so you can toggle between single-pass and refine-pass with a switch.
