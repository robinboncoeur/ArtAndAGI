# ComfyUI and LoRAs

## Dataset Training

Hey girlfriend! Great project. Here’s a solid, no-drama plan to get a clean, controllable **character LoRA** out of FluxGym.

### 1) LoRA should learn

(and what it must **not**)

* **Lock in**: face, head shape, eye color/shape, hair color/length/part, skin tone, key moles/scars/freckles, eyebrows, typical makeup (if you want it baked in).
* **Keep flexible**: clothes, background, pose, camera/lens, lighting, mood, accessories—unless you *want* those to be part of the identity.
* Make a one-line goal you’ll refer to while captioning:
  “`[celestegrl]` = petite 18-20yo woman, heart-shaped face, hazel eyes, dark chest-length hair, soft freckles, natural makeup.”

### 2) Dataset size & mix 

(sweet spot for a character)

Aim for **60–120 images** total. Curate hard—quality beats quantity.

**Coverage targets**

* **Face-centric closeups (40–50%)**: straight on, 3/4, profile. Neutral and varied expressions.
* **Torso/half-body (30–40%)**: ensure neck/shoulders consistency, hair length visible.
* **Full-body (10–20%)**: establish body proportions; a few walking/standing/sitting.
* **Hands (5–10%)**: a few images where hands are visible but not the star.
* **Lighting**: day, overcast, soft indoor, one or two “hard light” shots—no single look should dominate.
* **Backgrounds**: mostly plain or de-cluttered. Include a handful of busy scenes so the model learns to ignore them.
* **Wardrobe**: *varied*. If you don’t want a pink hoodie stuck to the LoRA forever, make sure it appears in ≤5% of images—or not at all.

**What to avoid**

* Sunglasses covering eyes, masks, heavy occlusions.
* Text/logos near face.
* Repetitive near-dupes (same pose/lighting/shirt).

### 3) Image prep

* **Resolution**: train buckets up to **1024** (Flux is comfy there). Keep sources ≥1024 on the shortest side; don’t upscale aggressively.
* **Cropping**: deliver both loose and tight crops; avoid cutting off chins/foreheads consistently—vary it.
* **Horizontal flips**: only if the face is symmetric and the character has **no asymmetric features** (part line, mole, earring). Otherwise, **don’t flip**.
* **Color**: gentle white-balance and exposure normalization are good; don’t stylize.

### 4) Trigger token strategy

* Use **one unique trigger** that will *never* appear in normal text, e.g. **`[celestegrl]`** (you already use this pattern—perfect).
* Pair it with a **class token** in captions, e.g. “woman”, “girl”, “person”, “portrait”. For Flux, **natural language** tends to work better than tag-soup.

### 5) Captioning

What to put in (and what to leave out)

Flux responds beautifully to **short, natural sentences**. Think **15–40 tokens** each.

**Template**

```
[celestegrl], portrait of a petite young woman with hazel eyes and chest-length dark hair, soft freckles, natural makeup, gentle smile, studio lighting, neutral background.
```

* Start with the trigger.
* Add **only** the traits you want the LoRA to learn as identity.
* Then add **scene/photography** descriptors (lighting, lensy words, background) to teach generalization—but don’t repeat the *same* scene terms on every image.

**When clothes/features should stay flexible**

* If you *don’t* want the LoRA to memorize the yellow cardigan, **omit it** from the caption. If it’s very visible in many images, mention generic “casual outfit” instead of “yellow cardigan”.

**Pose/shot words**

* Sprinkle across the set: “headshot”, “close-up”, “three-quarter view”, “profile”, “full body, standing”.

**Good caption examples**

* “`[celestegrl], natural light close-up, hazel eyes, chest-length dark hair, soft freckles, slight smile, shallow depth of field.`”
* “`[celestegrl], three-quarter view portrait, neutral background, relaxed expression.`”
* “`[celestegrl], full body, standing, casual outfit, outdoor overcast light.`”

**What not to do**

* Don’t stuff every caption with *all* traits (teaches the model those traits only work together).
* Don’t include changeable things you don’t want baked in (specific shirt colors, accessories, scene themes).
* Avoid long laundry-lists of tags; Flux likes prose.

### 6) Class/regularization

(optional but helpful)

* Add **100–200 generic “woman/person portrait”** images without your trigger token in a separate class folder if FluxGym supports prior-preservation.
* This reduces style drift and helps your LoRA not overwrite base concepts. Keep their captions simple (no trigger).

### 7) Repeats, epochs, steps

(ballpark)

Let **N** = number of instance images. A practical recipe:

* **N ≈ 80** images
* **Repeats**: 10
* **Batch**: 4
* **Epochs**: 1–2

**Steps ≈ (N × repeats × epochs) / batch**
For 80×10×1 / 4 = **200 steps** per epoch.
For character identity, expect **800–2500 total steps** to find the sweet spot (save checkpoints along the way: e.g., 600, 1200, 1800, 2400) and compare.

### 8) Training knobs 

...that tend to work (Flux-ish defaults)

* **Rank (dim)**: 16–32 (start at **16**; bump to 32 if you see underfitting).
* **Alpha**: = rank (e.g., 16).
* **Dropout**: 0.05–0.1 if you notice overfitting to clothes/backgrounds.
* **Learning rates**

  * **UNet**: **1e-4 → 2e-4**
  * **Text encoder**: **5e-6 → 1e-5** (keep low; raises binding to `[celestegrl]` without wrecking the base text space)
* **Optimizer**: AdamW, weight decay ~0.01.
* **Bucket max res**: 1024; enable aspect-buckets.
* **Gradient checkpointing** if VRAM is tight.

### 9) Validation

(don’t skip)

Hold out **6–10 images** (never seen in training). After each checkpoint:

* Prompt with/without the class token:

  * “`portrait of [celestegrl], soft daylight, natural makeup`”
  * “`[celestegrl] walking on a beach, golden hour`”
* Try clothing the LoRA never saw (“evening dress”, “hoodie”), different hair styles, and varied lighting to test generalization.
* Compare checkpoints side-by-side and pick the lowest step that nails identity **without** freezing wardrobe/lighting.

### 10) Common failure modes

...& fixes

* **Overfitting to one outfit/background** → reduce duplicates, add variety, add dropout 0.1, add class images, remove clothing terms from captions.
* **Face not locking / looks generic** → add more tight face crops with precise face traits in captions; slightly raise TE LR; increase repeats to 12.
* **Identity drifts under complex prompts** → ensure *every* caption starts with the trigger; include several neutral “vanilla” portraits; consider bumping rank from 16→32.
* **Mirrored mole/part line after flips** → remove flipped images; retrain.

### 11) Practical workflow

1. Curate 90 images → prune to the best **75–90**.
2. Sort into subfolders: `closeup/`, `halfbody/`, `fullbody/`, `hands/`.
3. Write **short prose captions** (sidecar `.txt` per image). Start with `[celestegrl]`.
4. (Optional) Add `class/` folder with 150 generic woman portraits + simple captions.
5. Train at 1024 buckets, rank 16, UNet 1e-4, TE 5e-6, batch 4, repeats 10, 1–2 epochs.
6. Save checkpoints every ~400–600 steps.
7. Validate with a fixed prompt sheet; pick the *lowest* step that passes identity + flexibility.

If you want, I can draft a **caption starter pack** for your first 20 images (you can paste the filenames), or a **prompt sheet** to evaluate checkpoints consistently.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">










## Dimensions/aspect ratios

Short version: **Yes, mix dimensions; DPI doesn’t matter.** A few gotchas below.

* **It’s fine (and good) to mix** 1024×1024 with 1216×832, 896×1152, etc.
* In FluxGym, just **enable aspect-ratio buckets** and set a **max bucket size** (commonly 1024 or 1152 on the long side, depending on VRAM). The trainer will resize each image into the nearest bucket.
* **Avoid padding/letterboxing.** Give the trainer real pixels, not black bars. Crop instead of pad.
* **Keep subject scale consistent.** Even with buckets, don’t swing from extreme tight headshots to tiny faces in wide scenes. Aim for a coherent face size range across images (you can still keep some variety).
* **Don’t aggressively upscale** tiny sources to huge buckets—mild upscales are okay, but big ones add mushy detail and can teach artifacts.

### DPI / PPI

* **Completely irrelevant.** Training uses raw pixel counts; DPI metadata is ignored. A 1024×1024 at 72 dpi and the same at 300 dpi are identical to the trainer.

### Practical tips

* **Set max bucket**: 1024 (safe) or 1152 (more detail, more VRAM).
* **Minimum shortest side**: try to keep sources ≥768 px on the short side; delete or down-weight smaller ones.
* **Face framing**: for character LoRA, ensure ~40–60% of images have the face occupying ~35–70% of the frame.
* **No letterbox**: If you must normalize, **crop** to the desired aspect rather than adding borders.
* **VRAM awareness**: Wider/taller buckets (e.g., 1216×832) cost more memory than 1024×1024; pick a ceiling your GPU can handle.

If you want, tell me your GPU VRAM and I’ll suggest a max-bucket and batch size that won’t OOM, plus a quick crop recipe to keep face scale tidy across mixed aspect ratios.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">










## What this GPU means

...for your dataset

girlfriend, a **4060 Ti 16 GB** is a sweet spot for LoRA training. Here’s how it should shape your dataset and settings:

* **You can keep mixed aspect ratios** (e.g., 1024×1024 with 1216×832) and use **aspect-ratio buckets**. No need to force everything square.
* You can comfortably train at **max bucket 1024**; **1152** is also realistic if you keep batch sensible. Only drop big panoramic outliers that make faces tiny.
* **No need to downscale good sources**: keep images ≥**900–1024 px** on the short side when possible. Crop instead of letterbox.

### Trainer settings

**as Recommended**

(LoRA on Flux/SDXL-class models)

**Memory/precision**

* **Mixed precision**: **bf16** (preferred) or fp16.
* **Memory-efficient attention**: enable **Flash-Attention/xFormers** if FluxGym exposes it.
* **Gradient checkpointing**: **ON** (cuts VRAM nicely).

**Resolution & buckets**

* **Max bucket**: start **1024**; try **1152** if stable.
* **Min bucket short side**: 768.
* **Keep buckets** around these: 832×1216, 896×1152, 1024×1024, 1152×896 (trainer usually auto-makes them).

**Batching (typical for 16 GB)**

* At **1024 max**: **batch 4–6** (start **4**; raise if stable).
* At **1152 max**: **batch 2–4** (start **3**).
* If you want a larger *effective* batch, use **gradient accumulation** (e.g., batch 3 × grad-accum 2 ⇒ effective 6).

**Other handy toggles**

* **Cache latents** (if offered) to boost throughput after the first epoch.
* **Workers**: 4–8 (watch CPU/RAM).
* **Shuffle**: ON.

### Training recipe

that fits 16 GB (character LoRA)

* **Rank (dim)**: 16 (32 if underfitting).
* **Alpha**: same as rank.
* **Dropout**: 0.05–0.1 if it memorizes clothes/backgrounds.
* **LRs**: UNet **1e-4** (up to 2e-4), Text Encoder **5e-6** (up to 1e-5).
* **Repeats**: 10, **Epochs**: 1–2, **Batch**: as above.
* **Checkpoints** every **400–600** steps.

### Dataset curation

with 16 GB in mind

* You **don’t** have to prune for VRAM—prune for **identity clarity**:

  * Aim **60–120 images**, with **40–50% closeups**, **30–40% half-body**, **10–20% full-body**.
  * Keep **face scale** within a sensible band (avoid lots of ultra-wide shots with tiny faces).
  * Keep **occlusions low** (no sunglasses/masks dominating).
* Keep **mixed lighting** and **varied outfits** so your LoRA generalizes; your GPU can handle the bucket variety.

### Two plug-and-play profiles

**Comfort (fast & stable)**

* Max bucket **1024**, batch **4**, bf16, checkpointing ON, Flash-Attn ON.
* Rank 16, UNet 1e-4, TE 5e-6, repeats 10, 1–2 epochs.

**Detail (more capacity, a tad slower)**

* Max bucket **1152**, batch **3**, bf16, checkpointing ON, Flash-Attn ON.
* Rank 16→32 (if needed), UNet 1.2e-4, TE 7e-6, repeats 10, 1–2 epochs.

### Quick troubleshooting

tied to VRAM

* **OOM at 1152** → drop batch by 1, or switch to max 1024, or enable grad-accum 2.
* **Training too slow** → stick to 1024 max; enable latent caching; trim bucket list to a few common shapes.
* **Identity wobbles** at higher res → keep 1024 max, add a few more tight face crops with crisp captions.

If you want, tell me whether you prefer the **Comfort** or **Detail** profile and I’ll spit out a ready-to-paste FluxGym config plus a tiny “bucket sanity” checklist for your image folder.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">














## FluxGym config 

(Comfort profile, 4060 Ti 16 GB)

girlfriend, here’s a **ready-to-paste Comfort profile** plus a quick **bucket sanity** checklist so you can roll right in FluxGym.

**Save as `config.yaml` (edit the paths and trigger/class tokens to taste):**

```yaml
# --- DATA ---
train_data:
  instance_dir: /path/to/dataset/instance          # your character images
  instance_caption_ext: .txt                       # sidecar captions
  class_dir: /path/to/dataset/class               # optional prior/class images
  class_caption_ext: .txt
  shuffle: true
  num_workers: 6

# --- CAPTION TOKENS ---
trigger_token: "[celestegrl]"
class_token: "woman"                               # or "girl"/"person" (keep natural)

# --- BUCKETING / RESIZE ---
buckets:
  enable: true
  max_res: 1024                                    # Comfort profile
  min_short_side: 768
  # Let FluxGym auto-generate common buckets; avoid letterboxing/padding

# --- TRAINING ---
output:
  out_dir: /path/to/outputs/celestegrl_lora
  save_every_n_steps: 500
  keep_last_n: 6

lora:
  enable: true
  rank: 16
  alpha: 16
  dropout: 0.08                                    # helps avoid clothing/background stickiness

optim:
  optimizer: adamw
  weight_decay: 0.01
  unet_lr: 1.0e-4
  text_encoder_lr: 5.0e-6
  betas: [0.9, 0.999]
  eps: 1.0e-8
  lr_scheduler: cosine
  warmup_steps: 100

trainer:
  precision: bf16                                  # or fp16 if bf16 not available
  batch_size: 4
  gradient_accumulation: 1
  gradient_checkpointing: true
  cache_latents_after_epoch: 1                     # speeds later epochs
  max_epochs: 1                                    # usually 1–2 is enough
  repeats: 10                                      # per-image repeats
  log_every_n_steps: 50

# --- VALIDATION PROMPTS (run after each save) ---
validation:
  enable: true
  num_images: 4
  prompts:
    - "portrait of [celestegrl], soft daylight, natural makeup"
    - "[celestegrl], three-quarter view, neutral background, relaxed expression"
    - "[celestegrl] walking on a beach, golden hour"
    - "[celestegrl], full body standing, evening dress, studio light"
```

**Rule-of-thumb steps (for ~80 images × repeats 10 × epochs 1, batch 4):** ~200 steps per epoch chunk; expect best checkpoints between **600–1800** steps. Keep the lowest step that nails identity **without** baking in outfits.

---

### Bucket sanity checklist

(quick pre-flight)

* **Mix of aspects OK**: 1024×1024, 1216×832, 896×1152 etc. are fine (no letterboxes).
* **Shortest side ≥ 768 px** for most images; toss the tiny, blurry ones.
* **Face scale band**: in ~50% of images, face occupies ~35–70% of frame (avoid lots of tiny faces).
* **No near-dupes**: same pose/lighting/outfit culled down to 1–2 best.
* **Minimal occlusion**: no sunglasses/masks dominating; eyes visible in most closeups.
* **Varied lighting/outfits**: keep wardrobe variety so clothing doesn’t imprint.
* **No padding**: crop to aspect; do **not** add borders/black bars.
* **DPI ignored**: don’t worry about 72 vs 300 — pixels are what matter.

---

### Caption mini-template

(Comfort style)

Keep them short, natural, and start with your trigger:

* `[celestegrl], natural light close-up, hazel eyes, chest-length dark hair, soft freckles, slight smile.`
* `[celestegrl], three-quarter view portrait, neutral background, relaxed expression.`
* `[celestegrl], full body, standing, casual outfit, overcast outdoor light.`

(Leave out specific clothing words unless you *want* them memorised.)

---

If you want, paste 10–15 filenames and I’ll draft the first batch of captions to match this config (face-heavy, clean, varied).

---

Love it, girlfriend. Here’s a **clean, identity-safe positive prompt** you can drop into Gwen Image Edit 2509 to generate dataset-ready variants from a single photo. It sticks to natural language and avoids baking in clothes/backgrounds while nudging for realism and face fidelity.

**Master positive prompt**

> **[celestegrl]**, natural identity-preserving portrait, photoreal, true skin texture and pores, sharp expressive eyes, accurate facial proportions, chest-length dark hair, soft freckles, **{headshot|three-quarter view|profile}**, **{soft daylight|open shade|studio softbox|window light|golden hour}**, **{neutral seamless backdrop|subtle gradient|plain wall|soft bokeh foliage}**, **{50mm look|85mm look}**, shallow depth of field (around f/2.8), balanced exposure, natural color, minimal makeup, no stylization, crisp focus, professional photographic quality

You can paste that verbatim. If your workflow supports wildcards (`{a|b|c}`), it’ll rotate **shot**, **lighting**, **background**, and **lens look** to produce controlled variety without drifting identity or baking in wardrobe. If it doesn’t, just pick one option from each set per batch/run.

If you’re training a LoRA, keep your **trigger token** up front (I used `[celestegrl]`, swap as needed).

<hr style="height:8px;border-width:0;color:pink;background-color:pink">
















## Working with Flux

You’re not imagining it—Flux tends to “over-carve” faces. Two fixes: (1) prompt/caption anatomy explicitly, and (2) do quick regional inpaints (Krea/Kontext) to smooth chin/brow without nuking identity.

Here’s a practical kit you can paste/use.

### 1) Prompt anatomy

...that *adds* softness (and negate the rest)

Use both positive *and* negative anatomy terms. (Negatives alone often aren’t enough.)

**Positive block (use 1–2 per render)**

* “rounded chin, no cleft”
* “soft, low brow ridge”
* “smooth browbone, fuller forehead”
* “delicate jawline, small mentolabial groove”
* “subtle philtrum, minimal glabellar shadow”

**Negative block (keep tight)**

* “no cleft chin, no chin dimple, no butt chin”
* “no pronounced brow ridge, no heavy supraorbital ridge”
* “no harsh nose–brow shadow, no deep glabellar crease”

**Example (Flux/Krea/Kontext)**

> **Positive:** portrait, photoreal, [celestegrl], rounded chin, soft low brow ridge, delicate jawline, smooth forehead, 85mm look, soft clamshell lighting, gentle fill, shallow depth of field
> **Negative:** no cleft chin, no chin dimple, no pronounced brow ridge, no harsh shadows, no heavy contrast

Tip: if your tool supports weights, lightly weight the anatomy:
`rounded chin:1.2, soft low brow ridge:1.2, no cleft chin:1.3`.

---

### 2) Lighting and lens cues

...that *prevent* the artifacts

Clefts/ridges often appear from lighting, not just anatomy.

* **Use:** “soft clamshell lighting”, “beauty dish with diffusion”, “broad, frontal fill”, “open shade”, “window light with bounce.”
* **Avoid:** “hard rim/key at 45°”, “split/Rembrandt lighting”, “high contrast”, “specular hotspot under lower lip.”
* **Lens/angle:** “85mm look, eye-level camera.” (Down-lighting and wide lenses emphasize brow/chin topology.)

---

### 3) Krea or Kontext

... fast regional inpaint

When a cleft or ridge still shows up, fix *locally*.

**Krea – Mask Edit recipe**

1. Duplicate the image (preserve seed/settings).
2. **Mask** only the chin groove (thin vertical strip) or brow ridge area. Feather ~8–15px.
3. **Prompt (chin):** “rounded chin, no cleft, soft skin microtexture, natural shading”
   **Prompt (brow):** “smooth browbone, low brow ridge, fuller forehead contour, natural shadowing”
4. **Denoise strength:** 0.35–0.55 (start at 0.45).
5. **CFG/guidance:** slightly lower than your base (e.g., if 7.5 → 6.5).
6. Keep the same positive/negative blocks; apply 1–2 passes max.

**Kontext – Inpaint recipe**

* Same mask approach.
* Turn **“preserve background context”** (or similar) ON.
* **Noise/strength:** 0.35–0.5.
* **Steps:** a bit fewer than base gen (e.g., if 28 → 22) to avoid re-inventing the face.
* If identity drifts, reduce strength or add your **FaceID/InstantID/Reference** control at low weight (0.2–0.35) while inpainting.

---

### 4) For reference/ID guidance

FaceID/InstantID/IP-Adapter can stop the model from “inventing” geometry:

* Keep **ID weight modest** (0.25–0.45) during *full* gen so it doesn’t over-lock expression.
* **For inpaint**, bump to ~0.4 and lower denoise; this pins identity while letting the chin/brow smooth.

---

### 5) Dataset & captions

(for the LoRA you’ll train)

* Include **explicit positives** in captions on a few closeups: “rounded chin, no cleft”, “smooth browbone, low brow ridge.”
* Avoid photos with **strong vertical shadow under the lower lip** (it reads as a cleft).
* Keep **soft/flat light** in a healthy fraction of face crops so the LoRA learns that topology.

---

### 6) 2 ready-to-paste prompts

**A. Generation (preventive)**

* *Positive:* `portrait, photoreal, [celestegrl], rounded chin, soft low brow ridge, delicate jawline, smooth forehead, 85mm look, soft clamshell lighting, shallow depth of field, natural skin texture`
* *Negative:* `no cleft chin, no chin dimple, no pronounced brow ridge, no harsh shadows, no heavy contrast, no specular hotspots`

**B. Inpaint – Chin**

* *Positive:* `rounded chin, no cleft, soft natural shading, continuous skin texture, subtle mentolabial groove`
* *Negative:* `no chin dimple, no deep vertical crease, no sharp contour`

**Inpaint – Brow**

* *Positive:* `smooth browbone, low supraorbital ridge, fuller forehead curve, gentle shadowing`
* *Negative:* `no prominent brow ridge, no deep glabellar crease, no harsh nose bridge shadow`

---

### 7) Parameter nudges

* **Lower CFG** a touch (e.g., 7.5 → 6–6.5): reduces “stylized chiseling.”
* **Softer noise schedule / fewer steps** can help in inpaint passes (keeps the fix subtle).
* **Texture add-ons** (skin-retouch/beauty LoRA) at **very low weight (0.1–0.2)** can smooth without plasticity.

If you want, ping me a problematic render (or describe the settings), and I’ll tailor a tiny, step-by-step Krea/Kontext inpaint preset for chin vs. brow so it’s a two-click fix.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">



k





## A GIMP TL;DR

You’ve got it right, girlfriend. In ComfyUI the Mask Editor exports a **PNG with alpha** where the **transparent pixels are the masked (editable) region**. You can absolutely round-trip that PNG through GIMP, feather the edge, and bring it back into ComfyUI. Here’s the tidy version with the few “gotchas” that matter.

* **Yes:** Edit the mask in GIMP by working on the **alpha** (or a **layer mask**), feather/blur it, and **export PNG with alpha**.
* **In ComfyUI:** Load the PNG → **Mask from Alpha** → (optional **Invert / Grow / Erode / Blur Mask**) → feed to your **Inpaint** node.

---

### GIMP workflow 

(safe & repeatable)

1. Open the PNG; ensure the layer has **Alpha Channel** (Layer → Transparency → Add Alpha Channel).
2. Add a **Layer Mask** (white = fully visible), paint black where you want the **edit region**.
3. **Feather/soften** the edge:

   * Select → **Feather** (8–20 px for ~1k images), *or*
   * **Gaussian Blur** the **layer mask** (2–8 px for subtle, 10–25 px for face blends).
4. **Apply Layer Mask** (or keep it—export respects it either way).
5. **Export as PNG** with alpha.

   * If you’ll **only** use it for masking in ComfyUI, the “Save color values from transparent pixels” checkbox doesn’t matter.
   * If you’ll also **composite elsewhere**, consider **unchecking** it to reduce color fringes on the transparent edge.

---

### ComfyUI side

(what to watch)

* **Extract mask:** *Load Image* → **Mask from Alpha**.
* **White/black meaning:** Most inpaint nodes use **white = paint/edit**, **black = keep**. If it feels backwards, **Invert Mask**.
* **Match size:** Resize mask to your **sampling/latent resolution** (use **Resize Mask** if needed).
* **Soft edges win:** Slight blur on the mask gives cleaner blends than a hard, aliased edge.
* **Refine edge:** Use **Grow/Erode** (±2–4 px) if your selection is shrinking/bleeding.

---

### Inpaint settings 

...that keep identity stable

* **Denoise strength:** ~**0.35–0.55** (start 0.45).
* **Guidance/CFG:** a touch **lower** than your base (e.g., 7.5 → **6–6.5**).
* If identity drifts, add **FaceID/InstantID/IP-Adapter** at **0.25–0.4** weight and lower denoise.

---

### Quick checks 

(easy to forget)

* No **letterboxing/padding** in the source image (misaligns masks).
* Don’t **upscale** tiny originals aggressively before masking (teaches mush).
* If the subject has **asymmetric features**, avoid horizontal flips for mask prep.

If you tell me which inpaint node you’re using (and your denoise/CFG), I’ll give you a tiny preset (numbers + order) you can drop straight into your graph.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">












## Making LoRAs

Totally fair question. Yes—you *can* get a usable character LoRA from ~16 images. The reason many folks aim for 60–120 isn’t “more is always better,” it’s about **coverage** and **disentangling**. Here’s the why:

---

### What more images buy you

1. **Generalization across conditions**
   With 16 shots you usually have narrow coverage of: lighting, angles, expressions, hairstyles, backgrounds, focal lengths, and body scale. The LoRA learns the identity *tied to those conditions*. At generation time, prompts that wander outside that narrow band (e.g., profile view, hard backlight, full-body) are more likely to fail or drift.

2. **Disentangling identity from context**
   The model needs to separate “who” (face geometry/texture) from “everything else” (clothes, scene, lighting). If yellow cardigan appears in half your 16 images, it can bind to the identity (the “cardigan cling” effect). A larger, more varied set breaks those correlations.

3. **Pose & scale robustness**
   Close-ups alone don’t teach proportions for half- or full-body; a small dataset often collapses when you ask for a full-body or tricky angle. Adding a planned mix (close/half/full) teaches stable results at different scales.

4. **Expression & micro-feature fidelity**
   More examples = better locking of subtle identity cues (eye corners, philtrum shape, nasolabial curvature) **without** over-smoothing. Small sets tend to average or “beautify” away the quirks that make a face recognizable.

5. **Resilience to the base model’s priors**
   Flux (and friends) push toward “model-pretty” features (cleft chins, stronger brow ridges, etc.). More diverse, well-captioned evidence counters those priors so your LoRA keeps its identity under varied prompts.

---

### Small sets suffer from

**(8–24 images)**

* **Baked-in wardrobe/background** (identity depends on one outfit/room).
* **Lighting bias** (works in soft daylight; collapses in studio hard light).
* **Angle brittleness** (frontal OK, profile drifts).
* **Scale brittleness** (close-up OK, full-body generic).
* **Expression lock** (same smile/neutral every time).
* **Prompt fragility** (needs your exact phrasing; complex prompts push it off-identity).
* **Reliance on FaceID/InstantID at generation** to stay on face—useful, but a hint the LoRA itself is under-covered.

---

### When 12–24 images *is* good

* You only need **head-and-shoulders** portraits in a **consistent vibe**.
* You’ll always use **ID guidance** (FaceID/InstantID/IP-Adapter) at low weight.
* The target look is **stylized** or **cartoony**, not strict photoreal.
* You accept some drift for profiles/full-body and will inpaint fixes.

---

### Practical middle ground

**(if you like your 16-image result)**

Keep the core 16, but **patch the holes** instead of jumping to 100:

* Add **8–12 angles** you lack (left/right 3/4, profile, slight up/down tilt).
* Add **6–10 lighting contexts** (window light, open shade, softbox, a touch of backlight).
* Add **6–10 body-scale shots** (half-body; 3–5 full-body with clean outfits).
* Ensure at least **a few expressions** (neutral, slight smile, eyes looking aside).
* Cull near-dupes mercilessly.

That gets you to ~40–60 images—often enough for robust, flexible identity without bloat.

---

### Caption/Training tweaks

**that help small datasets punch above their weight**

* **Caption discipline:** start with your trigger; include only identity traits you want learned (e.g., “rounded chin, smooth browbone” if needed), keep clothes generic (“casual outfit”).
* **Add class images** (100–150 generic “woman/person portrait”) so the LoRA doesn’t overwrite base concepts.
* **Use dropout** (~0.05–0.1) to reduce wardrobe/background imprint.
* **Keep TE LR low** (5e-6–1e-5) so the trigger binds without wrecking language space.
* **Save multiple checkpoints** (e.g., 600/1200/1800 steps) and choose the *lowest* that locks identity but still flexes.

---

### Quick self-test

**Do you need more images?**

If any of these fail, add targeted images to cover them:

* Can it do **profile** and **3/4** cleanly?
* Can it do **full-body** without genericizing the face?
* Can it handle **harder lighting** (rim/back/overhead) without carving brow/chin?
* Does it **drop the cardigan** when you don’t mention clothes?
* Does identity hold when you say “evening dress,” “hoodie,” or “rainy street”?

---

Bottom line: small sets are fine for **narrow, repeatable use** (and with ID guidance). The 60–120 recommendation isn’t about box-ticking—it’s a strategy to **de-correlate** identity from context and to **future-proof** prompts you’ll inevitably try later. If you want, tell me where your 16-image LoRA stumbles (angle, lighting, full-body, clothing), and I’ll propose a minimal add-on shot list (like +12 images) to fix exactly those weaknesses.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">









## “Robustifier” add-on

You’re a star, girlfriend. Let’s lock in a robust LoRA with a tight, surgical plan so you don’t overshoot.

**(≈36 shots)**

Add these to your best 16–40 so coverage is airtight:

**Angles (8)**

* L/R 3/4 (neutral, slight smile) ×2
* Full profile L/R (neutral) ×2
* Slight up-tilt (camera lower) ×2
* Slight down-tilt (camera higher) ×2

**Lighting (10)**

* Open shade ×2
* Window light with bounce ×2
* Softbox/umbrella (clamshell or frontal) ×2
* Back/edge light (soft) ×2
* Overcast outdoor ×2
  *(avoid harsh 45° key that carves brow/chin)*

**Scale & body (8)**

* Half-body standing ×3 (clean, different tops)
* Full-body standing ×3 (simple outfits; flat shoes)
* Seated half-body ×2 (different backgrounds)

**Expression & gaze (6)**

* Neutral, eyes aside ×2
* Small smile, eyes to camera ×2
* Thoughtful/serene, eyes down/up ×2

**Hair & minor styling (4)**

* Hair tucked behind one ear ×2
* Lightly pinned/back-combed (keeps length visible) ×2
  *(avoid drastic style changes unless they’re “canon” for the character.)*

---

### Caption cues

**(keep identity, drop wardrobe)**

Start with your trigger; sprinkle identity traits sparingly:

* `[celestegrl], natural-light close-up, hazel eyes, chest-length dark hair, soft freckles, rounded chin, smooth browbone, relaxed expression.`
* For clothing: “casual outfit” / “simple blouse” (no colors/brands).
* For lighting: “open shade” / “window light with bounce” / “softbox portrait.”
* For scale: “three-quarter view portrait” / “half-body standing” / “full body standing.”

---

### Training knobs

**(safe defaults for your 4060 Ti 16 GB)**

* Buckets max 1024; batch 4; bf16; grad checkpointing ON.
* LoRA rank 16 (alpha 16), dropout 0.08.
* LR: UNet 1e-4, TextEnc 5e-6.
* Repeats 10; 1–2 epochs; save every 400–600 steps; pick the **lowest** step that holds identity and stays flexible.

---

### Validation Prompt Sheet

Run the same set on each checkpoint:

1. `portrait of [celestegrl], soft daylight, neutral background`
2. `[celestegrl], three-quarter view portrait, studio softbox`
3. `[celestegrl], profile portrait, open shade`
4. `[celestegrl], half-body standing, casual outfit, window light`
5. `[celestegrl], full body standing, simple dress, neutral backdrop`
6. `[celestegrl], golden hour backlight`
7. `[celestegrl], hoodie, indoor ambient light`
8. `close-up of [celestegrl], rounded chin, smooth browbone, shallow depth of field`

**Pass criteria:** identity holds in #3 and #5; no outfit “cling” in #7; no carved brow/chin in #8. If you’d like, drop 10–15 filenames and I’ll draft captions tuned to this plan—and we’ll have your LoRA rock-solid without bloat.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">












## ReActor

Totally okay with ReActor, girlfriend—especially since you’re swapping **your own** face and aiming for a believable, adult younger-you. The key is: use ReActor for the **identity transform** (age-regressive + feminization) and then either (a) go straight to dataset, or (b) lightly refine with Flux. Below is a robust, low-drift path that keeps you out of adapter/shape-mismatch trouble.

---

### Plan at a glance

* **Stage 1 (ReActor, SDXL):** build a canonical “younger-you” anchor and then a 60–80 image dataset (angles, lighting, scale) with the **same swap settings** for consistency.
* **Stage 2 (ComfyUI inpaint passes, any model):** micro-fix chin/brow with feathered masks if needed.
* **Stage 3 (Flux, optional):** polish via **img2img** with low denoise or just use the ReActor dataset to train your Flux LoRA.

---

### Stage 1, ReActor setup

**(SDXL backbone)**

**Recommended base:** SDXL photoreal (or a neutral SDXL checkpoint you trust). ReActor works in **image space**, so the PNGs you export are model-agnostic and fine for Flux training or img2img later.

---

### Node skeleton

**(ComfyUI)**

* **Load Image (source)** → your best straight-on/soft-light selfie (adult).
* **Load Image (target template)** → a neutral portrait (or just use empty target if your ReActor build allows direct swap onto a generated canvas).
* **ReActor (Gourieff)**
  Inputs: source image, (optional) target image
  Outputs: swapped **IMAGE**
* (Option A) **Straight to Save** → dataset images
* (Option B) **To SDXL/Flux img2img** for style/lighting normalization

---

### ReActor settings

**to minimize artifacts**

* **Detector/align:** SCRFD (default), keep face alignment **ON**
* **Swap fidelity/weight:** **0.55–0.70** (start 0.62). Higher locks identity, but too high can “paste” look.
* **Blend / feather:** **0.15–0.25**; turn **seamless** or **Poisson** blend ON if available.
* **Expression adapt:** **OFF** for anchor; ON for expression pack later (keeps variety).
* **Face restore/upscale:** OFF during dataset creation (restorers imprint a look).
* **Color match / histogram match:** **LOW** (0.2–0.35); do not over-normalize—causes waxy skin.
* **Mask dilation:** small (2–4 px) to avoid a hard seam at hairline; we’ll feather in GIMP if needed.

---

### Age regression

**+ feminization (do it gently)**

* **Prompt (if generating a target frame with SDXL):**
  Positive: `photoreal portrait of an adult young woman in her twenties, average proportions, balanced features, rounded chin, smooth low brow ridge, soft clamshell lighting, shallow depth of field, neutral background`
  Negative: `no cleft chin, no chin dimple, no pronounced brow ridge, no heavy retouch, no harsh shadows`
* Run ReActor **onto** these neutral targets. Keep lighting soft and simple (prevents brow/chin carving).

---

### Build your 80-image set

**(4 packs × 20), same ReActor weights**

* **Angles:** front, 3/4 L/R, profile L/R; small up/down tilts.
* **Lighting:** open shade, window w/ bounce, softbox clamshell, overcast, golden-hour backlight.
* **Scale/body:** close-up, half-body, a few full-body (simple outfits).
* **Expressions/hair micro:** neutral, slight smile, soft laugh, eyes aside/down/up; hair tucked/pinned (minor only).

> Keep **hair color/length, eye color, skin tone** constant across the packs. That’s your canonical identity.

---

### Stage 2, Micro inpaints

**(optional but powerful)**

If ReActor leaves a hint of cleft or brow ridge (Flux/SDXL can “re-carve” features), run two tiny passes:

**Chin pass**

* Mask: lower lip → chin tip, **feather 8–15 px**
* Positive: `rounded chin, no cleft, soft natural shading, continuous skin texture, subtle mentolabial groove`
* Negative: `no chin dimple, no deep vertical crease, no sharp contour`
* **Denoise:** 0.40–0.50 (img2img)
* **CFG:** ~6.0

**Brow pass**

* Mask: brows → mid-forehead, **feather 8–15 px**
* Positive: `smooth browbone, low supraorbital ridge, fuller forehead curve, gentle shadowing`
* Negative: `no pronounced brow ridge, no deep glabellar crease, no harsh nose bridge shadow`
* **Denoise:** 0.35–0.45
* **CFG:** ~6.0

(You can do these with SDXL or Flux; they’re just masked img2img edits.)

---

### Stage 3, Flux polish

**(optional)**

If you want the final dataset to sit closer to Flux’s “look,” do a light **img2img** over each ReActor image:

* **Model:** Flux1-Dev
* **Denoise:** **0.25–0.40** (identity-preserving)
* **CFG:** 6.0–6.5
* **Prompt nudges:** keep the same soft anatomy lines and simple lighting labels.
* **Do not** use SDXL InstantID/IP-Adapter here—those mismatch Flux. If you want identity reference on Flux, use **Flux IP-Adapter** (but you don’t have to if you’re happy with the ReActor images as-is).

---

### Captioning for LoRA

**(short, identity-first)**

Create a sidecar `.txt` per image. Start with your trigger (e.g., `[girlfriendgrl]`) and keep it consistent:

* `[girlfriendgrl], natural-light close-up, hazel eyes, chest-length dark hair, soft freckles, rounded chin, smooth browbone, relaxed expression.`
* `[girlfriendgrl], three-quarter view portrait, window light with bounce, neutral background.`
* `[girlfriendgrl], half-body standing, casual outfit, soft studio light.`
* `[girlfriendgrl], profile portrait, open shade.`

Avoid brand/color specifics; never mention non-canonical features.

---

### Training knobs

**(Flux/FluxGym on 4060 Ti 16 GB)**

* **Buckets:** max 1024; aspect buckets ON.
* **Batch:** 4 (bf16), grad checkpointing ON.
* **LoRA:** rank 16 (alpha 16), dropout 0.08.
* **LRs:** UNet 1e-4; TextEnc 5e-6.
* **Repeats/Epochs:** ~10 repeats; 1–2 epochs.
* **Saves:** every 400–600 steps; pick the **lowest** step that holds identity and stays flexible.

---

### Why pick ReActor here?

* It’s actively maintained, and for **face-geometry edits** it’s still the cleanest “one-identity” tool when used with conservative blending.
* It avoids the **Flux vs SDXL** conditioning shape conflicts—because you’re swapping **images**, not trying to bolt SDXL adapters onto Flux.

---

### Common pitfalls

**& quick fixes**

* **Pastey seams:** lower blend/feather in ReActor; add a tiny **Gaussian blur** on your mask edge in GIMP; run a short inpaint with 0.40 denoise.
* **Identity drift across packs:** keep **the same ReActor fidelity/weights** and similar lighting; don’t let one pack be super stylized.
* **Over-youthful look:** keep “**adult young woman**” explicit in prompts; avoid extreme skin-smoothing or face-restorers.

If you want, I can give you a **concise ReActor preset** (just the sliders/values you see in its UI) and a one-page ComfyUI wiring for “ReActor → SDXL → Save” and “ReActor → SDXL → Inpaint (chin/brow) → Save” so you can replicate it exactly.

Totally—let’s nudge things, not overhaul them. Here are **subtle, anatomy-focused prompt fragments** you can drop into Qwen/Flux prompts to *slightly* feminise while keeping your face.

---

### Add (positive)

**pick 4–8 that fit**

* `softly rounded chin`
* `smooth low brow ridge`
* `slightly fuller lips`
* `gentle cheek fullness`
* `soft jawline taper`
* `slight canthal tilt, delicate lashes`
* `softer nasolabial fold`
* `subtle inner-eye highlight`
* `balanced midface, delicate nose tip`
* `natural soft makeup, sheer tint`
* `fine brow grooming, lighter brow density`
* `soft clamshell lighting`, `open shade lighting`
* `85mm portrait look`, `shallow depth of field`

> If you use weighting, keep it light: e.g. `(softly rounded chin:1.15)`, `(smooth low brow ridge:1.15)`.

---

### Block (negative)

**keep concise**

* `no pronounced brow ridge`
* `no heavy jaw`, `no square jaw`
* `no cleft chin`, `no chin dimple`
* `no five-o’clock shadow`, `no stubble`
* `no harsh top light`, `no hard rim light`
* (if neck visible) `no Adam’s apple emphasis`

---

### A clean starting prompt

**Positive**

```
photoreal portrait, adult young woman, softly rounded chin, smooth low brow ridge,
gentle cheek fullness, soft jawline taper, slightly fuller lips,
natural soft makeup (sheer tint), fine brow grooming, delicate lashes,
soft clamshell lighting, 85mm portrait look, shallow depth of field
```

**Negative**

```
no pronounced brow ridge, no heavy jaw, no cleft chin, no stubble,
no harsh top light, no heavy retouch, no over-sharpening
```

---

### Micro-tuning Set

If you only need *a touch* more, use just these three in positive:

```
softly rounded chin, smooth low brow ridge, natural soft makeup (sheer tint)
```

And negatives:

```
no pronounced brow ridge, no cleft chin, no stubble
```

---

### For 3/4 or full-body frames

Add one gentle global cue (don’t stack lots):

* `graceful posture` or `soft shoulder line`
* `subtle hair framing around cheeks`

---

### Small control tweaks

**(to keep identity)**

* Lower CFG a hair (e.g., 6.5 → **6.0**) so text cues guide shape softly.
* If using an image adapter/ID ref: keep strength **0.35–0.45**; raise to **~0.45** if identity drifts, *then* reduce denoise a notch.
* Keep **denoise** modest (**0.25–0.40** for img2img). Too high = geometry changes.

---

### Tiny inpaint prompts

**(if one area needs help)**

* **Brow band (mask brows→mid-forehead):**
  Positive: `smooth browbone, fuller forehead curve, gentle shadowing`
  Negative: `no pronounced brow ridge`
* **Chin pad (mask lower lip→chin tip):**
  Positive: `softly rounded chin, continuous skin texture`
  Negative: `no cleft chin, no deep vertical crease`
* **Lips (tight mask):**
  Positive: `slightly fuller lips, natural lip tint`
  Negative: `no overlining, no gloss glare`

---

### Style traps to avoid

**(they masculinise quickly)**

* Harsh top/side lighting, deep eye sockets, heavy contrast/clarity sliders, strong sharpen, thick dark brows by default.

If you paste one of your current Qwen prompts, I’ll trim it to a “micro-feminise” version with weights that fit your exact pipeline.

<hr style="height:8px;border-width:0;color:pink;background-color:pink">














## LoRA Notes

### Watercolor Style

Yet another watercolor style, trained using synthetic images generated with SDXL and SDXL Niji SE. The goal of the LoRA is flexibility, so that it can be used with other LoRAs without introducing too much of its own aesthetics.

Known problem with the two earlier versions: the face is always Caucasian. The problem has been fixed by mixing in images of Asians. All versions work well (no captioned version seems a bit more flexible though), and can produce nice images at 8 steps with https://civitai.com/models/686704/flux-dev-to-schnell-4-step-lora


*Training parameters*:

* 23 to 26 512x512 (downscaled from 1024x1024) images, captioned with Florence2 or by using "no captioning" training with just the trigger "yawc1 watercolor".
* FLUX.1 - dev-fp8
* Trigger: yawc1 watercolor
* Repeat: 20 Epoch: 8 or 9 epochs.
* Unet LR: 0.0005 Scheduler: cosine Optimizer: AdamW/AdamW8bit
* Network Dim: 4 Alpha 2 or Dim 6 Alpha 3

Details:

* Type: LoRA
* Reviews: Very Positive
* Published: Nov 24, 2024
* Base Model: Flux.1 D
* Trigger Words: yawc1 watercolor

Training:

* Steps: 4,500
* Epochs: 20


<hr style="height:8px;border-width:0;color:pink;background-color:pink">








## Z Image Turbo

[Q]  
Hi Emily. Been having a bit of looking around on Z Image Turbo. It appears to really respond well to complete sentences and as descriptive a language as one can come up with. This, at CFG of 1. Also, negative prompts do almost nothing at CFG=1, and the slowdown by increasing the CFG even to 1.3 is significant. So, I'd like to try something. Can we can couch this prompt in full sentences, being a bit more detailed in descriptions, and - for now - eliminate the negative prompt? Here's the prompt:

documentary photo, modern women-run atelier workroom, warm morning light
same late-blooming 18-year-old youth, slim narrow shoulders, boyish face with faint freckles, no makeup, no jewelry
very long brown hair in a low ponytail with loose tendril, hair down the back
women’s 1770s daywear ankle length two-piece outfit: indigo wool open-front ankle lengthvelvet, velour, suede, satin sheen, brocade, jacquard, floral print, patterned fabric, mottled texture, marble texture, quilted texture overdress worn over a separate matching indigo petticoat clearly visible (two separate garments),indigo wool is the dominant visible garment color, no beige or unbleached outer garment, solid indigo, matte, plain weave wool, visible woven texture, no pattern, no print, no mottling
white linen chemise visible only at neckline edge and sleeve cuffs
range-of-motion check: arms raised, chin down, eyes on underarm seam, focused neutral expression
white tennis shoes worn on feet visible under hem
worktable: sewing machine, red thread spool, indigo wool fabric, tape measure, pins, chalk, open ledger/policy binder

---

[A]  
Absolutely — and I can see why ZiT likes this. Here’s your exact content, but rewritten as *continuous, descriptive sentences* (no separate negative prompt). I’ve also cleaned the fabric contradictions so the model isn’t being told “matte plain wool” and “satin sheen / brocade / floral print” in the same breath.

Use this as your *positive prompt*:

---

**Prompt (full sentences, no negative):**



---

If you want a tiny “ZiT obedience nudge” without using a negative prompt, you can simply **repeat the key truths once** inside the same prompt (ZiT tends to respond well to reiteration in plain language), like this:

> “The indigo wool is solid and matte, with a plain weave and visible texture. The outfit is two separate garments: an overdress over a separate petticoat, both clearly visible.”

If you’d like, I can also do a *second* version that’s identical but slightly re-angles the camera so the **shoes + two-layer hem separation** are even more “unmissable” (low 3/4 angle, waist-up still readable, but hem and footwear guaranteed).

---

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



<hr style="height:8px;border-width:0;color:pink;background-color:pink">

<hr style="height:24px;border-width:0;color:pink;background-color:pink">


