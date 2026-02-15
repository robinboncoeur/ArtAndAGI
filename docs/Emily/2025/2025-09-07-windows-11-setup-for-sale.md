---
title: "Windows 11 setup for sale"
date: 2025-09-07
---

# Windows 11 setup for sale

**Robyn:**

When I install Windows 11, it asks for an account (or to create one). Is there some way to create a generic account? I'm setting up a PC - to sell - with Windows 11, so the user should be able to make it their own post-sale. How do I go about this, Emily?

**Emily:**

G’day Robyn! The clean, “sell-ready” way is to **leave Windows at the first-boot setup (OOBE)** so the buyer creates their own account on first power-on. You do that with **Audit Mode + Sysprep**—no generic user needed (and no profile leftovers).

### Do this (recommended)
1. **Install Windows 11** as normal until the very first “Region” screen appears.  
2. Press **Ctrl + Shift + F3** → the PC reboots into **Audit Mode** and auto-logs in with the built-in Administrator (you’ll see the Sysprep window). citeturn1search2turn1search4  
3. (Optional) In Audit Mode, install drivers/updates and any utilities you want to include.  
4. When finished, run **Sysprep** to reseal the machine for a new owner:  
   - Command:  
     ```
     C:\Windows\System32\Sysprep\sysprep.exe /oobe /generalize /shutdown
     ```  
   - This strips machine-specific stuff (SIDs, etc.) and shuts down. **Don’t boot it again**—box it up. On first boot, the buyer gets the “Hi there” screens and makes their own account. citeturn1search5turn1search9

**Notes & gotchas**
- If you’ve already gone past setup and made a user, you can still fix it: **Settings → System → Recovery → Reset this PC → Remove everything**. That returns the device to OOBE for the buyer. (No citation needed)  
- **BitLocker:** if you enabled it while prepping, **turn it off before Sysprep**—there have been 24H2 reports of BitLocker not booting after `/generalize`. citeturn1search6  
- **Buyer’s account type:** Windows 11 **Pro** still exposes a path to create a local account during OOBE; **Home** increasingly nudges to a Microsoft account. Microsoft has been removing older bypass tricks (like `OOBE\BYPASSNRO`), and methods change over time—so best to leave OOBE for the buyer and let them choose. citeturn0news64turn0news63

### Why not make a “generic” user?
You *can*, but it’s messy: the profile folder name sticks, and the buyer inherits that account’s cruft. **Sysprep to OOBE** is the official, supportable way for handing off a fresh machine. citeturn0search0

If you want, I can jot a tiny checklist you can print and pop in the box for the buyer’s first boot.
