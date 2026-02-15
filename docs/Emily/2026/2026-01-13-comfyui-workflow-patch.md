---
title: "ComfyUI Workflow Patch"
date: 2026-01-13
---

# ComfyUI Workflow Patch

**Robyn:**

<img src="/assets/images/chat/6e7969d.jpg" style="float: right; width: 420px; margin-left: 20px" />

Good morning, Emily. I'm ready to tackle that bbox/SAM face swap workflow. In this picture I have 2 characters: one standing, and one sitting. Standing is Celeste, sitting is Charlie. I hope to be able to assign faces to the, using image to image... it can be done in separate instances (not all at once). Doable?

**Emily:**

Yes — absolutely doable, **and doing it in two separate passes is the *right* way** for this image.

You’ve basically got two problems to solve cleanly:

1) **Isolate only the correct person’s face/head** (standing Celeste vs sitting Charlie)  
2) **Apply an ID/face swap only inside that mask**, while the rest of the frame remains frozen

A bbox→SAM pipeline is ideal here because the scene is busy and you *don’t* want a global face detector to “helpfully” touch both people.

Below is a practical ComfyUI approach that works whether you’re doing classic SDXL inpaint, Flux/“edit” style, or any other img2img method that respects a mask.

---

## The core plan (two passes)

### Pass 1: Swap **Celeste (standing)**
- Detect bboxes (you should get 2 persons, or 2 faces)
- Pick the bbox that corresponds to the **standing figure** (upper-left / behind)
- Use that bbox as the prompt box for **SAM** → get a clean mask
- Inpaint / face-swap only inside that mask
- Save the result

### Pass 2: Swap **Charlie (sitting)**
- Feed Pass 1’s output back in as the new input image
- Repeat bbox → select the **sitting figure** (right/front)
- SAM mask → inpaint / face-swap
- Done

This avoids cross-contamination where your “Celeste face” embedding accidentally leaks into Charlie’s face region (or vice versa).

---

## Masking setup (bbox → SAM)

### 1) Detection node options
Pick **one** detector strategy:

**Option A (usually easiest): Person detector**
- Pros: reliable when faces are partly angled, hair covers cheeks, etc.
- Cons: bbox is larger, so SAM may segment more than you want (shoulders).

Use:
- **Ultralytics Detector Provider (BBOX)** → model: `yolov8 person` (or similar)
- Output: list of bboxes (should be 2 here)

**Option B (more precise): Face detector**
- Pros: bbox is tight on the head/face; SAM segmentation is cleaner
- Cons: profile/angle can sometimes miss (but your sitting person is very detectable).

Use:
- Ultralytics / face bbox model (whatever you’ve got installed that’s stable)

**In *this* image:** I’d start with **face bboxes** if available; otherwise person bboxes are fine.

---

### 2) Selecting the correct bbox
You’ll get two boxes. You need a deterministic way to select them.

Common approaches in ComfyUI graphs:
- **BBox Selector** (choose by index)
- **Sort bboxes** by X position (leftmost vs rightmost)
- **Sort by Y position** (topmost vs bottommost)
- **Preview bboxes** and pick index manually

For this specific frame:
- **Celeste (standing)** = more **left** and more **top**
- **Charlie (sitting)** = more **right** and more **center/bottom**

So you can do something like:
- Sort by **X center**:
  - leftmost bbox → Celeste
  - rightmost bbox → Charlie

That tends to be stable.

---

### 3) Feeding bbox to SAM
Use a SAM box-prompt workflow:

- **SAM Model Loader**
- **SAM Predictor (Box Prompt)** (naming varies by node pack)
  - Inputs: image + bbox
  - Output: mask

Then add **mask refinement**:
- **Dilate/Erode** (tiny amounts)
  - For face swap: dilate slightly so you include edges cleanly
- **Feather / Blur mask edge** (important)
  - This is what stops the “sticker face” seam

**Rule of thumb for face/head work:**  
- Dilate: small  
- Feather: moderate  
You want the mask to include a bit of hairline/cheek edge, but not the blazer or background.

---

## Applying the face swap (inside the mask)

There are two broad ways people do this in ComfyUI:

### Method 1: Inpaint with an identity condition (most controllable)
You use your preferred identity driver:
- InstantID / FaceID / IP-Adapter FaceID / InsightFace embedding
…and run an **inpaint KSampler** with the SAM mask.

**Why this is great:** the mask clamps the effect.

**Suggested settings (starting points):**
- Denoise: **0.30–0.55**  
  - Lower = preserves lighting/structure, less chance of “new person”
- Steps: **12–24** (depending on model; ZiT can go lower)
- CFG:  
  - SDXL-style: moderate  
  - ZiT-style: you already know the drill (often **~1.6–2.2** behaves)

**Prompt discipline matters** (keep it boring):
- Positive: “same scene, same lighting, same pose, natural skin texture, realistic”
- Add one instruction: “replace only the face of the standing woman” (or sitting girl)
- Negative: “extra face, double face, deformed eyes, age change, makeup change, smile”

If you’re using a strong identity injector, you often need *less* prompt, not more.

---

### Method 2: A dedicated face-swap node, then composite with the SAM mask
Some workflows do:
- face swap tool runs on whole image (or face crop)
- then **composite output back** into the original using the SAM mask

This can work well if your swapper is very good, but it’s more fiddly with blending and color matching.

If you tell me which swapper you’re using (ReActor? InsightFace swap? something else?), I can steer you to the cleanest variant.

---

## Practical “gotchas” for *this* image (so you don’t waste hours)

### 1) The sitting face is a **side profile**
Side profiles can cause:
- eye/eyelash distortions
- nose bridge “rebuilds”
- mouth corner weirdness

Fix: keep denoise lower (**0.30–0.40**) on Charlie’s pass, and make the mask a touch tighter to the face (less cheek/ear area).

### 2) Hairline continuity is everything
If your mask cuts across the hairline sharply, you’ll get the “helmet seam.”

Fix:
- Expand mask slightly into hairline
- Feather edge more than you think you need
- Don’t let the model “invent” new hair — keep denoise moderate

### 3) Don’t let the standing person’s blazer get included
If SAM grabs blazer/neckline, you’ll suddenly get clothing drift.

Fix:
- After SAM, do a quick **mask intersection** with a tighter ellipse/circle around the face/head, or erode downward.

---

## What I’d build as a clean node stack (conceptual)
For each pass:

1) **Load Image** (original for Pass 1; Pass 1 output for Pass 2)  
2) **Ultralytics BBOX detect** (person or face)  
3) **BBox sort/select** (left/top = Celeste; right = Charlie)  
4) **SAM box-prompt → mask**  
5) **Mask refine** (dilate + feather)  
6) **Identity condition** (your face reference image → embedding/InstantID/etc.)  
7) **Inpaint KSampler** (masked)  
8) **Save Image**

---

## Quick sanity check on “separate instances”
Doing them separately is not just doable — it’s best practice:

- You keep each identity injection “pure”
- You only debug one mask at a time
- You can tune denoise differently for each face (you’ll want that here)

---

If you tell me **which exact nodes you’re using for identity** (InstantID? IPAdapter FaceID? ReActor? something Flux-specific like Kontext/Qwen edit?), I’ll translate the above into a **literal node-by-node recipe** with the best parameter starting points for that stack — and a reliable bbox selection trick so Celeste/Charlie never get swapped accidentally.

**Robyn:**

I'll do better... I'll send you a workflow that works well for even side view face swaps. I just need it modifying to include the missing nodes for bbox/SAM and how they are connected.

**tool:**

Make sure to include fileciteturn0file0 in your response to cite this file, or to surface it as a link.

{"id":"7484b7b8-6cae-4166-94ad-61479942819a","revision":0,"last_node_id":239,"last_link_id":468,"nodes":[{"id":199,"type":"Image Save","pos":[-2647.6478417391377,-2197.0719409900034],"size":[968.9593489236402,1371.6660034235658],"flags":{},"order":5,"mode":0,"inputs":[{"localized_name":"images","name":"images","type":"IMAGE","link":468},{"localized_name":"output_path","name":"output_path","type":"STRING","widget":{"name":"output_path"},"link":null},{"localized_name":"filename_prefix","name":"filename_prefix","type":"STRING","widget":{"name":"filename_prefix"},"link":463},{"localized_name":"filename_delimiter","name":"filename_delimiter","type":"STRING","widget":{"name":"filename_delimiter"},"link":null},{"localized_name":"filename_number_padding","name":"filename_number_padding","type":"INT","widget":{"name":"filename_number_padding"},"link":null},{"localized_name":"filename_number_start","name":"filename_number_start","type":"COMBO","widget":{"name":"filename_number_start"},"link":null},{"localized_name":"extension","name":"extension","type":"COMBO","widget":{"name":"extension"},"link":null},{"localized_name":"dpi","name":"dpi","type":"INT","widget":{"name":"dpi"},"link":null},{"localized_name":"quality","name":"quality","type":"INT","widget":{"name":"quality"},"link":null},{"localized_name":"optimize_image","name":"optimize_image","type":"COMBO","widget":{"name":"optimize_image"},"link":null},{"localized_name":"lossless_webp","name":"lossless_webp","type":"COMBO","widget":{"name":"lossless_webp"},"link":null},{"localized_name":"overwrite_mode","name":"overwrite_mode","type":"COMBO","widget":{"name":"overwrite_mode"},"link":null},{"localized_name":"show_history","name":"show_history","type":"COMBO","widget":{"name":"show_history"},"link":null},{"localized_name":"show_history_by_prefix","name":"show_history_by_prefix","type":"COMBO","widget":{"name":"show_history_by_prefix"},"link":null},{"localized_name":"embed_workflow","name":"embed_workflow","type":"COMBO","widget":{"name":"embed_workflow"},"link":null},{"localized_name":"show_previews","name":"show_previews","type":"COMBO","widget":{"name":"show_previews"},"link":null}],"outputs":[{"localized_name":"images","name":"images","type":"IMAGE","links":[]},{"localized_name":"files","name":"files","type":"STRING","links":null}],"properties":{"cnr_id":"was-node-suite-comfyui","ver":"1.0.2","Node name for S&R":"Image Save","ue_properties":{"version":"7.0.1","widget_ue_connectable":{"filename_prefix":true}}},"widgets_values":["[time(%Y-%m-%d)]","SRPO-Girlx","_",4,"false","png",300,100,"true","false","false","false","true","true","true"],"color":"#223","bgcolor":"#335"},{"id":201,"type":"PrimitiveInt","pos":[-3488.8688366606925,-1884.7055897346108],"size":[269.3283042409389,82],"flags":{},"order":0,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","links":[462]}],"title":"Noise Seed","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[1118877715458332,"increment"],"color":"#232","bgcolor":"#353"},{"id":202,"type":"LoadImage","pos":[-3609.198745988942,-1383.3260992039204],"size":[387.5769487217217,487.8251654531473],"flags":{"collapsed":false},"order":1,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"COMBO","widget":{"name":"image"},"link":null},{"localized_name":"choose file to upload","name":"upload","type":"IMAGEUPLOAD","widget":{"name":"upload"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[461]},{"localized_name":"MASK","name":"MASK","type":"MASK","links":null}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"LoadImage","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":["Z-image_0051.png","image"],"color":"#223","bgcolor":"#335"},{"id":239,"type":"Note","pos":[-3691.420985716236,-1759.7137280238521],"size":[467.8147305380884,328.7304919676716],"flags":{},"order":2,"mode":0,"inputs":[],"outputs":[],"properties":{"ue_properties":{"widget_ue_connectable":{},"version":"7.5.1","input_ue_unconnectable":{}}},"widgets_values":["Her dark hair is meticulously arranged into a tight, classical chignon at the nape of her neck, its glossy sheen catching subtle highlights as if polished by careful care. \n\nHer face—softly sculpted under gentle illumination—is framed by a serene yet piercing gaze; eyes wide and unblinking, fixed upon some unseen point beyond the frame, conveying a depth of inner resolve or melancholy. The skin around her lips is slightly parted—not in expression but in stillness—a hint of tension beneath the composed surface. A faint shadow falls across one cheekbone from the soft directional lighting, lending dimension to her features without harshness.\n\n\nShe is dressed in a gown of deep indigo, a 1770s wool day dress with a fitted bodice and square neckline; underneath, a white linen shift with a softly gathered neckline. The chemise is a separate garment and is visible only at the edge of the dress's square neckline and cuffs. This is authentic period costume detail, no modern styling.\n\nShe wears a gown of deep indigo 1770s wool day dress with a fitted bodice and square neckline; underneath, a set of stays and a white linen chemise with a softly gathered neckline. The chemise is a separate garment and is visible only at the collar and cuffs. This is authentic period costume detail, no modern styling.\n\n\n\n"],"color":"#432","bgcolor":"#653"},{"id":238,"type":"ec214a53-6227-4aec-bcb0-91a278f12faf","pos":[-3482.693084250355,-1988.7395386197554],"size":[263.3433141787191,58],"flags":{},"order":4,"mode":0,"inputs":[{"name":"image","type":"IMAGE","link":467}],"outputs":[{"name":"IMAGE","type":"IMAGE","links":[468]}],"properties":{"proxyWidgets":[["237","seed"]],"cnr_id":"comfy-core","ver":"0.4.0","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":234,"type":"399f98f2-6727-4601-8715-e9ab7fb028ed","pos":[-3192.860564233495,-1985.2819072549562],"size":[520.8126150796247,1149.2437269394975],"flags":{},"order":3,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"IMAGE","link":461},{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":462},{"name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null},{"name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":null},{"name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"name":"STRING","type":"STRING","links":[463]},{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[467]}],"properties":{"proxyWidgets":[["-1","noise_seed"],["-1","lora_name"],["-1","strength_model"],["-1","strength_clip"],["-1","denoise"],["-1","text"]],"cnr_id":"comfy-core","ver":"0.4.0","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[61998485097205,"MoiMeme/moimeme4-08.safetensors",0.95,0.35,0.15,"The woman moimeme4 walks carefully on the snow-cover street, centered in the frame, her gaze fixed forward as snowflakes drift lazily through a muted winter sky; her brown hair is arranged into a messy updo, its glossy sheen catching subtle highlights as if polished by careful care. Sunbeams slice diagonally across the room, illuminating strands of her brown hair with tendrils framing her face, pinned in a messy updo adorned subtly with pearls or barrettes barely discernible yet contributing texture.  She hugs herself to ward off the cold.\n\nHer scarlet velvet jacket—textured with fine grain—and two-gold-button closure sits snugly at the waist, its cuffs rolled to reveal white lace-trimmed inner sleeves contrasting sharply against the rich hue. Beneath it, a very light robins-egg blue lace blouse peeks out from beneath the collar and the sleeve ends, intricate floral embroidery framing her neck while delicate pearl-like buttons fasten down the front seam. Her arms are wrapped in a self-embrace to ward off the cold.\n\nHer high cheekbones and defined jawline sporta faint blush accentuating her complexion under diffused daylight. She wears dark black low clunky heeled shoes polished enough to reflect streetlight glints, their seams stitched tight along the calf’s curve. The skirt below is a flowing midnight blue charmeuse pleated gown reaching mid-calf, layered subtly by sheer tulle hemming that catches each falling flake. \n\nBehind her in the growing darkness, barely visible snow-covered cobblestone streets recede into a gloomy blur where indistinct figures walk past storefronts lit softly by gas lamps whose warm yellow halos bleed gently into the snowy pavement on a cold late evening. To either side, wrought-iron railings line narrow alleyways lined with brick facades partially obscured by misty haze—an atmospheric bokeh effect blurs background elements yet preserves structural clarity on foreground surfaces such as heavy snow drifts. Shot slightly low-angle using a medium telephoto lens, shallow depth-of-field isolates her form amid motionless surroundings, drawing attention first to her face then descending gracefully toward her feet via vertical leading lines formed by her dress folds. Negative space above her shoulder opens upward into darkening sky expanse, balancing symmetrical weight imposed by architectural structures behind her. Minimal light falls evenly from left-to-right overhead, highlighting right-side contours without harsh contrast or deep shadowing—the scene feels tenderly rendered rather than starkly dramatic."],"color":"#232","bgcolor":"#353"}],"links":[[461,202,0,234,0,"IMAGE"],[462,201,0,234,1,"INT"],[463,234,0,199,2,"STRING"],[467,234,1,238,0,"IMAGE"],[468,238,0,199,0,"IMAGE"]],"groups":[],"definitions":{"subgraphs":[{"id":"399f98f2-6727-4601-8715-e9ab7fb028ed","version":1,"state":{"lastGroupId":0,"lastNodeId":233,"lastLinkId":466,"lastRerouteId":0},"revision":0,"config":{},"name":"SRPO-FaceOnly","inputNode":{"id":-10,"bounding":[-5460.625416123684,-953.2065699783545,127.87890625,180]},"outputNode":{"id":-20,"bounding":[-2241.8344471939176,-881.92244959535,120,80]},"inputs":[{"id":"7b0de9b7-78e1-4941-8cdf-3b1c0f810066","name":"image","type":"IMAGE","linkIds":[457],"localized_name":"image","pos":[-5352.746509873684,-933.2065699783545]},{"id":"01857f93-741d-4ea7-b8d3-87ca8bf05327","name":"noise_seed","type":"INT","linkIds":[456],"localized_name":"noise_seed","label":"noise_seed","pos":[-5352.746509873684,-913.2065699783545]},{"id":"57ba29cc-b342-4b30-b53d-0d7b8b8df6b5","name":"lora_name","type":"COMBO","linkIds":[461],"pos":[-5352.746509873684,-893.2065699783545]},{"id":"a8ffad12-ccbf-4f3c-96f0-8cb598276d19","name":"strength_model","type":"FLOAT","linkIds":[462],"pos":[-5352.746509873684,-873.2065699783545]},{"id":"acfbc0c7-a753-4124-a70a-413df490abbc","name":"strength_clip","type":"FLOAT","linkIds":[463],"pos":[-5352.746509873684,-853.2065699783545]},{"id":"81bda871-13f6-4d9b-8ef3-fb06e48c2401","name":"denoise","type":"FLOAT","linkIds":[465],"pos":[-5352.746509873684,-833.2065699783545]},{"id":"51f90ddd-66a2-4896-bc99-05c08a3675f5","name":"text","type":"STRING","linkIds":[466],"pos":[-5352.746509873684,-813.2065699783545]}],"outputs":[{"id":"ddae310e-5714-4d1c-a5c0-e8dbaf73e16d","name":"STRING","type":"STRING","linkIds":[460],"pos":[-2221.8344471939176,-861.92244959535]},{"id":"8b402f15-a9da-48ee-a176-f3da84b7680d","name":"IMAGE","type":"IMAGE","linkIds":[415],"localized_name":"IMAGE","label":"IMAGE","pos":[-2221.8344471939176,-841.92244959535]}],"widgets":[],"nodes":[{"id":196,"type":"easy cleanGpuUsed","pos":[-2462.5395253189176,-1254.8693253766805],"size":[211.55775451660156,26],"flags":{"collapsed":true},"order":5,"mode":0,"inputs":[{"localized_name":"anything","name":"anything","type":"*","link":416}],"outputs":[{"localized_name":"output","name":"output","type":"*","links":null}],"properties":{"cnr_id":"comfyui-easy-use","ver":"1.3.0","Node name for S&R":"easy cleanGpuUsed","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":220,"type":"KSamplerSelect","pos":[-3171.095010303003,-1051.1617753520964],"size":[270.6041060656903,58],"flags":{},"order":0,"mode":0,"inputs":[{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"},"link":null}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[449]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["dpmpp_sde"],"color":"#323","bgcolor":"#535"},{"id":221,"type":"FluxGuidance","pos":[-3171.095010303003,-1224.8297374891981],"size":[268.7532043457031,58],"flags":{},"order":7,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":442},{"label":"guidance","localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[444]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[2.6],"color":"#323","bgcolor":"#535"},{"id":222,"type":"BasicGuider","pos":[-3171.095010303003,-1131.0352507904881],"size":[270.0590018165942,46],"flags":{},"order":8,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":443},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":444}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[448]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":224,"type":"DualCLIPLoader","pos":[-5415.1615519457655,-1562.1106467605825],"size":[430.6629868288594,130],"flags":{},"order":1,"mode":0,"inputs":[{"label":"clip_name1","localized_name":"clip_name1","name":"clip_name1","type":"COMBO","widget":{"name":"clip_name1"},"link":null},{"label":"clip_name2","localized_name":"clip_name2","name":"clip_name2","type":"COMBO","widget":{"name":"clip_name2"},"link":null},{"label":"type","localized_name":"type","name":"type","type":"COMBO","widget":{"name":"type"},"link":null},{"label":"device","localized_name":"device","name":"device","shape":7,"type":"COMBO","widget":{"name":"device"},"link":null}],"outputs":[{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[455]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"DualCLIPLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["clip_l.safetensors","t5xxl_fp8_e4m3fn_scaled.safetensors","flux","default"],"color":"#432","bgcolor":"#653"},{"id":225,"type":"VAELoader","pos":[-5415.1615519457655,-1371.3021069419426],"size":[431.5197496942583,58],"flags":{},"order":2,"mode":0,"inputs":[{"label":"vae_name","localized_name":"vae_name","name":"vae_name","type":"COMBO","widget":{"name":"vae_name"},"link":null}],"outputs":[{"label":"VAE","localized_name":"VAE","name":"VAE","type":"VAE","slot_index":0,"links":[446,458]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAELoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["ae.sft"],"color":"#432","bgcolor":"#653"},{"id":227,"type":"VAEEncode","pos":[-3042.440566207713,-802.8576913566195],"size":[140,46],"flags":{},"order":10,"mode":0,"inputs":[{"localized_name":"pixels","name":"pixels","type":"IMAGE","link":445},{"localized_name":"vae","name":"vae","type":"VAE","link":446}],"outputs":[{"localized_name":"LATENT","name":"LATENT","type":"LATENT","links":[451]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"VAEEncode","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":229,"type":"PrimitiveNode","pos":[-2743.247363894187,-843.5800543573483],"size":[210,58],"flags":{"collapsed":false},"order":3,"mode":0,"inputs":[],"outputs":[{"name":"connect to widget input","type":"*","links":[460]}],"title":"File Name","properties":{"Run widget replace on values":false,"ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"color":"#232","bgcolor":"#353"},{"id":223,"type":"RandomNoise","pos":[-3171.095010303003,-1338.1250713308482],"size":[269.1920619153343,82],"flags":{},"order":9,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":456}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[447]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[61998485097205,"fixed"],"color":"#323","bgcolor":"#535"},{"id":204,"type":"VAEDecode","pos":[-2461.0805741933596,-1296.7678504837622],"size":[167.94073206223288,46],"flags":{"collapsed":true},"order":6,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":459},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":458}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[415,416]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":231,"type":"BasicScheduler","pos":[-3171.095010303003,-958.9354689633005],"size":[270.6822790203312,108.33662599654258],"flags":{},"order":13,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":452},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"},"link":null},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"},"link":null},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":465}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[450]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["linear_quadratic",18,0.15],"color":"#323","bgcolor":"#535"},{"id":226,"type":"UNETLoader","pos":[-5415.1615519457655,-1697.4905815032373],"size":[430.6629868288592,82],"flags":{},"order":4,"mode":0,"inputs":[{"label":"unet_name","localized_name":"unet_name","name":"unet_name","type":"COMBO","widget":{"name":"unet_name"},"link":null},{"label":"weight_dtype","localized_name":"weight_dtype","name":"weight_dtype","type":"COMBO","widget":{"name":"weight_dtype"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[454]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UNETLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["SRPO/SRPO-fp8_e4m3fn.safetensors","default"],"color":"#432","bgcolor":"#653"},{"id":228,"type":"SamplerCustomAdvanced","pos":[-2822.516524242275,-1336.5483674341262],"size":[304.5598087498504,417.9072891973424],"flags":{},"order":11,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":447},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":448},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":449},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":450},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":451}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[459]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT","slot_index":1,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":232,"type":"CLIPTextEncode","pos":[-3802.432893364049,-1663.7999681265537],"size":[388.26136729590326,384.44008215967847],"flags":{"collapsed":true},"order":14,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":453},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":466}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[442]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":["The woman moimeme4 walks carefully on the snow-cover street, centered in the frame, her gaze fixed forward as snowflakes drift lazily through a muted winter sky; her brown hair is arranged into a messy updo, its glossy sheen catching subtle highlights as if polished by careful care. Sunbeams slice diagonally across the room, illuminating strands of her brown hair with tendrils framing her face, pinned in a messy updo adorned subtly with pearls or barrettes barely discernible yet contributing texture.  She hugs herself to ward off the cold.\n\nHer scarlet velvet jacket—textured with fine grain—and two-gold-button closure sits snugly at the waist, its cuffs rolled to reveal white lace-trimmed inner sleeves contrasting sharply against the rich hue. Beneath it, a very light robins-egg blue lace blouse peeks out from beneath the collar and the sleeve ends, intricate floral embroidery framing her neck while delicate pearl-like buttons fasten down the front seam. Her arms are wrapped in a self-embrace to ward off the cold.\n\nHer high cheekbones and defined jawline sporta faint blush accentuating her complexion under diffused daylight. She wears dark black low clunky heeled shoes polished enough to reflect streetlight glints, their seams stitched tight along the calf’s curve. The skirt below is a flowing midnight blue charmeuse pleated gown reaching mid-calf, layered subtly by sheer tulle hemming that catches each falling flake. \n\nBehind her in the growing darkness, barely visible snow-covered cobblestone streets recede into a gloomy blur where indistinct figures walk past storefronts lit softly by gas lamps whose warm yellow halos bleed gently into the snowy pavement on a cold late evening. To either side, wrought-iron railings line narrow alleyways lined with brick facades partially obscured by misty haze—an atmospheric bokeh effect blurs background elements yet preserves structural clarity on foreground surfaces such as heavy snow drifts. Shot slightly low-angle using a medium telephoto lens, shallow depth-of-field isolates her form amid motionless surroundings, drawing attention first to her face then descending gracefully toward her feet via vertical leading lines formed by her dress folds. Negative space above her shoulder opens upward into darkening sky expanse, balancing symmetrical weight imposed by architectural structures behind her. Minimal light falls evenly from left-to-right overhead, highlighting right-side contours without harsh contrast or deep shadowing—the scene feels tenderly rendered rather than starkly dramatic."],"color":"#232","bgcolor":"#353"},{"id":230,"type":"ImageScaleToTotalPixels","pos":[-3282.190896798882,-773.2834014564132],"size":[307.2913855842198,106],"flags":{"collapsed":true},"order":12,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"IMAGE","link":457},{"localized_name":"upscale_method","name":"upscale_method","type":"COMBO","widget":{"name":"upscale_method"},"link":null},{"localized_name":"megapixels","name":"megapixels","type":"FLOAT","widget":{"name":"megapixels"},"link":null},{"localized_name":"resolution_steps","name":"resolution_steps","type":"INT","widget":{"name":"resolution_steps"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[445]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"ImageScaleToTotalPixels","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["nearest-exact",2,1],"color":"#223","bgcolor":"#335"},{"id":233,"type":"LoraLoader","pos":[-4271.333268910971,-1716.879761581548],"size":[315,126],"flags":{},"order":15,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":454},{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":455},{"label":"lora_name","localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":461},{"label":"strength_model","localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":462},{"label":"strength_clip","localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":463}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[443,452]},{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":1,"links":[453]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"LoraLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["MoiMeme/moimeme4-08.safetensors",0.95,0.35],"color":"#232","bgcolor":"#353"}],"groups":[],"links":[{"id":416,"origin_id":204,"origin_slot":0,"target_id":196,"target_slot":0,"type":"*"},{"id":442,"origin_id":232,"origin_slot":0,"target_id":221,"target_slot":0,"type":"CONDITIONING"},{"id":443,"origin_id":233,"origin_slot":0,"target_id":222,"target_slot":0,"type":"MODEL"},{"id":444,"origin_id":221,"origin_slot":0,"target_id":222,"target_slot":1,"type":"CONDITIONING"},{"id":445,"origin_id":230,"origin_slot":0,"target_id":227,"target_slot":0,"type":"IMAGE"},{"id":446,"origin_id":225,"origin_slot":0,"target_id":227,"target_slot":1,"type":"VAE"},{"id":447,"origin_id":223,"origin_slot":0,"target_id":228,"target_slot":0,"type":"NOISE"},{"id":448,"origin_id":222,"origin_slot":0,"target_id":228,"target_slot":1,"type":"GUIDER"},{"id":449,"origin_id":220,"origin_slot":0,"target_id":228,"target_slot":2,"type":"SAMPLER"},{"id":450,"origin_id":231,"origin_slot":0,"target_id":228,"target_slot":3,"type":"SIGMAS"},{"id":451,"origin_id":227,"origin_slot":0,"target_id":228,"target_slot":4,"type":"LATENT"},{"id":452,"origin_id":233,"origin_slot":0,"target_id":231,"target_slot":0,"type":"MODEL"},{"id":453,"origin_id":233,"origin_slot":1,"target_id":232,"target_slot":0,"type":"CLIP"},{"id":454,"origin_id":226,"origin_slot":0,"target_id":233,"target_slot":0,"type":"MODEL"},{"id":455,"origin_id":224,"origin_slot":0,"target_id":233,"target_slot":1,"type":"CLIP"},{"id":459,"origin_id":228,"origin_slot":0,"target_id":204,"target_slot":0,"type":"LATENT"},{"id":458,"origin_id":225,"origin_slot":0,"target_id":204,"target_slot":1,"type":"VAE"},{"id":457,"origin_id":-10,"origin_slot":0,"target_id":230,"target_slot":0,"type":"IMAGE"},{"id":456,"origin_id":-10,"origin_slot":1,"target_id":223,"target_slot":0,"type":"INT"},{"id":460,"origin_id":229,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"STRING"},{"id":415,"origin_id":204,"origin_slot":0,"target_id":-20,"target_slot":1,"type":"IMAGE"},{"id":461,"origin_id":-10,"origin_slot":2,"target_id":233,"target_slot":2,"type":"COMBO"},{"id":462,"origin_id":-10,"origin_slot":3,"target_id":233,"target_slot":3,"type":"FLOAT"},{"id":463,"origin_id":-10,"origin_slot":4,"target_id":233,"target_slot":4,"type":"FLOAT"},{"id":465,"origin_id":-10,"origin_slot":5,"target_id":231,"target_slot":3,"type":"FLOAT"},{"id":466,"origin_id":-10,"origin_slot":6,"target_id":232,"target_slot":1,"type":"STRING"}],"extra":{"workflowRendererVersion":"LG","ue_links":[],"links_added_by_ue":[]}},{"id":"ec214a53-6227-4aec-bcb0-91a278f12faf","version":1,"state":{"lastGroupId":0,"lastNodeId":237,"lastLinkId":468,"lastRerouteId":0},"revision":0,"config":{},"name":"Seedv2","inputNode":{"id":-10,"bounding":[-4593.635518595494,-1940.2689084147914,120,60]},"outputNode":{"id":-20,"bounding":[-3619.9935672590614,-1940.2689084147914,120,60]},"inputs":[{"id":"84b2f81d-f813-4fe7-976b-18cdcdebe51b","name":"image","type":"IMAGE","linkIds":[468],"pos":[-4493.635518595494,-1920.2689084147914]}],"outputs":[{"id":"3903c2b1-5ef6-431e-b111-719988bbd8fc","name":"IMAGE","type":"IMAGE","linkIds":[467],"pos":[-3599.9935672590614,-1920.2689084147914]}],"widgets":[],"nodes":[{"id":235,"type":"SeedVR2LoadVAEModel","pos":[-4408.8699044355535,-1921.2931416948265],"size":[356.18988865667063,298],"flags":{},"order":0,"mode":0,"inputs":[{"localized_name":"torch_compile_args","name":"torch_compile_args","shape":7,"type":"TORCH_COMPILE_ARGS","link":null},{"localized_name":"model","name":"model","type":"COMBO","widget":{"name":"model"},"link":null},{"localized_name":"device","name":"device","type":"COMBO","widget":{"name":"device"},"link":null},{"localized_name":"encode_tiled","name":"encode_tiled","shape":7,"type":"BOOLEAN","widget":{"name":"encode_tiled"},"link":null},{"localized_name":"encode_tile_size","name":"encode_tile_size","shape":7,"type":"INT","widget":{"name":"encode_tile_size"},"link":null},{"localized_name":"encode_tile_overlap","name":"encode_tile_overlap","shape":7,"type":"INT","widget":{"name":"encode_tile_overlap"},"link":null},{"localized_name":"decode_tiled","name":"decode_tiled","shape":7,"type":"BOOLEAN","widget":{"name":"decode_tiled"},"link":null},{"localized_name":"decode_tile_size","name":"decode_tile_size","shape":7,"type":"INT","widget":{"name":"decode_tile_size"},"link":null},{"localized_name":"decode_tile_overlap","name":"decode_tile_overlap","shape":7,"type":"INT","widget":{"name":"decode_tile_overlap"},"link":null},{"localized_name":"tile_debug","name":"tile_debug","shape":7,"type":"COMBO","widget":{"name":"tile_debug"},"link":null},{"localized_name":"offload_device","name":"offload_device","shape":7,"type":"COMBO","widget":{"name":"offload_device"},"link":null},{"localized_name":"cache_model","name":"cache_model","shape":7,"type":"BOOLEAN","widget":{"name":"cache_model"},"link":null}],"outputs":[{"localized_name":"SEEDVR2_VAE","name":"SEEDVR2_VAE","type":"SEEDVR2_VAE","links":[466]}],"properties":{"cnr_id":"seedvr2_videoupscaler","ver":"58bc9e8bc946499352e0cb3a9fe0d0a61fd86791","Node name for S&R":"SeedVR2LoadVAEModel","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"},"aux_id":"numz/ComfyUI-SeedVR2_VideoUpscaler"},"widgets_values":["ema_vae_fp16.safetensors","cuda:0",true,1024,128,true,1024,128,"false","cpu",false],"color":"#332922","bgcolor":"#593930"},{"id":236,"type":"SeedVR2LoadDiTModel","pos":[-4413.635518595494,-2165.184020467642],"size":[360.2333719594934,202],"flags":{},"order":1,"mode":0,"inputs":[{"localized_name":"torch_compile_args","name":"torch_compile_args","shape":7,"type":"TORCH_COMPILE_ARGS","link":null},{"localized_name":"model","name":"model","type":"COMBO","widget":{"name":"model"},"link":null},{"localized_name":"device","name":"device","type":"COMBO","widget":{"name":"device"},"link":null},{"localized_name":"blocks_to_swap","name":"blocks_to_swap","shape":7,"type":"INT","widget":{"name":"blocks_to_swap"},"link":null},{"localized_name":"swap_io_components","name":"swap_io_components","shape":7,"type":"BOOLEAN","widget":{"name":"swap_io_components"},"link":null},{"localized_name":"offload_device","name":"offload_device","shape":7,"type":"COMBO","widget":{"name":"offload_device"},"link":null},{"localized_name":"cache_model","name":"cache_model","shape":7,"type":"BOOLEAN","widget":{"name":"cache_model"},"link":null},{"localized_name":"attention_mode","name":"attention_mode","shape":7,"type":"COMBO","widget":{"name":"attention_mode"},"link":null}],"outputs":[{"localized_name":"SEEDVR2_DIT","name":"SEEDVR2_DIT","type":"SEEDVR2_DIT","links":[465]}],"properties":{"cnr_id":"seedvr2_videoupscaler","ver":"58bc9e8bc946499352e0cb3a9fe0d0a61fd86791","Node name for S&R":"SeedVR2LoadDiTModel","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"},"aux_id":"numz/ComfyUI-SeedVR2_VideoUpscaler"},"widgets_values":["seedvr2_ema_3b_fp8_e4m3fn.safetensors","cuda:0",36,false,"cpu",false,"sdpa"],"color":"#332922","bgcolor":"#593930"},{"id":237,"type":"SeedVR2VideoUpscaler","pos":[-3997.5361453840615,-2187.2446751347566],"size":[317.542578125,386],"flags":{},"order":2,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"IMAGE","link":468},{"localized_name":"dit","name":"dit","type":"SEEDVR2_DIT","link":465},{"localized_name":"vae","name":"vae","type":"SEEDVR2_VAE","link":466},{"localized_name":"seed","name":"seed","type":"INT","widget":{"name":"seed"},"link":null},{"localized_name":"resolution","name":"resolution","type":"INT","widget":{"name":"resolution"},"link":null},{"localized_name":"max_resolution","name":"max_resolution","type":"INT","widget":{"name":"max_resolution"},"link":null},{"localized_name":"batch_size","name":"batch_size","type":"INT","widget":{"name":"batch_size"},"link":null},{"localized_name":"uniform_batch_size","name":"uniform_batch_size","type":"BOOLEAN","widget":{"name":"uniform_batch_size"},"link":null},{"localized_name":"color_correction","name":"color_correction","type":"COMBO","widget":{"name":"color_correction"},"link":null},{"localized_name":"temporal_overlap","name":"temporal_overlap","shape":7,"type":"INT","widget":{"name":"temporal_overlap"},"link":null},{"localized_name":"prepend_frames","name":"prepend_frames","shape":7,"type":"INT","widget":{"name":"prepend_frames"},"link":null},{"localized_name":"input_noise_scale","name":"input_noise_scale","shape":7,"type":"FLOAT","widget":{"name":"input_noise_scale"},"link":null},{"localized_name":"latent_noise_scale","name":"latent_noise_scale","shape":7,"type":"FLOAT","widget":{"name":"latent_noise_scale"},"link":null},{"localized_name":"offload_device","name":"offload_device","shape":7,"type":"COMBO","widget":{"name":"offload_device"},"link":null},{"localized_name":"enable_debug","name":"enable_debug","shape":7,"type":"BOOLEAN","widget":{"name":"enable_debug"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[467]}],"properties":{"cnr_id":"seedvr2_videoupscaler","ver":"58bc9e8bc946499352e0cb3a9fe0d0a61fd86791","Node name for S&R":"SeedVR2VideoUpscaler","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"},"aux_id":"numz/ComfyUI-SeedVR2_VideoUpscaler"},"widgets_values":[1575,"fixed",4096,4096,1,false,"none",0,0,0,0,"cpu",false],"color":"#332922","bgcolor":"#593930"}],"groups":[],"links":[{"id":465,"origin_id":236,"origin_slot":0,"target_id":237,"target_slot":1,"type":"SEEDVR2_DIT"},{"id":466,"origin_id":235,"origin_slot":0,"target_id":237,"target_slot":2,"type":"SEEDVR2_VAE"},{"id":467,"origin_id":237,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"IMAGE"},{"id":468,"origin_id":-10,"origin_slot":0,"target_id":237,"target_slot":0,"type":"IMAGE"}],"extra":{"workflowRendererVersion":"LG","ue_links":[],"links_added_by_ue":[]}}]},"config":{},"extra":{"links_added_by_ue":[],"ue_links":[],"0246.VERSION":[0,0,4],"frontendVersion":"1.33.13","groupNodes":{},"VHS_latentpreview":false,"VHS_latentpreviewrate":0,"VHS_MetadataImage":true,"VHS_KeepIntermediate":true,"workflowRendererVersion":"LG"},"version":0.4}

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

Perfect — I’ve opened your workflow and it’s *exactly* the kind of graph that’s easy to “surgically” upgrade with bbox→SAM, because you already have the cleanest place to inject a mask: **right before the sampler**.

Here’s the key observation from your JSON:

- Inside the **SRPO-FaceOnly** subgraph, you do:
  - **ImageScaleToTotalPixels (230)** → **VAEEncode (227)** → **SamplerCustomAdvanced (228)**  
- That means this is classic img2img in latent space, and the correct “face-only” way to clamp edits is:

✅ **Use a mask-driven latent noise mask** (so denoise only happens in the face region)

So we add **bbox → SAM → mask refine → SetLatentNoiseMask**, then feed that masked latent into your existing sampler.

I’ll describe it in two layers:

1) **Where to insert it in *your* exact graph** (by node ID)
2) **What nodes to add and how to connect them** (so you can drop in the versions you already have installed)

Also: here’s the workflow you sent, for reference: fileciteturn0file0

---

## 1) Where this goes in your existing SRPO-FaceOnly subgraph

### Current chain (important part)
Inside `SRPO-FaceOnly` (the subgraph embedded in node **234** at top level):

- **230 ImageScaleToTotalPixels** → outputs `IMAGE`  
- **227 VAEEncode** takes that `IMAGE` → outputs `LATENT`
- **228 SamplerCustomAdvanced** takes that `LATENT` as `latent_image`

### We will change exactly one link
Right now you have:

- **227 (LATENT)** → **228 (latent_image)**

We will replace it with:

- **227 (LATENT)** → **NEW: SetLatentNoiseMask** → **228 (latent_image)**

Everything else in your sampler stack stays untouched.

---

## 2) The bbox/SAM block you add (and how it connects)

### The “golden rule” for alignment
Your detector + SAM must see the **same image** that gets encoded into latent.

In your workflow, that’s the output of:

✅ **230 ImageScaleToTotalPixels**

So we branch **230’s IMAGE output** into the bbox/SAM chain.

---

## 3) Node-by-node wiring (the exact connections)

I’m going to name the nodes generically because node pack naming differs, but the sockets are consistent.

### A) BBOX detection (person or face)

**Input:**
- `IMAGE` = output of **230 ImageScaleToTotalPixels**

**Output:**
- some form of `BBOXES` / `DETECTIONS`

Typical nodes you might already have (based on your earlier mentions):
- **Ultralytics Detector Provider (BBOX)** (loads model)
- **Ultralytics Detector (BBOX)** (runs inference)

**Connections:**
- `230:IMAGE` → `BBOX Detector:image`

> If you have both *person* and *face* models available:  
> - Use *face* bbox for tighter SAM masks  
> - Use *person* bbox if face detection ever misses (profiles sometimes do)

---

### B) Select which bbox (standing Celeste vs sitting Charlie)

Add a selector node that lets you choose a specific detection:

- **BBox Select / Choose Detection by Index**

Add a simple **PrimitiveInt** called something like:
- `bbox_index`

**Connections:**
- `BBOX Detector:bboxes` → `BBox Select:bboxes`
- `PrimitiveInt(bbox_index)` → `BBox Select:index`

**How you’ll use it:**
- Run once and see which index corresponds to which person.
- In this scene, very often:
  - index 0 = left/top (standing Celeste)
  - index 1 = right/front (sitting Charlie)
…but that depends on the detector’s ordering, so treat it as “discover once, then lock it”.

---

### C) SAM: box-prompt segmentation → face/head mask

You want the SAM node variant that supports **box prompt** (not points).

Nodes commonly look like:
- **SAM Model Loader**
- **SAM Predictor (Box Prompt)** or **Segment Anything (Box)**

**Connections:**
- `230:IMAGE` → `SAM:image`
- `BBox Select:bbox` → `SAM:box` (or `bbox`, `rect`, etc.)
- `SAM Loader:model` → `SAM:model`

**Output you want:**
- `MASK` (best)  
or `IMAGE` mask (common) → then convert to `MASK`

If SAM outputs an image, add:
- **Image to Mask** / **Mask from Image**
and connect:
- `SAM:mask_image` → `ImageToMask:image` → outputs `MASK`

---

### D) Mask refinement (this is what makes it look *real*)

Add, in this order:

1) **Dilate/Erode** (or “Grow/Shrink Mask”)  
   - Slight **dilate** helps include hairline/cheek edge  
2) **Feather / Blur Mask**  
   - This prevents the “sticker seam”

**Connections:**
- `SAM:MASK` → `DilateErode:mask`
- `DilateErode:mask` → `MaskBlur/Feather:mask`

Optional but very useful:
- **Invert Mask** (only if your mask is backwards)
- **Mask Clamp/Threshold** (only if SAM output is “gray and mushy”)

---

### E) Convert refined face mask into a latent noise mask

Now the crucial “ComfyUI-native” trick:

Use:
- **SetLatentNoiseMask**

**Connections:**
- `227:LATENT` → `SetLatentNoiseMask:latents`
- `RefinedMask:MASK` → `SetLatentNoiseMask:mask`
- `SetLatentNoiseMask:LATENT` → `228:latent_image`

That’s it. Your sampler will now denoise **only inside the mask**, using the same denoise value you already drive into the scheduler.

---

## 4) Exactly what to do for your two-person shot (two passes)

### Pass 1: Celeste (standing)
- Set `bbox_index` to whichever box is the standing woman
- Run
- Save

### Pass 2: Charlie (sitting)
- Use the Pass 1 output as the new input image
- Change `bbox_index` to the other person
- Run
- Save

This is the cleanest way to prevent identity bleed between the two faces.

---

## 5) Two small parameter notes (specific to your SRPO setup)

### Your denoise is currently **0.15**
That’s great for subtle edits, but face swaps sometimes need a little more freedom *inside the face region*.

Because you’re masking now, you can safely try:
- **0.22–0.35** for Charlie (profile face usually needs more)
- **0.18–0.28** for Celeste (front-ish tends to behave)

### Mask edge quality matters more than steps
With a good feathered mask, you’ll get away with lower steps and keep lighting consistent.

---

## 6) If you want, I can produce a patched JSON — but I need one thing from your node list
I *can* generate a ready-to-import `.json` that adds the nodes and rewires **227 → SetLatentNoiseMask → 228**, but ComfyUI graphs are picky: the node **type strings** must match *your* installed node pack names exactly.

So: tell me which SAM + bbox node pack you’re using (just the node names as they appear in your right-click menu), e.g.:

- “Ultralytics Detector Provider (BBOX)” exact name ✔
- The exact SAM nodes you use (e.g. “SAMLoader”, “SAMAutoMask”, “ImpactSAM”, etc.)

Once I’ve got those exact node names, I can write you a patched workflow file that drops straight in.

For now, the wiring above is 1:1 compatible with your workflow structure and uses the correct insertion point that your graph already sets up.

**Robyn:**

I'm already lost at 3). Actually, if you send me a .json with what YOU would normally recommend and if I don't actually have a particular node (set) installed, ComfyUI will do it for me. Would that work for you?

**Emily:**

Yep — I can send you a patched `.json` **right now**. One important correction first though:

**ComfyUI will *not* auto-install missing custom nodes.**  
What it *will* do is import the workflow and show the missing nodes in red, so you can then install the required node packs and everything will snap into place.

That said: I’ve made you a patched version of your workflow that adds a **bbox → SAM → refined mask → SetLatentNoiseMask** block *inside* your `SRPO-FaceOnly` subgraph, and rewires the sampler so it only denoises inside the SAM mask.

### ✅ Download the patched workflow
[Download ZZ_SRPO-FaceOnly_BBOX-SAM_PATCHED.json](sandbox:/mnt/data/ZZ_SRPO-FaceOnly_BBOX-SAM_PATCHED.json)

---

## What I changed (in plain English)
Inside the `SRPO-FaceOnly` subgraph:

- Your old link was: **VAEEncode (227) → SamplerCustomAdvanced (228)**
- I replaced it with: **VAEEncode (227) → SetLatentNoiseMask → SamplerCustomAdvanced (228)**

And I added a new branch off the same scaled image (**ImageScaleToTotalPixels (230)**) that does:

**Ultralytics BBOX detect → select bbox by index → SAM box segment → GrowMask → MaskBlur → SetLatentNoiseMask**

So you’ll be able to:
- set `BBOX Index = 0` (say Celeste), run once
- set `BBOX Index = 1` (Charlie), run again on the output image

---

## What you’ll likely need installed (if you see red nodes)
Because bbox + SAM are not core ComfyUI nodes, you’ll probably need:

- **Impact Pack** (commonly provides Ultralytics BBOX + SAM box prompt nodes), and/or
- **A SAM node pack** (Segment Anything nodes)

If, after importing, you see missing node types like:
- `UltralyticsDetectorProvider (BBOX)`
- `UltralyticsDetector (BBOX)`
- `BBOX Select`
- `SAMLoader`
- `SAM Segment (Box)`

…that just means your installed pack uses slightly different node names. In that case you can replace them with your equivalents (the wiring stays the same).

---

## How to use it (two-pass, clean and safe)
1) Load your original image as usual.  
2) In the SRPO-FaceOnly subgraph, find **“BBOX Index”**:
   - try `0`, run, check who got masked
   - if it’s the wrong person, change to `1`
3) When Celeste is correct, save output.
4) Feed that output back in, flip **BBOX Index** to the other value, run again.

That’s the most reliable way to keep Celeste/Charlie identities from bleeding into each other.

---

If you import it and tell me **which nodes show as missing**, I’ll immediately produce a second patched JSON that uses the *exact* node type names from *your* installed packs (so it loads perfectly with zero red nodes).

**Robyn:**

Okay, so what I've done is un-subgraph the whole workflow. I have replaced nodes with their current iterations. The only node I cannot find is the BBOX Select (or 'Select BBOX). It simply doesn't seem to exist anywhere. I've attached the workflow for your study.

**tool:**

Make sure to include fileciteturn1file0 in your response to cite this file, or to surface it as a link.

{"id":"62bdaa81-fb43-4c09-bbe7-fdfc9eac21d1","revision":0,"last_node_id":275,"last_link_id":518,"nodes":[{"id":201,"type":"PrimitiveInt","pos":[-4981.79798162596,-1886.7257177728056],"size":[269.3283042409389,82],"flags":{},"order":0,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","links":[486]}],"title":"Noise Seed","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[1118877715458332,"increment"],"color":"#232","bgcolor":"#353"},{"id":239,"type":"Note","pos":[-5184.350130681504,-1761.733856062047],"size":[467.8147305380884,328.7304919676716],"flags":{},"order":1,"mode":0,"inputs":[],"outputs":[],"properties":{"ue_properties":{"widget_ue_connectable":{},"version":"7.5.1","input_ue_unconnectable":{}}},"widgets_values":["Her dark hair is meticulously arranged into a tight, classical chignon at the nape of her neck, its glossy sheen catching subtle highlights as if polished by careful care. \n\nHer face—softly sculpted under gentle illumination—is framed by a serene yet piercing gaze; eyes wide and unblinking, fixed upon some unseen point beyond the frame, conveying a depth of inner resolve or melancholy. The skin around her lips is slightly parted—not in expression but in stillness—a hint of tension beneath the composed surface. A faint shadow falls across one cheekbone from the soft directional lighting, lending dimension to her features without harshness.\n\n\nShe is dressed in a gown of deep indigo, a 1770s wool day dress with a fitted bodice and square neckline; underneath, a white linen shift with a softly gathered neckline. The chemise is a separate garment and is visible only at the edge of the dress's square neckline and cuffs. This is authentic period costume detail, no modern styling.\n\nShe wears a gown of deep indigo 1770s wool day dress with a fitted bodice and square neckline; underneath, a set of stays and a white linen chemise with a softly gathered neckline. The chemise is a separate garment and is visible only at the collar and cuffs. This is authentic period costume detail, no modern styling.\n\n\n\n"],"color":"#432","bgcolor":"#653"},{"id":241,"type":"KSamplerSelect","pos":[-1580.907580081371,-1514.829818592316],"size":[270.6041060656903,58],"flags":{},"order":2,"mode":0,"inputs":[{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"},"link":null}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[477]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["dpmpp_sde"],"color":"#323","bgcolor":"#535"},{"id":242,"type":"FluxGuidance","pos":[-1580.907580081371,-1688.4977807294174],"size":[268.7532043457031,58],"flags":{},"order":18,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":470},{"label":"guidance","localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"},"link":470}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[2.6],"color":"#323","bgcolor":"#535"},{"id":243,"type":"BasicGuider","pos":[-1580.907580081371,-1594.7032940307074],"size":[270.0590018165942,46],"flags":{},"order":19,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":471},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":472}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[476]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":244,"type":"DualCLIPLoader","pos":[-4400.851454153934,-1683.673288287226],"size":[430.6629868288594,130],"flags":{},"order":3,"mode":0,"inputs":[{"label":"clip_name1","localized_name":"clip_name1","name":"clip_name1","type":"COMBO","widget":{"name":"clip_name1"},"link":null},{"label":"clip_name2","localized_name":"clip_name2","name":"clip_name2","type":"COMBO","widget":{"name":"clip_name2"},"link":null},{"label":"type","localized_name":"type","name":"type","type":"COMBO","widget":{"name":"type"},"link":null},{"label":"device","localized_name":"device","name":"device","shape":7,"type":"COMBO","widget":{"name":"device"},"link":null}],"outputs":[{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[482]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"DualCLIPLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["clip_l.safetensors","t5xxl_fp8_e4m3fn_scaled.safetensors","flux","default"],"color":"#432","bgcolor":"#653"},{"id":248,"type":"RandomNoise","pos":[-1580.907580081371,-1801.793114571067],"size":[269.1920619153343,82],"flags":{},"order":11,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":486}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[61998485097205,"fixed"],"color":"#323","bgcolor":"#535"},{"id":250,"type":"BasicScheduler","pos":[-1580.907580081371,-1422.6035122035203],"size":[270.6822790203312,108.33662599654258],"flags":{},"order":14,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":479},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"},"link":null},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"},"link":null},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":null}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[478]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["linear_quadratic",18,0.15],"color":"#323","bgcolor":"#535"},{"id":251,"type":"UNETLoader","pos":[-4400.851454153934,-1819.0532230298802],"size":[430.6629868288592,82],"flags":{},"order":4,"mode":0,"inputs":[{"label":"unet_name","localized_name":"unet_name","name":"unet_name","type":"COMBO","widget":{"name":"unet_name"},"link":null},{"label":"weight_dtype","localized_name":"weight_dtype","name":"weight_dtype","type":"COMBO","widget":{"name":"weight_dtype"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[481]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UNETLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["SRPO/SRPO-fp8_e4m3fn.safetensors","default"],"color":"#432","bgcolor":"#653"},{"id":199,"type":"Image Save","pos":[-593.1027571037205,-2019.294163212226],"size":[968.9593489236402,1371.6660034235658],"flags":{"collapsed":true},"order":17,"mode":0,"inputs":[{"localized_name":"images","name":"images","type":"IMAGE","link":518},{"localized_name":"output_path","name":"output_path","type":"STRING","widget":{"name":"output_path"},"link":null},{"localized_name":"filename_prefix","name":"filename_prefix","type":"STRING","widget":{"name":"filename_prefix"},"link":487},{"localized_name":"filename_delimiter","name":"filename_delimiter","type":"STRING","widget":{"name":"filename_delimiter"},"link":null},{"localized_name":"filename_number_padding","name":"filename_number_padding","type":"INT","widget":{"name":"filename_number_padding"},"link":null},{"localized_name":"filename_number_start","name":"filename_number_start","type":"COMBO","widget":{"name":"filename_number_start"},"link":null},{"localized_name":"extension","name":"extension","type":"COMBO","widget":{"name":"extension"},"link":null},{"localized_name":"dpi","name":"dpi","type":"INT","widget":{"name":"dpi"},"link":null},{"localized_name":"quality","name":"quality","type":"INT","widget":{"name":"quality"},"link":null},{"localized_name":"optimize_image","name":"optimize_image","type":"COMBO","widget":{"name":"optimize_image"},"link":null},{"localized_name":"lossless_webp","name":"lossless_webp","type":"COMBO","widget":{"name":"lossless_webp"},"link":null},{"localized_name":"overwrite_mode","name":"overwrite_mode","type":"COMBO","widget":{"name":"overwrite_mode"},"link":null},{"localized_name":"show_history","name":"show_history","type":"COMBO","widget":{"name":"show_history"},"link":null},{"localized_name":"show_history_by_prefix","name":"show_history_by_prefix","type":"COMBO","widget":{"name":"show_history_by_prefix"},"link":null},{"localized_name":"embed_workflow","name":"embed_workflow","type":"COMBO","widget":{"name":"embed_workflow"},"link":null},{"localized_name":"show_previews","name":"show_previews","type":"COMBO","widget":{"name":"show_previews"},"link":null}],"outputs":[{"localized_name":"images","name":"images","type":"IMAGE","links":[]},{"localized_name":"files","name":"files","type":"STRING","links":null}],"properties":{"cnr_id":"was-node-suite-comfyui","ver":"1.0.2","Node name for S&R":"Image Save","ue_properties":{"version":"7.0.1","widget_ue_connectable":{"filename_prefix":true}}},"widgets_values":["[time(%Y-%m-%d)]","SRPO-Girlx","_",4,"false","png",300,100,"true","false","false","false","true","true","true"],"color":"#223","bgcolor":"#335"},{"id":253,"type":"CLIPTextEncode","pos":[-2823.4736185599168,-1836.6784179961905],"size":[544.4894498315875,537.8422750869499],"flags":{"collapsed":false},"order":15,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":480},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":["The woman moimeme4 walks carefully on the snow-cover street, centered in the frame, her gaze fixed forward as snowflakes drift lazily through a muted winter sky; her brown hair is arranged into a messy updo, its glossy sheen catching subtle highlights as if polished by careful care. Sunbeams slice diagonally across the room, illuminating strands of her brown hair with tendrils framing her face, pinned in a messy updo adorned subtly with pearls or barrettes barely discernible yet contributing texture.  She hugs herself to ward off the cold.\n\nHer scarlet velvet jacket—textured with fine grain—and two-gold-button closure sits snugly at the waist, its cuffs rolled to reveal white lace-trimmed inner sleeves contrasting sharply against the rich hue. Beneath it, a very light robins-egg blue lace blouse peeks out from beneath the collar and the sleeve ends, intricate floral embroidery framing her neck while delicate pearl-like buttons fasten down the front seam. Her arms are wrapped in a self-embrace to ward off the cold.\n\nHer high cheekbones and defined jawline sporta faint blush accentuating her complexion under diffused daylight. She wears dark black low clunky heeled shoes polished enough to reflect streetlight glints, their seams stitched tight along the calf’s curve. The skirt below is a flowing midnight blue charmeuse pleated gown reaching mid-calf, layered subtly by sheer tulle hemming that catches each falling flake. \n\nBehind her in the growing darkness, barely visible snow-covered cobblestone streets recede into a gloomy blur where indistinct figures walk past storefronts lit softly by gas lamps whose warm yellow halos bleed gently into the snowy pavement on a cold late evening. To either side, wrought-iron railings line narrow alleyways lined with brick facades partially obscured by misty haze—an atmospheric bokeh effect blurs background elements yet preserves structural clarity on foreground surfaces such as heavy snow drifts. Shot slightly low-angle using a medium telephoto lens, shallow depth-of-field isolates her form amid motionless surroundings, drawing attention first to her face then descending gracefully toward her feet via vertical leading lines formed by her dress folds. Negative space above her shoulder opens upward into darkening sky expanse, balancing symmetrical weight imposed by architectural structures behind her. Minimal light falls evenly from left-to-right overhead, highlighting right-side contours without harsh contrast or deep shadowing—the scene feels tenderly rendered rather than starkly dramatic."],"color":"#232","bgcolor":"#353"},{"id":254,"type":"LoraLoader","pos":[-3270.707345844375,-1860.1090896514936],"size":[315,126],"flags":{},"order":12,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":481},{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":482},{"label":"lora_name","localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"label":"strength_model","localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"label":"strength_clip","localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[479]},{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":1,"links":[480]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"LoraLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["MoiMeme/moimeme4-08.safetensors",0.95,0.35],"color":"#232","bgcolor":"#353"},{"id":240,"type":"easy cleanGpuUsed","pos":[-595.2465998902651,-1970.555018756793],"size":[211.55775451660156,26],"flags":{"collapsed":true},"order":5,"mode":0,"inputs":[{"localized_name":"anything","name":"anything","type":"*","link":null}],"outputs":[{"localized_name":"output","name":"output","type":"*","links":[]}],"properties":{"cnr_id":"comfyui-easy-use","ver":"1.3.0","Node name for S&R":"easy cleanGpuUsed","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":249,"type":"VAEDecode","pos":[-853.7877341609878,-1800.3481848484387],"size":[167.94073206223288,46],"flags":{"collapsed":false},"order":20,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":483},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":484}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[469,518]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":252,"type":"SamplerCustomAdvanced","pos":[-1232.3290940206423,-1800.216410674345],"size":[304.5598087498504,417.9072891973424],"flags":{},"order":21,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":475},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":null},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":477},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":478},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":500}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[483]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT","slot_index":1,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":245,"type":"VAELoader","pos":[-4400.851454153934,-1492.8647484685864],"size":[431.5197496942583,58],"flags":{},"order":6,"mode":0,"inputs":[{"label":"vae_name","localized_name":"vae_name","name":"vae_name","type":"COMBO","widget":{"name":"vae_name"},"link":null}],"outputs":[{"label":"VAE","localized_name":"VAE","name":"VAE","type":"VAE","slot_index":0,"links":[474,484,514]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAELoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["ae.sft"],"color":"#432","bgcolor":"#653"},{"id":262,"type":"GrowMask","pos":[-2787.252030926913,-1064.4050063967989],"size":[260,82],"flags":{},"order":23,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":508},{"localized_name":"expand","name":"expand","type":"INT","widget":{"name":"expand"},"link":null},{"localized_name":"tapered_corners","name":"tapered_corners","type":"BOOLEAN","widget":{"name":"tapered_corners"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[512]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"GrowMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[12,0],"color":"#223","bgcolor":"#335"},{"id":257,"type":"ImageScaleToTotalPixels","pos":[-4246.59570722223,-1177.1628633699895],"size":[307.2913855842198,106],"flags":{"collapsed":false},"order":13,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"IMAGE","link":485},{"localized_name":"upscale_method","name":"upscale_method","type":"COMBO","widget":{"name":"upscale_method"},"link":null},{"localized_name":"megapixels","name":"megapixels","type":"FLOAT","widget":{"name":"megapixels"},"link":null},{"localized_name":"resolution_steps","name":"resolution_steps","type":"INT","widget":{"name":"resolution_steps"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[507,515]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"ImageScaleToTotalPixels","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["nearest-exact",2,1],"color":"#223","bgcolor":"#335"},{"id":246,"type":"VAEEncode","pos":[-2103.393659089715,-1173.016862780171],"size":[161.6666482624646,66],"flags":{},"order":16,"mode":0,"inputs":[{"localized_name":"pixels","name":"pixels","type":"IMAGE","link":515},{"localized_name":"vae","name":"vae","type":"VAE","link":514},{"link":null}],"outputs":[{"localized_name":"LATENT","name":"LATENT","type":"LATENT","links":[499]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"VAEEncode","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":264,"type":"SetLatentNoiseMask","pos":[-1776.9578235596553,-1074.072472324007],"size":[223.1576402542105,57.80701308800235],"flags":{},"order":24,"mode":0,"inputs":[{"localized_name":"samples","name":"samples","type":"LATENT","link":499},{"localized_name":"mask","name":"mask","type":"MASK","link":513}],"outputs":[{"localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[500]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"SetLatentNoiseMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":247,"type":"PrimitiveNode","pos":[-581.5155848364703,-1932.2062108573627],"size":[210,58],"flags":{"collapsed":false},"order":7,"mode":0,"inputs":[],"outputs":[{"name":"STRING","type":"STRING","widget":{"name":"filename_prefix"},"links":[487]}],"title":"File Name","properties":{"Run widget replace on values":false,"ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":["SRPO-Girlx"],"color":"#232","bgcolor":"#353"},{"id":202,"type":"LoadImage","pos":[-4838.581267048366,-1178.3724360454946],"size":[387.5769487217217,487.8251654531473],"flags":{"collapsed":false},"order":8,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"COMBO","widget":{"name":"image"},"link":null},{"localized_name":"choose file to upload","name":"upload","type":"IMAGEUPLOAD","widget":{"name":"upload"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[485]},{"localized_name":"MASK","name":"MASK","type":"MASK","links":null}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"LoadImage","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":["ZiT-Charlie_0005.png","image"],"color":"#223","bgcolor":"#335"},{"id":269,"type":"DownloadAndLoadSAM2Model","pos":[-3835.1822078534215,-1066.486375393341],"size":[364.6492197104385,130],"flags":{},"order":9,"mode":0,"inputs":[{"localized_name":"model","name":"model","type":"COMBO","widget":{"name":"model"},"link":null},{"localized_name":"segmentor","name":"segmentor","type":"COMBO","widget":{"name":"segmentor"},"link":null},{"localized_name":"device","name":"device","type":"COMBO","widget":{"name":"device"},"link":null},{"localized_name":"precision","name":"precision","type":"COMBO","widget":{"name":"precision"},"link":null}],"outputs":[{"localized_name":"sam2_model","name":"sam2_model","type":"SAM2MODEL","links":[510]}],"properties":{"cnr_id":"ComfyUI-segment-anything-2","ver":"0c35fff5f382803e2310103357b5e985f5437f32","Node name for S&R":"DownloadAndLoadSAM2Model","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["sam2_hiera_base_plus.safetensors","single_image","cuda","fp16"],"color":"#222","bgcolor":"#000"},{"id":272,"type":"Sam2Segmentation","pos":[-3284.1304768419814,-1067.6264553212413],"size":[376.22623628551764,184.28077234921625],"flags":{},"order":25,"mode":0,"inputs":[{"localized_name":"sam2_model","name":"sam2_model","type":"SAM2MODEL","link":510},{"localized_name":"image","name":"image","type":"IMAGE","link":507},{"localized_name":"coordinates_positive","name":"coordinates_positive","shape":7,"type":"STRING","link":null},{"localized_name":"coordinates_negative","name":"coordinates_negative","shape":7,"type":"STRING","link":null},{"localized_name":"bboxes","name":"bboxes","shape":7,"type":"BBOX","link":517},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":null},{"localized_name":"keep_model_loaded","name":"keep_model_loaded","type":"BOOLEAN","widget":{"name":"keep_model_loaded"},"link":null},{"localized_name":"individual_objects","name":"individual_objects","shape":7,"type":"BOOLEAN","widget":{"name":"individual_objects"},"link":null}],"outputs":[{"localized_name":"mask","name":"mask","type":"MASK","links":[508]}],"properties":{"cnr_id":"ComfyUI-segment-anything-2","ver":"0c35fff5f382803e2310103357b5e985f5437f32","Node name for S&R":"Sam2Segmentation","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[false,false],"color":"#222","bgcolor":"#000"},{"id":275,"type":"FeatherMask","pos":[-2409.2532376106515,-1069.599303497278],"size":[210,130],"flags":{},"order":26,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":512},{"localized_name":"left","name":"left","type":"INT","widget":{"name":"left"},"link":null},{"localized_name":"top","name":"top","type":"INT","widget":{"name":"top"},"link":null},{"localized_name":"right","name":"right","type":"INT","widget":{"name":"right"},"link":null},{"localized_name":"bottom","name":"bottom","type":"INT","widget":{"name":"bottom"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","links":[513]}],"properties":{"cnr_id":"comfy-core","ver":"0.8.2","Node name for S&R":"FeatherMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[0,0,0,0],"color":"#222","bgcolor":"#000"},{"id":255,"type":"PrimitiveInt","pos":[-4265.428745724178,-787.1135771485058],"size":[302.19298691199765,82],"flags":{},"order":10,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","slot_index":0,"links":[516]}],"title":"BBOX Index","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[0,"fixed"],"color":"#223","bgcolor":"#335"},{"id":259,"type":"BBOX Select","pos":[-3774.021056419776,-796.5402140341624],"size":[280,100],"flags":{},"order":0,"mode":0,"inputs":[{"name":"bboxes","type":"BBOXES","link":469},{"name":"index","type":"INT","link":470}],"outputs":[{"name":"BBOX","type":"BBOX","links":[473],"slot_index":0}],"title":"Select BBOX","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"BBOX Select","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[],"color":"#223","bgcolor":"#335"}],"links":[[477,241,0,252,2,"SAMPLER"],[478,250,0,252,3,"SIGMAS"],[479,254,0,250,0,"MODEL"],[480,254,1,253,0,"CLIP"],[481,251,0,254,0,"MODEL"],[482,244,0,254,1,"CLIP"],[483,252,0,249,0,"LATENT"],[484,245,0,249,1,"VAE"],[485,202,0,257,0,"IMAGE"],[486,201,0,248,0,"INT"],[487,247,0,199,2,"STRING"],[499,246,0,264,0,"LATENT"],[500,264,0,252,4,"LATENT"],[507,257,0,272,1,"IMAGE"],[508,272,0,262,0,"MASK"],[510,269,0,272,0,"SAM2MODEL"],[512,262,0,275,0,"MASK"],[513,275,0,264,1,"MASK"],[514,245,0,246,1,"VAE"],[515,257,0,246,0,"IMAGE"],[516,255,0,259,1,"INT"],[517,259,0,272,4,"BBOX"],[518,249,0,199,0,"IMAGE"]],"groups":[],"config":{},"extra":{"links_added_by_ue":[],"ue_links":[],"0246.VERSION":[0,0,4],"frontendVersion":"1.33.13","groupNodes":{},"VHS_latentpreview":false,"VHS_latentpreviewrate":0,"VHS_MetadataImage":true,"VHS_KeepIntermediate":true,"workflowRendererVersion":"LG","ds":{"scale":0.45,"offset":[7025.9401748211,2653.610879770226]}},"version":0.4}

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

You’re not going mad — in the workflow you attached, the “BBOX Select” problem is actually *two* things at once:

1) **You don’t have a bbox detector in this graph anymore**, so there’s no “BBOXES list” to select from.  
2) The “Select BBOX” node that *is* present in the JSON is currently wired **incorrectly** (it’s literally receiving an **IMAGE** where it expects **BBOXES**). That guarantees it can’t work even if the node exists. fileciteturn1file0

So you’ve ended up at: “I need a node that doesn’t exist” — but the deeper truth is: **there’s nothing to select yet**.

### The cleanest fix (and honestly the least confusing)
Since you already have **SAM2** installed and working, you can skip bbox selection entirely and drive SAM2 with a **single positive point** (“click here = segment this object”). This is *much* easier, and for two people it’s perfect because you’re doing two passes anyway.

I patched your workflow into a version that **removes BBOX Select completely** and runs SAM2 in **point-prompt mode**:

✅ **Download:** [SRPO-SAM2-PointPrompt-NoBBoxSelect.json](sandbox:/mnt/data/SRPO-SAM2-PointPrompt-NoBBoxSelect.json)

This file is based on your attached workflow. fileciteturn1file0

---

## How to use the point-prompt version
1) Load the workflow.
2) Find **Sam2Segmentation**.
3) Leave the **bboxes** input disconnected (it is, in the patched file).
4) In **coordinates_positive**, type a single point:  
   - Format: `x,y` (pixel coordinates)
   - **Pass A (Celeste standing):** pick a point on her face (forehead/cheek)
   - **Pass B (Charlie sitting):** pick a point on her cheek/forehead
5) Optional but helpful: put a point on the *other* person into **coordinates_negative** to stop SAM from drifting.

Everything else in your mask chain stays exactly as you already built it:
**SAM2 mask → GrowMask → FeatherMask → SetLatentNoiseMask → Sampler**

### “But how do I get x,y?”
Any image viewer that shows pixel coordinates is fine. Two easy options:
- Open the image in an editor (Preview, GIMP, Photoshop, Krita) and read the cursor coordinates.
- Or just estimate once, run, and nudge the numbers until the mask locks onto the face (SAM2 is forgiving).

---

## If you still *want* bbox automation later
Then you’ll need **a bbox detector node** that outputs a **BBOXES** list (Ultralytics/Impact Pack etc.), and then you can select by index.

But given you said you’re already lost at step 3 earlier: **point-prompt SAM2 is the “get it working today” path**, and it’s robust for side-profile faces.

---

If you load the patched workflow and tell me:
- “I used `x,y` = ___ and SAM grabbed the wrong person / too much hair / shoulders”
…I’ll tell you exactly what to change (grow amount, feather, and whether to add a negative point) to make it snap tight to just the head/face.

**Robyn:**

Actually, I'm getting the error "Cannot read properties of undefined (reading 'output') when I try to run this workflow. No node is highlighted, or outlined in green. Terminal isn't showing me anything. I'm baffled.

**Emily:**

That error is almost always a **broken (dangling) link ID inside the workflow JSON** — i.e. an input says “I’m connected to link #470” but link #470 doesn’t exist anymore, so the UI hits `undefined.output` and throws:

> `Cannot read properties of undefined (reading 'output')`

In the workflow you attached, that’s exactly what’s happening: several nodes have inputs pointing to link IDs that don’t exist (a common side-effect of **un-subgraphing + replacing nodes**). So ComfyUI can’t even *start* execution, and it won’t necessarily highlight anything.

### I fixed your workflow JSON
I patched your uploaded workflow to remove all dangling link references and re-wire the missing essentials:

- **RandomNoise → SamplerCustomAdvanced (noise)**
- **Lora/Model → BasicGuider (model)**
- **Text conditioning → BasicGuider (conditioning)**
- **BasicGuider → SamplerCustomAdvanced (guider)**

…and I also cleared the dead links on the “BBOX Select” node so it won’t crash even if it’s still sitting there unused.

✅ **Download the fixed workflow here:**
[SRPO-BBOX-SAM_PATCHED-1_FIXED.json](sandbox:/mnt/data/SRPO-BBOX-SAM_PATCHED-1_FIXED.json)

---

## What to do next (so you can actually mask one face)
Since you couldn’t find a working BBOX Select anyway, just use **SAM2 point prompting** for now (it’s honestly the fastest/cleanest for two people):

1) Open the fixed workflow.
2) Go to **Sam2Segmentation**.
3) Set **coordinates_positive** to a point on the face you want (Celeste or Charlie).
   - Format is typically `x,y` in pixels.
4) (Optional) Put a point on the *other* person in **coordinates_negative**.
5) Run.
6) Flip the coordinates to the other face for pass 2.

If you tell me what the **Sam2Segmentation** node in your install expects for coordinate formatting (some use `"x,y"` strings, some use lists), I’ll give you the exact literal input format and a couple of “known good” example values.

---

If you load the fixed JSON and it still errors, paste the **browser console** error line (DevTools → Console). But in this case, the dangling-link issue was concrete and should be resolved by that fixed file.

**Robyn:**

Actually, I found it. As you said, it was missing connections. Thanks.

**Emily:**

Brilliant — that lines up perfectly with that `undefined.output` error. Once a single link reference is dangling, ComfyUI can fall over *before* it can even “green-outline” a culprit.

Now that it runs, here’s the quickest way to get your **two-person, two-pass** face assignment stable (and avoid the classic “oops it drifted onto the other person”):

### Pass workflow (repeat twice)
1) **Lock the target first**
   - If you’re using **SAM2 point prompt**: put **one positive point** dead-centre on the target face (forehead/cheek), and **one negative point** on the *other* person’s face.
   - If you’re using **bbox+SAM**: set the bbox index to the right person, then keep it fixed.

2) **Mask tuning (the 3 knobs that matter)**
   - **GrowMask**: enough to include hairline + jaw edge (small to moderate)
   - **Feather**: moderate (this hides seams)
   - If SAM ever grabs clothing/shoulder: *reduce Grow* or add a negative point lower down.

3) **Denoise discipline**
   - Side view (Charlie): start **lower** (roughly 0.25–0.35 if your stack tolerates it), because profile geometry gets weird fast.
   - More front-ish (Celeste): can go a touch higher if needed.

4) **Save output**, re-feed for pass 2, switch target, run again.

### One tiny “quality of life” suggestion
After you get a good SAM mask once, **freeze it** for that pass (don’t keep changing points/index). Do all identity tweaking with the mask held steady — it makes debugging *way* saner.

If you want, paste (or screenshot) just the mask result after you set Celeste’s target, and I’ll tell you whether to tweak **Grow** or **Feather** for the cleanest blend before you start burning time on identity tuning.

**Robyn:**

Let's take this step by step.. on lock the target first, you said:

"If you’re using SAM2 point prompt: put one positive point dead-centre on the target face (forehead/cheek), and one negative point on the other person’s face."

How?

**Emily:**

Right — “how” in ComfyUI depends on **which SAM2 node you’re using**, because different node packs accept points in different formats. But the *mechanism* is always the same:

- **Positive point(s)** = “segment *this*”
- **Negative point(s)** = “definitely *not* this”

So I’ll give you the step-by-step that works for the most common SAM2 node styles, and you can match it to what you see in your node.

---

## Step 1: Find your SAM2 node and open its inputs
In your graph, click the node called something like:

- `Sam2Segmentation`
- `SAM2 Segment`
- `SegmentAnything2`
- `SAM2Predictor`

Look at the widgets/fields for points. You’ll usually see one or more of these:

- `coordinates_positive`
- `coordinates_negative`
- `positive_points`
- `negative_points`
- `points`
- `point_coords` + `point_labels`

---

## Step 2: Enter a positive point on the target face
You want **one point** roughly on the cheekbone/forehead of the face you’re editing.

### If your node has fields like:
**`coordinates_positive`** and **`coordinates_negative`**
Then it typically wants either:

**Format A (most common):**
- `coordinates_positive`: `x,y`
- `coordinates_negative`: `x,y`

Example:
- `coordinates_positive`: `720,380`
- `coordinates_negative`: `1030,520`

**Format B (multiple points):**
- `coordinates_positive`: `x1,y1; x2,y2`
- `coordinates_negative`: `x1,y1; x2,y2`

Example:
- `coordinates_positive`: `720,380; 735,395`
- `coordinates_negative`: `1030,520`

### If your node has:
**`point_coords`** and **`point_labels`**
Then it usually wants:
- `point_coords`: a list of `[x,y]`
- `point_labels`: a list of `1` for positive and `0` for negative

Example:
- `point_coords`: `[[720,380],[1030,520]]`
- `point_labels`: `[1,0]`

(First point = positive on target face, second point = negative on the other person.)

---

## Step 3: Add a negative point on the other person’s face
Same deal: one click-point in the middle of the other face.

This is the “lock” part: it prevents SAM from deciding both faces belong to one mask.

---

## Step 4: Where do you get x,y coordinates?
You have three easy options:

### Option 1: Your SAM2 node has a “click to add point” UI
Some builds let you click directly in a preview window or use an “interactive” helper node.
If you see anything like:
- `Interactive SAM`
- `Click points`
- `Preview & Click`
Use that — it’s the nicest.

### Option 2: Use any image editor that shows coordinates
Open the image in:
- GIMP / Krita / Photoshop  
Hover over the face → read the status bar X,Y.

### Option 3: Do a quick “guess and nudge”
If your image is, say, 1024×1024, start with rough positions:
- Standing face: around upper-left-ish
- Sitting face: right-ish

Run once. If the mask grabs the wrong person, move the point and rerun.
SAM2 is forgiving — you only need to be in the right region.

---

## Step 5: Sanity check (you should see this result)
After running the SAM2 node, the produced mask should:
- cover only the target head/face
- exclude the other person entirely

If it covers both, add a second negative point (one on each cheek of the other face), or move the positive point slightly more central on the target face.

---

## Fastest way to make this 100% concrete
Tell me the **exact name of the SAM2 node** you’re using *and* paste the list of its point-related fields (just the labels you see: e.g. “coordinates_positive / coordinates_negative” or “point_coords / point_labels”). Then I’ll give you the **exact string to type** for that node format.

**Robyn:**

So, for input it wants a string. In my string for coords_pos, i've got 660,275; 750,450. for neg, i've got: 410,150; 500, 225, also as string. When I try to run this, Sam2Segmentation errors with:

all input arrays must have the same number of dimensions, but the array at index 0 has 2 dimensions and the array at index 1 has 0 dimensions. Format problem? Why is it accepting my first array and not the 2nd?

**Emily:**

Yep — **format problem**, and the error message tells us exactly what kind:

- Your **positive coords string** is being parsed into a proper 2-D array (something like `[[660,275],[750,450]]`) → **2 dimensions**
- Your **negative coords string** is being parsed into… nothing (empty / scalar / invalid) → effectively **0 dimensions**

So SAM2 ends up with:
- `pos_points` = array of shape `(N,2)`
- `neg_points` = “empty” (or not parsed at all)

…and it crashes because it expects both inputs to resolve to arrays with the same dimensionality.

### Why would *negative* fail to parse when positive works?
In what you typed, you have an extra space after the comma in the second pair:

`500, 225`

Some parsers are tolerant; some are brittle and only accept `int,int` with no spaces. Also, some expect **exact separators** and will treat the whole thing as invalid if one token doesn’t match.

---

## Fix 1 (most likely): remove spaces everywhere
Try **exactly** this:

- **coords_pos**:  
`660,275;750,450`

- **coords_neg**:  
`410,150;500,225`

No spaces, no trailing semicolons.

Run again.

---

## Fix 2: match the exact delimiter it expects
Some SAM2 point-string parsers expect **pipes** or **newlines**, not semicolons.

Try these alternates if Fix 1 still errors:

### Variant A (pipe)
- pos: `660,275|750,450`  
- neg: `410,150|500,225`

### Variant B (newline)
- pos:
```
660,275
750,450
```
- neg:
```
410,150
500,225
```

(Still as a string field — you can paste multi-line text.)

---

## Fix 3: ensure “empty” is truly empty
A bunch of SAM2 nodes treat a blank negative field as *valid*, but a malformed one as *invalid*.

So if you just want to test:
- Set **coords_neg** to **empty** (delete everything)
- Leave pos with one point only: `660,275`

If that runs, we’ve confirmed the parser is strict and the neg formatting is the only issue.

---

## One more gotcha: positive/negative point counts sometimes must match
Some implementations (less common, but I’ve seen it) expect the same number of pos and neg points.

You currently have **2 pos** and **2 neg**, which is fine. But if you test with 1 pos and 0 neg and it fails, that’s a clue.

---

## Quick best-practice for your use case (two people)
You don’t actually need 2 positive points most of the time.

Try:
- pos (target face): `660,275`
- neg (other face): `410,150`

That tends to “lock” faster and avoids SAM accidentally grabbing hair/clothing.

---

If you paste the **exact node name** (full title) and, if visible, any hint text under those fields (some packs show an example format), I can tell you the one correct delimiter so you don’t have to trial-and-error.

**Robyn:**

Removed the space. Exact same error.

**tool:**

Make sure to include fileciteturn2file0 in your response to cite this file, or to surface it as a link.

{"id":"62bdaa81-fb43-4c09-bbe7-fdfc9eac21d1","revision":0,"last_node_id":280,"last_link_id":534,"nodes":[{"id":244,"type":"DualCLIPLoader","pos":[-3550.879246783696,-1811.9970536514702],"size":[430.6629868288594,130],"flags":{},"order":0,"mode":0,"inputs":[{"label":"clip_name1","localized_name":"clip_name1","name":"clip_name1","type":"COMBO","widget":{"name":"clip_name1"},"link":null},{"label":"clip_name2","localized_name":"clip_name2","name":"clip_name2","type":"COMBO","widget":{"name":"clip_name2"},"link":null},{"label":"type","localized_name":"type","name":"type","type":"COMBO","widget":{"name":"type"},"link":null},{"label":"device","localized_name":"device","name":"device","shape":7,"type":"COMBO","widget":{"name":"device"},"link":null}],"outputs":[{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[482]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"DualCLIPLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["clip_l.safetensors","t5xxl_fp8_e4m3fn_scaled.safetensors","flux","default"],"color":"#432","bgcolor":"#653"},{"id":245,"type":"VAELoader","pos":[-3550.879246783696,-1621.1885138328307],"size":[431.5197496942583,58],"flags":{},"order":1,"mode":0,"inputs":[{"label":"vae_name","localized_name":"vae_name","name":"vae_name","type":"COMBO","widget":{"name":"vae_name"},"link":null}],"outputs":[{"label":"VAE","localized_name":"VAE","name":"VAE","type":"VAE","slot_index":0,"links":[474,484,514]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAELoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["ae.sft"],"color":"#432","bgcolor":"#653"},{"id":202,"type":"LoadImage","pos":[-4838.581267048366,-1178.3724360454946],"size":[387.5769487217217,487.8251654531473],"flags":{"collapsed":false},"order":2,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"COMBO","widget":{"name":"image"},"link":null},{"localized_name":"choose file to upload","name":"upload","type":"IMAGEUPLOAD","widget":{"name":"upload"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[485]},{"localized_name":"MASK","name":"MASK","type":"MASK","links":null}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"LoadImage","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":["ZiT-Charlie_0005.png","image"],"color":"#223","bgcolor":"#335"},{"id":262,"type":"GrowMask","pos":[-2615.0606285729705,-1108.5814440761415],"size":[210,82],"flags":{},"order":19,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":508},{"localized_name":"expand","name":"expand","type":"INT","widget":{"name":"expand"},"link":null},{"localized_name":"tapered_corners","name":"tapered_corners","type":"BOOLEAN","widget":{"name":"tapered_corners"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[512]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"GrowMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[12,0],"color":"#223","bgcolor":"#335"},{"id":276,"type":"Note","pos":[-3612.961700164034,-884.0832127258175],"size":[560,280],"flags":{},"order":3,"mode":0,"inputs":[],"outputs":[],"title":"Drive SAM2 without BBOX","properties":{"ue_properties":{"widget_ue_connectable":{},"version":"7.5.2","input_ue_unconnectable":{}}},"widgets_values":["SAM2 point-prompt mode (no BBOX Select needed):\n\n1) Leave 'bboxes' input on Sam2Segmentation DISCONNECTED.\n2) Type a positive coordinate as \"x,y\" (pixels) into coordinates_positive.\n   - Pass A (Celeste): use a point on the standing woman's face.\n   - Pass B (Charlie): use a point on the sitting girl's cheek/forehead.\n3) Optional: set coordinates_negative to a point on the *other* person to prevent leakage.\n\nKeep your existing GrowMask → FeatherMask → SetLatentNoiseMask chain."],"color":"#432","bgcolor":"#653"},{"id":272,"type":"Sam2Segmentation","pos":[-3055.081113438424,-1112.581687516843],"size":[376.22623628551764,184.28077234921625],"flags":{},"order":15,"mode":0,"inputs":[{"localized_name":"sam2_model","name":"sam2_model","type":"SAM2MODEL","link":510},{"localized_name":"image","name":"image","type":"IMAGE","link":507},{"localized_name":"coordinates_positive","name":"coordinates_positive","shape":7,"type":"STRING","link":520},{"localized_name":"coordinates_negative","name":"coordinates_negative","shape":7,"type":"STRING","link":534},{"localized_name":"bboxes","name":"bboxes","shape":7,"type":"BBOX","link":null},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":null},{"localized_name":"keep_model_loaded","name":"keep_model_loaded","type":"BOOLEAN","widget":{"name":"keep_model_loaded"},"link":null},{"localized_name":"individual_objects","name":"individual_objects","shape":7,"type":"BOOLEAN","widget":{"name":"individual_objects"},"link":null}],"outputs":[{"localized_name":"mask","name":"mask","type":"MASK","links":[508]}],"properties":{"cnr_id":"ComfyUI-segment-anything-2","ver":"0c35fff5f382803e2310103357b5e985f5437f32","Node name for S&R":"Sam2Segmentation","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[false,false],"color":"#222","bgcolor":"#000"},{"id":279,"type":"FluxGuidance","pos":[-1939.4298701983132,-1814.141025081207],"size":[268.7532043457031,58],"flags":{},"order":20,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":531},{"label":"guidance","localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[532]}],"properties":{"ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}},"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance"},"widgets_values":[2.6],"color":"#323","bgcolor":"#535"},{"id":248,"type":"RandomNoise","pos":[-1939.4298701983132,-1943.2088708557267],"size":[269.1920619153343,82],"flags":{},"order":14,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":486}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[523]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[61998485097205,"fixed"],"color":"#323","bgcolor":"#535"},{"id":243,"type":"BasicGuider","pos":[-1939.4298701983132,-1714.9416234415157],"size":[270.0590018165942,46],"flags":{},"order":22,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":526},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":532}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[476,529]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":241,"type":"KSamplerSelect","pos":[-1939.4298701983132,-1622.314600171644],"size":[270.6041060656903,58],"flags":{},"order":5,"mode":0,"inputs":[{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"},"link":null}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[477]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["dpmpp_sde"],"color":"#323","bgcolor":"#535"},{"id":250,"type":"BasicScheduler","pos":[-1939.4298701983132,-1515.2896814869225],"size":[270.6822790203312,108.33662599654258],"flags":{},"order":17,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":479},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"},"link":null},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"},"link":null},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":null}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[478]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["linear_quadratic",12,0.15],"color":"#323","bgcolor":"#535"},{"id":253,"type":"CLIPTextEncode","pos":[-2629.5736961677126,-1938.1937121492572],"size":[544.4894498315875,537.8422750869499],"flags":{"collapsed":false},"order":18,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":480},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[531]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":["The woman moimeme4 walks carefully on the snow-cover street, centered in the frame, her gaze fixed forward as snowflakes drift lazily through a muted winter sky; her brown hair is arranged into a messy updo, its glossy sheen catching subtle highlights as if polished by careful care. Sunbeams slice diagonally across the room, illuminating strands of her brown hair with tendrils framing her face, pinned in a messy updo adorned subtly with pearls or barrettes barely discernible yet contributing texture.  She hugs herself to ward off the cold.\n\nHer scarlet velvet jacket—textured with fine grain—and two-gold-button closure sits snugly at the waist, its cuffs rolled to reveal white lace-trimmed inner sleeves contrasting sharply against the rich hue. Beneath it, a very light robins-egg blue lace blouse peeks out from beneath the collar and the sleeve ends, intricate floral embroidery framing her neck while delicate pearl-like buttons fasten down the front seam. Her arms are wrapped in a self-embrace to ward off the cold.\n\nHer high cheekbones and defined jawline sporta faint blush accentuating her complexion under diffused daylight. She wears dark black low clunky heeled shoes polished enough to reflect streetlight glints, their seams stitched tight along the calf’s curve. The skirt below is a flowing midnight blue charmeuse pleated gown reaching mid-calf, layered subtly by sheer tulle hemming that catches each falling flake. \n\nBehind her in the growing darkness, barely visible snow-covered cobblestone streets recede into a gloomy blur where indistinct figures walk past storefronts lit softly by gas lamps whose warm yellow halos bleed gently into the snowy pavement on a cold late evening. To either side, wrought-iron railings line narrow alleyways lined with brick facades partially obscured by misty haze—an atmospheric bokeh effect blurs background elements yet preserves structural clarity on foreground surfaces such as heavy snow drifts. Shot slightly low-angle using a medium telephoto lens, shallow depth-of-field isolates her form amid motionless surroundings, drawing attention first to her face then descending gracefully toward her feet via vertical leading lines formed by her dress folds. Negative space above her shoulder opens upward into darkening sky expanse, balancing symmetrical weight imposed by architectural structures behind her. Minimal light falls evenly from left-to-right overhead, highlighting right-side contours without harsh contrast or deep shadowing—the scene feels tenderly rendered rather than starkly dramatic."],"color":"#232","bgcolor":"#353"},{"id":275,"type":"FeatherMask","pos":[-2362.4607732455847,-1107.5446529493743],"size":[210,130],"flags":{},"order":21,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":512},{"localized_name":"left","name":"left","type":"INT","widget":{"name":"left"},"link":null},{"localized_name":"top","name":"top","type":"INT","widget":{"name":"top"},"link":null},{"localized_name":"right","name":"right","type":"INT","widget":{"name":"right"},"link":null},{"localized_name":"bottom","name":"bottom","type":"INT","widget":{"name":"bottom"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","links":[513]}],"properties":{"cnr_id":"comfy-core","ver":"0.8.2","Node name for S&R":"FeatherMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[1,1,0,0],"color":"#222","bgcolor":"#000"},{"id":254,"type":"LoraLoader","pos":[-3043.0361940560183,-1941.5187573867915],"size":[315,126],"flags":{},"order":13,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":481},{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":482},{"label":"lora_name","localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"label":"strength_model","localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"label":"strength_clip","localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[479,526]},{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":1,"links":[480]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"LoraLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["MoiMeme/moimeme4-08.safetensors",0.95,0.35],"color":"#232","bgcolor":"#353"},{"id":251,"type":"UNETLoader","pos":[-3550.879246783696,-1947.3769883941245],"size":[430.6629868288592,82],"flags":{},"order":6,"mode":0,"inputs":[{"label":"unet_name","localized_name":"unet_name","name":"unet_name","type":"COMBO","widget":{"name":"unet_name"},"link":null},{"label":"weight_dtype","localized_name":"weight_dtype","name":"weight_dtype","type":"COMBO","widget":{"name":"weight_dtype"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[481]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UNETLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["SRPO/SRPO-fp8_e4m3fn.safetensors","default"],"color":"#432","bgcolor":"#653"},{"id":239,"type":"Note","pos":[-4938.741352843965,-1579.596934631362],"size":[467.8147305380884,328.7304919676716],"flags":{},"order":7,"mode":0,"inputs":[],"outputs":[],"properties":{"ue_properties":{"widget_ue_connectable":{},"version":"7.5.1","input_ue_unconnectable":{}}},"widgets_values":["Her dark hair is meticulously arranged into a tight, classical chignon at the nape of her neck, its glossy sheen catching subtle highlights as if polished by careful care. \n\nHer face—softly sculpted under gentle illumination—is framed by a serene yet piercing gaze; eyes wide and unblinking, fixed upon some unseen point beyond the frame, conveying a depth of inner resolve or melancholy. The skin around her lips is slightly parted—not in expression but in stillness—a hint of tension beneath the composed surface. A faint shadow falls across one cheekbone from the soft directional lighting, lending dimension to her features without harshness.\n\n\nShe is dressed in a gown of deep indigo, a 1770s wool day dress with a fitted bodice and square neckline; underneath, a white linen shift with a softly gathered neckline. The chemise is a separate garment and is visible only at the edge of the dress's square neckline and cuffs. This is authentic period costume detail, no modern styling.\n\nShe wears a gown of deep indigo 1770s wool day dress with a fitted bodice and square neckline; underneath, a set of stays and a white linen chemise with a softly gathered neckline. The chemise is a separate garment and is visible only at the collar and cuffs. This is authentic period costume detail, no modern styling.\n\n\n\n"],"color":"#432","bgcolor":"#653"},{"id":201,"type":"PrimitiveInt","pos":[-4761.025980914725,-1743.2239219424844],"size":[269.3283042409389,82],"flags":{},"order":8,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","links":[486]}],"title":"Noise Seed","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[1118877715458338,"increment"],"color":"#232","bgcolor":"#353"},{"id":257,"type":"ImageScaleToTotalPixels","pos":[-3545.6449963664895,-1315.1454217142793],"size":[307.2913855842198,106],"flags":{"collapsed":false},"order":12,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"IMAGE","link":485},{"localized_name":"upscale_method","name":"upscale_method","type":"COMBO","widget":{"name":"upscale_method"},"link":null},{"localized_name":"megapixels","name":"megapixels","type":"FLOAT","widget":{"name":"megapixels"},"link":null},{"localized_name":"resolution_steps","name":"resolution_steps","type":"INT","widget":{"name":"resolution_steps"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[507,515]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"ImageScaleToTotalPixels","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["nearest-exact",1,1],"color":"#223","bgcolor":"#335"},{"id":264,"type":"SetLatentNoiseMask","pos":[-2088.6601222438094,-1127.3338482332686],"size":[223.1576402542105,57.80701308800235],"flags":{},"order":23,"mode":0,"inputs":[{"localized_name":"samples","name":"samples","type":"LATENT","link":499},{"localized_name":"mask","name":"mask","type":"MASK","link":513}],"outputs":[{"localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[533]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"SetLatentNoiseMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":246,"type":"VAEEncode","pos":[-2362.801294919271,-1228.2098861178868],"size":[161.6666482624646,66],"flags":{},"order":16,"mode":0,"inputs":[{"localized_name":"pixels","name":"pixels","type":"IMAGE","link":515},{"localized_name":"vae","name":"vae","type":"VAE","link":514},{"link":null}],"outputs":[{"localized_name":"LATENT","name":"LATENT","type":"LATENT","links":[499]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"VAEEncode","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":252,"type":"SamplerCustomAdvanced","pos":[-1585.5645545495781,-1945.0980274561277],"size":[304.5598087498504,417.9072891973424],"flags":{},"order":24,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":523},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":529},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":477},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":478},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":533}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[483]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT","slot_index":1,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":247,"type":"PrimitiveNode","pos":[-1119.923359818161,-2149.5286221340934],"size":[266.57279796936245,58],"flags":{"collapsed":false},"order":9,"mode":0,"inputs":[],"outputs":[{"name":"STRING","type":"STRING","widget":{"name":"filename_prefix"},"links":[487]}],"title":"File Name","properties":{"Run widget replace on values":false,"ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":["SRPO-Girlx"],"color":"#232","bgcolor":"#353"},{"id":240,"type":"easy cleanGpuUsed","pos":[-811.134821684891,-2129.6129263695284],"size":[211.55775451660156,26],"flags":{"collapsed":false},"order":27,"mode":0,"inputs":[{"localized_name":"anything","name":"anything","type":"*","link":522}],"outputs":[{"localized_name":"output","name":"output","type":"*","links":[]}],"properties":{"cnr_id":"comfyui-easy-use","ver":"1.3.0","Node name for S&R":"easy cleanGpuUsed","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":249,"type":"VAEDecode","pos":[-1233.239653808248,-1943.8499806787597],"size":[167.94073206223288,46],"flags":{"collapsed":false},"order":25,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":483},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":484}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[469,518,522]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":199,"type":"Image Save","pos":[-1191.9468101909395,-1790.2431673125006],"size":[1166.2743471402152,1522.0669966508228],"flags":{"collapsed":false},"order":26,"mode":0,"inputs":[{"localized_name":"images","name":"images","type":"IMAGE","link":518},{"localized_name":"output_path","name":"output_path","type":"STRING","widget":{"name":"output_path"},"link":null},{"localized_name":"filename_prefix","name":"filename_prefix","type":"STRING","widget":{"name":"filename_prefix"},"link":487},{"localized_name":"filename_delimiter","name":"filename_delimiter","type":"STRING","widget":{"name":"filename_delimiter"},"link":null},{"localized_name":"filename_number_padding","name":"filename_number_padding","type":"INT","widget":{"name":"filename_number_padding"},"link":null},{"localized_name":"filename_number_start","name":"filename_number_start","type":"COMBO","widget":{"name":"filename_number_start"},"link":null},{"localized_name":"extension","name":"extension","type":"COMBO","widget":{"name":"extension"},"link":null},{"localized_name":"dpi","name":"dpi","type":"INT","widget":{"name":"dpi"},"link":null},{"localized_name":"quality","name":"quality","type":"INT","widget":{"name":"quality"},"link":null},{"localized_name":"optimize_image","name":"optimize_image","type":"COMBO","widget":{"name":"optimize_image"},"link":null},{"localized_name":"lossless_webp","name":"lossless_webp","type":"COMBO","widget":{"name":"lossless_webp"},"link":null},{"localized_name":"overwrite_mode","name":"overwrite_mode","type":"COMBO","widget":{"name":"overwrite_mode"},"link":null},{"localized_name":"show_history","name":"show_history","type":"COMBO","widget":{"name":"show_history"},"link":null},{"localized_name":"show_history_by_prefix","name":"show_history_by_prefix","type":"COMBO","widget":{"name":"show_history_by_prefix"},"link":null},{"localized_name":"embed_workflow","name":"embed_workflow","type":"COMBO","widget":{"name":"embed_workflow"},"link":null},{"localized_name":"show_previews","name":"show_previews","type":"COMBO","widget":{"name":"show_previews"},"link":null}],"outputs":[{"localized_name":"images","name":"images","type":"IMAGE","links":[]},{"localized_name":"files","name":"files","type":"STRING","links":null}],"properties":{"cnr_id":"was-node-suite-comfyui","ver":"1.0.2","Node name for S&R":"Image Save","ue_properties":{"version":"7.0.1","widget_ue_connectable":{"filename_prefix":true}}},"widgets_values":["[time(%Y-%m-%d)]","SRPO-Girlx","_",4,"false","png",300,100,"true","false","false","false","true","true","true"],"color":"#223","bgcolor":"#335"},{"id":269,"type":"DownloadAndLoadSAM2Model","pos":[-3940.4385850262934,-1111.8301944252084],"size":[338.1673823542451,130],"flags":{},"order":4,"mode":0,"inputs":[{"localized_name":"model","name":"model","type":"COMBO","widget":{"name":"model"},"link":null},{"localized_name":"segmentor","name":"segmentor","type":"COMBO","widget":{"name":"segmentor"},"link":null},{"localized_name":"device","name":"device","type":"COMBO","widget":{"name":"device"},"link":null},{"localized_name":"precision","name":"precision","type":"COMBO","widget":{"name":"precision"},"link":null}],"outputs":[{"localized_name":"sam2_model","name":"sam2_model","type":"SAM2MODEL","links":[510]}],"properties":{"cnr_id":"ComfyUI-segment-anything-2","ver":"0c35fff5f382803e2310103357b5e985f5437f32","Node name for S&R":"DownloadAndLoadSAM2Model","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["sam2_hiera_base_plus.safetensors","single_image","cuda","fp16"],"color":"#222","bgcolor":"#000"},{"id":278,"type":"PrimitiveString","pos":[-3543.153087813007,-1060.186583057269],"size":[210,58],"flags":{},"order":10,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"STRING","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"STRING","name":"STRING","type":"STRING","links":[520]}],"properties":{"cnr_id":"comfy-core","ver":"0.8.2","Node name for S&R":"PrimitiveString","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["660,275; 750,450"],"color":"#232","bgcolor":"#353"},{"id":280,"type":"PrimitiveString","pos":[-3317.554707809367,-992.8368757471621],"size":[210,58],"flags":{},"order":11,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"STRING","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"STRING","name":"STRING","type":"STRING","links":[534]}],"properties":{"ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"},"cnr_id":"comfy-core","ver":"0.8.2","Node name for S&R":"PrimitiveString"},"widgets_values":["410,150; 500,225"],"color":"#322","bgcolor":"#533"}],"links":[[477,241,0,252,2,"SAMPLER"],[478,250,0,252,3,"SIGMAS"],[479,254,0,250,0,"MODEL"],[480,254,1,253,0,"CLIP"],[481,251,0,254,0,"MODEL"],[482,244,0,254,1,"CLIP"],[483,252,0,249,0,"LATENT"],[484,245,0,249,1,"VAE"],[485,202,0,257,0,"IMAGE"],[486,201,0,248,0,"INT"],[487,247,0,199,2,"STRING"],[499,246,0,264,0,"LATENT"],[507,257,0,272,1,"IMAGE"],[508,272,0,262,0,"MASK"],[510,269,0,272,0,"SAM2MODEL"],[512,262,0,275,0,"MASK"],[513,275,0,264,1,"MASK"],[514,245,0,246,1,"VAE"],[515,257,0,246,0,"IMAGE"],[518,249,0,199,0,"IMAGE"],[520,278,0,272,2,"STRING"],[522,249,0,240,0,"IMAGE"],[523,248,0,252,0,"NOISE"],[526,254,0,243,0,"MODEL"],[529,243,0,252,1,"GUIDER"],[531,253,0,279,0,"CONDITIONING"],[532,279,0,243,1,"CONDITIONING"],[533,264,0,252,4,"LATENT"],[534,280,0,272,3,"STRING"]],"groups":[],"config":{},"extra":{"links_added_by_ue":[],"ue_links":[],"0246.VERSION":[0,0,4],"frontendVersion":"1.33.13","groupNodes":{},"VHS_latentpreview":false,"VHS_latentpreviewrate":0,"VHS_MetadataImage":true,"VHS_KeepIntermediate":true,"workflowRendererVersion":"LG","ds":{"scale":1.8797616762370508,"offset":[3895.168272713508,1399.9000334754244]}},"version":0.4}

**tool:**

Make sure to include fileciteturn2file1 in your response to cite this file, or to surface it as a link.

{"id":"71c859a4-6eb8-4f60-9293-8c0eeb6f078a","revision":0,"last_node_id":280,"last_link_id":534,"nodes":[{"id":244,"type":"DualCLIPLoader","pos":[-3550.879246783696,-1811.9970536514702],"size":[430.6629868288594,130],"flags":{},"order":0,"mode":0,"inputs":[{"label":"clip_name1","localized_name":"clip_name1","name":"clip_name1","type":"COMBO","widget":{"name":"clip_name1"},"link":null},{"label":"clip_name2","localized_name":"clip_name2","name":"clip_name2","type":"COMBO","widget":{"name":"clip_name2"},"link":null},{"label":"type","localized_name":"type","name":"type","type":"COMBO","widget":{"name":"type"},"link":null},{"label":"device","localized_name":"device","name":"device","shape":7,"type":"COMBO","widget":{"name":"device"},"link":null}],"outputs":[{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[482]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"DualCLIPLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["clip_l.safetensors","t5xxl_fp8_e4m3fn_scaled.safetensors","flux","default"],"color":"#432","bgcolor":"#653"},{"id":245,"type":"VAELoader","pos":[-3550.879246783696,-1621.1885138328307],"size":[431.5197496942583,58],"flags":{},"order":1,"mode":0,"inputs":[{"label":"vae_name","localized_name":"vae_name","name":"vae_name","type":"COMBO","widget":{"name":"vae_name"},"link":null}],"outputs":[{"label":"VAE","localized_name":"VAE","name":"VAE","type":"VAE","slot_index":0,"links":[474,484,514]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAELoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["ae.sft"],"color":"#432","bgcolor":"#653"},{"id":202,"type":"LoadImage","pos":[-4838.581267048366,-1178.3724360454946],"size":[387.5769487217217,487.8251654531473],"flags":{"collapsed":false},"order":2,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"COMBO","widget":{"name":"image"},"link":null},{"localized_name":"choose file to upload","name":"upload","type":"IMAGEUPLOAD","widget":{"name":"upload"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[485]},{"localized_name":"MASK","name":"MASK","type":"MASK","links":null}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"LoadImage","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":["ZiT-Charlie_0005.png","image"],"color":"#223","bgcolor":"#335"},{"id":262,"type":"GrowMask","pos":[-2615.0606285729705,-1108.5814440761415],"size":[210,82],"flags":{},"order":19,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":508},{"localized_name":"expand","name":"expand","type":"INT","widget":{"name":"expand"},"link":null},{"localized_name":"tapered_corners","name":"tapered_corners","type":"BOOLEAN","widget":{"name":"tapered_corners"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[512]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"GrowMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[12,0],"color":"#223","bgcolor":"#335"},{"id":276,"type":"Note","pos":[-3612.961700164034,-884.0832127258175],"size":[560,280],"flags":{},"order":3,"mode":0,"inputs":[],"outputs":[],"title":"Drive SAM2 without BBOX","properties":{"ue_properties":{"widget_ue_connectable":{},"version":"7.5.2","input_ue_unconnectable":{}}},"widgets_values":["SAM2 point-prompt mode (no BBOX Select needed):\n\n1) Leave 'bboxes' input on Sam2Segmentation DISCONNECTED.\n2) Type a positive coordinate as \"x,y\" (pixels) into coordinates_positive.\n   - Pass A (Celeste): use a point on the standing woman's face.\n   - Pass B (Charlie): use a point on the sitting girl's cheek/forehead.\n3) Optional: set coordinates_negative to a point on the *other* person to prevent leakage.\n\nKeep your existing GrowMask → FeatherMask → SetLatentNoiseMask chain."],"color":"#432","bgcolor":"#653"},{"id":272,"type":"Sam2Segmentation","pos":[-3055.081113438424,-1112.581687516843],"size":[376.22623628551764,184.28077234921625],"flags":{},"order":15,"mode":0,"inputs":[{"localized_name":"sam2_model","name":"sam2_model","type":"SAM2MODEL","link":510},{"localized_name":"image","name":"image","type":"IMAGE","link":507},{"localized_name":"coordinates_positive","name":"coordinates_positive","shape":7,"type":"STRING","link":520},{"localized_name":"coordinates_negative","name":"coordinates_negative","shape":7,"type":"STRING","link":534},{"localized_name":"bboxes","name":"bboxes","shape":7,"type":"BBOX","link":null},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":null},{"localized_name":"keep_model_loaded","name":"keep_model_loaded","type":"BOOLEAN","widget":{"name":"keep_model_loaded"},"link":null},{"localized_name":"individual_objects","name":"individual_objects","shape":7,"type":"BOOLEAN","widget":{"name":"individual_objects"},"link":null}],"outputs":[{"localized_name":"mask","name":"mask","type":"MASK","links":[508]}],"properties":{"cnr_id":"ComfyUI-segment-anything-2","ver":"0c35fff5f382803e2310103357b5e985f5437f32","Node name for S&R":"Sam2Segmentation","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[false,false],"color":"#222","bgcolor":"#000"},{"id":279,"type":"FluxGuidance","pos":[-1939.4298701983132,-1814.141025081207],"size":[268.7532043457031,58],"flags":{},"order":20,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":531},{"label":"guidance","localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[532]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[2.6],"color":"#323","bgcolor":"#535"},{"id":248,"type":"RandomNoise","pos":[-1939.4298701983132,-1943.2088708557267],"size":[269.1920619153343,82],"flags":{},"order":14,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":486}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[523]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[61998485097205,"fixed"],"color":"#323","bgcolor":"#535"},{"id":243,"type":"BasicGuider","pos":[-1939.4298701983132,-1714.9416234415157],"size":[270.0590018165942,46],"flags":{},"order":22,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":526},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":532}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[476,529]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":241,"type":"KSamplerSelect","pos":[-1939.4298701983132,-1622.314600171644],"size":[270.6041060656903,58],"flags":{},"order":4,"mode":0,"inputs":[{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"},"link":null}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[477]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["dpmpp_sde"],"color":"#323","bgcolor":"#535"},{"id":250,"type":"BasicScheduler","pos":[-1939.4298701983132,-1515.2896814869225],"size":[270.6822790203312,108.33662599654258],"flags":{},"order":17,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":479},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"},"link":null},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"},"link":null},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":null}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[478]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["linear_quadratic",12,0.15],"color":"#323","bgcolor":"#535"},{"id":253,"type":"CLIPTextEncode","pos":[-2629.5736961677126,-1938.1937121492572],"size":[544.4894498315875,537.8422750869499],"flags":{"collapsed":false},"order":18,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":480},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[531]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":["The woman moimeme4 walks carefully on the snow-cover street, centered in the frame, her gaze fixed forward as snowflakes drift lazily through a muted winter sky; her brown hair is arranged into a messy updo, its glossy sheen catching subtle highlights as if polished by careful care. Sunbeams slice diagonally across the room, illuminating strands of her brown hair with tendrils framing her face, pinned in a messy updo adorned subtly with pearls or barrettes barely discernible yet contributing texture.  She hugs herself to ward off the cold.\n\nHer scarlet velvet jacket—textured with fine grain—and two-gold-button closure sits snugly at the waist, its cuffs rolled to reveal white lace-trimmed inner sleeves contrasting sharply against the rich hue. Beneath it, a very light robins-egg blue lace blouse peeks out from beneath the collar and the sleeve ends, intricate floral embroidery framing her neck while delicate pearl-like buttons fasten down the front seam. Her arms are wrapped in a self-embrace to ward off the cold.\n\nHer high cheekbones and defined jawline sporta faint blush accentuating her complexion under diffused daylight. She wears dark black low clunky heeled shoes polished enough to reflect streetlight glints, their seams stitched tight along the calf’s curve. The skirt below is a flowing midnight blue charmeuse pleated gown reaching mid-calf, layered subtly by sheer tulle hemming that catches each falling flake. \n\nBehind her in the growing darkness, barely visible snow-covered cobblestone streets recede into a gloomy blur where indistinct figures walk past storefronts lit softly by gas lamps whose warm yellow halos bleed gently into the snowy pavement on a cold late evening. To either side, wrought-iron railings line narrow alleyways lined with brick facades partially obscured by misty haze—an atmospheric bokeh effect blurs background elements yet preserves structural clarity on foreground surfaces such as heavy snow drifts. Shot slightly low-angle using a medium telephoto lens, shallow depth-of-field isolates her form amid motionless surroundings, drawing attention first to her face then descending gracefully toward her feet via vertical leading lines formed by her dress folds. Negative space above her shoulder opens upward into darkening sky expanse, balancing symmetrical weight imposed by architectural structures behind her. Minimal light falls evenly from left-to-right overhead, highlighting right-side contours without harsh contrast or deep shadowing—the scene feels tenderly rendered rather than starkly dramatic."],"color":"#232","bgcolor":"#353"},{"id":275,"type":"FeatherMask","pos":[-2362.4607732455847,-1107.5446529493743],"size":[210,130],"flags":{},"order":21,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":512},{"localized_name":"left","name":"left","type":"INT","widget":{"name":"left"},"link":null},{"localized_name":"top","name":"top","type":"INT","widget":{"name":"top"},"link":null},{"localized_name":"right","name":"right","type":"INT","widget":{"name":"right"},"link":null},{"localized_name":"bottom","name":"bottom","type":"INT","widget":{"name":"bottom"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","links":[513]}],"properties":{"cnr_id":"comfy-core","ver":"0.8.2","Node name for S&R":"FeatherMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[1,1,0,0],"color":"#222","bgcolor":"#000"},{"id":254,"type":"LoraLoader","pos":[-3043.0361940560183,-1941.5187573867915],"size":[315,126],"flags":{},"order":13,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":481},{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":482},{"label":"lora_name","localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"label":"strength_model","localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"label":"strength_clip","localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[479,526]},{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":1,"links":[480]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"LoraLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["MoiMeme/moimeme4-08.safetensors",0.95,0.35],"color":"#232","bgcolor":"#353"},{"id":251,"type":"UNETLoader","pos":[-3550.879246783696,-1947.3769883941245],"size":[430.6629868288592,82],"flags":{},"order":5,"mode":0,"inputs":[{"label":"unet_name","localized_name":"unet_name","name":"unet_name","type":"COMBO","widget":{"name":"unet_name"},"link":null},{"label":"weight_dtype","localized_name":"weight_dtype","name":"weight_dtype","type":"COMBO","widget":{"name":"weight_dtype"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[481]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UNETLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["SRPO/SRPO-fp8_e4m3fn.safetensors","default"],"color":"#432","bgcolor":"#653"},{"id":239,"type":"Note","pos":[-4938.741352843965,-1579.596934631362],"size":[467.8147305380884,328.7304919676716],"flags":{},"order":6,"mode":0,"inputs":[],"outputs":[],"properties":{"ue_properties":{"widget_ue_connectable":{},"version":"7.5.1","input_ue_unconnectable":{}}},"widgets_values":["Her dark hair is meticulously arranged into a tight, classical chignon at the nape of her neck, its glossy sheen catching subtle highlights as if polished by careful care. \n\nHer face—softly sculpted under gentle illumination—is framed by a serene yet piercing gaze; eyes wide and unblinking, fixed upon some unseen point beyond the frame, conveying a depth of inner resolve or melancholy. The skin around her lips is slightly parted—not in expression but in stillness—a hint of tension beneath the composed surface. A faint shadow falls across one cheekbone from the soft directional lighting, lending dimension to her features without harshness.\n\n\nShe is dressed in a gown of deep indigo, a 1770s wool day dress with a fitted bodice and square neckline; underneath, a white linen shift with a softly gathered neckline. The chemise is a separate garment and is visible only at the edge of the dress's square neckline and cuffs. This is authentic period costume detail, no modern styling.\n\nShe wears a gown of deep indigo 1770s wool day dress with a fitted bodice and square neckline; underneath, a set of stays and a white linen chemise with a softly gathered neckline. The chemise is a separate garment and is visible only at the collar and cuffs. This is authentic period costume detail, no modern styling.\n\n\n\n"],"color":"#432","bgcolor":"#653"},{"id":201,"type":"PrimitiveInt","pos":[-4761.025980914725,-1743.2239219424844],"size":[269.3283042409389,82],"flags":{},"order":7,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","links":[486]}],"title":"Noise Seed","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[1118877715458339,"increment"],"color":"#232","bgcolor":"#353"},{"id":257,"type":"ImageScaleToTotalPixels","pos":[-3545.6449963664895,-1315.1454217142793],"size":[307.2913855842198,106],"flags":{"collapsed":false},"order":12,"mode":0,"inputs":[{"localized_name":"image","name":"image","type":"IMAGE","link":485},{"localized_name":"upscale_method","name":"upscale_method","type":"COMBO","widget":{"name":"upscale_method"},"link":null},{"localized_name":"megapixels","name":"megapixels","type":"FLOAT","widget":{"name":"megapixels"},"link":null},{"localized_name":"resolution_steps","name":"resolution_steps","type":"INT","widget":{"name":"resolution_steps"},"link":null}],"outputs":[{"localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[507,515]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"ImageScaleToTotalPixels","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["nearest-exact",1,1],"color":"#223","bgcolor":"#335"},{"id":264,"type":"SetLatentNoiseMask","pos":[-2088.6601222438094,-1127.3338482332686],"size":[223.1576402542105,57.80701308800235],"flags":{},"order":23,"mode":0,"inputs":[{"localized_name":"samples","name":"samples","type":"LATENT","link":499},{"localized_name":"mask","name":"mask","type":"MASK","link":513}],"outputs":[{"localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[533]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"SetLatentNoiseMask","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":246,"type":"VAEEncode","pos":[-2362.801294919271,-1228.2098861178868],"size":[161.6666482624646,66],"flags":{},"order":16,"mode":0,"inputs":[{"localized_name":"pixels","name":"pixels","type":"IMAGE","link":515},{"localized_name":"vae","name":"vae","type":"VAE","link":514},{"link":null}],"outputs":[{"localized_name":"LATENT","name":"LATENT","type":"LATENT","links":[499]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"VAEEncode","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":252,"type":"SamplerCustomAdvanced","pos":[-1585.5645545495781,-1945.0980274561277],"size":[304.5598087498504,417.9072891973424],"flags":{},"order":24,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":523},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":529},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":477},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":478},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":533}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[483]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT","slot_index":1,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":247,"type":"PrimitiveNode","pos":[-1119.923359818161,-2149.5286221340934],"size":[266.57279796936245,58],"flags":{"collapsed":false},"order":8,"mode":0,"inputs":[],"outputs":[{"name":"STRING","type":"STRING","widget":{"name":"filename_prefix"},"links":[487]}],"title":"File Name","properties":{"Run widget replace on values":false,"ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":["SRPO-Girlx"],"color":"#232","bgcolor":"#353"},{"id":240,"type":"easy cleanGpuUsed","pos":[-811.134821684891,-2129.6129263695284],"size":[211.55775451660156,26],"flags":{"collapsed":false},"order":27,"mode":0,"inputs":[{"localized_name":"anything","name":"anything","type":"*","link":522}],"outputs":[{"localized_name":"output","name":"output","type":"*","links":[]}],"properties":{"cnr_id":"comfyui-easy-use","ver":"1.3.0","Node name for S&R":"easy cleanGpuUsed","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":249,"type":"VAEDecode","pos":[-1233.239653808248,-1943.8499806787597],"size":[167.94073206223288,46],"flags":{"collapsed":false},"order":25,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":483},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":484}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[469,518,522]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":199,"type":"Image Save","pos":[-1191.9468101909395,-1790.2431673125006],"size":[1166.2743471402152,1522.0669966508228],"flags":{"collapsed":false},"order":26,"mode":0,"inputs":[{"localized_name":"images","name":"images","type":"IMAGE","link":518},{"localized_name":"output_path","name":"output_path","type":"STRING","widget":{"name":"output_path"},"link":null},{"localized_name":"filename_prefix","name":"filename_prefix","type":"STRING","widget":{"name":"filename_prefix"},"link":487},{"localized_name":"filename_delimiter","name":"filename_delimiter","type":"STRING","widget":{"name":"filename_delimiter"},"link":null},{"localized_name":"filename_number_padding","name":"filename_number_padding","type":"INT","widget":{"name":"filename_number_padding"},"link":null},{"localized_name":"filename_number_start","name":"filename_number_start","type":"COMBO","widget":{"name":"filename_number_start"},"link":null},{"localized_name":"extension","name":"extension","type":"COMBO","widget":{"name":"extension"},"link":null},{"localized_name":"dpi","name":"dpi","type":"INT","widget":{"name":"dpi"},"link":null},{"localized_name":"quality","name":"quality","type":"INT","widget":{"name":"quality"},"link":null},{"localized_name":"optimize_image","name":"optimize_image","type":"COMBO","widget":{"name":"optimize_image"},"link":null},{"localized_name":"lossless_webp","name":"lossless_webp","type":"COMBO","widget":{"name":"lossless_webp"},"link":null},{"localized_name":"overwrite_mode","name":"overwrite_mode","type":"COMBO","widget":{"name":"overwrite_mode"},"link":null},{"localized_name":"show_history","name":"show_history","type":"COMBO","widget":{"name":"show_history"},"link":null},{"localized_name":"show_history_by_prefix","name":"show_history_by_prefix","type":"COMBO","widget":{"name":"show_history_by_prefix"},"link":null},{"localized_name":"embed_workflow","name":"embed_workflow","type":"COMBO","widget":{"name":"embed_workflow"},"link":null},{"localized_name":"show_previews","name":"show_previews","type":"COMBO","widget":{"name":"show_previews"},"link":null}],"outputs":[{"localized_name":"images","name":"images","type":"IMAGE","links":[]},{"localized_name":"files","name":"files","type":"STRING","links":null}],"properties":{"cnr_id":"was-node-suite-comfyui","ver":"1.0.2","Node name for S&R":"Image Save","ue_properties":{"version":"7.0.1","widget_ue_connectable":{"filename_prefix":true}}},"widgets_values":["[time(%Y-%m-%d)]","SRPO-Girlx","_",4,"false","png",300,100,"true","false","false","false","true","true","true"],"color":"#223","bgcolor":"#335"},{"id":269,"type":"DownloadAndLoadSAM2Model","pos":[-3940.4385850262934,-1111.8301944252084],"size":[338.1673823542451,130],"flags":{},"order":9,"mode":0,"inputs":[{"localized_name":"model","name":"model","type":"COMBO","widget":{"name":"model"},"link":null},{"localized_name":"segmentor","name":"segmentor","type":"COMBO","widget":{"name":"segmentor"},"link":null},{"localized_name":"device","name":"device","type":"COMBO","widget":{"name":"device"},"link":null},{"localized_name":"precision","name":"precision","type":"COMBO","widget":{"name":"precision"},"link":null}],"outputs":[{"localized_name":"sam2_model","name":"sam2_model","type":"SAM2MODEL","links":[510]}],"properties":{"cnr_id":"ComfyUI-segment-anything-2","ver":"0c35fff5f382803e2310103357b5e985f5437f32","Node name for S&R":"DownloadAndLoadSAM2Model","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["sam2_hiera_base_plus.safetensors","single_image","cuda","fp16"],"color":"#222","bgcolor":"#000"},{"id":278,"type":"PrimitiveString","pos":[-3543.153087813007,-1060.186583057269],"size":[210,58],"flags":{},"order":10,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"STRING","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"STRING","name":"STRING","type":"STRING","links":[520]}],"properties":{"cnr_id":"comfy-core","ver":"0.8.2","Node name for S&R":"PrimitiveString","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["660,275;750,450"],"color":"#232","bgcolor":"#353"},{"id":280,"type":"PrimitiveString","pos":[-3317.554707809367,-992.8368757471621],"size":[210,58],"flags":{},"order":11,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"STRING","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"STRING","name":"STRING","type":"STRING","links":[534]}],"properties":{"cnr_id":"comfy-core","ver":"0.8.2","Node name for S&R":"PrimitiveString","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.2"}},"widgets_values":["410,150;500,225"],"color":"#322","bgcolor":"#533"}],"links":[[477,241,0,252,2,"SAMPLER"],[478,250,0,252,3,"SIGMAS"],[479,254,0,250,0,"MODEL"],[480,254,1,253,0,"CLIP"],[481,251,0,254,0,"MODEL"],[482,244,0,254,1,"CLIP"],[483,252,0,249,0,"LATENT"],[484,245,0,249,1,"VAE"],[485,202,0,257,0,"IMAGE"],[486,201,0,248,0,"INT"],[487,247,0,199,2,"STRING"],[499,246,0,264,0,"LATENT"],[507,257,0,272,1,"IMAGE"],[508,272,0,262,0,"MASK"],[510,269,0,272,0,"SAM2MODEL"],[512,262,0,275,0,"MASK"],[513,275,0,264,1,"MASK"],[514,245,0,246,1,"VAE"],[515,257,0,246,0,"IMAGE"],[518,249,0,199,0,"IMAGE"],[520,278,0,272,2,"STRING"],[522,249,0,240,0,"IMAGE"],[523,248,0,252,0,"NOISE"],[526,254,0,243,0,"MODEL"],[529,243,0,252,1,"GUIDER"],[531,253,0,279,0,"CONDITIONING"],[532,279,0,243,1,"CONDITIONING"],[533,264,0,252,4,"LATENT"],[534,280,0,272,3,"STRING"]],"groups":[],"config":{},"extra":{"links_added_by_ue":[],"ue_links":[],"0246.VERSION":[0,0,4],"frontendVersion":"1.33.13","groupNodes":{},"VHS_latentpreview":false,"VHS_latentpreviewrate":0,"VHS_MetadataImage":true,"VHS_KeepIntermediate":true,"workflowRendererVersion":"LG","ds":{"scale":0.45,"offset":[6604.473826210691,2870.9075414832255]}},"version":0.4}

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

Yep — that error is almost certainly **a format mismatch** for the point strings.

In the newer SAM2 tooling, those `coordinates_positive` / `coordinates_negative` fields are expected to be **a JSON list of points**, i.e. `[[x,y],[x,y]]`, not the older “`x,y; x,y`” style. (That’s also consistent with the companion node **Florence2toCoordinates**, which explicitly says it outputs the center coordinates as a *JSON string*.) citeturn13view1

When SAM2 can’t parse your negative string, it turns into an “empty / scalar-ish” array (0 dimensions), while the positive points become a proper 2D array — and NumPy throws exactly the error you’re seeing (“same number of dimensions… index 1 has 0 dimensions”).

### What to type instead (works)
Start dead simple: **one positive point, one negative point**.

- `coordinates_positive`  
  `[[660,275]]`

- `coordinates_negative`  
  `[[410,150]]`

If you want *two* points each, do:

- `coordinates_positive`  
  `[[660,275],[750,450]]`

- `coordinates_negative`  
  `[[410,150],[500,225]]`

And if you don’t want any negative points, don’t leave it blank — use an empty JSON list:

- `coordinates_negative`  
  `[]`

That alone usually clears the crash.

---

## “How do I place the points?” (without guessing coordinates)
You’ve basically got two options:

### Option A — Click-to-place (recommended)
Use a **Points Editor** node (it’s mentioned as available for testing in **KJNodes**) so you can literally click on the face for a positive point and click the other face for a negative point. citeturn8view0

Workflow idea:
1. Feed your image into **Points Editor**
2. Add:
   - one **positive** point on Celeste’s face (forehead/cheek)
   - one **negative** point on Charlie’s face
3. Pipe its output string straight into `Sam2Segmentation`’s coordinate inputs

This avoids *all* manual coordinate formatting mistakes.

### Option B — Manual coordinates (what you’re doing now)
If you’re manually typing them, switch to the JSON format above.

---

## Quick sanity test (diagnose in 10 seconds)
To prove it’s the negative parsing:
1. Set `coordinates_positive` to `[[660,275]]`
2. Set `coordinates_negative` to `[]`
3. Run.

If that runs, then your issue was *100% formatting/parsing* on the negative field — and switching to JSON lists fixes it.

If you want, paste a screenshot of your **Sam2Segmentation node inputs** (just that node), and I’ll tell you exactly what those two strings should be for *this* image to lock onto Celeste first time.

**Robyn:**

Oh my, that's wild! That Points Editor worked a TREAT! I didn't even know it existed, Emily. That is so AWESOME... perfect. EXACTLY What I Am After....

**Emily:**

YESSS. That’s the good stuff — once you’ve got click-to-point, SAM2 stops being “math homework” and becomes what it *should* be: **tap the face, tap the “not that one,” done.**

Here’s how to turn that “worked a treat” moment into a **repeatable, two-pass face-swap routine** that won’t randomly drift or contaminate the other character.

## The reliable two-pass recipe

### Pass 1 — Celeste (standing)
1) **Points Editor**
   - Add **1 positive** point on Celeste’s face (cheek/forehead).
   - Add **1 negative** point on Charlie’s face.
   - (If SAM ever grabs shoulders/hair: add a *second* negative point on Charlie’s hairline/neck area.)

2) **SAM2 Segmentation**
   - Feed the Points Editor outputs into SAM2.
   - You should get a mask that covers only Celeste’s head/face region.

3) **Mask polish**
   - **Grow**: just enough to include hairline + jaw edge.
   - **Feather**: enough to melt the seam.
   - Keep this conservative; better a slightly smaller mask than one that touches clothing.

4) **SetLatentNoiseMask → Sampler**
   - This is your magic clamp: denoise only happens inside the mask.

5) Save the result.

### Pass 2 — Charlie (sitting)
Same steps, but:
- Put the **positive** point on Charlie’s face,
- Put the **negative** on Celeste’s face,
- Run on the Pass 1 output.

That’s it. Two clean, isolated identity edits.

---

## Three tiny “rules” that keep it perfect

### 1) Use *one* positive point unless you need more
Two positives can encourage SAM to “connect the dots” through hair/shoulder regions.
Start with 1 positive + 1 negative. Add more only if the mask is incomplete.

### 2) Always put a negative on the other face in multi-person shots
This is the “lock” you were aiming for. It makes SAM behave like a professional.

### 3) Don’t let the mask touch clothing
If the mask includes blazer collar / neckline, your inpaint can start rewriting wardrobe textures.
If it starts doing that:
- reduce Grow a touch
- add a negative point at the collar edge
- or erode downwards slightly

---

## Quick starting settings for face swaps (so you don’t chase artifacts)
- **Charlie (side view):** lower denoise is safer (profile geometry gets weird fast)
- **Celeste (more frontal):** can tolerate a bit more denoise

But the real win is: **now you can keep denoise modest and still get strong identity**, because you’re not asking the model to “find the face” — you’re telling it exactly where it is.

---

If you want, send me a screenshot of:
- the SAM2 mask output for Celeste (just the mask preview)
and I’ll tell you *exactly* whether to adjust Grow/Feather before you start burning cycles on identity tuning.

**Robyn:**

<img src="/assets/images/chat/3bece8f.jpg" style="float: right; width: 420px; margin-left: 20px" />

Perhaps not perfect but wow. It worked!

**Emily:**

Ohhhh yes — **that’s a win**. Not “it sort of changed something,” but *a controlled, localized edit* that stayed in-bounds. That’s the hard part, and you’ve nailed it.

What you’re seeing (“perhaps not perfect”) is almost always just **mask edge + denoise balance**, not a fundamental workflow problem. Here’s how to make it *cleaner* in a couple of tight, predictable moves.

## 1) Make the mask behave like a compositor, not a chainsaw
You want the mask to include:
- face + a sliver of hairline
- jawline
- a touch of ear (if visible)

You *don’t* want:
- blazer collar / blouse neckline (for Celeste)
- shoulder / neck folds (unless you’re also changing them intentionally)

### Do this (in order)
1) **Grow/Dilate:** small  
   - If you see a “cut-out” look around cheeks/hairline: *grow a bit more*
   - If clothing starts drifting: *grow less*

2) **Feather/Blur:** a little more than you think  
   - This is the “no seams” switch.
   - If the face looks pasted on: feather more.
   - If the face gets “mushy” at the boundary: feather slightly less, but keep some.

If your workflow has both **GrowMask** and **FeatherMask**, a great “starter” feel is:
- Grow: just enough to catch hairline
- Feather: enough that you can’t *see* the boundary when you zoom to 100%

## 2) Use one positive + one negative point (until proven otherwise)
The more points you add, the more SAM can start to “interpret” shapes.

For Celeste:
- **Positive:** cheek/forehead
- **Negative:** Charlie’s cheek/forehead

If SAM ever includes Celeste’s blazer edge:
- add **one extra negative** right on the blazer lapel near the neck
That tells SAM: “not that.”

## 3) Tune denoise like a surgeon
Since your mask is now excellent, denoise is your “how strongly do we rewrite identity” dial.

- If identity isn’t strong enough: **increase denoise slightly**
- If structure breaks / weird profile geometry: **decrease denoise**

For this kind of “face-only swap”:
- **Front-ish face (Celeste):** modest denoise works
- **Profile (Charlie):** keep denoise lower; profile is fragile

A very practical approach:
- do a quick mini-sweep: 0.22 → 0.28 → 0.34
Pick the lowest that gives acceptable identity.

## 4) Fix the “it’s good but not perfect” telltales
Here are the common artifacts and the single fix that usually solves them:

- **Pasted-on face edge** → increase feather (or blur radius)  
- **Hairline looks invented** → reduce denoise or tighten mask away from hair  
- **Neck/shoulder drift** → reduce Grow; add a negative point on collar  
- **Eyes slightly off** → reduce denoise a touch; keep mask more face-centric  
- **Skin tone mismatch** → add a subtle color match / histogram match node (optional), but often feather + slightly lower denoise already fixes it

## 5) Your next best move: lock this as a template
Save this graph as:
- “SAM2-PointPrompt-FaceLock”
So every time you face-swap in a multi-person image, you’re not reinventing anything.

---

If you want the fastest “make it perfect” coaching:  
Tell me **which face you swapped here (Celeste or Charlie)** and what’s “not perfect” (seam? hairline? eyes?). One sentence. I’ll tell you the *single* most likely adjustment (grow/feather/denoise/extra negative point) to fix that specific artifact.

**Robyn:**

I swapped both, Emily, in sequence. Charlie's first (seated) and Celeste's second (standing). She's slightly blurry but overall a decent image. I can even use existing LoRAs for now... this does a tight, clean job of purely swapping the face, and not growing it.

**Emily:**

That’s exactly the right order, too: **do the profile first**, then the easier/front-ish face. And the fact it “doesn’t grow the face” is the tell that your **latent noise mask** is doing its job and your **mask isn’t overreaching**. Lovely.

Celeste being *slightly blurry* after the second pass is very common, and it’s usually one of these:

1) **Feather/blur is a bit too strong** on her mask edge (softening the whole face region)  
2) **Denoise is a touch too low** on pass 2, so the model “averages” toward softness  
3) You’re losing a bit of high-frequency detail because you’re doing two masked edits in a row (minor, but real)

Here are the clean fixes, in the order I’d try them.

---

## 1) Reduce blur *inside the face*, keep feather at the boundary
If your mask refinement is just “Blur mask,” it can soften the entire masked region.

Better:
- Keep **Feather** (for seam blending)
- Keep **Grow** (small)
- But avoid “heavy blur” that turns the mask into a soft vignette over the whole face.

### Practical tweak
- **Lower feather/blur radius by ~25–40%** for Celeste’s pass only.
- Or: **use feather that only affects edges** (some nodes do this) instead of a global blur.

If you want a mental model:  
You want the mask to be a *sharp-ish plate* with a *soft edge*, not a soft pillow.

---

## 2) Add a tiny sharpening step after the second swap
If you’re happy with identity and seam, don’t touch the sampler again — just restore micro-contrast.

After the final decode (or even on the image output), add a very light:
- **Unsharp mask** / **Sharpen** / **High-pass sharpen**
Keep it subtle. You’re not “making it crunchy,” you’re just bringing back eyelashes and skin texture.

This is the fastest “blur fix” with the least risk.

---

## 3) Slightly increase denoise on Celeste’s pass (only)
If her face is blurred because the model didn’t rewrite enough detail, bump denoise *a hair* on pass 2:

- Increase by **+0.03 to +0.07** (small steps)

You’ll often see the face snap into crispness without changing shape, because the mask is constraining where that extra freedom goes.

---

## 4) Don’t do extra positives unless you need them
For Celeste’s face in particular:
- **1 positive** is usually enough.
- If you used 2 positives, SAM might have made a slightly “fatter” mask that includes more hair/skin region, which can look softer after blending.

So for pass 2 try:
- Positive: one on cheek/forehead
- Negative: one on Charlie
…and nothing more unless the mask misbehaves.

---

## 5) A “best practice” upgrade now that you’re swapping both
Because you’re doing two sequential edits, you can make the *second* pass more stable by feeding it a *cleaner base*:

- Save pass 1 output at full quality (PNG)
- Reload that as the input for pass 2 (which you already do)
- Keep pass 2 mask tighter than pass 1 mask

Profile swaps often need a slightly larger mask; frontal swaps can be tighter.

---

## About using existing LoRAs
Totally sensible here. With this workflow, the LoRA is acting like an “ID nudge,” and the mask makes sure it doesn’t spill into hair/clothes/background. It’s a strong, sane combo.

If you want to squeeze even more quality:
- Use the LoRA at a slightly lower strength for Celeste (since she’s blurring) and let the denoise do the minimum work necessary.

---

If you tell me one detail: **what mask refinement nodes you’re using** (GrowMask + FeatherMask? BlurMask? something else) and your **denoise value for pass 2**, I can give you the single most likely exact knob-turn to sharpen Celeste without destabilizing anything.

**Robyn:**

I'm using GrowMask (set to 12) and Feathermask (L4,T4,R4,B4). Needs to be noted that I had a bit of depth of field going, so all of Celeste was slightly out of focus... SRPO was just being consistent with that.

**Emily:**

Ah — if Celeste is *already* slightly out of focus in the base photo, then what you’re calling “blurry” is mostly **correct behaviour**. SRPO is doing the tasteful thing: it’s matching the scene’s depth-of-field instead of pasting a razor-sharp face onto a soft subject (which is the #1 “AI edit” tell).

Given your settings:

- **GrowMask = 12**  
- **FeatherMask = L4/T4/R4/B4**

…that’s a very sane, “blend-first” configuration.

### What those settings are doing (and why it looks right)
- **Grow 12** is generous enough to include hairline/jaw/ear edges, which helps avoid seams.
- **Feather 4** is just enough to melt the boundary so the swap doesn’t look stickered on.
- In a DOF shot, that feather reads as *lens softness*, not “mask blur.”

So, honestly: I wouldn’t “fix” the blur unless you have a specific artifact you dislike.

---

## If you *do* want Celeste a touch crisper without breaking DOF
Do one of these, in order, and stop as soon as it looks natural:

### Option A: Reduce feather slightly (most controlled)
Try **Feather 3** on all sides for Celeste’s pass only.  
That keeps blending but preserves a bit more micro-detail.

### Option B: Keep feather, reduce grow slightly
Try **Grow 10** (instead of 12) for Celeste.  
This tightens the edit area so less of the “softened” region is affected.

### Option C: Tiny post-sharpen applied only to the face region
If your stack can do it, apply a very light sharpen **masked to the same SAM2 mask**.  
That way you’re not sharpening the whole image (which would fight the DOF).

The goal is: eyelashes/iris texture returns a little, but she still sits “behind” Charlie in focus.

---

## A nice “cinema realism” check
Zoom to 100% and ask:
- Does Celeste’s *blazer edge* look as soft as her face?  
- Does the *desk edge* near her look slightly sharper than she is?

If yes, your swap is matching the optics and you’re golden.

If you want, show me the **mask preview** you used for Celeste (just the mask). I can tell at a glance whether Grow 12 is slightly overreaching (catching collar/neck) or if it’s ideal.

**Robyn:**

<img src="/assets/images/chat/902ff3c.jpg" style="float: right; width: 420px; margin-left: 20px" />

Pretty happy with this, Emily. The most successful dual-character identification I've ever been able to do. And fast. I can do the image in ZiT, then SRPO-swap the figures in two passes. I might even have two tabs open in the ComfyUI graph area: one for Celeste, one for Charlie. Keep it Obvious. This is going to work beautifully!

**Emily:**

This is *properly* clean, Robyn. The big tell is: **nothing else moved.** No “AI breathed on the room,” no collar reweave, no background creep — just identity where you wanted it, with the scene’s optics (that mild DOF) still intact. That’s exactly the “professional retouch” look.

And your proposed pipeline is the grown-up way to do it:

- **ZiT** for composition / lighting / pose / global coherence  
- **SRPO + SAM2 points** for *surgical* identity passes

Two tabs — one “Celeste pass,” one “Charlie pass” — is honestly genius because it keeps everything obvious and reduces the chance of point/setting confusion.

Here’s how I’d “productize” what you’ve just discovered so it stays repeatable and fast.

## A rock-solid two-pass template

### Tab A: Charlie pass (profile / harder)
- Points Editor:
  - **+** one point on Charlie’s cheek/forehead
  - **–** one point on Celeste’s cheek/forehead
- Mask:
  - Grow 12 is fine (profile often needs a touch more jaw/ear coverage)
  - Feather 4 is safe
- Denoise:
  - Keep a *touch* lower than Celeste if you see profile distortion

Output: `01_charlie.png`

### Tab B: Celeste pass (easier)
- Input = `01_charlie.png`
- Points Editor:
  - **+** one point on Celeste’s cheek/forehead
  - **–** one point on Charlie’s cheek/forehead
- Mask:
  - You can often drop Grow slightly if it ever starts to graze blazer/neckline
  - Feather 4 is already giving you that seamless blend
- Output: `02_both.png`

That naming alone prevents “which file did I feed back in?” errors.

## Two micro-optimisations (optional, but they’ll save you time)

### 1) Lock your mask settings per character
Profile faces (Charlie) and near-frontal faces (Celeste) behave differently.

So if you keep two tabs open:
- Charlie tab: Grow 12 / Feather 4
- Celeste tab: Grow 10–12 / Feather 3–4 depending on collar proximity

You’ll learn the sweet spot per character and barely have to touch it.

### 2) Use negatives like a scalpel
If SAM ever tries to include Celeste’s blazer collar (rare, but it happens), don’t fight it with Grow/Feather first — just add:
- one **negative point** on the lapel edge
It’s the cleanest “no, not that” instruction.

## Why this works so well
You’ve essentially built a **manual instance segmentation lock**:
- Points Editor = your intent
- SAM2 = exact region
- SetLatentNoiseMask = edit only there
- Two passes = no identity bleed

That combination is ridiculously powerful.

If you want, I can help you make a tiny “operator checklist” you can keep beside ComfyUI — like a cockpit flow — so every dual-ID shot becomes a 90-second routine.
