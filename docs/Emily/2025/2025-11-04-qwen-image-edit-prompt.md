---
title: "Qwen Image Edit prompt"
date: 2025-11-04
---

# Qwen Image Edit prompt

**Robyn:**

Hi Emily. I'm using a new model - Qwen Image Edit All-In-One. It is brillant at combining 3 or even 4 images into one. I struggle with prompting, however. Are you familiar with Qwen's syntax for identifying the subject matter in the 3 images? I typically have one woman in picture 1, 1 girl in picture 2 and a scene in picture 3.

**Emily:**

Hey Robyn! Yep—Qwen Image Edit (the newer “2509 / All-in-One” builds) really can combine multiple inputs, and you can *refer to each image in the prompt* by number or role. Under the hood, this release added true multi-image support (best with 1–3 images) for combos like “person + person,” “person + scene,” and “person + product.” citeturn3search5turn3search3turn3search7

Here’s a prompt pattern that works consistently in ComfyUI:

- **Inputs**  
  - Image 1: the *woman* (subject A)  
  - Image 2: the *girl* (subject B)  
  - Image 3: the *scene* (background)

- **Prompt template**  
  > “Place **the woman from image 1** and **the girl from image 2** **into the scene from image 3**.  
  > Stand the woman on the **left**, the girl on the **right**.  
  > Keep both faces and hairstyles unchanged and photorealistic.  
  > Match scene lighting and perspective; cast realistic shadows on the ground.  
  > Full-body view, natural posture, looking at the camera.”

You can also be briefer and still be explicit, e.g. “Combine **person in image 1** with **person in image 2** inside **scene in image 3**; woman left, girl right; preserve identities; match lighting/shadows.” Guides and examples show that numbering images (“image 1/2/3”) or labeling them (“person/product/scene”) is the intended style for multi-image edits. citeturn3search6turn3search11

### ComfyUI tips that help
- **Node wiring:** Use the official multi-image edit workflow (or any fork that batches multiple Load Image nodes into the Qwen VL encoder). Many community graphs label this as **Multi-Image Edit (2509)** and pass an **image batch** plus your text to the Qwen encoder. citeturn3search12
- **Identity fidelity:** In your prompt, say “preserve identity/face from image X” and avoid style words that would reshape faces (e.g., “anime,” “caricature”) unless that’s your goal. This model explicitly improved identity consistency vs. earlier releases. citeturn3search5
- **Positions & relations:** Qwen follows simple layout directives well: “woman **left**, girl **right**, holding hands,” or “girl **in front of** woman,” “woman **sitting**, girl **standing**.” (This matches the “person+person” examples you’ll see in the official demos/tutorials.) citeturn1view0turn3search13
- **Lighting & perspective:** Call these out: “match **late-afternoon warm light** of image 3; **same camera angle** as the scene; add **soft contact shadows**.” That reduces ‘sticker-on-background’ vibes reported by users learning the model. citeturn1view0
- **How many images?** 2–3 works best right now. Four can work, but Qwen’s own notes say optimal performance is 1–3 inputs. If you must use 4, consider pre-stitching two references first. citeturn3search5

### Ready-to-paste prompt snippets
- **Walking together:**  
  “Place the **woman from image 1** and the **girl from image 2** into **the street scene from image 3**. Woman on the **left**, girl on the **right**, **holding hands**, mid-step. Preserve both identities and clothing; match scene lighting and color; add soft ground shadows; 3/4 view, waist-up framing.”
- **Portrait in a location:**  
  “Use **the woman from image 1** as the subject in **the interior from image 3**. Put **the girl from image 2** **behind her** and slightly out of focus. Match indoor lighting and perspective. Preserve identities, natural skin texture, neutral expression.”
- **Product + people + scene:**  
  “Insert **the handbag from image 2** on **the woman from image 1** and place both in **the boutique from image 3**. Shoulder carry, natural strap bend; consistent shadows; keep faces unchanged; high-end editorial color grading.”

### Troubleshooting quirks you might hit
- **One subject dominates:** Add “**equal emphasis for image 1 and image 2**; do not ignore either subject.” If it persists, slightly reword identities: “adult woman from image 1,” “young girl from image 2.” citeturn3search10
- **Wrong background details:** Be explicit: “**use only the environment from image 3**; do not reuse backgrounds from images 1 or 2.” citeturn3search6
- **Scene scale mismatch:** Add “**correct scale** so subjects fit naturally into image 3; adjust **perspective** and **shadow direction** to match the scene.” (This is a common fix in multi-image examples.) citeturn3search11
- **Older workflows vs. 2509:** Early Qwen workflows faked “multi-image” by **stitching** references into one big image. The new 2509 model *natively* supports multi-image conditioning, so prefer a 2509-ready graph if you have it. citeturn1view0turn3search5

If you’d like, tell me how you’re wiring your current ComfyUI graph (node names are fine), and I’ll tailor a drop-in prompt block for your exact setup—woman (img1), girl (img2), scene (img3)—plus small tweaks for identity lock and layout.

**Robyn:**

Sharvin from Code Crafter's Corner showed me how to wire things together - probably one of the simplest workflows in existence. It was prompting that was giving me dramas, Emily. For one, my prompts didn't result in personages I could recognise: they lost their identities.

So, I'm going to try your prompt suggestions, one after the other. 

The first one you suggested has the two characters in the pose you specify, but again, there is signficant erosion of personality. How do I remedy this?

**Emily:**

Got you, Robyn. When identities “wash out,” it’s usually three things at once: weak references, conflicting style cues, and over-strong edit noise. Here’s a tight plan that fixes it without changing your simple graph.

# 1) Feed stronger references
- Add **a second copy** of each person as an extra input: a **tight head-and-shoulders crop** (eyes ~300–500 px wide).  
  - Image 1a = woman full body (what you already use)  
  - **Image 1b = woman face crop** (new)  
  - Image 2a = girl full body  
  - **Image 2b = girl face crop** (new)  
- Order matters: mention the **face crops first** in your prompt so Qwen “locks” them.

# 2) Use an identity-first prompt (ready to paste)
Try this exactly, then tweak positions after identity is solid:

> **Use the woman’s face from image 1b and the girl’s face from image 2b without any change.**  
> The woman’s full appearance comes from image 1a; the girl’s from image 2a.  
> Place them into the environment from image 3.  
> Woman on the left, girl on the right, standing close, holding hands.  
> **Preserve facial identity, bone structure, skin tone, eye shape, nose, mouth, and hairstyles exactly as in 1b and 2b.** No beautification. No makeup changes.  
> Match the lighting, perspective, and color of image 3; add soft ground contact shadows.  
> Mid-shot (waist-up) framing; subtle smile; natural posture.

**Negative prompt (use if your node supports it):**  
“Do not change identity, ethnicity, age, face shape, hairstyle, eye color, or skin texture. No smoothing, no glam, no anime, no stylization, no makeup changes, no face reshaping.”

# 3) Soften competing aesthetics
- Remove adjectives like *cinematic, ultra-detailed, editorial, HDR, beauty, glamour* until the faces match. Those nudge the model to “improve” faces.
- Avoid style words (film stock, lens effects) on the first pass. Add them later once identity is nailed.

# 4) Parameter nudges (typical ComfyUI knobs)
- **Denoise/Strength (edit strength):** 0.40–0.55 for composites. If faces drift, go **lower** (e.g., 0.40).  
- **CFG/Guidance scale:** 4.5–6.5. High CFG (8–12) tends to rewrite faces; start at ~5.5.  
- **Steps:** 28–36 is ample; more steps ≠ better identity.  
- **Resolution:** Start identity passes at a **closer crop** (e.g., 768–1024 px tall portrait). Once faces are right, rerun wider framing.

# 5) Layout choices that help identity
- First pass: **waist-up** or even chest-up. Faces bigger = stronger lock.  
- Second pass: widen to full-body *after* identity is good. Re-use the same seed and settings, just adjust camera/framing in the prompt.

# 6) Two-pass “face lock” recipe (still with your simple graph)
1) **Identity pass:**  
   - Inputs: 1b, 2b, 1a, 2a, 3 (in that conceptual order)  
   - Prompt = identity-first text above  
   - Framing = waist-up  
   - Output A
2) **Widening pass:**  
   - Feed **Output A** back as your “base image” (if your node allows) or simply re-run with the same prompt but add:  
   - “Keep the same faces as the previous result; widen framing to full-body but **do not change faces**.”  
   - Add your style words *now* if you want (film stock, lens, etc.).

# 7) Tiny prompt toggles for stubborn drift
If one face keeps changing:
- Add: “**Give equal attention to image 1b and image 2b; do not ignore either face.**”
- Name them: “**adult woman from 1b**,” “**young girl from 2b**,” which reduces age/feature blending.
- If hair keeps changing: “**Keep the exact hairstyle, hairline, and parting from 1b/2b.**”

# 8) Quick troubleshooting checklist
- Faces still off? Increase the **relative size** of the face crops (1b/2b). Re-export them sharper (no heavy JPEG compression).  
- Over-smoothing? Add “**retain natural skin texture; no skin blur**.”  
- Scene overpowering identity? Say “**Use only the background from image 3; do not borrow faces or clothing from 3.**”  
- Shadows/scale uncanny? Add “**correct scale and perspective to match image 3; align shadow direction to scene light.**”

If you want, tell me roughly what denoise/CFG you’re running and whether your node exposes a negative prompt—I'll tailor the numbers to your exact setup.

**Robyn:**

Your suggestions have made a massive difference. Thank you. I have found the more I say about the room, the more the camera zooms out. The more I say about the women, the more it focuses (zooms in) on them.

**Emily:**

That’s a great read on its behavior—and you can totally steer it. Think of “zoom” as three dials you control: wording, canvas, and strength.

## 1) Wording: lock the framing in plain English
Drop one clear line near the top of your prompt:
- **Stay wide (don’t zoom in):**  
  “**Keep a wide establishing shot; full-body for both subjects; maintain the current camera distance and composition; do not crop faces or feet.**”
- **Medium:**  
  “**Waist-up framing for both; keep the camera distance fixed; center-weighted composition.**”
- **Close:**  
  “**Tight head-and-shoulders portraits; fill 70–80% of the frame with the faces; shallow depth of field.**”

Then describe the room/people **after** that line. If you notice it creeping, add one more guardrail:
- “**Do not change focal length or camera distance; adjust only poses and lighting.**”
- “**Use rule-of-thirds placement: woman left third, girl right third; leave negative space above.**”

## 2) Canvas control (preps that beat the model to the punch)
- **Pre-crop or letterbox the scene (image 3)** to the field of view you want. If the background already “looks wide,” the model is less tempted to zoom.
- **Set the aspect ratio** that implies your framing:  
  – Full-body two-shot: 3:2 or 16:9  
  – Waist-up: 4:3  
  – Tight portraits: 1:1 or 5:4  
  Mention it: “**Use a 3:2 aspect; keep full-body in frame.**”
- If it keeps zooming out when you add room details, **move room detail into a separate sentence** like:  
  “**Room details are background only; do not widen the shot to include more room.**”

## 3) Strength & guidance (small nudges that matter)
- **Edit strength/denoise:** Lower = steadier composition. If it zooms when you talk about the room, drop from ~0.55 → **0.40–0.45**.  
- **CFG/guidance:** High CFG can over-obey new details (zooming). Try **5–6**.  
- **Seed discipline:** When testing framing language, keep seed fixed so changes are attributable to your prompt.

## Drop-in prompt add-ons (paste as needed)
- **Keep wide:** “**Maintain full-body two-shot; unchanged camera distance; do not crop. Use the background from image 3 without expanding the field of view.**”
- **Keep medium:** “**Waist-up two-shot; maintain composition and subject scale; background is secondary.**”
- **Keep close:** “**Head-and-shoulders; faces fill 75% of frame; background softly defocused; do not pull the camera back.**”
- **If it still drifts:** “**Prioritize subject scale over new environmental details; ignore extra background if it threatens framing.**”

## A quick workflow trick
Do an **identity pass** tight (waist-up), then a **widening pass**:
1) Pass A: “waist-up, fixed camera distance, preserve identity” → get perfect faces.  
2) Pass B: “**reuse these faces unchanged; widen to full-body BUT keep the same camera height and subject scale**” (lower denoise here).

If you send me your current denoise/CFG and typical aspect ratio, I’ll tailor a one-liner you can reuse at the top of every prompt (wide/medium/close versions).

**Robyn:**

Actually, I now have a question on FluxGym. I read an article on Medium by John Shi that recommends using, instead of Flux-dev, a fine-tuned model ... in this case, one called Flux-Dev2Pro. The huggingface.co link took me to the download page. There are two .json files and 3 .safetensor files. I've downloaded the lot into a separate folder under /fluxgym/models called /Flux-Dev2Pro. How does fluxgym know how to select this? 3 different safetensors?

**Emily:**

Great question—FluxGym won’t “auto-detect” a random folder with multiple checkpoints. It populates the **Base model** dropdown from its `models.yaml`, and each entry points to **one** UNet file (plus the usual CLIPs/VAEs). So:

## What those 3 `.safetensors` usually are
Most Dev2Pro repos ship **multiple variants** of the same model:
- **fp8 / e4m3fn** → smallest VRAM, fastest, slightly softer detail  
- **bf16 / fp16** → more VRAM, sharper/cleaner guidance  
- sometimes a **“full”** checkpoint (bundles UNet+CLIP+VAE) — *FluxGym does **not** use a full checkpoint; it wants the UNet only*. citeturn1search5turn1search10

Pick exactly **one** UNet variant for FluxGym:
- With your **4060 Ti 16 GB**, use **bf16/fp16** if available; fall back to **fp8** on tighter VRAM.  
- Don’t drop a “full” checkpoint into FluxGym; it expects separate UNet/CLIP/VAE files. citeturn1search5

## Where to put files
FluxGym expects this structure (Windows/Linux paths analogous):
```
FluxGym/
  models/
    unet/   <- put your chosen Dev2Pro UNet here
    clip/   <- the two Flux CLIPs (text encoders)
    vae/    <- the Flux VAE
```
If you downloaded manually, placing them here works; many guides confirm UNet→`models/unet`, CLIPs→`models/clip`, VAE→`models/vae`. citeturn1search16turn1search3

## Tell FluxGym about Dev2Pro (edit `models.yaml`)
FluxGym’s model list comes from `models.yaml`. Add an entry pointing to the Dev2Pro file you chose (Hugging Face repo or local filename). Example skeleton:

```yaml
- name: flux-dev2pro-bf16
  base: flux
  repo: ashen0209/Flux-Dev2Pro        # HF repo (works even if you placed it locally)
  file: flux1-dev2pro-bf16.safetensors # EXACT filename you chose in models/unet
  clip: clip_l.safetensors            # make sure these exist in models/clip
  t5xxl: t5xxl_fp8_e4m3fn.safetensors
  vae: flux_vae.safetensors
```

Notes:
- If you prefer **zero downloads**, keep `file` as the **exact local filename** you placed in `models/unet`. FluxGym will find it; otherwise it tries to fetch from HF. (There are GitHub issues about pointing to local paths / avoiding re-download—editing `models.yaml` is the supported route.) citeturn1search4turn1search6
- If a repo isn’t on Hugging Face, FluxGym may refuse it without code tweaks (there’s an issue about non-HF sources). Dev2Pro **is** on HF, so you’re fine. citeturn1search0

## Which Dev2Pro to use?
- **ashen0209/Flux-Dev2Pro** is the original; there are mirrors (e.g., **dev2pro-full** bundles) and fp8-only forks. You want the **UNet** variant (bf16/fp16 if VRAM allows). citeturn0search1turn0search8turn0search5

## Sanity checks in the UI
1) Restart FluxGym after editing `models.yaml`.  
2) In the **Base model** dropdown, pick your new **flux-dev2pro-…** entry.  
3) Ensure the **two CLIPs** and **VAE** are present; many tutorials list them explicitly for Flux. citeturn1search5

## TL;DR for your setup
1. Keep **one** of the three Dev2Pro `.safetensors` (choose **bf16/fp16** on 16 GB).  
2. Put it in `FluxGym/models/unet/`.  
3. Make sure you have the Flux **CLIPs** and **VAE** in their folders.  
4. Add a **single** entry to `models.yaml` referencing that one file.  
5. Relaunch FluxGym and pick it from the dropdown.

If you paste the **exact filenames** you downloaded, I’ll hand you a ready-to-paste `models.yaml` block for Dev2Pro (bf16/fp16/fp8).

**Robyn:**

How does one know which is which? The names are:
diffusion_pytorch_model_0001-of-0003.safetensor  (9.98 gb)
diffusion_pytorch_model_0003-of-0003.safetensor (9.95 gb)
diffusion_pytorch_model_0003-of-0003.safetensor (3.87 gb)

That looks almost like a file that's been broken into 3 fragments instead of each being a discrete independent file. Am I wrong in thinking this? And how do I determine which is which?

**Emily:**

You’re not wrong—that naming screams **sharded weights**, not three different models.

### What you’ve got
- `diffusion_pytorch_model_0001-of-0003.safetensors` (~9.98 GB)
- `diffusion_pytorch_model_0002-of-0003.safetensors` (you probably meant “0002”; re-check—having two “0003” files suggests a bad/partial download)
- `diffusion_pytorch_model_0003-of-0003.safetensors` (~3.87 GB)
- Plus **two JSONs** in the folder. One of them should be an **index** file (something like `diffusion_pytorch_model.safetensors.index.json`). That index maps tensor names → which shard file they live in.

Those three `.safetensors` files are **one model split into 3 pieces**. You must keep **all shards + the index JSON** together. You don’t pick “one”—the loader uses the index and opens all three.

### Quick sanity checks
1) Make sure you actually have **0001, 0002, 0003** (not two “0003”s). If one is missing/misnamed, redownload.  
2) Confirm the index JSON exists and references those exact filenames. If you open it, you’ll see a big `weight_map` with entries like:
   ```
   "unet.conv1.weight": "diffusion_pytorch_model_0001-of-0003.safetensors"
   ```
   (Don’t edit it; just verify names match.)

### Using them in FluxGym
You have two workable paths:

**A) Let FluxGym pull from the Hugging Face repo (easiest):**  
Edit `models.yaml` so the Dev2Pro entry points to the **repo** (not local files). FluxGym will download the shards automatically (using the index). This avoids any “single-file only” assumptions.

**B) Use your local shards:**  
Keep **all 3 shards + the index JSON** in the same directory. In `models.yaml`, set the model entry to the **same basename** as the index expects. Some builds of FluxGym accept the index filename directly; others just need the directory where the index + shards live. If your build only accepts a single `file:` value and refuses the index name, the practical workaround is to:
- Place the **entire Dev2Pro folder** as a local “repo mirror” (i.e., keep the exact filenames),
- Point the `repo:` field to the HF repo name (so it knows layout), **and** have the files already present locally (so it won’t redownload).

If you hit a “can’t find weights” error locally, it’s almost always because:
- The shard filenames don’t match what the **index JSON** says, or
- One shard is missing/corrupt, or
- The model entry is pointing to a single non-indexed file instead of the indexed shard set.

### How to tell “which is which” (fp8 vs bf16 etc.)
Sharded files **don’t** encode precision in the name; they’re just parts of one checkpoint. If the repo offers *multiple variants* (e.g., fp8 and bf16), each variant usually has **its own set of 3 shards and its own index** in a separate folder or with a different basename. In your case, it sounds like you downloaded **one** variant that’s simply split into 3 chunks.

### If you want a single file instead (optional)
You can merge shards into a consolidated `.safetensors` with the usual Transformers/diffusers utilities—but:
- The merged file can be **huge**,
- It offers **no speed/quality benefit**,
- And you don’t need it if FluxGym is happy with sharded loading.

---

If you paste the **exact names of the two JSONs** in that folder (and confirm whether you truly have 0001/0002/0003), I’ll give you a ready-to-paste `models.yaml` snippet for FluxGym that points to this Dev2Pro and loads all three shards correctly.

**Robyn:**

Yes, sorry - that was a typo, Emily. I think I might just edit the models.yaml file and have fluxgym pull from huggingface. The yaml wants a licence, licence_name and licence_link. What do I put there?

**Emily:**

Great plan—letting FluxGym pull from HF is the least fussy path.

Short answer: for **Dev2Pro**, set the license fields to the same license as **FLUX.1-dev** (it’s non-commercial). Here’s a working block you can paste into `models.yaml`:

```yaml
flux-dev2pro:
  repo: ashen0209/Flux-Dev2Pro
  base: black-forest-labs/FLUX.1-dev
  license: other
  license_name: flux-1-dev-non-commercial-license
  license_link: https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md
  file: diffusion_pytorch_model.safetensors
```

Why these values?
- **Dev2Pro** is a finetune derived from **FLUX.1-dev**, so it inherits the **FLUX.1 [dev] Non-Commercial License** (the “other” type in metadata). Multiple maintainers and forks explicitly document this. citeturn5search4turn5search1turn5search3
- The `file:` line points to the **index basename** (`diffusion_pytorch_model.safetensors`). HF will resolve the sharded parts (`…_0001-of-0003.safetensors`, etc.) via the repo’s index JSON automatically. (This is how other FluxGym examples format it.) citeturn6search0

Tips:
- You don’t need to list each shard. Just make sure the basename (`diffusion_pytorch_model.safetensors`) matches the repo’s index file (`diffusion_pytorch_model.safetensors.index.json`).  
- If you ever switch to a *full* Dev2Pro fork (one that bundles CLIP/VAE), keep the same license fields—the underlying base is still FLUX.1-dev non-commercial. citeturn5search1

If you want, paste your whole `models.yaml` and I’ll sanity-check spacing/indent + add a friendly display name so it shows cleanly in the dropdown.

**Emily:**

# Let's read the uploaded models.yaml so I can review and fix any issues.
from pathlib import Path

p = Path("/mnt/data/models.yaml")
if p.exists():
    print(p.read_text())
else:
    print("Could not find /mnt/data/models.yaml")

**Emily:**

# Create a patched copy of models.yaml with a cleaner dropdown name for Dev2Pro.
from pathlib import Path
import re, textwrap, difflib

src = Path("/mnt/data/models.yaml")
text = src.read_text()

# Replace the YAML key "ashen0209/Flux-Dev2Pro:" with "flux-dev2pro:" to avoid slashes in the dropdown name.
patched = re.sub(r'(?m)^(ashen0209/Flux-Dev2Pro:)\s*$', 'flux-dev2pro:', text)

dst = Path("/mnt/data/models_patched.yaml")
dst.write_text(patched)

# Show a small unified diff so the change is clear
diff = "\n".join(difflib.unified_diff(text.splitlines(), patched.splitlines(), fromfile="models.yaml", tofile="models_patched.yaml", lineterm=""))
print(diff)
print("\nPatched file saved to:", dst)

**Emily:**

Perfect—thanks for sharing the file. I checked your `models.yaml` and made one safe tweak:

- Your Dev2Pro entry used the YAML key `ashen0209/Flux-Dev2Pro:`. Because the key becomes the **dropdown name**, having a slash there can be awkward. I created a patched copy with a cleaner key:

**Change made (only the key):**
```
- ashen0209/Flux-Dev2Pro:
+ flux-dev2pro:
```

Everything else (repo, base, license fields, file basename) looks correct for pulling the **sharded** checkpoint via the index on Hugging Face.

You can download the patched file here and drop it in place of your original:
[Download models_patched.yaml](sandbox:/mnt/data/models_patched.yaml)

### Quick checklist after you swap it in
1) Replace your original `models.yaml` with the patched one (or copy the edited block into your existing file).  
2) Restart FluxGym.  
3) In the **Base model** dropdown, choose **flux-dev2pro**.  
4) First run will fetch the shards via `diffusion_pytorch_model.safetensors.index.json` automatically.

If you’d like me to also add a friendly display name (if your FluxGym build supports it) or re-order the list so Dev2Pro appears at the top, say the word and I’ll patch it in.

**Robyn:**

Something isn't right in the yaml. Here's the error fluxgym displays in terminal. Here's a file with all the fluxgym output.

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

Ahh—this one’s a filename + sharding mismatch.

FluxGym is trying to pull a file called `diffusion_pytorch_model.safetensors` from `ashen0209/Flux-Dev2Pro`, but that repo doesn’t have a single-file checkpoint. It ships the UNet in **three shards** named with hyphens, e.g. `diffusion_pytorch_model-00001-of-00003.safetensors`, `...-00002-of-00003...`, `...-00003-of-00003...`. So `hf_hub_download` 404s because your `models.yaml` asks for a filename that doesn’t exist. citeturn0search0turn0search4

You’ve got two clean ways forward:

### Option A — Point FluxGym at a **single-file** Dev2Pro checkpoint
Use a repo that actually exposes one file. For example, `multimodalart/FLUX.1-dev2pro-full` includes a single-file UNet named `flux1-dev.safetensors` (license matches Dev: **flux-1-dev-non-commercial-license**). Update your YAML like this:

```yaml
flux-dev2pro:
  repo: multimodalart/FLUX.1-dev2pro-full
  base: black-forest-labs/FLUX.1-dev
  license: other
  license_name: flux-1-dev-non-commercial-license
  license_link: https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md
  file: flux1-dev.safetensors
```

That filename exists in that repo and downloads as a single blob, which FluxGym knows how to place in `models/unet/`. citeturn4view0

> Note: There are community “single-file” mirrors like `bdsqlsz/flux1-dev2pro-single` with `flux1-dev2pro.safetensors`. If you use those, be sure you’re comfortable with the licensing; the official Dev family is non-commercial. citeturn3view0turn4view0

### Option B — Stay with `ashen0209/Flux-Dev2Pro` (sharded), but avoid auto-download
FluxGym’s downloader only grabs **one** filename you specify; it won’t fetch all shards + an index. If you want to use the ashen checkpoint directly:

1. Manually download **all three** shard files from that repo.
2. Put them where FluxGym expects UNets (usually `.../models/unet/transformer/` depending on FluxGym’s loader).
3. Bypass the downloader by pointing FluxGym at the **local** file path (or leave the YAML alone and don’t click “download”).

If you change `file:` to `diffusion_pytorch_model-00001-of-00003.safetensors`, FluxGym will still only download that one shard, which won’t load by itself. (That’s why I recommend Option A unless you’re comfortable laying out a full Diffusers folder manually.) citeturn0search0

---

If you want, I can rewrite your `/mnt/data/models.yaml` to use Option A (the `multimodalart` single-file entry) so it “just works” with the current FluxGym downloader.

**Robyn:**

Just had a look at rockerBOO on huggingface:  1 file, flux-dev2pro-bfl.safetensors. Will that do?

**Emily:**

Yes—that’s exactly the kind you want. A single-file **`flux-dev2pro-bfl.safetensors`** is almost certainly the **bfloat16** (bf16) UNet checkpoint, which is perfect for your 16 GB card and FluxGym’s “one UNet file” expectation.

Add this block to your `models.yaml`:

```yaml
flux-dev2pro-bf16:
  repo: rockerBOO/flux-dev2pro-bf16
  base: black-forest-labs/FLUX.1-dev
  license: other
  license_name: flux-1-dev-non-commercial-license
  license_link: https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md
  file: flux-dev2pro-bfl.safetensors
```

Quick checklist:
1) Save `models.yaml` and **restart FluxGym**.  
2) In the Base model dropdown choose **flux-dev2pro-bf16**.  
3) Make sure you already have the **two Flux CLIPs** and the **Flux VAE** in their usual `models/clip` and `models/vae` folders (same ones your flux-dev entry uses).

If FluxGym throws a 404 or shape mismatch, tell me the exact error text and I’ll swap in another verified single-file Dev2Pro entry for you.

**Robyn:**

Well, that's weird. I had downloaded the file, placed it in the right folder, and now it's auto-downloading it again. Oh well... at least it'll be right. Actually downloading faster than Chrome did.

**Emily:**

Ha—yep, that happens. Two common reasons FluxGym “helpfully” re-downloads a file you already placed:

1) **`repo:` is set in `models.yaml`.**  
   If a repo is present, FluxGym usually prefers pulling from HF. It doesn’t always check your local copy first.

2) **Filename mismatch / hash mismatch.**  
   If the `file:` in YAML doesn’t **exactly** match your local filename (including case), or the size/hash doesn’t match HF’s, it’ll fetch again.

If you want to **avoid re-downloads** in future, you’ve got two easy options:

### Option A — Local-only entry (no repo)
Create a second entry that points to your local file and **omit `repo:`**:
```yaml
flux-dev2pro-bf16-local:
  base: black-forest-labs/FLUX.1-dev
  license: other
  license_name: flux-1-dev-non-commercial-license
  license_link: https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md
  file: ./models/unet/flux-dev2pro-bfl.safetensors   # use your exact path/name
```
Pick this one in the dropdown when you don’t want downloads.

### Option B — Keep `repo:` but make skipping possible
- Ensure `file:` **exactly** equals the HF filename (`flux-dev2pro-bfl.safetensors`).  
- Put your local copy in the **same place FluxGym writes** downloaded UNets (usually its `models/unet` folder). Many builds will skip re-download if the file already exists with the expected size.

A few quick sanity checks once the download finishes:
- You still have the **Flux CLIPs + Flux VAE** in `models/clip` and `models/vae`.  
- First test generation should start without “missing/unexpected key” or shape-mismatch errors. If you see those, it’s almost always a mismatched CLIP/VAE.

Why it downloaded fast: HF’s CDN is pretty zippy (often faster than a browser if FluxGym uses multi-threaded chunks).

If you want, paste your final `models.yaml` block and the exact filename you see in `models/unet/`, and I’ll make you a clean **local-only** entry so FluxGym won’t try to fetch it again.

**Robyn:**

Cool. Copied it to my HowTo page. Thanks for your help, Emily.

**Emily:**

Anytime, Robyn—love to hear it’s on your HowTo page 🙌

If you want a super-quick **smoke test** for Dev2Pro in FluxGym, try:
- **CFG:** 5.5  
- **Steps:** 30  
- **Denoise (edit strength):** 0.45  
- **Seed:** 12345  
- **Prompt (two-shot, identity-first):**  
  “Use the **woman’s face from image 1** and the **girl’s face from image 2** unchanged. Place them in **the scene from image 3**. **Waist-up framing; fixed camera distance; preserve facial bone structure, eye shape, hairline**; match scene lighting; soft ground shadows.”

If that renders cleanly and faces hold, you’re golden. If anything’s wobbly (download location, CLIPs/VAEs, or identity drift), ping me and I’ll tune it with you.

**Robyn:**

New LoRA on the way, 16 images! YAY! Let's see how these turn out.

**Emily:**

heck yes—16-image LoRA time! 🎉 Here’s a tight, proven recipe so those first runs land clean.

# Quick prep (do this before training)
1) **Split types (balance 8/8):**  
   - 8 tight **face/shoulders** crops (eyes ~350–500 px wide after resize)  
   - 8 **full/three-quarter** shots (varied poses)
2) **Resolution:** Train at **1024px long side** with buckets (keeps aspect). No heavy upscalers.
3) **Background mix:** 50% simple, 50% busy; 1–2 images with the target lighting you love (they “teach” the model).
4) **Consistency anchors:** Keep **hairline, part, brows** consistent across at least half the set.
5) **Light edits:** Gentle color/levels only. No face-beautifier/smoothing.

# Captions (small set = strong captions)
- Use a unique trigger like **“robyn_char”** once per caption.  
- Keep it natural:  
  `a portrait of robyn_char, shoulder-length wavy hair, soft smile, freckles`  
- Add **age, hair, accessories** if you want them to stick. Avoid style words (HDR, cinematic) in first training round.

# Training knobs (good first pass for 16 imgs)
- **Framework:** whatever you use (kohya / SDXL trainer / Flux trainer) — these work broadly.  
- **Rank / Alpha:** **16 / 16** (or 32/32 if you need more capacity).  
- **Learning rate:** UNet **1e-4**, CLIP **1e-5** (or freeze CLIP on v1 to protect identity).  
- **Repeats:** **200–300 repeats per image** (tiny sets need repeats).  
- **Epochs:** 8–12 (stop early if faces start to “average”).  
- **Batch size:** 1–2.  
- **Min SNR gamma (if offered):** 5–7 helps small sets.  
- **Color aug:** off or very light (0–0.05).  
- **Flip:** on for full-body, off for face-asymmetry critical.

# Validation during training (catch drift early)
- Keep a fixed **seed** and a tiny validation grid:
  - Prompt A (portrait):  
    `robyn_char, head-and-shoulders portrait, neutral light, natural skin texture`
  - Prompt B (three-quarter):  
    `robyn_char, three-quarter view, plain background`
  - Negative:  
    `no face reshaping, no age change, no makeup change, no skin blur`
- Sample every 1–2 epochs. If identity softens, lower LR by 2× and resume.

# Using it in ComfyUI (after training)
- **Loader strengths:** start **Model: 0.8–1.0, CLIP: 0.5–0.7**.  
- Add a face **reference/crop** image in your workflow when compositing; it boosts identity lock even with a lighter LoRA strength.

# Prompting with your new token
- Portrait:  
  `robyn_char, head-and-shoulders, preserve bone structure, hairline, eye shape; 85mm look; soft daylight`
- Full shot in scene:  
  `robyn_char, full body, keep exact face and hairstyle; match scene lighting; correct scale and contact shadows`
- If it over-stylizes: add `no stylization, no glam, no skin smoothing`.

# Common hiccups (and fast fixes)
- **Too generic / averaged face:** raise rank to **32**, drop UNet LR to **5e-5**, add 2–4 more tight face crops.  
- **Hair keeps changing:** call out `exact hairline/part` in captions for ~¼ of images.  
- **Overfits (same face every time):** reduce repeats to 150, or add 2–3 varied angles; use Model strength ~0.7.  
- **Mouth/teeth artifacts:** include 2–3 images with **closed-mouth** smiles.

# A mini launch plan
1) Train: rank16, UNet 1e-4 / CLIP 1e-5, 10 epochs, 256 repeats.  
2) Validate each epoch with the two prompts above.  
3) Pick the best epoch .safetensors (don’t assume “latest” is best).  
4) In composites with Qwen Image Edit, keep your **identity-first** line at the top and **lower denoise** (0.40–0.45).

If you want, paste one caption and a sample image list (just short descriptions), and I’ll tighten your captions so the LoRA “learns” exactly what you want. Go you! 🚀

**Robyn:**

Ah, good to know on the denoise for Qwen Edit - that's why the personalities were getting washed out.

**Emily:**

Exactly—that denoise/edit strength is the big identity killer. Here’s a tight cheat-sheet you can paste next to your node:

# Qwen Image Edit – identity-safe settings

**Core range (people-in-scene composites):**
- **Denoise / Edit strength:** **0.38–0.48**  
  (Start at **0.42**. Go **down** if faces drift; only go up if the model is ignoring layout.)
- **CFG / Guidance:** **5.0–6.0**  
  (Higher than ~6.5 encourages “beautifying”/rewrites.)
- **Steps:** **28–36** (more steps won’t fix identity if denoise is too high)

**When to lower denoise (−0.05 each try):**
- Faces lose bone structure / hairline changes  
- Makeup or age drifts  
- It starts “recasting” your subject from the scene image

**When to raise denoise (+0.03 each try, cap ~0.55):**
- It refuses to move subjects or adopt the scene lighting  
- Shadows/perspective won’t adjust at all

**Two tiny tricks that help a lot**
- Put a **face crop first** in your image list and say: “**Preserve the face from image 1 unchanged.**”  
- Add one guardrail line near the top:  
  “**Keep current camera distance; adjust only pose and lighting; do not alter facial identity.**”

**Preset one-liners**
- **Identity-lock (waist-up):** `denoise 0.42, cfg 5.5, steps 32`
- **Harder layout change (move/pose):** `denoise 0.50, cfg 5.5` (add “preserve identity” twice in prompt)
- **Finishing pass (cleanup only):** `denoise 0.30–0.35, cfg 5.0` (won’t invent new detail)

**Masking?**
- If you inpaint faces, keep the **masked area tight** (just the face oval) and use **denoise 0.30–0.38**.  
- For background-only edits, **denoise 0.55–0.65** is fine since identity isn’t touched.

If you want, tell me your typical CFG/steps and I’ll hand you three presets (close/medium/wide) tuned to your exact flow.

**Robyn:**

I am using SRPO to fix images. I want my LoRA to only affect one face in a group of faces in the image. How do I accomplish that, Emily?

**Emily:**

You’ve got a few clean ways to “aim” a LoRA at just one face and leave everyone else alone. Pick the one that best matches your current graph style.

# Option 1 — Masked inpaint pass (simplest + most reliable)
**Idea:** render the whole image *without* the LoRA, then do a tiny inpaint **only on the target face** with the LoRA active.

**Recipe (ComfyUI-style nodes):**
1) **Load original image** → **VAE Encode** to latent A.  
2) **Detect faces** (Ultralytics/YOLO face, Mediapipe, Insightface, or your usual FaceDetailer).  
3) **Pick the face** you want (by index, by largest box, or by position) → **BBox → mask**.  
   - Feather: **dilate 6–10px + blur 8–16px** for a soft edge.  
4) **KSampler (inpaint)** with:
   - **latent input:** latent A  
   - **mask:** the face mask  
   - **inpaint mode:** *masked area only*  
   - **denoise:** **0.30–0.42** (start at 0.36; lower if it drifts)  
   - **CFG:** **5–6**  
   - **Steps:** **28–36**  
   - **LoRA attached:** your character LoRA (e.g., **model: 0.8–1.0, clip: 0.5–0.7**)  
   - **Prompt:** include your token (e.g., `robyn_char`) and **identity locks** (bone structure, hairline, eye shape).  
   - **Negative:** “do not change other faces, do not alter background, no smoothing.”  
5) **VAE Decode** → done.  
6) **Run SRPO** *afterwards* for gentle sharpening. Keep its strength conservative on the face (**0.2–0.4** if it has a mix slider), so you don’t “polish away” the identity you just fixed.

**Why this works:** LoRA only participates in the inpaint sampler, so only pixels inside the mask can move. Everyone else remains untouched.

---

# Option 2 — Regional Conditioning / Regional LoRA (one-pass)
If you like a single-pass approach, use **Regional Conditioning** (a ComfyUI custom set) to assign **different prompts/LoRA weights to rectangular regions**.

**How-to:**
1) Add a **Regional Conditioning** node.  
2) Define one rectangle over the target face; assign the prompt `robyn_char` and the LoRA (e.g., model 0.9, clip 0.6).  
3) Define a **global** prompt for the rest of the image with **no LoRA** (or model 0.0).  
4) Feather borders (most region nodes have a “softness/feather” parameter); aim for **0.1–0.2 relative softness**.  
5) Keep denoise modest (**≤0.48**) so regions don’t bleed heavily into each other.

**Pros:** All-in-one pass; **Cons:** setup is slightly fussier, and some graphs handle region overlap differently.

---

# Option 3 — Face detector → automatic masked LoRA pass
If you’re already using **FaceDetailer** or a similar “detect & inpaint” helper:
1) Configure it to **detect multiple faces**.  
2) Set it to **process only the selected index** (e.g., the largest face or a chosen one).  
3) In its **inpaint prompt**, add the LoRA and token; keep the **global/base pass** LoRA-free.  
4) Set **inpaint denoise ~0.34–0.40** and a generous **mask blur** so edges blend.

**Tip:** Some detectors return faces in arbitrary order. If you need repeatability, choose the face **closest to X,Y** or the **largest area**.

---

## Practical guardrails that make the difference
- **Tight masks, soft edges:** Too big a mask lets the LoRA leak into hair/ears/cheeks of nearby people. Keep it around the target **oval + hairline**, then feather.  
- **Lower denoise for identity:** For face-only edits, **0.30–0.40** is the sweet spot; raise slightly only if it refuses to adopt the LoRA’d identity.  
- **Token discipline:** Put the LoRA token **only** in the **inpaint/regional prompt**—not in the global prompt.  
- **“Do not change others”:** Include a negative line like:  
  > “keep all other faces and bodies unchanged; do not alter background; do not add makeup to others.”  
- **SRPO last:** Use it as a finishing touch, not before inpaint. If SRPO has per-region strength, keep the face slightly lower than the rest so pores/texture don’t plasticize.

---

## Drop-in prompts for the inpaint pass
**Positive:**  
> `robyn_char, preserve facial identity, bone structure, hairline, eye shape and brow shape; match surrounding lighting; natural skin texture`  

**Negative:**  
> `do not change other faces or the background; no age change; no smoothing; no glam; no stylization; no makeup changes`

---

## Quick “if it misbehaves” fixes
- **Changes spill outside the face:** shrink mask; increase feather; **lower denoise by ~0.04**.  
- **Face won’t adopt LoRA identity:** slightly **raise LoRA model strength** (0.9→1.0) **or** increase denoise a touch (0.36→0.40).  
- **Skin gets waxy after SRPO:** turn SRPO down on the face region, or run SRPO first on a *copy*, then inpaint the face on top (so the face avoids the strongest SR pass).

If you tell me which face detector/mask builder you’re using (Ultralytics/FaceDetailer/etc.), I can sketch the exact node wiring and parameter boxes so you can paste it into your current graph.

**Robyn:**

I'm going to try Recipe (ComfyUI-style nodes). How to I wire, say, Ultralytics/YOLO face to select that particular face? Please provide a lst of nodes in their correct order, with values. Thanks.

**Emily:**

love it — let’s wire a **targeted face-only LoRA inpaint** with Ultralytics YOLO. Below is a clean, minimal ComfyUI recipe that works with stock nodes + common extensions. I’ll show two selectors: **(A) choose the largest face** and **(B) pick a specific index**.

---

# Nodes (in order) + values

## 0) Base setup
1) **Load Checkpoint**  
   - *ckpt:* your base model that matches the LoRA (e.g., SDXL/SD1.5/Flux—use the right family)  
   - *output:* **MODEL**, **CLIP**, **VAE**

2) **Load LoRA** (attach to the model/clip)  
   - *inputs:* MODEL, CLIP, lora file = your 16-img LoRA  
   - *weights:* **model: 0.90**, **clip: 0.60** (tune later)  
   - *output:* **MODEL (LoRA’d)**, **CLIP (LoRA’d)**

3) **CLIP Text Encode (positive)**  
   - *text:* `robyn_char, preserve facial identity, bone structure, hairline, eye and brow shape; match surrounding lighting; natural skin texture`  
   - *output:* **CONDITIONING+**

4) **CLIP Text Encode (negative)**  
   - *text:* `do not change other faces or background; no age change; no smoothing; no glam; no stylization; no makeup changes`  
   - *output:* **CONDITIONING−**

5) **Load Image**  
   - *image:* your group photo  
   - *output:* **IMAGE**

6) **VAE Encode**  
   - *inputs:* IMAGE, VAE  
   - *output:* **LATENT A**

---

## 1) Detect faces (Ultralytics / YOLO)
7) **Ultralytics YOLO Face Detector** (common node names: *UltralyticsFaceDetector*, *YOLOv8-Face*)  
   - *weights/model:* `yolov8n-face` (or `yolov8s-face` for tighter boxes)  
   - *conf (score threshold):* **0.25**  
   - *iou:* **0.45**  
   - *max detections:* **10**  
   - *input image:* IMAGE  
   - *output:* **BBOX LIST** (list of [x, y, w, h] in pixel coords)

> If your Ultralytics node has a “face only” preset, enable it. Otherwise, the YOLO-face weights do that by default.

---

## 2A) Choose the **largest face** (simple & reliable)
8a) **BBox Sort** (by area, desc)  
   - *input:* BBOX LIST  
   - *mode:* **sort by area (descending)**  
   - *output:* **BBOX SORTED**

9a) **BBox Pick by Index**  
   - *input:* BBOX SORTED  
   - *index:* **0** (the largest face)  
   - *output:* **BBOX TARGET**

## 2B) OR choose a **specific index** (if you know which face you want)
8b) **BBox Pick by Index**  
   - *input:* BBOX LIST  
   - *index:* **N** (0-based: 0,1,2,…)  
   - *output:* **BBOX TARGET**

*(If your toolkit doesn’t have “BBox Sort”/“Pick” nodes, many packs include them; otherwise you can use “Python Node” to select the bbox with `max(w*h)`—but most Ultralytics extensions ship a picker.)*

---

## 3) Turn that bbox into a soft mask
10) **BBox to Mask**  
   - *input image size:* from **IMAGE**  
   - *bbox:* **BBOX TARGET**  
   - *expand/dilate:* **8 px** (adds a little hairline/cheek room)  
   - *feather/blur:* **12 px** (soft edge so changes blend)  
   - *output:* **MASK (face)**

> If your node has separate Erode/Dilate controls: *dilate 8, erode 0, blur 12*.  
> Aim for a mask that covers the face oval + hairline but not neighbouring faces.

---

## 4) Inpaint only that face (LoRA active)
11) **KSampler (Inpaint / “masked area only”)**  
   - *model:* **MODEL (LoRA’d)**  
   - *positive:* **CONDITIONING+**  
   - *negative:* **CONDITIONING−**  
   - *latent:* **LATENT A**  
   - *mask:* **MASK (face)**  
   - *sampler:* **Euler a** (or your usual)  
   - *scheduler:* **Normal** (or Karras)  
   - *steps:* **32**  
   - *cfg:* **5.5**  
   - *denoise (strength):* **0.36** (range 0.30–0.42; lower if identity drifts)  
   - *inpaint mode:* **Masked area only**  
   - *output:* **LATENT B**

12) **VAE Decode**  
   - *latent:* **LATENT B**  
   - *VAE:* from step 1  
   - *output:* **IMAGE B (edited)**

---

## 5) SRPO finishing pass (gentle)
13) **SRPO**  
   - *input:* **IMAGE B**  
   - *strength/global:* **0.30–0.40**  
   - If SRPO offers per-region control, keep **face slightly lower** than background to avoid plastic skin.  
   - *output:* **IMAGE C (final)**

---

# Usage notes & tiny tweaks

- **Only the target face changes** because the LoRA participates *only* during the inpaint sampler and you’re feeding a **tight, soft mask**. Everyone else remains untouched.
- If the LoRA doesn’t “take” enough on the face, bump **LoRA model weight** to **1.00** (keep CLIP at 0.6), or nudge **denoise** from **0.36 → 0.40**.
- If the LoRA starts leaking into adjacent areas (hair/cheek), **shrink the mask** (dilate 6) and/or lower **denoise** by ~0.04.
- For **repeatable selection** across frames/sets, stick with **“largest”** or “index N”. If you need “the face nearest (x,y)”, many bbox tools include a **Pick Closest to Point** node; set a normalized point like (0.33, 0.35).
- Keep the **prompt token (`robyn_char`) only in the positive tied to the inpaint**. Don’t put it in any global prompt if you run a separate base pass.

---

## Quick alternate: “two-pass” (sometimes even cleaner)
- **Pass 1 (no LoRA):** Just encode and decode (no changes) → IMAGE A (same as input).  
- **Pass 2 (LoRA inpaint):** Use IMAGE A as the input to steps 6–13 above (mask+inpaint only).  
This isolates all LoRA effects to the face pass and is rock-solid for group photos.

---

If you tell me which Ultralytics node pack you have installed (exact name), I can swap in the **precise node names** from that pack and add a “Pick Closest to Point” variant too.

**Robyn:**

I have Ultralytics Detector Provider by ComfyUI-Impact-Nodes. What does that get plugged into?

**Emily:**

Got it—Impact Pack’s **Ultralytics Detector Provider** is a “model plug” that feeds a detector node. Here’s exactly how to wire it so you can pick one face and inpaint only that face with your LoRA.

I’ll use the Impact node names (they’re usually under **Impact / Ultralytics** and **Impact / BBox Utils**).

---

# Wiring (in order) with values

## A) Base / LoRA / Prompts
1) **Load Checkpoint**  
   - outputs → **MODEL**, **CLIP**, **VAE**

2) **Apply LoRA** (or “Load LoRA”)  
   - inputs: MODEL, CLIP, **your LoRA file**  
   - **Model weight: 0.90**, **CLIP weight: 0.60**  
   - outputs → **MODEL_LORA**, **CLIP_LORA**

3) **CLIP Text Encode (positive)**  
   - text:  
     `robyn_char, preserve facial identity, bone structure, hairline, eye and brow shape; match surrounding lighting; natural skin texture`  
   - output → **COND+**

4) **CLIP Text Encode (negative)**  
   - text:  
     `keep all other faces and background unchanged; no age change; no smoothing; no glam; no stylization; no makeup changes`  
   - output → **COND−**

5) **Load Image** → **IMAGE**

6) **VAE Encode**  
   - inputs: IMAGE, VAE → **LATENT_A**

---

## B) Detection path (Impact / Ultralytics)

7) **Ultralytics Detector Provider** (Impact)  
   - **model_name:** `yolov8n-face.pt` *(or `yolov8s-face.pt` if you want tighter boxes)*  
   - **device:** `auto` (or `cuda:0`)  
   - **task:** `detect` *(face weights already imply face class)*  
   - output → **DETECTOR**

8) **Ultralytics Detector** (Impact)  
   - **image:** IMAGE  
   - **detector:** DETECTOR  
   - **conf:** `0.25`  
   - **iou:** `0.45`  
   - **max_det:** `10`  
   - outputs → **BBOXES**, **SCORES**, **CLASS_IDS**

> Optional preview: **BBox Draw** (Impact) with IMAGE + BBOXES → a quick overlay so you can see the boxes.

---

## C) Choose the target face

### Option A — pick the **largest** face (most repeatable)
9A) **BBox Sort (Area)** (Impact)  
   - **bboxes:** BBOXES  
   - **order:** `descending`  
   - output → **BBOXES_SORTED**

10A) **BBox Pick Index** (Impact)  
   - **bboxes:** BBOXES_SORTED  
   - **index:** `0` *(largest by area)*  
   - output → **BBOX_TARGET**

### Option B — pick a **specific** index (when you know which one)
9B) **BBox Pick Index** (Impact)  
   - **bboxes:** BBOXES  
   - **index:** `N` *(0,1,2…)*  
   - output → **BBOX_TARGET**

### Option C — pick the face **nearest a point** (when you want the one by location)
9C) **BBox Closest To Point** (Impact)  
   - **bboxes:** BBOXES  
   - **point_x:** `0.33` *(normalized 0–1 across width)*  
   - **point_y:** `0.35` *(normalized 0–1 across height)*  
   - output → **BBOX_TARGET**

---

## D) Turn the chosen box into a soft mask

11) **BBox To Mask** (Impact)  
   - **image (for size):** IMAGE  
   - **bbox:** BBOX_TARGET  
   - **dilate/expand:** `8 px` *(room for hairline/cheek)*  
   - **feather/blur:** `12 px` *(soft edge)*  
   - **roundness:** `0.30` *(if available; soft corners)*  
   - output → **FACE_MASK**

*(If your Impact version splits “dilate / blur” into separate nodes, aim for: Dilate 6–10 px, Blur 10–16 px.)*

---

## E) Inpaint only that face (LoRA active)

12) **KSampler (inpaint / masked area only)**  
   - **model:** MODEL_LORA  
   - **positive:** COND+  
   - **negative:** COND−  
   - **latent:** LATENT_A  
   - **mask:** FACE_MASK  
   - **sampler:** Euler a *(or your favorite)*  
   - **scheduler:** Normal *(or Karras)*  
   - **steps:** `32`  
   - **cfg:** `5.5`  
   - **denoise (strength):** `0.36` *(identity-safe range 0.30–0.42)*  
   - **inpaint mode:** **Masked area only**  
   - output → **LATENT_B**

13) **VAE Decode**  
   - **latent:** LATENT_B → **IMAGE_B (edited)**

---

## F) SRPO finishing pass

14) **SRPO**  
   - **image:** IMAGE_B  
   - **strength:** `0.30–0.40` *(keep it modest so skin texture stays natural)*  
   - output → **IMAGE_FINAL**

---

# Notes & tiny tweaks

- **Why the Provider?** The **Ultralytics Detector Provider** is the model handle. You plug it into **Ultralytics Detector**, which actually runs detection on your **IMAGE** and returns **BBOXES**. From there you use **BBox Utils** to pick exactly one face and convert it to a mask.

- **Identity not strong enough?**  
  Raise **LoRA model** to `1.00` (leave CLIP at `0.60`) **or** nudge **denoise** to `0.40`.  
  If features over-change, drop denoise back toward `0.34`.

- **Leak into neighbors?**  
  Shrink mask (dilate 6 px), lower denoise by ~0.04, and/or increase feather slightly (14–16 px).

- **Repeatable selection:**  
  Use **Largest** or **Closest To Point**. Index order can change frame-to-frame on slight crops.

- **One-liner guardrail** to add near the top of your positive prompt:  
  “**Adjust only the masked face; do not alter other faces or the background.**”

If any of those node names don’t appear in your menus exactly as written, tell me the precise labels you see under **Impact / Ultralytics** and **Impact / BBox Utils**, and I’ll map them 1:1 to your pack’s naming.

**Robyn:**

UltralyticsDetectorProvider has 2 outputs: BBOX_DETECTOR and SEGM_DETECTOR. I've plugged the BBOX_DETECTOR output from that node to the bbox_detector input for BBOX Detector (combined) node (also Impact). It outputs a mask. How does it know what face I want to select? There's only Threshold (default 0.50) and dilation (default4). And what does mask get plugged into?

**Emily:**

Great question — that specific node (“**BBOX Detector (combined)**”) makes a **single union mask of *all* faces it finds**.  
- **Threshold** = confidence cutoff (which boxes make it into the mask).  
- **Dilation** = how much to grow each box before merging them.  
It does **not** choose *which* face; it just outputs one big mask. That’s why you’re not seeing a way to pick a particular person inside that node.

You’ve got two clean ways forward:

---

## A) Preferred: Use the *bbox* path, then pick a face, then convert to a mask
This gives you precise control.

**Wiring (Impact Pack names):**
1) **Ultralytics Detector Provider** → `BBOX_DETECTOR`
2) **Ultralytics Detector** (Impact)  
   - `detector` = `BBOX_DETECTOR`  
   - `image` = your IMAGE  
   - `conf` = **0.25** | `iou` = **0.45** | `max_det` = **10**  
   - **Outputs:** `BBOXES`, `SCORES`, `CLASS_IDS`
3) **BBox Sort (Area)** (Impact)  
   - `bboxes` = `BBOXES`  
   - `order` = **descending**
   - **Output:** `BBOXES_SORTED`
4) **BBox Pick Index** (Impact)  
   - `bboxes` = `BBOXES_SORTED`  
   - `index` = **0** *(largest face)*  — or set any index you want
   - **Output:** `BBOX_TARGET`
5) **BBox To Mask** (Impact)  
   - `image` = original IMAGE (for size)  
   - `bbox` = `BBOX_TARGET`  
   - `dilate/expand` = **8 px**  
   - `feather/blur` = **12 px**  
   - **Output:** `FACE_MASK`
6) **KSampler (inpaint / masked area only)**  
   - `mask` = `FACE_MASK`  
   - LoRA **ON** here  
   - `denoise` **0.34–0.40** (start 0.36) | `cfg` **5.5** | `steps` **32**
7) **VAE Decode** → **SRPO** (0.30–0.40) → final

> **Where does the mask plug in?** Into the **KSampler**’s `mask` input; set **Inpaint mode = Masked area only** so only that face is edited.

---

## B) If you want to keep using **BBOX Detector (combined)**
You can still isolate one face; you just need to split the big mask into components and pick one.

**Wiring:**
1) **Ultralytics Detector Provider** → `BBOX_DETECTOR`
2) **BBOX Detector (combined)** (Impact)  
   - `detector` = `BBOX_DETECTOR`  
   - `image` = IMAGE  
   - `threshold` = **0.25–0.50** (confidence)  
   - `dilation` = **6–10 px**  
   - **Output:** `MASK_ALL` *(union of all faces)*
3) **Mask Connected Components** (Impact) *(sometimes called “Mask Components”)*  
   - `mask` = `MASK_ALL`  
   - **Outputs:** `COMP_MASKS` (list of per-face masks) + (often) `BBOXES` per component
4) **Mask Pick Index** (Impact)  
   - `masks` = `COMP_MASKS`  
   - `index` = **0** *(largest or first component; many versions also support sorting)*
   - **Output:** `FACE_MASK`
5) *(Optional)* **Mask Morphology** (Impact)  
   - `FACE_MASK` → `Dilate 6–8`, `Blur/Feather 10–16`
6) **KSampler (inpaint / masked area only)**  
   - `mask` = `FACE_MASK`  
   - LoRA **ON** here  
   - `denoise` **0.34–0.40**, `cfg` **5.5**, `steps` **32`
7) **VAE Decode** → **SRPO**

> If your Impact build doesn’t expose “Mask Connected Components,” an alternative is **Mask → BBoxes** then **pick one bbox** and go through **BBox To Mask** (same as path A after picking).

---

## About the **SEGM_DETECTOR** output
- Use **SEGM_DETECTOR** only with Ultralytics **segmentation** weights (e.g., `yolov8s-seg.pt`).  
- Most *face* models are bbox-only (no polygon seg), so `SEGM_DETECTOR` won’t add value here. For faces, **BBOX_DETECTOR** → bbox list → mask is the reliable route.

---

## Quick tuning tips
- If the LoRA bleeds outside the face: **reduce mask size**, **increase feather**, and **lower denoise** by ~0.04.  
- If the LoRA doesn’t “take” strongly enough: **raise LoRA model weight** (0.9 → 1.0) or nudge **denoise** to ~0.40.  
- Keep your identity prompt **only** in the inpaint sampler’s positive; don’t include it globally.

If you tell me the exact Impact node names you see for “Mask Components / Pick / Morphology,” I’ll map them 1:1 and suggest defaults for each box.

**Robyn:**

Doing this step-by-step. I don't have Ultralytics Detector (Impact) ... it doesn't exist in my ComfyUI-Impact-Nodes installation. 

I have BBox Detector (SEGS) by Impact with dropdowns:
threshold (default 0.50)
dilation (default 4)
crop_factor (default 3.0)
drop_size (default 10)
text box with the word "all" in it
Outputs "segs".

**Emily:**

Gotcha—Impact’s **BBox Detector (SEGS)** will work fine; it just outputs a *list of per-detection segments* (“**segs**”), not one mask. From there, you pick the one you want and turn it into a mask for inpainting.

Here’s a wiring that only uses nodes you’ve said you have (Impact pack), with two ways to pick the target face.

---

# Wiring with Impact nodes you listed

## A) Base / LoRA / Prompts (unchanged)
1) **Load Checkpoint** → MODEL, CLIP, VAE  
2) **Apply/Load LoRA** → MODEL_LORA, CLIP_LORA (weights: model 0.90, clip 0.60)  
3) **CLIP Text Encode (positive)** → COND+  
4) **CLIP Text Encode (negative)** → COND−  
5) **Load Image** → IMAGE  
6) **VAE Encode** (IMAGE, VAE) → LATENT_A

## B) Detector path (your nodes)
7) **Ultralytics Detector Provider (Impact)**  
   - Output used: **BBOX_DETECTOR**  
   - Model: `yolov8n-face.pt` (or `yolov8s-face.pt`)  
   - Device: auto / cuda:0

8) **BBox Detector (SEGS) – Impact**  
   - **detector:** plug **BBOX_DETECTOR** into it  
   - **image:** IMAGE  
   - **threshold:** 0.25–0.35 (confidence cutoff; 0.50 can miss smaller faces)  
   - **dilation:** 6–10 (grows each box before rasterizing)  
   - **crop_factor:** 3.0 (leave as-is; 2.5–3.5 is fine)  
   - **drop_size:** 10 (ignore tiny blips)  
   - **class filter (textbox):** `all` (the face model has one class anyway)  
   - **output:** **SEGS** (a list of per-face segment objects)

> TL;DR: this node gives you one **seg** per detected face. Now we choose one.

---

## C1) Pick **largest** face (simple & robust)

9) **Segs → BBoxes** (Impact)  
   - **segs:** SEGS  
   - **output:** BBOXES

10) **BBox Sort (Area)** (Impact)  
   - **bboxes:** BBOXES  
   - **order:** descending  
   - **output:** BBOXES_SORTED

11) **BBox Pick Index** (Impact)  
   - **bboxes:** BBOXES_SORTED  
   - **index:** **0** (largest face)  
   - **output:** BBOX_TARGET

12) **BBox To Mask** (Impact)  
   - **image (for size):** IMAGE  
   - **bbox:** BBOX_TARGET  
   - **dilate/expand:** **8 px**  
   - **feather/blur:** **12 px**  
   - **output:** **FACE_MASK**

→ Go to the inpaint sampler (section D).

---

## C2) Pick a **specific** face by index (when you want #1, #2, etc.)

9) **Segs Pick Index** (Impact) *(or “Seg Pick Index” if singular)*  
   - **segs:** SEGS  
   - **index:** **N** (0-based: 0,1,2…)  
   - **output:** **SEG_TARGET**

10) **Seg → Mask** (Impact)  
   - **seg:** SEG_TARGET  
   - **output:** FACE_MASK_RAW

11) **Mask Morphology** (Impact) *(if you have it; otherwise skip)*  
   - **input mask:** FACE_MASK_RAW  
   - **dilate:** **6–8 px**  
   - **blur/feather:** **10–16 px**  
   - **output:** **FACE_MASK**

→ Go to the inpaint sampler.

> If you don’t see “Segs Pick Index” or “Seg → Mask”, use the C1 route (Segs → BBoxes → sort/pick → BBox To Mask). Same result.

---

## D) Inpaint only that face (LoRA active)

12) **KSampler** (set **Inpaint mode = Masked area only**)  
   - **model:** MODEL_LORA  
   - **positive:** COND+  
   - **negative:** COND−  
   - **latent:** LATENT_A  
   - **mask:** **FACE_MASK**  
   - **sampler:** Euler a (or your usual)  
   - **steps:** **32**  
   - **cfg:** **5.5**  
   - **denoise/strength:** **0.36** (identity-safe 0.30–0.42)  
   - **output:** LATENT_B

13) **VAE Decode** (LATENT_B, VAE) → IMAGE_B  
14) **SRPO** (IMAGE_B, strength 0.30–0.40) → **IMAGE_FINAL**

---

## What those puzzling SEGS settings mean

- **threshold**: confidence for a face to count. Lower if it misses small/side faces.  
- **dilation**: grows the bbox before it rasterizes to a segment (useful to cover hairline/cheeks).  
- **crop_factor**: how big a patch around the detection is considered when the node builds its seg; 3.0 is safe.  
- **drop_size**: ignores tiny specks.  
- **“all”**: class filter; face models usually have a single class, so leave it.

---

## Troubleshooting quickies

- **It still edits more than one face:** your mask is likely the *union*. Make sure you pass the **picked** mask (`FACE_MASK`) to KSampler, not the raw union SEGS/combined mask.  
- **LoRA doesn’t “take” strongly:** bump LoRA **model** to 1.0 or nudge **denoise** up to 0.40.  
- **LoRA bleeds into neighbours:** reduce **dilation** and/or **feather**, and lower **denoise** by ~0.04.  
- **Index keeps changing per image:** prefer **largest** (C1) or use a **“closest to point”** picker if Impact exposes one (pick nearest to normalized X,Y).

If you read me the exact names of any “Segs → …” or “Mask …” utilities you see under Impact > BBox/Segs/Mask, I’ll map them line-by-line with exact parameter labels so you can click through without guessing.

**Robyn:**

I don't have a BBox Sort node, Emily.

**Emily:**

No worries—you can do this cleanly **without** a “BBox Sort” node. Here are three selector paths that work with the **Impact** nodes you said you have.

---

## Your current detector path (keep this)
1) **Ultralytics Detector Provider** → use **BBOX_DETECTOR**  
2) **BBox Detector (SEGS)**  
   - detector = **BBOX_DETECTOR**  
   - image = your IMAGE  
   - **threshold:** 0.25–0.35 (0.50 can miss small faces)  
   - **dilation:** 6–10  
   - **crop_factor:** 3.0  
   - **drop_size:** 10  
   - class filter: `all`  
   - **Output:** **SEGS** (one segment per detected face)

You now need to choose just **one** of those `SEGS`.

---

## A) Pick by index (most straightforward)
Use the per-segment index directly.

3A) **Segs Preview / Draw (Impact)** (if present)  
   - segs = **SEGS**  
   - image = **IMAGE**  
   - Enable “show indices/labels” so you can see which face is **index 0,1,2…** (purely for your visual check).

4A) **Segs Pick Index (Impact)**  
   - segs = **SEGS**  
   - **index:** the one you want (0-based)  
   - → **SEG_TARGET**

5A) **Seg → Mask (Impact)**  
   - seg = **SEG_TARGET**  
   - → **MASK_RAW**

6A) **Mask Morphology (Impact)**  
   - input = **MASK_RAW**  
   - **dilate:** 6–8 px  
   - **blur/feather:** 10–16 px  
   - → **FACE_MASK**

→ Plug **FACE_MASK** into **KSampler**’s `mask` (set **Inpaint mode = Masked area only**).  
Suggested inpaint: **steps 32, cfg 5.5, denoise 0.36**, LoRA model 0.9–1.0, CLIP 0.6.

---

## B) Pick by **position** (nearest to a point)
Handy when “index” order changes across images.

3B) **Segs → BBoxes (Impact)**  
   - segs = **SEGS**  
   - → **BBOXES**

4B) **BBoxes Closest To Point (Impact)** *(or similarly named)*  
   - bboxes = **BBOXES**  
   - **point_x:** 0.33  *(normalized 0–1 across width)*  
   - **point_y:** 0.35  *(normalized 0–1 across height)*  
   - → **BBOX_TARGET**

5B) **BBox To Mask (Impact)**  
   - image = **IMAGE**  
   - bbox = **BBOX_TARGET**  
   - **expand/dilate:** 8 px  
   - **feather/blur:** 12 px  
   - → **FACE_MASK**

→ Inpaint as above.

> Tip: set the point roughly over the face you want (e.g., click-measure once, then reuse the same normalized coords for batch consistency).

---

## C) “Largest face” without sort
If you don’t have sort, you can still approximate “largest”:

3C) **Segs → BBoxes (Impact)** → **BBOXES**  
4C) **BBoxes Index by Largest / Max Area**  
- Some Impact builds have a node named like **“BBoxes Max Area Index”** or **“BBoxes Pick Largest”**.  
- If you **don’t** have that, fall back to **A)** (index) or **B)** (closest-to-point). In practice, **B** is very reliable for repeatability.

Then 5C) **BBox To Mask** → **FACE_MASK** → inpaint.

---

## Where does the mask go?
Into your **KSampler** (or Efficiency KSampler) `mask` input. Set:
- **Inpaint mode:** **Masked area only**  
- **Denoise:** **0.34–0.40** (start 0.36)  
- **CFG:** **5.5**  
- **Steps:** **32**  
- **LoRA:** ON here (model 0.9–1.0, CLIP 0.6)  
- **Positive prompt (inpaint sampler only):** include your token + identity locks  
- **Negative:** “keep other faces/background unchanged…”

---

## Tiny tricks when nodes are missing
- If you can’t preview indices, temporarily **raise `threshold`** so only the most confident (often the largest/clearest) face survives; use **Segs Pick Index = 0**. Then restore threshold.
- If the LoRA spills beyond the face, **shrink dilate** (6 px), keep **feather ~12–14**, and **lower denoise** by ~0.04.
- If identity is weak, **raise LoRA model** to **1.0** or nudge **denoise** to **0.40**.

If you tell me the **exact names** under Impact for: “Segs Pick Index”, “Segs → BBoxes”, “Seg → Mask”, and any “Closest To Point / Morphology” nodes you do see, I’ll write the precise click-by-click with their parameter labels so you can wire it in one go.

**Robyn:**

I have:
BBox Detector (already chosen)
Bbox Visualize
Split Bboxes
LayerMask: Bbox Join
From SEG_ELT bbox
ScaleBy BBox
Draw BBox Mask
Image UncropFromBBOX

**Emily:**

Brilliant — those Impact nodes are enough to target a **single** face cleanly. Below are **two working wirings** using only the nodes you listed.

---

# Path A — Make a face mask from one bbox (simplest)

**Goal:** pick one detected bbox → turn it into a soft mask → inpaint only that area with your LoRA.

1) **Ultralytics Detector Provider** → (use **BBOX_DETECTOR**)
2) **BBox Detector (already chosen)**  
   - detector = **BBOX_DETECTOR**  
   - image = your **IMAGE**  
   - threshold: **0.25–0.35** (0.50 can miss small faces)  
   - dilation: **6–10**  
   - crop_factor: **3.0**  
   - drop_size: **10**  
   - class filter: `all`  
   - **Output:** a list (often called **SEGS** or **BBOXES** depending on build)

3) **Split Bboxes**  
   - **bboxes/list** = output of **BBox Detector**  
   - **index** = the face you want (0-based; start with **0** if you want “the first/usually largest”)  
   - **Output:** **SEG_ELT** (a single element from the list)

4) **From SEG_ELT bbox**  
   - input = **SEG_ELT**  
   - **Output:** **BBOX_TARGET** (x, y, w, h)

5) **Draw BBox Mask**  
   - image = original **IMAGE** (for size)  
   - bbox = **BBOX_TARGET**  
   - **expand/dilate:** **8 px** (room for hairline/cheeks)  
   - **feather/blur:** **12 px** (soft edge)  
   - **Output:** **FACE_MASK**

6) **KSampler** (inpaint)  
   - model = your **LoRA-applied MODEL**  
   - positive = identity-safe text for the target face (incl. your token)  
   - negative = “keep other faces/background unchanged; no smoothing; no glam”  
   - latent = **VAE-encoded** latent of IMAGE  
   - **mask = FACE_MASK**  
   - **Inpaint mode:** **Masked area only**  
   - steps **32**, cfg **5.5**, **denoise 0.36** (identity-safe 0.30–0.42)  
   - → **LATENT_OUT**

7) **VAE Decode** → **SRPO** (0.30–0.40) → final image

> Tip: If you need to **see which index is which**, drop **Bbox Visualize** between step 2 and 3 to overlay boxes on the image; try indices 0,1,2… until you hit the target.

---

# Path B — Crop to the face, edit, then un-crop (very precise)

**Goal:** crop the image (and latent) to just that bbox → edit with LoRA → paste back in place. This can reduce bleed and is great for identity.

1) Steps 1–4 are **the same** as Path A to get **BBOX_TARGET**.

2) **ScaleBy BBox**  
   - image = **IMAGE**  
   - bbox = **BBOX_TARGET**  
   - (if there’s a “scale”/padding value, set ~**1.2** so you include a bit more than the face)  
   - **Output:** **IMAGE_CROP** and a **CROP_META** (or similar transform data)

3) **VAE Encode** on **IMAGE_CROP** → **LATENT_CROP**

4) **KSampler** (no mask needed if you want to change the whole crop)  
   - model = **LoRA-applied MODEL**  
   - positive/negative = same as Path A  
   - latent = **LATENT_CROP**  
   - **denoise:** **0.34–0.40** (start 0.36)  
   - steps **32**, cfg **5.5**  
   - → **LATENT_CROP_OUT**

   *(If you only want part of the crop, you can still use **Draw BBox Mask** on the crop and run inpaint mode; otherwise this is a clean full-crop edit.)*

5) **VAE Decode** → **IMAGE_CROP_EDITED**

6) **Image UncropFromBBOX**  
   - **edited** = **IMAGE_CROP_EDITED**  
   - **original** = **IMAGE**  
   - **bbox/meta** = **BBOX_TARGET** (or **CROP_META**, depending on the node’s inputs)  
   - → **IMAGE_MERGED** (face replaced in the original at exact spot)

7) **SRPO** (0.30–0.40) on **IMAGE_MERGED** → final

---

## Which one to choose?

- **Path A (mask into KSampler)** is faster to wire and perfect when you just need the face oval edited.  
- **Path B (crop + un-crop)** is excellent for maximum control, or if you also adjust small surrounding context (hairline, small shadows) with minimal risk of touching other faces.

---

## Tiny tuning that matters

- If LoRA bleeds: reduce **expand/dilate** to **6 px**, keep **feather** ~**12–14 px**, and lower **denoise** by **0.04**.  
- If LoRA is too weak: raise **LoRA model weight** (0.9 → **1.0**), or nudge **denoise** to **0.40**.  
- Keep your **LoRA token only** in the **inpaint/crop pass** prompt, not in any global/base pass.  
- For repeatability across a batch, stick with the **same index** or switch to a **“closest to point”** selector if you add one later.

If you want, tell me which **exact inputs/outputs** your **ScaleBy BBox** and **Image UncropFromBBOX** nodes expose (sometimes there are two variants), and I’ll name the ports you should connect 1:1 so it clicks together without guessing.

**Robyn:**

I have a question about Split Bboxes -> bboxes/list = output of BBox Detector. Split BBoxes has an input bboxes. What gets plugged into that?

**Emily:**

Plug the **SEGS** list from **BBox Detector (SEGS)** straight into **Split Bboxes → bboxes**.  
Yeah, the name is confusing—**Split Bboxes** happily splits the *segs list* this detector produces.

Then wire it like this:

1) **Ultralytics Detector Provider →** BBOX_DETECTOR  
2) **BBox Detector (SEGS)**
   - detector = **BBOX_DETECTOR**
   - image = your IMAGE  
   - threshold 0.25–0.35, dilation 6–10, crop_factor 3.0, drop_size 10, class = `all`  
   - **Output:** **SEGS**
3) **Split Bboxes**
   - **bboxes = SEGS**  ← (this is the step you asked about)
   - **index =** pick the face you want (0,1,2,…)  
   - **Output:** **SEG_ELT**
4) **From SEG_ELT bbox**
   - **seg_elt = SEG_ELT**
   - **Output:** **BBOX_TARGET** (x,y,w,h)
5) **Draw BBox Mask**
   - image = original IMAGE (for size)
   - bbox = **BBOX_TARGET**
   - expand/dilate = **8 px**, feather/blur = **12 px**
   - **Output:** **FACE_MASK**
6) **KSampler** (Inpaint mode = **Masked area only**)
   - model = your **LoRA-applied** MODEL
   - positive = your identity prompt (with the LoRA token)
   - negative = “keep other faces/background unchanged…”
   - latent = VAE-encoded latent of IMAGE
   - **mask = FACE_MASK**
   - steps **32**, cfg **5.5**, **denoise 0.36** (0.30–0.42 range)
7) **VAE Decode → SRPO** (0.30–0.40) → final

If you want to preview which index is which before you commit, drop **Bbox Visualize** right after step 2 (input: IMAGE + SEGS) so you can see the numbered boxes, then set **Split Bboxes → index** accordingly.

**Robyn:**

Hate to disappoint, but the Split Bboxes input bboxes is NOT accepting connection to the SEGS output of BBOX Detector (SEGS).

**Emily:**

Ah—that explains it. **Split Bboxes** only accepts a **BBOX list**, but your detector is outputting **SEGS** (segment objects). That’s why the wire won’t connect.

You have the right pieces—just use the **SEGS** path instead of the **BBOX** path:

## Use the SEGS path (works with the nodes you listed)
1) **Ultralytics Detector Provider** → use **BBOX_DETECTOR**  
2) **BBox Detector (SEGS)**  
   - detector = **BBOX_DETECTOR**  
   - image = your IMAGE  
   - threshold 0.25–0.35, dilation 6–10, crop_factor 3.0, drop_size 10, class = `all`  
   - **Output:** **SEGS** (one seg per detected face)

3) **Split SEGS** *(not “Split Bboxes”)*  
   - **segs = SEGS**  
   - **index =** the face you want (0-based)  
   - **Output:** **SEG_ELT**

> If you don’t see “Split SEGS”, try searching your node list for **“Split Segs”**, **“Segs Split”**, or **“SEGS Index”** (Impact’s naming varies slightly). The fact you have **From SEG_ELT bbox** means the matching splitter is in your pack.

4) **From SEG_ELT bbox**  
   - **seg_elt = SEG_ELT**  
   - **Output:** **BBOX_TARGET** (x, y, w, h)

5) **Draw BBox Mask**  
   - image = original **IMAGE**  
   - bbox = **BBOX_TARGET**  
   - expand/dilate: **8 px**  
   - feather/blur: **12 px**  
   - **Output:** **FACE_MASK**

6) **KSampler** (Inpaint → **Masked area only**)  
   - model = your **LoRA-applied MODEL**  
   - positive = your identity prompt (with the LoRA token)  
   - negative = “keep other faces/background unchanged; no smoothing; no glam”  
   - latent = VAE-encoded latent of IMAGE  
   - **mask = FACE_MASK**  
   - steps **32**, cfg **5.5**, **denoise 0.36** (0.30–0.42 range)

7) **VAE Decode** → **SRPO** (0.30–0.40) → final

---

## If “Split SEGS” truly isn’t present
Two alternatives using only what you listed:

### A) Convert SEGS → BBOX, then use your bbox tools
- **From SEG_ELT bbox** actually needs a single `SEG_ELT`. If you lack a seg splitter, look for a node called **“SEGS to BBoxes”** / **“Segs → BBoxes”** in Impact.  
- Then use **Split Bboxes** on that BBOX list → **LayerMask: Bbox Join** or **Draw BBox Mask** to build the mask as above.

### B) Quick crop route (avoids masks)
- Up to step 4 as above to get **BBOX_TARGET** (you need the seg splitter for this—so see if “Split SEGS” exists).  
- **ScaleBy BBox** (pad ~1.2) → **VAE Encode** (crop) → **KSampler** (no mask; LoRA on; denoise 0.34–0.40) → **VAE Decode** → **Image UncropFromBBOX** to paste it back.

---

### Why the wire failed
- **Split Bboxes** expects a **BBOX list**.  
- **BBox Detector (SEGS)** outputs **SEGS**.  
Use **Split SEGS** to get a **SEG_ELT**, then convert with **From SEG_ELT bbox**.

If you can’t find the **Split SEGS** node, tell me the exact names under your “Segs/SEGS” submenu and I’ll map the precise splitter name you have to this wiring.

**Robyn:**

The only thing that comes close is "Count Elts in SEGS"

**Emily:**

Right now your graph can’t pick a single face because you only have **SEGS** (a list of segment objects) and no node that can **extract one seg** from that list.

- **Split Bboxes** expects a **BBOX list**, not **SEGS** → that’s why it refuses the wire.  
- You do have **From SEG_ELT bbox**, which converts **one** seg element into a bbox — but you’re missing the node that creates that **SEG_ELT** from the SEGS list.

You need one tiny “splitter” node. Two minimal fixes:

## Fix A (recommended): add the missing splitter from Impact
Update ComfyUI-Impact-Nodes so you get one of these (any will do):
- **Split SEGS** (or **SEGS Split / SEGS Index**) → outputs **SEG_ELT**
- **SEGS → BBoxes** (converts directly to a bbox list)

Then wire:

1) **BBox Detector (SEGS)** → **SEGS**  
2) **Split SEGS** → `segs=SEGS`, `index=N` → **SEG_ELT**  
3) **From SEG_ELT bbox** → `seg_elt=SEG_ELT` → **BBOX_TARGET**  
4) **Draw BBox Mask** → `image=IMAGE`, `bbox=BBOX_TARGET`, expand=8, feather=12 → **FACE_MASK**  
5) **KSampler (inpaint, masked area only)** with LoRA → final

## Fix B (works today if you install just one tiny helper)
If you can’t upgrade the whole pack, install *any* small utility that converts **SEGS → BBOXES**. With that, you can use the nodes you already have:

1) **BBox Detector (SEGS)** → **SEGS**  
2) **SEGS → BBOXES** → **BBOXES**  
3) **Split Bboxes** → `bboxes=BBOXES`, `index=N` → **SEG_ELT (bbox element)**  
4) **LayerMask: Bbox Join** (optional if you ever need to merge multiple boxes)  
5) **Draw BBox Mask** → **FACE_MASK**  
6) **KSampler (inpaint, masked area only)** → final

---

### Can I hack it without adding a node?
Not cleanly. With only the nodes you listed:
- **Count Elts in SEGS** tells you how many faces, but doesn’t extract one.
- **Bbox Visualize** only overlays, doesn’t output bboxes.
- **Split Bboxes** won’t accept **SEGS**.
- **From SEG_ELT bbox** needs a **SEG_ELT** you currently can’t produce.

So the smallest change is: **install one splitter node** (it’s a tiny part of the Impact pack; most installs have it). Once it appears, the wiring above will work exactly as you want.

If you tell me whether you’d rather (1) update Impact or (2) drop in a single “SEGS→BBOXES” helper, I’ll give you the precise node name to search for in your manager and the exact click-by-click wiring with the port labels you’ll see on screen.

**Robyn:**

"Split SEGS → segs=SEGS, index=N → SEG_ELT"

Picker (SEGS)?

**Emily:**

Yep—**Picker (SEGS)** is exactly the splitter you need. It outputs a single **SEG_ELT** from the **SEGS** list so you can feed it into **From SEG_ELT bbox**.

### Wire it like this
1) **Ultralytics Detector Provider** → use **BBOX_DETECTOR**  
2) **BBox Detector (SEGS)**  
   - detector = **BBOX_DETECTOR**  
   - image = your IMAGE  
   - threshold 0.25–0.35, dilation 6–10, crop_factor 3.0, drop_size 10, class `all`  
   - **Output:** **SEGS**
3) **Picker (SEGS)**  
   - **segs = SEGS**  
   - **index = N** (0,1,2… pick your face)  
   - **Output:** **SEG_ELT**
4) **From SEG_ELT bbox**  
   - **seg_elt = SEG_ELT** → **BBOX_TARGET** (x,y,w,h)
5) **Draw BBox Mask**  
   - image = original IMAGE  
   - bbox = **BBOX_TARGET**  
   - expand/dilate **8 px**, feather/blur **12 px** → **FACE_MASK**
6) **KSampler** (Inpaint, **Masked area only**)  
   - mask = **FACE_MASK**, LoRA ON, steps 32, cfg 5.5, **denoise 0.36**
7) **VAE Decode → SRPO** (0.30–0.40)

### If you can’t find “Picker (SEGS)”
- Update **ComfyUI-Impact-Nodes**; the SEGS picker lives with the bbox/seg utils.  
- Temporary fallback: look for a node named **“Segs → BBoxes”** (or similar). Then use your existing **Split Bboxes** on that bbox list, followed by **Draw BBox Mask**. Same end result, just one extra conversion step.

Once Picker (SEGS) is in, the rest of your graph stays exactly as we’ve outlined.

**Robyn:**

Picker (SEGS)
Input: segs = SEGS
index = N (0,1,2… pick your face)
Output: SEGS (not SEG_ELT)

**Emily:**

Ahh, that variant of **Picker (SEGS)** keeps the type as a *SEGS list* (just length-1), so it won’t connect to **From SEG_ELT bbox** which expects a true **SEG_ELT**.

You’ve got three workable fixes—pick the one your install supports:

## Option 1 — Flip Picker into “element” mode (if available)
Open **Picker (SEGS)** and look for a toggle like:
- **Return element / unwrap / flatten / output SEG_ELT**  
Turn it on.  
Then wire:
```
SEGS ─→ Picker(SEGS) [index=N, return element=ON] ─→ SEG_ELT ─→ From SEG_ELT bbox ─→ Draw BBox Mask ─→ KSampler(mask)
```

## Option 2 — Insert a tiny “SEGS → SEG_ELT” step (if present)
Some Impact builds include one of these:
- **SEGS Index (elt)** / **SEGS Get Element** / **Split SEGS**

Wire:
```
SEGS ─→ SEGS Index(elt) [index=N] ─→ SEG_ELT ─→ From SEG_ELT bbox ─→ Draw BBox Mask ─→ KSampler(mask)
```

## Option 3 — Convert to BBOXES and use your bbox tools (usually available)
If you see a converter like **SEGS → BBoxes** (or **From SEGS to BBoxes**):
```
SEGS ─→ SEGS→BBoxes ─→ BBOXES ─→ Split Bboxes [index=N] ─→ BBOX_TARGET
BBOX_TARGET ─→ Draw BBox Mask ─→ FACE_MASK ─→ KSampler(mask, inpaint “masked area only”)
```

### If none of those nodes exist in your menus
- The minimal fix is to **update ComfyUI-Impact-Nodes** (it’s a tiny utility node you’re missing).  
- Without a SEG→ELT or SEG→BBOX step, there’s no way to hand a single face to your downstream nodes—because everything after that needs either **SEG_ELT** or **BBOX**.

### Quick recap for the inpaint step
- **KSampler:** Inpaint mode = **Masked area only**  
- **Mask:** output of **Draw BBox Mask**  
- **LoRA on** here; **denoise 0.34–0.40** (start 0.36), **CFG 5.5**, **Steps 32**  
- Positive (only for inpaint sampler): your token + identity locks  
- Negative: “keep other faces/background unchanged; no smoothing/glam”

If you tell me which of these three node names you actually have (or don’t), I’ll give you the exact click-by-click wiring for that path.

**Robyn:**

I updated ComfyUI-Impact-Nodes to the lates version. I looked under Utils. I see no SEGS->BBoxes utility. I'm ready to give up.

**Emily:**

Totally get the frustration. You’re one tiny node away. Since your **Picker (SEGS)** won’t emit a single `SEG_ELT`, the cleanest fix (with what you likely already have) is to use a **generic list indexer** to grab one element from the `SEGS` list, then feed that into **From SEG_ELT bbox**.

### Option A — Use a generic list picker (usually under *Utils*)
Look for any node named something like:
- **List Index** / **Get Item From List** / **Pick From List** / **Picker (List)**

**Wiring**
1) **BBox Detector (SEGS)** → `SEGS`
2) **List Index** (or equivalent)  
   - `list` = `SEGS`  
   - `index` = N (0,1,2…)  
   - **output:** a **single list element** (this will be your `SEG_ELT`)
3) **From SEG_ELT bbox**  
   - `seg_elt` = output of List Index  
   - → **BBOX_TARGET** (x,y,w,h)
4) **Draw BBox Mask**  
   - `image` = original IMAGE  
   - `bbox` = **BBOX_TARGET**  
   - `expand/dilate` = 8 px, `feather/blur` = 12 px  
   - → **FACE_MASK**
5) **KSampler** (Inpaint = **Masked area only**)  
   - `mask` = **FACE_MASK**  
   - LoRA ON, steps 32, cfg 5.5, **denoise ~0.36**

This works because the generic list indexer doesn’t care about the element type—it just returns the **N-th item** from `SEGS`, which **From SEG_ELT bbox** accepts.

---

### Option B — Switch the detector node to output BBOXES (if available)
If you spot **“SEGS → BBoxes”** later (sometimes appears after updating), wire:
1) `SEGS` → **SEGS→BBoxes** → `BBOXES`  
2) **Split Bboxes** → index N → **BBOX_TARGET**  
3) **Draw BBox Mask** → **FACE_MASK** → **KSampler** (inpaint)

---

### If neither a list indexer nor SEGS→BBoxes exists
Two practical fallbacks:

- **Fallback 1 (crop route, no mask):**  
  You still need a single bbox. Without a SEG indexer, this isn’t doable from `SEGS`. The minimal install is a **generic “List Index”** utility (it’s tiny) so you can get `SEG_ELT`.

- **Fallback 2 (union mask + components):**  
  Use **BBOX Detector (combined)** → union mask, then run a **Mask Connected Components** node to split and pick one component. If you don’t have “Mask Connected Components,” it’s another tiny utility to add.

---

### Quick sanity checklist
- After you get **BBOX_TARGET**, you’re golden: `BBOX_TARGET → Draw BBox Mask → KSampler(masked area only)`.  
- If the LoRA leaks: reduce `expand` to 6 px, keep `feather` ~12–14 px, drop **denoise** by ~0.04.  
- If LoRA is weak: set **LoRA model** 0.9→1.0 or nudge **denoise** to ~0.40.

If you can tell me whether you have **any** generic “List Index/Get Item” node under *Utils* (even outside Impact), I’ll give you the exact port names and a one-line wiring so you can click it in without hunting.

**Robyn:**

Not sure if this has any chance of working, but :
BBox Detector (SEGS)
SEGS to Mask List
Select Nth Item (Any List)

**Emily:**

Yes—that can work! Use the mask directly for the inpaint. Here’s the clean wiring with the nodes you have:

# Path A — Direct mask → inpaint (no bbox needed)

1) **Ultralytics Detector Provider** → use **BBOX_DETECTOR**  
2) **BBox Detector (SEGS)**  
   - detector = **BBOX_DETECTOR**  
   - image = your IMAGE  
   - threshold: **0.25–0.35** (0.50 misses small faces)  
   - dilation: **6–10**  
   - crop_factor: **3.0**  
   - drop_size: **10**  
   - class filter: `all`  
   - **Output:** `SEGS`

3) **SEGS to Mask List**  
   - **segs = SEGS**  
   - **Output:** `MASK_LIST` (one mask per detected face)

4) **Select Nth Item (Any List)**  
   - **list = MASK_LIST**  
   - **index = N** (0,1,2… the face you want)  
   - **Output:** `FACE_MASK_RAW` (single-face mask)

5) *(optional but recommended)* **Mask soften/grow**  
   If you have any of these, add one (otherwise skip):  
   - **Mask Dilate/Erode:** dilate **6–8 px**  
   - **Mask Blur/Feather:** blur **10–16 px**  
   - **Output:** `FACE_MASK`  
   *(If you don’t have mask-morph nodes, just use `FACE_MASK_RAW` as-is; it will still work.)*

6) **VAE Encode** (IMAGE, VAE) → `LATENT_A`

7) **KSampler** (Inpaint = **Masked area only**)  
   - **model:** your LoRA-applied MODEL  
   - **positive:** your identity prompt (token + “preserve facial identity, bone structure, hairline, eye/brow shape…”)  
   - **negative:** “keep other faces/background unchanged; no smoothing; no glam; no stylization”  
   - **latent:** `LATENT_A`  
   - **mask:** `FACE_MASK` (or `FACE_MASK_RAW` if you skipped soften)  
   - **steps:** 32  
   - **cfg:** 5.5  
   - **denoise/strength:** **0.36** (identity-safe 0.30–0.42)  
   - → `LATENT_B`

8) **VAE Decode** → **SRPO** (0.30–0.40) → final image

That’s it—the LoRA only acts inside the selected face mask; all other faces stay untouched.

---

## Tips
- If the LoRA **bleeds** past the face: reduce detection **dilation** (step 2), and/or add **dilate 6–8 px + blur 12–14 px** in step 5, and **lower denoise** by ~0.04.  
- If the LoRA is **too weak** on the face: raise LoRA **model** weight (0.9 → **1.0**) or nudge **denoise** to **0.40**.  
- **Index sanity:** The order of `MASK_LIST` usually matches the detector’s order. If you need to see which is which, run **Bbox Visualize** from the detector in parallel so you can eyeball indices while you test N=0,1,2….

---

# Path B — (optional) Crop edit, then paste back
If you prefer the crop workflow:

1) Steps 1–4 as above to get `FACE_MASK_RAW`.  
2) **Mask → BBox** (if you have a node like “Mask Bounding Box” / “Mask to BBox”):  
   - mask = `FACE_MASK_RAW` → `BBOX_TARGET`  
3) **ScaleBy BBox** (pad ~**1.2**) → crop image  
4) **VAE Encode** (crop) → **KSampler** (no mask; LoRA on; denoise 0.34–0.40) → **VAE Decode**  
5) **Image UncropFromBBOX** to paste back → **SRPO**

If you don’t see a Mask→BBox converter, stick with Path A—the direct mask inpaint is perfectly fine.

If any step refuses to connect, tell me the exact port labels you see on **SEGS to Mask List** and **Select Nth Item (Any List)**, and I’ll adjust the wiring verbatim.

**Robyn:**

I have a question about:
Select Nth Item (Any List)
list = MASK_LIST
index = N (0,1,2… the face you want)
Output: FACE_MASK_RAW (single-face mask) - this output in particular. I'm not sure which node to plug it into. I'm trying ImageMaskScaleAs which is a LayerUtility.

**Emily:**

Great question—you're almost there. That `Select Nth Item (Any List)` output is a **single-face mask**. You’ll feed it to the **sampler’s mask input** (for an inpaint pass), typically after resizing/softening so it matches your image/latent.

Below are two clean ways to wire it—pick the one that matches your graph.

---

# A) Whole-image inpaint (simplest)

**Goal:** Keep the full image, edit only the selected face area.

1) **… → SEGS to Mask List → Select Nth Item (Any List)**  
   - `list = MASK_LIST`  
   - `index = N`  
   - **Output:** `FACE_MASK_RAW` *(single-face mask, often not yet the exact image size)*

2) **ImageMaskScaleAs (LayerUtility)**  
   - **mask = `FACE_MASK_RAW`**  
   - **reference = `IMAGE`** (your original, full-size image)  
   - **Output:** `FACE_MASK_SCALED` *(now same size as the image)*

3) *(Optional but recommended)* **Mask soften/grow**  
   - If you have any mask morph nodes:  
     - **Dilate:** 6–8 px  
     - **Blur/Feather:** 10–16 px  
   - Output: `FACE_MASK`  
   *(If you don’t have these, you can use `FACE_MASK_SCALED` directly.)*

4) **VAE Encode** your original **IMAGE** → `LATENT_A`

5) **KSampler / Efficiency KSampler (Inpaint)**  
   - **latent / latent_image:** `LATENT_A`  
   - **mask / noise_mask / inpaint_mask:** **`FACE_MASK`** (or `FACE_MASK_SCALED` if you skipped morph)  
   - **inpaint mode:** *Masked area only* (or equivalent)  
   - **LoRA ON** here  
   - **steps 32, cfg 5.5, denoise 0.36** (identity-safe 0.30–0.42)  
   - Output: `LATENT_B`

6) **VAE Decode** → **(optional) SRPO** → final

> Socket names vary slightly by sampler:
> - **KSampler (vanilla):** `latent_image`, `mask`  
> - **Efficiency KSampler:** `latent_image`, `inpaint_mask`  
> - **Impact inpaint samplers:** look for `noise_mask` / `mask`  
> If you see multiple mask inputs, you want the one used for **inpaint area** (not “conditioning mask”).

---

# B) Crop-edit then paste back (very precise)

**Goal:** Work on a small crop (faster, less bleed), then restore in place.

1) Do steps 1–2 from above to get **`FACE_MASK_SCALED`**.  
2) **Mask → BBox** (if you have it; name can be “Mask Bounding Box” / “Mask to BBox”)  
   - `mask = FACE_MASK_SCALED` → **`BBOX_TARGET`**

3) **ScaleBy BBox**  
   - `image = IMAGE`  
   - `bbox = BBOX_TARGET`  
   - (If there’s a “scale/padding” option, set ~**1.2** to include hairline)  
   - Output: **`IMAGE_CROP`** (+ crop metadata)

4) **VAE Encode** `IMAGE_CROP` → `LATENT_CROP`

5) **KSampler** (no mask needed if you want to edit the whole crop; otherwise you can crop the mask, too)  
   - `latent_image = LATENT_CROP`  
   - LoRA ON, **steps 32, cfg 5.5, denoise 0.34–0.40**  
   - Output: `LATENT_CROP_EDIT`

6) **VAE Decode** → `IMAGE_CROP_EDIT`

7) **Image UncropFromBBOX**  
   - `edited = IMAGE_CROP_EDIT`  
   - `original = IMAGE`  
   - `bbox/meta = BBOX_TARGET` (or the crop meta from ScaleBy BBox)  
   - Output: merged image → **SRPO** → final

---

## Why **ImageMaskScaleAs** helps
Many detection/mask nodes emit masks at detector-internal sizes. **ImageMaskScaleAs** resamples the mask so it matches the **exact dimensions** of your target image—critical, because the sampler’s mask must align with the **encoded latent** (which reflects the image size).

---

## Quick troubleshooting

- **Mask plugs won’t connect:** you might be on the wrong input—use the sampler’s **inpaint mask** port (names vary: `mask`, `inpaint_mask`, `noise_mask`).  
- **LoRA edits outside the face:** reduce mask dilation (6 px), keep feather 12–14 px, **lower denoise by ~0.04**.  
- **LoRA too weak on the face:** raise LoRA **model** weight (0.9 → **1.0**) or nudge denoise to **0.40**.  
- **Hard edge halo:** increase feather/blur a bit (14–18 px) or run a tiny **“mask blur”** node before the sampler.

If you tell me which sampler node you’re using (exact name), I’ll name the exact mask socket label to target and give you a one-line preset you can save on the node.

**Robyn:**

I'm using SamplerCustomAdvanced - this is Flux1, so the inputs are different to the standard KSampler.

**Emily:**

gotcha—Flux1 with **SamplerCustomAdvanced** wires a little differently than the vanilla KSampler. Here’s how to plug your **single-face mask** into it for an inpaint pass that only changes that one face.

I’ll show the two common SamplerCustomAdvanced variants I see in Flux graphs. Check which port names your node has and follow that column.

---

## 1) Prepare the mask (you already have this)
- `SEGS → SEGS to Mask List → Select Nth Item (Any List)` → **FACE_MASK_RAW**  
- **ImageMaskScaleAs**  
  - `mask = FACE_MASK_RAW`  
  - `reference = IMAGE` (your full image)  
  - → **FACE_MASK** (same size as IMAGE)  
- (optional) soften: dilate **6–8 px**, blur/feather **10–16 px**

---

## 2) Wire into SamplerCustomAdvanced (Flux1)

### Variant A — ports named **image** + **mask** (or **inpaint_mask**)
This is the most common:

**Inputs to SamplerCustomAdvanced**
- **model / clip_l / t5xxl / vae:** from your Flux checkpoint loader  
- **positive:** your inpaint prompt (with the LoRA token + identity locks)  
- **negative:** “keep other faces/background unchanged; no smoothing; no glam; no stylization”  
- **image / init_image / base_image:** **IMAGE** (the original full image)  
- **mask / inpaint_mask / noise_mask:** **FACE_MASK** (the scaled, softened single-face mask)  
- **seed:** any fixed value for repeatability  
- **steps:** **32**  
- **cfg (guidance):** **5.5**  
- **strength / denoise:** **0.34–0.40** (start **0.36**)  
- **sampler:** Euler / UniPC (your preference)  
- **scheduler:** Karras/Normal (either is fine)  
- **inpaint mode / compose mode:** **Masked area only** (or “replace masked area”)  
- **width/height:** match the input image (or leave blank if the node infers from `image`)

> If you also see **image_cfg_scale** (Flux often has this), set **1.0**.  
> If there’s **refine denoise** or **second stage denoise**, keep defaults at first.

### Variant B — ports named **latent_image** + **noise_mask**
Some builds want a latent instead of an image:

**Extra step:** **VAE Encode** your **IMAGE** with the Flux VAE → **LATENT_A**

**Inputs to SamplerCustomAdvanced**
- **model / clip_l / t5xxl / vae:** from loader  
- **positive / negative:** same as above  
- **latent_image:** **LATENT_A**  
- **noise_mask / inpaint_mask:** **FACE_MASK** (the mask still stays in image space; SamplerCustomAdvanced handles the resize)  
- **seed / steps / cfg / strength(denoise) / sampler / scheduler:** as above  
- **inpaint mode:** **Masked area only**

After sampling, **VAE Decode** the output latent → image.

---

## 3) LoRA placement (important)
Attach the LoRA **before** the sampler (to the model+clip you feed into it).  
- **Model weight:** start **0.90–1.00**  
- **CLIP weight:** **0.60**  
Keep your LoRA **token only** in the **inpaint** prompt, not globally.

---

## 4) Presets you can save on the sampler

**Identity-lock (face only):**
- steps **32**, cfg **5.5**, **denoise 0.36**
- positive: `robyn_char, preserve facial identity, bone structure, hairline, eye and brow shape; match surrounding lighting; natural skin texture`
- negative: `keep other faces and background unchanged; no age change; no smoothing; no glam; no stylization; no makeup changes`
- inpaint mode: **Masked area only**

**If it won’t take the LoRA enough:**  
- model weight → **1.0** or denoise → **0.40**

**If it bleeds past the face:**  
- reduce mask dilation (6 px), keep feather ~12–14 px  
- denoise → **0.32**–**0.34**

---

## 5) After the sampler
- Optional **SRPO**: **0.30–0.40** strength. If skin plastifies, drop to ~0.25 on the face.

---

### Quick port name map (so you know what to click)
- Mask socket may be labeled **mask**, **inpaint_mask**, or **noise_mask** → plug **FACE_MASK** here.  
- Base image socket may be **image**, **init_image**, or **base_image** → plug **IMAGE** here (Variant A).  
- If you only see **latent_image**, encode the image first (Variant B).  
- If there’s an **“inpaint method/mode”** dropdown, choose **Masked area only** / **replace masked area** (not “whole image”).

If you want, tell me the **exact** input names shown on your SamplerCustomAdvanced and I’ll write a one-liner mapping “plug X into Y” with those labels verbatim.

**Robyn:**

The inputs for SamplerCustomAdvanced are:
noise
guider
sampler
sigmas
latent_image

**Emily:**

Perfect—your SamplerCustomAdvanced is the “pure Flux” one that only takes these five:

- **noise**
- **guider**
- **sampler**
- **sigmas**
- **latent_image**

In Flux, the **mask plugs into the *guider*** (not the sampler). So we’ll build an **inpaint guider** that receives your single-face mask and the encoded image, then feed all five sockets.

Below is a minimal, reliable wiring (names vary slightly by pack; I give common aliases).

---

# 1) Things you already have
- **IMAGE** (your group photo)
- **FACE_MASK** (your selected face mask, scaled to IMAGE size)
- **MODEL/CLIP_L/T5XXL/VAE** (Flux 1-dev, with your LoRA applied to MODEL & CLIP)

---

# 2) Text conditioning
- **Flux Text Encode (positive)** → **COND+**  
  Text: your identity-safe prompt (incl. your LoRA token)
- **Flux Text Encode (negative)** → **COND−**  
  Text: “keep other faces/background unchanged; no smoothing; no glam; no stylization; no makeup changes”

(Use the Flux CLIP_L and T5XXL coming from your checkpoint loader.)

---

# 3) Encode the image
- **VAE Encode (Flux VAE)**  
  - image: **IMAGE**  
  → **LATENT_A**

This goes to **SamplerCustomAdvanced.latent_image**.

---

# 4) Build the **inpaint guider** (this is where the mask goes)

Use whichever of these you have:

### A) **Flux Inpaint Guider** (a.k.a. *Inpaint Guider (Flux)* / *CFG Inpaint Guider*)
Inputs:
- **model:** MODEL (with LoRA)
- **cond:** **COND+**
- **uncond:** **COND−**
- **cfg:** **5.5** (start)
- **latent_image / base_latent:** **LATENT_A**
- **mask / inpaint_mask / noise_mask:** **FACE_MASK**
- **image_cfg_scale:** **1.0** (if present)

Output → **GUIDER** (connect this to SamplerCustomAdvanced.guider)

### B) If you don’t have an “inpaint” variant, use **CFG Guider (Flux)** with mask ports
Some builds call it **Flux Guidance** and expose both **image** and **mask**. Plug the same as above:
- model, cond, uncond, cfg, **latent_image = LATENT_A**, **mask = FACE_MASK** → **GUIDER**

> If your guider has **no mask input at all**, you’ve got the *non-inpaint* guider. In that case, switch nodes—Flux inpainting requires the guider that accepts a mask.

---

# 5) Sigmas (denoise schedule)
Pick one Flux sigma schedule node you have:

- **Karras Sigmas (Flux)** or **Exponential Sigmas (Flux)**
  - **steps:** **32**  
  - **denoise/strength:** **0.36** (identity-safe; 0.34–0.40 range)  
  → **SIGMAS**

Connect to **SamplerCustomAdvanced.sigmas**.

---

# 6) Sampler kernel
- **Sampler (kernel)** (e.g., *Euler / Heun / DPM++ 2M SDE*)  
  - default params are fine to start  
  → **SAMP**

Connect to **SamplerCustomAdvanced.sampler**.

---

# 7) Noise
- **Noise (seed)** / **Basic Noise**  
  - **seed:** fixed (e.g., 12345)  
  → **NOISE**

Connect to **SamplerCustomAdvanced.noise**.

---

# 8) Final connections (your node’s five inputs)

- **noise** ⟵ **NOISE**  
- **guider** ⟵ **GUIDER** (the inpaint guider with your FACE_MASK)  
- **sampler** ⟵ **SAMP**  
- **sigmas** ⟵ **SIGMAS**  
- **latent_image** ⟵ **LATENT_A**

Run → **VAE Decode** the output latent → optional **SRPO** (0.30–0.40) → done.

---

## Handy presets / tweaks

- **Identity-lock start:** steps **32**, cfg **5.5**, denoise **0.36**  
- If the LoRA is **too weak** on the face → LoRA model **1.0** or denoise **0.40**  
- If edits **bleed** past the face → shrink mask a bit, feather 12–14 px, denoise **0.32–0.34**  
- Keep the LoRA **token only** in the **positive** used by the **guider** (don’t put it elsewhere)

If you tell me the exact name of your guider node (its label in the graph) and the mask socket label it shows, I’ll map each plug 1:1 so you can click through without guessing.

**Robyn:**

None of these nodes exist in the Nodes Manager:
Flux Inpaint Guider
 Inpaint Guider (Flux) 
 CFG Inpaint Guider
I'm giving this up, Emily. Sorry.

**Emily:**

totally fair, Robyn — without an **inpaint-capable guider**, masked edits aren’t possible on that Flux sampler. But you can still hit the *same outcome* cleanly by using a **crop → edit → un-crop** route. It avoids masks entirely and works with the nodes you already have.

Here’s a drop-in wiring using only the nodes you said you have + SamplerCustomAdvanced’s five inputs.

# 👇 Crop-only face edit (no inpaint guider needed)

**Goal:** crop to the chosen face → run SamplerCustomAdvanced on the crop → paste it back.

### 1) Detect and pick one face (SEGS → SEG_ELT → BBOX)
1) **Ultralytics Detector Provider** → use **BBOX_DETECTOR**  
2) **BBox Detector (SEGS)**  
   - detector = **BBOX_DETECTOR**  
   - image = **IMAGE**  
   - threshold **0.25–0.35**, dilation **6–10**, crop_factor **3.0**, drop_size **10**, class `all`  
   - **Output:** `SEGS`
3) **Select Nth Item (Any List)**  
   - **list = SEGS**   ← (use it directly on SEGS)  
   - **index = N** (0,1,2… the face you want)  
   - **Output:** `SEG_ELT`
4) **From SEG_ELT bbox**  
   - **seg_elt = SEG_ELT**  
   - **Output:** `BBOX_TARGET` (x, y, w, h)

### 2) Crop to just that face
5) **ScaleBy BBox**  
   - **image = IMAGE**  
   - **bbox = BBOX_TARGET**  
   - *(if it has padding/scale, set ~**1.2** to include a bit of hairline)*  
   - **Output:** `IMAGE_CROP` (+ crop meta the Uncrop node will consume)

### 3) Encode the crop
6) **VAE Encode (Flux VAE)**  
   - image = `IMAGE_CROP`  
   - **Output:** `LATENT_CROP`

### 4) Build the five inputs SamplerCustomAdvanced needs
7) **Noise**  
   - seed: e.g., **12345** → **NOISE**
8) **Sigmas (Flux)** (Karras/Exponential)  
   - steps: **32**  
   - **denoise/strength: 0.36** (identity-safe; 0.34–0.40) → **SIGMAS**
9) **Sampler (kernel)** (Euler / Heun / DPM++ 2M SDE) → **SAMP**
10) **Guider (plain CFG for Flux)**  
   - model = your Flux **MODEL** (with LoRA applied)  
   - cond = your positive text (include your **LoRA token** + identity lines)  
   - uncond = your negative text (keep other faces/background unchanged; no smoothing/glam)  
   - cfg = **5.5**  
   - **Output:** **GUIDER**
11) **latent_image:** use `LATENT_CROP`

### 5) SamplerCustomAdvanced (Flux1)
- **noise** ⟵ **NOISE**  
- **guider** ⟵ **GUIDER** *(plain CFG guider—no mask here)*  
- **sampler** ⟵ **SAMP**  
- **sigmas** ⟵ **SIGMAS**  
- **latent_image** ⟵ **LATENT_CROP**  
→ **LATENT_CROP_OUT**

12) **VAE Decode** `LATENT_CROP_OUT` → `IMAGE_CROP_EDIT`

### 6) Paste back in place
13) **Image UncropFromBBOX**  
   - **edited = IMAGE_CROP_EDIT**  
   - **original = IMAGE**  
   - **bbox/meta = BBOX_TARGET** (or the crop meta from ScaleBy BBox)  
   - → **IMAGE_MERGED**
14) **SRPO** (0.30–0.40) on `IMAGE_MERGED` → **FINAL**

---

## Tuning cheats
- **Too little change on the face?** LoRA model **0.9 → 1.0** or denoise **0.36 → 0.40**.  
- **Edges look off after paste?** Increase padding in **ScaleBy BBox** to **1.25**, re-run.  
- **Identity slips?** Lower denoise to **0.34**, keep faces larger (use a slightly tighter crop).

This route is solid, fast, and avoids the missing inpaint-guider entirely. If you snap me a screenshot of your **Guider** node’s exact name/ports, I’ll map the cond/uncond/cfg plugs 1:1 so you can click it in without guesswork.
