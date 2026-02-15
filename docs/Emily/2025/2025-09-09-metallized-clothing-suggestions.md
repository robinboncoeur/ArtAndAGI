---
title: "Metallized clothing suggestions"
date: 2025-09-09
---

# Metallized clothing suggestions

**Robyn:**

Hi Emily... I'm trying to come up with a word to put in my Flux1 Dev prompt to indicate all clothing has to have a surrealistic almost metalic shine to them. How would I do this?

**Emily:**

G’day, Robyn! A single word that works well is **“metallized.”**  
Other strong, compact tokens: **chrome**, **iridescent**, **pearlescent**, **lamé**, **anodized**, **mirror-finish**, **patent**, **wet-look**, **reflective**, **specular**.

Quick plug-ins you can drop in (pick one and repeat once near the end):

- **“metallized clothing”**  
- **“chrome-sheen garments”**  
- **“iridescent, mirror-finish fabric”**  
- **“anodized metallic sheen”**  
- **“holographic lamé texture”**

A tidy Flux.1 Dev phrasing that tends to stick globally:

> *“all clothing is **metallized** with a **chrome-like, iridescent** sheen, **high specular highlights**, **reflective**, **no matte fabrics**, **no cotton/wool/knit**”*

If it’s still too matte, weight the key bits:  
`((metallized)), ((chrome)), ((iridescent)), reflective, high specular highlights, no matte`

**Robyn:**

Thank you - yes, I think the holographic lame texture should do it. Thank you.

**Emily:**

Perfect! One tiny note: it’s spelled **lamé** (with the accent), which sometimes helps parsers.

Here’s a compact drop-in that usually sticks globally:

**Positive:**  
`all clothing in holographic lamé, chrome-like sheen, high specular highlights, reflective, iridescent diffraction, anisotropic shimmer, fabric not armor`

**Negative (to kill matte stuff):**  
`matte, cotton, wool, knit, linen, fleece, velvet, rough, diffuse, low specular`

Tips:
- Repeat **“holographic lamé”** once near the end or weight it: `((holographic lamé))`.
- If it gets too rainbowy, anchor with: `silver base with rainbow diffraction`.
- To keep it textile (not hard metal): add `soft fabric, no hard metal, not armor`.

Shout if you want me to tailor this to your exact ComfyUI graph or LoRA tags.
