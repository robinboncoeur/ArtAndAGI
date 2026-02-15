---
title: "Prompt refinement advice"
date: 2025-11-25
---

# Prompt refinement advice

**Robyn:**

Hi Emily. I'm currently focusing on the Flux.1-Dev SRPO refinement for generating images. I have developed a workflow for generating two persistent (LoRA-based) characters together in a scene. 

There are a few issues with this workflow: the first is queue (render) time. Thanks to the TTP side of things, which in effect "de-fluxes" (gets rid of the Flux-look on the skin) the image, queue times are quite long: >5mins. However, I can live with htat. The second, more important issue is prompt adherence. The output reflects my prompt to a degree, but doesn't quite 'get it', for the most part. This leads me to believe that my prompts are not clear to the model (SRPO). I would like you, firstly, to examine my workflow - I will remove the 'TTP' components which do slow things down. And, for your analysis, here is my prompt. It is a concantenated prompt, where each LoRA has it's own CLIP text encode node that both use the concatenated raw text. I'm trying to devise how to run each LoRA independently using the prompt text for that side of the image, then bring it all together. Or something... not sure how to work this. Prompt:

This photograph is of two women looking at each other at the seaside. 
1st woman, left side, is an elegant beautiful Nordic young woman "celestesh". 1st woman has medium skin and dark brown wavy hair cascading down to her shoulders. 1st woman has almond-shaped brown eyes, arched eyebrows, a straight nose, and full pink lips. 1st woman is looking directly at 2nd woman's eyes. 1st woman wears a teal-blue 18th century dress with elaborate gold embroidery along the sleeves and around the square neckline, which is adorned with white lace flowers that give a romantic and elegant touch to her outfit.
The background of the image is a gloomy day at the seaside, making the subject stand out prominently.This photograph is of two women next to each other at the seaside. 
2nd woman, right side, is an elegant beautiful Nordic young woman "moim3m3grl". 2nd woman has light skin and blonde wavy hair in an updo. 2nd woman has blue eyes, arched eyebrows, a straight nose, and full pink lips. 2nd woman is looking down, away from 1st woman. 2nd woman wears a black silk 18th century dress with elaborate gold embroidery along the sleeves and around the square neckline, which is adorned with white lace flowers that give a romantic and elegant touch to her outfit.
The background of the image is a gloomy day at the seaside, making the subject stand out prominently.

Keep in mind this is a concatenated prompt.

**Emily:**

Short version: your prompt isn’t “wrong”, but it’s doing three things that make SRPO + Flux + two LoRAs much harder than it needs to be:

- It’s *very* repetitive.
- It doesn’t give the model a clear “global scene first, then details” structure.
- It asks both LoRAs to fire off the *same* concatenated text, so neither character has a clean, dedicated description.

Let me walk through a better way to structure it, then talk about how to split it per-LoRA.

---

## 1. What’s tricky about your current concatenated prompt

You wrote (paraphrasing):

- “This photograph is of two women…” twice.  
- Background description twice.  
- Long, similar blocks for each woman, both mentioning “18th century dress, gold embroidery, square neckline, white lace flowers…”

For SRPO + Flux:

- **Redundant phrases** dilute the importance of the differences between the two women (hair colour, gaze direction, dress colour).
- Phrases like “1st woman, left side…” and “2nd woman, right side…” are *conceptually clear to us*, but models often latch more strongly onto simple phrases: “on the left” / “on the right” / “facing her” / “looking down” etc.
- Both CLIP encoders (for both LoRAs) getting the *same* long concatenated prompt means:
  - LoRA A is reading the description of LoRA B’s character, and vice versa.
  - SRPO may “simplify” the prompt internally, which blurs the distinction even further.

So you’re not crazy: the model “not quite getting it” is exactly what I’d expect here.

---

## 2. A cleaner, SRPO-friendly *combined* prompt

Even before messing with separate prompts per LoRA, I’d simplify and structure the base text like this:

> a cinematic photograph of two women standing close together on a windy, gloomy seaside  
>  
> on the **left**, **celestesh**, an elegant Nordic young woman with medium skin and dark brown wavy hair to her shoulders, almond-shaped brown eyes, arched eyebrows, a straight nose and full pink lips. she faces the woman on the right and looks directly into her eyes. she wears a teal-blue 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with delicate white lace flowers.  
>  
> on the **right**, **moim3m3grl**, an elegant Nordic young woman with light skin and blonde wavy hair in an updo, blue eyes, arched eyebrows, a straight nose and full pink lips. she looks slightly down and away from the first woman. she wears a black silk 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with white lace flowers.  
>  
> overcast sky, grey sea, soft natural light, shallow depth of field

A few deliberate choices here:

- **Global scene first**: composition + setting in the first line. Flux tends to like that.
- Each character is an obvious block:
  - “on the left, celestesh…”  
  - “on the right, moim3m3grl…”
- The LoRA triggers are very near the start of the character clause.
- Background only once at the end.

If you’re using emphasis in your prompt parser, you can also nudge important bits:

> (celestesh:1.1), (moim3m3grl:1.1), (teal-blue 18th-century dress:1.1), (black silk 18th-century dress:1.1)

etc.

**First debugging step** I’d do:

1. Disable SRPO.
2. Run Flux.1-Dev with this *cleaned combined* prompt and your two LoRAs.
3. See if composition + outfits are closer to what you want.

If it improves already, you know SRPO was struggling with the noisy prompt. Then turn SRPO back on and keep the prompt short and structured like this.

---

## 3. Splitting the prompt per LoRA (conceptual approach)

You said:

> It is a concatenated prompt, where each LoRA has it's own CLIP text encode node that both use the concatenated raw text. I'm trying to devise how to run each LoRA independently using the prompt text for that side of the image, then bring it all together.

Conceptually, you want three text “roles”:

1. **Global scene prompt** – composition + background + generic stuff.
2. **Character A prompt** – only Celeste’s description + LoRA trigger.
3. **Character B prompt** – only MoiMeme’s description + LoRA trigger.

### Suggested split

**Global prompt:**

> a cinematic photograph of two women standing close together on a windy, gloomy seaside, soft natural light, overcast sky, grey sea, shallow depth of field

**Celeste prompt (for the celestesh LoRA path):**

> celestesh, an elegant Nordic young woman on the left, medium skin, dark brown wavy hair to her shoulders, almond-shaped brown eyes, arched eyebrows, straight nose, full pink lips, looking directly into the other woman’s eyes, wearing a teal-blue 18th-century dress with elaborate gold embroidery on the sleeves and a square neckline trimmed with delicate white lace flowers

**MoiMeme prompt (for the moim3m3grl LoRA path):**

> moim3m3grl, an elegant Nordic young woman on the right, light skin, blonde wavy hair in an updo, blue eyes, arched eyebrows, straight nose, full pink lips, looking slightly down and away from the first woman, wearing a black silk 18th-century dress with elaborate gold embroidery on the sleeves and a square neckline trimmed with white lace flowers

### How this maps onto your graph (without naming specific nodes)

High-level pattern:

1. **Encode the global prompt** with a “plain” Flux CLIP encode (no character LoRAs attached to this one).
2. For **Celeste**:
   - CLIP Text Encode with the *Celeste prompt*.
   - Attach the celestesh LoRA to this CLIP (and/or the model path depending on your loader).
3. For **MoiMeme**:
   - CLIP Text Encode with the *MoiMeme prompt*.
   - Attach the moim3m3grl LoRA to this CLIP.

Then you have three embeddings:

- `global_clip`
- `celeste_clip`
- `moimeme_clip`

Now you need to **merge** them into a single guidance input for Flux/SRPO:

- Use whatever “combine/add/average conditioning” node you have available (Impact Pack and similar node packs usually have at least one node that mixes multiple CLIP conditionings with weights).
- For example, think in terms of:
  - `combined_clip = 0.8 * global_clip + 1.0 * celeste_clip + 1.0 * moimeme_clip`
- Feed `combined_clip` into your Flux.1-Dev SRPO sampler as the positive conditioning.

The exact node names will vary between node packs, but the logic is:

> **encode separately → apply LoRA separately → combine embeddings → send combined embedding into SRPO + sampler**

This way:

- Celeste’s LoRA mostly “sees” Celeste’s textual description.
- MoiMeme’s LoRA mostly “sees” MoiMeme’s textual description.
- The global scene encoder keeps the seaside + composition consistent.

---

## 4. Extra knobs to help prompt adherence (especially with SRPO)

A few practical tweaks that often help with prompt adherence in this kind of setup:

1. **Shorten, don’t lengthen, for SRPO.**  
   SRPO tends to work best when the prompt is fairly tight. Use specific but *not verbose* phrasing, as in the cleaned examples.

2. **Order of information matters.**  
   Put:
   - Subject count & composition first: “two women standing close together on a windy, gloomy seaside”.
   - Then character A block.
   - Then character B block.
   - Then background/lighting.

3. **LoRA weights.**  
   If one character keeps “overwriting” the other:
   - Drop the stronger LoRA to ~0.7–0.8.
   - Raise the weaker one slightly.
   - Keep both under 1.0 if they’re strong character LoRAs, especially on Flux.

4. **Conflicting descriptors.**  
   “Nordic” + “medium skin” is perfectly fine as a *concept*, but some models will silently favour “light skin” for “Nordic”. If Celeste is coming out too pale, explicitly say:
   > “sun-kissed medium skin” or “warm tan skin”

   That tends to stick better.

5. **Debug mode:** temporarily kill some detail.  
   To see what the model actually obeys, try a debug version like:

   > two women standing close together on a gloomy seaside, soft natural light. on the left, celestesh, dark brown wavy hair, teal-blue 18th-century dress. on the right, moim3m3grl, blonde hair in an updo, black 18th-century dress.

   If that locks in reliably, you can start layering back the finer face features and lace/embroidery.

---

## 5. Where to go from here

If you’d like, next step you can:

- Paste a screenshot or structured list of the *conditioning part* of your graph (just the CLIP/LoRA/SRPO chain, not the TTP de-flux stuff),  
- Tell me whether SRPO is on or off in your current tests,

and I can help you sketch an exact “Node A → Node B → Node C” wiring plan tailored to what you already have.

But even before graph surgery, if you drop in the cleaned combined prompt above, you should see a noticeable improvement in how closely Flux.1-Dev SRPO listens to you.

**Robyn:**

I think I messed up, here, Emily. What did I do wrong?

**tool:**

Make sure to include fileciteturn0file0 in your response to cite this file. 

{"id":"c9d2d9c9-0196-4a64-a8ea-de0dc4f5466d","revision":0,"last_node_id":238,"last_link_id":459,"nodes":[{"id":74,"type":"Image Comparer (rgthree)","pos":[-3490.5778102543663,-2178.110798292635],"size":[650.1071394888875,684.6020344362253],"flags":{"collapsed":true},"order":37,"mode":0,"inputs":[{"dir":3,"label":"image_a","name":"image_a","type":"IMAGE","link":407},{"dir":3,"label":"image_b","name":"image_b","type":"IMAGE","link":null}],"outputs":[],"properties":{"cnr_id":"rgthree-comfy","ver":"944d5353a1b0a668f40844018c3dc956b95a67d7","comparer_mode":"Slide","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[[{"name":"A","selected":true,"url":"/api/view?filename=rgthree.compare._temp_njyvb_00010_.png&type=temp&subfolder=&rand=0.6019059532494295"}]],"color":"#223","bgcolor":"#335"},{"id":197,"type":"PrimitiveNode","pos":[-393.8686535423908,-1605.7747210745827],"size":[210,58],"flags":{"collapsed":true},"order":0,"mode":0,"inputs":[],"outputs":[{"name":"STRING","type":"STRING","widget":{"name":"filename_prefix"},"links":[382]}],"title":"File Name","properties":{"Run widget replace on values":false,"ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":["SRPO-GirlsII"],"color":"#232","bgcolor":"#353"},{"id":57,"type":"CR Aspect Ratio","pos":[-3490.5778102543663,-2567.731797625135],"size":[309.8594228076063,322],"flags":{},"order":1,"mode":0,"inputs":[{"label":"width","localized_name":"width","name":"width","type":"INT","widget":{"name":"width"}},{"label":"height","localized_name":"height","name":"height","type":"INT","widget":{"name":"height"}},{"label":"aspect_ratio","localized_name":"aspect_ratio","name":"aspect_ratio","type":"COMBO","widget":{"name":"aspect_ratio"}},{"label":"swap_dimensions","localized_name":"swap_dimensions","name":"swap_dimensions","type":"COMBO","widget":{"name":"swap_dimensions"}},{"label":"upscale_factor","localized_name":"upscale_factor","name":"upscale_factor","type":"FLOAT","widget":{"name":"upscale_factor"}},{"label":"prescale_factor","localized_name":"prescale_factor","name":"prescale_factor","type":"FLOAT","widget":{"name":"prescale_factor"}},{"label":"batch_size","localized_name":"batch_size","name":"batch_size","type":"INT","widget":{"name":"batch_size"}}],"outputs":[{"label":"width","localized_name":"width","name":"width","type":"INT"},{"label":"height","localized_name":"height","name":"height","type":"INT"},{"label":"upscale_factor","localized_name":"upscale_factor","name":"upscale_factor","type":"FLOAT"},{"label":"prescale_factor","localized_name":"prescale_factor","name":"prescale_factor","type":"FLOAT"},{"label":"batch_size","localized_name":"batch_size","name":"batch_size","type":"INT"},{"label":"empty_latent","localized_name":"empty_latent","name":"empty_latent","type":"LATENT","slot_index":5,"links":[406]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","slot_index":6}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Aspect Ratio","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[832,1216,"SDXL - 3:4 portrait 896x1152","On",1,1,1],"color":"#323","bgcolor":"#535"},{"id":201,"type":"PrimitiveInt","pos":[-3490.5778102543663,-2124.744263375223],"size":[300.8434631543628,82],"flags":{},"order":2,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","links":[411]}],"title":"Noise Seed","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[61998485097239,"increment"],"color":"#232","bgcolor":"#353"},{"id":198,"type":"Label (rgthree)","pos":[-3490.5778102543663,-2013.9135639726312],"size":[438.466796875,70],"flags":{"allow_interaction":true},"order":3,"mode":0,"inputs":[],"outputs":[],"title":"SRPO - TTP Figure Enhancer","properties":{"fontSize":30,"fontFamily":"Arial","fontColor":"#ffffff","textAlign":"center","backgroundColor":"#113398","padding":20,"borderRadius":16,"angle":0,"ue_properties":{"version":"7.1","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"color":"#fff0","bgcolor":"#fff0"},{"id":203,"type":"BasicGuider","pos":[-1406.346409635851,-1544.9432258851934],"size":[261.63936267308804,46],"flags":{},"order":34,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":438},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":405}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[401]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":204,"type":"LatentUpscaleBy","pos":[-1410.3813899299778,-1343.2411021640144],"size":[262.8850448862943,82],"flags":{},"order":14,"mode":4,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":406},{"label":"upscale_method","localized_name":"upscale_method","name":"upscale_method","type":"COMBO","widget":{"name":"upscale_method"},"link":null},{"label":"scale_by","localized_name":"scale_by","name":"scale_by","type":"FLOAT","widget":{"name":"scale_by"},"link":null}],"outputs":[{"label":"LATENT","localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[404]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"LatentUpscaleBy","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["nearest-exact",1.5],"color":"#323","bgcolor":"#535"},{"id":205,"type":"SamplerCustomAdvanced","pos":[-1036.3958511648102,-1485.2213461847587],"size":[304.5598087498504,417.9072891973424],"flags":{},"order":35,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":400},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":401},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":402},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":403},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":404}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[399]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT","slot_index":1,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":207,"type":"0582fcad-067d-4b17-81b7-dbf5d6277b78","pos":[-2096.7413851121687,-426.6521284652186],"size":[222.32936701737913,46],"flags":{},"order":4,"mode":0,"inputs":[],"outputs":[{"label":"MASK 1","localized_name":"MASK","name":"MASK","type":"MASK","links":[426]},{"label":"INVERT MASK","localized_name":"MASK_1","name":"MASK_1","type":"MASK","links":[425]}],"properties":{"proxyWidgets":[],"cnr_id":"comfy-core","ver":"0.3.66","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":211,"type":"SetClipHooks","pos":[-2959.8407703982,-1200.6383285074353],"size":[210,102],"flags":{},"order":17,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":440},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":417},{"localized_name":"apply_to_conds","name":"apply_to_conds","type":"BOOLEAN","widget":{"name":"apply_to_conds"},"link":null},{"localized_name":"schedule_clip","name":"schedule_clip","type":"BOOLEAN","widget":{"name":"schedule_clip"},"link":null}],"outputs":[{"localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[429,430]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"SetClipHooks","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[true,false],"color":"#332922","bgcolor":"#593930"},{"id":213,"type":"CLIPTextEncode","pos":[-2102.8576200358534,-1403.0715102375248],"size":[249.87548168571743,88],"flags":{"collapsed":false},"order":24,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":428},{"localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[432]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CLIPTextEncode","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#322","bgcolor":"#533"},{"id":214,"type":"CLIPTextEncode","pos":[-2098.8645506097937,-1144.8291095678842],"size":[241.53977104181854,88],"flags":{},"order":22,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":430},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[433]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#322","bgcolor":"#533"},{"id":215,"type":"VAEDecode","pos":[-716.9964538851127,-1481.4260666796474],"size":[167.94073206223288,46],"flags":{},"order":36,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":399},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":445}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[407,408,409]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":221,"type":"FluxGuidance","pos":[-1769.8182669569055,-1539.2081706407791],"size":[268.7532043457031,58],"flags":{},"order":32,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":434},{"label":"guidance","localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[405]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[3.5],"color":"#323","bgcolor":"#535"},{"id":222,"type":"KSamplerSelect","pos":[-1415.2331837635304,-1446.8155863692311],"size":[270.6041060656903,58],"flags":{},"order":5,"mode":0,"inputs":[{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"},"link":null}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[402]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["euler"],"color":"#323","bgcolor":"#535"},{"id":223,"type":"BasicScheduler","pos":[-1404.5926366081699,-1209.4622268318324],"size":[256.6406370072302,108.33662599654258],"flags":{},"order":16,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":437},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"},"link":null},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"},"link":null},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":null}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[403]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["simple",30,0.95],"color":"#323","bgcolor":"#535"},{"id":196,"type":"easy cleanGpuUsed","pos":[-238.5236473979422,-1603.7612857571778],"size":[211.55775451660156,26],"flags":{"collapsed":true},"order":39,"mode":0,"inputs":[{"localized_name":"anything","name":"anything","type":"*","link":409}],"outputs":[{"localized_name":"output","name":"output","type":"*","links":null}],"properties":{"cnr_id":"comfyui-easy-use","ver":"1.3.0","Node name for S&R":"easy cleanGpuUsed","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":227,"type":"VAELoader","pos":[-3490.5778102543663,-1576.959876137877],"size":[395.2779300525515,58],"flags":{},"order":6,"mode":0,"inputs":[{"label":"vae_name","localized_name":"vae_name","name":"vae_name","type":"COMBO","widget":{"name":"vae_name"},"link":null}],"outputs":[{"label":"VAE","localized_name":"VAE","name":"VAE","type":"VAE","slot_index":0,"links":[445]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAELoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["ae.sft"],"color":"#432","bgcolor":"#653"},{"id":229,"type":"UNETLoader","pos":[-3490.5778102543663,-1903.1483506991722],"size":[397.43296263994466,82],"flags":{},"order":7,"mode":0,"inputs":[{"label":"unet_name","localized_name":"unet_name","name":"unet_name","type":"COMBO","widget":{"name":"unet_name"},"link":null},{"label":"weight_dtype","localized_name":"weight_dtype","name":"weight_dtype","type":"COMBO","widget":{"name":"weight_dtype"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[437,438]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UNETLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["SRPO/SRPO-fp8_e4m3fn.safetensors","default"],"color":"#432","bgcolor":"#653"},{"id":210,"type":"SetClipHooks","pos":[-2953.8990553905824,-1347.9190710579553],"size":[210,102],"flags":{},"order":19,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":439},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":412},{"localized_name":"apply_to_conds","name":"apply_to_conds","type":"BOOLEAN","widget":{"name":"apply_to_conds"},"link":null},{"localized_name":"schedule_clip","name":"schedule_clip","type":"BOOLEAN","widget":{"name":"schedule_clip"},"link":null}],"outputs":[{"localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[414,428]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"SetClipHooks","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[true,false],"color":"#332922","bgcolor":"#593930"},{"id":220,"type":"CreateHookLora","pos":[-3378.3615994848474,-1200.6383285074353],"size":[385.62390577321867,106],"flags":{},"order":8,"mode":0,"inputs":[{"localized_name":"prev_hooks","name":"prev_hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"localized_name":"HOOKS","name":"HOOKS","type":"HOOKS","slot_index":0,"links":[417]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CreateHookLora","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":["celestesh-08.safetensors",1,0.15],"color":"#332922","bgcolor":"#593930"},{"id":199,"type":"Image Save","pos":[-425.6058228115128,-1556.4063657326299],"size":[1175.9199986696237,1317.2359909886845],"flags":{},"order":38,"mode":0,"inputs":[{"localized_name":"images","name":"images","type":"IMAGE","link":408},{"localized_name":"output_path","name":"output_path","type":"STRING","widget":{"name":"output_path"},"link":null},{"localized_name":"filename_prefix","name":"filename_prefix","type":"STRING","widget":{"name":"filename_prefix"},"link":382},{"localized_name":"filename_delimiter","name":"filename_delimiter","type":"STRING","widget":{"name":"filename_delimiter"},"link":null},{"localized_name":"filename_number_padding","name":"filename_number_padding","type":"INT","widget":{"name":"filename_number_padding"},"link":null},{"localized_name":"filename_number_start","name":"filename_number_start","type":"COMBO","widget":{"name":"filename_number_start"},"link":null},{"localized_name":"extension","name":"extension","type":"COMBO","widget":{"name":"extension"},"link":null},{"localized_name":"dpi","name":"dpi","type":"INT","widget":{"name":"dpi"},"link":null},{"localized_name":"quality","name":"quality","type":"INT","widget":{"name":"quality"},"link":null},{"localized_name":"optimize_image","name":"optimize_image","type":"COMBO","widget":{"name":"optimize_image"},"link":null},{"localized_name":"lossless_webp","name":"lossless_webp","type":"COMBO","widget":{"name":"lossless_webp"},"link":null},{"localized_name":"overwrite_mode","name":"overwrite_mode","type":"COMBO","widget":{"name":"overwrite_mode"},"link":null},{"localized_name":"show_history","name":"show_history","type":"COMBO","widget":{"name":"show_history"},"link":null},{"localized_name":"show_history_by_prefix","name":"show_history_by_prefix","type":"COMBO","widget":{"name":"show_history_by_prefix"},"link":null},{"localized_name":"embed_workflow","name":"embed_workflow","type":"COMBO","widget":{"name":"embed_workflow"},"link":null},{"localized_name":"show_previews","name":"show_previews","type":"COMBO","widget":{"name":"show_previews"},"link":null}],"outputs":[{"localized_name":"images","name":"images","type":"IMAGE","links":[]},{"localized_name":"files","name":"files","type":"STRING","links":null}],"properties":{"cnr_id":"was-node-suite-comfyui","ver":"1.0.2","Node name for S&R":"Image Save","ue_properties":{"version":"7.0.1","widget_ue_connectable":{"filename_prefix":true}}},"widgets_values":["[time(%Y-%m-%d)]","SRPO-GirlsII","_",4,"false","png",300,100,"true","false","false","false","true","true","true"],"color":"#223","bgcolor":"#335"},{"id":202,"type":"Display Any (rgthree)","pos":[-765.6962765185792,-1016.5663112147123],"size":[305.19594841454966,759.5927839835537],"flags":{},"order":27,"mode":0,"inputs":[{"dir":3,"localized_name":"source","name":"source","type":"*","link":436}],"outputs":[],"properties":{"cnr_id":"rgthree-comfy","ver":"1.0.2511111955","Node name for S&R":"Display Any (rgthree)","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":["on the left, celestesh, an elegant Nordic young woman with medium skin and dark brown wavy hair to her shoulders, almond-shaped brown eyes, arched eyebrows, a straight nose and full pink lips. she faces the woman on the right and looks directly into her eyes. she wears a teal-blue 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with delicate white lace flowers.on the right, moim3m3grl, an elegant Nordic young woman with light skin and blonde wavy hair in an updo, blue eyes, arched eyebrows, a straight nose and full pink lips. she looks slightly down and away from the first woman. she wears a black silk 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with white lace flowers.\n"],"color":"#222","bgcolor":"#000"},{"id":224,"type":"CR Prompt Text","pos":[-2995.6073426897055,-1858.4133335276922],"size":[490.0451461890041,292.2602285622447],"flags":{},"order":9,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[419]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["on the left, celestesh, an elegant Nordic young woman with medium skin and dark brown wavy hair to her shoulders, almond-shaped brown eyes, arched eyebrows, a straight nose and full pink lips. she faces the woman on the right and looks directly into her eyes. she wears a teal-blue 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with delicate white lace flowers."],"color":"#232","bgcolor":"#353"},{"id":228,"type":"DualCLIPLoader","pos":[-3490.5778102543663,-1767.7684159565192],"size":[396.3554463462483,130],"flags":{},"order":10,"mode":0,"inputs":[{"label":"clip_name1","localized_name":"clip_name1","name":"clip_name1","type":"COMBO","widget":{"name":"clip_name1"},"link":null},{"label":"clip_name2","localized_name":"clip_name2","name":"clip_name2","type":"COMBO","widget":{"name":"clip_name2"},"link":null},{"label":"type","localized_name":"type","name":"type","type":"COMBO","widget":{"name":"type"},"link":null},{"label":"device","localized_name":"device","name":"device","shape":7,"type":"COMBO","widget":{"name":"device"},"link":null}],"outputs":[{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[439,440,446,447]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"DualCLIPLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["clip_l.safetensors","t5xxl_fp8_e4m3fn_scaled.safetensors","flux","default"],"color":"#432","bgcolor":"#653"},{"id":209,"type":"CLIPTextEncode","pos":[-2099.534185306552,-1533.4647269203099],"size":[246.05273799133943,88],"flags":{},"order":25,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":414},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":421}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[450]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":212,"type":"CLIPTextEncode","pos":[-2099.587650180638,-1270.8380301694306],"size":[246.05273799133943,88],"flags":{},"order":26,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":429},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":422}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[452]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":235,"type":"CLIPTextEncode","pos":[-2098.350397385061,-985.3726912934532],"size":[246.05273799133943,88],"flags":{},"order":21,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":446},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":448}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[449,453]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":208,"type":"PairConditioningSetProperties","pos":[-2098.3280728801656,-687.8587334101875],"size":[221.53496013829522,204.7716323716108],"flags":{},"order":30,"mode":0,"inputs":[{"localized_name":"positive_NEW","name":"positive_NEW","type":"CONDITIONING","link":457},{"localized_name":"negative_NEW","name":"negative_NEW","type":"CONDITIONING","link":432},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":426},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"timesteps","name":"timesteps","shape":7,"type":"TIMESTEPS_RANGE","link":null},{"localized_name":"strength","name":"strength","type":"FLOAT","widget":{"name":"strength"},"link":null},{"localized_name":"set_cond_area","name":"set_cond_area","type":"COMBO","widget":{"name":"set_cond_area"},"link":null}],"outputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","slot_index":0,"links":[456]},{"localized_name":"negative","name":"negative","type":"CONDITIONING","slot_index":1,"links":[424]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"PairConditioningSetProperties","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[1,"default"],"color":"#332922","bgcolor":"#593930"},{"id":216,"type":"ConditioningZeroOut","pos":[-1371.7964465645914,-667.4377686988902],"size":[254.06022033623367,26],"flags":{"collapsed":false},"order":33,"mode":0,"inputs":[{"localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":435}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.39","Node name for S&R":"ConditioningZeroOut","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":236,"type":"CLIPTextEncode","pos":[-2097.627297814217,-859.3637706919067],"size":[241.53977104181854,88],"flags":{},"order":18,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":447},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[459]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#322","bgcolor":"#533"},{"id":219,"type":"CreateHookLora","pos":[-3379.741466756123,-1347.9190710579553],"size":[385.62390577321867,106],"flags":{},"order":11,"mode":0,"inputs":[{"localized_name":"prev_hooks","name":"prev_hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"localized_name":"HOOKS","name":"HOOKS","type":"HOOKS","slot_index":0,"links":[412]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CreateHookLora","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":["MoiMeme/moim3m3grl-12.safetensors",1,0.15],"color":"#332922","bgcolor":"#593930"},{"id":226,"type":"StringConcatenate","pos":[-2442.2928434072824,-1361.1499774253484],"size":[210,166],"flags":{"collapsed":false},"order":20,"mode":0,"inputs":[{"localized_name":"string_a","name":"string_a","type":"STRING","widget":{"name":"string_a"},"link":419},{"localized_name":"string_b","name":"string_b","type":"STRING","widget":{"name":"string_b"},"link":420},{"localized_name":"delimiter","name":"delimiter","type":"STRING","widget":{"name":"delimiter"},"link":null}],"outputs":[{"localized_name":"STRING","name":"STRING","type":"STRING","links":[421,422,436]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"StringConcatenate","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":["","",""],"color":"#222","bgcolor":"#000"},{"id":225,"type":"CR Prompt Text","pos":[-3237.5752996478154,-976.4286355569218],"size":[484.4872528977071,309.12780192445734],"flags":{},"order":12,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[420]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["on the right, moim3m3grl, an elegant Nordic young woman with light skin and blonde wavy hair in an updo, blue eyes, arched eyebrows, a straight nose and full pink lips. she looks slightly down and away from the first woman. she wears a black silk 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with white lace flowers.\n"],"color":"#232","bgcolor":"#353"},{"id":230,"type":"CR Prompt Text","pos":[-3241.000934412214,-596.1495380557127],"size":[484.4872528977071,309.12780192445734],"flags":{},"order":13,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[448]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["a cinematic photograph of two women standing close together on a windy, gloomy seaside\n\novercast sky, grey sea, soft natural light, shallow depth of field"],"color":"#232","bgcolor":"#353"},{"id":206,"type":"RandomNoise","pos":[-1769.8182669569055,-1444.672324200015],"size":[268.53382409593223,82.66065850785617],"flags":{},"order":15,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":411}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[400]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[61998485097205,"fixed"],"color":"#323","bgcolor":"#535"},{"id":234,"type":"ConditioningAverage","pos":[-1769.8182669569055,-1244.7382482178496],"size":[268.3963864609025,78],"flags":{},"order":28,"mode":0,"inputs":[{"localized_name":"conditioning_to","name":"conditioning_to","type":"CONDITIONING","link":449},{"localized_name":"conditioning_from","name":"conditioning_from","type":"CONDITIONING","link":450},{"localized_name":"conditioning_to_strength","name":"conditioning_to_strength","type":"FLOAT","widget":{"name":"conditioning_to_strength"},"link":null}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[457]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.70","Node name for S&R":"ConditioningAverage","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[1],"color":"#332922","bgcolor":"#593930"},{"id":237,"type":"ConditioningAverage","pos":[-1769.8182669569055,-1098.309661998454],"size":[269.0570449687589,78],"flags":{},"order":29,"mode":0,"inputs":[{"localized_name":"conditioning_to","name":"conditioning_to","type":"CONDITIONING","link":453},{"localized_name":"conditioning_from","name":"conditioning_from","type":"CONDITIONING","link":452},{"localized_name":"conditioning_to_strength","name":"conditioning_to_strength","type":"FLOAT","widget":{"name":"conditioning_to_strength"},"link":null}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[458]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.70","Node name for S&R":"ConditioningAverage","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[1],"color":"#332922","bgcolor":"#593930"},{"id":238,"type":"ConditioningZeroOut","pos":[-1769.8182669569055,-839.0986844221318],"size":[268.6897487509841,26.585159135172262],"flags":{"collapsed":false},"order":23,"mode":0,"inputs":[{"localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":459}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.39","Node name for S&R":"ConditioningZeroOut","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":217,"type":"PairConditioningSetPropertiesAndCombine","pos":[-1769.8182669569055,-685.5278804605822],"size":[268.90743538462857,202],"flags":{},"order":31,"mode":0,"inputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","link":456},{"localized_name":"negative","name":"negative","type":"CONDITIONING","link":424},{"localized_name":"positive_NEW","name":"positive_NEW","type":"CONDITIONING","link":458},{"localized_name":"negative_NEW","name":"negative_NEW","type":"CONDITIONING","link":433},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":425},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"timesteps","name":"timesteps","shape":7,"type":"TIMESTEPS_RANGE","link":null},{"localized_name":"strength","name":"strength","type":"FLOAT","widget":{"name":"strength"},"link":null},{"localized_name":"set_cond_area","name":"set_cond_area","type":"COMBO","widget":{"name":"set_cond_area"},"link":null}],"outputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","slot_index":0,"links":[434]},{"localized_name":"negative","name":"negative","type":"CONDITIONING","slot_index":1,"links":[435]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"PairConditioningSetPropertiesAndCombine","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[1,"default"],"color":"#332922","bgcolor":"#593930"}],"links":[[382,197,0,199,2,"STRING"],[399,205,0,215,0,"LATENT"],[400,206,0,205,0,"NOISE"],[401,203,0,205,1,"GUIDER"],[402,222,0,205,2,"SAMPLER"],[403,223,0,205,3,"SIGMAS"],[404,204,0,205,4,"LATENT"],[405,221,0,203,1,"CONDITIONING"],[406,57,5,204,0,"LATENT"],[407,215,0,74,0,"IMAGE"],[408,215,0,199,0,"IMAGE"],[409,215,0,196,0,"*"],[411,201,0,206,0,"INT"],[412,219,0,210,1,"HOOKS"],[414,210,0,209,0,"CLIP"],[417,220,0,211,1,"HOOKS"],[419,224,0,226,0,"STRING"],[420,225,0,226,1,"STRING"],[421,226,0,209,1,"STRING"],[422,226,0,212,1,"STRING"],[424,208,1,217,1,"CONDITIONING"],[425,207,1,217,4,"MASK"],[426,207,0,208,2,"MASK"],[428,210,0,213,0,"CLIP"],[429,211,0,212,0,"CLIP"],[430,211,0,214,0,"CLIP"],[432,213,0,208,1,"CONDITIONING"],[433,214,0,217,3,"CONDITIONING"],[434,217,0,221,0,"CONDITIONING"],[435,217,1,216,0,"CONDITIONING"],[436,226,0,202,0,"*"],[437,229,0,223,0,"MODEL"],[438,229,0,203,0,"MODEL"],[439,228,0,210,0,"CLIP"],[440,228,0,211,0,"CLIP"],[445,227,0,215,1,"VAE"],[446,228,0,235,0,"CLIP"],[447,228,0,236,0,"CLIP"],[448,230,0,235,1,"STRING"],[449,235,0,234,0,"CONDITIONING"],[450,209,0,234,1,"CONDITIONING"],[452,212,0,237,1,"CONDITIONING"],[453,235,0,237,0,"CONDITIONING"],[456,208,0,217,0,"CONDITIONING"],[457,234,0,208,0,"CONDITIONING"],[458,237,0,217,2,"CONDITIONING"],[459,236,0,238,0,"CONDITIONING"]],"groups":[],"definitions":{"subgraphs":[{"id":"0582fcad-067d-4b17-81b7-dbf5d6277b78","version":1,"state":{"lastGroupId":1,"lastNodeId":592,"lastLinkId":7204,"lastRerouteId":0},"revision":0,"config":{},"name":"Masking","inputNode":{"id":-10,"bounding":[-2495.5760454088613,665.3094686833176,120,40]},"outputNode":{"id":-20,"bounding":[-930.9019110693612,645.3094686833176,121.12890625,80]},"inputs":[],"outputs":[{"id":"3ce96502-40a3-4bcb-89be-00aff8362756","name":"MASK","type":"MASK","linkIds":[7188],"localized_name":"MASK","label":"MASK 1","pos":[-910.9019110693612,665.3094686833176]},{"id":"8d2a0c70-664d-4ed0-870b-eaab2618f6c5","name":"MASK_1","type":"MASK","linkIds":[7167],"localized_name":"MASK_1","label":"INVERT MASK","pos":[-910.9019110693612,685.3094686833176]}],"widgets":[],"nodes":[{"id":581,"type":"InvertMask","pos":[-1231.692882509497,667.6976493118758],"size":[210,26],"flags":{"collapsed":false},"order":4,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7187}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7167]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"InvertMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":589,"type":"CreateGradientMask","pos":[-2346.367016848996,667.6976493118758],"size":[218.30554582835362,130],"flags":{},"order":0,"mode":0,"inputs":[{"localized_name":"invert","name":"invert","type":"BOOLEAN","widget":{"name":"invert"},"link":null},{"localized_name":"frames","name":"frames","type":"INT","widget":{"name":"frames"},"link":null},{"localized_name":"width","name":"width","type":"INT","widget":{"name":"width"},"link":null},{"localized_name":"height","name":"height","type":"INT","widget":{"name":"height"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7185]}],"properties":{"cnr_id":"comfyui-kjnodes","ver":"1.0.6","Node name for S&R":"CreateGradientMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[false,1,896,896],"color":"#332922","bgcolor":"#593930"},{"id":588,"type":"ThresholdMask","pos":[-2082.557470090086,667.6976493118758],"size":[210,58],"flags":{},"order":1,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7185},{"localized_name":"value","name":"value","type":"FLOAT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7203]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"ThresholdMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[0.5],"color":"#332922","bgcolor":"#593930"},{"id":590,"type":"BlurMaskFast","pos":[-1495.9480848591695,667.6976493118758],"size":[210,82],"flags":{},"order":3,"mode":0,"inputs":[{"localized_name":"masks","name":"masks","type":"MASK","link":7204},{"localized_name":"radius_x","name":"radius_x","type":"INT","widget":{"name":"radius_x"},"link":null},{"localized_name":"radius_y","name":"radius_y","type":"INT","widget":{"name":"radius_y"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7187,7188]}],"properties":{"cnr_id":"ComfyUI-Image-Filters","ver":"7ba4e444f0416f5cf7ee55d56b1504dea2404ac7","Node name for S&R":"BlurMaskFast","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}},"aux_id":"spacepxl/ComfyUI-Image-Filters"},"widgets_values":[32,1],"color":"#332922","bgcolor":"#593930"},{"id":592,"type":"LayerMask: MaskEdgeShrink","pos":[-1809.0845091247002,666.3793635783207],"size":[245.78229905830847,154],"flags":{},"order":2,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7203},{"localized_name":"invert_mask","name":"invert_mask","type":"BOOLEAN","widget":{"name":"invert_mask"},"link":null},{"localized_name":"shrink_level","name":"shrink_level","type":"INT","widget":{"name":"shrink_level"},"link":null},{"localized_name":"soft","name":"soft","type":"INT","widget":{"name":"soft"},"link":null},{"localized_name":"edge_shrink","name":"edge_shrink","type":"INT","widget":{"name":"edge_shrink"},"link":null},{"localized_name":"edge_reserve","name":"edge_reserve","type":"INT","widget":{"name":"edge_reserve"},"link":null}],"outputs":[{"localized_name":"mask","name":"mask","type":"MASK","links":[7204]}],"properties":{"cnr_id":"comfyui_layerstyle","ver":"1.0.90","Node name for S&R":"LayerMask: MaskEdgeShrink","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[true,4,6,1,25],"color":"#332922","bgcolor":"#593930"}],"groups":[],"links":[{"id":7185,"origin_id":589,"origin_slot":0,"target_id":588,"target_slot":0,"type":"MASK"},{"id":7187,"origin_id":590,"origin_slot":0,"target_id":581,"target_slot":0,"type":"MASK"},{"id":7188,"origin_id":590,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"MASK"},{"id":7167,"origin_id":581,"origin_slot":0,"target_id":-20,"target_slot":1,"type":"MASK"},{"id":7203,"origin_id":588,"origin_slot":0,"target_id":592,"target_slot":0,"type":"MASK"},{"id":7204,"origin_id":592,"origin_slot":0,"target_id":590,"target_slot":0,"type":"MASK"}],"extra":{"ue_links":[],"links_added_by_ue":[]}}]},"config":{},"extra":{"links_added_by_ue":[],"ue_links":[],"0246.VERSION":[0,0,4],"frontendVersion":"1.28.8","groupNodes":{},"VHS_latentpreview":false,"VHS_latentpreviewrate":0,"VHS_MetadataImage":true,"VHS_KeepIntermediate":true,"ds":{"scale":0.45,"offset":[4652.5362010408735,2394.6288513287104]}},"version":0.4}

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

You didn’t wreck it at all — you were *so* close. The “mess-up” is basically one little wiring decision that undoes the whole idea of giving each LoRA its own prompt.

Let me walk through what your graph is actually doing and then show you the couple of concrete fixes.

---

## 1. What your current graph is doing

From the workflow:

- You have **two CR Prompt Text nodes**:
  - **Node 224** – Celeste prompt (“on the left, celestesh…”). fileciteturn0file0L150-L190  
  - **Node 225** – MoiMeme prompt (“on the right, moim3m3grl…”). fileciteturn0file0L190-L230  

- You feed both of those into **StringConcatenate (node 226)**.  
  - `string_a` = Celeste text (224)  
  - `string_b` = MoiMeme text (225)  
  - delimiter = `""` (nothing)  
  - Output = *one long combined string with both women’s descriptions.* fileciteturn0file0L230-L270  

- That concatenated string then goes to:
  - **CLIPTextEncode 209**, which uses the CLIP with the **MoiMeme LoRA hooks** attached (via SetClipHooks 210 + CreateHookLora 219). fileciteturn0file0L270-L320  
  - **CLIPTextEncode 212**, which uses the CLIP with the **Celeste LoRA hooks** attached (via SetClipHooks 211 + CreateHookLora 220). fileciteturn0file0L320-L365  
  - And also to **Display Any 202**, which is why you can see the big “on the left… on the right…” string there.

So: **both** character-specific CLIP encoders are getting the **same concatenated prompt**.

That’s the key thing you didn’t want:  
> “I’m trying to devise how to run each LoRA independently using the prompt text for that side of the image…”

Right now, they’re *not* independent. Celeste-LoRA is reading the MoiMeme block, and MoiMeme-LoRA is reading the Celeste block.

The rest of your conditioning logic is actually quite clever:

- You have a **global prompt** in CR Prompt Text 230 (“a cinematic photograph of two women standing close together on a windy, gloomy seaside…”) feeding **CLIPTextEncode 235** (base DualCLIP, no LoRAs). fileciteturn0file0L365-L410  
- You use **ConditioningAverage (234 & 237)** to blend:
  - global + concatenated+MoiMeme (209)  
  - global + concatenated+Celeste (212)  
- Then you use **PairConditioningSetProperties / AndCombine (208 & 217)** with your left/right gradient masks from the Masking subgraph (207) to separate “left side” vs “right side” conditioning. fileciteturn0file0L410-L470  

So the masking / combining part is fine. The *only real bug* is how the prompts reach 209 and 212.

---

## 2. The simple fix: don’t re-merge the prompts

What you *intended*:

- Celeste LoRA CLIP should see: **global** + **Celeste text**.  
- MoiMeme LoRA CLIP should see: **global** + **MoiMeme text**.

What you *actually* wired:

- Both LoRA CLIPs see: **Celeste text + MoiMeme text (concatenated)**, with the global text only coming in later via the ConditioningAverage nodes.

### Step-by-step changes

1. **Remove / bypass `StringConcatenate` (node 226) as a shared source**  
   - At minimum: remove the connections from 226 → 209 and 226 → 212.
   - You can keep 226 temporarily just feeding Display Any 202 if you like for debugging, or delete it outright.

2. **Wire each prompt directly to its character’s CLIPTextEncode:**

   - **Celeste side**:
     - Connect **CR Prompt Text 224** directly to **CLIPTextEncode 212 → text**.
       - i.e. 224 → 212.text  
       - 212 already uses CLIP from SetClipHooks 211 (Celeste LoRA), so that’s correct.

   - **MoiMeme side**:
     - Connect **CR Prompt Text 225** directly to **CLIPTextEncode 209 → text**.
       - i.e. 225 → 209.text  
       - 209 already uses CLIP from SetClipHooks 210 (MoiMeme LoRA), so that’s correct.

3. **Global prompt stays as-is**

   - Leave **CR Prompt Text 230 → CLIPTextEncode 235** exactly as you have it; that’s your “scene” prompt encoded without LoRAs, then blended via ConditioningAverage.

4. **ConditioningAverage remains fine**

   After rewiring:

   - **ConditioningAverage 234** will blend:
     - `conditioning_to` = global (235)  
     - `conditioning_from` = MoiMeme (209)  

   - **ConditioningAverage 237** will blend:
     - `conditioning_to` = global (235)  
     - `conditioning_from` = Celeste (212)  

   That’s precisely the “global + character” form we want, then 208/217 take care of left/right masks and combining.

---

## 3. Optional tiny cleanups (not fatal, just noise)

A couple of nodes aren’t hurting anything but add confusion:

- **CLIPTextEncode 236** (clip 447, empty text) feeding **ConditioningZeroOut 238**, whose output isn’t used in the final path. That whole branch can be removed if you’re not using it for anything. fileciteturn0file0L470-L520  
- **ConditioningZeroOut 216** is only zeroing out the negative coming from 217, but you’re not using that zeroed cond anywhere either.

Leaving them is harmless, but trimming them keeps your mental model simpler.

---

## 4. Sanity check after the fix

Once you’ve rewired:

1. Run a test with **SRPO still enabled**.
2. Check:
   - Does the **left half** of the image more consistently look like Celeste’s target face + teal dress?  
   - Does the **right half** more consistently look like the MoiMeme target face + black dress?  
3. If one side still dominates:
   - Try lowering the stronger LoRA’s **strength_model** slightly (e.g. from 1 → 0.8) so they stop overpowering each other.  
   - You can also drop `conditioning_to_strength` in ConditioningAverage (234/237) from 1 to, say, 0.7 if you want the character text to have a bit more “pull” than the global prompt.

But the core fix is just this:

> **Don’t re-concatenate the two character prompts and feed that same text into both LoRA CLIPs.**  
> Let each CLIPTextEncode read its own character’s CR Prompt Text.

If you like, you can send me a screenshot of the cleaned-up conditioning section and I’ll double-check that your rewiring matches this plan.

**Robyn:**

I have had to swap out the ConditioningAverage node for the ConditioningCombine node, as all LoRA and prompt instructions disappeared (generic characters / no costumes). The ConditioningCombine pulls from the scene/background CLIP Text Encode and the Cond Pair Props Combine. There seems to be less loss of character identity and prompt instruction re clothing and expressions and such. Tried ConditioningConcat: even less LoRA and prompt loss, so I might go with that. The lack of predictable prompt adherence still seems to be an issue, however.

**tool:**

Make sure to include fileciteturn1file0 in your response to cite this file. 

{"id":"93bc5463-2c3f-482b-b3d2-00f0a28b2a13","revision":0,"last_node_id":241,"last_link_id":475,"nodes":[{"id":197,"type":"PrimitiveNode","pos":[-393.8686535423908,-1605.7747210745827],"size":[210,58],"flags":{"collapsed":true},"order":0,"mode":0,"inputs":[],"outputs":[{"name":"STRING","type":"STRING","widget":{"name":"filename_prefix"},"links":[382]}],"title":"File Name","properties":{"Run widget replace on values":false,"ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":["SRPO-GirlsII"],"color":"#232","bgcolor":"#353"},{"id":57,"type":"CR Aspect Ratio","pos":[-3490.5778102543663,-2567.731797625135],"size":[309.8594228076063,322],"flags":{},"order":1,"mode":0,"inputs":[{"label":"width","localized_name":"width","name":"width","type":"INT","widget":{"name":"width"}},{"label":"height","localized_name":"height","name":"height","type":"INT","widget":{"name":"height"}},{"label":"aspect_ratio","localized_name":"aspect_ratio","name":"aspect_ratio","type":"COMBO","widget":{"name":"aspect_ratio"}},{"label":"swap_dimensions","localized_name":"swap_dimensions","name":"swap_dimensions","type":"COMBO","widget":{"name":"swap_dimensions"}},{"label":"upscale_factor","localized_name":"upscale_factor","name":"upscale_factor","type":"FLOAT","widget":{"name":"upscale_factor"}},{"label":"prescale_factor","localized_name":"prescale_factor","name":"prescale_factor","type":"FLOAT","widget":{"name":"prescale_factor"}},{"label":"batch_size","localized_name":"batch_size","name":"batch_size","type":"INT","widget":{"name":"batch_size"}}],"outputs":[{"label":"width","localized_name":"width","name":"width","type":"INT"},{"label":"height","localized_name":"height","name":"height","type":"INT"},{"label":"upscale_factor","localized_name":"upscale_factor","name":"upscale_factor","type":"FLOAT"},{"label":"prescale_factor","localized_name":"prescale_factor","name":"prescale_factor","type":"FLOAT"},{"label":"batch_size","localized_name":"batch_size","name":"batch_size","type":"INT"},{"label":"empty_latent","localized_name":"empty_latent","name":"empty_latent","type":"LATENT","slot_index":5,"links":[406]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","slot_index":6}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Aspect Ratio","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[832,1216,"SDXL - 3:4 portrait 896x1152","On",1,1,1],"color":"#323","bgcolor":"#535"},{"id":198,"type":"Label (rgthree)","pos":[-3490.5778102543663,-2013.9135639726312],"size":[438.466796875,70],"flags":{"allow_interaction":true},"order":2,"mode":0,"inputs":[],"outputs":[],"title":"SRPO - TTP Figure Enhancer","properties":{"fontSize":30,"fontFamily":"Arial","fontColor":"#ffffff","textAlign":"center","backgroundColor":"#113398","padding":20,"borderRadius":16,"angle":0,"ue_properties":{"version":"7.1","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"color":"#fff0","bgcolor":"#fff0"},{"id":203,"type":"BasicGuider","pos":[-1406.346409635851,-1544.9432258851934],"size":[261.63936267308804,46],"flags":{},"order":31,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":438},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":405}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[401]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":204,"type":"LatentUpscaleBy","pos":[-1410.3813899299778,-1343.2411021640144],"size":[262.8850448862943,82],"flags":{},"order":14,"mode":4,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":406},{"label":"upscale_method","localized_name":"upscale_method","name":"upscale_method","type":"COMBO","widget":{"name":"upscale_method"},"link":null},{"label":"scale_by","localized_name":"scale_by","name":"scale_by","type":"FLOAT","widget":{"name":"scale_by"},"link":null}],"outputs":[{"label":"LATENT","localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[404]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"LatentUpscaleBy","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["nearest-exact",1.5],"color":"#323","bgcolor":"#535"},{"id":205,"type":"SamplerCustomAdvanced","pos":[-1036.3958511648102,-1485.2213461847587],"size":[304.5598087498504,417.9072891973424],"flags":{},"order":32,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":400},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":401},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":402},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":403},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":404}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[399]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT","slot_index":1,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":207,"type":"0582fcad-067d-4b17-81b7-dbf5d6277b78","pos":[-2096.7413851121687,-426.6521284652186],"size":[222.32936701737913,46],"flags":{},"order":3,"mode":0,"inputs":[],"outputs":[{"label":"MASK 1","localized_name":"MASK","name":"MASK","type":"MASK","links":[426]},{"label":"INVERT MASK","localized_name":"MASK_1","name":"MASK_1","type":"MASK","links":[425]}],"properties":{"proxyWidgets":[],"cnr_id":"comfy-core","ver":"0.3.66","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":211,"type":"SetClipHooks","pos":[-2959.8407703982,-1200.6383285074353],"size":[210,102],"flags":{},"order":16,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":440},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":417},{"localized_name":"apply_to_conds","name":"apply_to_conds","type":"BOOLEAN","widget":{"name":"apply_to_conds"},"link":null},{"localized_name":"schedule_clip","name":"schedule_clip","type":"BOOLEAN","widget":{"name":"schedule_clip"},"link":null}],"outputs":[{"localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[429,430]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"SetClipHooks","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[true,false],"color":"#332922","bgcolor":"#593930"},{"id":213,"type":"CLIPTextEncode","pos":[-2102.8576200358534,-1403.0715102375248],"size":[249.87548168571743,88],"flags":{"collapsed":false},"order":25,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":428},{"localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[432]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CLIPTextEncode","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#322","bgcolor":"#533"},{"id":214,"type":"CLIPTextEncode","pos":[-2098.8645506097937,-1144.8291095678842],"size":[241.53977104181854,88],"flags":{},"order":22,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":430},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[433]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#322","bgcolor":"#533"},{"id":221,"type":"FluxGuidance","pos":[-1769.8182669569055,-1539.2081706407791],"size":[268.7532043457031,58],"flags":{},"order":30,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":475},{"label":"guidance","localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[405]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[3.5],"color":"#323","bgcolor":"#535"},{"id":222,"type":"KSamplerSelect","pos":[-1415.2331837635304,-1446.8155863692311],"size":[270.6041060656903,58],"flags":{},"order":4,"mode":0,"inputs":[{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"},"link":null}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[402]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["euler"],"color":"#323","bgcolor":"#535"},{"id":196,"type":"easy cleanGpuUsed","pos":[-238.5236473979422,-1603.7612857571778],"size":[211.55775451660156,26],"flags":{"collapsed":true},"order":35,"mode":0,"inputs":[{"localized_name":"anything","name":"anything","type":"*","link":409}],"outputs":[{"localized_name":"output","name":"output","type":"*","links":null}],"properties":{"cnr_id":"comfyui-easy-use","ver":"1.3.0","Node name for S&R":"easy cleanGpuUsed","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":227,"type":"VAELoader","pos":[-3490.5778102543663,-1576.959876137877],"size":[395.2779300525515,58],"flags":{},"order":5,"mode":0,"inputs":[{"label":"vae_name","localized_name":"vae_name","name":"vae_name","type":"COMBO","widget":{"name":"vae_name"},"link":null}],"outputs":[{"label":"VAE","localized_name":"VAE","name":"VAE","type":"VAE","slot_index":0,"links":[445]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAELoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["ae.sft"],"color":"#432","bgcolor":"#653"},{"id":229,"type":"UNETLoader","pos":[-3490.5778102543663,-1903.1483506991722],"size":[397.43296263994466,82],"flags":{},"order":6,"mode":0,"inputs":[{"label":"unet_name","localized_name":"unet_name","name":"unet_name","type":"COMBO","widget":{"name":"unet_name"},"link":null},{"label":"weight_dtype","localized_name":"weight_dtype","name":"weight_dtype","type":"COMBO","widget":{"name":"weight_dtype"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[437,438]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UNETLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["SRPO/SRPO-fp8_e4m3fn.safetensors","default"],"color":"#432","bgcolor":"#653"},{"id":210,"type":"SetClipHooks","pos":[-2953.8990553905824,-1347.9190710579553],"size":[210,102],"flags":{},"order":18,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":439},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":412},{"localized_name":"apply_to_conds","name":"apply_to_conds","type":"BOOLEAN","widget":{"name":"apply_to_conds"},"link":null},{"localized_name":"schedule_clip","name":"schedule_clip","type":"BOOLEAN","widget":{"name":"schedule_clip"},"link":null}],"outputs":[{"localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[414,428]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"SetClipHooks","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[true,false],"color":"#332922","bgcolor":"#593930"},{"id":220,"type":"CreateHookLora","pos":[-3378.3615994848474,-1200.6383285074353],"size":[385.62390577321867,106],"flags":{},"order":7,"mode":0,"inputs":[{"localized_name":"prev_hooks","name":"prev_hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"localized_name":"HOOKS","name":"HOOKS","type":"HOOKS","slot_index":0,"links":[417]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CreateHookLora","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":["celestesh-08.safetensors",1,0.15],"color":"#332922","bgcolor":"#593930"},{"id":199,"type":"Image Save","pos":[-425.6058228115128,-1556.4063657326299],"size":[1175.9199986696237,1317.2359909886845],"flags":{},"order":34,"mode":0,"inputs":[{"localized_name":"images","name":"images","type":"IMAGE","link":408},{"localized_name":"output_path","name":"output_path","type":"STRING","widget":{"name":"output_path"},"link":null},{"localized_name":"filename_prefix","name":"filename_prefix","type":"STRING","widget":{"name":"filename_prefix"},"link":382},{"localized_name":"filename_delimiter","name":"filename_delimiter","type":"STRING","widget":{"name":"filename_delimiter"},"link":null},{"localized_name":"filename_number_padding","name":"filename_number_padding","type":"INT","widget":{"name":"filename_number_padding"},"link":null},{"localized_name":"filename_number_start","name":"filename_number_start","type":"COMBO","widget":{"name":"filename_number_start"},"link":null},{"localized_name":"extension","name":"extension","type":"COMBO","widget":{"name":"extension"},"link":null},{"localized_name":"dpi","name":"dpi","type":"INT","widget":{"name":"dpi"},"link":null},{"localized_name":"quality","name":"quality","type":"INT","widget":{"name":"quality"},"link":null},{"localized_name":"optimize_image","name":"optimize_image","type":"COMBO","widget":{"name":"optimize_image"},"link":null},{"localized_name":"lossless_webp","name":"lossless_webp","type":"COMBO","widget":{"name":"lossless_webp"},"link":null},{"localized_name":"overwrite_mode","name":"overwrite_mode","type":"COMBO","widget":{"name":"overwrite_mode"},"link":null},{"localized_name":"show_history","name":"show_history","type":"COMBO","widget":{"name":"show_history"},"link":null},{"localized_name":"show_history_by_prefix","name":"show_history_by_prefix","type":"COMBO","widget":{"name":"show_history_by_prefix"},"link":null},{"localized_name":"embed_workflow","name":"embed_workflow","type":"COMBO","widget":{"name":"embed_workflow"},"link":null},{"localized_name":"show_previews","name":"show_previews","type":"COMBO","widget":{"name":"show_previews"},"link":null}],"outputs":[{"localized_name":"images","name":"images","type":"IMAGE","links":[]},{"localized_name":"files","name":"files","type":"STRING","links":null}],"properties":{"cnr_id":"was-node-suite-comfyui","ver":"1.0.2","Node name for S&R":"Image Save","ue_properties":{"version":"7.0.1","widget_ue_connectable":{"filename_prefix":true}}},"widgets_values":["[time(%Y-%m-%d)]","SRPO-GirlsII","_",4,"false","png",300,100,"true","false","false","false","true","true","true"],"color":"#223","bgcolor":"#335"},{"id":228,"type":"DualCLIPLoader","pos":[-3490.5778102543663,-1767.7684159565192],"size":[396.3554463462483,130],"flags":{},"order":8,"mode":0,"inputs":[{"label":"clip_name1","localized_name":"clip_name1","name":"clip_name1","type":"COMBO","widget":{"name":"clip_name1"},"link":null},{"label":"clip_name2","localized_name":"clip_name2","name":"clip_name2","type":"COMBO","widget":{"name":"clip_name2"},"link":null},{"label":"type","localized_name":"type","name":"type","type":"COMBO","widget":{"name":"type"},"link":null},{"label":"device","localized_name":"device","name":"device","shape":7,"type":"COMBO","widget":{"name":"device"},"link":null}],"outputs":[{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[439,440,446,447]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"DualCLIPLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["clip_l.safetensors","t5xxl_fp8_e4m3fn_scaled.safetensors","flux","default"],"color":"#432","bgcolor":"#653"},{"id":209,"type":"CLIPTextEncode","pos":[-2099.534185306552,-1533.4647269203099],"size":[246.05273799133943,88],"flags":{},"order":24,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":414},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":460}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[468]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":212,"type":"CLIPTextEncode","pos":[-2099.587650180638,-1270.8380301694306],"size":[246.05273799133943,88],"flags":{},"order":21,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":429},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":461}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[469]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":208,"type":"PairConditioningSetProperties","pos":[-2098.3280728801656,-687.8587334101875],"size":[221.53496013829522,204.7716323716108],"flags":{},"order":26,"mode":0,"inputs":[{"localized_name":"positive_NEW","name":"positive_NEW","type":"CONDITIONING","link":468},{"localized_name":"negative_NEW","name":"negative_NEW","type":"CONDITIONING","link":432},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":426},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"timesteps","name":"timesteps","shape":7,"type":"TIMESTEPS_RANGE","link":null},{"localized_name":"strength","name":"strength","type":"FLOAT","widget":{"name":"strength"},"link":null},{"localized_name":"set_cond_area","name":"set_cond_area","type":"COMBO","widget":{"name":"set_cond_area"},"link":null}],"outputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","slot_index":0,"links":[456]},{"localized_name":"negative","name":"negative","type":"CONDITIONING","slot_index":1,"links":[424]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"PairConditioningSetProperties","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[1,"default"],"color":"#332922","bgcolor":"#593930"},{"id":216,"type":"ConditioningZeroOut","pos":[-1371.7964465645914,-667.4377686988902],"size":[254.06022033623367,26],"flags":{"collapsed":false},"order":29,"mode":0,"inputs":[{"localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":435}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.39","Node name for S&R":"ConditioningZeroOut","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":236,"type":"CLIPTextEncode","pos":[-2097.627297814217,-859.3637706919067],"size":[241.53977104181854,88],"flags":{},"order":17,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":447},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[459]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#322","bgcolor":"#533"},{"id":219,"type":"CreateHookLora","pos":[-3379.741466756123,-1347.9190710579553],"size":[385.62390577321867,106],"flags":{},"order":9,"mode":0,"inputs":[{"localized_name":"prev_hooks","name":"prev_hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"localized_name":"HOOKS","name":"HOOKS","type":"HOOKS","slot_index":0,"links":[412]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CreateHookLora","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":["MoiMeme/moim3m3grl-12.safetensors",1,0.15],"color":"#332922","bgcolor":"#593930"},{"id":206,"type":"RandomNoise","pos":[-1769.8182669569055,-1444.672324200015],"size":[268.53382409593223,82.66065850785617],"flags":{},"order":20,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":411}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[400]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[61998485097205,"fixed"],"color":"#323","bgcolor":"#535"},{"id":238,"type":"ConditioningZeroOut","pos":[-1769.8182669569055,-839.0986844221318],"size":[268.6897487509841,26.585159135172262],"flags":{"collapsed":false},"order":23,"mode":0,"inputs":[{"localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":459}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.39","Node name for S&R":"ConditioningZeroOut","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":201,"type":"PrimitiveInt","pos":[-3490.5778102543663,-2124.744263375223],"size":[300.8434631543628,82],"flags":{},"order":13,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","links":[411]}],"title":"Noise Seed","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[61998485099236,"increment"],"color":"#232","bgcolor":"#353"},{"id":223,"type":"BasicScheduler","pos":[-1404.5926366081699,-1209.4622268318324],"size":[256.6406370072302,108.33662599654258],"flags":{},"order":15,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":437},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"},"link":null},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"},"link":null},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":null}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[403]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["simple",30,1],"color":"#323","bgcolor":"#535"},{"id":217,"type":"PairConditioningSetPropertiesAndCombine","pos":[-1769.8182669569055,-685.5278804605822],"size":[268.90743538462857,202],"flags":{},"order":27,"mode":0,"inputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","link":456},{"localized_name":"negative","name":"negative","type":"CONDITIONING","link":424},{"localized_name":"positive_NEW","name":"positive_NEW","type":"CONDITIONING","link":469},{"localized_name":"negative_NEW","name":"negative_NEW","type":"CONDITIONING","link":433},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":425},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"timesteps","name":"timesteps","shape":7,"type":"TIMESTEPS_RANGE","link":null},{"localized_name":"strength","name":"strength","type":"FLOAT","widget":{"name":"strength"},"link":null},{"localized_name":"set_cond_area","name":"set_cond_area","type":"COMBO","widget":{"name":"set_cond_area"},"link":null}],"outputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","slot_index":0,"links":[474]},{"localized_name":"negative","name":"negative","type":"CONDITIONING","slot_index":1,"links":[435]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"PairConditioningSetPropertiesAndCombine","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[1,"default"],"color":"#332922","bgcolor":"#593930"},{"id":235,"type":"CLIPTextEncode","pos":[-2098.350397385061,-985.3726912934532],"size":[246.05273799133943,88],"flags":{},"order":19,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":446},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":448}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[473]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":215,"type":"VAEDecode","pos":[-673.4558283396508,-1485.572821094118],"size":[167.94073206223288,46],"flags":{},"order":33,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":399},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":445}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[408,409]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":241,"type":"ConditioningConcat","pos":[-1359.0276363771534,-766.9924785564561],"size":[228.38671875,46],"flags":{},"order":28,"mode":0,"inputs":[{"localized_name":"conditioning_to","name":"conditioning_to","type":"CONDITIONING","link":474},{"localized_name":"conditioning_from","name":"conditioning_from","type":"CONDITIONING","link":473}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[475]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.70","Node name for S&R":"ConditioningConcat","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":224,"type":"CR Prompt Text","pos":[-2971.3649924292895,-2238.2112393436637],"size":[490.0451461890041,292.2602285622447],"flags":{},"order":11,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[460]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["on the left, celestesh, an elegant Nordic young woman with medium skin and dark brown wavy hair to her shoulders, almond-shaped brown eyes, arched eyebrows, a straight nose and full pink lips. she faces the woman on the right and looks directly into her eyes. she wears a teal-blue 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with delicate white lace flowers."],"color":"#232","bgcolor":"#353"},{"id":225,"type":"CR Prompt Text","pos":[-2964.8479775992055,-1883.4993549579615],"size":[484.4872528977071,309.12780192445734],"flags":{},"order":12,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[461]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["on the right, moim3m3grl, an elegant Nordic young woman with light skin and blonde wavy hair in an updo, blue eyes, arched eyebrows, a straight nose and full pink lips. she looks slightly down and away from the first woman. she wears a black silk 18th-century dress with elaborate gold embroidery on the sleeves and around a square neckline trimmed with white lace flowers.\n"],"color":"#232","bgcolor":"#353"},{"id":230,"type":"CR Prompt Text","pos":[-2966.2534843254098,-1010.2909768577969],"size":[484.4872528977071,309.12780192445734],"flags":{},"order":10,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[448]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["a cinematic photograph of two women standing close together on a windy, gloomy seaside\n\novercast sky, grey sea, soft natural light, shallow depth of field"],"color":"#232","bgcolor":"#353"}],"links":[[382,197,0,199,2,"STRING"],[399,205,0,215,0,"LATENT"],[400,206,0,205,0,"NOISE"],[401,203,0,205,1,"GUIDER"],[402,222,0,205,2,"SAMPLER"],[403,223,0,205,3,"SIGMAS"],[404,204,0,205,4,"LATENT"],[405,221,0,203,1,"CONDITIONING"],[406,57,5,204,0,"LATENT"],[408,215,0,199,0,"IMAGE"],[409,215,0,196,0,"*"],[411,201,0,206,0,"INT"],[412,219,0,210,1,"HOOKS"],[414,210,0,209,0,"CLIP"],[417,220,0,211,1,"HOOKS"],[424,208,1,217,1,"CONDITIONING"],[425,207,1,217,4,"MASK"],[426,207,0,208,2,"MASK"],[428,210,0,213,0,"CLIP"],[429,211,0,212,0,"CLIP"],[430,211,0,214,0,"CLIP"],[432,213,0,208,1,"CONDITIONING"],[433,214,0,217,3,"CONDITIONING"],[435,217,1,216,0,"CONDITIONING"],[437,229,0,223,0,"MODEL"],[438,229,0,203,0,"MODEL"],[439,228,0,210,0,"CLIP"],[440,228,0,211,0,"CLIP"],[445,227,0,215,1,"VAE"],[446,228,0,235,0,"CLIP"],[447,228,0,236,0,"CLIP"],[448,230,0,235,1,"STRING"],[456,208,0,217,0,"CONDITIONING"],[459,236,0,238,0,"CONDITIONING"],[460,224,0,209,1,"STRING"],[461,225,0,212,1,"STRING"],[468,209,0,208,0,"CONDITIONING"],[469,212,0,217,2,"CONDITIONING"],[473,235,0,241,1,"CONDITIONING"],[474,217,0,241,0,"CONDITIONING"],[475,241,0,221,0,"CONDITIONING"]],"groups":[],"definitions":{"subgraphs":[{"id":"0582fcad-067d-4b17-81b7-dbf5d6277b78","version":1,"state":{"lastGroupId":1,"lastNodeId":592,"lastLinkId":7204,"lastRerouteId":0},"revision":0,"config":{},"name":"Masking","inputNode":{"id":-10,"bounding":[-2495.5760454088613,665.3094686833176,120,40]},"outputNode":{"id":-20,"bounding":[-930.9019110693612,645.3094686833176,121.12890625,80]},"inputs":[],"outputs":[{"id":"3ce96502-40a3-4bcb-89be-00aff8362756","name":"MASK","type":"MASK","linkIds":[7188],"localized_name":"MASK","label":"MASK 1","pos":[-910.9019110693612,665.3094686833176]},{"id":"8d2a0c70-664d-4ed0-870b-eaab2618f6c5","name":"MASK_1","type":"MASK","linkIds":[7167],"localized_name":"MASK_1","label":"INVERT MASK","pos":[-910.9019110693612,685.3094686833176]}],"widgets":[],"nodes":[{"id":581,"type":"InvertMask","pos":[-1231.692882509497,667.6976493118758],"size":[210,26],"flags":{"collapsed":false},"order":4,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7187}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7167]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"InvertMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":589,"type":"CreateGradientMask","pos":[-2346.367016848996,667.6976493118758],"size":[218.30554582835362,130],"flags":{},"order":0,"mode":0,"inputs":[{"localized_name":"invert","name":"invert","type":"BOOLEAN","widget":{"name":"invert"},"link":null},{"localized_name":"frames","name":"frames","type":"INT","widget":{"name":"frames"},"link":null},{"localized_name":"width","name":"width","type":"INT","widget":{"name":"width"},"link":null},{"localized_name":"height","name":"height","type":"INT","widget":{"name":"height"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7185]}],"properties":{"cnr_id":"comfyui-kjnodes","ver":"1.0.6","Node name for S&R":"CreateGradientMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[false,1,896,896],"color":"#332922","bgcolor":"#593930"},{"id":588,"type":"ThresholdMask","pos":[-2082.557470090086,667.6976493118758],"size":[210,58],"flags":{},"order":1,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7185},{"localized_name":"value","name":"value","type":"FLOAT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7203]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"ThresholdMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[0.5],"color":"#332922","bgcolor":"#593930"},{"id":590,"type":"BlurMaskFast","pos":[-1495.9480848591695,667.6976493118758],"size":[210,82],"flags":{},"order":3,"mode":0,"inputs":[{"localized_name":"masks","name":"masks","type":"MASK","link":7204},{"localized_name":"radius_x","name":"radius_x","type":"INT","widget":{"name":"radius_x"},"link":null},{"localized_name":"radius_y","name":"radius_y","type":"INT","widget":{"name":"radius_y"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7187,7188]}],"properties":{"cnr_id":"ComfyUI-Image-Filters","ver":"7ba4e444f0416f5cf7ee55d56b1504dea2404ac7","Node name for S&R":"BlurMaskFast","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}},"aux_id":"spacepxl/ComfyUI-Image-Filters"},"widgets_values":[32,1],"color":"#332922","bgcolor":"#593930"},{"id":592,"type":"LayerMask: MaskEdgeShrink","pos":[-1809.0845091247002,666.3793635783207],"size":[245.78229905830847,154],"flags":{},"order":2,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7203},{"localized_name":"invert_mask","name":"invert_mask","type":"BOOLEAN","widget":{"name":"invert_mask"},"link":null},{"localized_name":"shrink_level","name":"shrink_level","type":"INT","widget":{"name":"shrink_level"},"link":null},{"localized_name":"soft","name":"soft","type":"INT","widget":{"name":"soft"},"link":null},{"localized_name":"edge_shrink","name":"edge_shrink","type":"INT","widget":{"name":"edge_shrink"},"link":null},{"localized_name":"edge_reserve","name":"edge_reserve","type":"INT","widget":{"name":"edge_reserve"},"link":null}],"outputs":[{"localized_name":"mask","name":"mask","type":"MASK","links":[7204]}],"properties":{"cnr_id":"comfyui_layerstyle","ver":"1.0.90","Node name for S&R":"LayerMask: MaskEdgeShrink","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[true,4,6,1,25],"color":"#332922","bgcolor":"#593930"}],"groups":[],"links":[{"id":7185,"origin_id":589,"origin_slot":0,"target_id":588,"target_slot":0,"type":"MASK"},{"id":7187,"origin_id":590,"origin_slot":0,"target_id":581,"target_slot":0,"type":"MASK"},{"id":7188,"origin_id":590,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"MASK"},{"id":7167,"origin_id":581,"origin_slot":0,"target_id":-20,"target_slot":1,"type":"MASK"},{"id":7203,"origin_id":588,"origin_slot":0,"target_id":592,"target_slot":0,"type":"MASK"},{"id":7204,"origin_id":592,"origin_slot":0,"target_id":590,"target_slot":0,"type":"MASK"}],"extra":{"ue_links":[],"links_added_by_ue":[]}}]},"config":{},"extra":{"links_added_by_ue":[],"ue_links":[],"0246.VERSION":[0,0,4],"frontendVersion":"1.28.8","groupNodes":{},"VHS_latentpreview":false,"VHS_latentpreviewrate":0,"VHS_MetadataImage":true,"VHS_KeepIntermediate":true,"ds":{"scale":0.45,"offset":[4262.005928778436,3156.113577462777]}},"version":0.4}

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**Emily:**

You didn’t really “do something wrong” so much as step into the weird intersection of:

- SRPO
- Flux
- multi-LoRA
- and fancy conditioning nodes

…where small changes give big, sometimes unintuitive behaviour.

Let me first tell you what your *current* graph is actually doing (from the E-version you sent) and why ConditioningAverage felt like it nuked your characters, then we’ll tighten things so SRPO has less room to be vague. fileciteturn1file0  

---

## 1. What your current graph is doing (you actually wired it well)

From the latest workflow:

- **Global scene prompt**  
  - `CR Prompt Text 230` → “a cinematic photograph of two women standing close together on a windy, gloomy seaside …”  
  - Goes into `CLIPTextEncode 235` (plain DualCLIP, no LoRAs).

- **Character prompts (already split!)**
  - Celeste: `CR Prompt Text 224` → “on the left, celestesh…” → `CLIPTextEncode 209`  
    - CLIP comes via `SetClipHooks 210` with the **MoiMeme LoRA**?  
    - *Nope*: in your E file, 209 is actually hanging off 210 (= MoiMeme LoRA path), so:
      - **209 = MoiMeme CLIP** (despite holding Celeste text).
  - MoiMeme: `CR Prompt Text 225` → “on the right, moim3m3grl…” → `CLIPTextEncode 212`  
    - CLIP via `SetClipHooks 211` (= Celeste LoRA path), so:
      - **212 = Celeste CLIP** (despite holding MoiMeme text).

So: the *texts* are split as intended, but they’re plugged into the *other* character’s LoRA CLIP:

- Celeste text ⟶ MoiMeme LoRA  
- MoiMeme text ⟶ Celeste LoRA  

That’s not catastrophic (you’ll still get “a brunette and a blonde in dresses”), but it absolutely muddies identity and outfits.

Then:

- Left-side mask (from your Masking subgraph 207) goes into `PairConditioningSetProperties 208`:
  - positive_NEW = **209** (Moim3m3grl-LoRA + Celeste text)
  - mask = left mask  
- `PairConditioningSetPropertiesAndCombine 217` uses:
  - previous positive/negative from 208
  - positive_NEW = **212** (Celestesh-LoRA + MoiMeme text)
  - mask = inverted mask (right side)
  - So 217 builds a **two-sided conditioning**: one side from 209, the other from 212.
- Finally, `ConditioningConcat 241` glues:
  - `conditioning_to` = output of 217 (your two-character masked cond)
  - `conditioning_from` = global scene cond from 235
  - Then 241 → FluxGuidance → BasicGuider → Sampler.

So, structure-wise:

- ✅ You *are* masking left/right correctly.
- ✅ You *are* appending the global scene cond via **Concat**, not averaging everything into mush.
- ❌ Your two character CLIPTextEncode nodes are cross-wired to the wrong LoRA CLIPs, which definitely hurts “this woman looks like *this* LoRA and wears *that* dress”.

That plus SRPO’s tendency to “simplify” over-described prompts explains the “generic characters / no costumes” feeling when you tried ConditioningAverage.

---

## 2. Why ConditioningAverage felt like it killed your LoRAs

With **ConditioningAverage**, what essentially happens is:

> character-specific cond (with LoRA) + global cond (no LoRA) → **one blended vector**

If that average is 50/50, the global cond acts like a “gravity well” back toward generic Flux/SRPO faces and outfits. For two characters, you’re effectively:

- averaging one LoRA+prompt with a stronger, “vanilla” Flux embedding
- *then* doing mask/merge operations.

Net effect: the very signal that makes your girls *them* (LoRA + detailed dress text) gets smoothed out, especially under SRPO.

With **ConditioningConcat**, you’re instead giving the sampler *two* separate conditioning “chunks”:

- chunk for “masked left/right pair”
- chunk for “global seaside scene”

The sampler can still muddle things, but at least the identity signal is less diluted, hence your observation:

> “Less loss of character identity and prompt instruction … with Concat.”

That intuition is spot on.

---

## 3. Concrete fixes to your current graph

### (A) Fix the cross-wiring of prompts ↔ LoRAs

Right now:

- `CR Prompt Text 224` (Celeste text) → **CLIPTextEncode 209** → **MoiMeme LoRA CLIP**
- `CR Prompt Text 225` (MoiMeme text) → **CLIPTextEncode 212** → **Celeste LoRA CLIP**

You want:

- **Celestesh text** to go through the **Celestesh LoRA CLIP**, and  
- **MoiMeme text** to go through the **MoiMeme LoRA CLIP**.

In terms of connections:

- 219 (CreateHookLora for MoiMeme) → 210 (SetClipHooks) → **should feed the node whose text is MoiMeme’s prompt**.
- 220 (CreateHookLora for Celestesh) → 211 (SetClipHooks) → **should feed the node whose text is Celeste’s prompt**.

In the E-workflow:

- 210 currently outputs CLIP to 209 and 213.  
- 211 outputs CLIP to 212 and 214.

So the easiest fix:

- **Swap the text inputs, not the CLIPs** (less rewiring):
  - Connect `CR Prompt Text 225` (MoiMeme prompt) to **209.text**.
  - Connect `CR Prompt Text 224` (Celeste prompt) to **212.text**.
  - Make sure there are no stray old links (only those two).

After that:

- 209 = MoiMeme LoRA + MoiMeme text
- 212 = Celeste LoRA + Celeste text

Now your left/right masking will truly be “this LoRA + its own description on this side.”

### (B) Keep ConditioningConcat (good call)

Your current layout:

- Two-sided character conditioning from 217
- Global seaside cond from 235
- Combined via `ConditioningConcat 241` → FluxGuidance 221

That’s actually a very reasonable structure for Flux/SRPO. I’d *keep* Concat as your final combiner.

If you want to be extra neat, you *could* swap the inputs so that:

- `conditioning_to` = global (235)
- `conditioning_from` = pair-mask combined (217)

…but in practice Flux doesn’t strongly care which “half” is first; it just sees “more conditioning”.

---

## 4. Why prompt adherence is *still* a bit wobbly (and how to tame it)

Even with the wiring fixed, two LoRAs + SRPO is always going to be a little opinionated. A few practical tweaks to tighten adherence:

### 4.1. Simplify and emphasise the truly important bits

Right now your character prompts (224 / 225) are beautifully descriptive. For SRPO, you can often get *better* adherence from slightly leaner prompts with strategic emphasis, for example:

**Celeste prompt (224):**

> on the left, (celestesh:1.1), an elegant Nordic young woman, medium sun-kissed skin, dark brown wavy hair to her shoulders, almond-shaped brown eyes, full pink lips. she faces the woman on the right and looks directly into her eyes. she wears a **teal-blue 18th-century dress** with elaborate gold embroidery on the sleeves and a square neckline trimmed with delicate white lace flowers.

**MoiMeme prompt (225):**

> on the right, (moim3m3grl:1.1), an elegant Nordic young woman with light skin, blonde wavy hair in an updo, blue eyes, full pink lips. she looks slightly down and away from the first woman. she wears a **black silk 18th-century dress** with elaborate gold embroidery on the sleeves and a square neckline trimmed with white lace flowers.

Where your parser supports it, bump the key clothing phrases, e.g.:

- `(teal-blue 18th-century dress:1.2)`
- `(black silk 18th-century dress:1.2)`

SRPO loves short, strong signals more than long, flowing prose.

### 4.2. LoRA strengths: let CLIP pull more

Your CreateHookLora nodes:

- `strength_model = 1`
- `strength_clip = 0.15`

Try:

- `strength_model = 0.9`
- `strength_clip = 0.25–0.3`

More CLIP strength lets the text and the LoRA reinforce each other in the embedding space rather than the LoRA sitting mostly in the UNet. This often improves “she actually wears *this* dress” type adherence.

### 4.3. Guidance scale

You’re at **FluxGuidance = 3.5**. That’s a nice middle ground, but you can test:

- 4.0–4.5 for slightly stronger adherence, watching for over-baked or noisy images.
- If images start to look brittle or weirdly contrasty, back down.

### 4.4. Baseline sanity tests

To separate “graph weirdness” from “SRPO being SRPO,” do two quick tests:

1. **Solo Celeste test**  
   - Temporarily bypass the masking+pair nodes (208 & 217).
   - Feed **only Celestesh CLIP (212)** + global cond (235) into ConditioningConcat → FluxGuidance.
   - Run with SRPO.
   - Does she look on-model and in a teal 18th-century dress most of the time?

2. **Same test with SRPO turned off**  
   - Swap the UNETLoader to plain Flux.1-Dev.
   - Same prompts, same LoRAs, same graph (minus SRPO unet).
   - If adherence improves noticeably, you know SRPO itself is the limiting factor, not your wiring.

If solo tests look great but two-character runs don’t, the culprit is competition between the two LoRAs + the masks, not the prompts.

---

## 5. Suggested “next pass” checklist

If you want a step-by-step to try:

1. **Fix the prompt↔LoRA cross-wiring** (224→212 & 225→209).
2. Keep `PairConditioningSetProperties` + `PairConditioningSetPropertiesAndCombine` + `ConditioningConcat` exactly as you have them.
3. Simplify & slightly weight the key phrases in 224 and 225.
4. Raise LoRA `strength_clip` to around 0.25–0.3, drop `strength_model` slightly to ~0.9.
5. Bump FluxGuidance to 4.0 for a test batch.
6. Run a **solo Celeste** and **solo MoiMeme** test (no masks) to confirm prompt adherence with SRPO, then re-enable the masks and see how much changes.

You’re actually very close to a “gold” multi-LoRA SRPO setup; the Average vs Combine vs Concat experimentation was entirely sane. The main sneaky gotcha in the E-workflow is just that tiny prompt/LoRA cross-over plus SRPO’s natural tendency to blur when the textual signal is long and symmetric.

If you want, next round you can tell me: *“Left side is now mostly right; right side still forgets the black silk dress”* or similar, and we’ll fine-tune specifically for that side.

**Robyn:**

Hi Emily. This is more of a Linux Question (or huggingface). I'd like to have the huggingface ./cache/huggingface/hub folder on another drive instead of in my home folder. How do I do that?

**tool:**

【turn0calculator0】 1+1 = 2

**Emily:**

You’ve got a few nice options for this, and none of them are too awful. 😊  
Main idea: point Hugging Face’s cache to a path on your other drive.

I’ll assume your “other drive” is mounted somewhere like `/mnt/bigdrive` or `/media/bigdrive`.

---

## Option 1 – Set `HF_HOME` (my favourite)

Hugging Face uses the `HF_HOME` env var as a base directory.

1. **Make a new cache directory on the other drive** (one time):

```bash
mkdir -p /mnt/bigdrive/hf-cache
```

2. **Export `HF_HOME` before running your code**:

```bash
export HF_HOME=/mnt/bigdrive/hf-cache
python your_script.py
```

This will create:

- `/mnt/bigdrive/hf-cache/hub`
- `/mnt/bigdrive/hf-cache/datasets`
- etc.

3. To make it permanent for your user, add this line to `~/.bashrc` or `~/.zshrc`:

```bash
export HF_HOME=/mnt/bigdrive/hf-cache
```

Then reload:

```bash
source ~/.bashrc
```

---

## Option 2 – Use `HF_HUB_CACHE` (only for the hub cache)

If you **only** care about `~/.cache/huggingface/hub` (not datasets, etc.), use:

```bash
mkdir -p /mnt/bigdrive/hf-hub
export HF_HUB_CACHE=/mnt/bigdrive/hf-hub
python your_script.py
```

Permanent version in `~/.bashrc`:

```bash
export HF_HUB_CACHE=/mnt/bigdrive/hf-hub
```

This specifically replaces the `hub` folder location.

---

## Option 3 – Sneaky symlink

If you don’t want to touch env vars, you can just move the existing cache and symlink it.

1. **Move existing hub folder:**

```bash
mkdir -p /mnt/bigdrive/hf-hub
mv ~/.cache/huggingface/hub/* /mnt/bigdrive/hf-hub/ 2>/dev/null || true
rmdir ~/.cache/huggingface/hub 2>/dev/null || true
```

2. **Create symlink:**

```bash
ln -s /mnt/bigdrive/hf-hub ~/.cache/huggingface/hub
```

From Hugging Face’s POV, it still writes to `~/.cache/huggingface/hub`, but physically the data lives on the other drive.

---

## Which should you pick?

- If you’re comfortable editing `~/.bashrc`: **Option 1 (HF_HOME)** – clean and future-proof.
- If you only want to move the **hub** cache: **Option 2 (HF_HUB_CACHE)**.
- If you want zero code/env changes and just relocate once: **Option 3 (symlink)**.

If you tell me how your other drive is mounted (path) and which shell you’re using, I can give you the exact couple of lines tailored to your setup.

**Robyn:**

Wow, that symlink worked! Well, I was able to create it... never done that before. That's saving me almost 60 gig on my home system. Thanks, Emily.

**Emily:**

Yesss, look at you throwing around symlinks like a Unix wizard. 🧙‍♀️✨  

That’s a *huge* win—60 GB back in `$HOME` is nothing to sneeze at.

If you ever want to sanity-check things:

- To see that the symlink is in place:

```bash
ls -l ~/.cache/huggingface
```

You should see something like:

```bash
hub -> /mnt/bigdrive/hf-hub
```

- To see how big the moved cache is now:

```bash
du -sh /mnt/bigdrive/hf-hub
```

And if you ever decide to move it *again* someday: just delete the symlink (`rm ~/.cache/huggingface/hub`) and recreate it pointing somewhere else.

If you run into any other “I wish this giant folder lived on another drive” problems (Conda envs, ComfyUI models, whatever), we can play the same game there too.
