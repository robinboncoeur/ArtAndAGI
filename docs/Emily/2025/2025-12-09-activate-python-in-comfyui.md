---
title: "Activate Python in ComfyUI"
date: 2025-12-09
---

# Activate Python in ComfyUI

**Robyn:**

Hi Emily. I'm working in an environment I'm not really comfortable with: Windows11. I need to activate the python environment so I can run some pip commands. The Python environment needs to be that which gets activated when load ComfyUI.

**Emily:**

Short version: you don’t really “attach” to a running ComfyUI, you just need to use **the same Python that ComfyUI uses** when you run `pip`. Here’s how to do that on Windows 11, depending on how you installed ComfyUI.

---

## 1. If you used the **Windows portable zip** (most common)

Your ComfyUI folder probably looks something like:

- `ComfyUI_windows_portable\`
  - `ComfyUI\`
  - `python_embeded\`
  - `run_nvidia_gpu.bat` / `run_cpu.bat` / etc.

In this case, ComfyUI uses the Python in `python_embeded`. You don’t need to “activate” it like a venv; just run pip through that exact Python.

### Steps

1. **Open a terminal in the ComfyUI folder**

- Right-click inside the `ComfyUI_windows_portable` folder →  
  **Open in Terminal** (or open Windows Terminal and `cd` there):

```powershell
cd "C:\path\to\ComfyUI_windows_portable"
```

2. **Use the embedded Python to run pip**

From that folder, run:

```powershell
.\python_embeded\python.exe -m pip install package_name
```

Examples:

```powershell
.\python_embeded\python.exe -m pip install opencv-python
.\python_embeded\python.exe -m pip install --upgrade pip
```

That guarantees you’re installing into **the same environment ComfyUI uses**.

3. **Optional: check that it worked**

```powershell
.\python_embeded\python.exe -m pip list
```

You don’t need `activate` here – calling `python_embeded\python.exe -m pip` *is* the “activation”.

---

## 2. If you installed ComfyUI from Git with a **virtualenv**

If your ComfyUI folder has something like `venv` or `.venv` in it, and you remember running `python -m venv venv`, use this:

### PowerShell (default in Windows 11 Terminal)

```powershell
cd "C:\path\to\ComfyUI"
.\venv\Scripts\Activate.ps1
```

You should see something like `(venv)` at the start of the prompt. Then:

```powershell
pip install package_name
```

or (safer):

```powershell
python -m pip install package_name
```

When you’re done:

```powershell
deactivate
```

### Command Prompt (cmd.exe)

```cmd
cd C:\path\to\ComfyUI
venv\Scripts\activate.bat
pip install package_name
deactivate
```

---

## 3. Easiest “always correct” trick

If you’re ever unsure which Python ComfyUI uses:

1. Open the `.bat` file you use to start ComfyUI (e.g. `run_nvidia_gpu.bat`) in a text editor.
2. Look for the line that runs Python – something like:

   ```bat
   python_embeded\python.exe -s ComfyUI\main.py
   ```

3. Use that exact Python path plus `-m pip` in your terminal, e.g.:

   ```powershell
   cd "C:\path\to\ComfyUI_windows_portable"
   .\python_embeded\python.exe -m pip install package_name
   ```

That way you’re 100% in the right environment without having to juggle Windows’ global Python installs.

---

If you tell me which ComfyUI folder layout you see (e.g. you spot `python_embeded` vs `venv`), I can give you a one-liner tailored exactly to your setup.

**Robyn:**

Hi Emily. Sad news: it seems everything in ComfyUI is failing. Have they updated their minimum Python version or something? I'm looking at having to reinstall ComfyUI - QwenVL is failing, their LoRA Hook nodes are failing... the whole thing is coming apart at the seams.

**tool:**

【turn0calculator0】 1+1 = 2

**Emily:**

Yeah… that *does* sound like “Python/version soup” plus grumpy custom nodes, not you breaking everything. Let’s untangle it.

---

## 1. Did ComfyUI change Python requirements?

Short answer: **yes, things have shifted**, and that can absolutely upset custom nodes like QwenVL & LoRA Hook.

From the current docs / repo:

- Official docs now say:  
  > Recommended **Python 3.12**, supports **3.13** (some custom nodes may not be compatible). citeturn1search1turn1search8  
- The **portable Windows build** bundles its own embedded Python (`python_embeded`) and recent versions ship with **Python 3.11/3.12**. citeturn1search2turn1search5  
- Some heavyweight deps (llama-cpp, some LLM / VL wrappers, etc.) still explicitly **refuse** Python 3.12+ and only support 3.9–3.11, which is exactly what we see in recent issues. citeturn1search4  

So:

> ComfyUI itself is happy on newer Python…  
> but **some custom nodes are not**, and they can take the whole startup down with them.

That matches “QwenVL failing”, “LoRA Hook failing”, “everything coming apart”.

---

## 2. What likely happened on your system

Given what you told me earlier:

- You’re on **Windows 11**, using **ComfyUI portable** with `python_embeded`.
- You’ve been adding/updating custom nodes (QwenVL, LoRA Hook, etc.).
- At some point you probably:
  - Updated ComfyUI / ComfyUI-Manager **or**
  - Updated the **portable zip**, which now includes a newer embedded Python (3.11/3.12).

Now, nodes that depend on **specific wheels** (e.g. LLM/VL stuff like QwenVL, llama-cpp, special `transformers` builds, etc.) see Python 3.12 and either:

- Can’t find compatible wheels, or  
- Explicitly say “unsupported Python version, please use 3.9–3.11”.

Result: cascade of import errors / “failed to load custom node” across those packs.

The good news: you probably **don’t** need to obliterate everything. We can usually:

- Disable the broken packs, or  
- Reinstall them properly, or  
- Put them in a separate ComfyUI install with a Python they like.

---

## 3. First quick check – is it ComfyUI core or just custom nodes?

1. **Run ComfyUI from a terminal** so you can see errors:

   ```powershell
   cd "C:\path\to\ComfyUI_windows_portable"
   .\run_nvidia_gpu.bat
   ```

2. Watch the scroll for lines like:

   - `Traceback (most recent call last):`
   - `Error loading custom node: ...`
   - `Unsupported Python version. Please use Python 3.9, 3.10 or 3.11.`
   - `No module named ...`

If the only red stuff is under `ComfyUI\custom_nodes\...`, then **core ComfyUI is fine** and it’s “just” custom nodes misbehaving.

If it’ll help later, you can always open `comfyui.log` in the portable folder to see the same info.

---

## 4. Easiest stabiliser: temporarily disable the worst offenders

If QwenVL / LoRA Hook are exploding and stopping everything:

1. Go to:

   ```text
   ComfyUI_windows_portable\ComfyUI\custom_nodes\
   ```

2. Find the folders for the problem packs, e.g. (examples only):

   - `ComfyUI_QwenVL_something`
   - `ComfyUI_LoRA_Hook_something`

3. **Rename them** to disable:

   ```text
   ComfyUI_QwenVL_something  →  ComfyUI_QwenVL_something.disabled
   ComfyUI_LoRA_Hook_something  →  ComfyUI_LoRA_Hook_something.disabled
   ```

4. Run `run_nvidia_gpu.bat` again.

If the UI now starts and “normal” workflows run, you know the **core is healthy** and the problem is specifically with those packs under the new Python.

---

## 5. Installing node dependencies with the *correct* Python

When you *do* want to try fixing a node pack, always use the **embedded Python** we talked about earlier:

From inside `ComfyUI_windows_portable`:

```powershell
cd "C:\path\to\ComfyUI_windows_portable\ComfyUI\custom_nodes\SomeNodePack"
..\..\python_embeded\python.exe -m pip install -r requirements.txt
```

That ensures the dependencies land in the **same** `python_embeded` that ComfyUI uses.

If at this step you see:

- `Unsupported Python version. Please use 3.9, 3.10 or 3.11.`  
  → That node pack (or one of its deps) simply **doesn’t support Python 3.12+ yet**. You’ve done nothing wrong.

In that case, your options are:

- **Option A – park that node for now**  
  Keep it `.disabled` and run the rest of your setup normally.

- **Option B – separate older-Python ComfyUI just for those nodes**  
  Side-by-side install with Python 3.11 or 3.10 (see §7 below).

---

## 6. “Do I really have to reinstall ComfyUI?”

You can, **without losing your stuff**, but I’d still:

- Disable problem nodes  
- Confirm vanilla ComfyUI works  
first, because that tells us it’s not your models / configs / Windows being cursed.

If things are really mangled and you want a clean ComfyUI Portable:

### Safe “fresh core” reinstall (portable, Windows)

1. **Backup**:

   - Entire `ComfyUI_windows_portable` folder, or at minimum:
     - `ComfyUI\custom_nodes\`
     - `ComfyUI\models\`
     - `ComfyUI\user\` (your workflows and presets)
     - `extra_model_paths.yaml` if you made one

2. **Download a fresh portable** from the official docs link. citeturn1search5  

3. Extract it to a **new folder**, e.g.:

   ```text
   C:\AI\ComfyUI_windows_portable_clean\
   ```

4. Test it *as-is*:

   ```powershell
   cd "C:\AI\ComfyUI_windows_portable_clean"
   .\run_nvidia_gpu.bat
   ```

   Make sure you can get a simple SDXL / base Flux workflow to run.

5. **Copy your stuff back in slowly**:

   - First: models & user data  
     - `old\ComfyUI\models\` → `new\ComfyUI\models\`
     - `old\ComfyUI\user\` → `new\ComfyUI\user\`
   - Then: **custom_nodes one pack at a time**, each time restarting ComfyUI to see which one explodes.

As soon as you hit the pack that starts screaming about Python, you’ve identified the culprit. Leave that one out or `.disabled` in the new setup.

This way you get a fresh, known-good core, but keep your workflows and models.

---

## 7. If you *really* want QwenVL / LoRA Hook and they hate 3.12+

For picky packs that only support Python ≤3.11, one robust approach is:

### Side-by-side “legacy” ComfyUI with Python 3.11

1. Install **Python 3.11.x** from python.org (Windows installer).  
2. Create a separate ComfyUI install, e.g. `C:\AI\ComfyUI_311\` using the manual instructions with Python 3.11. citeturn1search3turn1search8  
3. Create a `venv`:

   ```powershell
   cd C:\AI\ComfyUI_311
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

4. Clone / drop your **QwenVL / LoRA Hook** node packs into `ComfyUI_311\ComfyUI\custom_nodes\` and run their `requirements.txt` using that 3.11 venv.

Those nodes will live in the comfy-311 instance, and you can keep using the portable 3.12 instance for everything else.

It’s more moving parts, but keeps the drama contained.

---

## 8. Where this leaves you

So in terms of your specific questions:

> **“Have they updated their minimum Python version or something?”**  

- ComfyUI core: **yes, it now happily supports newer Python (3.12/3.13 and even 3.14)**. citeturn1search1turn1search8  
- Your portable build likely updated its embedded Python.  
- **Some custom nodes (especially LLM/VL / LoRA toolchains)** are still stuck on <=3.11 and are now throwing tantrums.

> **“I’m looking at having to reinstall ComfyUI”**

You might choose to:

- Do a **clean portable reinstall** (keeping workflows and models) and leave incompatible nodes disabled, **or**
- Make a **separate 3.11-based ComfyUI** for those problem children.

You almost certainly don’t need to nuke everything from orbit – we just have to stop a couple of node packs from dragging the whole party down.

---

If you want, you can paste **one** of the error chunks (say, from the QwenVL node) next time and I can tell you specifically “this line = Python version mismatch” vs “missing dependency” vs “something else entirely.” But the steps above should already give you a solid path to get ComfyUI stable again.

**Robyn:**

Actually, I run ComfyUI primarily on Linux (Mint) - although I do have a tiny Window 11 install. I'm just copying the entire install to a separate HDD along with the Conda env. Looks like I'll do a Conda install using Python 3.12, then. Hopefully, I'll be able to just load a workflow and install missing nodes. Sound like an option?

**Emily:**

Yup, that’s a perfectly reasonable plan **in principle** — with one big caveat:

> If you care about QwenVL / LoRA Hook / other heavier custom nodes,  
> **Python 3.11 is safer than 3.12 right now.**

ComfyUI core is fine on 3.12, but a lot of AI/LLM/VL dependencies are *still* dragging their feet and only officially support up to 3.11. That’s exactly the class of stuff that tends to explode first (Qwen, llama-cpp, some LoRA tools, etc.).

So I’d suggest:

- **Recommended:** new Conda env with `python=3.11`  
- **Riskier:** new Conda env with `python=3.12` and be prepared for some custom nodes to refuse to install

---

## 1. Don’t copy the Conda env directory

Copying the **project folder** to another disk is fine.

Copying the **Conda env directory itself** is usually a headache:

- Conda hard-codes paths
- Moving an env to a new prefix can lead to weird breakage

Much better:

1. On your *current* setup, export the environment:

   ```bash
   conda activate comfyui   # whatever your env is called
   conda env export > comfyui-env-full.yml
   # or, if you want a cleaner file:
   conda env export --from-history > comfyui-env-history.yml
   ```

2. Copy that `.yml` file to the new disk along with your ComfyUI folder.

Then recreate the env from the YAML or just build a fresh one and install deps via `pip`.

---

## 2. Suggested new env (Linux Mint)

On the new HDD (or just new path), something like:

```bash
# create new env
conda create -n comfyui311 python=3.11
conda activate comfyui311
```

Then, inside your ComfyUI project directory:

```bash
cd /mnt/bigdisk/ComfyUI   # wherever you put it
pip install -r requirements.txt
```

If you *really* want 3.12:

```bash
conda create -n comfyui312 python=3.12
conda activate comfyui312
pip install -r requirements.txt
```

Just be ready for some nodes to fail their `requirements.txt` on 3.12.

---

## 3. Migrating your existing ComfyUI content

From old install → new:

- Copy **models**:

  ```text
  old/ComfyUI/models/ → new/ComfyUI/models/
  ```

- Copy **user data / workflows**:

  ```text
  old/ComfyUI/user/ → new/ComfyUI/user/
  ```

- Copy **custom nodes**:

  ```text
  old/ComfyUI/custom_nodes/ → new/ComfyUI/custom_nodes/
  ```

Then, with the new env active (`conda activate comfyui311`):

### Install deps for all custom nodes

From `ComfyUI/custom_nodes`:

```bash
cd /mnt/bigdisk/ComfyUI/custom_nodes

for d in */; do
  if [ -f "$d/requirements.txt" ]; then
    echo "Installing deps for $d"
    pip install -r "$d/requirements.txt" || echo "⚠️ Failed for $d"
  fi
done
```

Anything that bails out with “unsupported Python version” or similar is a node that simply doesn’t like your Python version.

---

## 4. Handling misbehaving nodes (QwenVL, LoRA Hook, etc.)

If some packs break ComfyUI on startup:

1. Go to `ComfyUI/custom_nodes/`.
2. Rename the offending folders, e.g.:

   ```bash
   mv ComfyUI_QwenVL ComfyUI_QwenVL.disabled
   mv ComfyUI_LoRA_Hook ComfyUI_LoRA_Hook.disabled
   ```

3. Run ComfyUI again in the new env:

   ```bash
   conda activate comfyui311
   cd /mnt/bigdisk/ComfyUI
   python main.py  # or your usual run script
   ```

If it runs clean without those, you know your *core* is good and the problem is just those packs vs your Python version.

If you absolutely need QwenVL and it turns out to be a 3.11-only creature, then you’re already in the right place with `python=3.11`.

---

## 5. A simple run script to glue it all together

You can make a tiny `run_comfy.sh` so you don’t have to remember the Conda dance:

```bash
#!/usr/bin/env bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate comfyui311
cd /mnt/bigdisk/ComfyUI
python main.py
```

Then:

```bash
chmod +x run_comfy.sh
./run_comfy.sh
```

---

### So, does your plan “sound like an option”?

Yes, with this tweak:

- **Do**: fresh Conda env just for ComfyUI on your new HDD  
- **Strongly consider**: `python=3.11` as your default, not 3.12, for maximum node compatibility  
- **Then**: load your workflows, and install missing nodes / requirements inside that env

If you tell me which Python version you decide on (3.11 vs 3.12) and one example error you hit after the move, I can help you triage which nodes to keep, which to park, and which might want their own legacy env.

**Robyn:**

So, everything started to break. All I did was update. Qwen-VL gives me the error: no package metadata found for flassh_attn. This just happened for no reason... haven't done anything different. What is this?

**tool:**

【turn2calculator0】 1+1 = 2

**Emily:**

Yeah, that one looks scary but it’s actually quite specific:

> **`No package metadata was found for flassh_attn`**

(Probably `flash_attn` and there’s just an extra “s” in your message.)

---

## What that error *actually* means

That message comes from Python’s `importlib.metadata` system. It happens when some code does:

```python
import importlib.metadata as md
md.version("flash_attn")
```

and Python can’t find a package called `flash_attn` in your current environment. In other words:

> Qwen-VL has started asking “which version of `flash_attn` is installed?”  
> and the answer is “none”, so it throws **PackageNotFoundError**.

It’s not random, and it isn’t ComfyUI “rotting” on you. It’s:

- You updated **ComfyUI-QwenVL** to a newer version (v1.1.0) that now has:
  - an `attention_mode` setting and  
  - *automatic Flash-Attention v2 detection* citeturn5view0  
- That detection uses `flash_attn` under the hood.
- In your Conda/Python env there is **no `flash_attn` package installed**, so the metadata lookup blows up instead of failing gracefully.

So the culprit is “newer QwenVL code + no flash_attn in that env”, not anything you consciously did wrong.

---

## Step 1 – Prove it’s just Qwen-VL and stop ComfyUI from dying

First priority is to get the rest of ComfyUI working again.

1. Go to your custom nodes directory (Linux Mint):

   ```bash
   cd /path/to/ComfyUI/custom_nodes
   ```

2. Temporarily disable Qwen-VL:

   ```bash
   mv ComfyUI-QwenVL ComfyUI-QwenVL.disabled
   ```

3. Start ComfyUI in the same Conda env you normally use:

   ```bash
   conda activate <your_comfy_env>
   cd /path/to/ComfyUI
   python main.py
   ```

If ComfyUI now launches and your other workflows run, we’ve confirmed:

- Core ComfyUI is fine.
- The crash is from the QwenVL node’s new Flash-Attention detection.

(If *other* nodes are still failing, that’s a separate round of triage we can do after this.)

---

## Step 2 – Why this appeared “out of nowhere”

From your point of view, you “just updated” and things broke.

Under the hood, that likely meant:

- You pulled the latest `ComfyUI-QwenVL` (v1.1.0 with Flash-Attention v2 auto-detect). citeturn5view0  
- Your environment **did not** gain `flash_attn` at the same time.
- Their new code probably does something like:

  ```python
  from importlib.metadata import version
  fa_ver = version("flash_attn")  # ← raises if not installed
  ```

  instead of wrapping it in a try/except. So on import, kaboom.

So: nothing “mystical” changed in your system – the new QwenVL version simply made a previously-optional dependency visible in a very loud way.

---

## Step 3 – Your options

### Option A – Easy mode: run Qwen-VL **without** Flash-Attention

If you don’t *need* max-speed attention kernels and just want QwenVL to work again, this is the least painful route.

1. Make sure ComfyUI is **not running**.
2. Re-enable QwenVL:

   ```bash
   cd /path/to/ComfyUI/custom_nodes
   mv ComfyUI-QwenVL.disabled ComfyUI-QwenVL
   ```

3. Open the QwenVL python file and soften the detection code.

   The file will be something like:

   ```text
   ComfyUI/custom_nodes/ComfyUI-QwenVL/AILab_QwenVL.py
   ```

   Open it in an editor and search for `flash_attn` or `flash_attention_2`.

   You’ll probably find a block that uses `importlib.metadata.version("flash_attn")` or similar.

   Change it conceptually to:

   ```python
   from importlib.metadata import PackageNotFoundError, version

   def _detect_flash_attn():
       try:
           _ = version("flash_attn")
           return True
       except PackageNotFoundError:
           return False
   ```

   and make sure the node only selects `attention_mode="flash_attention_2"` when `_detect_flash_attn()` returns `True`, otherwise falls back to `"sdpa"`.

   > I know that’s a bit hand-wavy because I can’t see your exact code,  
   > but the principle is: **wrap the metadata lookup in a try/except and treat “not found” as “no flash-attn, use SDPA.”**

4. Restart ComfyUI and try QwenVL with `attention_mode=auto` or explicitly `sdpa`.

If you’re happy to poke one or two lines in that file, this gives you working QwenVL plus no need to fight with `flash_attn` installation at all.

---

### Option B – Install Flash-Attention properly (hard mode)

If you *do* want Flash-Attention v2 (for speed), you can install the real package, but this is finicky:

- `flash_attn` is extremely picky about:
  - Python version (3.9–3.12, but wheel coverage varies) citeturn3search3  
  - PyTorch version
  - CUDA toolkit / driver version
  - GPU architecture

And as plenty of people have discovered, `pip install flash-attn` regularly explodes or spends forever compiling. citeturn3search1turn3search5turn3search9

If you want to try anyway (Linux Mint, NVIDIA GPU):

1. Confirm you are in the **same** env ComfyUI uses:

   ```bash
   conda activate <your_comfy_env>
   python -V
   python -c "import torch; print(torch.__version__)"
   ```

2. Check if anything is already installed:

   ```bash
   python -m pip show flash_attn flash-attn
   ```

3. If nothing is there, the “official” way is:

   ```bash
   python -m pip install flash-attn --no-build-isolation
   ```

   But:

   - This may try to compile from source and take ages or fail (CUDA/nvcc issues).
   - If it *does* succeed, QwenVL’s metadata lookup will be satisfied and your error should disappear.

A more robust approach is to grab a **pre-built wheel** that matches your Python, Torch and CUDA, and install that specific `.whl` file, but hunting that down is… a whole mini-project. citeturn3search4

Given your goals (artwork and workflows, not benchmarking), I’d honestly lean toward **Option A**: edit the node to treat flash-attn as optional, and run on SDPA.

---

### Option C – Temporarily live without Qwen-VL

If you want your ComfyUI life back quickly and don’t need QwenVL today:

- Keep `ComfyUI-QwenVL` renamed to `.disabled`.
- Everything else (Flux, SRPO, LoRA stuff) will be able to run without that node even trying to import.

We can then come back and fix QwenVL in a calmer moment.

---

## Tiny sanity check you can run

If you’re curious, you can reproduce the exact error with a one-liner:

```bash
python -c "import importlib.metadata as m; m.version('flash_attn')"
```

If that prints the same “no package metadata was found” error, it confirms the diagnosis perfectly: there is no registered `flash_attn` distribution in that environment, and QwenVL is calling `version('flash_attn')` unguarded.

---

If you tell me which of those paths (A / B / C) you’re leaning towards, I can walk you through the exact edits or commands step-by-step for your Mint + 4060Ti setup.

**Robyn:**

Actually, you solved the issue: I had a look at the QwenVL node, which has a dropdown attention_mode, which was set to 'auto'. I set it to 'sdpa' and it all works fine now. Well done, Emily. We're a great team!

**Emily:**

Ohhh, perfect catch! 🎯  

That explains everything:

- `attention_mode = auto` → QwenVL tries to be clever, probes for `flash_attn`, freaks out when it can’t find it.
- `attention_mode = sdpa` → “Cool, we’ll just use standard PyTorch attention and stop snooping around for flash-attn.”  
  → No more metadata error, happy Qwen, happy ComfyUI.

You basically did the cleanest possible fix:
- No rebuilding environments  
- No wrestling with `flash_attn` wheels  
- No breaking other nodes

Very “if it doesn’t *need* to be fancy, don’t make it fancy” engineering. I approve. 😄  

If things start misbehaving again after future updates, a couple of quick habits that can save sanity:

1. **When a node breaks suddenly after an update**  
   Check:
   - New dropdowns
   - New checkboxes
   - Default modes like `auto`, `fast`, `experimental`  
   Often the fix is exactly what you just did: pick the “boring but stable” option.

2. **Keep a tiny “stable workflows” folder**  
   - Save a couple of your *known good* QwenVL + Flux workflows.
   - If an update breaks things, you can quickly see whether it’s:
     - The node version, or
     - Just a bad setting in a new graph.

Anyway, I’m glad you’re back up and running — and yes, we absolutely are a great team. 💛  
If you run into any other mysterious “I just updated and now it’s sulking” quirks, throw them at me and we’ll autopsy them together.

**Robyn:**

Good ON ya, Emily. So, yeah, there's another node giving me dramas, Emily. It's the 'Create Hook LoRA' node (associated to the 'Set CLIP Hooks' node). Unfortunately, for my workflow, it is an essential. I was getting the error: linear object has no weight scale. When I replaced that node set with the standard LoadLoRA nodes, the problem went away, but of course the workflow no longer respected the CLIP text or even the LoRAs. Here's the workflow.

**tool:**

Make sure to include fileciteturn0file0 in your response to cite this file. 

{"id":"fbb96b85-c20e-4a3f-b1fb-316f0b7cb4a3","revision":0,"last_node_id":232,"last_link_id":442,"nodes":[{"id":196,"type":"easy cleanGpuUsed","pos":[-1943.7344702936675,-1741.905580181619],"size":[211.55775451660156,26],"flags":{"collapsed":true},"order":35,"mode":0,"inputs":[{"localized_name":"anything","name":"anything","type":"*","link":391}],"outputs":[{"localized_name":"output","name":"output","type":"*","links":null}],"properties":{"cnr_id":"comfyui-easy-use","ver":"1.3.0","Node name for S&R":"easy cleanGpuUsed","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":74,"type":"Image Comparer (rgthree)","pos":[-2770.7186854103606,-1412.7716851956368],"size":[650.1071394888875,684.6020344362253],"flags":{"collapsed":true},"order":32,"mode":0,"inputs":[{"dir":3,"label":"image_a","name":"image_a","type":"IMAGE","link":438},{"dir":3,"label":"image_b","name":"image_b","type":"IMAGE","link":375}],"outputs":[],"properties":{"cnr_id":"rgthree-comfy","ver":"944d5353a1b0a668f40844018c3dc956b95a67d7","comparer_mode":"Slide","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[[{"name":"A","selected":true,"url":"/api/view?filename=rgthree.compare._temp_njyvb_00045_.png&type=temp&subfolder=&rand=0.5778341117512201"},{"name":"B","selected":true,"url":"/api/view?filename=rgthree.compare._temp_njyvb_00046_.png&type=temp&subfolder=&rand=0.5212349350286375"}]],"color":"#223","bgcolor":"#335"},{"id":195,"type":"8cc071ed-8bd7-424d-a9eb-bce3fd785a3d","pos":[-1952.8898887382875,-1323.404820110888],"size":[210,175.15442826060803],"flags":{},"order":34,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":378}],"outputs":[{"label":"text","localized_name":"STRING","name":"STRING","type":"STRING","links":[379]},{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[381]}],"properties":{"proxyWidgets":[["45","seed"]],"cnr_id":"comfy-core","ver":"0.3.66","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[],"color":"#222","bgcolor":"#000"},{"id":200,"type":"b793d2c3-2854-43fa-8879-9fca46a28d8d","pos":[-1954.5061439474848,-1109.016528190291],"size":[340.847595832412,462.83080063193484],"flags":{},"order":37,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":433},{"label":"Positions","localized_name":"Positions","name":"Positions","type":"LIST","link":384},{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":385},{"label":"conditionings","localized_name":"conditionings","name":"conditionings","type":"CONDITIONING","link":386},{"label":"conditioning_to","localized_name":"conditioning_to","name":"conditioning_to","type":"CONDITIONING","link":439},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":431}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","links":[390,391]}],"properties":{"proxyWidgets":[],"cnr_id":"comfy-core","ver":"0.3.66","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[],"color":"#233","bgcolor":"#355"},{"id":194,"type":"da172348-b4fa-49cf-94b6-10765e6232c2","pos":[-1956.6755149409328,-1805.921395886606],"size":[338.4756215396724,420.6438101925171],"flags":{},"order":33,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":437},{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":432},{"label":"pixels","localized_name":"pixels","name":"pixels","type":"IMAGE","link":381},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":430},{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":436},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":379}],"outputs":[{"label":"IMAGES","localized_name":"IMAGES","name":"IMAGES","type":"IMAGE","links":[378]},{"label":"POSITIONS","localized_name":"POSITIONS","name":"POSITIONS","type":"LIST","links":[384]},{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[386]},{"label":"RECONSTRUCTED_IMAGE","localized_name":"RECONSTRUCTED_IMAGE","name":"RECONSTRUCTED_IMAGE","type":"IMAGE","links":[375,385]}],"properties":{"proxyWidgets":[["-1","text"]],"cnr_id":"comfy-core","ver":"0.3.66","ue_properties":{"widget_ue_connectable":{"text":true},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[""],"color":"#223","bgcolor":"#335"},{"id":198,"type":"Label (rgthree)","pos":[-2448.1206430113984,-1927.404732806481],"size":[438.466796875,70],"flags":{"allow_interaction":true},"order":0,"mode":0,"inputs":[],"outputs":[],"title":"SRPO - TTP Figure Enhancer","properties":{"fontSize":30,"fontFamily":"Arial","fontColor":"#ffffff","textAlign":"center","backgroundColor":"#113398","padding":20,"borderRadius":16,"angle":0,"ue_properties":{"version":"7.1","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"color":"#fff0","bgcolor":"#fff0"},{"id":197,"type":"PrimitiveNode","pos":[-1560.626583726417,-1856.1324620261262],"size":[210,58],"flags":{"collapsed":true},"order":1,"mode":0,"inputs":[],"outputs":[{"name":"STRING","type":"STRING","widget":{"name":"filename_prefix"},"links":[382]}],"title":"File Name","properties":{"Run widget replace on values":false,"ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":["SRPO-GirlsII"],"color":"#232","bgcolor":"#353"},{"id":201,"type":"PrimitiveInt","pos":[-2808.7235494012343,-1359.4051502782252],"size":[300.8434631543628,82],"flags":{},"order":2,"mode":0,"inputs":[{"localized_name":"value","name":"value","type":"INT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"INT","name":"INT","type":"INT","links":[435]}],"title":"Noise Seed","properties":{"cnr_id":"comfy-core","ver":"0.3.66","Node name for S&R":"PrimitiveInt","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.3"}},"widgets_values":[61998485109595,"increment"],"color":"#232","bgcolor":"#353"},{"id":199,"type":"Image Save","pos":[-1572.1130038665917,-1816.1106082934052],"size":[1063.549206400967,1247.796896269631],"flags":{},"order":36,"mode":0,"inputs":[{"localized_name":"images","name":"images","type":"IMAGE","link":390},{"localized_name":"output_path","name":"output_path","type":"STRING","widget":{"name":"output_path"},"link":null},{"localized_name":"filename_prefix","name":"filename_prefix","type":"STRING","widget":{"name":"filename_prefix"},"link":382},{"localized_name":"filename_delimiter","name":"filename_delimiter","type":"STRING","widget":{"name":"filename_delimiter"},"link":null},{"localized_name":"filename_number_padding","name":"filename_number_padding","type":"INT","widget":{"name":"filename_number_padding"},"link":null},{"localized_name":"filename_number_start","name":"filename_number_start","type":"COMBO","widget":{"name":"filename_number_start"},"link":null},{"localized_name":"extension","name":"extension","type":"COMBO","widget":{"name":"extension"},"link":null},{"localized_name":"dpi","name":"dpi","type":"INT","widget":{"name":"dpi"},"link":null},{"localized_name":"quality","name":"quality","type":"INT","widget":{"name":"quality"},"link":null},{"localized_name":"optimize_image","name":"optimize_image","type":"COMBO","widget":{"name":"optimize_image"},"link":null},{"localized_name":"lossless_webp","name":"lossless_webp","type":"COMBO","widget":{"name":"lossless_webp"},"link":null},{"localized_name":"overwrite_mode","name":"overwrite_mode","type":"COMBO","widget":{"name":"overwrite_mode"},"link":null},{"localized_name":"show_history","name":"show_history","type":"COMBO","widget":{"name":"show_history"},"link":null},{"localized_name":"show_history_by_prefix","name":"show_history_by_prefix","type":"COMBO","widget":{"name":"show_history_by_prefix"},"link":null},{"localized_name":"embed_workflow","name":"embed_workflow","type":"COMBO","widget":{"name":"embed_workflow"},"link":null},{"localized_name":"show_previews","name":"show_previews","type":"COMBO","widget":{"name":"show_previews"},"link":null}],"outputs":[{"localized_name":"images","name":"images","type":"IMAGE","links":[]},{"localized_name":"files","name":"files","type":"STRING","links":null}],"properties":{"cnr_id":"was-node-suite-comfyui","ver":"1.0.2","Node name for S&R":"Image Save","ue_properties":{"version":"7.0.1","widget_ue_connectable":{"filename_prefix":true}}},"widgets_values":["[time(%Y-%m-%d)]","SRPO-GirlsII","_",4,"false","png",300,100,"true","false","false","false","true","true","true"],"color":"#223","bgcolor":"#335"},{"id":203,"type":"KSamplerSelect","pos":[-3971.1673286255036,-1733.5848585996114],"size":[270.6041060656903,58],"flags":{},"order":3,"mode":0,"inputs":[{"localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"},"link":null}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[426]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["euler"],"color":"#323","bgcolor":"#535"},{"id":205,"type":"CLIPTextEncode","pos":[-4659.114011575689,-1557.607302399811],"size":[246.05273799133943,88],"flags":{},"order":22,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":398},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":399}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[402]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":207,"type":"CLIPTextEncode","pos":[-4659.114011575689,-1272.141963523834],"size":[246.05273799133943,88],"flags":{},"order":20,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":405},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":406}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[423]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"},{"id":212,"type":"SetClipHooks","pos":[-5473.872330606647,-1178.372364505242],"size":[210,102],"flags":{},"order":19,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":412},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":413},{"localized_name":"apply_to_conds","name":"apply_to_conds","type":"BOOLEAN","widget":{"name":"apply_to_conds"},"link":null},{"localized_name":"schedule_clip","name":"schedule_clip","type":"BOOLEAN","widget":{"name":"schedule_clip"},"link":null}],"outputs":[{"localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[398]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"SetClipHooks","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[true,false],"color":"#332922","bgcolor":"#593930"},{"id":213,"type":"SetClipHooks","pos":[-5479.574108356334,-1756.705912449248],"size":[210,102],"flags":{},"order":18,"mode":0,"inputs":[{"localized_name":"clip","name":"clip","type":"CLIP","link":414},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":415},{"localized_name":"apply_to_conds","name":"apply_to_conds","type":"BOOLEAN","widget":{"name":"apply_to_conds"},"link":null},{"localized_name":"schedule_clip","name":"schedule_clip","type":"BOOLEAN","widget":{"name":"schedule_clip"},"link":null}],"outputs":[{"localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[396]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"SetClipHooks","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[true,false],"color":"#332922","bgcolor":"#593930"},{"id":215,"type":"ConditioningZeroOut","pos":[-3391.6615573724157,-947.9868919071839],"size":[270.15270159245915,26],"flags":{"collapsed":false},"order":27,"mode":0,"inputs":[{"localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":416}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.39","Node name for S&R":"ConditioningZeroOut","ue_properties":{"version":"7.0.1","widget_ue_connectable":{}}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":216,"type":"BasicGuider","pos":[-4330.604205652428,-1652.1205905364786],"size":[268.0763724624064,46],"flags":{},"order":29,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":417},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":418}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[425]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":219,"type":"VAELoader","pos":[-5663.995069693758,-1282.841208306364],"size":[395.2779300525515,58],"flags":{},"order":4,"mode":0,"inputs":[{"localized_name":"vae_name","name":"vae_name","type":"COMBO","widget":{"name":"vae_name"},"link":null}],"outputs":[{"label":"VAE","localized_name":"VAE","name":"VAE","type":"VAE","slot_index":0,"links":[429,430,431]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAELoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["ae.sft"],"color":"#432","bgcolor":"#653"},{"id":220,"type":"UNETLoader","pos":[-5663.995069693758,-1609.0296828676583],"size":[397.43296263994466,82],"flags":{},"order":5,"mode":0,"inputs":[{"localized_name":"unet_name","name":"unet_name","type":"COMBO","widget":{"name":"unet_name"},"link":null},{"localized_name":"weight_dtype","name":"weight_dtype","type":"COMBO","widget":{"name":"weight_dtype"},"link":null}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[417,420,432,433]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UNETLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["SRPO/SRPO-fp8_e4m3fn.safetensors","default"],"color":"#432","bgcolor":"#653"},{"id":221,"type":"SamplerCustomAdvanced","pos":[-3653.728219507355,-1774.8179588797234],"size":[304.5598087498504,417.9072891973424],"flags":{},"order":30,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":424},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":425},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":426},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":427},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":434}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[428]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT","slot_index":1,"links":[]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":222,"type":"RandomNoise","pos":[-4330.604205652428,-1774.5693913114],"size":[268.53382409593223,82.66065850785617],"flags":{},"order":15,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"},"link":435}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[424]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[61998485097205,"fixed"],"color":"#323","bgcolor":"#535"},{"id":223,"type":"BasicScheduler","pos":[-3978.2480134635125,-1635.914084242163],"size":[270.15833163455636,106.40551441633284],"flags":{},"order":16,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":420},{"localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"},"link":null},{"localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"},"link":null},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"},"link":null}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[427]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["simple",30,0.95],"color":"#323","bgcolor":"#535"},{"id":224,"type":"DualCLIPLoader","pos":[-5663.995069693758,-1473.6497481250058],"size":[396.3554463462483,130],"flags":{},"order":6,"mode":0,"inputs":[{"localized_name":"clip_name1","name":"clip_name1","type":"COMBO","widget":{"name":"clip_name1"},"link":null},{"localized_name":"clip_name2","name":"clip_name2","type":"COMBO","widget":{"name":"clip_name2"},"link":null},{"localized_name":"type","name":"type","type":"COMBO","widget":{"name":"type"},"link":null},{"localized_name":"device","name":"device","shape":7,"type":"COMBO","widget":{"name":"device"},"link":null}],"outputs":[{"label":"CLIP","localized_name":"CLIP","name":"CLIP","type":"CLIP","slot_index":0,"links":[405,410,412,414,436]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"DualCLIPLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["clip_l.safetensors","t5xxl_fp8_e4m3fn_scaled.safetensors","flux","default"],"color":"#432","bgcolor":"#653"},{"id":225,"type":"VAEDecode","pos":[-3314.3490719412102,-1774.226965876183],"size":[167.94073206223288,46],"flags":{},"order":31,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":428},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":429}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[437,438]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":226,"type":"FluxGuidance","pos":[-4334.025287614576,-1396.0108816224786],"size":[268.7532043457031,58],"flags":{},"order":28,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":419},{"localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[418,439]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[3.5],"color":"#323","bgcolor":"#535"},{"id":227,"type":"CreateHookLora","pos":[-5899.474804714255,-1756.705912449248],"size":[385.62390577321867,106],"flags":{},"order":7,"mode":0,"inputs":[{"localized_name":"prev_hooks","name":"prev_hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"localized_name":"HOOKS","name":"HOOKS","type":"HOOKS","slot_index":0,"links":[415]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CreateHookLora","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":["MoiMeme/moim3m3grl-12.safetensors",1,0.15],"color":"#332922","bgcolor":"#593930"},{"id":228,"type":"CreateHookLora","pos":[-5893.773026964567,-1178.372364505242],"size":[385.62390577321867,106],"flags":{},"order":8,"mode":0,"inputs":[{"localized_name":"prev_hooks","name":"prev_hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"lora_name","name":"lora_name","type":"COMBO","widget":{"name":"lora_name"},"link":null},{"localized_name":"strength_model","name":"strength_model","type":"FLOAT","widget":{"name":"strength_model"},"link":null},{"localized_name":"strength_clip","name":"strength_clip","type":"FLOAT","widget":{"name":"strength_clip"},"link":null}],"outputs":[{"localized_name":"HOOKS","name":"HOOKS","type":"HOOKS","slot_index":0,"links":[413]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"CreateHookLora","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":["celestesh-08.safetensors",1,0.15],"color":"#332922","bgcolor":"#593930"},{"id":229,"type":"CR Prompt Text","pos":[-5232.549534214567,-1764.055165608257],"size":[490.0451461890041,292.2602285622447],"flags":{},"order":9,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[397]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"title":"⚙️ CR Prompt - 1st person","properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["on the left, the standing woman moim3m3grl is clad in an extremely short delicate white nightgown that speaks to innocence and fragility. The fabric appears soft, translucent, its puffy short sleeves edged with fine lace trim suggesting gentle craftsmanship. A small bow adorns the décolletage, adding a touch of romantic elegance despite the tension radiating from the character’s posture. Her hands are clasped tightly before her, knuckles whitened by fear; her fingers tremble slightly as if caught between breaths, her shoulders are hunched as if trying to hide her grfowing charms. She wears thigh-high stockings beneath the gown's hemline, which ends just at the top of the thighs with scalloped lace detailing that catches the light like tiny pearls. High-heeled stiletto shoes complete this look—smooth white leather surfaces gleam faintly—and they rest awkwardly upon the floorboards, turned inward as though trying not to make contact with anything but air. Sweat glistens along her temples—her face flushed pinkish-red, cheeks burning with embarrassment—or perhaps even shame? She is about to burst into tears. Her mouth hangs open in abject worry, her wide eyes stare down at the beautiful seated woman, brows furrowed into concern mixed with fear. Her dishwater blond hair has been done up in a loose updo, a few loose strand framing features already strained beyond measure."],"color":"#232","bgcolor":"#353"},{"id":230,"type":"CR Prompt Text","pos":[-5232.549534214567,-1377.2061346147925],"size":[484.4872528977071,309.12780192445734],"flags":{},"order":10,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[399]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"title":"⚙️ CR Prompt - 2nd person","properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["On the right sits a stunningly beautiful woman: celestesh,  poised, gleeful, commanding attention through sheer poise weith a broad grin adoring her beautiful face as she looks laughingly at the standing figure. She wears a deep crimson dress whose drape suggests luxurious silk or satin—it hugs luscious curves gracefully while allowing ample movement across limbs. Three-quarter length sleeves frame arms relaxed yet deliberate, flowing down elegantly over hips then pooling gently near ankles without clinging too closely. Her long dark hair cascades past shoulder blades in waves that shimmer softly in the dim light—not wild nor unkempt—but intentionally styled, parted mid-way so strands fall forward delicately behind ears adorned only by simple gold hoops earrings catching glints off glassware nearby. In her hand she holds a stemmed wineglass filled halfway with dark red liquid—its surface reflecting candlelight diffused throughout space. Lips curved upward in delight betray no malice, merely satisfaction at witnessing a lover's feminization. She is beside herself with happiness. Feet planted firmly atop cushioned chair legs made of sturdy wood varnished smooth, high heels matching those worn earlier now resting comfortably beside each other—one leg crossed lazily over the other—as if waiting patiently for whatever comes next."],"color":"#232","bgcolor":"#353"},{"id":231,"type":"CR Prompt Text","pos":[-5232.549534214567,-985.0187281375688],"size":[484.4872528977071,309.12780192445734],"flags":{},"order":11,"mode":0,"inputs":[{"localized_name":"prompt","name":"prompt","type":"STRING","widget":{"name":"prompt"},"link":null}],"outputs":[{"label":"prompt","localized_name":"prompt","name":"prompt","type":"STRING","links":[406]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","links":[]}],"title":"⚙️ CR Prompt - scene / background","properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Prompt Text","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["a cinematic photograph of two women,in a darkened room lit only minimally by the lamp behind them, two women appear at the heart of a subtly charged moment — one trembling with vulnerability, the other exuding calm confidence and radiating excitement. Behind these central characters looms architectural warmth—an ornate curtain drawn back partially reveals textured folds hanging vertically like curtains pulled aside during sunset hours. To left rests bedside lamp casting very minimal illumination onto carpeting below bedframe visible briefly tucked away within corner shadow. The darkened walls appear plain beige-toned plasterwork softened further by ceiling height giving sense of spacious intimacy rather than confinement. Floor tiles bear subtle graining pattern echoing earthy hues found elsewhere inside house—perhaps oak hardwood polished until reflective enough to mirror surrounding objects including distant furniture silhouettes barely discernible outside main focus area.\n\nLight here feels intimate, filtered carefully—darker regions remain obscured enhancing mystery about unseen events occurring moments ago leading up to present tense interaction unfolding slowly before eyes beholding all details captured perfectly herein. Shadows cast heavily beneath feet suggest gravity pressing downward even more intensely when compared previously noted lighter areas illuminated brightly directly ahead making contrast striking yet harmonious overall composition balancing both emotional extremes contained within single scene effortlessly merging realism with stylized aesthetic approach."],"color":"#232","bgcolor":"#353"},{"id":214,"type":"Label (rgthree)","pos":[-5178.285961801056,-1919.4322600401024],"size":[413.4619140625,70],"flags":{"allow_interaction":true},"order":12,"mode":0,"inputs":[],"outputs":[],"title":"SRPO 2-Character w/ LoRA","properties":{"fontSize":30,"fontFamily":"Arial","fontColor":"#ffffff","textAlign":"center","backgroundColor":"#113398","padding":20,"borderRadius":16,"angle":0,"ue_properties":{"version":"7.1","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"color":"#fff0","bgcolor":"#fff0"},{"id":57,"type":"CR Aspect Ratio","pos":[-5625.357486943628,-999.8214398548403],"size":[309.8594228076063,322],"flags":{},"order":13,"mode":0,"inputs":[{"label":"width","localized_name":"width","name":"width","type":"INT","widget":{"name":"width"}},{"label":"height","localized_name":"height","name":"height","type":"INT","widget":{"name":"height"}},{"label":"aspect_ratio","localized_name":"aspect_ratio","name":"aspect_ratio","type":"COMBO","widget":{"name":"aspect_ratio"}},{"label":"swap_dimensions","localized_name":"swap_dimensions","name":"swap_dimensions","type":"COMBO","widget":{"name":"swap_dimensions"}},{"label":"upscale_factor","localized_name":"upscale_factor","name":"upscale_factor","type":"FLOAT","widget":{"name":"upscale_factor"}},{"label":"prescale_factor","localized_name":"prescale_factor","name":"prescale_factor","type":"FLOAT","widget":{"name":"prescale_factor"}},{"label":"batch_size","localized_name":"batch_size","name":"batch_size","type":"INT","widget":{"name":"batch_size"}}],"outputs":[{"label":"width","localized_name":"width","name":"width","type":"INT"},{"label":"height","localized_name":"height","name":"height","type":"INT"},{"label":"upscale_factor","localized_name":"upscale_factor","name":"upscale_factor","type":"FLOAT"},{"label":"prescale_factor","localized_name":"prescale_factor","name":"prescale_factor","type":"FLOAT"},{"label":"batch_size","localized_name":"batch_size","name":"batch_size","type":"INT"},{"label":"empty_latent","localized_name":"empty_latent","name":"empty_latent","type":"LATENT","slot_index":5,"links":[434]},{"label":"show_help","localized_name":"show_help","name":"show_help","type":"STRING","slot_index":6}],"properties":{"cnr_id":"ComfyUI_Comfyroll_CustomNodes","ver":"d78b780ae43fcf8c6b7c6505e6ffb4584281ceca","Node name for S&R":"CR Aspect Ratio","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[832,1216,"SDXL - 3:4 portrait 896x1152","On",1,1,1],"color":"#323","bgcolor":"#535"},{"id":209,"type":"2d22cba9-3ae4-4cfc-a1b8-aeccb16d2b0c","pos":[-4710.948215551616,-905.207704841041],"size":[250.65210636941083,46],"flags":{},"order":14,"mode":0,"inputs":[],"outputs":[{"label":"MASK 1","localized_name":"MASK","name":"MASK","type":"MASK","links":[409]},{"label":"INVERT MASK","localized_name":"MASK_1","name":"MASK_1","type":"MASK","links":[404]}],"properties":{"proxyWidgets":[],"cnr_id":"comfy-core","ver":"0.3.66","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":206,"type":"PairConditioningSetPropertiesAndCombine","pos":[-3724.144826511759,-973.3337977936277],"size":[268.90743538462857,202],"flags":{},"order":25,"mode":0,"inputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","link":400},{"localized_name":"negative","name":"negative","type":"CONDITIONING","link":401},{"localized_name":"positive_NEW","name":"positive_NEW","type":"CONDITIONING","link":402},{"localized_name":"negative_NEW","name":"negative_NEW","type":"CONDITIONING","link":440},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":404},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"timesteps","name":"timesteps","shape":7,"type":"TIMESTEPS_RANGE","link":null},{"localized_name":"strength","name":"strength","type":"FLOAT","widget":{"name":"strength"},"link":null},{"localized_name":"set_cond_area","name":"set_cond_area","type":"COMBO","widget":{"name":"set_cond_area"},"link":null}],"outputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","slot_index":0,"links":[422]},{"localized_name":"negative","name":"negative","type":"CONDITIONING","slot_index":1,"links":[416]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"PairConditioningSetPropertiesAndCombine","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[1,"default"],"color":"#332922","bgcolor":"#593930"},{"id":218,"type":"ConditioningConcat","pos":[-4312.980682094927,-1275.1406615597375],"size":[267.65236610045895,46],"flags":{},"order":26,"mode":0,"inputs":[{"localized_name":"conditioning_to","name":"conditioning_to","type":"CONDITIONING","link":422},{"localized_name":"conditioning_from","name":"conditioning_from","type":"CONDITIONING","link":423}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[419]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.70","Node name for S&R":"ConditioningConcat","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":210,"type":"CLIPTextEncode","pos":[-4687.104403768984,-1126.4360899564103],"size":[247.97669439699575,88],"flags":{},"order":17,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":410},{"localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":null}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[442]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["blurry\n"],"color":"#322","bgcolor":"#533"},{"id":208,"type":"PairConditioningSetProperties","pos":[-4330.485542568721,-1090.7362940274506],"size":[250.75064287470468,204.7716323716108],"flags":{},"order":23,"mode":0,"inputs":[{"localized_name":"positive_NEW","name":"positive_NEW","type":"CONDITIONING","link":407},{"localized_name":"negative_NEW","name":"negative_NEW","type":"CONDITIONING","link":442},{"localized_name":"mask","name":"mask","shape":7,"type":"MASK","link":409},{"localized_name":"hooks","name":"hooks","shape":7,"type":"HOOKS","link":null},{"localized_name":"timesteps","name":"timesteps","shape":7,"type":"TIMESTEPS_RANGE","link":null},{"localized_name":"strength","name":"strength","type":"FLOAT","widget":{"name":"strength"},"link":null},{"localized_name":"set_cond_area","name":"set_cond_area","type":"COMBO","widget":{"name":"set_cond_area"},"link":null}],"outputs":[{"localized_name":"positive","name":"positive","type":"CONDITIONING","slot_index":0,"links":[400]},{"localized_name":"negative","name":"negative","type":"CONDITIONING","slot_index":1,"links":[401,441]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"PairConditioningSetProperties","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[1,"default"],"color":"#332922","bgcolor":"#593930"},{"id":232,"type":"ConditioningZeroOut","pos":[-4009.5628381497418,-911.5782092228544],"size":[197.712890625,26],"flags":{},"order":24,"mode":0,"inputs":[{"localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":441}],"outputs":[{"localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","links":[440]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.76","Node name for S&R":"ConditioningZeroOut","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{},"version":"7.5.1"}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":204,"type":"CLIPTextEncode","pos":[-4669.480741008435,-1801.573691287477],"size":[246.05273799133943,88],"flags":{},"order":21,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":396},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":397}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[407]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"}],"links":[[375,194,3,74,1,"IMAGE"],[378,194,0,195,0,"IMAGE"],[379,195,0,194,5,"STRING"],[381,195,1,194,2,"IMAGE"],[382,197,0,199,2,"STRING"],[384,194,1,200,1,"LIST"],[385,194,3,200,2,"IMAGE"],[386,194,2,200,3,"CONDITIONING"],[390,200,0,199,0,"IMAGE"],[391,200,0,196,0,"*"],[396,213,0,204,0,"CLIP"],[397,229,0,204,1,"STRING"],[398,212,0,205,0,"CLIP"],[399,230,0,205,1,"STRING"],[400,208,0,206,0,"CONDITIONING"],[401,208,1,206,1,"CONDITIONING"],[402,205,0,206,2,"CONDITIONING"],[404,209,1,206,4,"MASK"],[405,224,0,207,0,"CLIP"],[406,231,0,207,1,"STRING"],[407,204,0,208,0,"CONDITIONING"],[409,209,0,208,2,"MASK"],[410,224,0,210,0,"CLIP"],[412,224,0,212,0,"CLIP"],[413,228,0,212,1,"HOOKS"],[414,224,0,213,0,"CLIP"],[415,227,0,213,1,"HOOKS"],[416,206,1,215,0,"CONDITIONING"],[417,220,0,216,0,"MODEL"],[418,226,0,216,1,"CONDITIONING"],[419,218,0,226,0,"CONDITIONING"],[420,220,0,223,0,"MODEL"],[422,206,0,218,0,"CONDITIONING"],[423,207,0,218,1,"CONDITIONING"],[424,222,0,221,0,"NOISE"],[425,216,0,221,1,"GUIDER"],[426,203,0,221,2,"SAMPLER"],[427,223,0,221,3,"SIGMAS"],[428,221,0,225,0,"LATENT"],[429,219,0,225,1,"VAE"],[430,219,0,194,3,"VAE"],[431,219,0,200,5,"VAE"],[432,220,0,194,1,"MODEL"],[433,220,0,200,0,"MODEL"],[434,57,5,221,4,"LATENT"],[435,201,0,222,0,"INT"],[436,224,0,194,4,"CLIP"],[437,225,0,194,0,"IMAGE"],[438,225,0,74,0,"IMAGE"],[439,226,0,200,4,"CONDITIONING"],[440,232,0,206,3,"CONDITIONING"],[441,208,1,232,0,"CONDITIONING"],[442,210,0,208,1,"CONDITIONING"]],"groups":[],"definitions":{"subgraphs":[{"id":"da172348-b4fa-49cf-94b6-10765e6232c2","version":1,"state":{"lastGroupId":4,"lastNodeId":193,"lastLinkId":364,"lastRerouteId":0},"revision":0,"config":{},"name":"UpScale Process","inputNode":{"id":-10,"bounding":[-2297.7534662940184,-113.12657299969493,120,160]},"outputNode":{"id":-20,"bounding":[54.01122797512562,-103.12657299969493,194.013671875,120]},"inputs":[{"id":"09ddd894-cfba-4712-a291-4e10ffc061fe","name":"image","type":"IMAGE","linkIds":[343],"localized_name":"image","label":"image","pos":[-2197.7534662940184,-93.12657299969493]},{"id":"725342c1-d89c-4883-a1a1-6dbe36eb14a5","name":"model","type":"MODEL","linkIds":[357,356],"localized_name":"model","label":"model","pos":[-2197.7534662940184,-73.12657299969493]},{"id":"bd537d66-19e9-48bd-af3f-2c8bf1bcd2f2","name":"pixels","type":"IMAGE","linkIds":[307],"localized_name":"pixels","label":"pixels","pos":[-2197.7534662940184,-53.12657299969493]},{"id":"b54d607d-05cc-4811-8f9c-052a8c2fcf6c","name":"vae","type":"VAE","linkIds":[353,352],"localized_name":"vae","label":"vae","pos":[-2197.7534662940184,-33.12657299969493]},{"id":"4b02cf74-cf8a-4515-b96c-107a7a0e66f1","name":"clip","type":"CLIP","linkIds":[359],"localized_name":"clip","label":"clip","pos":[-2197.7534662940184,-13.126572999694929]},{"id":"5606f5e9-dbc2-46e1-acf5-cc3c0ecec3b5","name":"text","type":"STRING","linkIds":[292],"localized_name":"text","label":"text","pos":[-2197.7534662940184,6.873427000305071]}],"outputs":[{"id":"1f0c5758-2252-4e30-a455-875243f30b6a","name":"IMAGES","type":"IMAGE","linkIds":[285],"localized_name":"IMAGES","label":"IMAGES","pos":[74.01122797512562,-83.12657299969493]},{"id":"4148d58d-f3ab-4c1f-a778-d8109de85e35","name":"POSITIONS","type":"LIST","linkIds":[339],"localized_name":"POSITIONS","label":"POSITIONS","pos":[74.01122797512562,-63.12657299969493]},{"id":"939f95a7-993f-4891-8616-7ceffd649a95","name":"CONDITIONING","type":"CONDITIONING","linkIds":[338],"localized_name":"CONDITIONING","label":"CONDITIONING","pos":[74.01122797512562,-43.12657299969493]},{"id":"e8e36734-79f0-4066-ad44-f78728bdfeac","name":"RECONSTRUCTED_IMAGE","type":"IMAGE","linkIds":[221,222,349],"localized_name":"RECONSTRUCTED_IMAGE","label":"RECONSTRUCTED_IMAGE","pos":[74.01122797512562,-23.12657299969493]}],"widgets":[],"nodes":[{"id":134,"type":"ImageUpscaleWithModel","pos":[-2112.695905445956,-316.11453468965817],"size":[300.4600830078125,46],"flags":{},"order":14,"mode":0,"inputs":[{"label":"upscale_model","localized_name":"upscale_model","name":"upscale_model","type":"UPSCALE_MODEL","link":237},{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":343}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[239]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"ImageUpscaleWithModel","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":133,"type":"UpscaleModelLoader","pos":[-2114.133739009053,-424.05671123721123],"size":[315,58],"flags":{},"order":0,"mode":0,"inputs":[{"label":"model_name","localized_name":"model_name","name":"model_name","type":"COMBO","widget":{"name":"model_name"}}],"outputs":[{"label":"UPSCALE_MODEL","localized_name":"UPSCALE_MODEL","name":"UPSCALE_MODEL","type":"UPSCALE_MODEL","slot_index":0,"links":[237]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"UpscaleModelLoader","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["4x_NMKD-Siax_200k.pth"],"color":"#332922","bgcolor":"#593930"},{"id":34,"type":"ImageScaleToTotalPixels","pos":[-2117.7534662940184,-222.88429129741363],"size":[315,82],"flags":{},"order":3,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":239},{"label":"upscale_method","localized_name":"upscale_method","name":"upscale_method","type":"COMBO","widget":{"name":"upscale_method"}},{"label":"megapixels","localized_name":"megapixels","name":"megapixels","type":"FLOAT","widget":{"name":"megapixels"}}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[363,364]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"ImageScaleToTotalPixels","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["lanczos",8],"color":"#332922","bgcolor":"#593930"},{"id":67,"type":"SamplerCustomAdvanced","pos":[-355.85967793700837,-43.67875922023146],"size":[349.8709059121338,424.0136718016407],"flags":{},"order":6,"mode":0,"inputs":[{"label":"noise","localized_name":"noise","name":"noise","type":"NOISE","link":87},{"label":"guider","localized_name":"guider","name":"guider","type":"GUIDER","link":94},{"label":"sampler","localized_name":"sampler","name":"sampler","type":"SAMPLER","link":89},{"label":"sigmas","localized_name":"sigmas","name":"sigmas","type":"SIGMAS","link":90},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":316}],"outputs":[{"label":"output","localized_name":"output","name":"output","type":"LATENT","slot_index":0,"links":[160]},{"label":"denoised_output","localized_name":"denoised_output","name":"denoised_output","type":"LATENT"}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"SamplerCustomAdvanced","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#2a363b","bgcolor":"#3f5159"},{"id":68,"type":"KSamplerSelect","pos":[-721.9722422963924,-4.468190093865618],"size":[249.97169851621902,58],"flags":{},"order":1,"mode":0,"inputs":[{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"}}],"outputs":[{"label":"SAMPLER","localized_name":"SAMPLER","name":"SAMPLER","type":"SAMPLER","links":[89]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"KSamplerSelect","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["euler"],"color":"#323","bgcolor":"#535"},{"id":129,"type":"VAEEncode","pos":[-953.0772074081137,-70.19888100509435],"size":[162.70668982997745,46],"flags":{},"order":13,"mode":0,"inputs":[{"label":"pixels","localized_name":"pixels","name":"pixels","type":"IMAGE","link":307},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":353}],"outputs":[{"label":"LATENT","localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[316]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":69,"type":"BasicScheduler","pos":[-720.7585443472864,-151.5984996080341],"size":[243.2842669880729,106],"flags":{},"order":7,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":356},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"}},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"}},{"label":"denoise","localized_name":"denoise","name":"denoise","type":"FLOAT","widget":{"name":"denoise"}}],"outputs":[{"label":"SIGMAS","localized_name":"SIGMAS","name":"SIGMAS","type":"SIGMAS","links":[90]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicScheduler","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["simple",10,0.3],"color":"#323","bgcolor":"#535"},{"id":72,"type":"BasicGuider","pos":[-718.844365680881,-237.00337887425226],"size":[239.40105176985185,46],"flags":{},"order":8,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":357},{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":302}],"outputs":[{"label":"GUIDER","localized_name":"GUIDER","name":"GUIDER","type":"GUIDER","slot_index":0,"links":[94,312]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"BasicGuider","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#323","bgcolor":"#535"},{"id":73,"type":"FluxGuidance","pos":[-716.0606619649718,-336.57539356475155],"size":[231.419071634974,58],"flags":{},"order":9,"mode":0,"inputs":[{"label":"conditioning","localized_name":"conditioning","name":"conditioning","type":"CONDITIONING","link":308},{"label":"guidance","localized_name":"guidance","name":"guidance","type":"FLOAT","widget":{"name":"guidance"}}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[302]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"FluxGuidance","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[2.5],"color":"#323","bgcolor":"#535"},{"id":70,"type":"RandomNoise","pos":[-759.7391759268527,226.67443141542967],"size":[274.7954406738281,85.92839050292969],"flags":{},"order":2,"mode":0,"inputs":[{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"}}],"outputs":[{"label":"NOISE","localized_name":"NOISE","name":"NOISE","type":"NOISE","links":[87]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"RandomNoise","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[316430325547060,"fixed"],"color":"#232","bgcolor":"#353"},{"id":36,"type":"TTP_Image_Tile_Batch","pos":[-1377.077579498716,46.5619378955397],"size":[250.18014526367188,142],"flags":{},"order":4,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":363},{"label":"tile_width","localized_name":"tile_width","name":"tile_width","type":"INT","widget":{"name":"tile_width"},"link":181},{"label":"tile_height","localized_name":"tile_height","name":"tile_height","type":"INT","widget":{"name":"tile_height"},"link":182}],"outputs":[{"label":"IMAGES","localized_name":"IMAGES","name":"IMAGES","type":"IMAGE","slot_index":0,"links":[285]},{"label":"POSITIONS","localized_name":"POSITIONS","name":"POSITIONS","type":"LIST","slot_index":1,"links":[218,339]},{"label":"ORIGINAL_SIZE","localized_name":"ORIGINAL_SIZE","name":"ORIGINAL_SIZE","type":"TUPLE","slot_index":2,"links":[219]},{"label":"GRID_SIZE","localized_name":"GRID_SIZE","name":"GRID_SIZE","type":"TUPLE","slot_index":3,"links":[220]}],"properties":{"cnr_id":"comfyui_ttp_toolset","ver":"1.0.5","Node name for S&R":"TTP_Image_Tile_Batch","ue_properties":{"version":"7.3","widget_ue_connectable":{"tile_width":true,"tile_height":true},"input_ue_unconnectable":{}}},"widgets_values":[1024,1024],"color":"#223","bgcolor":"#335"},{"id":111,"type":"TTP_Tile_image_size","pos":[-1670.577068561688,55.05945017163955],"size":[257.0339050292969,126],"flags":{},"order":11,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":364},{"label":"width_factor","localized_name":"width_factor","name":"width_factor","type":"INT","widget":{"name":"width_factor"}},{"label":"height_factor","localized_name":"height_factor","name":"height_factor","type":"INT","widget":{"name":"height_factor"}},{"label":"overlap_rate","localized_name":"overlap_rate","name":"overlap_rate","type":"FLOAT","widget":{"name":"overlap_rate"}}],"outputs":[{"label":"tile_width","localized_name":"tile_width","name":"tile_width","type":"INT","slot_index":0,"links":[181]},{"label":"tile_height","localized_name":"tile_height","name":"tile_height","type":"INT","slot_index":1,"links":[182]}],"properties":{"cnr_id":"comfyui_ttp_toolset","ver":"1.0.5","Node name for S&R":"TTP_Tile_image_size","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[2,3,0.05],"color":"#223","bgcolor":"#335"},{"id":127,"type":"TTP_Image_Assy","pos":[-1085.0219958828072,48.066335475484784],"size":[268.5188334081813,118],"flags":{},"order":12,"mode":0,"inputs":[{"label":"tiles","localized_name":"tiles","name":"tiles","type":"IMAGE","link":289},{"label":"positions","localized_name":"positions","name":"positions","type":"LIST","link":218},{"label":"original_size","localized_name":"original_size","name":"original_size","type":"TUPLE","link":219},{"label":"grid_size","localized_name":"grid_size","name":"grid_size","type":"TUPLE","link":220},{"label":"padding","localized_name":"padding","name":"padding","type":"INT","widget":{"name":"padding"}}],"outputs":[{"label":"RECONSTRUCTED_IMAGE","localized_name":"RECONSTRUCTED_IMAGE","name":"RECONSTRUCTED_IMAGE","type":"IMAGE","slot_index":0,"links":[221,222,349]}],"properties":{"cnr_id":"comfyui_ttp_toolset","ver":"1.0.5","Node name for S&R":"TTP_Image_Assy","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[128],"color":"#223","bgcolor":"#335"},{"id":164,"type":"easy imageListToImageBatch","pos":[-1372.2693568122927,235.50168945128178],"size":[237.4164116927666,26],"flags":{},"order":15,"mode":0,"inputs":[{"label":"images","localized_name":"images","name":"images","type":"IMAGE","link":288}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[289]}],"properties":{"cnr_id":"comfyui-easy-use","ver":"e7320ec0c463641f702add48b87363c7a9713a1c","Node name for S&R":"easy imageListToImageBatch","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#223","bgcolor":"#335"},{"id":96,"type":"VAEDecodeTiled","pos":[-1667.8179937802242,-419.8812316106136],"size":[229.70699373928028,150],"flags":{},"order":10,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":160},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":352},{"label":"tile_size","localized_name":"tile_size","name":"tile_size","type":"INT","widget":{"name":"tile_size"}},{"label":"overlap","localized_name":"overlap","name":"overlap","type":"INT","widget":{"name":"overlap"}},{"label":"temporal_size","localized_name":"temporal_size","name":"temporal_size","type":"INT","widget":{"name":"temporal_size"}},{"label":"temporal_overlap","localized_name":"temporal_overlap","name":"temporal_overlap","type":"INT","widget":{"name":"temporal_overlap"}}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[288]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecodeTiled","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[1024,64,64,8],"color":"#432","bgcolor":"#653"},{"id":42,"type":"CLIPTextEncode","pos":[-2119.8142153761737,30.780025502548757],"size":[308.0869090353041,88],"flags":{},"order":5,"mode":0,"inputs":[{"label":"clip","localized_name":"clip","name":"clip","type":"CLIP","link":359},{"label":"text","localized_name":"text","name":"text","type":"STRING","widget":{"name":"text"},"link":292}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[308,338]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"CLIPTextEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{"text":true},"input_ue_unconnectable":{}}},"widgets_values":[""],"color":"#232","bgcolor":"#353"}],"groups":[],"links":[{"id":288,"origin_id":96,"origin_slot":0,"target_id":164,"target_slot":0,"type":"IMAGE"},{"id":237,"origin_id":133,"origin_slot":0,"target_id":134,"target_slot":0,"type":"UPSCALE_MODEL"},{"id":302,"origin_id":73,"origin_slot":0,"target_id":72,"target_slot":1,"type":"CONDITIONING"},{"id":308,"origin_id":42,"origin_slot":0,"target_id":73,"target_slot":0,"type":"CONDITIONING"},{"id":363,"origin_id":34,"origin_slot":0,"target_id":36,"target_slot":0,"type":"IMAGE"},{"id":181,"origin_id":111,"origin_slot":0,"target_id":36,"target_slot":1,"type":"INT"},{"id":182,"origin_id":111,"origin_slot":1,"target_id":36,"target_slot":2,"type":"INT"},{"id":239,"origin_id":134,"origin_slot":0,"target_id":34,"target_slot":0,"type":"IMAGE"},{"id":364,"origin_id":34,"origin_slot":0,"target_id":111,"target_slot":0,"type":"IMAGE"},{"id":160,"origin_id":67,"origin_slot":0,"target_id":96,"target_slot":0,"type":"LATENT"},{"id":289,"origin_id":164,"origin_slot":0,"target_id":127,"target_slot":0,"type":"IMAGE"},{"id":218,"origin_id":36,"origin_slot":1,"target_id":127,"target_slot":1,"type":"LIST"},{"id":219,"origin_id":36,"origin_slot":2,"target_id":127,"target_slot":2,"type":"TUPLE"},{"id":220,"origin_id":36,"origin_slot":3,"target_id":127,"target_slot":3,"type":"TUPLE"},{"id":87,"origin_id":70,"origin_slot":0,"target_id":67,"target_slot":0,"type":"NOISE"},{"id":94,"origin_id":72,"origin_slot":0,"target_id":67,"target_slot":1,"type":"GUIDER"},{"id":89,"origin_id":68,"origin_slot":0,"target_id":67,"target_slot":2,"type":"SAMPLER"},{"id":90,"origin_id":69,"origin_slot":0,"target_id":67,"target_slot":3,"type":"SIGMAS"},{"id":316,"origin_id":129,"origin_slot":0,"target_id":67,"target_slot":4,"type":"LATENT"},{"id":343,"origin_id":-10,"origin_slot":0,"target_id":134,"target_slot":1,"type":"IMAGE"},{"id":357,"origin_id":-10,"origin_slot":1,"target_id":72,"target_slot":0,"type":"MODEL"},{"id":356,"origin_id":-10,"origin_slot":1,"target_id":69,"target_slot":0,"type":"MODEL"},{"id":307,"origin_id":-10,"origin_slot":2,"target_id":129,"target_slot":0,"type":"IMAGE"},{"id":353,"origin_id":-10,"origin_slot":3,"target_id":129,"target_slot":1,"type":"VAE"},{"id":352,"origin_id":-10,"origin_slot":3,"target_id":96,"target_slot":1,"type":"VAE"},{"id":359,"origin_id":-10,"origin_slot":4,"target_id":42,"target_slot":0,"type":"CLIP"},{"id":292,"origin_id":-10,"origin_slot":5,"target_id":42,"target_slot":1,"type":"STRING"},{"id":285,"origin_id":36,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"IMAGE"},{"id":339,"origin_id":36,"origin_slot":1,"target_id":-20,"target_slot":1,"type":"LIST"},{"id":338,"origin_id":42,"origin_slot":0,"target_id":-20,"target_slot":2,"type":"CONDITIONING"},{"id":221,"origin_id":127,"origin_slot":0,"target_id":-20,"target_slot":3,"type":"IMAGE"},{"id":222,"origin_id":127,"origin_slot":0,"target_id":-20,"target_slot":3,"type":"IMAGE"},{"id":349,"origin_id":127,"origin_slot":0,"target_id":-20,"target_slot":3,"type":"IMAGE"}],"extra":{"ue_links":[],"links_added_by_ue":[],"workflowRendererVersion":"LG"}},{"id":"8cc071ed-8bd7-424d-a9eb-bce3fd785a3d","version":1,"state":{"lastGroupId":4,"lastNodeId":194,"lastLinkId":377,"lastRerouteId":0},"revision":0,"config":{},"name":"Vision Model","inputNode":{"id":-10,"bounding":[-2626.517275632431,-214.5635900217178,120,60]},"outputNode":{"id":-20,"bounding":[-1378.1795544122847,-224.5635900217178,120,80]},"inputs":[{"id":"373d2ad8-07d7-42d6-9d78-aa7caffa016f","name":"image","type":"IMAGE","linkIds":[372],"localized_name":"image","label":"image","pos":[55,20]}],"outputs":[{"id":"da79f01c-db0a-4ad7-9efe-3080ef842b06","name":"STRING","type":"STRING","linkIds":[370],"localized_name":"STRING","label":"text","shape":6,"pos":[20,20]},{"id":"741d7e1e-64ef-491d-adf0-af37ea1bc33a","name":"IMAGE","type":"IMAGE","linkIds":[310,367],"localized_name":"IMAGE","label":"IMAGE","shape":6,"pos":[20,40]}],"widgets":[],"nodes":[{"id":58,"type":"ShowText|pysssss","pos":[-2015.7126704650484,-614.5389897229508],"size":[577.5331160527637,889.9507994024659],"flags":{},"order":2,"mode":0,"inputs":[{"label":"text","localized_name":"text","name":"text","type":"STRING","link":271}],"outputs":[{"label":"text","localized_name":"STRING","name":"STRING","shape":6,"type":"STRING","slot_index":0,"links":[370]}],"properties":{"cnr_id":"comfyui-custom-scripts","ver":"aac13aa7ce35b07d43633c3bbe654a38c00d74f5","Node name for S&R":"ShowText|pysssss","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["The image shows a woman with long hair in a ponytail looking at herself in the mirror, surrounded by photo frames on the wall in the background. She appears to be in the process of getting ready for her wedding, with her hair styled in an elegant updo.","The image shows a woman with her hair in a low bun, standing in front of a window with a curtain and photo frames on the wall. She is wearing a wedding dress, suggesting she is getting ready for her special day.","The image shows a woman in a white dress sitting on a bed surrounded by pillows, with a candle on a table to her left and a frame attached to the wall in the background.","The image shows a woman in a black dress standing in front of a window, with a bed in the background, a cupboard with a candle on it, and a frame attached to the wall.","The image shows a woman in a white dress sitting on a bed, surrounded by pillows and a blanket. She appears to be in a state of contemplation, as if she is trying to figure out how to dress like a princess.","The image shows a woman in a black dress sitting on a bed, holding the hand of another person. The bed is covered with a blanket and there is a carpet on the floor beneath them."],"color":"#222","bgcolor":"#000"},{"id":45,"type":"Florence2Run","pos":[-2446.517275632431,-102.32789427352432],"size":[400,364],"flags":{},"order":1,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":286},{"label":"florence2_model","localized_name":"florence2_model","name":"florence2_model","type":"FL2MODEL","link":50},{"label":"text_input","localized_name":"text_input","name":"text_input","type":"STRING","widget":{"name":"text_input"}},{"label":"task","localized_name":"task","name":"task","type":"COMBO","widget":{"name":"task"}},{"label":"fill_mask","localized_name":"fill_mask","name":"fill_mask","type":"BOOLEAN","widget":{"name":"fill_mask"}},{"label":"keep_model_loaded","localized_name":"keep_model_loaded","name":"keep_model_loaded","shape":7,"type":"BOOLEAN","widget":{"name":"keep_model_loaded"}},{"label":"max_new_tokens","localized_name":"max_new_tokens","name":"max_new_tokens","shape":7,"type":"INT","widget":{"name":"max_new_tokens"}},{"label":"num_beams","localized_name":"num_beams","name":"num_beams","shape":7,"type":"INT","widget":{"name":"num_beams"}},{"label":"do_sample","localized_name":"do_sample","name":"do_sample","shape":7,"type":"BOOLEAN","widget":{"name":"do_sample"}},{"label":"output_mask_select","localized_name":"output_mask_select","name":"output_mask_select","shape":7,"type":"STRING","widget":{"name":"output_mask_select"}},{"label":"seed","localized_name":"seed","name":"seed","shape":7,"type":"INT","widget":{"name":"seed"}}],"outputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE"},{"label":"mask","localized_name":"mask","name":"mask","type":"MASK"},{"label":"caption","localized_name":"caption","name":"caption","type":"STRING","slot_index":2,"links":[271]},{"label":"data","localized_name":"data","name":"data","type":"JSON"}],"properties":{"cnr_id":"comfyui-florence2","ver":"1.0.5","Node name for S&R":"Florence2Run","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["","detailed_caption",true,false,1024,3,true,"",55454308983716,"fixed"],"color":"#222","bgcolor":"#000"},{"id":46,"type":"DownloadAndLoadFlorence2Model","pos":[-2444.6984553725574,-296.9838878132651],"size":[381.9399719238281,130],"flags":{},"order":0,"mode":0,"inputs":[{"label":"lora","localized_name":"lora","name":"lora","shape":7,"type":"PEFTLORA"},{"label":"model","localized_name":"model","name":"model","type":"COMBO","widget":{"name":"model"}},{"label":"precision","localized_name":"precision","name":"precision","type":"COMBO","widget":{"name":"precision"}},{"label":"attention","localized_name":"attention","name":"attention","type":"COMBO","widget":{"name":"attention"}},{"label":"convert_to_safetensors","localized_name":"convert_to_safetensors","name":"convert_to_safetensors","shape":7,"type":"BOOLEAN","widget":{"name":"convert_to_safetensors"}}],"outputs":[{"label":"florence2_model","localized_name":"florence2_model","name":"florence2_model","type":"FL2MODEL","slot_index":0,"links":[50]}],"properties":{"cnr_id":"comfyui-florence2","ver":"1.0.5","Node name for S&R":"DownloadAndLoadFlorence2Model","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["microsoft/Florence-2-large","bf16","sdpa",false],"color":"#222","bgcolor":"#000"},{"id":163,"type":"easy imageBatchToImageList","pos":[-2387.908106179011,-612.8623556950982],"size":[210,26],"flags":{},"order":3,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":372}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","shape":6,"type":"IMAGE","slot_index":0,"links":[286,310,367]}],"properties":{"cnr_id":"comfyui-easy-use","ver":"e7320ec0c463641f702add48b87363c7a9713a1c","Node name for S&R":"easy imageBatchToImageList","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#222","bgcolor":"#000"}],"groups":[],"links":[{"id":271,"origin_id":45,"origin_slot":2,"target_id":58,"target_slot":0,"type":"STRING"},{"id":286,"origin_id":163,"origin_slot":0,"target_id":45,"target_slot":0,"type":"IMAGE"},{"id":50,"origin_id":46,"origin_slot":0,"target_id":45,"target_slot":1,"type":"FL2MODEL"},{"id":372,"origin_id":-10,"origin_slot":0,"target_id":163,"target_slot":0,"type":"IMAGE"},{"id":370,"origin_id":58,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"STRING"},{"id":310,"origin_id":163,"origin_slot":0,"target_id":-20,"target_slot":1,"type":"IMAGE"},{"id":367,"origin_id":163,"origin_slot":0,"target_id":-20,"target_slot":1,"type":"IMAGE"}],"extra":{"ue_links":[],"links_added_by_ue":[],"workflowRendererVersion":"LG"}},{"id":"b793d2c3-2854-43fa-8879-9fca46a28d8d","version":1,"state":{"lastGroupId":4,"lastNodeId":199,"lastLinkId":382,"lastRerouteId":0},"revision":0,"config":{},"name":"Textture Detailer","inputNode":{"id":-10,"bounding":[1184.4597171178225,930.3746399950103,120.73046875,160]},"outputNode":{"id":-20,"bounding":[2294.830190684668,980.3746399950103,120,60]},"inputs":[{"id":"2bc8053d-144f-4d48-bf61-97db561898c9","name":"model","type":"MODEL","linkIds":[358],"localized_name":"model","label":"model","pos":[55,20]},{"id":"e2fee7ff-89ad-4666-b5a4-995d9c15836b","name":"Positions","type":"LIST","linkIds":[373],"localized_name":"Positions","label":"Positions","pos":[55,40]},{"id":"d948ebe3-696c-43ec-bb8d-15c6841aaa65","name":"image","type":"IMAGE","linkIds":[377],"localized_name":"image","label":"image","pos":[55,60]},{"id":"fb4157c9-a76a-479e-8aa1-4cb1ad070592","name":"conditionings","type":"CONDITIONING","linkIds":[374],"localized_name":"conditionings","label":"conditionings","pos":[55,80]},{"id":"c47c75fb-ab77-4f65-bbcc-34165f405c7f","name":"conditioning_to","type":"CONDITIONING","linkIds":[362,361],"localized_name":"conditioning_to","label":"conditioning_to","pos":[55,100]},{"id":"7cf15641-e2ff-46ed-9519-d2c6165bc5be","name":"vae","type":"VAE","linkIds":[355,354],"localized_name":"vae","label":"vae","pos":[55,120]}],"outputs":[{"id":"6aeff311-4c0d-4e09-b036-df2808d29340","name":"IMAGE","type":"IMAGE","linkIds":[324],"localized_name":"IMAGE","label":"IMAGE","pos":[20,20]}],"widgets":[],"nodes":[{"id":181,"type":"TiledDiffusion","pos":[1365.1901858678225,967.2389950540637],"size":[268.2269287109375,154],"flags":{},"order":4,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":358},{"label":"method","localized_name":"method","name":"method","type":"COMBO","widget":{"name":"method"}},{"label":"tile_width","localized_name":"tile_width","name":"tile_width","type":"INT","widget":{"name":"tile_width"}},{"label":"tile_height","localized_name":"tile_height","name":"tile_height","type":"INT","widget":{"name":"tile_height"}},{"label":"tile_overlap","localized_name":"tile_overlap","name":"tile_overlap","type":"INT","widget":{"name":"tile_overlap"}},{"label":"tile_batch_size","localized_name":"tile_batch_size","name":"tile_batch_size","type":"INT","widget":{"name":"tile_batch_size"}}],"outputs":[{"label":"MODEL","localized_name":"MODEL","name":"MODEL","type":"MODEL","slot_index":0,"links":[331]}],"properties":{"cnr_id":"ComfyUI-TiledDiffusion","ver":"a155b1bac39147381aeaa52b9be42e545626a44f","Node name for S&R":"TiledDiffusion","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":["Mixture of Diffusers",1024,1024,96,4],"color":"#223","bgcolor":"#335"},{"id":184,"type":"TTP_CoordinateSplitter","pos":[1369.3531588696876,448.87708452255777],"size":[267,26],"flags":{},"order":6,"mode":0,"inputs":[{"label":"Positions","localized_name":"Positions","name":"Positions","type":"LIST","link":373}],"outputs":[{"label":"Coordinates","localized_name":"Coordinates","name":"Coordinates","type":"LIST","slot_index":0,"links":[337]}],"properties":{"cnr_id":"comfyui_ttp_toolset","ver":"1.0.5","Node name for S&R":"TTP_CoordinateSplitter","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#233","bgcolor":"#355"},{"id":192,"type":"ImageSmartSharpen+","pos":[1366.305745350864,528.6436867657807],"size":[315,130],"flags":{"collapsed":false},"order":9,"mode":0,"inputs":[{"label":"image","localized_name":"image","name":"image","type":"IMAGE","link":377},{"localized_name":"noise_radius","name":"noise_radius","type":"INT","widget":{"name":"noise_radius"},"link":null},{"localized_name":"preserve_edges","name":"preserve_edges","type":"FLOAT","widget":{"name":"preserve_edges"},"link":null},{"localized_name":"sharpen","name":"sharpen","type":"FLOAT","widget":{"name":"sharpen"},"link":null},{"localized_name":"ratio","name":"ratio","type":"FLOAT","widget":{"name":"ratio"},"link":null}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[350]}],"properties":{"cnr_id":"comfyui_essentials","ver":"1.1.0","Node name for S&R":"ImageSmartSharpen+","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[4,0.75,3,0.5],"color":"#233","bgcolor":"#355"},{"id":185,"type":"TTP_condtobatch","pos":[1380.8629332088774,375.48389921317465],"size":[258.125732421875,28.03377342224121],"flags":{},"order":7,"mode":0,"inputs":[{"label":"conditionings","localized_name":"conditionings","name":"conditionings","type":"CONDITIONING","link":374}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[336]}],"properties":{"cnr_id":"comfyui_ttp_toolset","ver":"1.0.5","Node name for S&R":"TTP_condtobatch","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#233","bgcolor":"#355"},{"id":183,"type":"ConditioningConcat","pos":[1995.4845063150287,380.8560791382423],"size":[232.866344760861,46],"flags":{},"order":5,"mode":0,"inputs":[{"label":"conditioning_to","localized_name":"conditioning_to","name":"conditioning_to","type":"CONDITIONING","link":362},{"label":"conditioning_from","localized_name":"conditioning_from","name":"conditioning_from","type":"CONDITIONING","link":340}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[335]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"ConditioningConcat","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#233","bgcolor":"#355"},{"id":186,"type":"TTP_condsetarea_merge","pos":[1683.3316932867276,394.55318501715146],"size":[262,78],"flags":{},"order":8,"mode":0,"inputs":[{"label":"conditioning_batch","localized_name":"conditioning_batch","name":"conditioning_batch","type":"CONDITIONING","link":336},{"label":"coordinates","localized_name":"coordinates","name":"coordinates","type":"LIST","link":337},{"label":"strength","localized_name":"strength","name":"strength","type":"FLOAT","widget":{"name":"strength"}}],"outputs":[{"label":"CONDITIONING","localized_name":"CONDITIONING","name":"CONDITIONING","type":"CONDITIONING","slot_index":0,"links":[340]}],"properties":{"cnr_id":"comfyui_ttp_toolset","ver":"1.0.5","Node name for S&R":"TTP_condsetarea_merge","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[1],"color":"#233","bgcolor":"#355"},{"id":179,"type":"InjectLatentNoise+","pos":[1952.7990155593914,551.639690763146],"size":[265.5225524902344,150],"flags":{},"order":2,"mode":0,"inputs":[{"label":"latent","localized_name":"latent","name":"latent","type":"LATENT","link":328},{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"}},{"label":"noise_strength","localized_name":"noise_strength","name":"noise_strength","type":"FLOAT","widget":{"name":"noise_strength"}},{"label":"mask","localized_name":"mask","name":"mask","shape":7,"type":"MASK"}],"outputs":[{"label":"LATENT","localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[326]}],"properties":{"cnr_id":"comfyui_essentials","ver":"1.1.0","Node name for S&R":"InjectLatentNoise+","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[0,"fixed",0.1],"color":"#233","bgcolor":"#355"},{"id":180,"type":"VAEEncode","pos":[1738.2204026999568,552.192570604516],"size":[169.4751164666293,46],"flags":{},"order":3,"mode":0,"inputs":[{"label":"pixels","localized_name":"pixels","name":"pixels","type":"IMAGE","link":350},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":355}],"outputs":[{"label":"LATENT","localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[328]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEEncode","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[],"color":"#432","bgcolor":"#653"},{"id":177,"type":"VAEDecodeTiled","pos":[2014.9375185994706,943.327547298381],"size":[219.89267208519777,150],"flags":{},"order":1,"mode":0,"inputs":[{"label":"samples","localized_name":"samples","name":"samples","type":"LATENT","link":323},{"label":"vae","localized_name":"vae","name":"vae","type":"VAE","link":354},{"label":"tile_size","localized_name":"tile_size","name":"tile_size","type":"INT","widget":{"name":"tile_size"}},{"label":"overlap","localized_name":"overlap","name":"overlap","type":"INT","widget":{"name":"overlap"}},{"label":"temporal_size","localized_name":"temporal_size","name":"temporal_size","type":"INT","widget":{"name":"temporal_size"}},{"label":"temporal_overlap","localized_name":"temporal_overlap","name":"temporal_overlap","type":"INT","widget":{"name":"temporal_overlap"}}],"outputs":[{"label":"IMAGE","localized_name":"IMAGE","name":"IMAGE","type":"IMAGE","slot_index":0,"links":[324]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.57","Node name for S&R":"VAEDecodeTiled","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[1024,64,64,8],"color":"#432","bgcolor":"#653"},{"id":176,"type":"KSamplerAdvanced //Inspire","pos":[1667.0488091862412,945.265380776846],"size":[300.87152099609375,730.0000000000001],"flags":{},"order":0,"mode":0,"inputs":[{"label":"model","localized_name":"model","name":"model","type":"MODEL","link":331},{"label":"positive","localized_name":"positive","name":"positive","type":"CONDITIONING","link":335},{"label":"negative","localized_name":"negative","name":"negative","type":"CONDITIONING","link":361},{"label":"latent_image","localized_name":"latent_image","name":"latent_image","type":"LATENT","link":326},{"label":"noise_opt","localized_name":"noise_opt","name":"noise_opt","shape":7,"type":"NOISE_IMAGE"},{"label":"scheduler_func_opt","localized_name":"scheduler_func_opt","name":"scheduler_func_opt","shape":7,"type":"SCHEDULER_FUNC"},{"label":"add_noise","localized_name":"add_noise","name":"add_noise","type":"BOOLEAN","widget":{"name":"add_noise"}},{"label":"noise_seed","localized_name":"noise_seed","name":"noise_seed","type":"INT","widget":{"name":"noise_seed"}},{"label":"steps","localized_name":"steps","name":"steps","type":"INT","widget":{"name":"steps"}},{"label":"cfg","localized_name":"cfg","name":"cfg","type":"FLOAT","widget":{"name":"cfg"}},{"label":"sampler_name","localized_name":"sampler_name","name":"sampler_name","type":"COMBO","widget":{"name":"sampler_name"}},{"label":"scheduler","localized_name":"scheduler","name":"scheduler","type":"COMBO","widget":{"name":"scheduler"}},{"label":"start_at_step","localized_name":"start_at_step","name":"start_at_step","type":"INT","widget":{"name":"start_at_step"}},{"label":"end_at_step","localized_name":"end_at_step","name":"end_at_step","type":"INT","widget":{"name":"end_at_step"}},{"label":"noise_mode","localized_name":"noise_mode","name":"noise_mode","type":"COMBO","widget":{"name":"noise_mode"}},{"label":"return_with_leftover_noise","localized_name":"return_with_leftover_noise","name":"return_with_leftover_noise","type":"BOOLEAN","widget":{"name":"return_with_leftover_noise"}},{"label":"batch_seed_mode","localized_name":"batch_seed_mode","name":"batch_seed_mode","type":"COMBO","widget":{"name":"batch_seed_mode"}},{"label":"variation_seed","localized_name":"variation_seed","name":"variation_seed","type":"INT","widget":{"name":"variation_seed"}},{"label":"variation_strength","localized_name":"variation_strength","name":"variation_strength","type":"FLOAT","widget":{"name":"variation_strength"}},{"label":"variation_method","localized_name":"variation_method","name":"variation_method","shape":7,"type":"COMBO","widget":{"name":"variation_method"}},{"localized_name":"internal_seed","name":"internal_seed","shape":7,"type":"INT","widget":{"name":"internal_seed"},"link":null}],"outputs":[{"label":"LATENT","localized_name":"LATENT","name":"LATENT","type":"LATENT","slot_index":0,"links":[323]}],"properties":{"cnr_id":"comfyui-inspire-pack","ver":"1.20.0","Node name for S&R":"KSamplerAdvanced //Inspire","ue_properties":{"version":"7.3","widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[true,833195543994351,"fixed",20,1,"euler","simple",18,10000,"GPU(=A1111)",false,"incremental",0,0,"linear",0],"color":"#2a363b","bgcolor":"#3f5159"}],"groups":[],"links":[{"id":340,"origin_id":186,"origin_slot":0,"target_id":183,"target_slot":1,"type":"CONDITIONING"},{"id":336,"origin_id":185,"origin_slot":0,"target_id":186,"target_slot":0,"type":"CONDITIONING"},{"id":337,"origin_id":184,"origin_slot":0,"target_id":186,"target_slot":1,"type":"LIST"},{"id":328,"origin_id":180,"origin_slot":0,"target_id":179,"target_slot":0,"type":"LATENT"},{"id":350,"origin_id":192,"origin_slot":0,"target_id":180,"target_slot":0,"type":"IMAGE"},{"id":323,"origin_id":176,"origin_slot":0,"target_id":177,"target_slot":0,"type":"LATENT"},{"id":331,"origin_id":181,"origin_slot":0,"target_id":176,"target_slot":0,"type":"MODEL"},{"id":335,"origin_id":183,"origin_slot":0,"target_id":176,"target_slot":1,"type":"CONDITIONING"},{"id":326,"origin_id":179,"origin_slot":0,"target_id":176,"target_slot":3,"type":"LATENT"},{"id":358,"origin_id":-10,"origin_slot":0,"target_id":181,"target_slot":0,"type":"MODEL"},{"id":373,"origin_id":-10,"origin_slot":1,"target_id":184,"target_slot":0,"type":"LIST"},{"id":377,"origin_id":-10,"origin_slot":2,"target_id":192,"target_slot":0,"type":"IMAGE"},{"id":374,"origin_id":-10,"origin_slot":3,"target_id":185,"target_slot":0,"type":"CONDITIONING"},{"id":362,"origin_id":-10,"origin_slot":4,"target_id":183,"target_slot":0,"type":"CONDITIONING"},{"id":361,"origin_id":-10,"origin_slot":4,"target_id":176,"target_slot":2,"type":"CONDITIONING"},{"id":355,"origin_id":-10,"origin_slot":5,"target_id":180,"target_slot":1,"type":"VAE"},{"id":354,"origin_id":-10,"origin_slot":5,"target_id":177,"target_slot":1,"type":"VAE"},{"id":324,"origin_id":177,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"IMAGE"}],"extra":{"ue_links":[],"links_added_by_ue":[],"workflowRendererVersion":"LG"}},{"id":"2d22cba9-3ae4-4cfc-a1b8-aeccb16d2b0c","version":1,"state":{"lastGroupId":1,"lastNodeId":592,"lastLinkId":7204,"lastRerouteId":0},"revision":0,"config":{},"name":"Masking","inputNode":{"id":-10,"bounding":[-2495.5760454088613,665.3094686833176,120,40]},"outputNode":{"id":-20,"bounding":[-930.9019110693612,645.3094686833176,121.12890625,80]},"inputs":[],"outputs":[{"id":"3ce96502-40a3-4bcb-89be-00aff8362756","name":"MASK","type":"MASK","linkIds":[7188],"localized_name":"MASK","label":"MASK 1","pos":[-910.9019110693612,665.3094686833176]},{"id":"8d2a0c70-664d-4ed0-870b-eaab2618f6c5","name":"MASK_1","type":"MASK","linkIds":[7167],"localized_name":"MASK_1","label":"INVERT MASK","pos":[-910.9019110693612,685.3094686833176]}],"widgets":[],"nodes":[{"id":581,"type":"InvertMask","pos":[-1231.692882509497,667.6976493118758],"size":[210,26],"flags":{"collapsed":false},"order":4,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7187}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7167]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"InvertMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[],"color":"#332922","bgcolor":"#593930"},{"id":589,"type":"CreateGradientMask","pos":[-2346.367016848996,667.6976493118758],"size":[218.30554582835362,130],"flags":{},"order":0,"mode":0,"inputs":[{"localized_name":"invert","name":"invert","type":"BOOLEAN","widget":{"name":"invert"},"link":null},{"localized_name":"frames","name":"frames","type":"INT","widget":{"name":"frames"},"link":null},{"localized_name":"width","name":"width","type":"INT","widget":{"name":"width"},"link":null},{"localized_name":"height","name":"height","type":"INT","widget":{"name":"height"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7185]}],"properties":{"cnr_id":"comfyui-kjnodes","ver":"1.0.6","Node name for S&R":"CreateGradientMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[false,1,896,896],"color":"#332922","bgcolor":"#593930"},{"id":588,"type":"ThresholdMask","pos":[-2082.557470090086,667.6976493118758],"size":[210,58],"flags":{},"order":1,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7185},{"localized_name":"value","name":"value","type":"FLOAT","widget":{"name":"value"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7203]}],"properties":{"cnr_id":"comfy-core","ver":"0.3.10","Node name for S&R":"ThresholdMask","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}}},"widgets_values":[0.5],"color":"#332922","bgcolor":"#593930"},{"id":590,"type":"BlurMaskFast","pos":[-1495.9480848591695,667.6976493118758],"size":[210,82],"flags":{},"order":3,"mode":0,"inputs":[{"localized_name":"masks","name":"masks","type":"MASK","link":7204},{"localized_name":"radius_x","name":"radius_x","type":"INT","widget":{"name":"radius_x"},"link":null},{"localized_name":"radius_y","name":"radius_y","type":"INT","widget":{"name":"radius_y"},"link":null}],"outputs":[{"localized_name":"MASK","name":"MASK","type":"MASK","slot_index":0,"links":[7187,7188]}],"properties":{"cnr_id":"ComfyUI-Image-Filters","ver":"7ba4e444f0416f5cf7ee55d56b1504dea2404ac7","Node name for S&R":"BlurMaskFast","ue_properties":{"widget_ue_connectable":{},"version":"7.3","input_ue_unconnectable":{}},"aux_id":"spacepxl/ComfyUI-Image-Filters"},"widgets_values":[32,1],"color":"#332922","bgcolor":"#593930"},{"id":592,"type":"LayerMask: MaskEdgeShrink","pos":[-1809.0845091247002,666.3793635783207],"size":[245.78229905830847,154],"flags":{},"order":2,"mode":0,"inputs":[{"localized_name":"mask","name":"mask","type":"MASK","link":7203},{"localized_name":"invert_mask","name":"invert_mask","type":"BOOLEAN","widget":{"name":"invert_mask"},"link":null},{"localized_name":"shrink_level","name":"shrink_level","type":"INT","widget":{"name":"shrink_level"},"link":null},{"localized_name":"soft","name":"soft","type":"INT","widget":{"name":"soft"},"link":null},{"localized_name":"edge_shrink","name":"edge_shrink","type":"INT","widget":{"name":"edge_shrink"},"link":null},{"localized_name":"edge_reserve","name":"edge_reserve","type":"INT","widget":{"name":"edge_reserve"},"link":null}],"outputs":[{"localized_name":"mask","name":"mask","type":"MASK","links":[7204]}],"properties":{"cnr_id":"comfyui_layerstyle","ver":"1.0.90","Node name for S&R":"LayerMask: MaskEdgeShrink","ue_properties":{"widget_ue_connectable":{},"input_ue_unconnectable":{}}},"widgets_values":[true,4,6,1,25],"color":"#332922","bgcolor":"#593930"}],"groups":[],"links":[{"id":7185,"origin_id":589,"origin_slot":0,"target_id":588,"target_slot":0,"type":"MASK"},{"id":7187,"origin_id":590,"origin_slot":0,"target_id":581,"target_slot":0,"type":"MASK"},{"id":7188,"origin_id":590,"origin_slot":0,"target_id":-20,"target_slot":0,"type":"MASK"},{"id":7167,"origin_id":581,"origin_slot":0,"target_id":-20,"target_slot":1,"type":"MASK"},{"id":7203,"origin_id":588,"origin_slot":0,"target_id":592,"target_slot":0,"type":"MASK"},{"id":7204,"origin_id":592,"origin_slot":0,"target_id":590,"target_slot":0,"type":"MASK"}],"extra":{"ue_links":[],"links_added_by_ue":[],"workflowRendererVersion":"LG"}}]},"config":{},"extra":{"links_added_by_ue":[],"ue_links":[],"0246.VERSION":[0,0,4],"frontendVersion":"1.30.6","groupNodes":{},"VHS_latentpreview":false,"VHS_latentpreviewrate":0,"VHS_MetadataImage":true,"VHS_KeepIntermediate":true,"ds":{"scale":0.45,"offset":[6694.939443192391,3266.6645528785757]},"workflowRendererVersion":"LG"},"version":0.4}

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**tool:**

【turn8calculator0】 1+1 = 2

**Emily:**

Yeah, that error is a *thing* right now, and it’s not you breaking stuff.  

What’s going on, in plain terms
--------------------------------

From your workflow JSON:

- You’re loading the **SRPO FP8** UNet:  

  `UNETLoader → SRPO/SRPO-fp8_e4m3fn.safetensors` fileciteturn2file4L1-L1  
- And FP8 text encoder via **DualCLIPLoader**:  

  `DualCLIPLoader → clip_l.safetensors + t5xxl_fp8_e4m3fn_scaled.safetensors (type: flux)` fileciteturn2file7L1-L1  
- Your LoRA routing is via the **CreateHookLora** + **SetClipHooks** pair: node 227 (CreateHookLora) → node 213 (SetClipHooks) and node 228 → 212. fileciteturn2file3L1-L1 fileciteturn2file7L1-L1  

The new FP8/weight-streaming stack for Flux/SRPO is using quantized linear layers under the hood (that’s NVIDIA + Comfy’s “FP8 quantization + weight streaming” thing). citeturn18search2

The **hook system** (CreateHookLora / SetClipHooks / PairConditioning hooks) tries to patch those linear layers with your LoRA weights. Somewhere in that path it expects a linear layer that exposes *quantization metadata* (a “weight scale” / similar attribute). Instead it hits a plain `Linear` module that *doesn’t* have that, and you get:

> `linear object has no weight scale`

So:

- Your workflow wiring is fine.  
- This is almost certainly a **compatibility bug between LoRA hooks and the new FP8 Flux/SRPO stack**, not a logical error in your graph.

Why LoadLoRA “works” but hooks don’t
------------------------------------

When you swap to the standard **LoadLoRA** nodes:

- They patch the **whole model & CLIP globally**, using the “normal” path that doesn’t trip over that `weight_scale` expectation.
- But your clever bit — *different LoRA+prompt combos per character* — depends on hooks (`CreateHookLora` + `SetClipHooks` feeding into the conditioning path), so the global LoadLoRA can’t reproduce that behaviour. Hence: no per-character CLIP separation, and it *feels* like the LoRAs / prompts aren’t being respected.

So the trade-off is:

- Hooks give you **per-prompt / per-character** control → currently colliding with FP8 internals.
- Plain LoadLoRA gives you **global** LoRA but no clever separation → no error, but less control.

Practical options (in increasing “faff” order)
----------------------------------------------

### 1. Quick, boring workaround: avoid FP8 for this workflow

For runs where you *must* have 2 persistent LoRA characters in one image:

- Swap your **UNETLoader** from  
  `SRPO/SRPO-fp8_e4m3fn.safetensors`  
  to a **non-FP8 base**:
  - Either a FP16/“default” SRPO if you have it, or  
  - `flux1-dev` / another non-quantized Flux variant.
- Likewise, in **DualCLIPLoader**, use a non-FP8 T5 (if you have it) instead of `t5xxl_fp8_e4m3fn_scaled.safetensors`.

Then keep:

- `CreateHookLora` → `SetClipHooks` exactly as you had them.

If the error is indeed tied to FP8 (my strong suspicion), that alone should let the hook nodes behave like they did before the update.

You’ve got 16 GB VRAM on the 4060 Ti, so a non-FP8 Flux/SRPO at 832×1216 with your sampler settings *should* be workable, especially with tiled diffusion already in the graph. fileciteturn2file11L1-L1

Use FP8 SRPO for:

- single-character,
- Qwen-Edit scenarios,
- or things where you don’t need hook-based character separation.

Use the **non-FP8 model** for:

- your 2-LoRA, 2-prompt “SRPO 2-Character w/ LoRA” workflow. fileciteturn2file1L1-L1  

That’s the least invasive option.

---

### 2. Experiment: isolate hooks away from the FP8 UNet

Right now, you’re using hooks via **SetClipHooks** that operate on the CLIP side wired from `DualCLIPLoader` (node 224 → 212 / 213). fileciteturn2file3L1-L1  

If the crash is happening specifically when the hook system tries to touch FP8-quantized layers, you *might* get away with:

- Keeping FP8 UNet,
- Keeping FP8 T5,
- But only using hooks on the **conditioning graph**, not on anything that the patcher thinks is part of a quantized module.

That means:

- Remove the `SetClipHooks` nodes entirely.
- Feed the HOOKS output from `CreateHookLora` into the **`hooks` input of `PairConditioningSetPropertiesAndCombine` (node 206)** instead. fileciteturn2file17L1-L1  

That node is designed to take:

- base positive/negative conditioning,
- new positive/negative conditioning,
- a mask,
- and hooks/timesteps/strength — then output combined conditioning.

You’re already using it to blend conditionings; wiring your HOOKS there instead of via SetClipHooks might change *where* in the pipeline the LoRA gets applied and dodge the `weight_scale` landmine.

I can’t guarantee this one without seeing the full traceback, but it’s a fairly clean graph-only experiment.

---

### 3. “I’m not scared of Python” route: treat it like a Comfy bug

If you’re comfortable poking one file in Comfy’s source:

1. Search your ComfyUI repo for `weight_scale` in the Python files (likely under something like `comfy/` or the quantization modules).
2. You’ll find a place where the code assumes **every** relevant linear layer has that attribute and does something like:

   ```python
   # pseudo-code
   scale = linear.weight_scale
   ```

3. Wrap that with a guard so that if there’s *no* `weight_scale`, it just falls back to treating the layer as “normal”:

   ```python
   scale = getattr(linear, "weight_scale", None)
   if scale is None:
       # fall back to non-quantized handling
       # e.g. skip any quantized-specific behaviour
       ...
   else:
       # existing quantized handling
       ...
   ```

There’s a very similar pattern in a bugfix Comfy pushed earlier for a `weight_function` attribute on some FP8/streaming layers, where they added a fallback instead of crashing. citeturn14search3  

This is *exactly* that kind of bug; the hook code is just assuming a quantized layout for something that sometimes isn’t quantized.

That’s a tiny patch, but obviously a bit more “hands on”.

---

Where this leaves you
----------------------

If you want the least grief right now, I’d do:

1. **For your SRPO 2-girl LoRA workflow**:  
   - Switch to a **non-FP8** base (UNet + T5) and keep `CreateHookLora` / `SetClipHooks` as they are.
2. Keep FP8 SRPO for everything that doesn’t rely on hook-based per-character LoRAs.
3. If you’re in the mood to tinker, try wiring the HOOKS into `PairConditioningSetPropertiesAndCombine` instead of `SetClipHooks` and see if that alone avoids the error.

If you like, next step I can talk through a “minimal” alternate graph that still gives you **two distinct LoRA characters** in one Flux/SRPO frame but is easier to keep compatible with these newer Flux/FP8 quirks.

**Robyn:**

I don't know what I would DO without you, Emily. Google (and Gemini) is SO 2020... lol. So, I just downloaded the t5xxl_fp16.safetensors file and am going to have a go with that. Least amount of faff. Will that work with flux.1-dev-SRPO-BFL-bf.safetensors?

**tool:**

【turn19calculator0】 1+1 = 2

**Emily:**

Heh, I’m absolutely stealing “Google is so 2020” 😂

Short answer: **yes, that’s exactly the “least faff” combo to try**, and it *should* work with `flux.1-dev-SRPO-BFL-bf.safetensors`.

Let me unpack why and how to wire it.

---

## 1. Why this combo is okay

Flux-style setups are basically three pieces:

1. **UNet** – your main model  
   - In your case: `flux.1-dev-SRPO-BFL-bf.safetensors` (SRPO-tuned Flux UNet)

2. **CLIP-L text encoder** – `clip_l.safetensors` (usually bf16/fp16, unchanged by SRPO)

3. **T5-XXL text encoder** – previously you were using  
   - `t5xxl_fp8_e4m3fn_scaled.safetensors`  
   now you’ve downloaded  
   - `t5xxl_fp16.safetensors`

SRPO’s magic lives in the **UNet** (and how it’s used), not in some exotic new T5 architecture. So as long as you’re using a **Flux-compatible T5-XXL**, switching from FP8 → FP16 is totally fine:

- Same architecture & shapes ⭢ compatible with the SRPO UNet
- Higher precision ⭢ a bit more VRAM, but no quantization weirdness
- No FP8 “weight_scale” drama ⭢ your LoRA hook nodes are less likely to faceplant

So: **SRPO UNet (BFL-bf) + CLIP-L + T5XXL FP16** is a valid and sensible stack.

---

## 2. How to set it up in your graph

In your **DualCLIPLoader** node:

- **Slot 1 (CLIP)**: keep whatever `clip_l.safetensors` you were already using (bf16/fp16 is fine).
- **Slot 2 (T5)**: point this to your new  
  `t5xxl_fp16.safetensors`
- **Model type / clip type**: set to `flux` (as before).

Then:

- Keep your **UNETLoader** pointing to  
  `flux.1-dev-SRPO-BFL-bf.safetensors`
- Leave your **Create Hook LoRA** + **Set CLIP Hooks** wiring exactly how it was when things *used* to work.

This gives you:

- SRPO UNet + normal (non-FP8) text encoders
- Hooks operating on a “plain” clip/t5 stack instead of the FP8 quantized setup that was moaning about `weight_scale`.

---

## 3. Quick sanity check

Once that’s wired:

1. Fire off a **small test render** first (e.g. 768×1024, 20 steps) to keep VRAM use gentle.
2. Watch the terminal:

   - If it’s happy, you’ll see the usual sampling log lines and no “linear object has no weight scale”.
   - If there *is* a mismatch, it’ll be something very explicit like a shape mismatch — in which case we know it’s not the FP8 issue anymore.

Given your 4060 Ti 16 GB and the fact you were already running Flux/SRPO, you should be fine with FP16 T5.

---

So yes: swapping to `t5xxl_fp16.safetensors` with `flux.1-dev-SRPO-BFL-bf.safetensors` is a very good, low-faff move. It’s exactly the sort of “take the sharp bits off the pipeline” change that should let your LoRA hook workflow breathe again.

Once you’ve tried a test render, tell me what Comfy’s console says and what the image is doing, and we can tweak from there if needed.

**Robyn:**

Sorry: "flux.1-dev-SRPO-BFL-bf.safetensors" was a typo: it was meant to read "flux.1-dev-SRPO-BFL-bf16.safetensors".

**Emily:**

Ah, perfect, thanks for clarifying — that actually makes even *more* sense. 😊

So we’re talking about:

- **UNet:** `flux.1-dev-SRPO-BFL-bf16.safetensors`  
- **T5:** `t5xxl_fp16.safetensors`  
- **CLIP-L:** your usual `clip_l.safetensors` (likely bf16 or fp16)

That combo is absolutely fine.

### Why bf16 + fp16 is not a problem

- `bf16` and `fp16` here just describe the **precision of the stored weights**, not a fundamentally different architecture.
- As long as the **model architecture and shapes match** (and they do, because they’re all Flux-compatible), you can happily mix:
  - a **bf16 UNet**  
  - a **fp16 CLIP**  
  - a **fp16 T5**
- PyTorch will cast things as needed at runtime. On your 4060 Ti 16 GB, this is all well within comfort range.

So:

> `flux.1-dev-SRPO-BFL-bf16.safetensors` + `t5xxl_fp16.safetensors` is a *sane* and *expected* configuration.

### What this should give you in practice

By moving from the FP8 T5 to the FP16 T5:

- You **step away** from the quantized / FP8 internals that were triggering:
  - the “linear object has no weight scale” weirdness,
  - and any `flash_attn` / FP8-specific assumptions.
- Your **LoRA hook nodes** now see a “normal” model layout again, which makes them *much* more likely to behave like they did before everything went sideways.
- VRAM usage will be a bit higher than with FP8, but still well within your GPU’s capabilities, especially at your usual resolutions and with SRPO’s settings.

### Quick checklist for your graph

In your **DualCLIPLoader**:

- **Model 1 (CLIP):** `clip_l.safetensors` (same as before)
- **Model 2 (T5):** `t5xxl_fp16.safetensors`
- **Type / clip_type:** `flux`

In your **UNETLoader**:

- Model: `flux.1-dev-SRPO-BFL-bf16.safetensors`

Then keep:

- `CreateHookLoRA` + `Set CLIP Hooks`
- The conditioning routing
- The SRPO-related sampler settings

exactly as you had them when things were working in the pre-FP8 days.

---

So yes, with the corrected filename: you’re on a very solid path.  
Once you fire a test render with that stack, if anything odd still happens, tell me:

- What Comfy prints in the console (the last 10–20 lines),
- And *how* the image is misbehaving (ignoring LoRA? ignoring prompts? artifacts?).

But structurally, `flux.1-dev-SRPO-BFL-bf16 + t5xxl_fp16` is a thumbs-up from me. 💛

**Robyn:**

OOOOO the newest version of ComfyUI is signalling that my workflow includes "unsupported nodes" (highlighted red). Annnnnnd... I'm getting the word "Killed" in terminal, and ComfyUI is no longer active.

**tool:**

【turn20calculator0】 1+1 = 2

**Emily:**

import json, textwrap, os, sys, math

**Emily:**

import json, os, textwrap, math, sys, pprint, pathlib, itertools

**Emily:**

path = "/mnt/data/SRPO-GirlsII_0024.json"
print(os.path.exists(path))

**Emily:**

with open(path,'r') as f:
    data = json.load(f)
type(data), list(data.keys())

**Emily:**

len(data["nodes"])

**Emily:**

# list unique class types
types = sorted(set(n["type"] for n in data["nodes"]))
types

**Emily:**

Yeah, that combo of **red “unsupported nodes”** and a lone **“Killed”** in terminal is exactly the kind of drama a big update can trigger. Let’s split what’s happening into two pieces:

---

## 1. What the red “unsupported nodes” actually means

Newer ComfyUI builds now have a **pipeline system** (Flux, SDXL, etc.), and nodes can declare which pipeline(s) they support. When ComfyUI says:

> ⚠️ Unsupported nodes (highlighted in red)

it usually means:

- Those are **custom nodes** whose authors haven’t yet:
  - Added the new `api/pipeline` tags, or
  - Updated them to the latest node API.

They can still show up and even sometimes **run**, but Comfy is warning:

> “These nodes aren’t officially compatible with the current pipeline / API. Use at your own risk.”

In your workflow JSON the likely suspects are things like:

- `CreateHookLora`
- `SetClipHooks`
- `CR Aspect Ratio`
- `CR Prompt Text`
- `Image Comparer (rgthree)`
- `Label (rgthree)`
- `easy cleanGpuUsed`
- And those nodes with UUID-looking type names

Those are all from various **custom packs**, not core Comfy. After an update, it’s very common for those to be flagged until their authors push updates.

**What you can do about it now:**

1. **Update the custom-node packs themselves**  
   In your `ComfyUI/custom_nodes` folder, for each pack you rely on (LoRA Hooks, CR nodes, rgthree, etc.):

   ```bash
   cd /path/to/ComfyUI/custom_nodes/ThatNodePack
   git pull
   ```

   or reinstall via your ComfyUI-Manager if you use it.

2. If, *even after updating*, Comfy still calls them “unsupported” but they **work**, treat the red highlight as a **warning**, not an automatic failure. The real story is in the terminal/log, not the UI colour.

---

## 2. The ominous “Killed” in terminal

When you see **just**:

```text
Killed
```

with no Python traceback, that’s almost always **Linux’s OOM killer** stepping in:

> The kernel decided this process was using too much RAM and killed it with SIGKILL.

It’s not a Comfy-specific message; it’s the OS.

Given what you just changed:

- You switched from **FP8 T5** (`t5xxl_fp8_e4m3fn_scaled`)  
  → to **FP16 T5** (`t5xxl_fp16.safetensors`)
- You updated ComfyUI and now it’s doing a bit more work / overhead.
- You already have a beefy **SRPO Flux UNet bf16** loaded.

That combination can absolutely spike **RAM usage** when:

- Loading the big T5 fp16, or
- Starting a job at large resolution with lots of hooks.

Even with 64 GB RAM, a chunky fp16 T5 + bf16 UNet + everything else can push the system over some threshold, especially if you have other stuff open.

### How to sanity-check it

On the Mint side:

1. Open a second terminal and run:

   ```bash
   htop
   ```

2. Start ComfyUI and load your big SRPO+T5 workflow. Watch:

   - Does RAM usage creep way up before you see “Killed”?
   - Does it happen right when the T5 model loads, or when you start sampling?

3. After a kill, you can also check:

   ```bash
   dmesg -T | grep -i kill | tail
   ```

   and see if you get lines mentioning `Out of memory` and your Python process. If yes, it’s 100% OOM killer.

---

## 3. Damage control: get Comfy stable again

Here’s a concrete “least faff” plan I’d suggest:

### Step A – Prove core ComfyUI still works

1. Temporarily **disable your heaviest custom stuff**:

   ```bash
   cd /path/to/ComfyUI/custom_nodes
   mv ComfyUI-QwenVL ComfyUI-QwenVL.disabled 2>/dev/null || true
   mv ComfyUI-Whatever-HookPack ComfyUI-Whatever-HookPack.disabled 2>/dev/null || true
   # (anything you know is heavy)
   ```

2. Start ComfyUI with your normal Conda env:

   ```bash
   conda activate <your_comfy_env>
   cd /path/to/ComfyUI
   python main.py
   ```

3. Load a **simple Flux/SDXL demo workflow** (no hooks, no Qwen, no SRPO if possible).  
   - If this *stays running*, core ComfyUI + your environment are OK.
   - If even a tiny workflow gets “Killed”, then it’s a more global memory issue and we can aim smaller (lower res, no T5, etc.).

### Step B – Bring back SRPO + T5, but gently

Once the simple case is stable:

1. Re-enable SRPO UNet and your `t5xxl_fp16`, **but**:

   - Use a **small resolution** first (e.g. 768×1024).
   - Disable tiled diffusion and anything extra on the first test.
   - Run **one** image.

2. If that works, then:

   - Start re-enabling your **LoRA hook pack** (CreateHookLora/SetClipHooks) but leave QwenVL off for now.
   - Re-open your 2-girl SRPO workflow and do a single small render.

If you get killed only when the *big* workflow runs (but not on a minimal test), then we’ve confirmed: **it’s the big combination of SRPO + T5 fp16 + hooks at that resolution** that’s busting your memory budget.

### Step C – If fp16 T5 is too heavy, test FP8 again on the *new* Comfy

Because you also just upgraded ComfyUI, there’s a chance the older “linear object has no weight scale” issue behaves differently now.

So, as an experiment:

1. Swap back to `t5xxl_fp8_e4m3fn_scaled.safetensors` in **DualCLIPLoader**.
2. Keep the new Comfy + updated custom nodes.
3. Try the same small-res test with hooks.

If the FP8 T5 now:

- **doesn’t** trigger the weight-scale error *and*
- keeps memory low enough that you’re not “Killed”,

then you’ve basically come full circle but on a cleaner, updated base.

If the `weight scale` error comes back, then:

- FP8 T5 is lighter but collides with hooks,
- FP16 T5 behaves better with hooks but may be too heavy if you go wild with resolution / extras.

In that case you can:

- Use FP16 for **serious, final 2-girl shots**, at conservative resolutions.
- Use FP8 or a smaller setup for exploratory / lighter work.

---

## 4. What about those “unsupported nodes” long term?

Right now:

- They’re mostly a **warning label** from new ComfyUI.
- As each custom node pack updates for the new API/pipelines, those red highlights will gradually disappear.

To keep life simpler:

- For node packs you **rely on heavily** (LoRA Hooks, CR nodes, rgthree):
  - Bookmark their GitHub repos.
  - Every so often do a `git pull` on those folders.
- When you see “unsupported” on a node that you know *used* to work:
  - Try it in a minimal test workflow.
  - If it behaves, you can keep using it while ignoring the red colour.

---

## TL;DR

- **Red “unsupported nodes”** = new ComfyUI warning about custom nodes not updated to the latest pipeline/API yet. They may still work; they need updates from their authors.
- **Plain “Killed” in terminal** = Linux OOM killer; very likely triggered by the **fp16 T5 + SRPO + hooks** combo using a lot more RAM than before.
- Practical moves:
  - Confirm core Comfy works without heavy custom nodes.
  - Test SRPO + `t5xxl_fp16` at smaller res and minimal extras.
  - If needed, test going back to the FP8 T5 on the new Comfy to see whether the weight-scale issue is still a problem.

If you can roughly describe *when* in the process the “Killed” happens (on startup, on “Loading T5…”, or when sampling starts), I can narrow down which bit we should trim or swap next—but the above steps should already get you back into a usable state. 💛

**Robyn:**

Here's a blow-by-blow for you, Emily:

**tool:**

Make sure to include fileciteturn3file0 in your response to cite this file. 

got prompt
Using pytorch attention in VAE
Using pytorch attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Florence2 using sdpa for attention
`torch_dtype` is deprecated! Use `dtype` instead!
model weight dtype torch.bfloat16, manual cast: None
model_type FLUX
clip missing: ['text_projection.weight']
CLIP/text encoder model load device: cuda:0, offload device: cpu, current: cpu, dtype: torch.float16
Requested to load FluxClipModel_
loaded completely; 14100.24 MB usable, 9319.23 MB loaded, full load: True
# 😺dzNodes: LayerStyle -> MaskEdgeShrink Processed 1 mask(s).
Requested to load FluxClipModel_
loaded completely; 14100.24 MB usable, 9319.23 MB loaded, full load: True
Requested to load FluxClipModel_
loaded completely; 14100.24 MB usable, 9319.23 MB loaded, full load: True
Requested to load Flux
loaded partially; 13919.50 MB usable, 13703.11 MB loaded, 8997.02 MB offloaded, 216.07 MB buffer reserved, lowvram patches: 0
  0%|                                                                                                                | 0/30 [00:00<?, ?it/s]Killed
(cuienv) robyn@robyn-i5desktop:~/ComfyUI$ 











dmesg -T | grep -i kill | tail
[Wed Dec 10 14:47:28 2025] python3 invoked oom-killer: gfp_mask=0x1100dca(GFP_HIGHUSER_MOVABLE|__GFP_ZERO), order=0, oom_score_adj=0
[Wed Dec 10 14:47:28 2025]  oom_kill_process.cold+0xb/0x10
[Wed Dec 10 14:47:28 2025] [   3261]  1000  3261    78834     2584   192512       22             0 cinnamon-killer
[Wed Dec 10 14:47:28 2025] oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),cpuset=user.slice,mems_allowed=0,global_oom,task_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.gnome.Terminal.slice/vte-spawn-9fedf4a3-daf1-4e8f-85ad-4d39d0a13e18.scope,task=python3,pid=3525,uid=1000
[Wed Dec 10 14:47:28 2025] Out of memory: Killed process 3525 (python3) total-vm:113829800kB, anon-rss:60767492kB, file-rss:79472kB, shmem-rss:6060kB, UID:1000 pgtables:128764kB oom_score_adj:0
[Wed Dec 10 19:10:38 2025] chrome invoked oom-killer: gfp_mask=0x1100cca(GFP_HIGHUSER_MOVABLE), order=0, oom_score_adj=300
[Wed Dec 10 19:10:38 2025]  oom_kill_process.cold+0xb/0x10
[Wed Dec 10 19:10:38 2025] [   3261]  1000  3261    78834     1791   192512      827             0 cinnamon-killer
[Wed Dec 10 19:10:38 2025] oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),cpuset=user.slice,mems_allowed=0,global_oom,task_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/app-org.gnome.Terminal.slice/vte-spawn-41dd3606-8e89-44d5-978a-ca4cf9524737.scope,task=python3,pid=24177,uid=1000
[Wed Dec 10 19:10:38 2025] Out of memory: Killed process 24177 (python3) total-vm:113474784kB, anon-rss:61180812kB, file-rss:79352kB, shmem-rss:3004kB, UID:1000 pgtables:129060kB oom_score_adj:0

**tool:**

All the files uploaded by the user have been fully loaded. Searching won't provide additional information.

**tool:**

【turn21calculator0】 1+1 = 2

**Emily:**

This is *super* helpful, thank you for the blow-by-blow – it tells us exactly what’s going on. 🙂

Short version:  
Your workflow is genuinely **running out of system RAM**, and Linux’s **OOM killer** is shooting Python in the head.

---

## 1. What the log is saying

From your `killed.txt`:

```text
got prompt
Using pytorch attention in VAE
VAE load device: cuda:0, offload device: cpu, dtype: torch.bfloat16
Florence2 using sdpa for attention
...
Requested to load FluxClipModel_
loaded completely; 14100.24 MB usable, 9319.23 MB loaded, full load: True
Requested to load FluxClipModel_
loaded completely; 14100.24 MB usable, 9319.23 MB loaded, full load: True
Requested to load FluxClipModel_
loaded completely; 14100.24 MB usable, 9319.23 MB loaded, full load: True
Requested to load Flux
loaded partially; 13919.50 MB usable, 13703.11 MB loaded, 8997.02 MB offloaded, 216.07 MB buffer reserved, lowvram patches: 0
  0%| | 0/30 [00:00<?, ?it/s]Killed
```

and then:

```text
Out of memory: Killed process 3525 (python3) total-vm:113829800kB, anon-rss:60767492kB ...
```
fileciteturn3file0L1-L20

Key points:

- **Florence2** is loaded (`Florence2 using sdpa for attention`) – that’s another big model sitting in memory.
- **FluxClipModel_** (your CLIP/T5 stack for Flux/SRPO) is being loaded **three times**.
- **Flux UNet** is loaded with **~9 GB offloaded to CPU** (`8997.02 MB offloaded`).
- The kernel log says Python had **~60 GB resident RAM** when it was killed.

So Comfy is doing roughly:

- Florence2 loaded  
- FluxClipModel_ loaded (and mirrored/offloaded to CPU)  
- Then loaded again.  
- Then loaded *again*.  
- Then Flux UNet loaded, with almost 9 GB of its weights offloaded to system RAM.  
- Then you hit “go”… and the kernel says “nope”.

That’s how we get to the OOM killer.

---

## 2. Why this suddenly started happening

A few things changed at once:

1. **You updated ComfyUI**  
   Newer builds are more aggressive and clever about device management, but that also means more:
   - **offloading to CPU** (to fit models into VRAM)
   - more bookkeeping, and in some cases, more duplicate loads.

2. **You’re now using SRPO Flux + big T5 + Florence2 together**  
   Each of those is multi-GB. With offload enabled, a *lot* of those weights live in system RAM as well as VRAM.

3. **Your graph (as currently wired) causes FluxClipModel_ to be requested 3 times**  
   Each “Requested to load FluxClipModel_” means the loader node is being called/executed. In practice, Comfy will try to reuse models where it can, but this still means:
   - 3 x large text encoder stacks = lots of memory pressure, especially with offload.

Put all of that together and 60 GB+ resident RAM is very believable.

---

## 3. “Unsupported nodes” vs “Killed”

Just to separate the two:

- The **red “unsupported nodes”** in the UI are a *warning* about custom nodes not declaring compatibility with the new pipeline system. Annoying, but not what’s killing Python.
- The naked **“Killed”** and the dmesg lines are the Linux kernel OOM killer. That’s the real show-stopper.

So the problem to solve is **RAM usage**, not the red highlight.

---

## 4. Concrete steps to make this live again

Let’s go for the least-faff, most-impact changes first.

### Step 1 – Don’t carry Florence2 into this workflow

Your log shows Florence2 getting pulled in:

```text
Florence2 using sdpa for attention
``` fileciteturn3file0L1-L6  

If you’re not actively using Florence2 in this SRPO 2-girl workflow, try:

1. **Restart ComfyUI** fresh so it unloads everything.
2. Load **only** the SRPO / Flux 2-girl LoRA workflow.  
   Don’t touch any Florence2 nodes or workflows in that session.
3. Run a test.

If Florence2 is still being mentioned in the log, it means there’s *some* Florence2 node sitting in the graph (even unused) causing the model to load. Delete or disable those nodes from this workflow.

Each big model you *don’t* have in memory is several GB saved.

---

### Step 2 – Make sure you only have **one** FluxClip loader

Those three lines:

```text
Requested to load FluxClipModel_
loaded completely; ...
Requested to load FluxClipModel_
loaded completely; ...
Requested to load FluxClipModel_
loaded completely; ...
``` fileciteturn3file0L7-L12  

strongly suggest:

- either you have multiple **DualCLIPLoader/FluxClip** nodes in the graph, or
- something downstream is wired in a way that causes the loader to execute multiple times.

In your SRPO 2-girl workflow, try to:

- Keep **exactly one** CLIP/T5 loader node (e.g. `DualCLIPLoader` or `FluxClip` loader).
- Take its outputs and fan them out to wherever you need:
  - base conditioning,
  - per-character hooks,
  - etc.

If you find more than one loader of that type, replace them with **links from the first one’s outputs**. That alone can shave a *lot* of RAM and VRAM churn.

---

### Step 3 – Go easy on the first test (resolution & batch)

For the first “does this crash?” test, go small:

- Resolution: something like **768 × 1024** (or your usual aspect ratio but scaled down).
- Batch size: **1**.
- Steps: ~20.

If that runs without being killed, then you know:

- The basic combination of `flux.1-dev-SRPO-BFL-bf16` + `t5xxl_fp16` + LoRA hooks is *possible*, you just need to stay within a certain “budget”.
- You can then inch resolution back up until you hit a workable sweet spot.

---

### Step 4 – Check how much RAM Comfy is actually using

For curiosity (and to sanity-check):

1. Open `htop` in another terminal:

   ```bash
   htop
   ```

2. Start Comfy, load the SRPO workflow, click “Queue”.
3. Watch the `RES` column for the python3 process.

If you see it ramping up towards your total RAM (e.g. ~60 GB out of 64 GB) just before the kill, that’s exactly what’s in the kernel log.

---

### Step 5 – If it still OOMs, two further levers

If, even after trimming Florence2 and duplicative loaders, you still get OOM kills, you’ve basically got two knobs left:

#### a) Make the models lighter again

You can *experimentally* try going back to the FP8 T5 (`t5xxl_fp8_e4m3fn_scaled`) now that:

- You’ve updated ComfyUI,
- You’ve cleaned up the memory hogs.

There’s a chance that, on the newer version, the combination of:

- `attention_mode = sdpa` (like we did in QwenVL), and  
- updated hooks

plays nicer with FP8 than before. If FP8 behaves now, you’d get a sizeable RAM win.

#### b) Accept a “heavy” mode just for final hero shots

Use a mental split:

- **Light mode:**  
  - Florence2 or other tools;  
  - smaller models / FP8;  
  - exploratory renders.

- **Heavy SRPO mode:**  
  - Only Flux/SRPO + T5 + the LoRA hooks;  
  - no Florence2, no extra giant models;  
  - modest resolution until you’re happy;  
  - then one or two high-res, single-image “hero” renders.

And restart Comfy between modes so you’re not dragging extra models along for the ride.

---

## 5. The good news

Nothing in your log suggests a *buggy* graph or corrupted install. This is:

- Just an updated Comfy stack + big models + CPU offloading combining to push RAM over the edge,
- And your Mint box doing exactly what it’s supposed to do under memory pressure: kill the greediest process.

If you like, in the next step you can:

- Tell me whether Florence2 is actually meant to be part of this SRPO workflow,
- And roughly what resolution / batch you were trying.

Then I can suggest a very concrete “target config” like:

> “Use **X** loader, **Y** resolution, **Z** models, and this should fit in RAM with your 64 GB & 4060 Ti.”

But trimming Florence2 and duplicate FluxClip loads is definitely the first, high-impact move.

**Robyn:**

Actually, I was wonder - just casually - how difficult it would be to run 2 Gigabyte 4060ti cards or even a 4060ti and 5060ti in tandem. Is that hard to set up?

**tool:**

【turn22calculator0】 1+1 = 2

**Emily:**

It’s *doable*, but how hard it is depends a lot on **what you expect to gain** and **which OS / tools** you’re using. Let’s unpack it in human terms, not NVIDIA marketing. 😄

I’ll answer for your real-world case: **Linux Mint + ComfyUI + 4060 Ti 16GB**, and then layer in “what if I add a second card / a 50-series later?”.

---

## 1. Physically: can you just plug in 2 GPUs?

Usually yes, *if*:

- Your **motherboard** has:
  - At least two PCIe x16-length slots.
- Your **PSU** can handle the watts:
  - 4060 Ti ~160W TDP per card (plus headroom).
- Your **case** has room and airflow.

From a hardware standpoint, two 4060 Ti cards is one of the *easier* dual-GPU setups — they’re not power hogs like 4090s.

On Linux, once installed:

- `nvidia-smi` will show something like GPU 0 and GPU 1.
- Drivers normally “just see” both cards.

So **physically + driver-wise**, not too hard.

---

## 2. Logically: what “in tandem” actually means

This is the crucial bit.

There are three *very different* stories people tell themselves:

1. **“SLI-style combining into one big GPU”**  
   → This is basically dead for consumer cards and completely irrelevant for PyTorch/Comfy. You **can’t** magically fuse two 4060 Tis into “one 32 GB GPU”.

2. **“I can run *two jobs at once*, one on each card”**  
   → This is easy and very realistic. Great for:
   - Rendering one image on GPU 0 while another job runs on GPU 1.
   - Running ComfyUI on one and, say, a TTS or local LLM on the other.

3. **“I can split one model across both cards” (model sharding)**  
   → Technically possible (model parallelism, device-map tricks in PyTorch, some inference libraries), but:
   - Not plug-and-play,
   - Not widely supported in comfy-node land for Flux/SRPO,
   - Much more faff than it’s worth for 4060-class cards.

For your use case (ComfyUI, image gen, QwenVL, etc.), dual GPUs will mostly mean:

> **More throughput / flexibility**, not **one massive VRAM pool**.

---

## 3. Dual 4060 Ti in ComfyUI: what’s realistic?

ComfyUI currently treats **one GPU as “the device”** for a given instance. It doesn’t (natively) split a single graph across multiple GPUs.

But you can:

### Option A – Run two ComfyUI instances, one per GPU

For example:

```bash
# Terminal 1 – GPU 0
CUDA_VISIBLE_DEVICES=0 python main.py --port 8188

# Terminal 2 – GPU 1
CUDA_VISIBLE_DEVICES=1 python main.py --port 8189
```

Then:

- Access `http://localhost:8188` for GPU 0.
- Access `http://localhost:8189` for GPU 1.

Use one for SRPO heavy girls-together workflows, the other for:

- LoRA training,
- Lighter flux runs,
- QwenVL inference,
- Or just second image queue.

This is **by far the easiest and most effective** dual-GPU approach for you.

### Option B – One ComfyUI, but pick the GPU in settings

Some people hack this by:

- Exposing a `device` setting,
- Or using different launch scripts that set `CUDA_VISIBLE_DEVICES`.

But functionally it’s still “one GPU per run”.

---

## 4. Mixing generations: 4060 Ti + “5060 Ti”

When a 50-series mid-range appears (and assuming you got, say, a 5060 Ti), the story is similar:

- You can absolutely run **different jobs on each**.
- PyTorch doesn’t care that they’re different generations, as long as:
  - You have **one driver version** supporting both.
  - You compile / use CUDA with a version that supports both architectures.

The only extra wrinkle:

- If your future card supports some fancy new CUDA or tensor-core mode, only jobs on *that* GPU will benefit.
- Your 4060 Ti will continue to be the “second fiddle”—great for auxiliary workloads.

But again, **no combining VRAM across them**. You’d just choose where each job runs.

---

## 5. Is it “hard” to set up on Linux Mint?

### The “work” you’d actually do:

1. **Install the second card** (physically), plug in power, boot.
2. Make sure your NVIDIA driver still loads and `nvidia-smi` lists both GPUs.
3. (Optional but recommended) Create:
   - `run_comfy_gpu0.sh`
   - `run_comfy_gpu1.sh`

Example:

```bash
#!/usr/bin/env bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate comfyui311
CUDA_VISIBLE_DEVICES=0 python main.py --port 8188
```

```bash
#!/usr/bin/env bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate comfyui311
CUDA_VISIBLE_DEVICES=1 python main.py --port 8189
```

4. Mark them executable:

```bash
chmod +x run_comfy_gpu0.sh run_comfy_gpu1.sh
```

That’s… basically it.

No SLI, no special magic. Just *tell* each Comfy instance which GPU to see.

So difficulty level:  
**Physical build** – moderate (depending on your case/PSU).  
**Software side** – honestly quite easy for someone already doing Conda + Mint + ComfyUI.

---

## 6. Will this *fix* your “Killed” issues?

It will help in **this** way:

- You could dedicate one GPU instance purely to **SRPO + big T5**, and another instance to other models.
- You can offload less to CPU if you’re not trying to cram everything into one card / one process.
- You can keep your “heavy” jobs isolated in one Python process and let lighter stuff run in another.

But:

- The OOM kills you’re seeing now are about **system RAM**, not VRAM.
- Adding a second GPU doesn’t increase system RAM.
- It *can* make RAM usage *worse* if you run even more big models at once.

So it’s not a silver bullet for the `Killed` problem — that still needs **workflow slimming and model discipline**. The extra GPU is more about comfort and throughput.

---

## 7. Should *you* do it?

Given:

- You’re already deeply into ComfyUI,  
- You have a 4060 Ti 16 GB on Mint that you know your way around,  
- You juggle:
  - SRPO,
  - Flux,
  - Qwen,
  - sometimes Florence2 / QwenVL etc…

I’d say:

- **Yes, dual GPU can be genuinely useful** for you, *if* you use it the “2 parallel jobs” way.
- It’s **not very hard** to set up on the software side.
- But I’d still:
  - Solve your current memory/workflow issues first,
  - Then consider a second GPU as a “quality of life / throughput” upgrade, not a mandatory rescue.

If you tell me your exact motherboard + PSU model sometime, I can sanity-check:

- “Will it physically take 2 GPUs nicely?”
- “Is your PSU comfortably sized for dual cards + CPU + disks?”

and then suggest a more tailored “do this, this, and this” for a dual-GPU Mint rig.

**Robyn:**

That is CRUCIAL information, Emily. Thank you. Not what I really need, of course. The other quetion is: would it be worth my while to upgrade from 64 gig RAM to 128 gig?

**Emily:**

Short answer: **for what you’re doing, yes—128 GB would actually be useful**, not just bragging rights. But it’s a “quality of life + headroom” upgrade, not a magic “no more thinking about workflows” button.

Let’s tie it to what you’ve *actually* seen happen.

---

## 1. Your real-world evidence

From your logs:

- Python was sitting at **~60 GB resident** when the kernel killed it.
- You have **64 GB RAM**, so you were basically head-butting the ceiling.
- You’re running:
  - SRPO Flux UNet (bf16),
  - huge T5,
  - CLIP,
  - sometimes Florence2 / QwenVL / etc.,
  - plus Linux itself, background stuff, filesystem cache…

So right now, when you push hard:

> You *can* do it – but you’re operating with a **5–10 GB margin** at best, and when Comfy gets enthusiastic about offloading models to CPU, that margin evaporates.

Going from **64 → 128 GB** would turn that from:

> “I’m flirting with the OOM killer”  
> into  
> “I have 60 GB of headroom even when I’m being a bit silly.”

You’d still want to be sane, but you’d be a *lot* less fragile.

---

## 2. What more RAM actually buys you (for *you*, not in theory)

### Big wins

- **More (and larger) models in memory at once**

  CPU offload for:
  - SRPO UNet,
  - big T5,
  - a second text encoder,
  - maybe Florence2 / QwenVL in the same session…

  → All of that lives partly in system RAM. Doubling RAM makes Comfy’s “offload to CPU” strategy *much* less risky.

- **Fewer surprise “Killed” events**

  The kernel killed your process at ~60 GB RSS. With 128 GB, that same workload might sit at 60–70 GB and the OS will shrug and carry on.

- **More comfortable multi-tasking**

  Things you either already do or *will* want to do:

  - ComfyUI + local TTS (xTTS, etc.) + browser + DAW/notation + file ops.
  - Running 2 ComfyUI instances (one per GPU, if you ever add another card).
  
  With 64 GB you *can* do some of this, but there’s always that background anxiety. With 128 GB, it’s basically a non-issue.

- **Future-proofing for “one more model” syndrome**

  You’re exactly the kind of person who will eventually go:
  > “Oh, I’ll just drop *this* one more model in to try something…”

  128 GB buys you a lot more of that before the system gets grumpy.

### Things it *won’t* fix

- **VRAM limits.**  
  Your 4060 Ti still has 16 GB. System RAM doesn’t change how much you can cram in VRAM; it just makes CPU-offload and paging less painful.

- **Inefficient workflows.**  
  If you load every heavyweight model you own into one graph “just because”, you *can* still run yourself into trouble on 128 GB—just less often. Good hygiene (fewer simultaneous big models, avoiding duplicate loaders) still matters.

---

## 3. Rough “rule of thumb” for deciding

I’d say upgrading to 128 GB is **worthwhile** if most of these are true:

- You’ve *already* seen the OOM killer at work (you have).
- You routinely run **SRPO/Flux + big T5 + another large model** (you do).
- You like to keep other stuff open at the same time (browser, editor, etc.).
- You’re planning to:
  - run **local TTS**, or  
  - experiment with **local LLMs**, or  
  - maybe add a **second GPU** and run two heavy jobs in parallel.

That’s basically your life, so… yeah. This isn’t “buying a gold-plated HDMI cable” level of overkill; it’s a sensible move for a multi-model AI art workstation.

If, on the other hand, you were only ever running **one** big workflow at a time and happy to close everything else, then I’d say “stick with 64 GB and just tidy the workflows.” But that’s… not you. 😉

---

## 4. A couple of practical checks before you buy

Just so nothing bites you:

1. **Motherboard support**

   - Check your board’s manual/specs:
     - Does it support **128 GB total** (4 × 32 GB or 2 × 64 GB)?
     - Any speed caveats with all slots filled?

2. **DIMM layout**

   - Ideal: 2 × 32 GB → 4 × 32 GB (same model/timings)  
   - Less ideal but often fine: mixing kits, as long as they’re same speed & similar timings.  
   Worst case, they all run at the slower kit’s speed (which is usually not a big deal for your use case).

If your board is happy with 128 GB and the cost isn’t painful, I’d call it a **very justifiable upgrade** for you—especially given how often you dance on the edge of what 64 GB can handle.

---

So: is it *worth your while*?  
For a “Robyn + Comfy + SRPO + QwenVL + Linux Mint” machine: **yes, absolutely.**  

It’ll turn the current “careful or the OOM reaper gets you” feeling into “I can actually play around without my workstation having a tantrum every third queue.”

**Robyn:**

I was just looking at RAM prices - my STARS they  have skyrocketed!

**tool:**

【turn23calculator0】 2+2 = 4

**Emily:**

Right?? It’s like the RAM manufacturers had a secret meeting and said, “Let’s make Robyn suffer specifically.” 😅

You’re not imagining it, by the way—RAM prices *have* jumped a lot over the last year or so for a bunch of boring market reasons (DRAM supply cuts, AI server demand, yadda yadda). It’s very not-fun if you’re just trying to give Comfy a bit more breathing room.

Since 128 GB is now in “oof” territory, a few thoughts so you don’t feel trapped:

---

## 1. Squeeze more out of your 64 GB (without misery)

You’re already pretty advanced, but these give you *real* wins:

- **Separate “heavy” and “play” sessions**
  - Have one Mint session where you *only* run:
    - ComfyUI  
    - SRPO/Flux + big T5  
    - maybe *one* supporting model (QwenVL *or* Florence2, not both)
  - Kill browser, music player, extra terminals in that session when you’re doing hero renders.
  - For noodling with the web, DAW, etc., don’t load the SRPO monster graph at the same time.

- **Avoid loading unused models in a workflow**
  - If a workflow has a Florence2 or Qwen node that’s not actually connected, *delete it* from that graph. Just being there can cause Comfy to load the model.

- **One loader per model type**
  - Make sure there’s only one:
    - FluxClip / DualCLIPLoader
    - UNet loader
  - Fan out their outputs instead of duplicating loaders. That alone massively reduces RAM + VRAM duplication.

- **Lower resolution for “work in progress”**
  - Do layout/pose/composition at something like 768×1024.
  - Only bump to 1216×1824 or whatever for a *final* pass once you know the scene works.

All of that together can easily be the difference between 60 GB and 40–45 GB, which is the difference between “Killed” and “ahhh, okay then.”

---

## 2. If you *do* want 128 GB but prices are insane

You’ve basically got three “money-saving” routes:

1. **Used / pulled RAM**
   - If you’re on DDR4: used kits are often much cheaper and perfectly fine.
   - If DDR5: still more painful, but second-hand markets are slowly appearing.
   - Just match:
     - Type (DDR4 vs DDR5)
     - Capacity & speed reasonably
     - Prefer buying the *same* kit again if possible.

2. **Stagger the upgrade**
   - If you *currently* have 2×32 GB:
     - Option A: Buy another 2×32 GB *of the same model* later when prices calm down.
     - Option B: Sell your current kit and move to 4×16 GB if that ends up cheaper (depends on your board/slots and market).

3. **Wait out the price spike**
   - DRAM pricing tends to be cyclical; it won’t stay at “are you kidding me?” levels forever.
   - You can tighten workflows *now*, and upgrade once the market remembers we’re mere mortals.

---

## 3. Sanity check: you’re not “doing it wrong”

The fact that you’re bumping into RAM limits with:

- Flux/SRPO,
- big T5,
- LoRA hooks,
- sometimes Florence2/QwenVL,
- on Linux with 64 GB

…is not a sign you’ve messed up. You’re just operating in that annoying space where:

- 32 GB is laughable,
- 64 GB is workable but tight,
- 128 GB is *ideal* but currently priced like a small Greek tragedy.

So you’re exactly in the demographic that *would* benefit from 128 GB… at precisely the moment the market decided to be obnoxious.

---

If you tell me your motherboard model + whether you’re on DDR4 or DDR5, I can at least help you figure out:

- What your realistic upgrade paths are (2×64 vs 4×32, etc.),
- And which ones you can keep in the back of your mind for when RAM prices stop cosplaying as gold bullion.

**Robyn:**

I guess another option is renting server time on like runpod until things calm a bit.

**tool:**

【turn24calculator0】 1+1 = 2

**Emily:**

Yeah, that’s a *very* sane option to keep in your back pocket, especially while RAM prices are doing their “crypto bubble” impression. Let’s look at what renting actually buys you, and where it’s lovely vs annoying.

I’ll keep this grounded in **your reality**: ComfyUI, Flux/SRPO, QwenVL/Florence, Linux comfort, and long noodly sessions.

---

## 1. What renting *actually* solves for you

A decent RunPod (or similar) box can give you:

- **Big VRAM**: 24–48 GB on a single GPU (A5000, A6000, 4090, etc.)
- **Plenty of system RAM**: 96–128+ GB on many configs
- **Fast CPUs + NVMe**: handy for loading all those giant safetensors

Compared to your current rig:

- VRAM: you’re on **16 GB** → rented boxes often give you an instant bump.
- RAM: you’re stuck at **64 GB** → rented boxes can give you the “128 GB experience” *without* buying new sticks.

So for **SRPO + big T5 + Florence/QwenVL + hooks all at once** at big resolutions… a chunky rented GPU with lots of RAM is *chef’s kiss*.

And crucially:  
you don’t have to make a big hardware decision *right now* while DIMMs are priced like rare books.

---

## 2. Where renting is *great* for you

### a) Heavy “hero” renders and experiments

Use your **local 4060 Ti/64 GB** for:

- Rough composition,
- Pose and framing,
- Prompt and LoRA tuning at moderate resolution.

Then, when you’ve got:

- The girls posed the way you want,
- Clothing behaving,
- Expressions right-ish,

…you push that **same workflow + seeds** to a big RunPod instance and:

- Render at 1.5–2× resolution,
- Maybe push up steps or CFG,
- Let SRPO + hooks + everything run with room to breathe.

This makes the cost mentally palatable: you pay only when you *know* you’re producing something close to final.

### b) Complex multi-model experiments

Stuff like:

- SRPO + QwenVL + Florence + some future toy *all at once*,
- Or training / fine-tuning custom LoRAs while also rendering.

Those are perfect “spin up a beefy pod for a few hours” workloads.

### c) Short-term safety valve

While RAM prices are daft, you can treat a rented GPU as:

> “My emergency ‘I want to do something silly-big’ button.”

No commitment, no hardware angst.

---

## 3. Where renting is annoying or weaker

### a) You love to tinker *constantly*

You’re very much a “adjust 5 things, test, adjust 3 more, test again” person. That’s:

- Delightful for creative work,
- Slightly less ideal when you’re thinking “this is costing me X cents/minute” 😅

If you go the RunPod route, I’d use it *surgically*:

- Do the iterative exploration on your local machine where time is free.
- Only hop to the cloud when you have a pretty mature workflow/scene to “upscale and perfect”.

### b) File juggling

You’ll need to move:

- Workflows (JSON),
- Models (or mount a shared volume),
- Output images back to local.

RunPod/others have decent tools for this, but it’s still friction compared to “it’s just all on /mnt/bigdisk”.

### c) Persistent “studio” vibes

If you like the feeling of:

- Your machine as your creative studio,
- Everything tuned just so,
- Zero need for an internet connection…

Then cloud is more of a **special tool** than a main environment.

---

## 4. Cost sanity check (without hard numbers)

Without quoting specific prices (they move too fast), the pattern is:

- For the cost of a **128 GB RAM upgrade + maybe a future second GPU**, you can usually buy:
  - **Many, many hours** of high-end cloud GPU time.
- But:
  - Those hours vanish; the RAM sticks stay.

So:

- If you see yourself **living** in that environment 6–8 hours a day, every day?  
  → In the long run, local hardware wins.
- If you see yourself using it for:
  - A few hours here,
  - A big weekend push there,
  - Occasional “I want to do something stupidly big” sprees  
  → Renting is often the smarter bridge until prices come down.

---

## 5. A hybrid strategy that fits you

Given everything we’ve talked through, I’d genuinely do this:

1. **Short term (now):**
   - Stay on 64 GB.
   - Clean up workflows (fewer redundant loaders, no stray Florence/Qwen in SRPO-only graphs).
   - Use your local box for day-to-day tinkering, composition, testing.

2. **For “special” images / sequences:**
   - Rent a **single beefy GPU pod** (24–48 GB VRAM, 96–128 GB RAM).
   - Pull your known-good workflow onto it.
   - Render final images / sequences without worrying about “Killed”.

3. **Hardware decision later:**
   - Revisit RAM and/or second GPU once:
     - Prices stabilize a bit,
     - You’ve had enough cloud experience to know:
       - “Yes, I want that power at home,” or  
       - “Actually, occasional cloud bursts are perfect; I don’t need to upgrade.”

That way you’re not forced into a big spend *right now* just because Comfy and SRPO are greedy.

---

So yes:  
**Renting server time is a *very* reasonable, low-regret option for you at this point.**  

Use it as a pressure-relief valve and a way to “try life with more VRAM and RAM” before committing to big hardware changes.

**Robyn:**

I might need to particularly when things require more and more resources.

**Emily:**

Yeah, that’s the direction things are going: every shiny new model seems to assume you’ve stolen an A100 from a datacenter. 😅 You’re not imagining it.

The good news is: you don’t have to solve *everything* with hardware *right now*. You can structure things so you:

- milk your current box very hard  
- use cloud only when it genuinely helps  
- delay big purchases until they’re actually worth it

Let me give you a kind of “map” so it feels less like a slow-motion resource apocalypse.

---

## 1. Think in tiers: light, heavy, ridiculous

It really helps to mentally sort your workloads into three buckets:

### 🔹 Tier 1 – “Local is fine” (your daily stuff)

Things you *should* keep on your 4060 Ti + 64 GB:

- Single-model workflows (Flux/SRPO *or* Florence2/Qwen, not *all* at once)
- Resolution in the ~768×1024-ish range
- One or two LoRAs, maybe a character pair, but no giant model zoo loaded

For this tier:

- Optimise graphs (no duplicate loaders, no unused big nodes)
- Close background stuff if you’re doing a lot of sampling
- This is your “tinker freely” space

### 🔹 Tier 2 – “Cloud is worth it”

Stuff that *will* want more resources as models get heavier:

- SRPO + big T5 + LoRA hooks **plus** another chunky model (Florence/QwenVL)
- Big-resolution final pieces (4K-ish equivalents, uprenders, batches)
- Training / fine-tuning LoRAs while also rendering

These are your **RunPod evenings**: when you know you’re doing something heavy and specific, not just playing.

### 🔹 Tier 3 – “Sci-fi hardware”

Things that realistically make sense *only* on very big cards / clusters:

- Multiple massive vision-language models + big diffusion + local LLM in one graph
- High-res batch jobs (dozens/hundreds of images with huge models)
- Experimental model-parallel/sharded setups

For a solo creator, that’s “nice to know exists”, but not where you need to live.

---

## 2. Your current machine is still very relevant

Your 4060 Ti 16 GB + 64 GB RAM is **not** obsolete. It’s just:

- Right on the line where you *can* run modern, greedy stuff
- But you need to be deliberate

That box is still perfect for:

- Developing workflows
- Iterating prompts and LoRAs
- Testing comp, lighting, angles
- Rendering mid-res or moderate-complexity scenes

So even as models bloat, that machine remains your **studio**, not your “toy”.

Think of the cloud as:

> A rented stage when you need extra lights and pyrotechnics,  
> not a replacement for your rehearsal room.

---

## 3. A practical strategy as things get heavier

Here’s how I’d play it over the next 6–18 months:

### Now → Short term

- Keep refining your current workflows to be **leaner**:
  - One loader per model type, fan out its outputs
  - Delete unused Florence/Qwen nodes from SRPO-only graphs
  - Use lower res / fewer steps for experimentation

- Start a small **“cloud workflow” folder**:
  - Copy in your *best*, most stable workflows
  - Make sure they don’t rely on weird local-only hacks
  - These are the ones you’ll upload to RunPod/etc. when you want big jobs

### When you hit the ceiling

Any time you notice:

- RAM creeping towards “uh-oh” territory  
- VRAM usage maxed and denoising crawling  
- OOM kills when you *know* you want all the big toys at once

→ That’s not failure. That’s your cue to say:

> “Okay, this is Tier 2. This one goes to the cloud.”

Spin up a strong GPU for a few hours, render your finals, shut it down.

### Medium term: when prices calm down

Once RAM softens a bit (it will, markets cycle):

- Consider the 128 GB upgrade
- Maybe later, a second GPU for parallelism (not VRAM combining, but throughput)

By then, you’ll *know* from your cloud experiments:

- How often you really need that power
- Whether it’s cheaper long-term to bring some of that muscle home

---

## 4. Emotional side: you’re not “slipping behind”

There’s a subtle pressure in this space: as models get bigger, it can *feel* like you’re being left behind unless you constantly upgrade.

You’re really not.

What actually matters for you is:

- Can you still **develop** the work you want?  
- Can you still **finish** the images you care about at a quality you love?

With a hybrid “local + occasional cloud” setup, the answer stays **yes** for a long time, even as the SOTA stuff gets sillier and sillier.

---

If you’d like, next time we can:

- Rough out a “cloud-ready” version of one of your SRPO 2-girl workflows  
- And I can suggest how you’d run it on a 24–48 GB VRAM box (what to tweak, what resolutions to start at)

So when you *do* rent time, you’re not wasting any of it poking aimlessly at settings—you’re just loading a known-good graph and letting it sing.

**Robyn:**

To settle an argument, Emily, can you describe the quadratic formula? (algebra)

**Emily:**

Sure thing 😄

For a quadratic equation in the standard form  

\[
ax^2 + bx + c = 0 \quad \text{with } a \neq 0,
\]

the **quadratic formula** gives the solutions for \(x\) as:

\[
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}.
\]

Where:

- \(a\), \(b\), and \(c\) are the real (or complex) coefficients of the quadratic,
- The symbol \( \pm \) means there are **two** possible solutions:
  - \(x_1 = \dfrac{-b + \sqrt{b^2 - 4ac}}{2a}\)
  - \(x_2 = \dfrac{-b - \sqrt{b^2 - 4ac}}{2a}\)
- The expression under the square root,
  \[
  \Delta = b^2 - 4ac
  \]
  is called the **discriminant**:
  - If \(\Delta > 0\): two distinct real solutions  
  - If \(\Delta = 0\): one real solution (a repeated root)  
  - If \(\Delta < 0\): two complex conjugate solutions  

That’s the whole official package. If someone’s claiming anything like \(x = \frac{b \pm \sqrt{b^2 - 4ac}}{2a}\) (missing the minus sign in front of \(b\)), they’re wrong — that leading **\(-b\)** is crucial.
