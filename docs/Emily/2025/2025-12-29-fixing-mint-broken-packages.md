---
title: "Fixing Mint Broken Packages"
date: 2025-12-29
---

# Fixing Mint Broken Packages

**Robyn:**

Hi Emily. I just upgraded my Ryzen 5 PC from 8 to 16 gig VRAM 5060ti card. Linux Mint 21.3 seems to have trouble configuring it correctly. I'm at the CLI in the GUI... are there any commands I can enter to get X11 to recognise the card? BTW, the flatpak.desktop NVidia graphics driver just now updated.

**Emily:**

Yep — you can do a lot from the terminal, but first: that **Flatpak “org.freedesktop.Platform.GL.nvidia …” update is *not* your system’s NVIDIA driver**. It’s a *userspace* OpenGL/Vulkan runtime used **only by Flatpak apps**, and it has to match whatever NVIDIA driver you have installed on the host. It won’t make X11 suddenly “see” the card by itself. citeturn1view5turn0search19turn0search3

Also, for the **RTX 5060 Ti specifically**, multiple reports indicate you need **the “open kernel modules” variant** and a **minimum ~570.153.xx**-class driver; the “fully proprietary” kernel module path may fail for this GPU on Mint/Ubuntu-family setups. citeturn1view1

Below is the fastest CLI checklist + the usual fixes.

---

## 1) Confirm what X11 is actually using (and whether NVIDIA loaded)

Run these **exactly as-is**:

```bash
# Are you in X11 at all?
echo "DISPLAY=$DISPLAY  XDG_SESSION_TYPE=$XDG_SESSION_TYPE"
ps -e | egrep 'Xorg|Xwayland' | grep -v egrep

# What GPU(s) does the kernel see and what driver is bound?
lspci -nnk | sed -n '/VGA compatible controller\|3D controller/,+4p'

# Is the NVIDIA kernel module loaded?
lsmod | egrep 'nvidia|nouveau' | cat

# If the driver is alive, this works
nvidia-smi || true

# Mint/Ubuntu also logs GPU decisions here:
cat /var/log/gpu-manager.log 2>/dev/null | tail -n 120
```

**Interpretation (quick):**
- If `lspci -nnk` shows your NVIDIA device but **“Kernel driver in use” is not `nvidia`**, X won’t use it properly yet.
- If `nvidia-smi` says it can’t communicate, your NVIDIA kernel module isn’t loaded (or is blocked).
- `gpu-manager.log` often bluntly tells you what it decided and why. (Mint forum helpers rely on it for this exact issue.) citeturn1view1

---

## 2) The #1 gotcha: Secure Boot quietly blocks the NVIDIA module

Check:

```bash
mokutil --sb-state
```

If it says **SecureBoot enabled**, that’s very often why `nvidia` won’t load. Mint users with 50xx cards hit this a lot. citeturn1view1

**Fix:** disable Secure Boot in BIOS/UEFI *or* enroll/sign the module (MOK). Disabling is the quickest sanity test.

---

## 3) Make sure you’re installing the *right* driver (5060 Ti wants “-open”)

On Mint 21.3 (Ubuntu 22.04 base), the default repos may be too old. You want to see what Mint thinks is available:

```bash
ubuntu-drivers devices
apt-cache search '^nvidia-driver-[0-9]+' | sort -V | tail -n 30
```

What you’re aiming for (for this GPU class) is typically:

- `nvidia-driver-570-open` **or newer** (and specifically an **“open kernel modules”** build). citeturn1view1

### If Mint 21.3 doesn’t offer 570/575+ in your current repos
A common Ubuntu-family route is the graphics-drivers PPA (not “pure Mint official,” but widely used):

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
apt-cache search '^nvidia-driver-(570|575).*open' | sort -V
```

Then install the newest *open* option you see (example shown — pick what actually appears on your machine):

```bash
sudo apt install nvidia-driver-570-open
```

Reboot after driver/kernel module changes.

*(Why this matters: reports indicate 5060 Ti needs at least ~570.153.xx and “open” modules to behave on Mint/Ubuntu stacks.)* citeturn1view1

---

## 4) If you have a Ryzen iGPU as well, X may be happily using *that* instead

Check providers:

```bash
xrandr --listproviders 2>/dev/null || true
```

And see what renderer you’re getting (install `mesa-utils` if needed):

```bash
glxinfo -B 2>/dev/null | egrep 'OpenGL vendor|OpenGL renderer|OpenGL version' || true
```

If it’s AMD/llvmpipe when you want NVIDIA, then after the correct driver is installed you may need to select the NVIDIA path (varies by setup). On many Mint/Ubuntu systems:

```bash
prime-select query 2>/dev/null || true
```

If `prime-select` exists, switching is:

```bash
sudo prime-select nvidia
sudo reboot
```

(If you don’t have `prime-select`, no stress — the earlier driver binding checks are still the real truth.)

---

## 5) If you’re stuck at a CLI “inside the GUI” and want to restart X cleanly

Mint Cinnamon typically uses LightDM. After installing the driver (and ideally after reboot), you can restart the display manager:

```bash
sudo systemctl restart lightdm
```

If you’re unsure which DM:

```bash
systemctl status display-manager --no-pager
sudo systemctl restart display-manager
```

Then check `/var/log/Xorg.0.log` for NVIDIA errors:

```bash
grep -E "(EE)|NVRM|nvidia" /var/log/Xorg.0.log | tail -n 80
```

---

## The fastest path I’d try in your shoes
1) Run the block in section **1** and see if `nvidia` is bound + whether `nvidia-smi` works.  
2) If not, check **Secure Boot** (section **2**).  
3) Ensure you’re on a **570+ “-open”** driver line (section **3**), which is a known requirement for 5060 Ti-class support on Mint/Ubuntu. citeturn1view1

If you paste the outputs of:
- `lspci -nnk | sed -n '/VGA compatible controller\|3D controller/,+4p'`
- `nvidia-smi`
- `mokutil --sb-state`
- last ~80 lines of `/var/log/gpu-manager.log`

…I can tell you *exactly* which branch you’re in (secure-boot block vs wrong driver vs iGPU stealing the session) and what single change will likely flip it.

**Robyn:**

It failed here, Emily:

Then install the newest open option you see (example shown — pick what actually appears on your machine):
sudo apt install nvidia-driver-570-open

Says I hold broken packages. I'll probably have to do a complete re-install of Mint. Here's the thing: on another SSD (mounted to the MB, I have a Windows11 install. I was going to do an update, but now it is telling me I need a MS account. On that system, I have a MS account. I am NOT going to struggle with MS for an OS I really don't want - it is getting dodgier and dodgier - and so will wipe Win11, copy my Comfy stuff to that empty (new) partitition and re-install Mint.

**Emily:**

Ah — “held broken packages” is *exactly* the sort of thing that makes you want to throw the whole OS in the sea… but it’s usually recoverable. And even if you still decide to reinstall (totally fair), we can make that reinstall **clean, fast, and driver-proof**.

Below are two paths: **(A) fix Mint now** and **(B) wipe Windows, reinstall Mint, restore Comfy**.

---

## A) Fix Mint 21.3 without reinstall (most likely fix)

### 1) See what’s actually “held”
Run:

```bash
apt-mark showhold
```

If it lists anything NVIDIA-ish (or kernels), unhold them:

```bash
sudo apt-mark unhold <package-name>
```

Then:

```bash
sudo apt update
sudo dpkg --configure -a
sudo apt --fix-broken install
```

This “dpkg + fix-broken” combo clears a lot of half-installed driver states. (It’s the standard first move for this exact error class.) citeturn0search10

### 2) Check if you’ve got a version-mismatch conflict in the NVIDIA stack
A common modern failure is: one repo offers `nvidia-firmware-570` or `libnvidia-*` at one version, while the driver metapackage pulls another — the solver gives up and screams “broken packages.” There are active reports of this kind of dependency conflict on Ubuntu 22.04-family systems. citeturn0search7

To inspect versions you’re pulling from repositories:

```bash
apt-cache policy nvidia-driver-570-open nvidia-firmware-570 | sed -n '1,120p'
```

If you see mixed origins (e.g. some from a PPA, some from Ubuntu repos, some from CUDA repo), that’s often the culprit.

### 3) If your system is already “poisoned” by partial NVIDIA installs, do a clean purge and re-install
This is the “wipe the driver stack, not the OS” approach:

```bash
sudo apt purge 'nvidia-*' 'libnvidia-*'
sudo apt autoremove --purge
sudo apt --fix-broken install
sudo reboot
```

After reboot, install via **Driver Manager** if possible, or via CLI once the package system is healthy again.

### 4) Kernel reality check (important for new cards)
Mint 21.3 ships with the older 5.15 kernel by default; Mint themselves provide an **Edge ISO** specifically because newer hardware often needs newer kernels — the 21.3 Edge ships with kernel **6.5**. citeturn1search1turn1search21

So even if you fix the packages, you may still be fighting the platform a bit on 21.3 unless you’re on Edge/HWE.

---

## B) If you’re done with it: wipe Win11, reinstall Mint, restore ComfyUI cleanly

### 1) About Windows 11 suddenly demanding a Microsoft account
You’re not imagining it. Windows 11 has been increasingly pushy about “online account” setup, and Microsoft has been actively closing common bypasses in newer builds (at least in Insider/Dev channel testing). citeturn0news39turn0news40turn0news41

If you ever need to reinstall Windows and keep it local: on many Windows 11 24H2 setups people have used **Shift+F10** during OOBE and run:

- `start ms-cxh:localonly` citeturn0search14turn0search18  
- or `OOBE\BYPASSNRO` (works on some builds; increasingly hit-or-miss) citeturn0search22turn0search0

But since you’re wiping Windows anyway: good riddance, honestly.

### 2) Back up ComfyUI properly (so the reinstall is painless)
On your current Mint, I’d back up **at least**:

- your whole `ComfyUI/` folder (especially `custom_nodes/`, `workflows/`, `input/`, `output/`)
- your models folders (often the biggest: `models/checkpoints`, `vae`, `clip`, `loras`, etc.)
- any Python venv/conda info (optional, but helpful)

If you’re copying to that new partition, `rsync` is your best friend:

```bash
sudo mkdir -p /mnt/backup
# example: if your new partition is /dev/nvme0n1pX
sudo mount /dev/nvme0n1pX /mnt/backup

rsync -aHAX --info=progress2 ~/ComfyUI /mnt/backup/
# if you keep models elsewhere, add those too:
# rsync -aHAX --info=progress2 /path/to/models /mnt/backup/
```

And grab a “recipe” of your Python environment (handy later):

```bash
python3 -m pip freeze > /mnt/backup/comfy_pip_freeze.txt 2>/dev/null || true
```

### 3) Reinstall Mint — but I would not go back to 21.3 for this GPU
Mint 22.2 is current and is designed around a newer Ubuntu base — much better odds for a new RTX card. citeturn1search0turn1search9

So I’d install **Linux Mint 22.2** (Cinnamon, MATE, whatever you prefer), then:

1) Update fully
2) Use **Driver Manager** to install the recommended NVIDIA driver
3) Confirm with:
   ```bash
   nvidia-smi
   glxinfo -B | egrep 'OpenGL vendor|OpenGL renderer'
   ```

---

## The key thing I’d do *right now*
Before you commit to the wipe, do this one tiny diagnostic on Mint (it often explains the entire “broken packages” story):

```bash
apt-mark showhold
apt-cache policy nvidia-driver-570-open nvidia-firmware-570 | sed -n '1,120p'
```

If you paste that output (just those two commands), I can tell you *whether it’s a simple unhold / repo mismatch / firmware conflict*, and give you the exact one-liner that usually resolves it — or confirm that reinstalling is genuinely the least-annoying route.

**Robyn:**

Here's the error I'm getting:

base) robyn@robyn-2600:~$ sudo apt install nvidia-driver-570-open
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 nvidia-dkms-570-open : Depends: dkms (>= 3.1.8) but 2.8.7-2ubuntu2.2mint1 is to be installed
E: Unable to correct problems, you have held broken packages.

**Emily:**

Perfect — that error is *very* revealing, and it means your Mint 21.3 package ecosystem simply can’t satisfy what you’re asking for.

### What the error actually means
`nvidia-dkms-570-open` requires **dkms ≥ 3.1.8**, but Mint 21.3 (Ubuntu 22.04 “jammy” base) provides **dkms 2.8.7** (the exact version you see in the message). So apt isn’t “being difficult” — it’s telling you the request is **mathematically impossible** on that base without pulling in a newer DKMS from a newer distro (which is where systems get… messy). citeturn0search2turn1search4

So: you’re trying to install a **driver packaging stream meant for a newer base** than Mint 21.3.

---

## Option 1 (recommended): Reinstall/upgrade Mint to a newer base, then install NVIDIA normally
If you’re already mentally committed to wiping Windows and reinstalling Mint, do it — but I’d strongly steer you to **Mint 22.2** (current stable) or **Mint 22.3** (currently beta as of Dec 2025). citeturn1search0turn1search3

On Mint 22.x, you’ll be on a newer stack and this DKMS mismatch problem goes away in the normal course of things.

**After reinstall:**
1. Run Update Manager updates first.
2. Open **Driver Manager** and install the recommended NVIDIA driver.
3. Confirm:
   ```bash
   nvidia-smi
   ```

*(Also: keep Secure Boot off during initial bring-up if you can — it’s a classic “module won’t load” trap.)*

---

## Option 2: Salvage Mint 21.3 by backing out the 570 packages cleanly
This is what you do if you want to get Mint “back to sane” *before* you wipe anything.

### Step A — identify where those 570 packages came from
Run:

```bash
apt-cache policy nvidia-dkms-570-open dkms | sed -n '1,160p'
```

If you see a PPA (often `ppa:graphics-drivers/ppa`) or an NVIDIA/CUDA repo, that’s your mismatch source.

### Step B — if it’s the graphics-drivers PPA, purge it back to Mint’s versions
```bash
sudo apt install ppa-purge
sudo ppa-purge ppa:graphics-drivers/ppa
sudo apt --fix-broken install
```

That will revert packages to versions compatible with Mint 21.3.

### Step C — if you just want to nuke all NVIDIA attempts and start over on 21.3
```bash
sudo apt purge 'nvidia-*' 'libnvidia-*'
sudo apt autoremove --purge
sudo apt --fix-broken install
```

After that, Mint 21.3 will typically offer something like 535/550-era drivers via Driver Manager — but whether those support your **5060 Ti** properly is the big question, and it’s why the clean solution is really Mint 22.x.

---

## About your wipe plan (Win11 → Mint + Comfy)
If you’re wiping Windows anyway, your strategy is solid: **copy ComfyUI + models to the “empty/new” partition first**, *then* wipe, *then* install Mint, *then* copy it back.

The one thing I’d do *before* you touch partitions is make a “no surprises” backup copy command (adjust paths as needed):

```bash
# Example target mountpoint; use your actual one
lsblk -f
sudo mkdir -p /mnt/backup
sudo mount /dev/nvme0n1pX /mnt/backup

rsync -aHAX --info=progress2 ~/ComfyUI /mnt/backup/
```

---

### If you want the fastest, least-drama path
Given your new GPU and your stated willingness to wipe: **go straight to Mint 22.2** (or 22.3 once it’s final), then install the NVIDIA driver via Driver Manager. Mint themselves position 22.2 as the current release, and 22.3 is in beta right now. citeturn1search0turn1search3

If you paste the output of:
```bash
apt-cache policy nvidia-dkms-570-open dkms | sed -n '1,160p'
```
…I can tell you *exactly* which repo introduced the “DKMS ≥ 3.1.8” requirement and give you the cleanest removal command for that specific case (PPA vs CUDA repo vs something else).
