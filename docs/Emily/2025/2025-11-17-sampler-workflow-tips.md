---
title: "Sampler workflow tips"
date: 2025-11-17
---

# Sampler workflow tips

**Robyn:**

Hi Emily. I was just wondering if you had a breakdown of current image models (Flux.1 Dev / Kontext / SRPO / Qwen) and which samplers and schedulers work best for the different models?

**tool:**

【turn0calculator0】 1+1 = 2

**Emily:**

Short version:  
- **Flux.1 Dev / Kontext / SRPO** all behave like “Flux” models → they like **low CFG (1.0)**, **no negative prompt**, and **Euler-family or DPM++ 2M samplers**.  
- **Qwen-Image** is very similar (DiT + flow matching) but with its own sweet spots: **few steps, low CFG, and either Euler or res_multistep**. citeturn0search25turn2view0turn4view0  

Below is a breakdown by model, with **ComfyUI-style presets** you can drop straight into KSampler / SamplerCustom.

---

## 1. FLUX.1 Dev – general text-to-image

**What it is**  
Flux.1 [dev] is the open-weights “base” model from Black Forest Labs, trained with flow-matching / rectified flow; CFG is effectively baked into the distillation process. citeturn4view0turn0search25  

**Key quirks**

- **CFG scale ≈ 1.0** (this is *not* SDXL – high CFG just wrecks it). citeturn4view0  
- No true negative prompt; you steer by re-phrasing the *positive* prompt. citeturn4view0  
- You normally get best results around **20–30 steps**. citeturn4view0  

### Recommended samplers / schedulers (what people actually use)

From Forge / SD.Next docs and community testing:  

- **Euler (a/normal) + Simple/Normal scheduler** is a very solid default; this is also what the Forge “Flux” preset uses. citeturn4view0turn7search1  
- A lot of ComfyUI folks report **Euler + Beta scheduler** (or “Euler beta”) giving slightly better edges/details at similar speed. citeturn0search7turn5search6  
- For “classic” diffusion workflow, **DPM++ 2M (or DPMPP_2M_SDE) + Karras** is a great quality preset; a ComfyUI tips article explicitly calls out DPM++ 2M Karras as the go-to quality sampler. citeturn5search9  

### Concrete ComfyUI presets

**Flux.1 Dev – “Safe default” (portraits / general work)**  
- **Sampler**: `euler` (or `Samueler (Euler)` equivalent in SamplerCustom)  
- **Scheduler**: `simple` or `normal`  
- **Steps**: 24–28  
- **CFG**: `1.0`  
- **FluxGuidance / Distilled CFG scale**: `3.0–3.8` for photorealism, `4.5–5.5` for stylised / illustration. citeturn4view0  
- **Denoise**: `1.0` for pure txt2img  

**Flux.1 Dev – “High detail” (slower, sharper)**  
- **Sampler**: `dpmpp_2m_sde`  
- **Scheduler**: `karras`  
- **Steps**: 28–32  
- **CFG**: `1.0`  
- **FluxGuidance**: `3.0–4.0`  

**Flux.1 Dev – “Fast draft”**  
- **Sampler**: `euler`  
- **Scheduler**: `simple`  
- **Steps**: 16–18  
- **CFG**: `1.0`  
- **FluxGuidance**: `2.5–3.0`  

---

## 2. FLUX.1 Kontext Dev – image editing specialist

**What it is**  
Kontext is an image+text editing model: you give it an input image and an instruction (“change the car to red, keep composition and person identical”) and it does targeted edits. citeturn0search23turn3view1  

Architecturally it’s still Flux1-ish, so **the same sampler logic applies** – it’s just optimised for *lower denoise* image-to-image.

**Official / community hints**

- Comfy / Forge guides treat it like other Flux models: **Euler + Simple** is the “reliable baseline”. citeturn7search3turn4view0  
- BFL’s preferred resolutions list still applies (832×1248, 1024×1024, 1184×880, 1216×832, etc.). citeturn7search3  

### Editing-oriented presets (ComfyUI I2I)

**Kontext – “Targeted edit” (small changes, maximum character stability)**  
- **Sampler**: `euler`  
- **Scheduler**: `simple`  
- **Steps**: 16–22  
- **CFG**: `1.0`  
- **FluxGuidance**: `2.5–3.5`  
- **Denoise**: `0.25–0.45`  
  - 0.25 if you only want colour / lighting tweaks  
  - 0.35–0.45 for swapping backgrounds, clothes, etc.  

**Kontext – “Heavier rework” (same person, new setting / wardrobe)**  
- **Sampler**: `dpmpp_2m_sde`  
- **Scheduler**: `karras`  
- **Steps**: 22–26  
- **CFG**: `1.0`  
- **FluxGuidance**: `3.5–4.5`  
- **Denoise**: `0.45–0.6`  

Practical rule of thumb:  
- If a face is drifting, **lower denoise** *before* you raise steps.  
- If changes are too timid, bump **FluxGuidance** slightly rather than CFG.

---

## 3. FLUX.1 SRPO – Tencent’s preference-tuned Flux

**What it is**  
SRPO isn’t a new architecture; it’s Flux.1-Dev fine-tuned with Tencent’s **Semantic-Relative Preference Optimisation** – essentially RL on human preference across the whole diffusion / flow trajectory. citeturn5search2turn5search10turn5search16  

So, inference-wise it behaves like Flux.1 Dev with slightly different “taste”: more natural skin, fewer plastic-looking artifacts, especially on faces. citeturn5search6turn5search26  

**Sampler behaviour from early tests**

- Users report **Euler (normal) works well**, just like base Flux. citeturn5search6turn5search11  
- Some of the “it looks better” anecdotes came from **Euler + beta scheduler**, not from SRPO itself – i.e. scheduler choice still matters a lot. citeturn5search6turn0search7  

### Suggested ComfyUI presets

You can almost drop in your Flux.1 Dev settings and just lean a bit into realism:

**SRPO – “Realistic portraits”**  
- **Sampler**: `euler`  
- **Scheduler**: `beta` (or `simple` if you don’t want to fuss)  
- **Steps**: 24–30  
- **CFG**: `1.0`  
- **FluxGuidance**: `2.8–3.5` (keep slightly lower than your illustration work)  
- **Resolution**: stay near BFL-friendly sizes (e.g. 1216×832 or 1184×880)  

**SRPO – “Max quality, still portraits / fashion”**  
- **Sampler**: `dpmpp_2m_sde`  
- **Scheduler**: `karras`  
- **Steps**: 26–32  
- **CFG**: `1.0`  
- **FluxGuidance**: `3.0–3.8`  

If it starts to look *too* crunchy or noisy:  
- Drop **FluxGuidance** before you touch steps.  
- If grain persists, try `euler` + `simple` instead of DPM++.

---

## 4. Qwen-Image – DiT-style, text-savvy foundation model

**What it is**  
Qwen-Image is Alibaba’s 20B-parameter multimodal DiT diffusion model; open-sourced and meant as a general foundation model with strong multilingual text rendering and editing. citeturn1view0turn2view0  

Comfy’s official guide distinguishes:  

- **Original fp8/bf16 model** – heavier, more steps.  
- **Distilled model** – fewer steps, slightly lower fidelity.  
- **Lightning LoRA (8-step)** – very fast, requires specific sampler config. citeturn1view0turn2view0  

The docs explicitly recommend:  

- **Distilled Qwen-Image**: ~**15 steps**, **CFG 1.0**, works well even at 10 steps with CFG 1.0.  
- For the distilled version, **Euler or res_multistep** are recommended samplers depending on the image type. citeturn2view0  

There’s also a lot of community testing that leans on Euler + normal / Karras, similar to Flux. citeturn5search1turn5search9  

### ComfyUI presets

**Qwen-Image Distilled – “Official-ish” settings**  
(from the ComfyUI wiki notes) citeturn2view0  

- **Sampler**: `euler` *or* `res_multistep`  
- **Scheduler**:  
  - with `euler`: `normal` or `karras`  
  - with `res_multistep`: use the matching multistep scheduler node if you have it; otherwise `karras` is fine  
- **Steps**:  
  - **15** (author-recommended)  
  - **10** if you’re using it like a “lightning” model  
- **CFG**: `1.0`  

**Qwen-Image Full fp8 – “Quality” preset**  

- **Sampler**: `dpmpp_2m_sde`  
- **Scheduler**: `karras`  
- **Steps**: 20–24  
- **CFG**: `1.0–1.3` (you *can* push a tad above 1 here; it’s less fragile than Flux, but still hates SDXL-style 7–12 CFG)  
- For tight text (signage, posters): lean `euler + karras, 18–20 steps`, still at **CFG 1.0**.  

**Qwen-Image + Lightning 8-step LoRA**  

- Enable the Lightning LoRA (`Qwen-Image-Lightning-8steps-V1.0`) and: citeturn2view0  
  - **Steps**: `8`  
  - **Sampler**: `euler`  
  - **Scheduler**: `karras`  
  - **CFG**: `1.0`  

---

## 5. How I’d pick between them in practice

Given your setup (ComfyUI, 4060 Ti 16GB, character-focused work):

- **Character portraits / realistic women**  
  - Start with **Flux.1 SRPO**, `euler + beta`, 24–28 steps, CFG 1.0, FluxGuidance ~3.2.  
  - If it feels “too Flux-pretty” / plastic, nudge guidance *down* a bit rather than up.  

- **Multi-lingual text on images (posters, covers, signage)**  
  - **Qwen-Image (distilled)**, `euler + karras`, 15 steps, CFG 1.0. It’s simply better at text layout. citeturn2view0  

- **Complex edit chains on a favourite render** (hair, setting, outfit swaps while keeping “your girl” consistent)  
  - **Flux.1 Kontext**, denoise 0.3–0.45, `euler + simple`, 18–22 steps.  

- **Weird stylised / painterly stuff**  
  - Either **Flux.1 Dev** or **Qwen-Image fp8** with `dpmpp_2m_sde + karras`, slightly higher FluxGuidance (4–5) or CFG (1.2–1.4 for Qwen).  

---

If you like, next step I can sketch **a tiny SamplerCustomAdvanced “matrix” workflow** for you: one input model (say SRPO) feeding three or four parallel sampler/scheduler combos so you can eyeball differences on your favourite test prompt in one go.

**Robyn:**

This is EPIC. Thank you, Emmily - once again, you're a legend!

**Emily:**

You’re so sweet, thank you 🥹  
I’m really glad that helped make sense of the sampler soup.

One tiny pro tip while you’re experimenting with Flux/Qwen flavours:

- Pick **one “benchmark girl” prompt** (the sort you *actually* use for your work).
- Render a **2×2 or 3×2 grid** where *only* the sampler/scheduler combo changes:
  - Row 1: `euler + simple`, `euler + beta`, `dpmpp_2m_sde + karras`
  - Row 2: same combos but with guidance nudged (e.g. 3.0 vs 3.8 on Flux)
- Save your favourites with the settings in the filename, e.g.  
  `SRPO_portrait_euler-beta_26steps_g3.2.png`

Within a couple of evenings you’ll have **your own personal “house recipes”** for Flux/SRPO/Qwen that you can just reuse forever and only tweak for special cases.

And if you ever want, I can lay out a **mini ComfyUI sampler bake-off workflow** for you (one prompt in, multiple samplers out) so you don’t have to wire it from scratch.

**Robyn:**

Actually, what I could really use is a workflow for Kontext... I want to create a costume image collection, where the image has purely the costume in it. If I sent you the workflow, could you identify why it is not obeying my prompts? The prompt is a simple one: "Remove the woman from the image" I also tried "remove the woman", "Remove the person", etc. I can't use a negative prompt as Flux doesn't support that. May I send you my workflow?

**Emily:**

Ohhh, *that* is a fun use for Kontext 😈—a wardrobe archive without the inconvenient human attached.

Yes, absolutely, you can send me your workflow.  
If you paste the JSON (or a screenshot plus node list), I can walk through:

- where the **input image** goes,  
- how the **instruction text** is wired,  
- which node is actually doing the Kontext call,  
- and whether **denoise / guidance / masks** are sabotaging your “remove the woman” request.

Since you haven’t pasted it yet, let me give you some likely culprits up-front so you can already sanity-check your graph:

---

## 1. How Kontext thinks about “remove the person”

Kontext is *much* happier with instructions like:

- “Make the woman disappear and show only the dress on a white background.”
- “Remove the woman and leave only the costume on a mannequin, plain studio white background.”
- “Replace the woman with empty space; keep only the clothes on a white backdrop.”

Purely negative commands like **“remove the woman”** can be too vague:

- What should go *in her place*?  
- Do we keep the clothes floating? Replace with background? Mannequin? Floor?

So: **always tell it what the final image should look like**, not just what to delete.

---

## 2. Denoise: the #1 reason edits don’t “take”

For Kontext in ComfyUI, if you’re doing image-to-image:

- **Denoise too low (≤0.25)** → the model barely touches the image; your woman stays.  
- **Good range for removal / strong edit**: `0.45–0.65`  
  - 0.45–0.5 → medium change (pose/wardrobe tweaks).  
  - 0.55–0.65 → aggressive change (remove subject, change background, etc.).

So if your current chain is something like:

> Kontext → SamplerCustomAdvanced → VAE Decode  

check what **Denoise** value you’re feeding into the sampler. If it’s 0.2-ish, Kontext is obeying you but the sampler simply won’t let it overwrite the base image.

---

## 3. Guidance: Flux-style low, but not *too* low

Because Kontext is Flux-based:

- **CFG scale in the sampler** should be around `1.0`  
- Any extra “Flux guidance” / “Edit guidance” scale:
  - Try starting at `3.0–3.5`  
  - If the woman isn’t removed enough → nudge that to `4.0–4.5`  
  - If things go chaos / weird → back it down again

If you’re using one of those combined “Flux denoiser / guider” nodes, I’ll need to see which slots you’re filling, but the rule of thumb is:

> Don’t crank CFG like SDXL; **keep it low and move the model-specific guidance instead**.

---

## 4. Masking vs. global edit

Depending how your workflow is built:

- If you **don’t use a mask**, Kontext has to reinterpret the *whole* image. That can work, but it may only *soften* the person instead of truly removing them.
- A stronger pattern for “remove the woman, keep costume” is:
  1) Use a segmentation / manual mask that covers **the body and head** but *not* the clothes you want to preserve.  
  2) Run **only that region** through Kontext with something like:
     > “Remove the woman’s body and leave only the clothes, on a plain white background.”
  3) Composite back into original or onto a fresh background.

If your graph sends the **entire image + no mask** into Kontext with a vague instruction, it’ll often lean toward “style shift” rather than truly deleting the person.

---

## 5. Prompt style that usually works better for this

When you send your workflow, I’ll adapt this precisely, but you can already try:

> **Instruction / positive prompt** (Kontext text input):  
> “Remove the woman’s body and face and leave only her clothes, as if they are neatly arranged on a mannequin, on a clean white studio background. The costume should be fully visible, no human skin, no head, no hands or feet.”

And avoid using **negative text** (“no woman, no person, no head”)—Flux-style models don’t really use a true negative prompt channel.

---

If you paste your workflow next, I’ll go node-by-node and tell you:

- which node should handle the Kontext call,  
- whether the **connections** are right,  
- where to set **denoise / guidance**,  
- and how to tweak the prompt so the poor woman actually vanishes and leaves you a tidy costume shot.

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**tool:**

【turn0calculator0】 1+1 = 2

**Emily:**

Ohhh nice, thank you for the JSON, that makes things much clearer. 🧵  
Short version: your workflow is basically *correct* for Kontext Dev – it’s very close to the official Comfy template – but a few details make your “remove the woman” request *easy to ignore*:

1. The way Kontext wants instructions phrased.  
2. Denoise / guidance / sampler settings.  
3. The fact you’re asking for *removal* without telling it what the *new* state should be.

Let me walk through what you’ve got and then give you a “do this next” checklist.

---

## 1. What your workflow is doing now

Key nodes in your graph:

- **UNETLoader (200)** – loads `flux1-dev-kontext_fp8_scaled.safetensors` ✅  
- **DualCLIPLoader (209)** – loads `t5xxl_fp8...` + `clip_l.safetensors` ✅  
- **VAELoader (201)** – loads `ae.safetensors` ✅  
- **LoadImage (195)** → **ImageScaleToTotalPixels (202)** → **ImageSizeDetector (203)** → **EmptySD3LatentImage (214)**  
  - That creates an *empty latent* at the input image’s size – this is the standard Flux/Komtext pattern. citeturn3view0  
- **VAEEncode (206)** encodes the original image → **ReferenceLatent (210)** combines:
  - the encoded latent, and  
  - your **CLIPTextEncode (215)** (“Remove the woman from the image…”)  
- **FluxGuidance (211)** adds a guidance scale (`2.8`) to the conditioning and sends that as **positive** into:  
- **KSampler (212)** with:
  - sampler: `euler`  
  - scheduler: `ddim_uniform`  
  - steps: `30`  
  - cfg: `1`  
  - denoise: `1`  

You’re also doing a neat trick:

- **ConditioningZeroOut (213)** takes the *same* text encoding from (215), zeroes it, and feeds that into **KSampler negative** – so the “negative” input is effectively neutral. 👍

So structurally: **this is a legit Kontext Dev editing workflow**, very similar to the official Comfy one. citeturn3view0  
The problem isn’t wiring – it’s *how hard the model is allowed to move away*, and *what you’re actually asking it to do*.

---

## 2. Why “Remove the woman” isn’t landing

Kontext is tuned around prompts like (from the Comfy docs): citeturn3view0turn4view0  

- “Change the car color to red.”  
- “Change the background to a beach while keeping the person in the exact same position and pose.”  
- “Change the clothes to be a viking warrior while preserving facial features.”

Notice the pattern:

> **Change [thing] to [new state], keep [other thing] unchanged.**

Your current prompt:

> “Remove the woman from the image. Preserve the dress exactly. No woman is in the image.”

To a model that’s *designed* to preserve structure and characters, that’s very vague:

- Remove her *how*? Replace with background? With nothing? With a mannequin?  
- Should the dress still be on a body, or floating, or laid out on a flat surface?  
- “No woman is in the image” is a semantic negative, but Kontext doesn’t have a separate “negative prompt” channel to lean on – it just sees that as more abstract text to juggle. citeturn3view0turn4view0  

So what it tends to do is:  
**“Okay, the main subject is a woman-in-dress → that must stay** (because preservation is a first-class goal), but maybe I’ll tweak lighting, pose, style a bit.”

For real object removal, people have found you need to be *extremely explicit* about what the final image should look like. citeturn4view0  

---

## 3. Concrete changes I’d make to your workflow

### (A) Fix the sampler + scheduler combo

Right now, KSampler is:

- **sampler_name**: `euler`  
- **scheduler**: `ddim_uniform`  

For Flux/Komtext, the comfy docs and community tests consistently lean on: citeturn3view0turn4view0  

- `euler` + **simple** (most common)  
- or `euler` + **karras`** for a bit more “quality” feel.

**Change in node 212 (KSampler):**

- `sampler_name`: keep `euler`  
- `scheduler`: change from `ddim_uniform` → **`simple`**  

Leave **steps = 30, cfg = 1** for now.

---

### (B) Adjust denoise & FluxGuidance for a *big* edit

For Kontext, the denoise value is the *edit strength*:

- Too low (≲0.25) → barely touches the image.  
- Too high (1.0) → it wants to redraw everything, but the reference latent still pulls the subject back in.

You currently have **denoise = 1**. That’s full redraw, which can actually *hurt* object-removal, because the model keeps trying to “recreate a nice-looking photo of a woman in a dress” instead of obeying the instruction.

**In node 212 (KSampler):**

- Set **denoise** to **`0.55`** to start.  
  - If the woman is still too present → try **0.65**.  
  - If the costume starts changing shape too much → drop toward **0.45**.

In **FluxGuidance (211)**:

- Right now guidance = `2.8`.  
- For a major structural edit, bump this slightly so the text can overpower the original image a bit:

  - Try **`3.8`**.  
  - If it still clings too hard to the figure, go to **`4.2`**.  
  - If things get chaotic or the dress warps, back down toward `3.2–3.5`.

---

### (C) Rewrite the prompt in Kontext’s preferred pattern

Let’s aim explicitly at “wardrobe archive shot”:

In **CLIP Text Encode (215)**, replace your text with something like:

> **“Change the woman’s body into an invisible mannequin wearing the same dress.  
> Show only the dress clearly, on a plain white studio background.  
> Keep the dress design, colours and folds exactly the same.  
> No human skin, no face or hair, no hands or feet.”**

Why this works better:

- **“Change [X] into [Y]”** – explicit before/after.  
- “Invisible mannequin wearing the same dress” gives it a *concrete* stand-in for the human.  
- “Plain white studio background” tells it what to put behind the dress instead of guessing.  
- “No human skin, no face or hair, no hands or feet” is a backup clause, but we’ve already told it what *to* render, which matters more.

If you want the dress to be *off* the body entirely (laying flat / hung up):

> “Change the woman into an invisible hanger and show only the dress hanging neatly on a white studio background, no human body at all. Keep the dress design, colours and folds exactly the same, no skin, no head, no arms or legs.”

That aligns *perfectly* with the Comfy docs advice: object modification is “Change object to new state, keep content to preserve unchanged.” citeturn3view0  

---

## 4. Optional: masking for cleaner removal

Your current workflow uses **no mask** – Kontext is editing the *entire* image at once. That can work, but if the dress is large and the woman’s skin is relatively small, the model may just keep redrawing her.

If you’re up for one extra step, you can tighten it with a simple mask:

1. Use **LoadImage → Mask Editor** (or paint in GIMP) to create a mask that covers:
   - the **head, neck, arms, legs**, but  
   - *not* the dress itself.
2. Feed that mask into a **Masked KSampler** (or use your current KSampler with a mask input if you swap node type).
3. Keep the same prompt as above – now Kontext only has permission to rewrite the masked body parts, leaving the dress pixels intact.

That’s the “surgical” version; I’d still test the **unmasked** version first with the prompt + denoise/guidance changes, because Kontext really is quite good at object removal when the text is clear. citeturn4view0  

---

## 5. Tiny clean-up

You’ve also got a **LoadImageOutput (147)** at the top that isn’t wired into anything. It’s harmless, but you can safely delete it to avoid confusion – you’re already using **LoadImage (195)** for the real input.

---

## TL;DR: the exact edits to try first

1. **KSampler (212):**
   - `scheduler`: `simple` (keep `euler` as sampler)  
   - `denoise`: `0.55` (tune 0.45–0.65 as needed)  
   - keep `steps = 30`, `cfg = 1`

2. **FluxGuidance (211):**
   - `guidance`: from `2.8` → **`3.8`** to start.

3. **CLIP Text Encode (215) prompt:**

   ```text
   Change the woman’s body into an invisible mannequin wearing the same dress.
   Show only the dress clearly, on a plain white studio background.
   Keep the dress design, colours and folds exactly the same.
   No human skin, no face or hair, no hands or feet.
   ```

Run that on one of your outfit shots and see how she behaves. If she’s still clinging on stubbornly, tell me *exactly* how (ghost limbs? full body still there?) and we can nudge denoise / guidance or add a simple body-mask step to make her properly… surplus to requirements. 💅

**Robyn:**

So, my first run was: euler/simple; 30 steps; .55 denoise; 3.8 guidance.
I got a line drawing of the girl, the dress.
Second run was: euler/simple; 30 steps; .70 denoise; 3.8 guidance.
I got a line drawing of the girl, the dress, in greater detail.
Third run was: euler/simple; 30 steps; .80 denoise; 5.5 guidance.
I got a photograph of a dressmaker's mannequin on a black wooden stand; no girl, no dress.
Fourth run was: euler/simple; 30 steps; .80 denoise; 5.0 guidance.
I got a line drawing of the dress;  no girl.
Fourth run was: euler/simple; 30 steps; .85 denoise; 5.0 guidance.
I got a rather hallucinogenic, woodcut rendition of a dress, not that dress; no girl.
Fifth run was: euler/simple; 30 steps; .85 denoise; 4.8 guidance.
I got a Macy's mannequin on a stand wearing the dress, zoomed out.
I might try the mask approach. Which nodes do I use for that, please?

**Emily:**

This is *really* useful info, thank you — it tells us Kontext is listening, but it has too much freedom and not enough structure.

- The **line drawings** at lower guidance/denoise = it’s trying to “sketch” a new scene based on your instruction, but still anchored to the original.
- The **mannequin only / no dress** at 0.8 + 5.5 guidance = full redraw, instruction wins completely.
- The **Macy’s mannequin in the dress, zoomed out** = actually quite promising: it understood “invisible mannequin wearing the dress”, but it’s re-framing the scene.

So yes: time to put it on a leash with a mask.  

---

## Strategy: mask the *body* (skin), not the dress

For a wardrobe archive vibe, the simplest useful version is:

- **Keep the dress pixels mostly intact.**
- Only let Kontext rewrite **head, arms, legs, any exposed skin**, and optionally the immediate background.

So our mask will cover:  

- face, hair, neck, arms, legs, bare chest/shoulder skin;  
- *not* the dress itself.

Kontext then only gets to “paint over” the human bits, leaving the costume as close to original as possible.

---

## Nodes you can use (ComfyUI)

I’ll describe this in terms of **standard nodes** you already have:

- `Load Image` (you already use it)  
- `ImageScaleToTotalPixels` (you already use it)  
- **Mask Editor / Image Canvas** (from the image preview’s “Open in Mask Editor | Image Canvas”)  
- `VAE Encode` (in your graph)  
- `EmptySD3LatentImage` (in your graph)  
- **KSampler (Advanced)** or **KSampler (Inpaint)** (depending on what’s available)

You *don’t* strictly need fancy extra nodes; just a sampler that accepts a **mask** input.

---

## Step 1 – Create a body mask

Right now you have:

```text
LoadImage → ImageScaleToTotalPixels → (into VAEEncode etc.)
```

1. **On the preview of your scaled image**, right-click (or click the little wand) and choose  
   **“Open in Mask Editor | Image Canvas”**.  
   - This creates a new node (often called `ImageCanvas`) that has **image** and **mask** outputs.

2. In that mask editor:
   - Paint over **all skin**: face, neck, arms, legs, bare shoulders, etc.  
   - **Avoid painting over the dress** as much as practical.
   - Save/commit in the editor (so the mask gets stored in that node).

Now you have:

- `ImageCanvas` (or similar) with:
  - **image** → use this where you previously used the scaled image.
  - **mask** → we’ll feed this into the sampler.

So your chain becomes:

```text
LoadImage → ImageScaleToTotalPixels → ImageCanvas
                                          ├─ image → VAEEncode / ReferenceLatent etc.
                                          └─ mask  → KSampler mask input
```

---

## Step 2 – Swap your sampler to an inpaint-capable one

You’re currently using plain `KSampler` (no mask).

### Option A: If you have **KSampler (Inpaint)**

Many Comfy installs have `KSampler (Inpaint)` or something similar. If you do:

1. Replace your current `KSampler` node with **KSampler (Inpaint)**.
2. Wire it like this:

- `model` → your Kontext UNet  
- `positive` → output from `FluxGuidance`  
- `negative` → output from `ConditioningZeroOut`  
- `latent_image` → **VAEEncode( image from ImageCanvas )**  
- `noise` → Noise from `EmptySD3LatentImage` as before  
- `mask` → **mask** output from `ImageCanvas`  
- `steps` → 30  
- `sampler` → `euler`  
- `scheduler` → `simple`  
- `cfg` → 1.0  
- `denoise` → start with `0.6`

This tells the sampler: “Only denoise the masked region; leave unmasked (dress) alone.”

### Option B: If you only have **KSampler (Advanced)**

If you don’t see “Inpaint” but do have **KSampler (Advanced)** with `mask` and `latent_to` inputs:

1. Drop in **KSampler (Advanced)**.
2. Wire:

- `model` → Kontext UNet  
- `positive` → FluxGuidance output  
- `negative` → ConditioningZeroOut output  
- `latent_image` → **the latent you want to edit** (encoded original)  
- `noise` → from EmptySD3LatentImage  
- `mask` → mask from ImageCanvas  
- `latent_to` → **same encoded latent** (so it blends altered and original correctly)  
- steps/sampler/scheduler/cfg/denoise as above

You’re basically saying: *“Here’s the original latent; only change it inside this mask.”*

---

## Step 3 – Adjust the prompt for masked editing

Because we’re now only letting it touch the body, we can be very specific:

In your **CLIP Text Encode** node, try:

```text
Replace the woman’s head, hair, arms and legs with a plain white background.
Leave the dress exactly as it is.
Only remove all human skin, face, hair, hands and feet, keeping the whole dress visible.
```

Key point: because the **mask is already telling Kontext where the human is**, the text doesn’t need to fight the whole picture — it just needs to say *what to fill those masked areas with*.

If you prefer the mannequin look:

```text
Replace the woman’s body with an invisible mannequin wearing the same dress.
Keep the dress exactly as it is.
Remove all human skin, face, hair, hands and feet.
Fill the background where the body was with plain white studio background.
```

---

## Step 4 – Suggested starting values

In the inpaint sampler:

- **Steps**: 30  
- **Sampler**: `euler`  
- **Scheduler**: `simple`  
- **CFG**: 1.0  
- **Denoise**: start at **0.6**  
  - If you still see bits of skin / ghost limbs → 0.65–0.7  
  - If the dress starts melting or changing design → drop toward 0.5

In **FluxGuidance**:

- Start at **3.8**  
- If it’s still too shy about removing skin → push up to **4.2**  
- If things go weird / woodcutty again → ease back to **3.2–3.5**

---

## What results to expect

With this setup:

- The **dress** should stay very close to the original photograph.
- The **head / arms / legs** should dissolve into white (or into your mannequin idea) because they’re inside the mask.
- You should no longer get those full-frame hallucinations (Macy’s mannequins, different dresses), because Kontext is no longer allowed to rewrite the entire latent.

If you like, next time you can paste a quick screenshot of the nodes around the **ImageCanvas → mask → sampler** area, and I’ll sanity-check the wiring / suggest refinements so you end up with the kind of wardrobe-archive shots you actually need.

**Robyn:**

Emily, when I enter the MaskEditor, my mouse becomes hard to control. How do I fix that? It is slow to respond to my actions... almost impossible to work with.

**tool:**

【turn5calculator0】 1+1 = 2

**Emily:**

Yeah, that laggy brush is *infuriating* – you’re not imagining it. The Mask Editor can feel like painting through treacle, especially with big images and a 4K-ish display.

Here are the main ways to make it usable again, roughly in order of “quick wins”:

---

## 1. Shrink what you’re painting on

The Mask Editor is working at whatever resolution you fed it. If that’s 1024×1024 or 1216×832, it’s OK-ish; if it’s bigger, it can crawl.

- In your workflow, you already have **ImageScaleToTotalPixels**.  
- Make sure that’s set to something modest, e.g.  
  - `Total pixels`: around **0.7–1.0 MP** (e.g. 896×896-ish) instead of big 2–4 MP images.  
- Then open **that** scaled image in Mask Editor.

You can always do your *final* costume images at full-res later by:
- Making the mask at modest res,
- Then upscaling & re-running with the same mask (or upscaled mask).

---

## 2. Drop brush size while painting

The bigger the brush, the more pixels it has to update each stroke.

- In the Mask Editor UI, try:
  - Using a **smaller brush radius**, then
  - Zooming in on the area you’re masking (face, arms, legs).
- Do broad blocking with a middling brush, then clean edges with a small brush.  

Even halving the brush size can make the cursor feel way less “sticky”.

---

## 3. Check your browser / window zoom

If you’re running ComfyUI in a browser:

- **Zoom the page out** a bit (Ctrl/Cmd `-`) so the canvas isn’t massive.
- Avoid having the window maximised on a huge monitor while masking; a slightly smaller window can help.

Sometimes the browser is just struggling to redraw a huge canvas every frame.

---

## 4. Use an external editor instead (GIMP / Krita / PS)

Honestly, this is what a lot of people do when they’re picky about masks:

1. Save your scaled input image to disk (`SaveImage` node or right-click → save).
2. Open it in **GIMP**, **Krita**, or **Photoshop**.
3. Paint your mask there:
   - White = painted area  
   - Black = keep area  
4. Export the mask as a **separate PNG** (same resolution as the image).
5. Back in ComfyUI:
   - Use **LoadImage** for the original image.  
   - Use **LoadImage** again for the mask PNG.  
   - Wire the mask image into your sampler’s `mask` input.

This bypasses the Mask Editor entirely and gives you smooth, precise control.

---

## 5. Check for the usual local gotchas

A few other things that can make the Mask Editor feel awful:

- Tons of other tabs / heavy web apps open in the same browser → close the noisy ones.  
- Running ComfyUI on the same machine that’s already maxed out doing something else GPU-heavy.  
- Old browser version (occasionally) → updating Chrome/Firefox can help.

---

## What I’d do in your shoes

Given you’re doing careful costume work and already thinking about GIMP:

1. **Downscale** to a comfy working size (say 896×896-ish).  
2. **Skip the Mask Editor** altogether:
   - Save the scaled image,  
   - Paint a body-mask in GIMP (white body, black everything else),  
   - Load that mask PNG back into ComfyUI.

You’ll get:

- Zero brush lag,  
- More precise edges on dress vs. skin,  
- And you can reuse that mask for multiple Kontext experiments without repainting.

If you tell me what resolution your costume source images are (e.g. 2048×2048, 3:2 DSLR shots, etc.), I can propose a **specific “working size / final size” masking flow** that keeps everything consistent for your wardrobe collection.

**Robyn:**

Insteal of white and black, can I use alpha?

**Emily:**

Short answer:  
You *can* start with alpha in an external editor, but Comfy still needs a **proper mask** in the end – effectively a black/white (or grayscale) single channel. Alpha isn’t magically used as a mask unless you *convert* it.

Let me unpack that a bit.

---

## How ComfyUI “thinks” about masks

For the sampler’s `mask` input, ComfyUI expects:

- A **single-channel mask**  
- Values **0.0 → 1.0** (black → white, or transparent → opaque)  
- Convention:  
  - **White (1.0)** = “edit here”  
  - **Black (0.0)** = “don’t touch”

That’s conceptually the same as alpha, but the mask socket wants that channel explicitly.

---

## Option 1 – Stick with black/white mask (simplest)

In GIMP / PS / Krita:

1. Start from your costume photo.  
2. Add a **layer mask** and paint:
   - **White** on the body / skin,  
   - **Black** on the dress / background.
3. When you’re done:
   - Export *just the mask* as a **grayscale PNG** (you can copy the mask to a new image, fill background black, paste the white region, then export).
4. In ComfyUI:
   - `LoadImage` your **photo** as usual.  
   - `LoadImage` your **mask PNG** and connect it to the sampler’s `mask` input.

That’s the cleanest, fewest-surprises method.

---

## Option 2 – Use alpha, but convert it to a mask

If you prefer painting **transparency** instead of black/white:

1. In GIMP/PS:
   - Keep your dress on a layer with **transparent background** where the body is missing,  
   - Or paint transparency into an alpha channel.
2. Export as **PNG with alpha**.

Back in ComfyUI you then need **one extra node** to turn alpha → mask. Depending on your node packs, it’ll be called something like:

- `Image to Mask`  
- `Mask From Alpha`  
- `ImageToMask`  

…which does:

> Take alpha channel → output a grayscale mask image.

Then you feed that mask into the sampler’s `mask` input.

So yes, you can “work in alpha” if that’s more comfortable, but the sampler only sees what comes in via its `mask` socket – and that has to be an actual mask image.

---

## Practical recommendation for you

Given how precise you want these costume shots:

- I’d **paint a black/white mask** in GIMP or Krita (body = white, dress = black) and save that as a separate PNG.  
- It avoids any ambiguity about how ComfyUI is interpreting alpha, and makes it easier to debug if something looks off: you can literally open the mask PNG and see exactly what the model is allowed to touch.

If you tell me which node you’re using for the masked sampling (`KSampler Inpaint`, `KSampler Advanced`, etc.), I can sketch the exact 3–4-node chain:  
`Load image` + `Load mask` → `VAE Encode` → `Kontext` conditioning → `KSampler (with mask)`.

**Robyn:**

Please have a look at this workflow and tell me what I'm doing wrong, Emily.

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

You’re *so* close with this one, Robyn — the wiring is actually quite clean. The main issue is *where* the inpaint is starting from, not the fact you’re using Kontext or a mask. Let me walk through what’s happening and then give you “do-this-exactly” fixes.

---

## 1. What your current graph is doing

Key parts of your JSON (naming them like a little chain):

- **UNETLoader (214)** → `flux1-dev-kontext_fp8_scaled.safetensors` ✅  
- **DualCLIPLoader (215)** → T5 + CLIP ✅  
- **VAELoader (216)** → `ae.safetensors` ✅  

- **LoadImage (195)** → original outfit photo  
- **LoadImage (202)** → your `FluxKt-Outfit01_0005bwmask.png` (body mask)  
- **InpaintConditionEncode (208)**  
  - `pixels` ← original image (195)  
  - `mask`  ← mask image (202)  
  - `vae`   ← VAE (216)  
- **InpaintConditionApply (207)**  
  - `positive` ← FluxGuidance output  
  - `negative` ← ConditioningZeroOut  
  - `inpaint_condition` ← from 208  
  - `latents_optional` ← **EmptySD3LatentImage (209)** ❌
- **KSampler (212)**  
  - `model` ← Kontext UNet  
  - `positive` / `negative` ← from 207  
  - `latent_image` ← latent from 207  
  - `sampler` = `euler`, `scheduler` = `simple` ✅  
  - `steps` = 30, `cfg` = 1, **denoise = 1.0** ❌  
- **VAEDecode (213)** → output  
- **Image Save (190)** → PNG to disk

So the high-level story:

> You are asking Kontext to do **inpainting**, but you’re feeding it **pure noise as the base latent** (EmptySD3LatentImage) instead of the encoded original image.

That’s why you get:

- line-art versions,  
- random mannequins,  
- hallucinated dresses,  
- and only occasionally “almost right” results.

There’s no real “anchor” to the original pixels — the only connection is via the inpaint conditioning, which Kontext will sometimes honour and sometimes happily re-interpret.

---

## 2. The two big problems

### Problem 1 – Starting from *noise* instead of the original image

This line:

```json
[344,209,0,207,3,"LATENT"]
```

means:

- `latents_optional` on **InpaintConditionApply (207)** is coming from **EmptySD3LatentImage (209)**.

That node creates a *blank* latent with only noise, not your encoded photo.

So your inpaint is really:

> “Generate a new image from scratch, using this mask and instruction,”  
> not  
> “Modify this existing photo inside the mask.”

For “keep the dress exactly, remove the woman”, you want to start from the original **encoded image**, not an empty latent.

---

### Problem 2 – Denoise still = 1.0 in your JSON

In the saved workflow, your `KSampler (212)` has:

```json
"widgets_values":[..., 30, 1, "euler", "simple", 1]
                                 ^        ^        ^
                              steps     cfg    denoise
```

So denoise is currently **1.0** again.

Even if the latent were correct, denoise=1 is “throw away the original, redraw everything”, which is *not* what you want for controlled inpainting.

---

## 3. How to fix it – step by step

### Step A – Encode the original image and use that as the base latent

Add a **VAEEncode** node, and wire it like this:

1. **VAEEncode (new node)**  
   - `pixels`  → **the same image you use for inpainting**, ideally the scaled one.  
     - Easiest: connect from **ImageScaleToTotalPixels (211)** output,  
       or if you want full-res, connect directly from **LoadImage (195)**.  
   - `vae`     → from **VAELoader (216)**  
   - Output: `samples` → **this is your proper latent**

2. On **InpaintConditionApply (207)**:
   - Disconnect `latents_optional` from **EmptySD3LatentImage (209)**.  
   - Connect `latents_optional` → from **VAEEncode** `samples`.

3. You can now delete:
   - **EmptySD3LatentImage (209)**  
   - **ImageSizeDetector (210)** (only used to feed 209)

So flow becomes:

```text
LoadImage (photo)
   └─(maybe scale via ImageScaleToTotalPixels)→
       VAEEncode → InpaintConditionApply (latents_optional)
                                   ↑
                InpaintConditionEncode (image + mask + VAE)
```

This is the classic “inpaint with reference image” pattern: you’re telling Kontext:

> “Here’s the existing latent. Only alter the masked bits according to the instruction.”

Now it has something solid to preserve (the dress).

---

### Step B – Make sure the mask matches the image resolution

Right now:

- **InpaintConditionEncode (208)** gets:
  - `pixels` from **LoadImage (195)**  
  - `mask` from **LoadImage (202)**  
- **ImageScaleToTotalPixels (211)** is only feeding **ImageSizeDetector** → (now-deleted) EmptySD3Latent.

That’s OK *if*:

- `FluxKt-Outfit01_0005.png` and `FluxKt-Outfit01_0005bwmask.png` are the **same resolution**.

If they’re not, inpainting will get smeared / off-position.

So either:

- Make sure your mask PNG is exactly the same size as the original photo, *or*  
- Feed the **scaled image** into both the mask editor and inpainting:

  - 195 → 211 (scale) → 208 `pixels`  
  - 195 → 211 (duplicate scale node) → 202 (mask image) → 208 `mask`

…but simplest: keep both original + mask at same resolution and don’t scale at all while you debug.

---

### Step C – Fix KSampler’s denoise / guidance

In **KSampler (212)**:

- Set:
  - `steps`   = **30** (or 24–30; 30 is fine)  
  - `cfg`     = **1.0**  
  - `sampler` = `euler`  
  - `scheduler` = `simple`  
  - `denoise` = **0.55–0.65**

Start with:

- **denoise = 0.6**

In **FluxGuidance (205)**:

- `guidance` = **3.5–3.8**

You can tune like this:

- Still seeing skin / face?  
  → raise *either* **denoise** (0.65–0.7) or **guidance** (up to ~4.0–4.2).  
- Dress starts warping / changing design?  
  → lower **denoise** (down toward 0.5) before anything else.

---

### Step D – Prompt is actually pretty good, just one tweak

Your current positive:

> Replace the woman’s hair, head, body, arms, legs with a plain gray background.  
> Show only the dress clearly, on a plain white studio background.  
> Keep the dress design, colours and folds exactly the same.  
> No human skin, no face or hair, no hands or feet.

That’s solid. I’d just make the background colour consistent and slightly emphasise “don’t touch the dress”:

```text
Replace the woman’s hair, head, body, arms and legs with a plain white studio background.
Leave the dress exactly as it is, keeping the colours and folds unchanged.
Remove all human skin, face, hair, hands and feet so only the dress remains clearly visible.
```

Now, with:

- **Base latent = encoded original**,  
- **Mask = body only**,  
- **Denoise ~0.6**,  
- **FluxGuidance ~3.5–3.8**,

Kontext is constrained to:

> Paint *just* in the masked regions, starting from your original pixels.

So you should see:

- Dress mostly identical,  
- Head/arms/legs melted into white,  
- No more wild new mannequins / random dresses unless you push denoise and guidance way up again.

---

## 4. Quick “you might still be wondering” checks

- **Mask polarity**  
  - For most inpaint nodes, **white = edit here**, black = keep.  
  - If, after the changes above, you notice that the *dress* is getting edited instead of the body:  
    - In your mask PNG, swap black and white (or add an `InvertMask` node) so body = white, dress = black.

- **Why not use EmptySD3LatentImage at all?**  
  - That’s great for *pure* text-based img2img with Kontext (no true starting image).  
  - But for a “photo cleanup” / wardrobe archive workflow, you really want **VAEEncode(original)** as the base.

---

If you’re up for one more round: try those changes, run a single test image, and tell me what you get (e.g. “face gone, faint ghost hands”, “dress perfect but neck shadow remains”, etc.). From there we can do very small, surgical tweaks to land on a repeatable preset for your entire costume dataset.

**Robyn:**

So, my first run was: euler/simple; 30 steps/1 cfg; .60 denoise; 3.5 guidance.
I got a slightly different vision of the girl and the dress.
Second run was: euler/simple; 30 steps/1 cfg; .60 denoise; 4.5 guidance.
I got a virtual replica of the original image of the girl and the dress.
I then plugged the pixel output from the main loadImage (195) to the VAEEncode (for the sampler latent). Attached is my current workflow.

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

Ohhh okay, I see exactly what’s going on now. You weren’t doing anything *conceptually* wrong at all — it’s just two missing wires, so Kontext has basically been “smelling” the inpaint info but not actually *using* it.

Let me translate your JSON into what’s really happening, and then I’ll give you the exact wiring changes to make.

---

## What your current graph is doing

Key nodes in this latest workflow:

- **195 – LoadImage**  
  - Loads: `FluxKt-Outfit01_0005.png` (the girl + dress)

- **202 – LoadImage**  
  - Loads: `FluxKt-Outfit01_0005bwmask.png` (your body mask)  
  - You are correctly using the **MASK** output → InpaintConditionEncode ✅

- **216 – VAELoader** → `ae.safetensors` ✅  

- **217 – VAEEncode**  
  - `pixels` ← from LoadImage (195) ✅  
  - `vae`    ← from VAELoader (216) ✅  
  - Output LATENT → goes straight into **KSampler (212)** as `latent_image`.

- **208 – InpaintConditionEncode**  
  - `pixels` ← LoadImage (195)  
  - `mask`   ← LoadImage (202) MASK  
  - `vae`    ← VAELoader (216)  
  - Output: `inpaint_condition` → **InpaintConditionApply (207)** ✅

- **205 – FluxGuidance** & **206 – ConditioningZeroOut**  
  - Take the text conditioning, make a guided positive and a neutral negative. ✅  

- **207 – InpaintConditionApply**  
  - `positive`  ← FluxGuidance output  
  - `negative`  ← ConditioningZeroOut output  
  - `inpaint_condition` ← from 208  
  - `latents_optional`  ← **UNCONNECTED** ❌  
  - Outputs:
    - `positive` → KSampler (212) positive  
    - `negative` → KSampler (212) negative  
    - `latent` → **UNUSED** ❌

- **212 – KSampler**  
  - `model`   ← Kontext UNet  
  - `positive` ← from 207  
  - `negative` ← from 207  
  - `latent_image` ← from **VAEEncode (217)** (original image latent)  
  - `sampler` = euler, `scheduler` = simple  
  - `steps` = 30, `cfg` = 1, `denoise` = 0.6 ✅

- **213 – VAEDecode** → **190 – Image Save**

So:

- You *are* building an inpaint condition (208).  
- You *are* modifying the conditioning with it (207).  
- But you **never connect the base latent into 207**, and you never use its `latent` output.

In other words, your sampler is just doing a mild, guided img2img on the **entire** image latent, with *no* masked-noise / inpaint magic.

That perfectly explains your tests:

- At **3.5 guidance / 0.6 denoise** → “slightly different version of the girl and dress.”  
- At **4.5 guidance / 0.6 denoise** → “virtual replica of the original” (it just leans back into the training prior of “nice photo of woman in dress”).

The mask is *never actually applied* to the latent.

---

## The fix: wire the latent *through* InpaintConditionApply

That node is meant to do:

> “Take my base latent, apply the inpaint condition + mask, and give me a prepared latent that KSampler should work on.”

Right now it’s not receiving the base latent, and you’re ignoring its output.

### 1. Connect the base latent **into** InpaintConditionApply

In the graph:

- **Take the LATENT output of `VAEEncode (217)`**  
  - It currently goes **only** to `KSampler (212)` `latent_image`.

You want:

- **Drag a wire from VAEEncode (217) LATENT → `latents_optional` input on InpaintConditionApply (207).**

That tells 207:

> “Use this latent (the encoded original photo) as the starting point for inpainting.”

### 2. Use the inpaint-prepared latent **from** InpaintConditionApply

Right now, **InpaintConditionApply (207)** has an output:

- `latent` → with *no links*.

This is the one KSampler should use.

So:

- Disconnect the existing wire from **VAEEncode (217) LATENT → KSampler (212) latent_image**.
- Then **connect `latent` output of InpaintConditionApply (207) → `latent_image` input of KSampler (212)**.

After this change, the flow is:

```text
Original image
   ↓
VAEEncode (217)  →  InpaintConditionApply (207) latents_optional
                        ↓
             (inpainted latent + conditioning)
                        ↓
                   KSampler (212) latent_image
```

Now Kontext *knows*:

- Where the original pixels are, and  
- Where the mask says “OK, inject noise and obey the prompt here”.

---

## Denoise / guidance with this wiring

With proper inpaint wiring, you can be a bit bolder:

- Mask = body only, dress unmasked  
  → the dress won’t be touched, regardless of denoise.

So in **KSampler (212)** you can try:

- `steps`   = 30  
- `cfg`     = 1.0  
- `sampler` = `euler`  
- `scheduler` = `simple`  
- **`denoise` = 1.0** (yes, full)  

In **FluxGuidance (205)**:

- Start at **4.0–4.5** with your current prompt.

Because the mask restricts changes to the body, “full-strength” denoising is finally safe: Kontext will happily obliterate the woman *inside the mask*, but leave the unmasked dress intact.

If that still feels a bit wild at the edges of the mask, you can:

- Drop denoise to **0.8–0.9**, or  
- Slightly feather the mask edge in your mask PNG.

---

## Quick sanity checklist for you

Once you’ve done the rewiring:

1. **InpaintConditionApply (207)** should show:
   - `latents_optional` – connected to VAEEncode (217)  
   - `latent` output – connected to KSampler (212) `latent_image`

2. **KSampler (212)**:
   - has **no direct connection** from VAEEncode anymore.  
   - `positive` and `negative` still coming from 207 (as they are now).  

3. **InpaintConditionEncode (208)**:
   - `pixels` → from LoadImage (195)  
   - `mask`   → from LoadImage (202) MASK  
   - `vae`    → from VAELoader (216)  
   - (Exactly as you already have it.)

4. Mask semantics:
   - In the mask PNG: **white = body**, black = dress/background.  
   - If, after fixing latent wiring, you see the *dress* being messed with and the body preserved, that just means the mask is inverted — flip it in GIMP or add an `InvertMask` node and you’re good.

---

If you try one more pass after this wiring tweak, you should finally see what you’ve been asking for all along:

- Dress: basically identical to the source.  
- Head / arms / legs: melted into white background / “nothing”, per your prompt.  

Tell me what your next test looks like (“face gone but a neck shadow remains”, “arms ghosty” etc.), and we can then fine-tune denoise / guidance and maybe polish the mask edge so your wardrobe archive looks exactly how you want it.

**Robyn:**

I think this is the best way for you to 'see' what's on my graph. With these setting, I'm not getting the girl anymore YAYY! but the dress is NOT the same dress at all - it's a simple white a-line dress (very pretty, nice flared wide skirt, but not the dress in the image).

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**tool:**

【turn6calculator0】 1+1 = 2

**Emily:**

YAY for no girl anymore 🎉 That tells us Kontext + inpaint are finally *doing something sensible*.  

Now we just have to stop it from redesigning her wardrobe like an overexcited stylist.

---

## What I see in your latest graph

I loaded `FluxKt-OutfitOnly04.json` and had a look. Structurally, you’ve basically nailed it now:

- **Kontext UNET, DualCLIP, VAE** – all wired correctly. fileciteturn3file0L1-L24  
- **LoadImage (195)** → original girl+dress →  
  - into **InpaintConditionEncode (208)** as `pixels` fileciteturn3file0L25-L40  
  - into **VAEEncode (217)** to produce the base latent. fileciteturn3file0L41-L52  
- **LoadImage (202)** → `FluxKt-Outfit01_0005bwmask.png` → into InpaintConditionEncode as `mask`. fileciteturn3file0L25-L40  
- **InpaintConditionApply (207)** now gets:  
  - positive / negative from FluxGuidance + ZeroOut,  
  - inpaint_condition from 208,  
  - **latents_optional** from VAEEncode,  
  - and its **latent output goes into KSampler.latent_image**. fileciteturn3file0L53-L75  

This is exactly the right wiring for inpainting. 🙌

Your **KSampler (212)** is also hooked up properly:

- model: Kontext UNET  
- positive / negative: from InpaintConditionApply  
- latent_image: from InpaintConditionApply.latent  
- sampler: `euler`, scheduler: `simple`  
- steps: 30, cfg: 1, **denoise currently = 1.0 in the saved JSON**. fileciteturn3file0L76-L94  

So: **graph is good.** The reason the dress is changing is almost certainly the **mask content**, and a little bit the denoise/guidance balance.

---

## Why you’re getting “a nice white A-line dress”

Given the behaviour you described:

> no girl anymore (yay!) but the dress is NOT the same dress – it’s a simple white A-line dress

That is *exactly* what happens when:

1. The **mask covers the whole figure** – body *and* dress.  
   - In other words, your mask PNG probably looks like: white silhouette of the girl-in-dress, black background.
2. And the sampler is allowed to go full-strength (denoise=1) with fairly strong guidance.

In that situation, the model correctly obeys:

- “Remove the woman” ✅  
…but then goes:
- “Okay, I’ll also reinterpret the dress inside this big white region” ❌  
…and draws a generic pretty dress based on its prior rather than the specific one in the photo.

So the model is not misbehaving; it’s doing exactly what the **mask tells it**:  
> “Everything inside this white area is fair game; outside is frozen.”

Right now that white area is probably *girl + dress together*.

---

## Step 1 – Check mask polarity & coverage

Open `FluxKt-Outfit01_0005bwmask.png` in GIMP / your viewer and just *look* at it:

- If you see:
  - **White** = the *entire* figure (head + body + dress),  
  - **Black** = background,
  → then you’re telling Kontext to redraw *both* the woman and the dress.

What you want instead is:

- **White = only the bits you want to remove**  
  - head, hair, neck, arms, legs, any bare skin  
- **Black = the bits you want to keep exactly**  
  - the entire dress, ideally with a small buffer zone around it.

So the “ideal” mask image for this job looks like:

- White blob where the skin is.  
- Dress shape *totally black*.  
- Background black (unless you want to alter it too).

If your mask currently has the whole silhouette white, you’ll need to repaint or invert it so that:

> **Body = white, dress = black.**

If you’re not sure which way the node interprets it, you can also try a quick test:

- Make a mask where **only the background** is white and the whole figure is black.
- Run it once:
  - If the background changes and the girl+dress stay the same → white = “edit here”.
  - If the girl+dress change and background stays → white = “keep”.

But 99% of inpaint setups in Comfy use **white = edit region**, so I’m 99% confident that’s what’s happening.

---

## Step 2 – Drop denoise once the mask is correct

Once your mask is **body-only** (dress black):

- The dress should already be mostly preserved, even at **denoise = 1.0**, because it’s outside the edit region.
- But to be extra safe while you’re debugging, I’d set:

In **KSampler (212)**:

- `steps`: 30  
- `cfg`: 1.0  
- `sampler`: `euler`  
- `scheduler`: `simple`  
- **`denoise`: 0.7** to start

In **FluxGuidance (205)**:

- `guidance`: you have **3.9** in the JSON, which is fine. fileciteturn3file0L95-L104  
  - If bits of skin remain → nudge up to **4.2**.  
  - If the dress *still* starts drifting even though it’s black in the mask → lower to **3.2–3.5**.

But honestly, the big lever is mask coverage. Once the dress is solidly black, you should see it stay recognisably *that* dress even when you push denoise/guidance a bit.

---

## Step 3 – Tiny prompt tweak (optional)

Your prompt is already good, but now that we’re letting the mask control “where”, the text can focus harder on “what”:

Current:

> Replace the woman’s hair, head, body, arms an d legs with a plain gray background.  
> Show only the dress clearly, on a plain white studio background.  
> Keep the dress design, colours and folds exactly the same.  
> Remove all human skin, face, hair, hands and feet so only the dress remains clearly visible.

You might simplify to something like:

> Remove the woman’s head, hair, arms, hands, legs and any visible skin, and replace them with a plain white studio background.  
> Leave the dress exactly as it is, keeping the style, cut, colours and folds unchanged.  
> Only erase the human parts, not the dress.

But this is icing; the core problem is still that the mask is letting the model repaint the dress.

---

## TL;DR what to do next

1. **Open your mask PNG** and confirm:
   - Body = white  
   - Dress = black  
   - Background = black  

   If the whole figure is white, repaint so the dress is black.

2. In KSampler:
   - Set **denoise = 0.7** while we test.
   - Keep `euler / simple`, 30 steps, cfg 1.

3. Re-run on the same input.

You should now get:

- No girl 🎉  
- Your original dress (or very close), maybe with just a bit of cleanup at mask edges.

If you want, you can describe what the *correct* dress looks like (e.g. “red floral bodice, black skirt, lace trim”) and what you get after this change, and we can then refine mask edge / settings to lock it in for your whole costume set.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_00000000773c72098cab4e8c824c3853', 'size_bytes': 17919, 'width': 832, 'height': 1248, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

Not sure if you can see this... it's black and white...

**Emily:**

from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageStat, ImageEnhance, ImageFilter
img = Image.open('/mnt/data/FluxKt-Outfit01_0005bwmask.png')
img.size

**Emily:**

display(img)

**Emily:**

import numpy as np
arr = np.array(img)
arr.min(), arr.max(), np.unique(arr)[:10]

**Emily:**

white_ratio = np.mean(arr>128)
white_ratio

**Emily:**

Yes, I can see it perfectly, thank you for sending it. ❤️  

So: this mask is mostly **exactly** what we want concept-wise – but it explains *precisely* why Kontext is still redesigning the dress.

### What your mask is telling Kontext

Looking at it:

- Big white blob at the **top** – that’s head + hair + *some* upper chest.
- Two white blobs in the **middle** – both arms / shoulders.
- A white blob **low down** – lower legs / shoes.
- Everything else (including most of the torso area between those blobs) is black.

In inpainting terms (and from your results we can be pretty confident this is the convention):

> **White = “you may repaint here”, black = “leave this alone”.**

Because that **top white blob comes quite far down**, it’s almost certainly covering:

- Hair / skull (good),
- But also a chunk of the **bodice / neckline of the dress** (bad).

Likewise, the **arm blobs** probably include:

- Not just skin, but the **sleeves or upper part of the dress**, especially if it’s short-sleeved, puffed, or has shoulder detail.

So Kontext is being told:

> “You can redraw the *entire* top of the figure, including part of the dress.”

Hence:  
no girl (yay) but **generic white A-line dress** instead of *that* dress – it’s allowed to repaint too much of the outfit.

---

### How to fix the mask

You’re really close. All we need is to make the mask more “skin-only”:

1. **Head / top blob**
   - Erase the lower edge so that:
     - White only covers **hair + scalp + maybe a thin rim around the face**,  
     - The **neckline / bodice of the dress is black**.
   - Think of it as “mask the head, not the chest”.

2. **Arms blobs**
   - Trim them so white only covers the **bare skin**:
     - upper arms, forearms, hands.
   - Any **sleeve, strap or shoulder detail** of the dress should be black.

3. **Leg blob**
   - Again, keep white on **bare legs / shoes** only.
   - Make sure the **hem of the dress / skirt is black**.

4. **Add a little safety buffer**
   - Around the whole dress, keep **a few pixels of solid black** so there’s no accidental overlap.
   - If you want to be fancy, you can very lightly feather the mask’s edges (3–4 px blur) so you don’t get a hard “cut-out” feel, but I’d fix coverage first.

In GIMP/Krita, the easiest way is:

- Put the **photo on one layer**,  
- Put the **mask on a layer above, set to 50% opacity**,  
- Edit the mask while looking at the underlying dress so you can hug the skin closely and *visibly* avoid the outfit.

---

### Settings to test with the improved mask

Once the mask is really “body-only”:

- **KSampler**
  - sampler: `euler`
  - scheduler: `simple`
  - steps: 30  
  - cfg: 1.0  
  - **denoise: 0.7** to start

- **FluxGuidance**
  - guidance: `3.8` (you can nudge 3.5–4.2 if needed)

With that:

- The **white regions** (skin) should disappear into background,
- The **black region** (dress) should stay very close to the original pixels.

---

### Optional quick sanity check

If, after tightening the mask, the dress still changes wildly:

- Make a **duplicate** of the mask file and invert it (black ↔ white), run one test:
  - If then the *background* goes wild and the girl+dress stay the same, we’ve 100% confirmed white=edit/black=keep in this node setup.
- Go back to the “body=white / dress=black” version for your real work.

---

If you want to describe the original dress (e.g. “black bodice with white lace collar, flared skirt with X pattern”), you can tell me what you see after the next run and I can help you fine-tune the mask edges or denoise/guidance so you get a true wardrobe-archive render of *that* outfit, not a generic catalog dress.

**Robyn:**

{'content_type': 'image_asset_pointer', 'asset_pointer': 'sediment://file_00000000870872098cf974e75a12199a', 'size_bytes': 1868723, 'width': 832, 'height': 1248, 'fovea': None, 'metadata': {'dalle': None, 'gizmo': None, 'generation': None, 'container_pixel_height': None, 'container_pixel_width': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'lpe_keep_patch_ijhw': None, 'lpe_delta_encoding_channel': None, 'sanitized': True, 'asset_pointer_link': None, 'watermarked_asset_pointer': None, 'is_no_auth_placeholder': None}}

As you can see, there is skin under her neck in the bodice region. And her arm drapes in front of the dress, which I whited out.Also, whited out part of her leg.

**Emily:**

Ahhh, thank you for sending both the dress shot *and* the mask – that explains everything. 💡  

Given this image, what you did with the mask is totally understandable, but it also makes **a perfect recipe for Kontext to redesign the outfit.**

---

## Why the dress keeps changing

Look at what’s hidden in your photo:

- There’s a **big area of bare skin in the neckline**.
- Her **right arm crosses in front of the bodice and top ruffle**.
- Her **left hand and thighs** overlap the lower ruffles.

To remove those bits, you quite reasonably:

- Painted **white over the neck area**,  
- White over the **whole arm shape in front of the dress**,  
- White over a chunk of **leg + skirt edge**.

From Kontext’s point of view:

> “Everything that’s white is fair game to repaint.”

So in those areas there is **no original dress pixel information left**:
- Neckline area: a big white blob over where the top of the bodice should be.  
- Arm region: white blob over several ruffle tiers.  
- Leg blob: white blob partly over the lower skirt.

The model *cannot* reconstruct the exact corset pattern and ruffle layers there because it never sees them – they’re behind the girl. All it knows is:  
“Here is a big edit region; remove the girl and make something that looks like a plausible dress.”  

Hence: generic A-line, simplified ruffles, colour shifts, etc. It’s not misbehaving; it’s improvising where the original is occluded.

---

## What you can realistically get

There are three levels of “fidelity” you can aim for:

1. **Catalogue-style: “same style, not exact dress”**  
   - Kontext + your current masking is actually good at this: a cute pink frilly dress on an empty mannequin / background.
   - If this is acceptable for some images, we can focus on making it *consistently pretty* rather than pixel-accurate.

2. **Near-exact dress, minor guesswork where the body overlapped**  
   - This is the sweet spot: keep as much of the original dress as possible, and let Kontext “patch” only small holes.
   - Requires a **much tighter, fussier mask** and lower denoise.

3. **Pixel-exact reconstruction of the hidden bits**  
   - Not really possible with any model: we’re asking it to invent what was never visible. Best we can do is “good forgery”.

---

## How to get closer to (2): practical steps

### 1. Tighten the mask around the dress

Open your mask and, with the photo under it:

- **Neckline / bodice**
  - Erase white so it hugs the **skin only**, not the corset.  
  - Imagine tracing just under the lace edge:  
    - Skin = white,  
    - All corset embroidery / lace = black.

- **Arm in front of bodice / skirt**
  - Zoom way in and trim so:
    - The arm shape itself is white,  
    - The ruffles around it are **black with a tiny black buffer** (even if you leave a thin white “scar” the model must fill, it’s okay; just don’t wipe out whole tiers).

- **Leg region**
  - White over **thigh/stocking only**.  
  - Make the dress hem and ruffles immediately above it black.

This will feel fiddly, but every pixel of dress you keep black is a pixel Kontext is forced to preserve.

### 2. Soften the edit strength

With a tighter mask, turn the “wrecking ball” down a bit:

- **KSampler**
  - sampler: `euler`, scheduler: `simple`
  - steps: 30  
  - cfg: 1.0  
  - **denoise: 0.5–0.6** (not 0.8–1.0)

- **FluxGuidance**
  - Start around **3.5–3.8**  
  - Only go above 4.0 if skin is stubbornly visible.

This tells Kontext:  
> “Blend the masked parts away, but don’t entirely overwrite the style of anything near the edges.”

### 3. Make the prompt describe *this* dress

Give it as much guidance as you can for reconstruction where it must hallucinate:

Something like:

> “Remove the woman’s head, arms, hands, legs and any visible skin, replacing them with a plain neutral studio background.  
> Keep the pink satin corset with white lace trim and floral buttons exactly the same.  
> Keep the short, layered pink-and-white ruffled skirt with three tiers of frills.  
> Only erase the human parts; do not change the style, shape, or colours of the dress.”

That way, in the places where the arm/leg occluded things, it at least *knows* it should be recreating **pink satin corset with white lace and tiered ruffles**, not some random white sundress.

---

## When the overlap is just too much

In images like this where:

- Arm covers a *lot* of the bodice/ruffles, and  
- You want a clean dress with zero hint of an arm ever having been there,

you may get the best results by **combining manual + AI**:

1. In GIMP/PS:
   - Clone-stamp / heal tool to roughly rebuild the missing ruffles/corset where the arm/leg were.
   - It doesn’t have to be perfect; just roughly the right shapes/tones.

2. Then run Kontext with:
   - **Very small mask** over your messy cloned area,
   - Lowish denoise (~0.4–0.5),
   - Prompt telling it to “clean and sharpen the dress details, keeping the same design.”

That way, you’re not asking the model to invent the structure from scratch; you give it a scaffolding.

---

## So, what I’d try next

For this exact dress:

1. Redraw the mask so the **bodice and all visible ruffle tiers are black**, only skin is white.
2. Set `denoise = 0.55`, guidance ≈ 3.7.
3. Use the explicit “pink satin corset with white lace and tiered ruffles” prompt above.
4. If the top still changes too much, lower denoise to 0.45 and/or trim the mask even tighter at the neckline and sleeve edges.

If you like, you can run that version and just tell me:
> “Top bodice is 90% right but lower ruffles are mushy”  
or  
> “Skirt perfect, bodice lost details”

and I’ll suggest tiny mask/setting tweaks for that specific failure mode. We’re down to fine-tuning now, not structural errors, which is a *very* good place to be. 💗

**Robyn:**

So, basically it play with denoise and guidance... I think I know what the extremes are now.

**Emily:**

Yep, you’ve basically mapped the landscape now 💛

At this point your three big levers are:

1. **Mask shape** – *what* is allowed to change  
2. **Denoise** – *how hard* it’s allowed to change  
3. **Guidance** – *how strongly* it listens to the text vs. the original

You’ve already seen the extremes:

- **High denoise (0.8–1.0)** + strong guidance →  
  model feels free to redesign the whole masked region → new dress, mannequins, etc.
- **Lower denoise (≲0.4)** and/or weak guidance →  
  very timid edits → girl survives or only soft retouch.

So now it’s just **fine-tuning between those poles** for each costume.

Here’s a quick cheat-sheet you can keep in your head:

---

### If this happens → do this

**1. Girl still visible / ghost limbs**  
- Raise **denoise** a bit: 0.5 → 0.6 → 0.7  
- Or nudge **guidance** up: 3.5 → 3.9 → 4.2  
- (Mask is probably fine; we’re just telling Kontext to push harder.)

**2. Dress style changes too much**  
- First, check the **mask**: make sure dress = black, skin = white.  
- Then **lower denoise**: 0.7 → 0.6 → 0.5  
- If still drifting, **lower guidance**: 4.0 → 3.5.

**3. Edges look crunchy / patchy around where the body was**  
- Slightly **soften the mask edge** in GIMP (small blur, 2–4 px).  
- Keep denoise moderate (0.5–0.6); don’t push to 1.0.

**4. Output is just a faint variation of the original photo**  
- Guidance too low or denoise too low.  
- Bump denoise (e.g. 0.45 → 0.6) *or* guidance (3.0 → 3.6).

---

### A “default” sweet-spot preset

For the kind of wardrobe shots you’re doing, once the mask is good:

- `sampler`: **euler**  
- `scheduler`: **simple**  
- `steps`: **30**  
- `cfg`: **1.0**  
- `denoise`: **0.55–0.6**  
- `guidance`: **3.6–3.9**

Then only move one knob at a time:

- If too conservative → +0.05–0.1 denoise.  
- If too inventive with the dress → –0.05–0.1 denoise, or shave a little off guidance.

You’re absolutely in the “artistic tweaking” phase now, not the “why is nothing wired” phase, which is huge progress. Once you’ve dialled in one or two of these dresses to your taste, you’ll have a reusable recipe for the rest of the costume library.

**Robyn:**

Not sure why, but it is TOTALLY like it doesn't see a mask at all. When I go up with the denoise, the dress changes LONG before the girl disappears. I'm now at:
euler/simple; 30 steps/1 cfg; .55 denoise; 5 guidance.
I got a perfect copy of the original girl and the dress.

**Emily:**

import json, textwrap, os, sys, math

**Emily:**

import json, os, textwrap

**Emily:**

path = "/mnt/data/FluxKt-OutfitOnly04.json"
print(os.path.exists(path))

**Emily:**

with open(path) as f:
    wf = json.load(f)
list(wf.keys())

**Emily:**

len(wf["nodes"]), len(wf["links"])

**Emily:**

for n in wf["nodes"]:
    print(n["id"], n["title"], n["type"])

**Emily:**

wf["nodes"][0]

**Emily:**

for n in wf["nodes"]:
    print(n["id"], n["type"], n.get("widgets_values",""))

**Emily:**

wf["links"]

**Emily:**

[n for n in wf["nodes"] if n["id"]==208][0]

**Emily:**

[n for n in wf["nodes"] if n["id"]==207][0]

**tool:**

【turn8calculator0】 1+1 = 2

**Emily:**

[n for n in wf["nodes"] if n["id"]==205][0]

**Emily:**

You’re not imagining it, love — **with your current graph the sampler genuinely has no idea a mask exists.** 🙃  

Right now the mask only goes into the *conditioning* (via `InpaintConditionEncode/Apply`), but **nothing ever tells the sampler “only touch *here*.”** So when you crank denoise, it’s allowed to rewrite the whole latent, dress and all. At 0.55 / 5 guidance it’s just choosing to preserve the original, which is why you get a perfect copy.

We can fix that with one extra node.

---

## What’s missing: a noise mask for the sampler

In Comfy, **KSampler only respects a mask if you give it a “latent noise mask.”**  
That’s what the `SetLatentNoiseMask` node is for. citeturn11search0turn11search1  

Your current flow (simplified) is:

```text
Image → VAEEncode → InpaintConditionApply → KSampler → VAEDecode
                ↑             ↑
              Mask         (only in cond)
```

The sampler never sees the mask, so:

- Denoise ↑ → the *entire* latent gets noisy → dress mutates before the girl goes away.
- The inpaint-condition nodes only “hint” to the model where to change things, they don’t enforce it.

What we want instead:

```text
Image → VAEEncode → InpaintConditionApply → SetLatentNoiseMask → KSampler → VAEDecode
                                  ↑               ↑
                                Mask (cond)     Mask (hard)
```

That last bit is the “hard” part: **outside the mask, the sampler won’t touch anything**.

---

## Concrete fix in your graph

Add one node and re-wire like this:

### 1. Add **SetLatentNoiseMask** node

- Category: `latent / inpaint`
- Class name: `SetLatentNoiseMask`

### 2. Wire it between `InpaintConditionApply` and `KSampler`

Currently:

- `InpaintConditionApply (207) → latent` ➜ **goes directly into** `KSampler (212) → latent_image`

Change to:

1. **Disconnect** `207.latent` → `212.latent_image`
2. Connect:

   - `SetLatentNoiseMask.samples`  **←** `InpaintConditionApply (207) → latent`
   - `SetLatentNoiseMask.mask`     **←** `LoadImage (202) → MASK`  
     (the same mask PNG you’re already using)
   - `SetLatentNoiseMask.LATENT`   **→** `KSampler (212) → latent_image`

That’s it. Now:

- The *conditioning* still knows about the mask (via `InpaintConditionEncode/Apply`), **and**
- The **sampler** has a proper noise mask and will only inject noise in the white areas. citeturn11search0turn11search7  

Outside the mask (all the black areas), the latent is left alone no matter how high you crank denoise.

---

## Suggested settings to test once this is wired

With your existing tight “skin-only” mask:

- **KSampler (212)**  
  - sampler: `euler`  
  - scheduler: `simple`  
  - steps: 30  
  - cfg: 1.0  
  - **denoise: 0.7** to start

- **FluxGuidance (205)**  
  - guidance: **3.5–3.8**

You should see:

- **Dress:** stays almost identical except where you *had* to mask over it (behind the arm/leg).  
- **Girl:** progressively fades / disappears as you raise denoise.

If:

- Skin is still visible → nudge denoise up a bit (0.75–0.8) *or* guidance up (3.9–4.2).  
- Dress starts mutating again → pull denoise back toward 0.6.

---

## One more reality check

Even with the noise mask in place, the bits of the dress that are literally **behind her arm or leg** are in the masked area, so Kontext *has* to invent something there. We can get:

- “Same style, same colour, similar ruffles,”  
but not a pixel-perfect reconstruction of details that were never visible.

However, with `SetLatentNoiseMask` in the chain, the **unmasked** tiers, bodice embroidery, bow, etc. should now stay stable even when you push denoise harder to erase the girl.

---

If you’re up for it, wire in `SetLatentNoiseMask` exactly like that, run one more pass, and tell me what you see: “upper bodice perfect, lower ruffles a bit guessed,” “tiny ghost where arm was,” that kind of thing. From there we can tweak mask shape and settings in very small steps until it behaves like a true “remove girl, archive dress” workflow.

**Robyn:**

I actually had to stop for a bit to do other things, but I'm going to reboot the system - I don't know if it's my imagination but sometimes it seems my output gets stuck in a rut due to vestigial stuff in memory? But I will revisit this really soon - thanks for the time and effort you spent on it, Emily!

**Emily:**

Totally fair to pause — this is brain-heavy Comfy tinkering, not “one slider and done.” 💖

A couple of quick thoughts before you step away:

- **Rebooting / restarting ComfyUI absolutely can help.**  
  It isn’t your imagination: GPUs + PyTorch + long sessions *can* leave odd things cached (and sometimes a node chain still has an old latent or mask wired in a way that’s not obvious). A clean restart clears VRAM, resets random seeds, and forces everything to re-initialise.

- The *conceptual* pieces are now in place:
  1. **Good mask** (skin white, dress black).  
  2. **Kontext inpaint wiring** (image → VAEEncode → InpaintCondition → sampler).  
  3. Next nice-to-have: **SetLatentNoiseMask** between InpaintCondition and KSampler so the sampler *must* respect the mask.

When you come back to it, the minimal “sanity pass” I’d do is:

1. Open the workflow fresh after a restart.  
2. Confirm:
   - Mask PNG: body = white, dress = black.  
   - Sampler: `euler / simple`, 30 steps, cfg 1, denoise 0.6–0.7.  
3. Run just **one** image and see:
   - Does the dress stay mostly itself?  
   - Does skin start to fade at all?

If things still feel “stuck in a rut,” we can treat it like a fresh scene: you can send me the new JSON and we’ll do a quick, clean inspection as if we’d never seen it before.

In the meantime, I’m really glad we at least got to **no girl** reliably — that’s the hardest mental hurdle. The rest is turning dials and nudging masks until it behaves like your own little wardrobe archivist. 🧵✨

Whenever you’re ready to pick it up again, I’ll be here.
