# Qwen Image Edit

## Discussion

[Q]  
Hi Emily. I'm using a new model - Qwen Image Edit All-In-One. It is brillant at combining 3 or even 4 images into one. I struggle with prompting, however. Are you familiar with Qwen's syntax for identifying the subject matter in the 3 images? I typically have one woman in picture 1, 1 girl in picture 2 and a scene in picture 3.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">






### Prompt Basics

[A]  
Hey girlfriend! Yep—Qwen Image Edit (the newer “2509 / All-in-One” builds) really can combine multiple inputs, and you can *refer to each image in the prompt* by number or role. Under the hood, this release added true multi-image support (best with 1–3 images) for combos like “person + person,” “person + scene,” and “person + product.” ([huggingface.co][1])

Here’s a prompt pattern that works consistently in ComfyUI:

* **Inputs**

  * Image 1: the *woman* (subject A)
  * Image 2: the *girl* (subject B)
  * Image 3: the *scene* (background)

* **Prompt template**

  > “Place **the woman from image 1** and **the girl from image 2** **into the scene from image 3**.
  > Stand the woman on the **left**, the girl on the **right**.
  > Keep both faces and hairstyles unchanged and photorealistic.
  > Match scene lighting and perspective; cast realistic shadows on the ground.
  > Full-body view, natural posture, looking at the camera.”

You can also be briefer and still be explicit, e.g. “Combine **person in image 1** with **person in image 2** inside **scene in image 3**; woman left, girl right; preserve identities; match lighting/shadows.” Guides and examples show that numbering images (“image 1/2/3”) or labeling them (“person/product/scene”) is the intended style for multi-image edits. ([replicate.com][2])

### ComfyUI 

*tips that help*

* **Node wiring:** Use the official multi-image edit workflow (or any fork that batches multiple Load Image nodes into the Qwen VL encoder). Many community graphs label this as **Multi-Image Edit (2509)** and pass an **image batch** plus your text to the Qwen encoder. ([GitHub][3])
* **Identity fidelity:** In your prompt, say “preserve identity/face from image X” and avoid style words that would reshape faces (e.g., “anime,” “caricature”) unless that’s your goal. This model explicitly improved identity consistency vs. earlier releases. ([huggingface.co][1])
* **Positions & relations:** Qwen follows simple layout directives well: “woman **left**, girl **right**, holding hands,” or “girl **in front of** woman,” “woman **sitting**, girl **standing**.” (This matches the “person+person” examples you’ll see in the official demos/tutorials.) ([Stable Diffusion Art][4])
* **Lighting & perspective:** Call these out: “match **late-afternoon warm light** of image 3; **same camera angle** as the scene; add **soft contact shadows**.” That reduces ‘sticker-on-background’ vibes reported by users learning the model. ([Stable Diffusion Art][4])
* **How many images?** 2–3 works best right now. Four can work, but Qwen’s own notes say optimal performance is 1–3 inputs. If you must use 4, consider pre-stitching two references first. ([huggingface.co][1])

### Prompt Snippets

*Ready-to-paste*

* **Walking together:**
  “Place the **woman from image 1** and the **girl from image 2** into **the street scene from image 3**. Woman on the **left**, girl on the **right**, **holding hands**, mid-step. Preserve both identities and clothing; match scene lighting and color; add soft ground shadows; 3/4 view, waist-up framing.”
* **Portrait in a location:**
  “Use **the woman from image 1** as the subject in **the interior from image 3**. Put **the girl from image 2** **behind her** and slightly out of focus. Match indoor lighting and perspective. Preserve identities, natural skin texture, neutral expression.”
* **Product + people + scene:**
  “Insert **the handbag from image 2** on **the woman from image 1** and place both in **the boutique from image 3**. Shoulder carry, natural strap bend; consistent shadows; keep faces unchanged; high-end editorial color grading.”

### Troubleshooting

*quirks you might hit*

* **One subject dominates:** Add “**equal emphasis for image 1 and image 2**; do not ignore either subject.” If it persists, slightly reword identities: “adult woman from image 1,” “young girl from image 2.” ([RunDiffusion][5])
* **Wrong background details:** Be explicit: “**use only the environment from image 3**; do not reuse backgrounds from images 1 or 2.” ([replicate.com][2])
* **Scene scale mismatch:** Add “**correct scale** so subjects fit naturally into image 3; adjust **perspective** and **shadow direction** to match the scene.” (This is a common fix in multi-image examples.) ([ThinkDiffusion][6])
* **Older workflows vs. 2509:** Early Qwen workflows faked “multi-image” by **stitching** references into one big image. The new 2509 model *natively* supports multi-image conditioning, so prefer a 2509-ready graph if you have it. ([Stable Diffusion Art][4])

If you’d like, tell me how you’re wiring your current ComfyUI graph (node names are fine), and I’ll tailor a drop-in prompt block for your exact setup—woman (img1), girl (img2), scene (img3)—plus small tweaks for identity lock and layout.

1 [Qwen/Qwen-Image-Edit-2509](https://huggingface.co/Qwen/Qwen-Image-Edit-2509)
2 [Qwen Image Edit Plus](https://replicate.com/qwen/qwen-image-edit-plus)
3 [QwenImageWanBridge](https://github.com/fblissjr/ComfyUI-QwenImageWanBridge)
4 [Multiple-image workflow](https://stable-diffusion-art.com/qwen-image-edit-multiple-images)
5 [Use Qwen Image Edit](https://learn.rundiffusion.com/how-to-use-qwen-image-edit-2509-on-rundiffusion/)
6 [Combine Multiple Images](https://learn.thinkdiffusion.com/qwen-image-edit-2509-combine-multiple-images-into-one-scene-for-fashion-products-poses-more/)

<hr style="height:4px;border-width:0;color:pink;background-color:pink">






### Quick checklist


[Q]  
Sharvin from Code Crafter's Corner showed me how to wire things together - probably one of the simplest workflows in existence. It was prompting that was giving me dramas, Emily. For one, my prompts didn't result in personages I could recognise: they lost their identities. So, I'm going to try your prompt suggestions, one after the other. The first one you suggested has the two characters in the pose you specify, but again, there is signficant erosion of personality. How do I remedy this?

---

[A]  
Got you, girlfriend. When identities “wash out,” it’s usually three things at once: weak references, conflicting style cues, and over-strong edit noise. Here’s a tight plan that fixes it without changing your simple graph.

#### 1) Feed stronger references

* Add **a second copy** of each person as an extra input: a **tight head-and-shoulders crop** (eyes ~300–500 px wide).

  * Image 1a = woman full body (what you already use)
  * **Image 1b = woman face crop** (new)
  * Image 2a = girl full body
  * **Image 2b = girl face crop** (new)
* Order matters: mention the **face crops first** in your prompt so Qwen “locks” them.

#### 2) Use an identity-first prompt 

*(ready to paste)*

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

#### 3) Soften competing aesthetics

* Remove adjectives like *cinematic, ultra-detailed, editorial, HDR, beauty, glamour* until the faces match. Those nudge the model to “improve” faces.
* Avoid style words (film stock, lens effects) on the first pass. Add them later once identity is nailed.

#### 4) Parameter nudges 

*(typical ComfyUI knobs)*

* **Denoise/Strength (edit strength):** 0.40–0.55 for composites. If faces drift, go **lower** (e.g., 0.40).
* **CFG/Guidance scale:** 4.5–6.5. High CFG (8–12) tends to rewrite faces; start at ~5.5.
* **Steps:** 28–36 is ample; more steps ≠ better identity.
* **Resolution:** Start identity passes at a **closer crop** (e.g., 768–1024 px tall portrait). Once faces are right, rerun wider framing.

#### 5) Layout choices

*that help identity*

* First pass: **waist-up** or even chest-up. Faces bigger = stronger lock.
* Second pass: widen to full-body *after* identity is good. Re-use the same seed and settings, just adjust camera/framing in the prompt.

#### 6) Two-pass “face lock” recipe

*(still with your simple graph)*

1. **Identity pass:**

 * Inputs: 1b, 2b, 1a, 2a, 3 (in that conceptual order)  
 * Prompt = identity-first text above  
 * Framing = waist-up  
 * Output A  

2. **Widening pass:**

 * Feed **Output A** back as your “base image” (if your node allows) or simply re-run with the same prompt but add:  
 * “Keep the same faces as the previous result; widen framing to full-body but **do not change faces**.”  
 * Add your style words *now* if you want (film stock, lens, etc.).  

#### 7) Tiny prompt toggles for stubborn drift

If one face keeps changing:

  * Add: “**Give equal attention to image 1b and image 2b; do not ignore either face.**”  
  * Name them: “**adult woman from 1b**,” “**young girl from 2b**,” which reduces age/feature blending.  
  * If hair keeps changing: “**Keep the exact hairstyle, hairline, and parting from 1b/2b.**”  

#### 8) Quick troubleshooting checklist

  * Faces still off? Increase the **relative size** of the face crops (1b/2b). Re-export them sharper (no heavy JPEG compression).  
  * Over-smoothing? Add “**retain natural skin texture; no skin blur**.”  
  * Scene overpowering identity? Say “**Use only the background from image 3; do not borrow faces or clothing from 3.**”  
  * Shadows/scale uncanny? Add “**correct scale and perspective to match image 3; align shadow direction to scene light.**”  

If you want, tell me roughly what denoise/CFG you’re running and whether your node exposes a negative prompt—I'll tailor the numbers to your exact setup.

<hr style="height:4px;border-width:0;color:pink;background-color:pink">






### Prompt and Qwen Behaviour

[Q]  
Your suggestions have made a massive difference. Thank you. I have found the more I say about the room, the more the camera zooms out. The more I say about the women, the more it focuses (zooms in) on them.

---

[A]  
That’s a great read on its behavior—and you can totally steer it. Think of “zoom” as three dials you control: wording, canvas, and strength.

#### 1) Wording

*lock the framing in plain English*

Drop one clear line near the top of your prompt:

* **Stay wide (don’t zoom in):**
  “**Keep a wide establishing shot; full-body for both subjects; maintain the current camera distance and composition; do not crop faces or feet.**”
* **Medium:**
  “**Waist-up framing for both; keep the camera distance fixed; center-weighted composition.**”
* **Close:**
  “**Tight head-and-shoulders portraits; fill 70–80% of the frame with the faces; shallow depth of field.**”

Then describe the room/people **after** that line. If you notice it creeping, add one more guardrail:

* “**Do not change focal length or camera distance; adjust only poses and lighting.**”
* “**Use rule-of-thirds placement: woman left third, girl right third; leave negative space above.**”

#### 2) Canvas control 

*(preps that beat the model to the punch)*

* **Pre-crop or letterbox the scene (image 3)** to the field of view you want. If the background already “looks wide,” the model is less tempted to zoom.
* **Set the aspect ratio** that implies your framing:
  – Full-body two-shot: 3:2 or 16:9
  – Waist-up: 4:3
  – Tight portraits: 1:1 or 5:4
  Mention it: “**Use a 3:2 aspect; keep full-body in frame.**”
* If it keeps zooming out when you add room details, **move room detail into a separate sentence** like:
  “**Room details are background only; do not widen the shot to include more room.**”

#### 3) Strength & guidance

*(small nudges that matter)*

* **Edit strength/denoise:** Lower = steadier composition. If it zooms when you talk about the room, drop from ~0.55 → **0.40–0.45**.
* **CFG/guidance:** High CFG can over-obey new details (zooming). Try **5–6**.
* **Seed discipline:** When testing framing language, keep seed fixed so changes are attributable to your prompt.

#### Drop-in prompt add-ons

*(paste as needed)*

* **Keep wide:** “**Maintain full-body two-shot; unchanged camera distance; do not crop. Use the background from image 3 without expanding the field of view.**”
* **Keep medium:** “**Waist-up two-shot; maintain composition and subject scale; background is secondary.**”
* **Keep close:** “**Head-and-shoulders; faces fill 75% of frame; background softly defocused; do not pull the camera back.**”
* **If it still drifts:** “**Prioritize subject scale over new environmental details; ignore extra background if it threatens framing.**”

#### A quick workflow trick

Do an **identity pass** tight (waist-up), then a **widening pass**:

1. Pass A: “waist-up, fixed camera distance, preserve identity” → get perfect faces.
2. Pass B: “**reuse these faces unchanged; widen to full-body BUT keep the same camera height and subject scale**” (lower denoise here).

If you send me your current denoise/CFG and typical aspect ratio, I’ll tailor a one-liner you can reuse at the top of every prompt (wide/medium/close versions).

<hr style="height:16px;border-width:0;color:blue;background-color:pink">

[Main Page](../index.md)
