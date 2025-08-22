# ComfyUI Tips and Tricks

## LoRA Notes

### Yet Another Watercolor Style

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
