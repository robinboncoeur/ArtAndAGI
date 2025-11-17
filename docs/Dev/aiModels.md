# Image Models

## Samplers and Schedulers

Short version:

* **Flux.1 Dev / Kontext / SRPO** all behave like “Flux” models → they like **low CFG (1.0)**, **no negative prompt**, and **Euler-family or DPM++ 2M samplers**.
* **Qwen-Image** is very similar (DiT + flow matching) but with its own sweet spots: **few steps, low CFG, and either Euler or res_multistep**. ([Medium][1])

Below is a breakdown by model, with **ComfyUI-style presets** you can drop straight into KSampler / SamplerCustom.

<hr style="height:2px;border-width:0;color:pink;background-color:pink">



### FLUX.1 Dev

**general text-to-image**

**What it is**
Flux.1 [dev] is the open-weights “base” model from Black Forest Labs, trained with flow-matching / rectified flow; CFG is effectively baked into the distillation process. ([andreaskuhr.com][2])

**Key quirks**

* **CFG scale ≈ 1.0** (this is *not* SDXL – high CFG just wrecks it). ([andreaskuhr.com][2])
* No true negative prompt; you steer by re-phrasing the *positive* prompt. ([andreaskuhr.com][2])
* You normally get best results around **20–30 steps**. ([andreaskuhr.com][2])

#### Recommended samplers

**& schedulers (what people actually use)**

From Forge / SD.Next docs and community testing:

* **Euler (a/normal) + Simple/Normal scheduler** is a very solid default; this is also what the Forge “Flux” preset uses. ([andreaskuhr.com][2])
* A lot of ComfyUI folks report **Euler + Beta scheduler** (or “Euler beta”) giving slightly better edges/details at similar speed. ([Reddit][3])
* For “classic” diffusion workflow, **DPM++ 2M (or DPMPP_2M_SDE) + Karras** is a great quality preset; a ComfyUI tips article explicitly calls out DPM++ 2M Karras as the go-to quality sampler. ([comfyuiweb.com][4])

#### Concrete ComfyUI presets

**Flux.1 Dev – “Safe default” (portraits / general work)**

* **Sampler**: `euler` (or `Samueler (Euler)` equivalent in SamplerCustom)
* **Scheduler**: `simple` or `normal`
* **Steps**: 24–28
* **CFG**: `1.0`
* **FluxGuidance / Distilled CFG scale**: `3.0–3.8` for photorealism, `4.5–5.5` for stylised / illustration. ([andreaskuhr.com][2])
* **Denoise**: `1.0` for pure txt2img

**Flux.1 Dev – “High detail” (slower, sharper)**

* **Sampler**: `dpmpp_2m_sde`
* **Scheduler**: `karras`
* **Steps**: 28–32
* **CFG**: `1.0`
* **FluxGuidance**: `3.0–4.0`

**Flux.1 Dev – “Fast draft”**

* **Sampler**: `euler`
* **Scheduler**: `simple`
* **Steps**: 16–18
* **CFG**: `1.0`
* **FluxGuidance**: `2.5–3.0`

<hr style="height:2px;border-width:0;color:pink;background-color:pink">




### FLUX.1 Kontext Dev

**image editing specialist**

**What it is**
Kontext is an image+text editing model: you give it an input image and an instruction (“change the car to red, keep composition and person identical”) and it does targeted edits. ([NVIDIA Developer][5])

Architecturally it’s still Flux1-ish, so **the same sampler logic applies** – it’s just optimised for *lower denoise* image-to-image.

**Official / community hints**

* Comfy / Forge guides treat it like other Flux models: **Euler + Simple** is the “reliable baseline”. ([GitHub][6])
* BFL’s preferred resolutions list still applies (832×1248, 1024×1024, 1184×880, 1216×832, etc.). ([GitHub][6])

#### Editing-oriented presets

**(ComfyUI I2I)**

**Kontext – “Targeted edit” (small changes, maximum character stability)**

* **Sampler**: `euler`
* **Scheduler**: `simple`
* **Steps**: 16–22
* **CFG**: `1.0`
* **FluxGuidance**: `2.5–3.5`
* **Denoise**: `0.25–0.45`

  * 0.25 if you only want colour / lighting tweaks
  * 0.35–0.45 for swapping backgrounds, clothes, etc.

**Kontext – “Heavier rework” (same person, new setting / wardrobe)**

* **Sampler**: `dpmpp_2m_sde`
* **Scheduler**: `karras`
* **Steps**: 22–26
* **CFG**: `1.0`
* **FluxGuidance**: `3.5–4.5`
* **Denoise**: `0.45–0.6`

Practical rule of thumb:

* If a face is drifting, **lower denoise** *before* you raise steps.
* If changes are too timid, bump **FluxGuidance** slightly rather than CFG.

<hr style="height:2px;border-width:0;color:pink;background-color:pink">





### FLUX.1 SRPO

**Tencent’s preference-tuned Flux**

**What it is**
SRPO isn’t a new architecture; it’s Flux.1-Dev fine-tuned with Tencent’s **Semantic-Relative Preference Optimisation** – essentially RL on human preference across the whole diffusion / flow trajectory. ([GitHub][7])

So, inference-wise it behaves like Flux.1 Dev with slightly different “taste”: more natural skin, fewer plastic-looking artifacts, especially on faces. ([Reddit][8])

**Sampler behaviour from early tests**

* Users report **Euler (normal) works well**, just like base Flux. ([Reddit][8])
* Some of the “it looks better” anecdotes came from **Euler + beta scheduler**, not from SRPO itself – i.e. scheduler choice still matters a lot. ([Reddit][8])

#### ComfyUI presets

*Suggested*

You can almost drop in your Flux.1 Dev settings and just lean a bit into realism:

**SRPO – “Realistic portraits”**

* **Sampler**: `euler`
* **Scheduler**: `beta` (or `simple` if you don’t want to fuss)
* **Steps**: 24–30
* **CFG**: `1.0`
* **FluxGuidance**: `2.8–3.5` (keep slightly lower than your illustration work)
* **Resolution**: stay near BFL-friendly sizes (e.g. 1216×832 or 1184×880)

**SRPO – “Max quality, still portraits / fashion”**

* **Sampler**: `dpmpp_2m_sde`
* **Scheduler**: `karras`
* **Steps**: 26–32
* **CFG**: `1.0`
* **FluxGuidance**: `3.0–3.8`

If it starts to look *too* crunchy or noisy:

* Drop **FluxGuidance** before you touch steps.
* If grain persists, try `euler` + `simple` instead of DPM++.

<hr style="height:2px;border-width:0;color:pink;background-color:pink">





### Qwen-Image

**DiT-style, text-savvy foundation model**

**What it is**
Qwen-Image is Alibaba’s 20B-parameter multimodal DiT diffusion model; open-sourced and meant as a general foundation model with strong multilingual text rendering and editing. ([ComfyUI][9])

Comfy’s official guide distinguishes:

* **Original fp8/bf16 model** – heavier, more steps.
* **Distilled model** – fewer steps, slightly lower fidelity.
* **Lightning LoRA (8-step)** – very fast, requires specific sampler config. ([ComfyUI][9])

The docs explicitly recommend:

* **Distilled Qwen-Image**: ~**15 steps**, **CFG 1.0**, works well even at 10 steps with CFG 1.0.
* For the distilled version, **Euler or res_multistep** are recommended samplers depending on the image type. ([comfyui-wiki.com][10])

There’s also a lot of community testing that leans on Euler + normal / Karras, similar to Flux. ([comfyuiweb.com][11])

#### ComfyUI presets

**Qwen-Image Distilled – “Official-ish” settings**
(from the ComfyUI wiki notes) ([comfyui-wiki.com][10])

* **Sampler**: `euler` *or* `res_multistep`
* **Scheduler**:

  * with `euler`: `normal` or `karras`
  * with `res_multistep`: use the matching multistep scheduler node if you have it; otherwise `karras` is fine
* **Steps**:

  * **15** (author-recommended)
  * **10** if you’re using it like a “lightning” model
* **CFG**: `1.0`

**Qwen-Image Full fp8 – “Quality” preset**

* **Sampler**: `dpmpp_2m_sde`
* **Scheduler**: `karras`
* **Steps**: 20–24
* **CFG**: `1.0–1.3` (you *can* push a tad above 1 here; it’s less fragile than Flux, but still hates SDXL-style 7–12 CFG)
* For tight text (signage, posters): lean `euler + karras, 18–20 steps`, still at **CFG 1.0**.

**Qwen-Image + Lightning 8-step LoRA**

* Enable the Lightning LoRA (`Qwen-Image-Lightning-8steps-V1.0`) and: ([comfyui-wiki.com][10])

  * **Steps**: `8`
  * **Sampler**: `euler`
  * **Scheduler**: `karras`
  * **CFG**: `1.0`

<hr style="height:4px;border-width:0;color:pink;background-color:pink">







## How to Pick

**between them in practice**

Given your setup (ComfyUI, 4060 Ti 16GB, character-focused work):

* **Character portraits / realistic women**

  * Start with **Flux.1 SRPO**, `euler + beta`, 24–28 steps, CFG 1.0, FluxGuidance ~3.2.
  * If it feels “too Flux-pretty” / plastic, nudge guidance *down* a bit rather than up.

* **Multi-lingual text on images (posters, covers, signage)**

  * **Qwen-Image (distilled)**, `euler + karras`, 15 steps, CFG 1.0. It’s simply better at text layout. ([comfyui-wiki.com][10])

* **Complex edit chains on a favourite render** (hair, setting, outfit swaps while keeping “your girl” consistent)

  * **Flux.1 Kontext**, denoise 0.3–0.45, `euler + simple`, 18–22 steps.

* **Weird stylised / painterly stuff**

  * Either **Flux.1 Dev** or **Qwen-Image fp8** with `dpmpp_2m_sde + karras`, slightly higher FluxGuidance (4–5) or CFG (1.2–1.4 for Qwen).

---

If you like, next step I can sketch **a tiny SamplerCustomAdvanced “matrix” workflow** for you: one input model (say SRPO) feeding three or four parallel sampler/scheduler combos so you can eyeball differences on your favourite test prompt in one go.

[1]: https://medium.com/%40furkangozukara/decoding-the-shift-and-diffusion-models-training-like-qwen-image-flux-sdxl-and-more-f96be44fedef?utm_source=chatgpt.com "Decoding the Shift and Diffusion Models Training ..."
[2]: https://andreaskuhr.com/en/flux-ai-guide.html "The Flux AI guide: installation, models, prompts and settings"
[3]: https://www.reddit.com/r/StableDiffusion/comments/1fmcrfi/i_tried_all_samplerscheduler_combinations_with/?utm_source=chatgpt.com "I tried all sampler/scheduler combinations with flux-dev-fp8 ..."
[4]: https://comfyuiweb.com/posts/essential-comfyui-tips-and-tricks?utm_source=chatgpt.com "25 Essential ComfyUI Tips and Tricks to Master AI Image ..."
[5]: https://developer.nvidia.com/blog/optimizing-flux-1-kontext-for-image-editing-with-low-precision-quantization/?utm_source=chatgpt.com "Optimizing FLUX.1 Kontext for Image Editing with Low- ..."
[6]: https://github.com/DenOfEquity/forge2_flux_kontext?utm_source=chatgpt.com "DenOfEquity/forge2_flux_kontext"
[7]: https://github.com/Tencent-Hunyuan/SRPO?utm_source=chatgpt.com "Directly Aligning the Full Diffusion Trajectory with Fine- ..."
[8]: https://www.reddit.com/r/StableDiffusion/comments/1ndbdi9/srpo_a_fluxdev_finetune_made_by_tencent/?utm_source=chatgpt.com "SRPO: A Flux-dev finetune made by Tencent."
[9]: https://docs.comfy.org/tutorials/image/qwen/qwen-image "Qwen-Image ComfyUI Native Workflow Example - ComfyUI"
[10]: https://comfyui-wiki.com/en/tutorial/advanced/image/qwen/qwen-image "Qwen-Image ComfyUI Native, GGUF, and Nunchaku Workflow Complete Usage Guide | ComfyUI Wiki"
[11]: https://comfyuiweb.com/tutorials/comfyui-beginners-guide?utm_source=chatgpt.com "ComfyUI Beginner's Ultra-Detailed Guide"

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Clothing Only

Ohhh, *that* is a fun use for Kontext 😈—a wardrobe archive without the inconvenient human attached.

Yes, absolutely, you can send me your workflow.
If you paste the JSON (or a screenshot plus node list), I can walk through:

* where the **input image** goes,
* how the **instruction text** is wired,
* which node is actually doing the Kontext call,
* and whether **denoise / guidance / masks** are sabotaging your “remove the woman” request.

Since you haven’t pasted it yet, let me give you some likely culprits up-front so you can already sanity-check your graph:

---

### How Kontext Thinks

**about “remove the person”**

Kontext is *much* happier with instructions like:

* “Make the woman disappear and show only the dress on a white background.”
* “Remove the woman and leave only the costume on a mannequin, plain studio white background.”
* “Replace the woman with empty space; keep only the clothes on a white backdrop.”

Purely negative commands like **“remove the woman”** can be too vague:

* What should go *in her place*?
* Do we keep the clothes floating? Replace with background? Mannequin? Floor?

So: **always tell it what the final image should look like**, not just what to delete.

---

### Denoise

**the #1 reason edits don’t “take”**

For Kontext in ComfyUI, if you’re doing image-to-image:

* **Denoise too low (≤0.25)** → the model barely touches the image; your woman stays.
* **Good range for removal / strong edit**: `0.45–0.65`

  * 0.45–0.5 → medium change (pose/wardrobe tweaks).
  * 0.55–0.65 → aggressive change (remove subject, change background, etc.).

So if your current chain is something like:

> Kontext → SamplerCustomAdvanced → VAE Decode

check what **Denoise** value you’re feeding into the sampler. If it’s 0.2-ish, Kontext is obeying you but the sampler simply won’t let it overwrite the base image.

---

### Guidance

**Flux-style low, but not TOO low**

Because Kontext is Flux-based:

* **CFG scale in the sampler** should be around `1.0`
* Any extra “Flux guidance” / “Edit guidance” scale:

  * Try starting at `3.0–3.5`
  * If the woman isn’t removed enough → nudge that to `4.0–4.5`
  * If things go chaos / weird → back it down again

If you’re using one of those combined “Flux denoiser / guider” nodes, I’ll need to see which slots you’re filling, but the rule of thumb is:

> Don’t crank CFG like SDXL; **keep it low and move the model-specific guidance instead**.

---

### Masking vs Global Edit

Depending how your workflow is built:

* If you **don’t use a mask**, Kontext has to reinterpret the *whole* image. That can work, but it may only *soften* the person instead of truly removing them.
* A stronger pattern for “remove the woman, keep costume” is:

  1. Use a segmentation / manual mask that covers **the body and head** but *not* the clothes you want to preserve.
  2. Run **only that region** through Kontext with something like:

     > “Remove the woman’s body and leave only the clothes, on a plain white background.”
  3. Composite back into original or onto a fresh background.

If your graph sends the **entire image + no mask** into Kontext with a vague instruction, it’ll often lean toward “style shift” rather than truly deleting the person.

---

### Prompt style

**...that usually works better for this**

When you send your workflow, I’ll adapt this precisely, but you can already try:

> **Instruction / positive prompt** (Kontext text input):
> “Remove the woman’s body and face and leave only her clothes, as if they are neatly arranged on a mannequin, on a clean white studio background. The costume should be fully visible, no human skin, no head, no hands or feet.”

And avoid using **negative text** (“no woman, no person, no head”)—Flux-style models don’t really use a true negative prompt channel.

---

If you paste your workflow next, I’ll go node-by-node and tell you:

* which node should handle the Kontext call,
* whether the **connections** are right,
* where to set **denoise / guidance**,
* and how to tweak the prompt so the poor woman actually vanishes and leaves you a tidy costume shot.



<hr style="height:24px;border-width:0;color:pink;background-color:pink">

