---
title: "File server options comparison"
date: 2025-09-15
---

# File server options comparison

**Robyn:**

Hi Emily. Quick question about online file servers: I need to be able to create a link to a video file on a page, and have that video play. Can Google Drive serve as that sort of file server? If not, are there low-cost online services that do this?

**Emily:**

Hey Robyn! Short answer: Google Drive isn’t great for this.

Drive will *preview* a video in its own player (you can iframe the preview), but it doesn’t reliably give you a clean, CORS-friendly file URL you can drop into `<video src="...">`. It’s also subject to unpredictable “too many users have viewed or downloaded this file recently” lockouts that can last ~24 hours—bad for public embeds. citeturn1search1turn1search14

Here are low-cost options that *do* work well:

- **Cloudflare Stream** — full video hosting/encoding + an embed player or HLS/DASH URLs. Simple pricing: **$5 per 1,000 minutes stored** and **$1 per 1,000 minutes delivered**, egress included. Solid for reliably embedded playback without you managing storage/CDN. citeturn2view0

- **Bunny Stream** — very cheap and simple: **storage from $0.01/GB** and **delivery from $0.005/GB** with a **$1/mo minimum**, includes player and transcoding. Great bang-for-buck if you’re cost-sensitive. citeturn3view0

- **Backblaze B2 + Cloudflare CDN (DIY)** — host MP4s in B2 (**$6/TB/month**), put Cloudflare in front. You get **free egress up to 3× your stored data** (and zero-cost egress when served through Cloudflare thanks to the Bandwidth Alliance). You’ll handle encoding yourself, but it’s very economical for simple `<video>` playback. citeturn6view0turn4search19turn4search17

- **Vimeo / YouTube** — easy embeds. YouTube (unlisted) is free but branded; Vimeo is cleaner but paid tiers vary, and the free plan now only allows **1 GB total lifetime uploads**, so it’s not viable for ongoing hosting. citeturn5search13turn5search1

### If you want your own `<video>` tag
Encode H.264/AAC MP4, set correct `Content-Type: video/mp4`, enable CORS on the bucket/CDN, and then:

```html
<video controls preload="metadata" width="800"
       src="https://cdn.yourdomain.com/videos/clip.mp4" type="video/mp4">
  Sorry, your browser can’t play this video.
</video>
```

If you’d like, tell me roughly how many minutes you’ll host and typical monthly watch-time, and I’ll run quick cost comparisons between Stream, Bunny, and B2+Cloudflare and sketch the setup steps you’d follow for each.

**Robyn:**

Thanks, Emily. I doubt I have much more than 3 or 4 gig of video, to be honest. At this stage, Cloudflare Stream looks quite interesting. However, there are some terms I don't understand. What is embedded playback? Also, "egress"... not sure what that is.

**Emily:**

Great question!

**Embedded playback**  
That just means you place a tiny snippet on your page (usually an `<iframe>` or JS player) and the vendor’s player does the work—streaming the right formats (HLS/DASH), adaptive bitrate, captions, poster image, etc. With **Cloudflare Stream**, you drop in an embed like:

```html
<iframe src="https://customer-<CODE>.cloudflarestream.com/<VIDEO_UID>/iframe"
        allowfullscreen style="border:none;width:100%;height:480px"></iframe>
```

…and you’re done—no raw file URL needed, and it plays on phones/desktops reliably. citeturn0search2turn0search14

**Egress**  
“Egress” is outbound data transfer—i.e., bytes leaving the provider to viewers’ browsers. Many services bill egress per GB; it’s why video/CDN bills can spike. Cloudflare Stream’s pricing rolls bandwidth into “minutes delivered,” so there are **no separate egress fees** on top of playback minutes. citeturn0search4turn0search0turn0search12

### What this means for you
- If you have **3–4 GB** of video total: at a typical 1080p bitrate (~5 Mb/s), that’s roughly **86–115 minutes** of content.  
- **Cloudflare Stream** prices: **$5 per 1,000 minutes stored** (prepaid) and **$1 per 1,000 minutes delivered**. So storing ~100 minutes is about **$0.50/month**; if viewers watch a combined **300 minutes** in a month, playback is **$0.30**. (Encoding & ingress are free.) citeturn0search0turn0search6

### When to use embedded playback vs a raw file
- **Use embedded (Stream/Vimeo/YouTube)** when you want plug-and-play reliability, adaptive streaming, captions, and fewer MIME/CORS headaches. citeturn0search2  
- **Use a raw `<video src="...">`** only if you’re self-hosting and comfortable managing MP4 encoding, CORS, correct `Content-Type`, and a CDN.

If you’d like, I can jot down the exact step-by-step to get your first video live in Cloudflare Stream (upload → copy embed → paste into your page) and a minimal HTML sample you can drop into your site.

**Robyn:**

Silly question: in the case of the Cloudflare Stream solution (which is looking better and better), where are the video files actually stored?

**Emily:**

Not silly at all—good question!

With **Cloudflare Stream**, your videos live in **Cloudflare’s own managed storage**, not in a bucket you manage. You upload via the Stream dashboard/API, Stream **stores the original**, **encodes multiple renditions** (HLS/DASH), and serves them from Cloudflare’s global network (cached across their 300+ data centers). You don’t even need a domain to use it. citeturn1search10turn0search13turn0search9turn0search16

If you ever need a file back (e.g., an MP4 or just the audio), Stream also provides **download endpoints** for the processed files. citeturn1search0

If you specifically wanted to “own” the storage as raw objects, that’d be a different setup (e.g., Cloudflare **R2** + a player/CDN), but that’s not how Stream works by default—it’s fully managed. citeturn1search8

Happy to sketch both approaches (Stream vs. DIY R2) if you’d like a side-by-side.

**Robyn:**

Yes please, that would make things perfectly clear, Emily.

**Emily:**

Got you, Robyn — here’s a clear side-by-side.

# Cloudflare Stream (fully-managed video)
**What it is:** You upload a file; Stream stores the source, transcodes to adaptive HLS/DASH, and serves it worldwide with an embed player or raw manifests. You don’t manage storage buckets, CORS, or bitrates. citeturn6search2

**How it’s billed:**  
- **$5 per 1,000 minutes stored** (prepaid, based on *duration*, not file size).  
- **$1 per 1,000 minutes delivered** (playback minutes; bandwidth/egress already included). Ingest and encoding are free. citeturn1view0

**Your size (3–4 GB) in practice:** ~**86–115 minutes** at a typical 1080p bitrate. Rough monthly: store ~100 min ⇒ **~$0.50**; if viewers watch a combined 300 min ⇒ **~$0.30** for delivery. (Exact cost scales with actual minutes.) citeturn1view0

**Embed on a page (copy-paste):**
```html
<iframe src="https://customer-<CODE>.cloudflarestream.com/<VIDEO_UID>/iframe"
        allowfullscreen style="border:none;width:100%;max-width:800px;height:450px"></iframe>
```
(That’s the official player; you can also use HLS/DASH URLs in your own player.) citeturn2view0turn6search1

**Access control:** toggle **signed URLs/tokens** to lock playback to your site/users. citeturn3view0

**Downloads (optional):** generate downloadable MP4/M4A versions; billed as delivered minutes, no extra storage. citeturn6search0

**Best for you if:** you want the simplest, most robust path (transcoding + adaptive streaming + analytics + easy embeds) without touching storage/CORS.

---

# DIY on Cloudflare R2 (+ your player)
**What it is:** Raw object storage (S3-compatible) with **no egress fees**. You upload MP4s or your own HLS renditions and serve from a custom domain via Cloudflare. You handle encoding, MIME types, and CORS. citeturn4view0

**How it’s billed:** storage **$0.015/GB-mo** + request costs; **egress is free**. (Free tier: 10 GB storage, 1M Class-A + 10M Class-B ops/month.) citeturn4view0

**What you must do:**
1. **Public access & custom domain:** connect `cdn.yourdomain.com` to the bucket. citeturn5search0turn5search14  
2. **Set proper headers:** upload with **Content-Type: video/mp4** (or HLS types) and any Cache-Control you want. citeturn5search1  
3. **Enable CORS** (so your site can fetch from the bucket). citeturn0search3  
4. **Decide delivery format:**
   - **Simple MP4** (progressive). Easiest, but no adaptive bitrates.  
   - **HLS**: you pre-encode (e.g., ffmpeg) `.m3u8 + .ts` (or fMP4) and upload the whole ladder; play with hls.js/Video.js. citeturn5search2turn5search5

**Minimal examples:**

*Progressive MP4*  
```html
<video controls preload="metadata" width="800"
  src="https://cdn.yourdomain.com/videos/clip.mp4" type="video/mp4"></video>
```

*HLS with your own player (browser fallback via hls.js)*  
```html
<video id="v" controls width="800"></video>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<script>
if (Hls.isSupported()) {
  const hls = new Hls();
  hls.loadSource('https://cdn.yourdomain.com/hls/clip.m3u8');
  hls.attachMedia(document.getElementById('v'));
} else {
  document.getElementById('v').src = 'https://cdn.yourdomain.com/hls/clip.m3u8';
}
</script>
```
citeturn6search7

**Gotchas:** you do the encoding ladder yourself; ensure correct CORS; make sure Range requests work (they do); and test from multiple regions. citeturn0search3turn5search7

**Best for you if:** you want rock-bottom storage costs, a custom domain URL for the files, and don’t mind owning the encode/CORS/player bits.

---

## Quick recommendation for your case
With only ~100 minutes of content, **Cloudflare Stream** is likely the least effort and still very inexpensive. Paste the embed and you’re done; no CORS or player headaches, and adaptive streaming “just works.” If you later want raw files under your domain, keep **R2** in mind — you can always move/dual-host since R2 egress is free. citeturn1view0turn4view0

If you want, I’ll drop a 5-step “first upload to Stream” checklist and a parallel “R2 (HLS) setup” checklist you can follow line-by-line.

**Robyn:**

I think I'm going to go with the Cloudflare Stream option, Emily.

**Emily:**

Excellent choice. Here’s a tight, “do-this-then-that” for **Cloudflare Stream** plus a few smart options you can switch on later.

# Quick start (dashboard only)
1) **Upload**: Cloudflare Dashboard → *Stream* → *Videos* → *Upload*. (Drag–drop is fine.) citeturn0search0  
2) **Embed**: Open the video → *Embed & Links* → copy the player iframe and paste into your page:
```html
<div style="position:relative;padding-top:56.25%">
  <iframe src="https://customer-<CODE>.cloudflarestream.com/<VIDEO_UID>/iframe"
          allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture"
          allowfullscreen
          style="border:none;position:absolute;inset:0;width:100%;height:100%"></iframe>
</div>
```
That’s it—adaptive streaming, codecs, CDN, the lot. citeturn1search9

3) **(Optional) Use your own player**: If you prefer `<video>` with hls.js/Shaka, copy the **HLS or DASH manifest URL** from the video’s *Settings*. citeturn0search3

# Nice polish (flip on when ready)
- **Poster / thumbnail**: Add a poster frame (or animated GIF) via a special thumbnail URL. Example format is shown in the docs; you can pass `time=`, `height=`, etc. citeturn1search0turn1search13  
- **Captions/Subtitles**: Upload VTTs (multiple languages supported). The Stream player exposes a language menu automatically. citeturn0search4  
- **Analytics**: Views, watch-time, geography—available in Dash and via GraphQL if you want to pull reports. citeturn2search1turn2search3

# Lock it down (if you don’t want public URLs)
- **Signed URLs / tokens**: Mark a video as “require signed URL,” create a signing key, then your server issues short-lived tokens for embed/manifest URLs. Works with the iframe or custom players. citeturn0search2turn0search9

# Autoplay reality check
Browsers generally block **autoplay with sound**; autoplay works if **muted** (users can unmute). Plan UI accordingly. citeturn2search0turn2search6

# Cost sanity check for your library
You said **~3–4 GB** total. At a typical 1080p bitrate (~5 Mb/s) that’s roughly **~80–107 minutes** of content. Stream bills **$5 per 1,000 minutes stored** and **$1 per 1,000 minutes delivered**:  
- Storage for ~100 min ≈ **$0.50/month**  
- Delivery: 300 total watch-minutes in a month ≈ **$0.30**; 1,000 ≈ **$1**. (Ingest/encoding included.) citeturn0search1turn0search8

---

If you want, I can tailor a tiny **HTML snippet with a poster + captions + privacy token** once you have your `<VIDEO_UID>` (and I’ll include a one-liner Node/Python example to mint the signed token).

**Robyn:**

That would be lovely - thank you, Emily.

**Emily:**

Perfect — here’s a **ready-to-paste embed** plus **token generators** in Node and Python. I’ve used placeholders you can swap in.

# 1) Minimal HTML (Stream iframe + custom poster + privacy token)
```html
<!-- Replace the ALL_CAPS placeholders before using -->
<div style="position:relative;padding-top:56.25%">
  <iframe
    src="https://customer-CUSTOMER_CODE.cloudflarestream.com/SIGNED_TOKEN/iframe
         ?poster=https%3A%2F%2Fcustomer-CUSTOMER_CODE.cloudflarestream.com%2FSIGNED_TOKEN%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D5s%26height%3D720"
    allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
    allowfullscreen
    style="border:none;position:absolute;inset:0;width:100%;height:100%">
  </iframe>
</div>
```

- **`SIGNED_TOKEN`** replaces the usual `<VIDEO_UID>` *everywhere* (iframe path **and** poster URL) when the video requires signed URLs. That’s exactly how Stream secures private videos. citeturn2view0  
- The `poster=` parameter points to a Stream **thumbnail endpoint**; you can change `time=` and `height=` to taste. If your video requires signed URLs, pass the **signed token path** in that poster URL too (as shown). citeturn1view0  
- **Captions:** once you upload WebVTT tracks to the video (see §3 below), the Stream player auto-shows a captions menu—no extra HTML needed. citeturn5view0

---

# 2) Create a signing key (one-time)
Run once to get your **key ID** and **private key** for minting tokens:

```bash
curl -X POST \
  -H "Authorization: Bearer <API_TOKEN>" \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/keys"
# → Save the returned key "id" and PEM/JWK (shown only once)
```

You’ll use that key to sign JWT tokens locally (no per-view API call needed). citeturn4view0

---

# 3) Add captions (WebVTT)
Upload a caption file (e.g., English) in BCP-47 code `en` or `en-AU`:

```bash
curl -X PUT \
  -H "Authorization: Bearer <API_TOKEN>" \
  -F file=@/path/to/subtitles.en.vtt \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/<VIDEO_UID>/captions/en-AU"
```

After this, the built-in player exposes a captions toggle automatically. (You can also auto-generate captions from the API if you prefer.) citeturn5view0

---

# 4) Make the video private (require signed URLs)
Flip this on for the video so only tokenised URLs work:

```bash
curl -X PATCH \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"requireSignedURLs": true}' \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/<VIDEO_UID>"
```

From then on, **replace `<VIDEO_UID>` with `SIGNED_TOKEN`** in the iframe/manifest/thumbnail URLs. citeturn2view0

---

# 5) Mint the `SIGNED_TOKEN`

### Option A — Node.js (using `jsonwebtoken`)
```js
// npm i jsonwebtoken
const jwt = require("jsonwebtoken");
const fs = require("fs");

// ---- Fill these in ----
const VIDEO_UID = "YOUR_VIDEO_UID";
const KEY_ID = "YOUR_STREAM_KEY_ID";            // from /stream/keys
const PRIVATE_KEY_PEM = fs.readFileSync("./stream-private-key.pem", "utf8");
// ------------------------

const token = jwt.sign(
  // payload
  {
    sub: VIDEO_UID,                  // which video this token grants access to
    exp: Math.floor(Date.now()/1000) + 60*60, // expires in 60 min (max 24h)
    // Optional: restrict by country/IP or allow downloads:
    // downloadable: true,
    // accessRules: [{ type: "ip.geoip.country", action: "block", country: ["US","MX"] }]
  },
  PRIVATE_KEY_PEM,
  {
    algorithm: "RS256",
    header: { kid: KEY_ID }          // key ID in JWT header
  }
);

console.log(token);
```

### Option B — Python (using `PyJWT`)
```python
# pip install pyjwt
import jwt, time

VIDEO_UID = "YOUR_VIDEO_UID"
KEY_ID = "YOUR_STREAM_KEY_ID"
PRIVATE_KEY_PEM = open("stream-private-key.pem","r").read()

payload = {
    "sub": VIDEO_UID,
    "exp": int(time.time()) + 60*60,  # 60 minutes
    # "downloadable": True,
    # "accessRules": [{"type":"ip.geoip.country","action":"allow","country":["AU"]}]
}

token = jwt.encode(payload, PRIVATE_KEY_PEM, algorithm="RS256", headers={"kid": KEY_ID})
print(token)
```

Use the printed token in the iframe/manifest URL (as in section **1**). These claims/headers match Stream’s **signed URL** spec (RS256, `kid` header, `sub` = video UID, `exp` ≤ 24h), and you can add geoblocking or download permissions via `accessRules` / `downloadable`. citeturn4view0turn4view0

---

## Handy references
- **Signed URLs / tokens** (how tokens replace the UID in iframe/manifest; claims you can set). citeturn2view0  
- **Posters/thumbnails** (using the `poster=` param and thumbnail endpoints). citeturn1view0  
- **Captions** (upload/generate WebVTT with BCP-47 language tags). citeturn5view0

If you want, tell me your **customer code** (the `customer-XXXX` bit) and I’ll fill these placeholders exactly, including a ready-to-paste snippet with your token emitted from your preferred language.

**Robyn:**

Okay, here's my customer code:

customer-ze4n45l8rqsb9yse.cloudflarestream.com

and here's the Video ID I want to create a 'player' for on my Cloudflare Projects page:

f16255e78c021b7a0e5fae66ae554133

**Emily:**

Perfect—here are copy-paste snippets using **your** customer code and **that** video.

---

# 1) Quick public embed (no token)
> Works if the video **does not** require signed URLs yet.
```html
<!-- Public embed for f16255e78c021b7a0e5fae66ae554133 -->
<div style="position:relative;padding-top:56.25%">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/iframe
         ?poster=https%3A%2F%2Fcustomer-ze4n45l8rqsb9yse.cloudflarestream.com%2Ff16255e78c021b7a0e5fae66ae554133%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D5s%26height%3D720"
    allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
    allowfullscreen
    style="border:none;position:absolute;inset:0;width:100%;height:100%">
  </iframe>
</div>
```

Poster frame shows the 5-second mark at 720px height. Change `time=` and `height=` as you like.

---

# 2) Make it private (require signed URLs)
Flip privacy on for this exact video (run once):
```bash
curl -X PATCH \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"requireSignedURLs": true}' \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/f16255e78c021b7a0e5fae66ae554133"
```

---

# 3) Signed embed (replace UID with a token)
Once privacy is on, **replace the UID with a short-lived signed token** everywhere (iframe path and poster URL):

```html
<!-- Secure embed: paste your generated SIGNED_TOKEN below -->
<div style="position:relative;padding-top:56.25%">
  <iframe
    src="https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/SIGNED_TOKEN/iframe
         ?poster=https%3A%2F%2Fcustomer-ze4n45l8rqsb9yse.cloudflarestream.com%2FSIGNED_TOKEN%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D5s%26height%3D720"
    allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
    allowfullscreen
    style="border:none;position:absolute;inset:0;width:100%;height:100%">
  </iframe>
</div>
```

> You’ll generate `SIGNED_TOKEN` with the code below.  
> Token expiry can be up to **24h**; I recommend 30–60 minutes.

---

# 4) Create a Stream signing key (one-time)
```bash
curl -X POST \
  -H "Authorization: Bearer <API_TOKEN>" \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/keys"
# Save the returned key "id" (KEY_ID) and the private key (PEM) securely.
```

---

# 5) Mint the token

### Option A — Node.js (jsonwebtoken)
```js
// npm i jsonwebtoken
const jwt = require("jsonwebtoken");
const fs = require("fs");

// --- Fill these with your values ---
const VIDEO_UID = "f16255e78c021b7a0e5fae66ae554133";
const KEY_ID = "YOUR_STREAM_KEY_ID";                 // from /stream/keys
const PRIVATE_KEY_PEM = fs.readFileSync("./stream-private-key.pem", "utf8");
// -----------------------------------

const token = jwt.sign(
  {
    sub: VIDEO_UID,                                   // which video
    exp: Math.floor(Date.now()/1000) + 60*60,         // 60 min
    // Optional extras:
    // downloadable: true,
    // accessRules: [{ type: "ip.geoip.country", action: "allow", country: ["AU"] }]
  },
  PRIVATE_KEY_PEM,
  { algorithm: "RS256", header: { kid: KEY_ID } }
);

console.log(token); // <- paste this as SIGNED_TOKEN in the iframe URL
```

### Option B — Python (PyJWT)
```python
# pip install pyjwt
import jwt, time

VIDEO_UID = "f16255e78c021b7a0e5fae66ae554133"
KEY_ID = "YOUR_STREAM_KEY_ID"  # from /stream/keys
PRIVATE_KEY_PEM = open("stream-private-key.pem","r").read()

payload = {
    "sub": VIDEO_UID,
    "exp": int(time.time()) + 60*60,  # 60 minutes
    # "downloadable": True,
    # "accessRules": [{"type":"ip.geoip.country","action":"allow","country":["AU"]}]
}

token = jwt.encode(payload, PRIVATE_KEY_PEM, algorithm="RS256", headers={"kid": KEY_ID})
print(token)  # <- paste as SIGNED_TOKEN
```

---

## (Optional) Use your own player instead of the iframe
You can feed HLS/DASH manifests to `hls.js`/Shaka:

- **Public (no token):**  
  `https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/manifest/video.m3u8`  
  `https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/f16255e78c021b7a0e5fae66ae554133/manifest/video.mpd`

- **Private (signed):** replace the UID with your `SIGNED_TOKEN`:  
  `https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/SIGNED_TOKEN/manifest/video.m3u8`

Minimal HLS example:
```html
<video id="v" controls playsinline style="max-width:800px;width:100%"></video>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<script>
  const src = "https://customer-ze4n45l8rqsb9yse.cloudflarestream.com/SIGNED_TOKEN/manifest/video.m3u8";
  const video = document.getElementById("v");
  if (Hls.isSupported()) {
    const hls = new Hls(); hls.loadSource(src); hls.attachMedia(video);
  } else {
    video.src = src; // Safari/iOS can play HLS natively
  }
</script>
```

---

If you’d like, send me the **KEY_ID** once you’ve created it and I’ll drop back a finished HTML block with your first real token in place (no secrets shared—just the public token string that expires).
