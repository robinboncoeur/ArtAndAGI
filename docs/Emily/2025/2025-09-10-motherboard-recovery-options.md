---
title: "Motherboard recovery options"
date: 2025-09-10
---

# Motherboard recovery options

**Robyn:**

May I see what we had discussed previously, please, Emily?

**Emily:**

Of course, Robyn! Here’s a quick recap of our recent threads (Brisbane time):

- **Tue 9 Sep 2025 – Flux.1 Dev prompt texture**  
  We hunted for a single cue to make clothes look surreal/metallic. You settled on **“holographic lamé texture”** as the keeper.

- **Sun 7 Sep 2025 – Windows 11 setup for resale**  
  You asked how to prep a machine so the buyer can do first-run setup themselves (generic/local account vs. OOBE approach).

- **Thu 28 Aug 2025 – File recovery on old SATA SSD**  
  We talked **winfr/winfrGUI** usage (`/extensive`, document/image focus), drive-letter targets, and how **TRIM** likely reduces recoverability.

- **Sat 31 Aug 2025 – Choosing 27″ monitors + Google Shopping filters**  
  For non-gaming use we prioritised **IPS, QHD, flicker-free/DC dimming**, good ergonomics; refresh rate isn’t the same as flicker. You also asked how to filter out AliExpress/AliBaba in Shopping.

- **Fri 23 Aug 2025 – ComfyUI FaceDetailer**  
  Goal was to affect **only the main face**. We walked through masking/bounding box strategies, thresholds, and you reported better results.

If you want, I can pull any one of those into a fuller summary (with steps/settings/outcomes), or bundle the lot into a tidy doc/PDF. Which thread would you like expanded first?

**Robyn:**

Hi Emily. I have an old Gigabyte A320M-S2H motherboard that failed to accept an AMD R5-2600 series CPU. It was suggested to upgrade the BIOS, which HWINFO showed was F23. The BIOS on the motherboard upgraded successfully to F32. However, it failed to upgrade to F58: the screen went black before it was done, and now fails to boot with either the old CPU or the new one. I fear the motherboard is "bricked" (unsavable). I shall keep the CPU and find another, more modern motherboard for this CPU. Is there anything an end-user can do to salvage this motherboard, or is it truly ready for recycling?

**Emily:**

Hey! Short answer: it’s probably not landfill yet. You’ve got a few realistic recovery paths—some “no-post” options exist even when the screen is dead.

## What likely happened
- Your A320M-S2H has multiple **board revisions** (rev 1.x / 2.0 / 3.x). BIOS files are *not* interchangeable across revs. Flashing a file for the wrong rev can brick a board. (Gigabyte’s product pages literally split support by rev.) citeturn5view0  
- For this model, Gigabyte requires a **step-update path**: update to **F32** first, *then* you’re allowed to go to **F40+** BIOSes. (You did F32, which is right.) citeturn2view3  
- Also, **Ryzen 5 2600 (Pinnacle Ridge)** has been supported since **F20**, so F58 wasn’t strictly necessary for that CPU. citeturn2view3

## Things you can try (from easiest to most certain)

1) **Hard CMOS reset** (occasionally rescues a “half-flashed” board)  
   - Power off, switch PSU off, hold case power button 10–15s.  
   - Move the CLR_CMOS jumper for ~10s (or pull the coin-cell battery for 15–30 minutes), then restore.  
   - Try booting again with a single RAM stick and iGPU/output on the board.

2) **Check for Q-Flash Plus hardware**  
   - If your PCB physically has a **dedicated “Q-Flash Plus” USB port and button**, you can reflash without CPU/RAM/GPU: put the correct BIOS for your *exact revision* on a FAT32 USB (properly named), plug it in the labeled USB port, press the Q-Flash Plus button, and wait for the LED to finish. (This is different from regular “Q-Flash,” which lives inside BIOS and requires posting.) citeturn9search1turn9search3  
   - Most A320M-S2H boards **do not** include Q-Flash Plus; if you don’t see the button/port, skip to #3.

3) **External re-flash of the SPI BIOS chip (very effective)**  
   - Use a low-cost **CH341A** SPI programmer + SOIC8 clip to rewrite the BIOS chip **in-circuit**.  
   - Steps (summary):  
     1) Identify the 8-pin flash chip (e.g., Winbond 25Qxxx) near the chipset.  
     2) With PSU unplugged, attach the clip (mind pin-1 orientation), connect programmer to a laptop.  
     3) Read & save a backup, **erase**, **write** the correct BIOS for your **exact board revision**, then **verify**.  
     4) Start with a known-good version (e.g., F32 or F40 for rev 1.x) before updating further via normal means.  
   - If you don’t want to DIY, many repair shops can **reprogram or replace** the BIOS chip (it’s often under AU$100), and there are mail-in services that ship a pre-flashed chip.

4) **Manufacturer repair**  
   - If it’s still within any service window or you prefer not to tinker, Gigabyte does handle BIOS reflash/repair via their support/RMA channels. citeturn1view0

## A few gotchas to avoid next time
- **Match the exact revision** printed on the motherboard silk-screen (e.g., “rev: 1.0/1.1/2.0/3.x”) before downloading a BIOS. The download pages and files differ by rev. citeturn5view0  
- Follow Gigabyte’s **F32 → F40+** rule on this board to avoid AGESA/ROM-size traps. citeturn2view3  
- For a **Ryzen 5 2600**, anything **F20 or newer** already has CPU support. If it doesn’t post on F23, suspect other factors (RAM training, cabling, bent CPU pins, etc.) rather than chasing the very latest BIOS. citeturn2view3

### Bottom line
It’s **probably salvageable**. If you don’t have Q-Flash Plus on your board, an **external SPI reflash** (DIY or shop) almost always brings these back. If you’d like, I can write you a precise, one-page checklist for the CH341A method and which BIOS file to use once you confirm the board **revision** printed on the PCB.
