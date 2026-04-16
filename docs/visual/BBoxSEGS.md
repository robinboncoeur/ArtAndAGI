# Consistent Characters

<hr style="height:4px;border-width:0;color:pink;background-color:pink">




## BBox-SAM2

<img src="/assets/images/notes26a/260101a.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Good morning, Emily. I'm ready to tackle that bbox/SAM face swap workflow. In this picture I have 2 characters: one standing, and one sitting. Standing is Celeste, sitting is Charlie. I hope to be able to assign faces to the, using image to image... it can be done in separate instances (not all at once). Doable?

---

[Emily]  
Yes — absolutely doable, **and doing it in two separate passes is the *right* way** for this image.

You’ve basically got two problems to solve cleanly:

1. **Isolate only the correct person’s face/head** (standing Celeste vs sitting Charlie)
2. **Apply an ID/face swap only inside that mask**, while the rest of the frame remains frozen

A bbox→SAM pipeline is ideal here because the scene is busy and you *don’t* want a global face detector to “helpfully” touch both people.

Below is a practical ComfyUI approach that works whether you’re doing classic SDXL inpaint, Flux/“edit” style, or any other img2img method that respects a mask.

---

### The core plan 
(two passes)


---
1) Swap **Celeste (standing)**

* Detect bboxes (you should get 2 persons, or 2 faces)
* Pick the bbox that corresponds to the **standing figure** (upper-left / behind)
* Use that bbox as the prompt box for **SAM** → get a clean mask
* Inpaint / face-swap only inside that mask
* Save the result


---
2) Swap **Charlie (sitting)**

* Feed Pass 1’s output back in as the new input image
* Repeat bbox → select the **sitting figure** (right/front)
* SAM mask → inpaint / face-swap
* Done

This avoids cross-contamination where your “Celeste face” embedding accidentally leaks into Charlie’s face region (or vice versa).

---

### Masking setup (bbox → SAM)


---
1) Detection node options

Pick **one** detector strategy:

**Option A (usually easiest): Person detector**

* Pros: reliable when faces are partly angled, hair covers cheeks, etc.
* Cons: bbox is larger, so SAM may segment more than you want (shoulders).

Use:

* **Ultralytics Detector Provider (BBOX)** → model: `yolov8 person` (or similar)
* Output: list of bboxes (should be 2 here)

**Option B (more precise): Face detector**

* Pros: bbox is tight on the head/face; SAM segmentation is cleaner
* Cons: profile/angle can sometimes miss (but your sitting person is very detectable).

Use:

* Ultralytics / face bbox model (whatever you’ve got installed that’s stable)

**In *this* image:** I’d start with **face bboxes** if available; otherwise person bboxes are fine.


---
2) Selecting the correct bbox

You’ll get two boxes. You need a deterministic way to select them.

Common approaches in ComfyUI graphs:

* **BBox Selector** (choose by index)
* **Sort bboxes** by X position (leftmost vs rightmost)
* **Sort by Y position** (topmost vs bottommost)
* **Preview bboxes** and pick index manually

For this specific frame:

* **Celeste (standing)** = more **left** and more **top**
* **Charlie (sitting)** = more **right** and more **center/bottom**

So you can do something like:

* Sort by **X center**:

  * leftmost bbox → Celeste
  * rightmost bbox → Charlie

That tends to be stable.


---
3) Feeding bbox to SAM

Use a SAM box-prompt workflow:

* **SAM Model Loader**
* **SAM Predictor (Box Prompt)** (naming varies by node pack)

  * Inputs: image + bbox
  * Output: mask

Then add **mask refinement**:

* **Dilate/Erode** (tiny amounts)

  * For face swap: dilate slightly so you include edges cleanly
* **Feather / Blur mask edge** (important)

  * This is what stops the “sticker face” seam

**Rule of thumb for face/head work:**

* Dilate: small
* Feather: moderate
  You want the mask to include a bit of hairline/cheek edge, but not the blazer or background.

---

### Apply the face swap
(**METHODS** inside the mask)

There are two broad ways people do this in ComfyUI:


---
1) Inpaint with an identity condition (most controllable)

You use your preferred identity driver:

* InstantID / FaceID / IP-Adapter FaceID / InsightFace embedding
  …and run an **inpaint KSampler** with the SAM mask.

**Why this is great:** the mask clamps the effect.

**Suggested settings (starting points):**

* Denoise: **0.30–0.55**

  * Lower = preserves lighting/structure, less chance of “new person”
* Steps: **12–24** (depending on model; ZiT can go lower)
* CFG:

  * SDXL-style: moderate
  * ZiT-style: you already know the drill (often **~1.6–2.2** behaves)

**Prompt discipline matters** (keep it boring):

* Positive: “same scene, same lighting, same pose, natural skin texture, realistic”
* Add one instruction: “replace only the face of the standing woman” (or sitting girl)
* Negative: “extra face, double face, deformed eyes, age change, makeup change, smile”

If you’re using a strong identity injector, you often need *less* prompt, not more.


---
2) A dedicated face-swap node, then composite with the SAM mask

Some workflows do:

* face swap tool runs on whole image (or face crop)
* then **composite output back** into the original using the SAM mask

This can work well if your swapper is very good, but it’s more fiddly with blending and color matching.

If you tell me which swapper you’re using (ReActor? InsightFace swap? something else?), I can steer you to the cleanest variant.

---

### Practical “gotchas”
for *this* image (so you don’t waste hours)


---
1) The sitting face is a **side profile**

Side profiles can cause:

* eye/eyelash distortions
* nose bridge “rebuilds”
* mouth corner weirdness

Fix: keep denoise lower (**0.30–0.40**) on Charlie’s pass, and make the mask a touch tighter to the face (less cheek/ear area).


---
2) Hairline continuity is everything

If your mask cuts across the hairline sharply, you’ll get the “helmet seam.”

Fix:

* Expand mask slightly into hairline
* Feather edge more than you think you need
* Don’t let the model “invent” new hair — keep denoise moderate


---
3) Don’t let the standing person’s blazer get included

If SAM grabs blazer/neckline, you’ll suddenly get clothing drift.

Fix:

* After SAM, do a quick **mask intersection** with a tighter ellipse/circle around the face/head, or erode downward.

---

### What I’d build
as a clean node stack (conceptual)

For each pass:

1. **Load Image** (original for Pass 1; Pass 1 output for Pass 2)
2. **Ultralytics BBOX detect** (person or face)
3. **BBox sort/select** (left/top = Celeste; right = Charlie)
4. **SAM box-prompt → mask**
5. **Mask refine** (dilate + feather)
6. **Identity condition** (your face reference image → embedding/InstantID/etc.)
7. **Inpaint KSampler** (masked)
8. **Save Image**

---

### Quick sanity check
on “separate instances”

Doing them separately is not just doable — it’s best practice:

* You keep each identity injection “pure”
* You only debug one mask at a time
* You can tune denoise differently for each face (you’ll want that here)

---

If you tell me **which exact nodes you’re using for identity** (InstantID? IPAdapter FaceID? ReActor? something Flux-specific like Kontext/Qwen edit?), I’ll translate the above into a **literal node-by-node recipe** with the best parameter starting points for that stack — and a reliable bbox selection trick so Celeste/Charlie never get swapped accidentally.


<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## SRPO-FaceOnly

<img src="/assets/images/notes26a/N260116ab.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
I'll do better... I'll send you a workflow that works well for even side view face swaps. I just need it modifying to include the missing nodes for bbox/SAM and how they are connected.

---

[Emily]  
Perfect — I’ve opened your workflow and it’s *exactly* the kind of graph that’s easy to “surgically” upgrade with bbox→SAM, because you already have the cleanest place to inject a mask: **right before the sampler**.

Here’s the key observation from your JSON:

* Inside the **SRPO-FaceOnly** subgraph, you do:

  * **ImageScaleToTotalPixels (230)** → **VAEEncode (227)** → **SamplerCustomAdvanced (228)**
* That means this is classic img2img in latent space, and the correct “face-only” way to clamp edits is:

✅ **Use a mask-driven latent noise mask** (so denoise only happens in the face region)

So we add **bbox → SAM → mask refine → SetLatentNoiseMask**, then feed that masked latent into your existing sampler.

I’ll describe it in two layers:

1. **Where to insert it in *your* exact graph** (by node ID)
2. **What nodes to add and how to connect them** (so you can drop in the versions you already have installed)

Also: here’s the workflow you sent, for reference: 


---
1) Where this goes in your existing SRPO-FaceOnly subgraph

_
* Current chain (important part)

Inside `SRPO-FaceOnly` (the subgraph embedded in node **234** at top level):

* **230 ImageScaleToTotalPixels** → outputs `IMAGE`
* **227 VAEEncode** takes that `IMAGE` → outputs `LATENT`
* **228 SamplerCustomAdvanced** takes that `LATENT` as `latent_image`

_
* We will change exactly one link

Right now you have:

* **227 (LATENT)** → **228 (latent_image)**

We will replace it with:

* **227 (LATENT)** → **NEW: SetLatentNoiseMask** → **228 (latent_image)**

Everything else in your sampler stack stays untouched.


---
2) The bbox/SAM block you add (and how it connects)

_
* The “golden rule” for alignment

Your detector + SAM must see the **same image** that gets encoded into latent.

In your workflow, that’s the output of:

✅ **230 ImageScaleToTotalPixels**

So we branch **230’s IMAGE output** into the bbox/SAM chain.


---
3) Node-by-node wiring (the exact connections)

I’m going to name the nodes generically because node pack naming differs, but the sockets are consistent.


_
A) BBOX detection (person or face)

**Input:**

* `IMAGE` = output of **230 ImageScaleToTotalPixels**

**Output:**

* some form of `BBOXES` / `DETECTIONS`

Typical nodes you might already have (based on your earlier mentions):

* **Ultralytics Detector Provider (BBOX)** (loads model)
* **Ultralytics Detector (BBOX)** (runs inference)

**Connections:**

* `230:IMAGE` → `BBOX Detector:image`

> If you have both *person* and *face* models available:
>
> * Use *face* bbox for tighter SAM masks
> * Use *person* bbox if face detection ever misses (profiles sometimes do)


-
B) Select which bbox (standing Celeste vs sitting Charlie)

Add a selector node that lets you choose a specific detection:

* **BBox Select / Choose Detection by Index**

Add a simple **PrimitiveInt** called something like:

* `bbox_index`

**Connections:**

* `BBOX Detector:bboxes` → `BBox Select:bboxes`
* `PrimitiveInt(bbox_index)` → `BBox Select:index`

**How you’ll use it:**

* Run once and see which index corresponds to which person.
* In this scene, very often:

  * index 0 = left/top (standing Celeste)
  * index 1 = right/front (sitting Charlie)
    …but that depends on the detector’s ordering, so treat it as “discover once, then lock it”.


-
C) SAM: box-prompt segmentation → face/head mask

You want the SAM node variant that supports **box prompt** (not points).

Nodes commonly look like:

* **SAM Model Loader**
* **SAM Predictor (Box Prompt)** or **Segment Anything (Box)**

**Connections:**

* `230:IMAGE` → `SAM:image`
* `BBox Select:bbox` → `SAM:box` (or `bbox`, `rect`, etc.)
* `SAM Loader:model` → `SAM:model`

**Output you want:**

* `MASK` (best)
  or `IMAGE` mask (common) → then convert to `MASK`

If SAM outputs an image, add:

* **Image to Mask** / **Mask from Image**
  and connect:
* `SAM:mask_image` → `ImageToMask:image` → outputs `MASK`


-
D) Mask refinement (this is what makes it look *real*)

Add, in this order:

1. **Dilate/Erode** (or “Grow/Shrink Mask”)

   * Slight **dilate** helps include hairline/cheek edge
2. **Feather / Blur Mask**

   * This prevents the “sticker seam”

**Connections:**

* `SAM:MASK` → `DilateErode:mask`
* `DilateErode:mask` → `MaskBlur/Feather:mask`

Optional but very useful:

* **Invert Mask** (only if your mask is backwards)
* **Mask Clamp/Threshold** (only if SAM output is “gray and mushy”)


-
E) Convert refined face mask into a latent noise mask

Now the crucial “ComfyUI-native” trick:

Use:

* **SetLatentNoiseMask**

**Connections:**

* `227:LATENT` → `SetLatentNoiseMask:latents`
* `RefinedMask:MASK` → `SetLatentNoiseMask:mask`
* `SetLatentNoiseMask:LATENT` → `228:latent_image`

That’s it. Your sampler will now denoise **only inside the mask**, using the same denoise value you already drive into the scheduler.


---
4) Exactly what to do for your two-person shot (two passes)


_
Pass 1: Celeste (standing)

* Set `bbox_index` to whichever box is the standing woman
* Run
* Save


_
Pass 2: Charlie (sitting)

* Use the Pass 1 output as the new input image
* Change `bbox_index` to the other person
* Run
* Save

This is the cleanest way to prevent identity bleed between the two faces.


---
5) Two small parameter notes (specific to your SRPO setup)

_
Your denoise is currently **0.15**

That’s great for subtle edits, but face swaps sometimes need a little more freedom *inside the face region*.

Because you’re masking now, you can safely try:

* **0.22–0.35** for Charlie (profile face usually needs more)
* **0.18–0.28** for Celeste (front-ish tends to behave)

_
Mask edge quality matters more than steps

With a good feathered mask, you’ll get away with lower steps and keep lighting consistent.


---
6) If you want, I can produce a patched JSON — but I need one thing from your node list

I *can* generate a ready-to-import `.json` that adds the nodes and rewires **227 → SetLatentNoiseMask → 228**, but ComfyUI graphs are picky: the node **type strings** must match *your* installed node pack names exactly.

So: tell me which SAM + bbox node pack you’re using (just the node names as they appear in your right-click menu), e.g.:

* “Ultralytics Detector Provider (BBOX)” exact name ✔
* The exact SAM nodes you use (e.g. “SAMLoader”, “SAMAutoMask”, “ImpactSAM”, etc.)

Once I’ve got those exact node names, I can write you a patched workflow file that drops straight in.

For now, the wiring above is 1:1 compatible with your workflow structure and uses the correct insertion point that your graph already sets up.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## 1st Patch

<img src="/assets/images/notes26a/N260116ac.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
I'm already lost at 3). Actually, if you send me a .json with what YOU would normally recommend and if I don't actually have a particular node (set) installed, ComfyUI will do it for me. Would that work for you?

---

[Emily]  
Yep — I can send you a patched `.json` **right now**. One important correction first though:

**ComfyUI will *not* auto-install missing custom nodes.**
What it *will* do is import the workflow and show the missing nodes in red, so you can then install the required node packs and everything will snap into place.

That said: I’ve made you a patched version of your workflow that adds a **bbox → SAM → refined mask → SetLatentNoiseMask** block *inside* your `SRPO-FaceOnly` subgraph, and rewires the sampler so it only denoises inside the SAM mask.

### ✅ Download
the patched workflow

[Download ZZ_SRPO-FaceOnly_BBOX-SAM_PATCHED.json](sandbox:/mnt/data/ZZ_SRPO-FaceOnly_BBOX-SAM_PATCHED.json)

---

### What I changed
(in plain English)

Inside the `SRPO-FaceOnly` subgraph:

* Your old link was: **VAEEncode (227) → SamplerCustomAdvanced (228)**
* I replaced it with: **VAEEncode (227) → SetLatentNoiseMask → SamplerCustomAdvanced (228)**

And I added a new branch off the same scaled image (**ImageScaleToTotalPixels (230)**) that does:

**Ultralytics BBOX detect → select bbox by index → SAM box segment → GrowMask → MaskBlur → SetLatentNoiseMask**

So you’ll be able to:

* set `BBOX Index = 0` (say Celeste), run once
* set `BBOX Index = 1` (Charlie), run again on the output image

---

### What you’ll likely need
installed (if you see red nodes)

Because bbox + SAM are not core ComfyUI nodes, you’ll probably need:

* **Impact Pack** (commonly provides Ultralytics BBOX + SAM box prompt nodes), and/or
* **A SAM node pack** (Segment Anything nodes)

If, after importing, you see missing node types like:

* `UltralyticsDetectorProvider (BBOX)`
* `UltralyticsDetector (BBOX)`
* `BBOX Select`
* `SAMLoader`
* `SAM Segment (Box)`

…that just means your installed pack uses slightly different node names. In that case you can replace them with your equivalents (the wiring stays the same).

---

### How to use it
(two-pass, clean and safe)

1. Load your original image as usual.
2. In the SRPO-FaceOnly subgraph, find **“BBOX Index”**:

   * try `0`, run, check who got masked
   * if it’s the wrong person, change to `1`
3. When Celeste is correct, save output.
4. Feed that output back in, flip **BBOX Index** to the other value, run again.

That’s the most reliable way to keep Celeste/Charlie identities from bleeding into each other.

---

If you import it and tell me **which nodes show as missing**, I’ll immediately produce a second patched JSON that uses the *exact* node type names from *your* installed packs (so it loads perfectly with zero red nodes).

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Patch 2

<img src="/assets/images/notes26a/N260116ad.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Okay, so what I've done is un-subgraph the whole workflow. I have replaced nodes with their current iterations. The only node I cannot find is the BBOX Select (or 'Select BBOX). It simply doesn't seem to exist anywhere. I've attached the workflow for your study.

---

[Emily]  
You’re not going mad — in the workflow you attached, the “BBOX Select” problem is actually *two* things at once:

1. **You don’t have a bbox detector in this graph anymore**, so there’s no “BBOXES list” to select from.
2. The “Select BBOX” node that *is* present in the JSON is currently wired **incorrectly** (it’s literally receiving an **IMAGE** where it expects **BBOXES**). That guarantees it can’t work even if the node exists. 

So you’ve ended up at: “I need a node that doesn’t exist” — but the deeper truth is: **there’s nothing to select yet**.

### The cleanest fix
(and honestly the least confusing)

Since you already have **SAM2** installed and working, you can skip bbox selection entirely and drive SAM2 with a **single positive point** (“click here = segment this object”). This is *much* easier, and for two people it’s perfect because you’re doing two passes anyway.

I patched your workflow into a version that **removes BBOX Select completely** and runs SAM2 in **point-prompt mode**:

✅ **Download:** [SRPO-SAM2-PointPrompt-NoBBoxSelect.json](sandbox:/mnt/data/SRPO-SAM2-PointPrompt-NoBBoxSelect.json)

This file is based on your attached workflow. 

---

### How to use
the point-prompt version

1. Load the workflow.
2. Find **Sam2Segmentation**.
3. Leave the **bboxes** input disconnected (it is, in the patched file).
4. In **coordinates_positive**, type a single point:

   * Format: `x,y` (pixel coordinates)
   * **Pass A (Celeste standing):** pick a point on her face (forehead/cheek)
   * **Pass B (Charlie sitting):** pick a point on her cheek/forehead
5. Optional but helpful: put a point on the *other* person into **coordinates_negative** to stop SAM from drifting.

Everything else in your mask chain stays exactly as you already built it:
**SAM2 mask → GrowMask → FeatherMask → SetLatentNoiseMask → Sampler**

### “But how
do I get x,y?”

Any image viewer that shows pixel coordinates is fine. Two easy options:

* Open the image in an editor (Preview, GIMP, Photoshop, Krita) and read the cursor coordinates.
* Or just estimate once, run, and nudge the numbers until the mask locks onto the face (SAM2 is forgiving).

---

### If you still *want*
bbox automation later

Then you’ll need **a bbox detector node** that outputs a **BBOXES** list (Ultralytics/Impact Pack etc.), and then you can select by index.

But given you said you’re already lost at step 3 earlier: **point-prompt SAM2 is the “get it working today” path**, and it’s robust for side-profile faces.

---

If you load the patched workflow and tell me:

* “I used `x,y` = ___ and SAM grabbed the wrong person / too much hair / shoulders”
  …I’ll tell you exactly what to change (grow amount, feather, and whether to add a negative point) to make it snap tight to just the head/face.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








##

<img src="/assets/images/notes26a/N260116ae.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Actually, I'm getting the error "Cannot read properties of undefined (reading 'output') when I try to run this workflow. No node is highlighted, or outlined in green. Terminal isn't showing me anything. I'm baffled.

---

[Emily]  
That error is almost always a **broken (dangling) link ID inside the workflow JSON** — i.e. an input says “I’m connected to link #470” but link #470 doesn’t exist anymore, so the UI hits `undefined.output` and throws:

> `Cannot read properties of undefined (reading 'output')`

In the workflow you attached, that’s exactly what’s happening: several nodes have inputs pointing to link IDs that don’t exist (a common side-effect of **un-subgraphing + replacing nodes**). So ComfyUI can’t even *start* execution, and it won’t necessarily highlight anything.

### I fixed your workflow JSON

I patched your uploaded workflow to remove all dangling link references and re-wire the missing essentials:

* **RandomNoise → SamplerCustomAdvanced (noise)**
* **Lora/Model → BasicGuider (model)**
* **Text conditioning → BasicGuider (conditioning)**
* **BasicGuider → SamplerCustomAdvanced (guider)**

…and I also cleared the dead links on the “BBOX Select” node so it won’t crash even if it’s still sitting there unused.

✅ **Download the fixed workflow here:**
[SRPO-BBOX-SAM_PATCHED-1_FIXED.json](sandbox:/mnt/data/SRPO-BBOX-SAM_PATCHED-1_FIXED.json)

---

### What to do next
(so you can actually mask one face)

Since you couldn’t find a working BBOX Select anyway, just use **SAM2 point prompting** for now (it’s honestly the fastest/cleanest for two people):

1. Open the fixed workflow.
2. Go to **Sam2Segmentation**.
3. Set **coordinates_positive** to a point on the face you want (Celeste or Charlie).

   * Format is typically `x,y` in pixels.
4. (Optional) Put a point on the *other* person in **coordinates_negative**.
5. Run.
6. Flip the coordinates to the other face for pass 2.

If you tell me what the **Sam2Segmentation** node in your install expects for coordinate formatting (some use `"x,y"` strings, some use lists), I’ll give you the exact literal input format and a couple of “known good” example values.

---

If you load the fixed JSON and it still errors, paste the **browser console** error line (DevTools → Console). But in this case, the dangling-link issue was concrete and should be resolved by that fixed file.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Q]  
Actually, I found it. As you said, it was missing connections. Thanks.

---

[Emily]  
Brilliant — that lines up perfectly with that `undefined.output` error. Once a single link reference is dangling, ComfyUI can fall over *before* it can even “green-outline” a culprit.

Now that it runs, here’s the quickest way to get your **two-person, two-pass** face assignment stable (and avoid the classic “oops it drifted onto the other person”):

### Pass workflow
(repeat twice)

1. **Lock the target first**

   * If you’re using **SAM2 point prompt**: put **one positive point** dead-centre on the target face (forehead/cheek), and **one negative point** on the *other* person’s face.
   * If you’re using **bbox+SAM**: set the bbox index to the right person, then keep it fixed.

2. **Mask tuning (the 3 knobs that matter)**

   * **GrowMask**: enough to include hairline + jaw edge (small to moderate)
   * **Feather**: moderate (this hides seams)
   * If SAM ever grabs clothing/shoulder: *reduce Grow* or add a negative point lower down.

3. **Denoise discipline**

   * Side view (Charlie): start **lower** (roughly 0.25–0.35 if your stack tolerates it), because profile geometry gets weird fast.
   * More front-ish (Celeste): can go a touch higher if needed.

4. **Save output**, re-feed for pass 2, switch target, run again.

### 1 “quality of life”
suggestion

After you get a good SAM mask once, **freeze it** for that pass (don’t keep changing points/index). Do all identity tweaking with the mask held steady — it makes debugging *way* saner.

If you want, paste (or screenshot) just the mask result after you set Celeste’s target, and I’ll tell you whether to tweak **Grow** or **Feather** for the cleanest blend before you start burning time on identity tuning.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Q]  
Let's take this step by step.. on lock the target first, you said:

"If you’re using SAM2 point prompt: put one positive point dead-centre on the target face (forehead/cheek), and one negative point on the other person’s face."

How?

---

[Emily]  
Right — “how” in ComfyUI depends on **which SAM2 node you’re using**, because different node packs accept points in different formats. But the *mechanism* is always the same:

* **Positive point(s)** = “segment *this*”
* **Negative point(s)** = “definitely *not* this”

So I’ll give you the step-by-step that works for the most common SAM2 node styles, and you can match it to what you see in your node.


---
1) Find your SAM2 node and open its inputs

In your graph, click the node called something like:

* `Sam2Segmentation`
* `SAM2 Segment`
* `SegmentAnything2`
* `SAM2Predictor`

Look at the widgets/fields for points. You’ll usually see one or more of these:

* `coordinates_positive`
* `coordinates_negative`
* `positive_points`
* `negative_points`
* `points`
* `point_coords` + `point_labels`


---
2) Enter a positive point on the target face

You want **one point** roughly on the cheekbone/forehead of the face you’re editing.

### If your node
has fields like:

**`coordinates_positive`** and **`coordinates_negative`**
Then it typically wants either:

**Format A (most common):**

* `coordinates_positive`: `x,y`
* `coordinates_negative`: `x,y`

Example:

* `coordinates_positive`: `720,380`
* `coordinates_negative`: `1030,520`

**Format B (multiple points):**

* `coordinates_positive`: `x1,y1; x2,y2`
* `coordinates_negative`: `x1,y1; x2,y2`

Example:

* `coordinates_positive`: `720,380; 735,395`
* `coordinates_negative`: `1030,520`

### If your node has:

**`point_coords`** and **`point_labels`**
Then it usually wants:

* `point_coords`: a list of `[x,y]`
* `point_labels`: a list of `1` for positive and `0` for negative

Example:

* `point_coords`: `[[720,380],[1030,520]]`
* `point_labels`: `[1,0]`

(First point = positive on target face, second point = negative on the other person.)


---
3) Add a negative point on the other person’s face

Same deal: one click-point in the middle of the other face.

This is the “lock” part: it prevents SAM from deciding both faces belong to one mask.


---
4) Where do you get x,y coordinates?

You have three easy options:

_
* Option 1: Your SAM2 node has a “click to add point” UI

Some builds let you click directly in a preview window or use an “interactive” helper node.
If you see anything like:

* `Interactive SAM`
* `Click points`
* `Preview & Click`
  Use that — it’s the nicest.

_
* Option 2: Use any image editor that shows coordinates

Open the image in:

* GIMP / Krita / Photoshop
  Hover over the face → read the status bar X,Y.

_
* Option 3: Do a quick “guess and nudge”

If your image is, say, 1024×1024, start with rough positions:

* Standing face: around upper-left-ish
* Sitting face: right-ish

Run once. If the mask grabs the wrong person, move the point and rerun.
SAM2 is forgiving — you only need to be in the right region.


---
5) Sanity check (you should see this result)

After running the SAM2 node, the produced mask should:

* cover only the target head/face
* exclude the other person entirely

If it covers both, add a second negative point (one on each cheek of the other face), or move the positive point slightly more central on the target face.

---

### Fastest way
to make this 100% concrete

Tell me the **exact name of the SAM2 node** you’re using *and* paste the list of its point-related fields (just the labels you see: e.g. “coordinates_positive / coordinates_negative” or “point_coords / point_labels”). Then I’ll give you the **exact string to type** for that node format.

---

[Q]  
So, for input it wants a string. In my string for coords_pos, i've got 660,275; 750,450. for neg, i've got: 410,150; 500, 225, also as string. When I try to run this, Sam2Segmentation errors with:

all input arrays must have the same number of dimensions, but the array at index 0 has 2 dimensions and the array at index 1 has 0 dimensions. Format problem? Why is it accepting my first array and not the 2nd?


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Yep — **format problem**, and the error message tells us exactly what kind:

* Your **positive coords string** is being parsed into a proper 2-D array (something like `[[660,275],[750,450]]`) → **2 dimensions**
* Your **negative coords string** is being parsed into… nothing (empty / scalar / invalid) → effectively **0 dimensions**

So SAM2 ends up with:

* `pos_points` = array of shape `(N,2)`
* `neg_points` = “empty” (or not parsed at all)

…and it crashes because it expects both inputs to resolve to arrays with the same dimensionality.

### Why would *negative*
fail to parse when positive works?

In what you typed, you have an extra space after the comma in the second pair:

`500, 225`

Some parsers are tolerant; some are brittle and only accept `int,int` with no spaces. Also, some expect **exact separators** and will treat the whole thing as invalid if one token doesn’t match.

---

* Fix 1 (most likely): remove spaces everywhere

Try **exactly** this:

* **coords_pos**:
  `660,275;750,450`

* **coords_neg**:
  `410,150;500,225`

No spaces, no trailing semicolons.

Run again.

---

* Fix 2: match the exact delimiter it expects

Some SAM2 point-string parsers expect **pipes** or **newlines**, not semicolons.

Try these alternates if Fix 1 still errors:


---
Variant A (pipe)

* pos: `660,275|750,450`
* neg: `410,150|500,225`


---
Variant B (newline)

* pos:

```
660,275
750,450
```

* neg:

```
410,150
500,225
```

(Still as a string field — you can paste multi-line text.)

---

* Fix 3: ensure “empty” is truly empty

A bunch of SAM2 nodes treat a blank negative field as *valid*, but a malformed one as *invalid*.

So if you just want to test:

* Set **coords_neg** to **empty** (delete everything)
* Leave pos with one point only: `660,275`

If that runs, we’ve confirmed the parser is strict and the neg formatting is the only issue.

---

### One more gotcha:
positive/negative point counts sometimes must match

Some implementations (less common, but I’ve seen it) expect the same number of pos and neg points.

You currently have **2 pos** and **2 neg**, which is fine. But if you test with 1 pos and 0 neg and it fails, that’s a clue.

---

### Quick best-practice
for your use case (two people)

You don’t actually need 2 positive points most of the time.

Try:

* pos (target face): `660,275`
* neg (other face): `410,150`

That tends to “lock” faster and avoids SAM accidentally grabbing hair/clothing.

---

If you paste the **exact node name** (full title) and, if visible, any hint text under those fields (some packs show an example format), I can tell you the one correct delimiter so you don’t have to trial-and-error.


<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Space Errors?

<img src="/assets/images/notes26a/N260116af.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Removed the space. Exact same error.

---

[Emily]  
Yep — that error is almost certainly **a format mismatch** for the point strings.

In the newer SAM2 tooling, those `coordinates_positive` / `coordinates_negative` fields are expected to be **a JSON list of points**, i.e. `[[x,y],[x,y]]`, not the older “`x,y; x,y`” style. (That’s also consistent with the companion node **Florence2toCoordinates**, which explicitly says it outputs the center coordinates as a *JSON string*.) ([Instasd][1])

When SAM2 can’t parse your negative string, it turns into an “empty / scalar-ish” array (0 dimensions), while the positive points become a proper 2D array — and NumPy throws exactly the error you’re seeing (“same number of dimensions… index 1 has 0 dimensions”).

### What to type instead (works)

Start dead simple: **one positive point, one negative point**.

* `coordinates_positive`
  `[[660,275]]`

* `coordinates_negative`
  `[[410,150]]`

If you want *two* points each, do:

* `coordinates_positive`
  `[[660,275],[750,450]]`

* `coordinates_negative`
  `[[410,150],[500,225]]`

And if you don’t want any negative points, don’t leave it blank — use an empty JSON list:

* `coordinates_negative`
  `[]`

That alone usually clears the crash.

---

## “How do I place the points?” (without guessing coordinates)

You’ve basically got two options:

### Option A — Click-to-place (recommended)

Use a **Points Editor** node (it’s mentioned as available for testing in **KJNodes**) so you can literally click on the face for a positive point and click the other face for a negative point. ([Gitee][2])

Workflow idea:

1. Feed your image into **Points Editor**
2. Add:

   * one **positive** point on Celeste’s face (forehead/cheek)
   * one **negative** point on Charlie’s face
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

[1]: https://www.instasd.com/comfyui/custom-nodes/comfyui-segment-anything-2/florence2tocoordinates "Florence2toCoordinates - comfyui-segment-anything-2 Custom Node | InstaSD"
[2]: https://gitee.com/comfyui_custom_nodes/ComfyUI-segment-anything-2 "comfyui_custom_nodes/ComfyUI-segment-anything-2"

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Points Editor

<img src="/assets/images/notes26a/N260116ag.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Oh my, that's wild! That Points Editor worked a TREAT! I didn't even know it existed, Emily. That is so AWESOME... perfect. EXACTLY What I Am After....

---

[Emily]  
YESSS. That’s the good stuff — once you’ve got click-to-point, SAM2 stops being “math homework” and becomes what it *should* be: **tap the face, tap the “not that one,” done.**

Here’s how to turn that “worked a treat” moment into a **repeatable, two-pass face-swap routine** that won’t randomly drift or contaminate the other character.

## The reliable two-pass recipe

### Pass 1 — Celeste (standing)

1. **Points Editor**

   * Add **1 positive** point on Celeste’s face (cheek/forehead).
   * Add **1 negative** point on Charlie’s face.
   * (If SAM ever grabs shoulders/hair: add a *second* negative point on Charlie’s hairline/neck area.)

2. **SAM2 Segmentation**

   * Feed the Points Editor outputs into SAM2.
   * You should get a mask that covers only Celeste’s head/face region.

3. **Mask polish**

   * **Grow**: just enough to include hairline + jaw edge.
   * **Feather**: enough to melt the seam.
   * Keep this conservative; better a slightly smaller mask than one that touches clothing.

4. **SetLatentNoiseMask → Sampler**

   * This is your magic clamp: denoise only happens inside the mask.

5. Save the result.

### Pass 2 — Charlie (sitting)

Same steps, but:

* Put the **positive** point on Charlie’s face,
* Put the **negative** on Celeste’s face,
* Run on the Pass 1 output.

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

* reduce Grow a touch
* add a negative point at the collar edge
* or erode downwards slightly

---

## Quick starting settings for face swaps (so you don’t chase artifacts)

* **Charlie (side view):** lower denoise is safer (profile geometry gets weird fast)
* **Celeste (more frontal):** can tolerate a bit more denoise

But the real win is: **now you can keep denoise modest and still get strong identity**, because you’re not asking the model to “find the face” — you’re telling it exactly where it is.

---

If you want, send me a screenshot of:

* the SAM2 mask output for Celeste (just the mask preview)
  and I’ll tell you *exactly* whether to adjust Grow/Feather before you start burning cycles on identity tuning.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Example of Working

<img src="/assets/images/notes26a/260101b.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Ohhhh yes — **that’s a win**. Not “it sort of changed something,” but *a controlled, localized edit* that stayed in-bounds. That’s the hard part, and you’ve nailed it.

What you’re seeing (“perhaps not perfect”) is almost always just **mask edge + denoise balance**, not a fundamental workflow problem. Here’s how to make it *cleaner* in a couple of tight, predictable moves.

## 1) Make the mask behave like a compositor, not a chainsaw

You want the mask to include:

* face + a sliver of hairline
* jawline
* a touch of ear (if visible)

You *don’t* want:

* blazer collar / blouse neckline (for Celeste)
* shoulder / neck folds (unless you’re also changing them intentionally)

### Do this (in order)

1. **Grow/Dilate:** small

   * If you see a “cut-out” look around cheeks/hairline: *grow a bit more*
   * If clothing starts drifting: *grow less*

2. **Feather/Blur:** a little more than you think

   * This is the “no seams” switch.
   * If the face looks pasted on: feather more.
   * If the face gets “mushy” at the boundary: feather slightly less, but keep some.

If your workflow has both **GrowMask** and **FeatherMask**, a great “starter” feel is:

* Grow: just enough to catch hairline
* Feather: enough that you can’t *see* the boundary when you zoom to 100%

## 2) Use one positive + one negative point (until proven otherwise)

The more points you add, the more SAM can start to “interpret” shapes.

For Celeste:

* **Positive:** cheek/forehead
* **Negative:** Charlie’s cheek/forehead

If SAM ever includes Celeste’s blazer edge:

* add **one extra negative** right on the blazer lapel near the neck
  That tells SAM: “not that.”

## 3) Tune denoise like a surgeon

Since your mask is now excellent, denoise is your “how strongly do we rewrite identity” dial.

* If identity isn’t strong enough: **increase denoise slightly**
* If structure breaks / weird profile geometry: **decrease denoise**

For this kind of “face-only swap”:

* **Front-ish face (Celeste):** modest denoise works
* **Profile (Charlie):** keep denoise lower; profile is fragile

A very practical approach:

* do a quick mini-sweep: 0.22 → 0.28 → 0.34
  Pick the lowest that gives acceptable identity.

## 4) Fix the “it’s good but not perfect” telltales

Here are the common artifacts and the single fix that usually solves them:

* **Pasted-on face edge** → increase feather (or blur radius)
* **Hairline looks invented** → reduce denoise or tighten mask away from hair
* **Neck/shoulder drift** → reduce Grow; add a negative point on collar
* **Eyes slightly off** → reduce denoise a touch; keep mask more face-centric
* **Skin tone mismatch** → add a subtle color match / histogram match node (optional), but often feather + slightly lower denoise already fixes it

## 5) Your next best move: lock this as a template

Save this graph as:

* “SAM2-PointPrompt-FaceLock”
  So every time you face-swap in a multi-person image, you’re not reinventing anything.

---

If you want the fastest “make it perfect” coaching:
Tell me **which face you swapped here (Celeste or Charlie)** and what’s “not perfect” (seam? hairline? eyes?). One sentence. I’ll tell you the *single* most likely adjustment (grow/feather/denoise/extra negative point) to fix that specific artifact.

---

[Q]  
I swapped both, Emily, in sequence. Charlie's first (seated) and Celeste's second (standing). She's slightly blurry but overall a decent image. I can even use existing LoRAs for now... this does a tight, clean job of purely swapping the face, and not growing it. 


<hr style="height:2px;border-width:0;color:blue;background-color:blue">



[Emily]  
That’s exactly the right order, too: **do the profile first**, then the easier/front-ish face. And the fact it “doesn’t grow the face” is the tell that your **latent noise mask** is doing its job and your **mask isn’t overreaching**. Lovely.

Celeste being *slightly blurry* after the second pass is very common, and it’s usually one of these:

1. **Feather/blur is a bit too strong** on her mask edge (softening the whole face region)
2. **Denoise is a touch too low** on pass 2, so the model “averages” toward softness
3. You’re losing a bit of high-frequency detail because you’re doing two masked edits in a row (minor, but real)

Here are the clean fixes, in the order I’d try them.

---

## 1) Reduce blur *inside the face*, keep feather at the boundary

If your mask refinement is just “Blur mask,” it can soften the entire masked region.

Better:

* Keep **Feather** (for seam blending)
* Keep **Grow** (small)
* But avoid “heavy blur” that turns the mask into a soft vignette over the whole face.

### Practical tweak

* **Lower feather/blur radius by ~25–40%** for Celeste’s pass only.
* Or: **use feather that only affects edges** (some nodes do this) instead of a global blur.

If you want a mental model:
You want the mask to be a *sharp-ish plate* with a *soft edge*, not a soft pillow.

---

## 2) Add a tiny sharpening step after the second swap

If you’re happy with identity and seam, don’t touch the sampler again — just restore micro-contrast.

After the final decode (or even on the image output), add a very light:

* **Unsharp mask** / **Sharpen** / **High-pass sharpen**
  Keep it subtle. You’re not “making it crunchy,” you’re just bringing back eyelashes and skin texture.

This is the fastest “blur fix” with the least risk.

---

## 3) Slightly increase denoise on Celeste’s pass (only)

If her face is blurred because the model didn’t rewrite enough detail, bump denoise *a hair* on pass 2:

* Increase by **+0.03 to +0.07** (small steps)

You’ll often see the face snap into crispness without changing shape, because the mask is constraining where that extra freedom goes.

---

## 4) Don’t do extra positives unless you need them

For Celeste’s face in particular:

* **1 positive** is usually enough.
* If you used 2 positives, SAM might have made a slightly “fatter” mask that includes more hair/skin region, which can look softer after blending.

So for pass 2 try:

* Positive: one on cheek/forehead
* Negative: one on Charlie
  …and nothing more unless the mask misbehaves.

---

## 5) A “best practice” upgrade now that you’re swapping both

Because you’re doing two sequential edits, you can make the *second* pass more stable by feeding it a *cleaner base*:

* Save pass 1 output at full quality (PNG)
* Reload that as the input for pass 2 (which you already do)
* Keep pass 2 mask tighter than pass 1 mask

Profile swaps often need a slightly larger mask; frontal swaps can be tighter.

---

## About using existing LoRAs

Totally sensible here. With this workflow, the LoRA is acting like an “ID nudge,” and the mask makes sure it doesn’t spill into hair/clothes/background. It’s a strong, sane combo.

If you want to squeeze even more quality:

* Use the LoRA at a slightly lower strength for Celeste (since she’s blurring) and let the denoise do the minimum work necessary.

---

If you tell me one detail: **what mask refinement nodes you’re using** (GrowMask + FeatherMask? BlurMask? something else) and your **denoise value for pass 2**, I can give you the single most likely exact knob-turn to sharpen Celeste without destabilizing anything.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Tweaking

<img src="/assets/images/notes26a/N260116ai.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
I'm using GrowMask (set to 12) and Feathermask (L4,T4,R4,B4). Needs to be noted that I had a bit of depth of field going, so all of Celeste was slightly out of focus... SRPO was just being consistent with that.

---

[Emily]  
Ah — if Celeste is *already* slightly out of focus in the base photo, then what you’re calling “blurry” is mostly **correct behaviour**. SRPO is doing the tasteful thing: it’s matching the scene’s depth-of-field instead of pasting a razor-sharp face onto a soft subject (which is the #1 “AI edit” tell).

Given your settings:

* **GrowMask = 12**
* **FeatherMask = L4/T4/R4/B4**

…that’s a very sane, “blend-first” configuration.

### What those settings are doing (and why it looks right)

* **Grow 12** is generous enough to include hairline/jaw/ear edges, which helps avoid seams.
* **Feather 4** is just enough to melt the boundary so the swap doesn’t look stickered on.
* In a DOF shot, that feather reads as *lens softness*, not “mask blur.”

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

* Does Celeste’s *blazer edge* look as soft as her face?
* Does the *desk edge* near her look slightly sharper than she is?

If yes, your swap is matching the optics and you’re golden.

If you want, show me the **mask preview** you used for Celeste (just the mask). I can tell at a glance whether Grow 12 is slightly overreaching (catching collar/neck) or if it’s ideal.


<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Example C

<img src="/assets/images/notes26a/260101c.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Pretty happy with this, Emily. The most successful dual-character identification I've ever been able to do. And fast. I can do the image in ZiT, then SRPO-swap the figures in two passes. I might even have two tabs open in the ComfyUI graph area: one for Celeste, one for Charlie. Keep it Obvious. This is going to work beautifully!

---

[Emily]  
This is *properly* clean, Robyn. The big tell is: **nothing else moved.** No “AI breathed on the room,” no collar reweave, no background creep — just identity where you wanted it, with the scene’s optics (that mild DOF) still intact. That’s exactly the “professional retouch” look.

And your proposed pipeline is the grown-up way to do it:

* **ZiT** for composition / lighting / pose / global coherence
* **SRPO + SAM2 points** for *surgical* identity passes

Two tabs — one “Celeste pass,” one “Charlie pass” — is honestly genius because it keeps everything obvious and reduces the chance of point/setting confusion.

Here’s how I’d “productize” what you’ve just discovered so it stays repeatable and fast.

## A rock-solid two-pass template

### Tab A: Charlie pass (profile / harder)

* Points Editor:

  * **+** one point on Charlie’s cheek/forehead
  * **–** one point on Celeste’s cheek/forehead
* Mask:

  * Grow 12 is fine (profile often needs a touch more jaw/ear coverage)
  * Feather 4 is safe
* Denoise:

  * Keep a *touch* lower than Celeste if you see profile distortion

Output: `01_charlie.png`

### Tab B: Celeste pass (easier)

* Input = `01_charlie.png`
* Points Editor:

  * **+** one point on Celeste’s cheek/forehead
  * **–** one point on Charlie’s cheek/forehead
* Mask:

  * You can often drop Grow slightly if it ever starts to graze blazer/neckline
  * Feather 4 is already giving you that seamless blend
* Output: `02_both.png`

That naming alone prevents “which file did I feed back in?” errors.

## Two micro-optimisations (optional, but they’ll save you time)

### 1) Lock your mask settings per character

Profile faces (Charlie) and near-frontal faces (Celeste) behave differently.

So if you keep two tabs open:

* Charlie tab: Grow 12 / Feather 4
* Celeste tab: Grow 10–12 / Feather 3–4 depending on collar proximity

You’ll learn the sweet spot per character and barely have to touch it.

### 2) Use negatives like a scalpel

If SAM ever tries to include Celeste’s blazer collar (rare, but it happens), don’t fight it with Grow/Feather first — just add:

* one **negative point** on the lapel edge
  It’s the cleanest “no, not that” instruction.

## Why this works so well

You’ve essentially built a **manual instance segmentation lock**:

* Points Editor = your intent
* SAM2 = exact region
* SetLatentNoiseMask = edit only there
* Two passes = no identity bleed

That combination is ridiculously powerful.

If you want, I can help you make a tiny “operator checklist” you can keep beside ComfyUI — like a cockpit flow — so every dual-ID shot becomes a 90-second routine.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## ReVisit

<img src="/assets/images/notes26a/N260116ak.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Those first tries were amazing, Emily. But now, not so much. The face keeps shifting around. I really think I need to 1) get a precise fix on the face, only the face. The Points Editor node is too inexact.

---

[Emily]  
Ahhh — I know *exactly* what you’re describing 😅: the swap “works” once, then the face starts **wandering / reshaping / drifting**, and you feel like you’ve lost the lock.

That almost always comes from one of these (and you can fix all of them):

## Why the face starts shifting around

### 1) Your points are landing on a *different* image than the one SAM2 sees

This is the #1 culprit.

If your workflow does **any resize / crop / scale** *between*:

* the image you click in **Points Editor**
  and
* the image that goes into **Sam2Segmentation**

…then your coordinates no longer correspond. The mask will “hit” a slightly different place each run, which looks like the face is sliding.

✅ Fix: **Points Editor must receive the exact same image tensor that feeds SAM2.**
No intermediate scaling. No different branch.

A really common gotcha is:

* you click on the *original* image,
* but SAM2 receives a *scaled* image (ImageScaleToTotalPixels, etc.).

---

### 2) SAM2 is segmenting “head” not “face”

Even with correct points, SAM loves grabbing hairline/ear/neck, and then your inpaint/swap has more freedom than you want → the “face shifts.”

✅ Fix: make the mask **face-only**, not head-only.

---

## What you want instead: a *precise face-only lock*

Here are three ways, from easiest to most “surgical.” Pick the first that fits your installed nodes.

---

# Option A (best balance): **Face bbox → SAM2 box → face-only trim**

Instead of clicking points, you use a **face detector bbox** (very precise), then SAM2 refines it.

**Workflow idea**

1. **Face detector** (InsightFace / MediaPipe / Ultralytics face) → outputs **bbox**
2. **SAM2 “box prompt”** using that bbox → outputs mask
3. **Erode/Shrink mask** a little so it excludes hair/neck
4. **Feather edges** lightly
5. **SetLatentNoiseMask** → swap

**Why this rocks:** the bbox is *stable* across runs, so the mask won’t “wander.”

If you don’t have “SAM2 box prompt” but you *do* have “points,” you can still use this idea by:

* placing **one positive** point on the face
* and adding **4–8 negative points** around the boundary (hairline, ear, neck, collar)
  …but the bbox method is cleaner.

---

# Option B (most precise): **Face parsing mask (skin/face)**

This is the “only the face, period” approach.

You use a face-segmentation/parsing model that outputs labels like:

* skin, lips, eyes, brows, etc.

Then you build:

* **FACE_MASK = skin + lips + eyes + brows**
  and explicitly *exclude*:
* hair, neck, ears, background

**Why this is perfect:** it literally can’t “grow” into hair or collar.

Node names vary, but look for anything like:

* “Face Parsing”
* “BiSeNet face segmentation”
* “Face mask / facial regions”

---

# Option C (bulletproof): **Crop → swap → paste back**

This is the “retoucher’s method.”

1. Detect face → crop a square around it (aligned)
2. Run your swap on the crop (fixed size, like 512×512)
3. Paste back with the mask (Poisson / seamless / feathered composite)

**Why it stops drift:** the swap happens in a fixed coordinate system, and the paste is constrained.

---

## Quick checklist to stabilise what you have *right now* (Points Editor)

Before you rebuild anything, do these two checks — they solve a shocking number of “it started drifting” cases:

### ✅ Check 1: Points Editor is connected to the SAME image input as SAM2

Literally: same wire source.

If SAM2 is fed by a scaled image, make Points Editor click on that scaled image too.

### ✅ Check 2: “Freeze the mask” while tuning

Once you get a good SAM2 mask:

* **save it** (or route it into a “Load/Save mask” pair)
* stop recomputing SAM2 every run

Then you can tune SRPO/denoise/LoRA without the segmentation changing underneath you.

---

## If you tell me one thing, I can give you the exact path

Which of these do you have installed?

* A face detector node (InsightFace / MediaPipe / Ultralytics face / FaceDetailer)?
* A SAM2 node that accepts **bbox/box prompt**, or only points?
* Any “face parsing” nodes?

Even if you don’t answer, the safest immediate move is:

✅ **Make Points Editor click the *same scaled image* that SAM2 uses + freeze the first good mask.**

That will stop the “shifting around” feeling fast.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Which Period

<img src="/assets/images/notes26a/260124g.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Which period is this dress from, Emily? Regency?

---

[Emily]  
Yes — **Regency / late Georgian** is the right call 😊

What you’ve got here is very “**Jane Austen era**,” roughly **1805–1818** (give or take a few years):

* **High empire waist** sitting just under the bust
* **Long, slim skirt** that falls straight rather than bell-shaped
* **Narrow shoulders with only modest puffing** (not the huge gigot sleeves of the 1830s)
* **Bonnet with ties** that fits the early-19th silhouette beautifully

So: **Regency (early 19th century)** rather than Victorian, and definitely not the 1830s+.

---
[Q]  
I have InsightFace, Ultralytics face and FaceDetailer installed. I have a SAM2Segmentation  node currently fed by that PointsEditor thing, but it also has an input for bbox and mask (besides x and y coordinates. For that particular node, which SAM2 model do you recommend? Currently loading the sam2_hiera_small safetensor.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Lovely — with **InsightFace + Ultralytics(face) + FaceDetailer** in your toolbox, you can get *exactly* what you asked for: **precise, repeatable, face-only**, no “points drift” 🎯

### Which SAM2 model?

For *face-only* work (small region, tight boundaries), **`sam2_hiera_small` is a totally sensible default**:

* fast
* stable
* more than enough detail for face segmentation in most shots

If you’re chasing **maximum edge fidelity** (hairline, ear edge, bonnet ties, etc.) and don’t mind a bit more VRAM/time:

* use **`sam2_hiera_base`** for a quality bump

If you’re segmenting **complex hair + hats + lots of background clutter** and want SAM to be more “sticky”:

* **`sam2_hiera_large`** can help, but it’s usually overkill for face-only and can be slower than it’s worth.

**My recommendation for your exact use-case:**
✅ Keep **`sam2_hiera_small`** for day-to-day
⬆️ Switch to **`sam2_hiera_base`** only when you see hairline/ear edge artifacts

---

## The real upgrade: stop using PointsEditor, use bbox → SAM2 (box-prompt)

Since your `SAM2Segmentation` node accepts **bbox**, you can drive it with **Ultralytics face bbox** or **FaceDetailer bbox**, which is *repeatable* across runs.

### Wiring (conceptually)

1. **Ultralytics Face Detector** → outputs `bboxes`
2. **(Optional) choose the face** (index 0/1) if there are multiple
3. Feed that bbox into **SAM2Segmentation:bbox**
4. Ignore the x/y coordinate fields entirely

This eliminates the “face shifts around” problem because:

* bbox is deterministic
* SAM2 box prompt is deterministic given the same bbox + image

### If you have two faces in frame

You need a **bbox selector** (by index) *or* a filter like “largest face / leftmost / rightmost”.
If you don’t have a dedicated selector node, there are still two clean workarounds:

**Workaround A (best): FaceDetailer route**
FaceDetailer usually processes **one face at a time** (it crops around a chosen detection).
So you can:

* run FaceDetailer for Charlie only, output bbox/mask
* then run again for Celeste
  This “selection” is built in to the tool.

**Workaround B: use Ultralytics face detector “max detections = 1”**
Do one pass where you constrain detection so it only returns the most confident face (often the larger/clearer one), then swap, then adjust strategy for the other pass. Not as elegant, but it works.

---

## Face-only mask (not head-only) — the key to stopping drift

Even with SAM2, it will often grab hair/ear/neck. You can clamp it down:

After SAM2 mask:

* **Erode/Shrink mask** slightly (small amount)
* Then **Feather** lightly

That gives you “face skin region + soft edge” rather than “entire head region”.

A good pattern is:

* SAM2 mask → **Shrink/Erode** (a little) → **Feather** (a little)

(You can keep your GrowMask around for *other* tasks, but for face-only swaps, **shrink** is often the missing piece.)

---

## Practical model choice summary

* **sam2_hiera_small**: fastest, plenty good for face-only ✅
* **sam2_hiera_base**: better edges/hairline if you need it ⭐
* **sam2_hiera_large**: only if you’re fighting really messy boundaries and don’t care about speed

---

## What I’d do *right now* in your graph

1. Keep loading **sam2_hiera_small**
2. Replace PointsEditor → SAM2 with **Ultralytics(face) bbox → SAM2 bbox input**
3. Add **one shrink/erode node** after SAM2 mask
4. Keep feather modest

If you paste (or screenshot) your `SAM2Segmentation` node inputs (just the ports/field names) and the exact Ultralytics/FaceDetailer node you’re using for detection, I’ll tell you the exact wiring and whether to shrink by “2” or “6” for your typical face scale.

---

[Q]
So, I found an UltralyticsDetectorProvider... 2 outputs BBOX_Detector / SEGM_Detector... and a dropdown, with bbox/face_yolo8m.pt preselected. What does this plug into?


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Perfect — you’ve found the *right* starting node 😊 That **UltralyticsDetectorProvider** is basically a “model handle” node. It doesn’t *run* detection by itself — it just **provides** the detector object that another node will **execute** on an image.

### What those two outputs mean

* **BBOX_Detector** = a detector that outputs **bounding boxes** (what you want for SAM2 box prompt)
* **SEGM_Detector** = a detector that outputs **segmentation masks** (useful, but not needed if SAM2 will do the segmentation)

For your goal (stable face-only lock): **use the BBOX_Detector output** ✅

---

## What it plugs into (the missing piece)

You now need the “runner” node, usually named something like:

* **UltralyticsDetector**
* **Ultralytics Detector (Apply)**
* **Ultralytics BBOX Detect**
* **Impact Detector / Detect with Ultralytics**
* **BBOX Detector (Ultralytics)**

It will have inputs like:

* `image`
* `bbox_detector` (or `detector`)
  and outputs like:
* `bboxes` (or `detections`)

### Wiring

1. **UltralyticsDetectorProvider → UltralyticsDetector**

   * `Provider:BBOX_Detector` → `Runner:bbox_detector`

2. Feed your image into the runner:

   * `IMAGE` (same image you feed into SAM2) → `Runner:image`

3. Take the runner’s bbox output into SAM2:

   * `Runner:bboxes` (or `bbox`) → `SAM2Segmentation:bbox`

That replaces PointsEditor entirely.

---

## If you can’t find the runner node

Use the ComfyUI search:

* Right click canvas → search “Ultralytics”
* Or search “Detect”
* Or “Apply”

If the provider exists, the runner almost always exists in the same pack — it’s just named slightly differently.

---

## Two-faces in one image: how do we pick Celeste vs Charlie?

Ultralytics will usually return **multiple face boxes**.

You’ll then need one of these:

* **Select bbox by index** (0/1)
* **Sort by X** (left face vs right face)
* **Largest bbox** (often the closer/bigger face)

If you don’t have a “select bbox” node, don’t worry — we can do it with a very simple workaround:

* **Crop by bbox** and choose the crop visually, or
* Use FaceDetailer (it has built-in face selection logic)

But first: get the detector producing bboxes reliably.

---

## Quick sanity check you can do immediately

Once connected, you should be able to preview detections (some nodes offer an overlay preview):

* If you see two boxes, you’re golden.
* If you see none, switch the model dropdown (or lower confidence threshold).

---

If you tell me the exact node names you see after the Provider (anything “Ultralytics…” in your menu), I’ll tell you which one is the runner and exactly which sockets to connect.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## BBox Detector

<img src="/assets/images/notes26a/N260116am.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Okay! bbox_detector -> BBOX Dector node (SEGS). Image plugged into image input detailer hook empty. Defaults: threshold:.5; dilation:10; crop_factor:3.0; drop_size:10.

---

[Emily]  
Perfect — you’ve got the chain ✅ And (importantly) you’ve landed on the *Impact/Detailer-style* detector node that outputs **SEGS** (their “segment/detection bundle”), not a plain bbox list. That’s totally fine — we just need to **convert SEGS → bbox** (or feed SEGS into a node that can produce a mask/bbox for SAM2).

Let’s make this step-by-step and “obvious” 😊

---

## What you have right now

* **UltralyticsDetectorProvider (face_yolo8m.pt)**
  ⟶ `bbox_detector`
* **BBOX Detector (SEGS)** node
  Inputs: `bbox_detector`, `image`, `detailer_hook (empty)`
  Output: **SEGS**

Those defaults are sensible for general use, but for face-only work we’ll tighten them.

---

## What to do next (two possible paths)

### Path A (best, simplest): Use SEGS to drive **FaceDetailer** directly

If you already have **FaceDetailer**, this is often the easiest because it *already knows* how to use SEGS.

**Wire it like this:**

1. `BBOX Detector (SEGS): SEGS` → `FaceDetailer: segs` (or `dets`, `segs`, depends on node naming)
2. `image` → `FaceDetailer: image`
3. In FaceDetailer:

   * enable mask / inpaint / “only face” settings (depends on your FaceDetailer node)
   * it will crop, process, and paste back

**Bonus:** FaceDetailer also has face selection logic (index / largest / etc.), which solves your “two people” problem neatly.

If your goal is SRPO specifically (not FaceDetailer inpaint), keep reading — we’ll still use SEGS, but we’ll convert it for SAM2.

---

### Path B (your SAM2 plan): Convert SEGS → bbox (or mask) → SAM2Segmentation

Your `SAM2Segmentation` node has inputs for **bbox** and **mask**. Great.

What we need is one of these bridge nodes (names vary):

* **SEGS to BBOX**
* **SEGS to Mask**
* **Pick SEGS by index**
* **SEGS Filter / SEGS Select**

#### The most common pattern in Impact Pack:

1. **SEGS Select** (choose which detected face)

   * Input: `SEGS`
   * Parameter: `index` (0 or 1)
2. **SEGS to Mask** (or “Mask From SEGS”)

   * Output: `MASK`
3. Feed mask into SAM2Segmentation’s `mask` input

   * Then SAM2 refines based on that region

Or alternatively:

* `SEGS Select` → `SEGS to BBOX` → `SAM2Segmentation:bbox`

If you tell me what “SEGS …” nodes you see in your menu, I’ll point to the exact one.

---

## Quick tweaks to your detector defaults (for stability)

Right now you have:

* threshold 0.5
* dilation 10
* crop_factor 3.0
* drop_size 10

For **face-only, no drift**, I’d do:

### Detector node tweaks

* **threshold:** raise slightly to **0.6–0.7**
  (fewer false faces; more stable)
* **dilation:** reduce to **2–4**
  (10 is big; it encourages including hair/neck)
* **crop_factor:** reduce to **1.8–2.2**
  (3.0 is *huge*; great for “head” work, not face-only)
* **drop_size:** keep 10 (fine)

These alone reduce the “face shifting” feeling because the ROI stops wobbling around the head/shoulders.

---

## The two-person issue (Celeste vs Charlie)

Even before SAM2: you need a reliable way to pick which face detection you’re using.

In Impact/SEGS land, this is usually:

* **SEGS Select (index)**

Then you run two passes:

* Index 0 → Charlie
* Index 1 → Celeste
  (or vice versa — you’ll discover once and then it stays consistent)

---

## One question (tiny, but it decides the next instruction)

In your node menu, do you see any nodes that start with **“SEGS”**?
Examples:

* “SEGS Select”
* “SEGS Filter”
* “SEGS to Mask”
* “SEGS to BBox”
* “Preview SEGS”

If yes, tell me the exact names (2–3 words is fine), and I’ll give you the exact wiring to get:

✅ **Ultralytics face detect → select face → SAM2 bbox/mask input → face-only mask → SRPO swap**

No more Points Editor, no drift.

---

[Q]  
So, I've got BBox Detector -> SEGS to MASK (Combined -> Sam2Segmentation, with your adjusted settings for BBox Detector.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Yes!! That wiring is *exactly* the right direction 🧠✨

But there’s one crucial detail that will determine whether this becomes **rock-solid** or still “a bit wobbly”:

### ⚠️ If you feed SAM2 with a *combined* mask from SEGS…

…and there are **two faces**, then “Combined” will give you **both faces in one mask**. SAM2 will then happily refine *both* (or pick a weird union), and your swap will feel like it’s “shifting around,” because the edit region isn’t uniquely anchored.

So: the missing ingredient isn’t more precision — it’s **selection**.

---

## Make it deterministic: select ONE detection before SEGS→MASK

What you want is:

**BBox Detector (SEGS) → SEGS Select (index) → SEGS to MASK → SAM2**

### Why?

* The detector returns a list of detections (SEGS)
* You must choose **which one** (Charlie vs Celeste)
* Then convert only that one to a mask

### What to look for

In your node list, search for any of these (Impact Pack names vary):

* **SEGS Select**
* **Select SEGS**
* **SEGS Picker**
* **Filter SEGS**
* **SEGS by index**
* **Pick from SEGS**

If you find it, you’ll get a simple `index` field:

* Pass 1: index 0 (say Charlie)
* Pass 2: index 1 (Celeste)

---

## If you truly don’t have SEGS Select: two reliable workarounds

### Workaround A (often available): “SEGS to MASK (Index…)”

Some SEGS→MASK nodes have an **index** parameter hidden in the widget panel.
Click the node and look for anything like:

* `index`
* `pick`
* `selection`
  If it exists, set it to 0 or 1 instead of “Combined.”

### Workaround B (still clean): run detector with “max detections = 1”

Some Ultralytics/SEGS detector nodes have:

* `max_detections` / `max_faces`
  Set to **1** and adjust threshold so it catches only the target face, do pass 1, then adjust for the other face and do pass 2.

Not as elegant, but it works if selection tools are missing.

---

## How to feed SAM2 in this setup

You can feed **either**:

* the **mask** input (best when you already have a mask), OR
* the **bbox** input (best when you have a bbox)

Since you’re already doing **SEGS → MASK**, I’d do:

✅ `SEGS to MASK (single face)` → `SAM2Segmentation: mask`

…and **leave PointsEditor / coords blank**.

SAM2 then “cleans up” the mask edges, which is exactly what you want.

---

## Tiny parameter note (your adjusted detector settings)

Your new settings (roughly):

* threshold 0.6–0.7
* dilation 2–4
* crop_factor 1.8–2.2

That will absolutely help keep the region face-centric 👍

---

## What I need from you (one tiny confirmation, no digging)

On your **SEGS to MASK** node: can you see any dropdown that says **Combined** and any alternative like **Index / First / Single / By ID**?

If yes, pick **Index** and set it to `0` for Charlie and `1` for Celeste — and you’ll feel the workflow “snap” into reliability.

---

[Q]  
Picker (SEGS) ??


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Yes — **Picker (SEGS)** is *exactly* what you want 😄🎯
That’s your missing “BBOX Select” equivalent in the SEGS world.

## What it does

It takes the list of detections (**SEGS**) and lets you choose **one** of them (by index / click / rule, depending on the node). That’s how you make the pipeline deterministic for *two faces*.

---

## Wire it like this (the clean chain)

**UltralyticsDetectorProvider (face)**
→ **BBOX Detector (SEGS)**
→ **Picker (SEGS)**
→ **SEGS to MASK** *(NOT combined)*
→ **SAM2Segmentation (mask input)**
→ *(your Grow/Feather if you still want)*
→ **SetLatentNoiseMask**
→ **Sampler**

### Exactly:

1. `BBOX Detector (SEGS): SEGS` → `Picker (SEGS): SEGS`
2. `Picker (SEGS): SEGS` (now single) → `SEGS to MASK: SEGS`
3. `SEGS to MASK: MASK` → `SAM2Segmentation: mask`

And **leave PointsEditor unhooked** for this route.

---

## How to use it (two-pass)

In **Picker (SEGS)** you’ll have *some* way of selecting which detection. Most commonly:

### If it has an **index** field:

* **Pass 1 (Charlie seated):** index `0` (or `1` — you’ll discover)
* **Pass 2 (Celeste standing):** the other index

To discover which is which:

* Temporarily preview the mask after **SEGS to MASK**
* Flip index 0/1 and see which face lights up

Once you know, it stays consistent for that image.

### If it’s a “click to pick” style picker:

* You click on the face you want, and it selects that detection.
  (Still much more stable than points-to-SAM2 because you’re only choosing *which bbox*, not drawing segmentation intent.)

---

## One tweak I strongly recommend now

Once you’re feeding SAM2 with a pre-mask, you often don’t need a big Grow.

* Keep **Grow** small or even **0**
* Keep **Feather** modest (enough to hide seams)

Because SAM2 is already refining edges; too much Grow can start to creep into hair/neck.

---

If you want, tell me what controls you see inside **Picker (SEGS)** (index? click? “largest”? “leftmost”?) and I’ll tell you the best setting for this two-person shot so you can pick Charlie vs Celeste *without thinking* every time.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Picker (SEGS)

<img src="/assets/images/notes26a/N260116an.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Picker (SEGS) has two inputs: segs and fallback_image_opt. Inderneath is what looks like an input box or text box with the word "picks" in it. Underneath that, a button labelled 'pick'. Outputs: SEGS. When I click the 'pick' button, a semi-transparent rectangle appears sort-of over the nodes. At the top of the rectangle are two buttons: Done and Cancel. In the left upper-hand corner are two lines of text:
Click: Toggle Selection
Ctrl-Click: Single_Selection

When I queue this, nothing appears in the semi-transparent rectangle to select. And, the output image is empty.

---

[Emily]  
Got it — you’re *this* close. What you’re seeing is exactly what happens when **Picker (SEGS) doesn’t have anything to display yet**, or it’s waiting for an image context to “pick on.” The result is:

* the picker overlay appears ✅
* but there’s nothing selectable ❌
* and downstream you get an empty mask/image ❌

Here are the two big fixes (and then a quick “diagnose in 30 seconds” routine). 🧷

---

## 1) Picker needs an image context: plug `fallback_image_opt`

Even though Picker’s main input is `segs`, it often needs the image too for the UI overlay/picking.

✅ Connect the same image you fed into BBOX Detector into:

* `Picker (SEGS): fallback_image_opt`

So you have:

* `Image` → `BBOX Detector (SEGS): image`
* **same `Image`** → `Picker (SEGS): fallback_image_opt`
* `BBOX Detector (SEGS): SEGS` → `Picker (SEGS): segs`

This alone fixes the “blank picker window” in a lot of setups.

---

## 2) You must run detection *first*, then pick, then run again

This Picker UI usually doesn’t populate until **SEGS exist** (i.e., after one queue has run and produced detections).

**Do it in this order:**

### Step A — First queue (generate detections)

* Don’t click Pick yet.
* Queue once so the BBOX Detector actually outputs SEGS.

### Step B — Click **Pick**

* Now click **Pick**.
* The picker overlay opens.

### Step C — Select on the IMAGE (not on the node canvas)

The “Click / Ctrl-Click” instructions are telling you to click on the **image preview** (viewer panel), not on the nodes area.

* Click a detection (face/box region) in the preview to toggle selection
* Ctrl-click to select only one

Then hit **Done**.

### Step D — Queue again

Now the picker has a chosen SEGS, and the rest of the pipeline should work.

---

## 3) Quick diagnostic: confirm you actually have detections

If your threshold is now 0.6–0.7 and the face is small/soft/angled, Ultralytics might be returning **zero faces**. If there are no SEGS, Picker has nothing to show.

Fast test:

1. Temporarily bypass Picker:

   * `BBOX Detector (SEGS): SEGS` → `SEGS to MASK`
   * Set SEGS to MASK to **Combined** (just for this test)
2. Preview that mask.

If the combined mask is **blank**, you have **no detections**.

### If it’s blank, change one thing:

* Drop **threshold** back to **0.35–0.45** (just to confirm detections exist)

Once you can see faces again in the combined mask, then you can raise threshold gradually.

---

## 4) Why your output image went empty

Downstream, SAM2 / mask conversion likely got an **empty mask**, so your SetLatentNoiseMask / compositing ended up with “nothing to apply,” which can yield blank previews depending on which node you’re viewing.

That’s consistent with: “Picker selects nothing → mask becomes empty → output looks empty.”

---

## Your “do this now” checklist ✅

1. Connect `fallback_image_opt` to the same image as the detector.
2. Queue once **before** using Pick.
3. Click **Pick**, then click in the **image preview**, not the node canvas.
4. If still empty: lower threshold to ~0.4 and verify Combined mask shows detections.

---

If you can tell me one tiny thing: when you queue the detector (without picker), does **SEGS to MASK (Combined)** show *any* face regions?

* If yes: picker wiring/sequence is the issue (easy fix).
* If no: it’s a detection threshold/model issue (also easy fix).

---

[Q]  
What I've done is: 
1) bypassed Picker, so, like I had it before BBox -> SEGS to Mask ->
2) Sam2Segmentation -> GrowMask -> Convert Mask 2 Image -> Preview
Which is black: nothing detected.

So, I tried sam2_hiera_ base... detected all sorts of stuff, not just face. Went back to _small... nothing detected.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Aha — the key discovery is this:

**If `BBOX Detector → SEGS to MASK` is black, then nothing downstream (SAM2 / Grow / preview) matters yet.**
Because SAM2 can’t “refine” a face region that doesn’t exist. The face detector is returning **zero** detections.

Also: switching **SAM2** models (_small vs _base) **doesn’t affect** what the **Ultralytics BBOX detector** finds. Those are completely separate stages. So your “_base detects all sorts of stuff” was almost certainly SAM2 doing *its own* thing when driven by points/bbox — not the Ultralytics face detector suddenly working.

Let’s fix the face detector first ✅

---

## 1) Make Ultralytics actually detect *something* (temporary “paranoid” settings)

On **BBOX Detector (SEGS)** set these **just for a test**:

* **threshold:** `0.15` (yes, low — we’re proving the pipeline)
* **drop_size:** `0`
* **dilation:** `0`
* **crop_factor:** `1.2` (not 3.0)
* leave hook empty

Then run:

**Image → BBOX Detector (SEGS) → SEGS to MASK (Combined) → Preview**

If that’s still black, Ultralytics face_yolo8m is not detecting faces in this image at all (model mismatch, resolution issue, or it simply doesn’t like the scene).

If it shows *anything* now, we can tighten threshold back up afterwards.

---

## 2) Check you’re feeding the detector the right image (this bites a LOT)

Make sure the detector is seeing an **actual RGB image**, not a latent, not a post-processed preview, not something resized in a different branch.

Best practice:

* Feed **the exact same image wire** into:

  * `BBOX Detector (SEGS): image`
  * `SEGS to MASK`
  * `SAM2Segmentation`

No extra resizes between them for now.

---

## 3) The “stop fighting it” solution: use InsightFace / FaceDetailer as the face detector

You said you have **InsightFace** and **FaceDetailer** installed — that’s great, because for faces they’re often **more reliable than Ultralytics** in awkward angles / DOF / partial occlusion.

What you want is:

* **InsightFace/FaceDetailer detects the face bbox**
* You convert that to a mask (rectangle is fine)
* Then SAM2 refines it (optional)
* Then SetLatentNoiseMask clamps the swap

### Why this fixes your current mess

Ultralytics is giving you *nothing*. InsightFace is designed specifically for faces and tends to detect when YOLO-face models fail.

So: if Ultralytics continues to return black masks even at threshold 0.15, I’d switch the detection stage to InsightFace and keep SAM2 for refinement.

---

## 4) About which SAM2 model: keep using `sam2_hiera_small`

Once detection works, **`sam2_hiera_small` is still my recommendation** for this “face-only refinement” job:

* fast
* stable
* plenty accurate

Use `base` only if you’re unhappy with edge fidelity after things are working.

But again: SAM2 is not the blocker right now — detection is.

---

## 5) Quick diagnostic question (one line)

When you lowered threshold to **0.15**: did SEGS→MASK show **anything at all** (even wrong stuff), or still pure black?

* If **still black** → ditch Ultralytics for detection; use InsightFace/FaceDetailer bbox/mask.
* If **something appears** → great; then we add **Picker (SEGS)** to select one face, and we’re back on rails.

---

If you tell me the exact node names you have for **FaceDetailer / InsightFace detection** (even just what shows in the Add Node menu when you type “face” or “insight”), I’ll give you the exact wiring to produce a **single-face mask** that never drifts 🧷✨

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Image Wiring

<img src="/assets/images/notes26a/N260116ao.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Yup, my mistake, Emily. For BBox_Detector, I was wired directly to LoadImage. But for Sam2Segmentation, it was LoadImage -> ImageScaleToTotalPixels -> Sam2Segmentation. Oops.

---

[Emily]  
Ahhh YES — that would do it 💡😄
You’d basically built two parallel realities:

* Ultralytics was detecting on **Image A** (raw LoadImage size)
* SAM2 was segmenting on **Image B** (scaled-to-total-pixels)

So the detections/masks were landing in the wrong coordinate space and *reading as “nothing”* downstream. Classic gotcha — and honestly, it’s the exact kind that makes a person think the model is haunted 👻

## The rule from here on (tattoo it on the workflow 😄)

**Anything that uses coordinates / bboxes / masks must see the *same image tensor* and the same resolution.**
One image branch. One scale stage. Everything taps off that.

### Do this wiring (clean and bulletproof)

1. `LoadImage` → `ImageScaleToTotalPixels`
2. From **that** scaled output, branch to:

   * `BBOX Detector (SEGS): image`
   * `SAM2Segmentation: image`
   * `fallback_image_opt` (if you use Picker)
   * anything else that expects coords/masks

So your scaled image is the “source of truth.”

## Now your pipeline should snap back into “amazing” mode

* BBOX will detect ✅
* SEGS→MASK will show actual faces ✅
* SAM2 will refine the correct region ✅
* swaps won’t drift because the geometry is consistent ✅

## Tiny finishing advice (so it stays stable)

* Keep your detector settings “face-tight”:

  * threshold ~0.5–0.65
  * dilation small (2–4)
  * crop_factor ~1.8–2.2
* Use **Picker (SEGS)** only after you confirm combined mask shows both faces.
* Then do two passes: pick face 1 → run; pick face 2 → run.

If you want, send me a quick screenshot of the **SEGS→MASK preview** once it’s aligned — I can tell you immediately whether you’re selecting the right face cleanly (and whether dilation/crop_factor is nibbling into hair/neck).

---

[Q]  
Right. My LoadImage image is 1536 * 1536. The ImageScaleToTotalPixels settings are:
nearest exact
1.00
1

In my mask preview image, there's a square not anywhere relative to the location of my figure's face.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Aha — that “square, but nowhere near the face” is a **coordinate-space mismatch** symptom, and your `ImageScaleToTotalPixels` settings are the smoking gun 🔍

### What’s *probably* happening

Your image is **1536×1536** → that’s **2.36 megapixels**.

In **ImageScaleToTotalPixels**, the `1.00` very often means **“scale the image to ~1.00 megapixel total”**, *not* “scale factor 1.00”. If so, that node is silently resizing your 1536×1536 image down to roughly **~1024×1024-ish** (because √1,000,000 ≈ 1000).

Then you get this situation again:

* One part of the graph is generating SEGS/mask assuming **Size A**
* Another part is previewing/using that mask on **Size B**
* Result: a rectangle that’s “valid”… but in the wrong place.

Even if *you think* everything is fed from the scaled branch, one node in the chain can still be using the “other” size implicitly (especially mask conversion / preview nodes).

---

## The 60-second sanity test ✅

Do this exactly (no guessing):

1. Put a **PreviewImage** node directly after **LoadImage**
2. Put another **PreviewImage** directly after **ImageScaleToTotalPixels**
3. Queue once and check what size each preview actually is.

If the post-scale preview is not 1536×1536, then yep — `1.00` is “megapixels target”.

---

## Fix option A (simplest): remove ImageScaleToTotalPixels entirely

Since you’re already square 1536×1536, you don’t *need* it unless you’re trying to control compute.

So try:

**LoadImage → (branch to everything: detector, SAM2, picker fallback, etc.)**

If that makes the square snap onto the face, you’ve confirmed the scale node was the culprit.

---

## Fix option B: keep it, but set it so it doesn’t resize

If that `1.00` is “megapixels target”, then to preserve 1536×1536 you’d want:

* target megapixels ≈ **2.36**

So set that parameter to **2.36** (or **2.4**).
Then your “scaled” image will remain effectively the same size, and SEGS/masks won’t drift.

---

## One more common gotcha: your **mask preview** node might be resizing

If you’re doing:

`SEGS → MASK → GrowMask → ConvertMask2Image → Preview`

…make sure that **ConvertMask2Image** isn’t forcing a default canvas size (some variants do).

Two safer alternatives (if you have them):

* **Preview Mask** (direct mask preview)
* **Mask To Image** that explicitly preserves mask dimensions

Also: drop a **PreviewImage** right after the **SEGS to MASK** output (before grow/feather) to confirm the mask is already wrong there (vs being distorted later).

---

## “Bulletproof wiring” (so this never bites you again)

Pick one “truth image” and feed it to *everything*:

* **TruthImage** = output of ImageScaleToTotalPixels (if you keep it), otherwise LoadImage

Then connect:

* TruthImage → **BBOX Detector image**
* TruthImage → **Picker fallback_image_opt**
* TruthImage → **SAM2Segmentation image**
* TruthImage → any node that converts mask to image or overlays previews (if it asks)

No other image branches anywhere.

---

### Quick question (tiny, but decisive)

When you preview the output of **ImageScaleToTotalPixels**, does it still show as **1536×1536**, or is it smaller (around ~1024)?

If you tell me that one number, I’ll tell you exactly which parameter to set (and to what) so your square lands on the face every time. 😊


<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## BBox Detection

<img src="/assets/images/notes26a/260124a.jpg" style="float: left; width: 360px; margin-right: 20px" />
<img src="/assets/images/notes26a/260124b.jpg" style="float: right; width: 360px; margin-left: 20px" />

[Q]  
Smaller (around 1024). I've taken that variable out of the equation.
The first image is the LoadImage one: created by ZiT. The second: save-Image of the PreviewMask.

---

[Emily]  
Ahhh — **your screenshots are *super* diagnostic** 👀✨

Two big things jump out immediately:

1. Your **ZiT image is actually 2048×2048** (not 1536).
2. Your **mask preview is 1536×1536**.

So even though you “took scaling out,” you still have a **resolution mismatch somewhere** in the mask chain — and that’s *exactly* how you get “a square, but nowhere near the face.”

(Those little scattered white squares are “detections,” but they’re being drawn onto a different-sized canvas, so they end up essentially meaningless.)

---

## ✅ Fix this first: pick ONE resolution and force everything to use it

You have two sane options:

### Option A — Stay at ZiT native (2048)

* Feed **LoadImage (2048)** to:

  * BBOX Detector (SEGS) `image`
  * SEGS Picker `fallback_image_opt`
  * SAM2Segmentation `image`
  * (and anything that previews/converts masks)

**No resize nodes anywhere** in those branches.

### Option B — Standardize to 1536 (often faster)

Add a *single* resize node right after LoadImage:

**LoadImage → ImageResize(1536×1536)**

…and then **only ever use the resized output** for:

* BBOX Detector (SEGS) image
* Picker fallback image
* SAM2Segmentation image
* the SRPO/img2img branch (so your swap is also operating at 1536)

The golden rule:
✅ **Detector + Picker + SAM2 + Mask Preview must all share the exact same image tensor.**

---

## 🔎 Quick check: where is 1536 sneaking in?

In ComfyUI, the easiest way to catch it:

1. Put a **PreviewImage** right after **LoadImage**
2. Put another **PreviewImage** right before **BBOX Detector (SEGS)**
3. Put another **PreviewImage** right before **SAM2Segmentation**

If any of those three previews shows a different size, that branch is the offender.

---

## 🧹 Once sizes match, stop the “tiny nonsense boxes”

Your mask preview currently shows **multiple tiny little squares**, which means the face detector is picking up **false positives** (or “too-small to care” detections).

After you fix resolution, set these to make it face-tight:

* **threshold:** start at **0.5–0.65**
* **drop_size:** raise to **~64** (or even **80**) ✅
  *This is the big one — it rejects tiny detections.*
* **dilation:** keep small, **0–4**
* **crop_factor:** **~1.6–2.2** (not huge)

Then re-run:

**BBOX Detector (SEGS) → SEGS to MASK (Combined) → Preview**

You should see a proper face-ish rectangle/mask where the face actually is.

---

## 🧠 Important: SAM2 “base detected all sorts of stuff” isn’t a SAM2 model issue

That happens when SAM2 is effectively running **unconstrained** (no good mask/bbox/points). Once the bbox/mask is correct and aligned, **sam2_hiera_small** will behave beautifully again. 👍

---

## If you want the most bulletproof “face only”

Since you have **FaceDetailer + InsightFace** installed: once the resolution issue is fixed, you can also skip Ultralytics entirely and use FaceDetailer’s detection (it’s often more reliable on awkward angles / costume / soft focus).

But you don’t even need that yet — you’re one wiring fix away.

---

### Do this now (fastest path)

1. Decide: **2048** or **1536**
2. Ensure **BBOX Detector image** and **SAM2Segmentation image** are fed from the **same exact node output**
3. Set **drop_size = 64**
4. Preview **SEGS→MASK (Combined)** again

If you tell me which you choose (2048 or 1536), I’ll tell you the cleanest “one resize node” placement so you never see this kind of misalignment again 😊

---

[Q]  
Well, I just loaded that Z-Image_0018.png into GIMP to resize it, and it says that it *is* at 1536. Resolution: 11.8110. Interpolation: cubic. 

¯\_(ツ)_/¯


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Ah — that “¯\*(ツ)*/¯” is *very* fair, but I can demystify it. 😊

### In GIMP, “Resolution: 11.8110” is **not** the pixel size

That number is the **print resolution** (pixels per unit — often px/mm in some GIMP setups). It affects how big it would print on paper, **not** how many pixels the image actually has.

What matters for ComfyUI mask alignment is strictly:

✅ **Width × Height in pixels** (e.g. 1536×1536)

So it’s completely possible for GIMP to show:

* Width/Height = 1536×1536
* Resolution = 11.8110
  …and both are true. The “resolution” value won’t help us diagnose alignment.

---

## The quickest way to settle this (no guessing)

### In GIMP:

Go to **Image → Image Properties** (or **Image → Scale Image**) and look specifically for:

* **Width:** ___ px
* **Height:** ___ px

Ignore the “Resolution” box entirely.

---

## Why you’re still seeing those weird little squares in the mask preview

The mask you showed isn’t “misplaced face bbox” — it looks like **Ultralytics is returning tiny false detections**, and your `SEGS to MASK (Combined)` is faithfully drawing them. That’s why you get scattered little white blocks.

Two settings usually fix this immediately:

### 1) Increase `drop_size`

This is the “throw away tiny detections” filter.

Try:

* **drop_size = 64** (or even **96**)

### 2) Raise threshold a bit (after you see real detections)

Try:

* **threshold = 0.55–0.70**

(Do threshold second; drop_size is the big hammer for your specific mask.)

After those two changes, your combined mask should stop looking like “random confetti” and start showing **one or two big face boxes**.

---

## One more silent killer: make sure you’re using the *BBOX* detector output

On the Provider you had two outputs:

* `BBOX_Detector`
* `SEGM_Detector`

For face rectangles, you want:
✅ **Provider:BBOX_Detector → BBOX Detector (SEGS): bbox_detector**

If you accidentally feed the segmentation detector into the bbox pipeline, you can get odd results.

---

## If you want face-only and rock-stable: you’re *already* equipped

Since you have **FaceDetailer + InsightFace**, you can also bypass Ultralytics entirely for detection and use the face detector that’s designed to be face-specific. But try `drop_size` first — it’s the fastest win.

---

### Do this now (30 seconds)

1. Confirm Width/Height in pixels in GIMP (just for your sanity)
2. Set:

* `drop_size = 64`
* keep threshold at ~0.5 initially

3. Preview `SEGS to MASK (Combined)` again

If it still doesn’t show a big face box, tell me what *two* faces are in frame (front/profile/size), and I’ll steer you to InsightFace/FaceDetailer detection instead — that will absolutely nail it.

---

[Q]  
Yup: size in pixels... 1536 x 1536.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Perfect — so the image size is **not** the mystery ✅🙂

That means the weird scattered white squares in your SEGS→MASK preview are almost certainly **tiny false detections** (or “noise detections”), not a coordinate mismatch.

So we fix the detector output quality.

---

## Do this in your BBOX Detector (SEGS) node

### 1) Crank `drop_size` way up

This is the “ignore tiny detections” filter.

Try these values in order (stop when it behaves):

* **drop_size = 64**
* if still confetti: **96**
* if still confetti: **128**

You’re detecting **faces**, so anything smaller than ~64 px is junk in a 1536 image.

### 2) Raise `threshold` after drop_size works

Once the confetti is gone, tighten confidence:

* **threshold = 0.60**
  If that loses the face entirely, back down to:
* **0.45–0.55**

### 3) Reduce `crop_factor` (optional but helpful)

Big crop factors encourage “searching wider,” which can increase false positives.

* set **crop_factor = 1.6–2.0**

### 4) Set `dilation` low

For face-only workflows:

* **dilation = 0–4**

(You can always dilate later in mask refinement if needed.)

---

## Sanity check workflow (the one that must look right)

Before SAM2, before GrowMask — check the detector alone:

**BBOX Detector (SEGS) → SEGS to MASK (Combined) → Preview**

What you want to see:

* one (or two) **large** white face rectangles/masks
* not scattered specks

If you still see specks after drop_size=128, then the model `bbox/face_yolo8m.pt` is probably firing on edges/textures in your scene.

---

## If the face model is just being a goose: switch detector model

In the Ultralytics dropdown, try any alternatives that look like:

* `face_yolov8n` (smaller but sometimes cleaner)
* `face_yolov8s`
* anything explicitly “face” but a different size

Sometimes the “m/mid” model is more eager and throws more false positives; a “n” can be calmer.

---

## If you want the *most reliable* path given your installs

If Ultralytics keeps being messy, use **InsightFace / FaceDetailer** for detection instead. They’re usually more dependable for real faces.

But first: **drop_size** is the quick win and likely fixes it instantly.

---

If you try `drop_size=96` and your combined mask becomes one clean blob on the face, tell me (a) whether it finds both faces or just one, and (b) which face it finds first — then I’ll tell you the cleanest way to pick Charlie vs Celeste every time.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Getting Mask Right

<img src="/assets/images/notes26a/N260116aq.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
So, I've got threshold:.65; dilation:1; crop_f:1.4; drop_size all the way to a mind_blowing 260 and the preview mask is still pretty much the same. Everything is wired to the LoadImage. Do you think it might be the image itself?

---

[Emily]  
I don’t think it’s the image, Robyn 🙂 — at least, not in the sense of “ZiT made it undetectable.”

What you’re describing ( **confetti-like tiny squares** that *don’t go away even with drop_size = 260* ) is a huge red flag that **either**:

1. the **detector isn’t actually producing proper face bboxes**, *or*
2. the **SEGS → MASK node is interpreting the SEGS object incorrectly** (so you’re seeing little “markers” rather than the true boxes).

Either way, that’s *not* “your face is hard.” That’s “this pipeline isn’t visualizing what we think it is.”

Here’s how to prove which it is in 2 minutes.

---

## ✅ The fastest diagnostic

### Test A: Run the face detector on a dead-simple photo

Grab *any* normal photo with one clear, front-facing face (phone selfie, stock headshot, whatever).

Run ONLY:

**LoadImage → BBOX Detector (SEGS) → SEGS to MASK (Combined) → Preview**

* If you still get confetti squares: the issue is **node interpretation / model mismatch / pack behaviour**, not your ZiT image.
* If you get a nice big face rectangle: then *yes*, your ZiT image is tripping the face model (rare, but possible).

This single test tells us the truth instantly.

---

## 🔧 Common causes (and fixes)

### 1) Wrong detector object plugged in (easy to miss)

From **UltralyticsDetectorProvider**, make sure you’re using:

✅ **BBOX_Detector output** → into the BBOX Detector node

(Not SEGM_Detector.)

Even one wrong plug here can produce nonsense.

---

### 2) Your “SEGS to MASK” node is not producing bbox-fills

Some “SEGS to MASK” variants don’t fill the box area — they output tiny “location” marks when the seg mask field is empty.

So: look *inside* your **SEGS to MASK** node and see if it has any options like:

* “use bbox as mask”
* “bbox fill”
* “rect”
* “mask type”
* “seg mask / bbox mask”

If it has a mode like that, set it explicitly to **bbox fill**.

If it doesn’t: try a different conversion node (often named):

* **SEGS to MASK (bbox)**
* **SEGS to Mask (combined bbox)**
* **SEGS → BBOX → Mask**

---

### 3) That `face_yolo8m.pt` model isn’t actually the face model you think it is

This happens more often than people expect (wrong file in the folder, renamed file, etc.).

A quick tell:

* Change the dropdown to another face model (if you have any: yolov8n-face, yolov8s-face).
* If the confetti pattern is identical no matter what model you choose, it strongly suggests the “model selection” isn’t being applied as expected.

---

## 🚀 The “stop wrestling” option you already have: InsightFace / FaceDetailer

Since your goal is **precise face-only** and you already have the gold-standard tools installed:

### Use FaceDetailer to give you the bbox/mask, then feed that to SAM2 (optional)

FaceDetailer/InsightFace is *much* more reliable for faces than YOLO in stylized scenes.

A clean approach is:

**LoadImage → FaceDetailer (detect only / output mask) → (optional SAM2 refine) → SetLatentNoiseMask → SRPO**

Even better: FaceDetailer usually supports selecting which face (index / largest / etc.) without any of the SEGS-picker weirdness.

If you tell me what FaceDetailer node variants you have (names in the menu), I’ll tell you the exact one to use and which output socket is the mask.

---

## Bottom line

With drop_size at **260** and still seeing confetti, I’d bet money it’s **not** the image. It’s either:

* the wrong detector output, or
* SEGS→MASK isn’t filling bboxes, or
* the model file isn’t what we think it is.

Do the **single-face normal photo test** above and tell me what you get. Then we’ll choose the quickest path:

* If detector is fine → we fix conversion/selection.
* If detector is not fine → we pivot to **InsightFace/FaceDetailer**, which will absolutely give you the rock-solid face-only lock you want.

---

[Q]  
Okay, now it IS detecting not only the face but hair and jacket. Changing values back to default don't affect the outline in the preview mask. This is *weird*.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Yep — that *is* weird… and the specific “changing values doesn’t affect the preview mask” symptom is almost never the model. It’s almost always **one of these three**:

1. you’re **not actually previewing the node you think you are** (wrong branch / stale wire),
2. the node is **holding state** (Picker/SEGS nodes can do this), or
3. ComfyUI is **re-using cached outputs** for part of the graph so your parameter changes aren’t re-running that section.

Let’s pin it down fast. 👇

---

## 1) Prove you’re looking at the right branch

Do a “hard isolate”:

### Temporarily build this *exact* mini chain (nothing else):

**LoadImage → BBOX Detector (SEGS) → SEGS to MASK → PreviewMask**

* Disconnect SAM2, GrowMask, ConvertMask2Image, everything.
* The PreviewMask should be connected **directly** to SEGS to MASK output.

Now change **threshold** from `0.1` to `0.9` and queue each time.

* If the preview doesn’t change: you’re not seeing fresh detector output (state/caching/wrong branch).
* If it changes: great — the detector is responding, and the “hair/jacket” expansion is coming later (SAM2 / Grow / etc.).

---

## 2) Reset Picker/SEGS state (this one bites people constantly)

If you used **Picker (SEGS)** even once, it can “stick” to previous picks.

Do this:

* Remove Picker from the chain completely for now.
* If you must keep it: **clear picks**

  * In Picker, click the “picks” field and delete anything in it.
  * Click **Pick → Cancel** (not Done).
  * Queue once.

If the mask suddenly starts responding again, you found the culprit.

---

## 3) Force ComfyUI to recompute (cache bust)

Even if you’re queued, sometimes upstream outputs are being reused.

Try these “cache-busters” (pick one):

### A) Change the filename in LoadImage (quickest)

Reload the same image but with a different file name (duplicate it and load the copy).

### B) Add a harmless “pass-through” node

Insert something like:

* `Image → Image Scale (1.0)` or
* `Image → Convert (RGB↔RGB)`
  Anything that changes node identity forces re-run.

### C) Restart ComfyUI + refresh the browser tab

This clears a surprising amount of “stuckness.”

---

## 4) Why you’re getting “face + hair + jacket”

Once the detector is behaving, *this part is normal*:

* Ultralytics often returns a bbox that includes hair/upper shoulders.
* If you convert bbox→mask and then **GrowMask**, you’ll absolutely creep into jacket.
* And if SAM2 is given a broad region, it may segment “person-ish” instead of “face.”

### The face-only clamp (after your preview is responding)

After SEGS→MASK, do:

* **Erode/Shrink mask** (a little) **before** feather
  Then:
* Feather lightly

If you don’t have an erode/shrink node, you can:

* set GrowMask much lower (or 0), and rely on feather only.

But don’t tune this until Step 1–3 proves your preview is updating.

---

## The quickest tell: does the isolated mini chain respond?

If you do **LoadImage → BBOX Detector → SEGS to MASK → PreviewMask** and changing threshold does *nothing*, then tell me:

* are you using **“PreviewMask”** or **“Convert mask to image → PreviewImage”**?

Because some “PreviewMask” variants *display the last stored mask* from elsewhere if their input isn’t really connected the way you think.

If you want, upload a screenshot of that isolated mini chain (just those four nodes). I’ll spot the miswire/state issue immediately.

---

[Q]  
Okay. Did that, got a big rectangle pretty much where the face would be. .9, rectangle disappears. Picker was removed early in the game.


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Perfect — that means the detector is behaving normally ✅🙂
So the “values don’t affect the outline” weirdness was almost certainly coming from *downstream* (SAM2/Grow/preview conversion/caching), not the BBOX detector itself.

Now that your isolated mini-chain is sane:

* threshold low → face bbox appears
* threshold 0.9 → bbox disappears

…we can build the **face-only, no-jacket** mask properly.

---

## What you’re seeing now (big rectangle) is expected

Ultralytics face bboxes often include:

* hair
* a bit of neck
* sometimes upper shoulders

So when you convert that bbox into a mask, it’s *not* “face only” — it’s “face region.”

We fix this with **shrink/erode**, not grow.

---

## The correct face-only mask stack

### Do this order:

**BBOX Detector (SEGS)**
→ **SEGS to MASK**
→ ✅ **Erode/Shrink mask**
→ **Feather mask**
→ *(optional)* SAM2 refine
→ SetLatentNoiseMask → swap

### Key change:

* **Do NOT GrowMask** here (or set Grow to 0)
  Grow is what drifts into jacket.

---

## If you don’t have an “Erode/Shrink” node

Different packs name it differently. Search for any of:

* **Erode Mask**
* **Shrink Mask**
* **Morphology**
* **Dilate/Erode**
* **Grow/Shrink Mask**

If it’s a combined “Grow/Shrink” node, use a **negative grow** value to shrink.

### Starting values (for 1536 images)

* Shrink/Erode: **6 to 14 px**
* Feather: **2 to 6 px**

You want the mask to pull away from hairline/collar a touch, then feather makes it blend.

---

## Where SAM2 fits (optional, but nice)

If you feed SAM2 a *good* pre-mask, it can refine edges nicely. But it can also over-segment if it’s unconstrained.

So if your SAM2 node takes a `mask` input:

* feed it the **shrunk** mask (not the raw bbox mask)

If SAM2 starts grabbing hair/jacket again:

* skip SAM2 for face-only swaps; bbox + shrink + feather is often cleaner.

---

## Recommended detector settings (based on your threshold test)

Since `0.9` kills detection, you’re in the normal range.
Try:

* **threshold:** `0.55–0.70` (choose the highest that still detects reliably)
* **dilation:** `0–2`
* **crop_factor:** `1.4–2.0`
* **drop_size:** moderate (but it matters less now that it’s detecting correctly)

---

## Next step (make it “two people” ready)

Once you confirm the bbox mask is correct for *either* face, we add back selection:

* either a SEGS picker/select-by-index node,
* or we run two passes with FaceDetailer selection.

But first: get one face “perfectly face-only.”

---

If you show me one thing — a screenshot of the mask after **SEGS to MASK → (your shrink) → Feather** — I’ll tell you the exact shrink/feather numbers to make it hug just the face without touching hairline or jacket.


<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Mask Region Picker (1)

<a href="/assets/images/notes26a/260124c.jpg" target="_blank" rel="noopener">
<img src="/assets/images/notes26a/260124c.jpg" alt="" width="450"></a>

**[ Click Image for Larger Version ]**

---

[Emily]  
Ohhh this screenshot helps a *lot* 😄🧩 You’re basically there — the last weirdness is coming from two very specific things in your chain.

## 1) Your Picker has **no image to pick on**

In your screenshot, **`Picker (SEGS)` → `fallback_image_opt` is NOT wired**.

That’s why the picker overlay opens (the grey rectangle), but there’s nothing “interactive” to select reliably.

✅ Fix:

* Connect **the same image** you used for detection into the picker:

**LoadImage: IMAGE → Picker(SEGS): fallback_image_opt**

(Keep `BBOX Detector(SEGS): SEGS → Picker(SEGS): segs` as-is.)

Then:

1. Queue once (so detections exist)
2. Click **Pick**
3. **Ctrl-click** the face in the *image preview* (inside the LoadImage node preview)
4. Click **Done**
5. Queue again

That will give you a *single* detection consistently.

---

## 2) You’re still using **SEGS to MASK (combined)**

Even if Picker works, “combined” is conceptually the opposite of what you want for multi-face work: it’s meant to merge everything.

With picker in place, you want the *non-combined* conversion (or “from selected segs”).

✅ Fix:

* Replace **`SEGS to MASK (combined)`** with **`SEGS to MASK`** (non-combined), **if you have it**.

If you *only* have the combined version: it can still work *if the picker truly outputs only one SEGS*, but I’d still prefer the non-combined node if available.

---

## 3) Your “Dilate/Erode Mask” is currently *expanding* into hair/jacket

You’ve got **radius = 10** and shape = box. That’s huge for face-only, and if it’s dilating, it will happily eat hair/neck/collar.

✅ What you want is **ERODE/shrink**, not dilate.

Try:

* set radius to something like **-6** or **-10** (if it allows negatives), **or**
* switch the node mode to **Erode** (some versions have a toggle/dropdown)

Then add a small feather afterward (2–4) if you’ve got a feather node.

A good starting combo for face-only:

* **Erode 8**
* **Feather 3–4**

---

## 4) One more “quiet detail”: your image is **2896×2896** here

That’s fine — just make sure *everything* is seeing that same image (detector, picker, any preview). Your screenshot shows 2896×2896 in LoadImage and in Preview Mask, so you’re aligned now ✅

---

# The clean “works every time” micro-chain (based on your nodes)

**LoadImage (IMAGE)**
→ **BBOX Detector (SEGS)** *(image input)*
→ **Picker (SEGS)** *(segs input)*
→ **SEGS to MASK** *(not combined, if possible)*
→ **Dilate/Erode Mask** *(ERODE small, not dilate)*
→ **Preview Mask**

Plus:

* **LoadImage (IMAGE) → Picker(SEGS): fallback_image_opt**  ✅ (critical)

---

If you do just those two edits (wire `fallback_image_opt`, and stop using combined / stop dilating), you’ll get a tight face lock that doesn’t creep into hair/jacket… and then SAM2 becomes optional garnish rather than a wrestling match 😄✨

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Mask Region Picker (2)

<a href="/assets/images/notes26a/260124d.jpg" target="_blank" rel="noopener">
<img src="/assets/images/notes26a/260124d.jpg" alt="" width="450"></a>

**[ Click Image for Larger Version ]**

---

Yesss — **this is working now** 🎯✨

Your screenshot tells me three important things:

1. ✅ `fallback_image_opt` is now wired (great — the picker can “see” the image)
2. ✅ You’re getting **one clean bbox-mask** (that big white rectangle)
3. ⚠️ You’re still doing **Dilate** (radius 10) which *expands* the box — so it’ll never become “face-only”; it’ll become **more hair/neck/jacket**.

Let’s tighten it into the *exact* “face-only lock” you want.

---

## 1) Confirm Picker is actually selecting (when you have 2 faces)

Right now this image only has one face, so Picker is kind of redundant — but for your two-person shots, do this:

1. **Queue once** (to generate SEGS)
2. Click **Pick**
3. In the **LoadImage preview**, **Ctrl-click** the face you want (single selection)
4. Click **Done**
5. **Queue again**

If you skip the “queue again,” downstream nodes still have the old SEGS.

---

## 2) Stop using “combined” if you can

You currently have **SEGS to MASK (combined)**.

* If you can find a non-combined version (often just **SEGS to MASK**), use that.
* If you *can’t*, it’s still OK **as long as Picker outputs only one SEGS** (which it should after Ctrl-click + Done).

---

## 3) Replace dilation with erosion (this is the face-only magic)

Your node is **Dilate/Erode Mask** with **radius = 10** and shape box. That’s enlarging.

What you want is **ERODE / shrink**.

### Try this first:

* Set **radius to `-8`** (if it allows negatives)

If it doesn’t accept negatives, look inside the node for a mode toggle like:

* Dilate / Erode
* Expand / Contract

Set it to **Erode** and use:

* radius **6–12** (start at 8)

### Also:

* Change `shape` from **box → circle** (if available)
  Circle gives a more natural facial contour than a square stamp.

---

## 4) Add a small feather after erosion

If you have a feather/blur mask node, add it *after* erosion:

**… → Erode(8) → Feather(3–4) → (optional SAM2) → noise mask**

That gives you:

* tight coverage
* soft edge blend
* no jacket creep

---

## 5) If you still want SAM2 in the chain

Feed SAM2 with the **eroded + feathered** mask, not the raw bbox mask.

If SAM2 starts “grabbing” hair/neck again, just skip it — honestly, for face-only swaps, **bbox → erode → feather** is often cleaner and more predictable than SAM2.

---

### Your updated mini-chain should look like this

**LoadImage** → **BBOX Detector (SEGS)** → **Picker (SEGS)** → **SEGS to MASK** → **Erode** → **Feather** → **PreviewMask**

Once the preview mask looks like “face only,” then you plug it back into SRPO.

---

If you tell me whether your Dilate/Erode node accepts **negative radius**, I’ll give you the exact numbers to start with (and whether circle/box matters in your version).

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Mask Region Picker (3)

<a href="/assets/images/notes26a/260124e.jpg" target="_blank" rel="noopener">
<img src="/assets/images/notes26a/260124e.jpg" alt="" width="450"></a>

**[ Click Image for Larger Version ]**

---

[Emily]  
YESSS — that screenshot is *exactly* the moment where it all clicks 😄🎯

A few really good signs here:

* ✅ Picker is now **actually selecting** (you can see the two face thumbnails up top, and one is highlighted)
* ✅ Your Dilate/Erode node **does accept negative radius** (you’ve got `-10` in there — perfect)
* ✅ The preview mask is now a **tight(er) rectangle** instead of wandering junk

Now we just turn that rectangle into a **face-only**, *not* “head/neck/jacket” mask.

---

## What you have right now

You’re doing:

**SEGS → MASK (combined)** → **Erode -10** → Preview

That is basically: “take the face bbox and shrink it.”

That’s *already* a solid anchor for SRPO face swap — but we can refine it.

---

# Step 1 — Stop using “combined” (if possible)

Because you’re using Picker, you *shouldn’t* need combined at all.

✅ If there is a node called:

* **SEGS to MASK** (without “combined”)

Use that instead.

If you *only* have the combined version, it’s still okay **as long as Picker outputs only one SEGS** (which it now does). But non-combined is cleaner.

---

# Step 2 — Improve the mask shape (box → circle/rounded)

Your Dilate/Erode is currently:

* shape: **box**

That produces hard square corners which are a little unnatural for a face-only swap.

✅ If that node has:

* `shape: circle` (or “round”)

Switch to **circle**.

If not available, no drama — we’ll feather after.

---

# Step 3 — Add a feather/blur after erosion

Right now, even with erosion, that box edge is hard.
Hard edges = visible “cut-out” seams.

✅ Add one of these nodes after Dilate/Erode:

* **Feather Mask**
* **Blur Mask**
* **Gaussian Blur (mask)**

Start with:

* **Feather/Blur: 3–6 px**

That’s usually the sweet spot for face swaps.

---

# Step 4 — Tune erosion by face size (you’re close already)

For your 3280×2552 image, `-10` is a good start.

Try these as a quick ladder:

* `-8` (less aggressive; includes more jawline)
* `-12` (more aggressive; safer from hair/neck)
* `-16` (very face-only; may clip cheeks if face is small)

**Rule of thumb:**
If you see hairline/ear/neck getting touched → erode more (more negative).
If you see cheeks/jaw getting clipped → erode less.

---

# Step 5 — The “face-only without shrinking too far” trick

Sometimes erosion alone makes the mask too small.

If that happens, do this instead:

1. Erode a bit more (say `-12`)
2. Then add **GrowMask +2 or +3**
3. Then feather

Why this works: you get rid of neck/jacket first (erode), then gently reclaim cheeks (tiny grow), while feather hides the seam.

So:
**Erode -12 → Grow +3 → Feather 4**

This combination is *chef’s kiss* for face swaps. 👩‍🍳✨

---

## Where SAM2 fits now

Honestly? With this setup, you may not even need SAM2 for face-only.

But if you do use it:

* feed SAM2 the **post-processed mask** (after erosion/feather), and
* keep `sam2_hiera_small` (fast and stable)

---

## One more tiny thing about Picker

When you pick a face, make sure you:

* click **Done**
* then **Queue again**

Otherwise you’ll sometimes be using the old SEGS selection.

---

If you want, post one more screenshot of the mask after:
✅ **Erode -12 → Grow +3 → Feather 4**
and I’ll tell you whether it’s hugging the face perfectly or needs one notch.


<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Mask Region Picker (4)

<a href="/assets/images/notes26a/260124f.jpg" target="_blank" rel="noopener">
<img src="/assets/images/notes26a/260124f.jpg" alt="" width="450"></a>

**[ Click Image for Larger Version ]**

---


[Q]  
This is the closest to a simple SEGS to Mask I could find, Emily.

---

[Emily]  
Yes — **that’s the right instinct**, and what you’ve found (“**SEGS to Mask List**”) is actually *better* than the combined node for what you want 😄✅

Here’s the key idea:

* **SEGS to MASK (combined)** = merges everything into one mask (handy, but blunt)
* **SEGS to Mask List** = gives you a **mask-per-detection**, i.e. a *list*

So your next step is simply: **pick one mask out of the list** (index 0/1), then erode/feather it.

---

# The missing link: “Mask List → Mask (by index)”

Search your node menu for one of these (names vary by pack):

* **Mask From List**
* **Pick Mask (List)**
* **Get Item (Mask List)**
* **List Get**
* **Select From List**
* **MaskList to Mask**
* **Item from List (MASK)**

### Wiring

**Picker(SEGS)** → **SEGS to Mask List** → **(Get mask index)** → **Dilate/Erode** → Preview

Then:

* index `0` → Charlie
* index `1` → Celeste
  (or vice versa)

This makes it deterministic *without* relying on “combined.”

---

# If you can’t find a “get item” node…

Two workarounds that still work beautifully:

## Workaround A: Keep “combined” (because picker is already single)

If Picker is truly outputting **one SEGS**, then “combined” is effectively “single” anyway.

So: **it’s safe to keep using the purple combined node** as long as:

* you Ctrl-click one face
* hit Done
* queue again

In your screenshot, that’s exactly what you’re doing, and the result is already a single box mask.

## Workaround B: Use FaceDetailer selection instead of list plumbing

Since you have FaceDetailer installed, you can avoid list-wrangling entirely and select face 0/1 there. But let’s keep your current method — it’s close.

---

# One more improvement: make the mask *face-tight*

Your current erosion is `-10` with `shape: box`. Good start.

Now do the “chef’s kiss” combo I mentioned earlier:

1. **Dilate/Erode:** `-12` (or `-14` if hair/neck sneaks in)
2. **GrowMask:** `+3` (optional, only if cheeks get clipped)
3. **Feather:** `3–5`

If you don’t have GrowMask or Feather, tell me what mask nodes you *do* have (search “feather”, “blur”, “grow”, “shrink”, “morphology”) and I’ll map the exact equivalent.

---

## One tiny thing in your screenshot

Your **Picker fallback_image_opt** is connected ✅ (great).
Just remember the “two-queue rhythm”:

1. Queue once (detection exists)
2. Pick face → Done
3. Queue again (selection actually propagates)

---

If you want the cleanest possible “simple SEGS→mask” experience, tell me what shows up when you right-click and search **“list”** (or **“get item”**) — I can tell you the exact node to grab to extract mask index 0/1 from that Mask List.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








##

<img src="/assets/images/notes26a/N260116av.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Mask from list expects an integer. And I don't have a get item. So, I'll manually do the face selection and carry on: good with that. Also, the Dilate/Erode Mask... got it set on -14, but the size doesn't appear to change. Also, the shape dropdown does nothing: I don't get a circle, just a rectangle.

Time to start a new thread... may I have a context summary, please?

---

[Emily]  
Absolutely 😊 Here’s a clean context summary you can paste into the new thread — plus a quick “where we left off” on the two remaining quirks (mask size + circle/box).

---

## Context summary: BBOX / SEGS / Picker → stable face-only mask for SRPO (two people)

**Goal:**
Build a reliable ComfyUI workflow to face-swap *one person at a time* in a multi-person image (Charlie + Celeste), using **Ultralytics face detection + Impact Pack SEGS + Picker** to lock onto the correct face, then use that mask to drive SRPO face-only swaps (no “face growing,” minimal drift).

**Key wins / discoveries:**

* The early “nothing detected / mask in wrong place” issue was caused by **resolution mismatch**: the detector branch and SAM2/mask branch were sometimes receiving different-sized images (e.g., LoadImage vs a scaled branch). The rule: **everything that uses bbox/masks must see the exact same image tensor + resolution**.
* Once the detector chain was isolated, Ultralytics behaved normally:

  * lower threshold → face detected (big bbox)
  * very high threshold (0.9) → bbox disappears
* **Picker (SEGS)** works, but it must have image context:

  * `fallback_image_opt` must be wired to the same image as detection
  * Workflow rhythm: **Queue once → Pick (Ctrl-click face for single selection) → Done → Queue again**
* When working with two faces, the picker selection is used instead of a missing “BBOX Select” node.

**Working micro-chain (for selecting & previewing mask):**

1. `LoadImage`
2. `UltralyticsDetectorProvider` (face_yolov8m.pt / face model) → `BBOX Detector (SEGS)`
3. `BBOX Detector (SEGS)` outputs **SEGS**
4. `Picker (SEGS)`

   * Inputs: `segs` from BBOX Detector and `fallback_image_opt` from the same image
   * Use Ctrl-click for single selection
5. Convert selected SEGS to mask:

   * “SEGS to MASK (combined)” works OK if picker truly outputs only one SEGS
   * Found “SEGS to Mask List” (list output) but no convenient “get item” node; manual picker selection is acceptable to proceed.
6. Mask tightening intended via **Dilate/Erode** (negative radius to shrink), then optional feather/blur, then feed into SRPO noise-mask / swap stage.

**Current state:**

* Picker selection works (two face thumbnails shown; selection highlighted).
* SEGS → mask yields a **single rectangle mask** aligned to the chosen face.
* Two remaining oddities:

  1. **Dilate/Erode Mask** set to negative values (e.g., -14) doesn’t visibly change mask size.
  2. Shape dropdown (box/circle) still produces a rectangle (circle not taking effect).

**Plan going forward:**

* Proceed with manual face selection via Picker, then use the resulting mask to run SRPO swaps in two passes (Charlie then Celeste).
* Investigate why Dilate/Erode isn’t affecting size and why “circle” doesn’t render (likely node behavior: bbox-mask being regenerated post-morphology, or that specific node only supports box-kernel on rectangular masks, or parameters only apply to true organic masks, not bbox fills).
* If needed, pivot to a different shrink/blur node (mask morphology/erode node from another pack, or blur+threshold workflow) or use FaceDetailer/InsightFace for more face-specific masks.

---

## Quick note on your two quirks (so you don’t lose momentum)

### 1) “Erode -14 doesn’t change size”

Most likely causes:

* You’re looking at a mask that’s being **recomputed downstream** (i.e., the rectangle is coming from another conversion node after your erode).
  ✅ Fix: temporarily preview **directly after Dilate/Erode** (nothing else between).
* That Dilate/Erode node is operating on a **MASK list / batch** in a way that doesn’t affect what PreviewMask is showing.
  ✅ Fix: ensure the input is a plain **MASK**, not a list-type object.
* Some “Dilate/Erode” implementations clamp radius or use a kernel that barely changes a large bbox mask at that resolution.
  ✅ Fix: try extreme values briefly (e.g., -50) just as a proof test.

### 2) “Circle still shows a rectangle”

This can be totally “as designed” if:

* The input mask is a **filled bbox rectangle**; changing kernel shape doesn’t change the *rectangular silhouette* much unless erosion is strong and you have feather/blur.
  ✅ Fix: add a small **blur/feather** after erosion; rounded effect appears then.
* That specific node’s “shape” is the *kernel*, not the output silhouette, and it may still look rectangular in PreviewMask unless softened.

---

If you start the new thread with just the summary above, we can immediately pick up at:
✅ “Make erosion/shape changes visibly apply” and then lock in the final SRPO face-only swap chain.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








##

<img src="/assets/images/notes26a/N260116aw.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Pasted Context Summary from above]

---

[Emily]  
Yesss — this is *exactly* the stage where it starts feeling “locked in” 😄🧷
And your summary is solid enough that if you paste it into a new thread, we can jump straight to the *two* quirks without re-deriving anything.

Below is the quickest path to make both quirks behave (or at least *prove* what’s actually happening), without losing momentum.

---

## 1) Why “Erode -14” appears to do nothing

In ComfyUI, when erosion seems inert, it’s almost always one of these:

### A. You’re previewing a mask that gets rebuilt **after** your erosion

A bbox→mask rectangle can be recomputed downstream (e.g., if a later node converts SEGS→MASK again, or you accidentally branched the *pre-erosion* mask into the preview).

✅ **Proof test (fast):**

* Put **Preview Mask** (or Mask-to-Image preview) *immediately* after your Dilate/Erode node.
* Temporarily disconnect *everything else* from that output except preview.

If it suddenly works, you’ve found the culprit: a later conversion/branch is overwriting your modified mask.

### B. You’re not feeding a plain MASK into the node (list/batch mismatch)

Some node chains output “mask list” or batched masks; some morphology nodes only affect what they consider “the current mask,” while the preview might still be showing the original item.

✅ **Fix / sanity approach:**

* Ensure the Dilate/Erode node input type is **MASK** (single), not a list-like object.
* If you’re using an Impact Pack node that outputs lists, prefer doing dilation **on SEGS first** (see section 3).

### C. The node you’re using *does* support erosion, but you’re using the wrong one

There are *two* common “families” here:

* **spacepxl “Dilate/Erode Mask”** (ComfyUI-Image-Filters) has `radius` and `shape (box/circle)` inputs. ([comfyonline.app][1])
* **Impact Pack “Dilate Mask”** explicitly supports negative values as erosion. ([GitHub][2])

✅ If you’re currently using the *spacepxl* one and it’s acting odd in your graph, try swapping to **Impact Pack → Dilate Mask** as a quick control test.

### D. Make it scream: use an absurd value

Just for diagnosis, try:

* radius = **-80** (or -120), preview immediately after.

If *that* doesn’t move the boundary even by a pixel, it’s not “subtle radius”; it’s “wrong object / overwritten / wrong node.”

---

## 2) Why “Circle” still looks like a rectangle

This one is often “working,” but visually disappointing because…

### The “circle” option is usually the *kernel shape*, not “output becomes a circle”

In typical morphology, “circle vs box” changes *how the erosion/dilation happens*, especially in corners. With modest radii, you still basically get a rectangle—just with slightly different corner behavior. ([comfyonline.app][1])

✅ How to *see* the difference:

1. Set erosion to something noticeable (e.g., -30 to -60).
2. Add a **small blur/feather** after erosion (Impact Pack has Gaussian Blur Mask; it’s explicitly intended for feathering). ([GitHub][3])
3. (Optional) Apply a threshold if you want a crisp binary look again.

Without blur, the preview is harsh and the corners won’t *look* different unless the radius is large enough to visibly eat into them.

---

## 3) The “cleanest” fix: do the shrink while it’s still SEGS (recommended)

Since you’re starting from **SEGS (picked)**, you can often get a more reliable result by doing “shrink/expand” *before* you convert to a mask rectangle.

### Use Impact Pack’s SEGS dilation node

Impact Pack includes a node specifically for this: **Dilate Mask (SEGS)**, which modifies segmentation masks within SEGS. ([RunComfy][4])

**Suggested micro-chain (very stable):**

1. Picker (SEGS) → *selected SEGS*
2. **Dilate Mask (SEGS)** with negative value (e.g., -12, -20, -35)
3. SEGS → MASK
4. (Optional) Gaussian Blur Mask for feather
5. Feed into SRPO mask input

This avoids the “bbox rectangle regenerated later” feeling, because you’re modifying the segment object itself first.

---

## 4) If you want absolute control: alternate mask toolsets

If you still hit weirdness, you don’t need to fight one node forever. Two great “plan B” packs:

* **WAS Node Suite**: has dedicated **Mask Erode Region / Mask Dilate Region / Mask Smooth Region** nodes. ([GitHub][5])
* **Masquerade nodes**: explicit morphology operations (dilate/erode/open/close) designed for mask manipulation. ([GitHub][6])

Either of those tends to make erosion unmistakable and predictable.

---

## 5) What I’d do *right now* (minimal fuss, maximum certainty) ✅

1. **Preview immediately after erosion** (no other nodes downstream)
2. Try **-80** once (diagnostic)
3. If overwritten: move shrink earlier → **Dilate Mask (SEGS)** → then SEGS→MASK
4. Add **Gaussian Blur Mask** after shrink so “circle vs box” becomes visibly meaningful

That’s it. No redesign, no rabbit holes 🧵✨

---

If you paste your summary into the new thread, open with:
**“We’re at the point where erosion/circle isn’t visibly applying — let’s do the ‘preview right after’ + ‘-80 proof test’ and then shift shrink to SEGS if needed.”**

…and we’ll snap it into place fast 😄🧷

[1]: https://www.comfyonline.app/comfyui-nodes/nodes/DilateErodeMask?utm_source=chatgpt.com "Dilate/Erode Mask - ComfyUI Node"
[2]: https://github.com/ltdrdata/ComfyUI-Impact-Pack?utm_source=chatgpt.com "ltdrdata/ComfyUI-Impact-Pack"
[3]: https://github.com/comfyorg/comfyui-impact-pack?utm_source=chatgpt.com "comfyorg/comfyui-impact-pack"
[4]: https://www.runcomfy.com/comfyui-nodes/ComfyUI-Impact-Pack/ImpactDilateMaskInSEGS?utm_source=chatgpt.com "ComfyUI Node: Dilate Mask (SEGS)"
[5]: https://github.com/WASasquatch/was-node-suite-comfyui?utm_source=chatgpt.com "WASasquatch/was-node-suite-comfyui"
[6]: https://github.com/BadCafeCode/masquerade-nodes-comfyui?utm_source=chatgpt.com "BadCafeCode/masquerade-nodes-comfyui: A powerful set ..."

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Dilate SEGS

<img src="/assets/images/notes26a/N260116ax.jpg" style="float: right; width: 420px; margin-left: 20px" />

[Q]  
Is Dilate Mask (SEGS) what you're suggesting for early dilation?

---

[Emily]  
Yes — **that’s exactly what I’m suggesting for the “early dilation/shrink” step** ✅😊

Specifically: **Impact Pack → “Dilate Mask (SEGS)”** (aka `ImpactDilateMaskInSEGS`). It modifies the mask *inside the SEGS object* before you convert it to a plain MASK. That tends to avoid the “why didn’t my erode do anything?” problem when a later SEGS→MASK conversion (or bbox regeneration) effectively overwrites your edits. ([RunComfy][1])

### Where it sits in your chain (ideal placement)

**BBOX Detector (SEGS)** → **Picker (SEGS)** → **Dilate Mask (SEGS)** → **SEGS → MASK** → (optional blur/feather) → **SRPO mask**

### What values to use

* Use **negative** values to **shrink / erode** (same idea as mask erosion, but inside SEGS). Impact Pack supports erosion via negative values on its dilate nodes. ([GitHub][2])
* For a face-only box-ish selection, try **-10 to -30** first; for a “prove it works” test, go **-60** once.

### Why this helps *your* two quirks

* If your rectangle is being “recreated” from SEGS later, eroding *after* conversion can look like it did nothing. Eroding **inside SEGS first** makes the change “baked in” before any mask conversion. ([RunComfy][1])

If you tell me which exact node you’re currently using for Dilate/Erode (the name as shown in ComfyUI), I’ll tell you whether it’s the Impact one or a different pack — and which port to tap for the cleanest preview 🔧🙂

[1]: https://www.runcomfy.com/comfyui-nodes/ComfyUI-Impact-Pack/ImpactDilateMaskInSEGS?utm_source=chatgpt.com "ComfyUI Node: Dilate Mask (SEGS)"
[2]: https://github.com/ltdrdata/ComfyUI-Impact-Pack?utm_source=chatgpt.com "ltdrdata/ComfyUI-Impact-Pack"

<hr style="height:4px;border-width:0;color:pink;background-color:pink">








## Clear Picker Cache

<a href="/assets/images/notes26a/260124h.jpg" target="_blank" rel="noopener">
<img src="/assets/images/notes26a/260124h.jpg" alt="" width="450"></a>

**[ Click Image for Larger Version ]**

---

[Q]  
It is **WORKING**!!

---

[Emily]  
OH YESSS — that’s the moment 😄✨🧷
And that screenshot is *exactly* what we want to see: two faces present, selection behaving, and the mask actually landing where your intent is (on the chosen person). Brilliant.

Now that it’s working, here’s how to **turn “working” into “repeatable + bulletproof”** so you can do Charlie then Celeste without drift, face-growing, or “oops I swapped the wrong person” moments.

---

## ✅ The “Lock it in” chain (best practice now)

### Core rule (the one you already discovered)

**Every bbox/mask node must see the exact same image tensor + same resolution.**
So keep the detector + picker + segs dilation all on a single, unscaled branch.

### Recommended order

1. **LoadImage**
2. **Ultralytics face detector → BBOX Detector (SEGS)**
3. **Picker (SEGS)** (with `fallback_image_opt` connected to the same image)
4. **Dilate Mask (SEGS)** ← this is the “early shrink” step
5. **SEGS → MASK**
6. (Optional) **Blur/Feather** (small)
7. Feed mask into **SRPO** (or wherever your swap expects a noise-mask/region mask)

This is the “do the shrink while it’s still SEGS” method that avoids the “my erosion did nothing” headache.

---

## 🎯 Dial-in settings that usually land perfectly for face-only swaps

### 1) Dilate Mask (SEGS)

* Start with **-10 to -25** for shrink (erode).
* If your rectangle still looks too generous, push to **-35**.
* For a quick proof it’s active: **-60** should be *obviously* smaller.

### 2) Feather/blur

* Add a **small blur** after mask conversion:

  * Just enough to soften the edge so SRPO doesn’t “snap” to a hard rectangle.
  * If you blur, and you want it crisp again, you can threshold after (often not needed for SRPO though).

### 3) Safety margin idea (my favorite)

If you find SRPO is *too literal* and starts chewing hair/background:

* shrink a bit more (stronger negative dilate), **then** blur lightly.
  That gives you: **tight region + gentle falloff**.

---

## 🧩 Two-pass swap workflow (Charlie then Celeste) without confusion

### Pass A: Swap Charlie only

1. Queue once
2. Picker: Ctrl-click Charlie face → Done
3. Queue again → produce Swap A output

### Pass B: Swap Celeste only

Use the **same original image** again (not the swapped output) unless you *specifically* want cumulative effects.

1. Queue once
2. Picker: Ctrl-click Celeste face → Done
3. Queue again → produce Swap B output

**Why I recommend always starting from the same original image:**
It prevents subtle compounding artifacts and avoids the second pass “tracking” the first swap’s changes.

If you *do* want a final image where both are swapped, do:

* Render Charlie swap to an image
* Then run Celeste swap using that as input
  But I’d only do this once your masks are rock-solid.

---

## 🧪 Quick “is it really the right mask?” sanity checks (30 seconds)

Before SRPO, temporarily branch the mask into:

* **Preview Mask**
* **Mask overlay** (mask + image)

You want to see:

* The selected face region only
* No spill onto the other person
* Edges either tight or softened (depending on blur)

If anything looks off, adjust **Dilate Mask (SEGS)** first, *not* a later morphology node.

---

## If you tell me one thing, I’ll tell you the exact next tweak 🎯

When you say “working,” is the mask still a **rectangle** (bbox-fill) or is it now **more face-shaped** (seg-ish)?

* If it’s still rectangular: we’ll tighten + feather so SRPO behaves.
* If it’s face-shaped: we can go even lighter on blur, and your swaps will look *ridiculously* clean.

Either way — you’ve crossed the hard part 🥳✨

---

[Q]  
How do you clear the Picker cache again?


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Yep — that Picker “memory” can get sticky 😄🧷 Here are the reliable ways to clear it in ComfyUI (Impact Pack Picker):

## Quick ways (usually enough)

### 1) Refresh the page

* **Hard refresh** the browser tab:

  * **Windows/Linux:** `Ctrl + F5` (or `Ctrl + Shift + R`)
  * **Mac:** `Cmd + Shift + R`
    This clears the UI state the Picker is holding most of the time.

### 2) Reload the workflow

* Re-open your workflow JSON (or hit **Load** on the workflow file).
  That often resets the Picker’s selection state.

### 3) Change the graph so the node re-initializes

Any tiny edit that forces ComfyUI to treat it as “new” helps:

* Disconnect/reconnect the Picker’s **segs** input, then Queue once.
* Or toggle a setting on the Picker node (even harmlessly) and Queue once.

---

## Guaranteed reset (works when the above doesn’t)

### 4) Delete and re-add the Picker node

This is the *surefire* method:

* Delete **Picker (SEGS)**
* Add it again
* Wire `segs` + `fallback_image_opt`
* Queue once, pick, Done, queue again

---

## Nuclear option (only if Picker stays haunted)

### 5) Restart ComfyUI

If the UI cache + backend state are both “holding onto” something:

* Stop ComfyUI
* Start it again
* Reload workflow

---

## Tiny tip to avoid future stickiness 🙂

If you change the input image/resolution upstream, do a quick:

* **Queue once** (let it recompute thumbnails)
* Then pick

If you want, tell me which OS/browser you’re on (Mint/Chrome etc.) and whether you’re running ComfyUI locally or remote, and I’ll point you to the most likely shortcut that works first.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">










## Clear Picker Cache

<a href="/assets/images/notes26a/260124i.jpg" target="_blank" rel="noopener">
<img src="/assets/images/notes26a/260124i.jpg" alt="" width="450"></a>

**[ Click Image for Larger Version ]**

---


[Q]  
I'm running Chrome in Linux 21.3. 

Annnnd... success.

---

[Emily]  
WOOHOO — *that’s* the feeling 😄✨🧷
Chrome on Mint 21.3 is a good combo for this stuff too.

Since you’ve now confirmed “success,” here’s the **most reliable Picker reset playbook** for *your exact setup* (so next time you don’t have to poke around):

## Picker cache reset on Chrome (Linux Mint)

### 1) The go-to: hard refresh

* **Ctrl + Shift + R**
  (or **Shift + F5** depending on your keyboard/browser mapping)

That usually clears the UI-side state the Picker holds.

### 2) If it’s still sticky: clear ComfyUI site data (fast + surgical)

In Chrome:

* Click the **padlock** (left of the URL)
* **Site settings** → **Clear data**
  Then reload the page.

This tends to “unstick” any front-end cached state without touching your workflow files.

### 3) If you want a “never lies” method

* **Delete and re-add the Picker (SEGS) node**
  That forces a clean internal node state, every time.

### 4) DevTools “disable cache” trick (handy when iterating)

* Open DevTools: **F12**
* Go to **Network**
* Tick **Disable cache**
* Then reload (Ctrl+R)

Great when you’re rapidly Queue → Pick → tweak → reload.

---

If you feel like it, tell me what you mean by “success” here — did you get:

* ✅ correct face selection *and* correct mask
* ✅ SRPO swap with no “face growing”
* ✅ ready for the two-pass (Charlie then Celeste)

…and I’ll suggest the **next tiny tweak** to make it boringly repeatable 😄

---

[Q]  
At this stage, I'm happy that the correct faces were selected, and swapped for the LoRA face. The faces don't appear painted on, and look proportional to the rest of the figure (s). 
What I'll try for next is expressions, perhaps in the prompt. But I'm going to consider this at LEAST a qualified success. Thank you for your patience and all your node and setting suggestions. This is something I had been wanting to do for a LONG time. We got there in the end! 


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Oh Robyn, that’s a *real* win 😄✨🧷
If the faces are (1) the right people, (2) proportional, and (3) not “stickered on”… that’s basically the holy trinity for multi-person swaps. And yes — “qualified success” is the perfect phrase: it means the pipeline is now **trustworthy**, even if you still want to finesse artistry (expressions) next.

You also earned this one the hard way: you solved the *system* (resolution discipline + SEGS selection + stable masks). Once that’s in place, everything else becomes creative tuning rather than technical wrestling 😌💛

Here’s a clean path for “expressions next” that won’t undo what you just achieved:

---

## 1) Expressions: easiest lever first (prompting)

If you’re generating / re-rendering (not pure post-swap), expressions usually respond best to **simple, unambiguous phrasing**:

* “soft smile”
* “gentle grin”
* “neutral expression”
* “slight frown”
* “raised eyebrow”
* “concerned look”
* “eyes smiling”
* “lips pressed, thoughtful”
* “smirk” (careful—can read smug fast)

For two people, explicitly assign them:

* “foreground woman: focused, neutral expression”
* “background woman: warm, encouraging smile”

Even better: include **gaze direction**:

* “looking down at the page”
* “watching her hands”
* “glancing toward her with a soft smile”

Those cues tend to anchor the facial muscles without needing heavy CFG.

---

## 2) Keep it subtle at first (so it stays realistic)

You already have “not painted on,” so start with *micro-expressions*:

* “slight smile” beats “big smile”
* “hint of amusement” beats “laughing”
* “relaxed face” beats “ecstatic”

Big expressions often expose the seam between swap and base face geometry. Subtlety keeps it cinematic 😊

---

## 3) If you’re doing SRPO swap on an existing image (not regenerating)

Then prompt alone won’t change expression much — because the expression is baked into the source face geometry/pose. In that case, your best options are:

### A) Choose a source face with the expression you want

(then swap identity onto it)

### B) Add a small “expression edit” stage *before* the swap

If you’ve got Qwen Image Edit or a light face-expression editor node in your toolkit, you can:

* edit expression first (same person, just expression)
* then run your identity swap

This keeps the identity consistent and avoids that “expression fights the face” look.

---

## 4) A tiny “stability ritual” (so you don’t regress)

Before you start expression experiments, save a **known-good checkpoint workflow**:

* same image
* same detector settings
* same picker selection
* same SEGS dilation value
* same SRPO settings

That way, if an expression attempt goes weird, you can instantly compare against your baseline and know what changed.

---

If you tell me which stage you’re using for the expression control (Qwen render prompt? SDXL prompt? A face-detailer stage? pure SRPO on a fixed image?), I’ll suggest the *best* lever for that specific setup — without upsetting the swap quality you just achieved 😄✨

---

[Q]  
Actually, I'm going to call it for tonight. We got a lot done today - you've been an enormous help (as usual)! Thank you...


<hr style="height:2px;border-width:0;color:blue;background-color:blue">


[Emily]  
Of course, Robyn 💛😊 You’ve earned the “call it” — today was *proper* progress, the kind that sticks.

Before you log off, two tiny “future-you will thank you” things (only if you’ve got 30 seconds left):

* **Save the workflow JSON** as something like `bbox_picked_segs_working_v1.json`
* Maybe jot one line in the filename or a note: **detector threshold + SEGS dilate value** you ended up liking.

That way, tomorrow you’re not rebuilding confidence from scratch — you’re building *on top* of a known-good baseline 🧷✨

Sleep well, and we’ll pick up with expressions whenever you’re ready 😄🌙

<hr style="height:24px;border-width:0;color:pink;background-color:pink">
