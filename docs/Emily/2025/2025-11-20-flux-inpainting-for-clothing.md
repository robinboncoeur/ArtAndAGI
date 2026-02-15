---
title: "Flux inpainting for clothing"
date: 2025-11-20
---

# Flux inpainting for clothing

**Robyn:**

Hi Emily. I've had quite a bit of suscess segmenting clothing from figures in images and pasted the segmented clothing into new images against a grey background. I use a LayerMark: SegmentAnything v2 node, which is a lot less work than manually painting a mask. However, if there's a hand in the way or even hair, then the article of clothing has missing bits. I'm wondering if there is a Flux-based inpainting technique that could fix those items for me.

**Emily:**

Ohhh yes, this is *exactly* the kind of thing Flux is good at: hallucinating the missing fabric where SAM carved bits out. 💅

You’re absolutely right about the limitation: any segmenter (SAMv2 included) can’t see “behind” hands or hair, so the clothing cut-out literally *has no pixels* there. To fix that, you need a generative pass that:

- **Keeps** the existing garment as-is,  
- **Only re-draws** the “holes” / damaged areas,  
- And **understands** “this is fabric, not skin / hands / hair”.

Below is a practical Flux-based approach in ComfyUI that should slot nicely into your existing workflow.

---

## Strategy overview

You’ve already got:

- A clothing-only image on a **neutral grey background** (great!),  
- The problem: **gaps / bite marks** in the garment where hands or hair used to be.

The idea is:

1. Take that grey-background clothing image.  
2. Quickly mask the damaged areas (far less work than masking the whole garment).  
3. Use **Flux inpainting in latent space** so only the masked areas are regenerated, guided by a prompt like *“red satin dress, no hands, no hair, smooth fabric”*.  
4. Decode → you now have a “repaired” garment you can reuse in composites.

---

## Option 1 – Fix the garment on the grey background (recommended)

This works entirely on your clothing cut-out and doesn’t touch the original figure.

### 1. Prepare the image and mask

1. **Load the clothing cut-out**  
   - `Load Image` → your grey-background clothing PNG/JPG.

2. **Create a repair mask**  
   - Use `Open in Mask Editor` on this image.  
   - Roughly paint **white** over:
     - Any holes where the hand/hair was.
     - Any jagged / chewed edges you’d like Flux to smooth.  
   - Everything you *don’t* want changed stays black.

   It’s a small mask, so still way easier than masking the entire garment.

3. (Nice-to-have) **Soften the mask edges**  
   - Run the mask through something like:
     - `Morphology (Erode/Dilate)` to shrink / expand a bit if needed.
     - `Blur Mask` (radius 4–8) to feather edges so Flux doesn’t leave seams.

---

### 2. Encode with Flux

You’re already using `SamplerCustomAdvanced` for Flux, so let’s stick to that style.

1. **Load Flux model**  
   - `Load Checkpoint` → your Flux.1 model (e.g. `flux1-dev`, `flux1-dev-8steps`, whatever you’re using now).

2. **Text conditioning**  
   - `CLIP Text Encode (Prompt)`:
     - **Positive prompt example:**
       > “elegant [garment description], clean continuous fabric, no hands, no hair, detailed folds, high quality”
     - **Negative prompt example:**
       > “hands, arms, fingers, skin, hair, face, body, distortion, artifacts”
   - Feed this into your **guider** setup exactly as you do in your usual Flux workflow.

3. **Encode image to latents**  
   - Use the appropriate Flux image-to-latent node (whatever you currently use to make `latent_image` for `SamplerCustomAdvanced`):
     - `VAE Encode` / `Image to Latent` → `LATENT_BASE`.

---

### 3. Turn the mask into an inpaint latent

You want **only** the masked area to start as noise (to be regenerated), and the rest to start from the existing garment.

A common pattern (names will differ slightly depending on nodes you have, but concept is the same):

1. **Create a noise latent**  
   - `Latent Noise` / `Empty Latent` sized to match `LATENT_BASE` → call it `LATENT_NOISE`.

2. **Composite latents using the mask**  
   - Use a node like `LatentComposite`, `LatentCompositeMasked`, or an Impact node that mixes two latents by a mask:
     - Base: `LATENT_BASE`
     - Overlay: `LATENT_NOISE`
     - Mask: your (blurred) mask
     - Output → `LATENT_INPAINT`

   Interpretation:
   - Unmasked area = original garment latent (so it barely changes).  
   - Masked area = noise → Flux has freedom to *rebuild* that region.

3. **Feed to Flux sampler**

   With `SamplerCustomAdvanced`, you’ll hook it up roughly like:

   - `latent_image` → `LATENT_INPAINT`
   - `noise` → you can often leave as-is or feed `LATENT_INPAINT` depending on your current graph; stick to what your working Flux setup expects, just **swap in this new latent** where you previously sent the vanilla encoded latent.

---

### 4. Sampler settings for gentle, fabric-only fixes

You *don’t* want Flux to invent a totally new outfit, just to heal the scars.

Try something like:

- **Steps**: 20–30  
- **CFG / guidance**: 3–5 (Flux is happier lower than SDXL-style CFG values)  
- **Denoise strength**:  
  - Start at **0.35–0.45**  
  - If it’s too timid and the hole is still visible → bump up toward **0.55–0.6**.  
  - If Flux keeps redesigning the whole garment → *lower* denoise.

Decode the result with your Flux VAE → `Save Image`.

You should now have a continuous garment with the hand/hair invisibly “removed”, and the grey background largely intact.

---

## Option 2 – Work on the original full-body image, *then* re-segment

Sometimes Flux repairs better when it sees the **whole figure**, not just floating clothes.

Workflow idea:

1. Load the original figure image.  
2. Use SAM v2 not to slice out clothing, but just to select a rough region around the clothing + hand/hair.  
3. Make a mask where:
   - White = the **hand/hair and damaged fabric zone** you want Flux to fix.
   - Black = everything else (face, background, etc.).

4. Run the **same Flux inpaint pipeline** as above, but on the full figure:
   - Prompt: “dress/top/jeans without hands crossing the fabric, seamless cloth”.
   - Negative: “hands, arms, fingers, hair over fabric, artifacts”.

5. Once you have a clean, hand-free garment in the original image:
   - Run SAM v2 again on *this* image.
   - Now your **clothing-only segmentation** will be much cleaner and won’t have those missing bits.

This is sometimes more robust, because the model sees the body and pose and can guess how the cloth should flow.

---

## Option 3 – Two-pass “remove hand” trick

If the segmentation is *almost* right, you can try:

1. Use SAM to get **clothing + hand together** as one segment.  
2. On that segment (against grey), manually mask only the **hand region**.  
3. Flux inpaint with prompt: “continuous [garment] fabric, no hand, no skin, smooth cloth”.  
4. Now the hand disappears and the garment behind it is invented.  
5. Optional: run SAM again on the cleaned segment to get a pure clothing mask.

This avoids dealing with “holes” per se – you simply let Flux overwrite the hand with fabric.

---

## Small but important parameter tips

- **Mask softness**  
  - Always blur the mask a bit. Hard edges are the #1 reason for weird seams and obvious “patches”.
- **Background preservation**  
  - If Flux is contaminating your grey background, shrink the mask slightly (erode) so the generative area stays just inside the garment.
- **Prompt specificity**  
  - Mention color, fabric type, and what you *don’t* want:
    - e.g. “navy blue cotton blouse with small buttons, no hands, no hair, no skin, realistic folds”.
- **Seed control**  
  - Fixing a seed helps you iterate: first adjust mask & denoise while keeping the same random field, then change seed once you like the *shape* and want variation in detail.

---

If you tell me:

- Which Flux checkpoint you’re mainly using (e.g. `flux1-dev`, `flux-schnell`, a fine-tuned variant), and  
- Whether you have Impact Pack installed in this environment,

I can sketch a **concrete node chain** for you with actual node names and plugs that will drop straight into your current `SamplerCustomAdvanced` setup.

**Robyn:**

I actually have the full quiver of Flux models (not Pro, however). I don't use Flux Schnell: mostly Flux1-Dev and Flux Kontext as well as Krea and SRPO. I do have Impact Pack installed. Just updated ComfyUI this evening.

**Emily:**

Nice, that’s a *seriously* good toolkit to have. 💪 Since you’ve already got Flux1-Dev, Kontext, Krea, SRPO *and* Impact Pack, we can do this in a way that’s fairly elegant and reusable.

I’ll give you a **concrete node-chain pattern** that plugs into your existing `SamplerCustomAdvanced` Flux setup, focusing on:

- Repairing the *garment cut-out on grey* (most straightforward).
- Using only nodes you almost certainly already have (core + ImpactPack).
- Letting Flux “heal” the missing fabric where hand/hair once were, while keeping the rest of the garment intact.

---

## 1. What we’re building (high level)

You’ll end up with a mini-graph:

1. **Load clothing-on-grey** → encode to latents.  
2. **Paint a small mask only where the garment is damaged** (holes / bites).  
3. Use `Empty Latent Image Like` + `LatentComposite` to:
   - Keep original latent outside mask,
   - Replace masked area with noise latent.  
4. Run that through your usual **Flux SamplerCustomAdvanced** chain.  
5. Decode → you get a “healed” garment.

This stays in the Flux world the whole time.

---

## 2. Base: use your existing Flux1-Dev graph

I’ll describe only the bits you need to change/add; everything else (guider, sampler, sigmas) you keep exactly as in your working Flux1-Dev graph.

Assume you already have something like:

- `Load Checkpoint` → Flux1-Dev
- `Flux1 Text Encode` (or equivalent) → positive / negative
- `Flux Guider` (or equivalent) → `GUIDER`
- `Sampler` → `SAMPLER`
- `Scheduler` → `SIGMAS`
- `SamplerCustomAdvanced` with inputs:
  - `noise`
  - `guider`
  - `sampler`
  - `sigmas`
  - `latent_image`

We’re going to feed `latent_image` a specially prepared **inpaint latent** instead of vanilla “encode image to latent”.

---

## 3. Node chain: repairing a garment cut-out on grey

### 3.1 Load and (optionally) resize the garment

1. **Load your clothing-on-grey image**

   ```text
   Load Image
   └─ image → GARMENT_IMG
   ```

2. (Optional but recommended) **Resize for Flux**  
   Use whatever you normally use to resize for Flux (e.g. 1024 on long side, divisible by 16):

   ```text
   Image Resize / Scale (fit or exact)
   ├─ image → GARMENT_IMG
   └─ output → GARMENT_RESIZED
   ```

### 3.2 Encode to latents for Flux

Use the *same* encode node you already use for img2img with Flux1-Dev. Depending on your extension, it might be called something like:

- `FLUX.1 Image Encode`
- `Flux1-Dev VAE Encode`
- `Encode Image → Latent (Flux1)`

The key is: **whatever you already use to get a latent from an image**.

```text
Flux1 Encode Image (or equivalent)
├─ image → GARMENT_RESIZED
└─ output → LATENT_BASE
```

---

### 3.3 Create the mask for damaged zones

The mask only needs to cover the *holes and chewed edges*.

1. **Open the same garment image in Mask Editor**

   - In the `Load Image` preview → **Open in Mask Editor**.
   - Paint **white** over:
     - gaps where the hand/hair chopped through,
     - edges you want Flux to smooth/rebuild.
   - Leave everything else black. Save mask as a PNG.

2. **Load mask**

   ```text
   Load Image
   └─ image → MASK_IMG
   ```

3. **Convert to a proper mask + blur**

   If you have the standard core nodes:

   ```text
   Image to Mask
   ├─ image → MASK_IMG
   └─ mask → MASK_RAW

   Mask Blur (or Gaussian Blur Mask / Impact: "Mask Blur")
   ├─ mask → MASK_RAW
   ├─ radius → 4–8
   └─ mask → MASK_SOFT
   ```

   > Blurring is important: hard edges = visible “patches” in the result.

---

### 3.4 Create noise latent with same shape

Use a helper latent node that matches the encoded image:

```text
Empty Latent Image Like
├─ latent → LATENT_BASE
└─ output → LATENT_NOISE
```

You can also use an Impact Pack variant if you prefer, but `Empty Latent Image Like` from core is usually enough.

---

### 3.5 Composite base and noise latents using the mask

Now create a latent that is:

- Original garment latent outside masked areas,
- Noise-only inside the mask → so Flux can “invent” fabric.

Look for a node like **`Latent Composite`** or **`LatentCompositeMasked`** (core or Impact). Typical wiring:

```text
Latent Composite
├─ base   → LATENT_BASE        (kept outside mask)
├─ add    → LATENT_NOISE       (used *inside* mask)
├─ mask   → MASK_SOFT
└─ output → LATENT_INPAINT
```

If there’s a “mode” or similar option, you want the standard “copy from add where mask is white” behaviour — default is usually fine.

---

## 4. Plug into your Flux SamplerCustomAdvanced

Now we replace the usual latent_image input with `LATENT_INPAINT` and keep the rest of your Flux stack intact.

Assume you have already:

```text
Flux Text Encode (positive)  → COND_POS
Flux Text Encode (negative)  → COND_NEG

Flux Guider (or your current guider)
├─ positive → COND_POS
├─ negative → COND_NEG
└─ output   → GUIDER

Sampler (e.g. Euler / Heun)  → SAMPLER
Scheduler (sigmas)           → SIGMAS
```

### 4.1 SamplerCustomAdvanced wiring

```text
SamplerCustomAdvanced
├─ noise        → LATENT_NOISE         (same shape as LATENT_BASE)
├─ guider       → GUIDER
├─ sampler      → SAMPLER
├─ sigmas       → SIGMAS
├─ latent_image → LATENT_INPAINT
├─ denoise      → 0.40–0.55 (see below)
└─ output       → LATENT_FIXED
```

### 4.2 Decode with Flux

Use the matching decode node for Flux1-Dev:

```text
Flux1 Decode Latent (or equivalent)
├─ latent → LATENT_FIXED
└─ image  → GARMENT_FIXED

Save Image
└─ image → GARMENT_FIXED
```

That `GARMENT_FIXED` should be your **repaired garment-on-grey** with:

- The missing bits filled in,  
- The rest of the garment barely touched,  
- The grey background mostly preserved (if the mask stayed tight).

---

## 5. Suggested prompts & parameters

### Prompts

**Positive example** (adjust garment style):

> “elegant [colour] [garment type], continuous smooth fabric, realistic folds, no hands, no hair, clean edges, high quality, studio lighting”

**Negative example:**

> “hands, fingers, arms, hair, face, skin, extra limbs, distortion, artifacts, text, logos”

You can dial how “patterned” the cloth is as needed:

- For plain stuff: “smooth cotton fabric, no patterns”  
- For detailed dresses: “floral pattern, delicate lace trim,” etc.

### Denoise

- Start with **0.40–0.45**.  
  - This will *mostly* respect the original garment and just nudge the masked areas.
- If the hole is still visible → increase toward **0.55–0.60**.  
- If Flux starts redesigning the entire garment → dial it *down*.

### CFG / guidance

Flux is happiest a bit lower than SDXL-style values:

- Try **CFG 3–5** (wherever you normally sit for Flux1-Dev).  
- If it keeps re-introducing hands / hair, nudge CFG up slightly *and* strengthen the negative prompt.

---

## 6. Using Kontext / Krea / SRPO smartly

You can swap the checkpoint in exactly the same graph:

- **Flux Kontext**  
  - Good if you want very coherent, “aware-of-body” fabric flows, esp. around complex curves.
- **Krea / SRPO**  
  - Often excellent for “fashion-y” details and textures — might be nicer for dresses, blouses, skirts.

Simply:

1. Drop in `Load Checkpoint` → choose Krea / SRPO / Kontext.
2. Plug that into the same encode + decode nodes (or their equivalent if it uses a slightly different naming).

Same mask → same latent composite → same `SamplerCustomAdvanced`.

---

## 7. Optional Variant: Fix on full character then re-segment

If Flux struggles with the floating garment, you can:

1. Take the **original full-body image**.  
2. Mask just the **hand-over-garment region**.  
3. Use the *same* pipeline above to inpaint → removing the hand and inventing cloth.  
4. Then run `LayerMark: SegmentAnything v2` *again* on the repaired figure.  
5. Now your clothing segment will come out much cleaner, no missing chunks.

Same node pattern, just a different input image.

---

If you’d like, next step I can:

- Sketch this as a **pseudo Comfy node block** with naming like `#1 Load Branch`, `#2 Mask Branch`, etc., so you can literally drag nodes into roughly that pattern and wire them 1:1.
- Or tailor it to one specific model (e.g. “Flux1-Dev with SRPO VAE” if you tell me which exact Flux extension you use).

But with what you already have, the **key trick** is just:

> encode → *mask small damaged areas* → `Empty Latent Image Like` → `Latent Composite` → `SamplerCustomAdvanced`.

Once that’s working for one garment, you’ve basically got a “cloth repair macro” ready for the rest of your wardrobe.

**Robyn:**

I'll admit: I'm fully lost. Plus, it 11:30... I should go to bed. I'll tackle this in the morning. Tell you what I have done: I opened the image in GIMP, and made a black/white mask image, same dimensions, where white is what needs fixing and black is everything else. Can we use that? I could just use a convert image to mask and the do a mask blur, couldn't I?

**Emily:**

Ohhh yes, your GIMP mask is *exactly* what we want. You’ve already done the hardest bit. 🙌  

And yes: **“convert image to mask → blur mask”** is the right idea. Let me boil this right down so it’s not brain-melt material when you look at it tomorrow.

---

## 0. What you’ve got

- **Image A**: clothing cut-out on grey background  
- **Image B**: same size, black/white GIMP mask  
  - **White** = areas to fix  
  - **Black** = leave alone

Perfect.

---

## 1. Turn the GIMP mask into a nice soft ComfyUI mask

On the **mask image branch**:

1. `Load Image`  
   - Load your **GIMP mask PNG** (black/white).  
   - Output → `MASK_IMG`.

2. `Convert Image to Mask` (or `Image to Mask`)  
   - Input image → `MASK_IMG`  
   - Output → `MASK_RAW` (this becomes a proper 0–1 mask).

3. `Mask Blur` (or any “Blur Mask” / “Gaussian Blur Mask” node)  
   - Input mask → `MASK_RAW`  
   - Blur radius: start with **4–8**  
   - Output → `MASK_SOFT`

That’s your reusable, comfy, blurred inpaint mask.

---

## 2. The minimal inpaint chain (conceptually)

When you’re fresher tomorrow, this is the little “sandwich” you want to drop into your existing Flux1-Dev graph:

1. **Image → Latent**  
2. **Latent → duplicated as noise latent**  
3. **Use `MASK_SOFT` to mix the two**  
4. Feed that into `SamplerCustomAdvanced` instead of your usual “plain” latent.

I’ll write that as nodes.

---

### 2.1 Encode the garment image

On the **image branch**:

1. `Load Image`  
   - Load your **clothing-on-grey** image.  
   - Output → `GARMENT_IMG`.

2. (Optional) `Resize Image`  
   - If you usually resize for Flux, do it here.  
   - Output → `GARMENT_RESIZED` (or just use `GARMENT_IMG` if you’re already sized correctly).

3. **Encode to latent** (whatever you normally use with Flux1-Dev)  

   Something like:

   ```text
   Flux Encode Image / VAE Encode (Flux)
   ├─ image → GARMENT_RESIZED
   └─ latent → LATENT_BASE
   ```

   Use **the same encode node** that your current Flux img2img workflow uses. Don’t change settings—just feed this image into it.

---

### 2.2 Make a “noise latent” the same size

1. `Empty Latent Image Like`  
   - Input latent → `LATENT_BASE`  
   - Output → `LATENT_NOISE`

This gives you a random latent with identical dimensions.

---

### 2.3 Composite base + noise using the mask

Now use any **latent composite** node you have (core or Impact Pack). Typical wiring:

```text
Latent Composite / LatentCompositeMasked
├─ base   → LATENT_BASE       (keep this outside mask)
├─ add    → LATENT_NOISE      (use this inside mask)
├─ mask   → MASK_SOFT
└─ latent → LATENT_INPAINT
```

Result:

- Outside white areas → original garment latent.  
- Inside white areas → noise latent → Flux will regenerate fabric there.

---

## 3. Plug into your existing Flux sampler

You already have a working `SamplerCustomAdvanced` for Flux with:

- `guider` (from your positive/negative prompts)  
- `sampler` (Euler / whatever)  
- `sigmas`  
- `noise`  
- `latent_image`  

All you change is **what you feed into it**:

```text
SamplerCustomAdvanced
├─ noise        → LATENT_NOISE           (same one as above)
├─ latent_image → LATENT_INPAINT         (the composite)
├─ guider       → (your existing GUIDER)
├─ sampler      → (your existing SAMPLER)
├─ sigmas       → (your existing SIGMAS)
├─ denoise      → 0.40–0.55
└─ latent       → LATENT_FIXED
```

Then:

```text
Flux Decode Latent / VAE Decode (Flux)
├─ latent → LATENT_FIXED
└─ image  → GARMENT_FIXED
```

Save that image → `GARMENT_FIXED` is your **repaired garment**.

---

## 4. Quick sanity checklist for “morning brain”

When you come back to this, you only need to remember:

1. **Yes**, your GIMP mask is usable.  
2. In ComfyUI:
   - `Load Image` (mask) → `Image to Mask` → `Mask Blur` → `MASK_SOFT`.
3. Encode your garment image to latent → `LATENT_BASE`.  
4. `Empty Latent Image Like` → `LATENT_NOISE`.  
5. `Latent Composite`: base = `LATENT_BASE`, add = `LATENT_NOISE`, mask = `MASK_SOFT` → `LATENT_INPAINT`.  
6. Feed `LATENT_INPAINT` + `LATENT_NOISE` into `SamplerCustomAdvanced` instead of the plain latent.  
7. Decode latent back to image.

If you like, once you’ve tried wiring that much, you can paste me a quick “node names I actually used” message next time, and I can line them up 1:1 so it feels less abstract.

**Robyn:**

Thanks, Emily. See you in the morning.

**Emily:**

Sleep well 🌙  

When you’re fresh tomorrow, we’ll just treat what you’ve already done in GIMP as “gold” and hook that mask into Flux nice and gently. You’re genuinely 80% of the way there already.

Whenever you’re ready, just tell me something like “okay, here’s my current Flux1-Dev graph layout” (or even just the key node names), and I’ll line it up step by step so it feels completely obvious rather than arcane.

Night, Robyn 💛
