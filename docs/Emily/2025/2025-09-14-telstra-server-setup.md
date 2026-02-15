---
title: "Telstra server setup"
date: 2025-09-14
---

# Telstra server setup

**Robyn:**

Hi Emily. For this project I need you to put your Linux tech support hat on. Please think hard about your answers: I need them to be as accurate and detailed as possible. I want to create an internet-facing server. The OS needs to be a 'headless' hardened Linux-based server, preferably Debian-based as I am more familiar with APT than YUM. My challenges include: I connect to the internet using a Telstra FTTP Broadband account... I am not certain that Telstra supports internet-facing servers, hardened or otherwise. I see this as my initial hurtle. The next would be setting up the server, and making sure it is completely separate from all other internet connections. I would like to tackle these challenges first before embarking on anything further.

**Emily:**

Hi Robyn—Linux hat on. Let’s tackle the two big hurdles first: (1) whether Telstra FTTP will even let you run an internet-facing box, and (2) how to keep that server totally separate from the rest of your network.

# 1) Can you run an internet-facing server on Telstra FTTP?
**Short answer: yes, with options.**

- **Public IP / Static IP:** Telstra now offers a *static IPv4* add-on for home NBN/OptiComm for ~$10/month, which is ideal for hosting. You add it yourself in My Telstra. citeturn1search4  
- **Port forwarding:** Telstra documents port-forwarding on its modems, which implies inbound connections are supported. citeturn1search14  
- **CGNAT:** On *fixed-line* NBN, Telstra typically does **not** put you behind CGNAT (their *mobile* network is CGNAT). A Whirlpool mod confirms this common split. If you ever do encounter CGNAT, there are clean workarounds (below). citeturn1search10

**Feasibility checklist (10 minutes):**
1) From any device on your Telstra link:  
   `curl -4 ifconfig.co` and note the IP. Then check your router’s **WAN** IP. If they match (and it’s not RFC1918/100.64.0.0/10), you’re not behind CGNAT.  
2) If you don’t want to rely on Dynamic DNS, enable Telstra’s **Static IP** add-on. citeturn1search4  
3) Temporary inbound test: on your server `python3 -m http.server 8080`, create a port-forward 8080→server, then hit `http://<your-public-ip>:8080` from your phone on 4G. If it loads, you’re green.

> **Email hosting caution:** Even if port 25 isn’t filtered, deliverability is painful from residential IPs. Use a relay (Mailgun, Postmark, SES) and don’t expose 25/587 publicly unless you really must.

# 2) Keep the server *completely separate* from everything else
You’ve got three robust patterns; pick one based on budget and risk tolerance:

## A) **Physical isolation (best): second NBN service on another UNI-D port**
Order a **second** NBN service (can be Telstra or another ISP) on UNI-D 2/3/4 of the NBN FTTP NTD. Put a dedicated firewall + server behind it; nothing touches your home LAN. Telstra’s own guide notes that multiple UNI-D ports can be active. citeturn1search8  
**Sketch:**  
ONT(UNI-D1) → Home router/LAN  
ONT(UNI-D2) → Firewall #2 → Hardened server (public site)

Pros: Total blast-radius separation, clean IP reputation, simple mental model.  
Cons: A second monthly service.

## B) **Single service, *logical* isolation with VLAN/DMZ**
Keep your existing Telstra NBN service but introduce a proper firewall (OPNsense/pfSense/MikroTik) or a Linux router with `nftables`.  
- Create **VLAN 10 = LAN**, **VLAN 20 = DMZ** (server).  
- **Default deny** DMZ→LAN; allow only DMZ→Internet and *your admin IP* → server SSH.  
- Port-forward only 80/443 to the DMZ host.  
Pros: One service, low cost.  
Cons: Slightly more complex to get right; mistakes can bridge networks.

## C) **No inbound ports at all: Cloudflare Tunnel or Tailscale Funnel**
Your server dials **out** to the provider; they terminate TLS and route traffic back to you. Great if CGNAT ever appears or you don’t want to expose your home IP.  
- **Cloudflare Tunnel (cloudflared):** free, handles certs, DDoS, WAF; map `site.example.com` → local `127.0.0.1:8080`. citeturn0search13turn0search3  
- **Tailscale Funnel:** expose a local HTTP/TCP service publicly over HTTPS, toggleable per service. citeturn0search4turn0search14  
Pros: No NAT/port-forwarding, hides your IP, easy TLS.  
Cons: You depend on a third-party edge; some self-hosters prefer direct control.

---

# 3) Headless, hardened **Debian 12** (APT-friendly) baseline
Use this once you’ve picked A/B/C.

**Install & users**
- Minimal install, **OpenSSH server**, no desktop.  
- Create admin user, `sudo` only; leave root password blank or lock it: `sudo passwd -l root`.

**SSH hardening (`/etc/ssh/sshd_config`)**
```
Port 22
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AllowUsers <youruser>
```
Then: `sudo systemctl reload ssh`.

**Firewall (UFW over nftables)**
```
sudo apt update && sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
# If you’ll admin over Tailscale (recommended):
# sudo ufw allow in on tailscale0 to any port 22 proto tcp
# Otherwise, from your static admin IP only:
# sudo ufw allow from <your-admin-ip>/32 to any port 22 proto tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

**Auto-patching & basics**
```
sudo apt install unattended-upgrades fail2ban needrestart chrony apparmor apparmor-utils
sudo dpkg-reconfigure --priority=low unattended-upgrades
```
- `fail2ban` with the stock `sshd` jail is fine to start.  
- Keep **AppArmor** enforcing; avoid random “disable apparmor” blog advice.

**Optional but excellent**
- **Tailscale** for admin: lock SSH to `tailscale0` only.  
- **Caddy** or **Nginx** as reverse proxy. If you’re not using Cloudflare Tunnel/Tailscale Funnel, let Caddy handle Let’s Encrypt automatically.  
- **Backups:** `restic` to Backblaze B2/Object Storage; test restores quarterly.  
- **Monitoring:** `uptime-kuma` or just a remote `systemd` watchdog + `logwatch`.

**IPv6**
If Telstra assigns IPv6, be sure your firewall has **matching v6 rules** (UFW handles both if you `set ipv6=yes`). If you don’t want IPv6 exposure yet, disable it server-side until you’re ready.

---

# 4) A concrete “first week” plan
**Day 1–2: feasibility & isolation choice**
1) Run the **public IP/CGNAT** test above.  
2) Decide: **A (second UNI-D)**, **B (VLAN/DMZ)**, or **C (Tunnel)**.  
3) If hosting directly, enable **Static IP** in My Telstra. citeturn1search4

**Day 3–4: network build**
- **A:** Order second service on UNI-D2; plug a small firewall (OPNsense box) → server. citeturn1search8  
- **B:** Introduce firewall, create VLANs, move server into DMZ; set strict rules.  
- **C:** Install **cloudflared** or **tailscale**; create the tunnel/funnel mapping. citeturn0search13turn0search4

**Day 5–7: server hardening & smoke tests**
- Install Debian 12 headless; apply SSH/UFW/fail2ban/unattended-upgrades.  
- Reverse proxy + TLS (Caddy), or rely on Tunnel/Funnel TLS.  
- Probe from outside: `curl -I https://your-domain/` on mobile data; watch logs; load test lightly.

---

## Quick answers to your initial concerns
- **“Does Telstra allow it?”** There’s no current Telstra doc forbidding self-hosting, and they actively document port-forwarding and sell a Static IP add-on for NBN—both are signs they expect inbound hosting use-cases. citeturn1search14turn1search4  
- **“Full separation from my other internet connections?”** The cleanest path is **a second service on another UNI-D port** (true physical separation). Logical isolation with VLAN/DMZ is also strong if done carefully. citeturn1search8  
- **“What if CGNAT pops up?”** Use **Cloudflare Tunnel** or **Tailscale Funnel**—no inbound ports, public HTTPS, and you keep your home IP private. citeturn0search13turn0search4

If you want, I can sketch a DMZ ruleset (OPNsense or plain `nftables`) and a minimal Caddy reverse-proxy config for Debian next.

**Robyn:**

I'm going to take this step by step, doing your checklist. I'll let you know if I run into issues, thanks Emily. Going to check on that Static IP add-on for NBN thing first.

**Emily:**

Perfect—great first step. Here’s a tight checklist just for the **Static IP add-on** so you can verify and enable it quickly:

## How to check/enable Telstra Static IP (NBN/OptiComm)
1) **Open My Telstra → Services →** select your **Home Internet** service → **Extras → Add static IP address**. It’s listed at **$10/month** for consumer NBN and **$0** on business NBN. Follow the prompts to confirm. citeturn0search0turn0search5

2) **Renew the WAN lease** after enabling (quick modem/router reboot is fine). Telstra’s static IP is normally delivered by DHCP reservation—no manual IP entry needed on your router. citeturn1search3

3) **Verify you’ve got it:**
   - From any device on your Telstra link: `curl -4 ifconfig.co` (or visit any “what’s my IP” page) and note the IPv4.
   - Check your router’s **WAN IP**—they should match and remain the same across a reboot.  
   - If you don’t see the add-on in My Telstra or it won’t stick, it’s worth contacting Telstra, as the add-on **is** officially offered for home NBN. citeturn0search0

### Two small gotchas (so you’re not blindsided)
- **Reverse DNS (PTR):** On consumer static IPs, changing PTR is typically not self-service (that’s a Telstra Business feature). If you plan to run an SMTP server, use a reputable relay instead. citeturn1search7turn1search12  
- **4G/5G Mobile Backup:** If your modem fails over to mobile backup, inbound hosting will stop working (mobile paths sit behind carrier NAT / inbound filtering). You’ll see “mobile backup” indicated on the modem/My Telstra. Hosting resumes once you’re back on fixed-line. citeturn2search0turn3search13

If you want, once you’ve confirmed the static IP is active, I’ll give you a minimal, hardened Debian 12 + UFW + Fail2ban + Caddy template and (if you prefer) a quick DMZ/VLAN sketch.
