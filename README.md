"""
🩸 BLOOD GHOST ZOMBIE — FINAL ULTIMATE FUSION EDITION v1.0
"Untuk orang yang kusayangi — selamanya dalam kode ini."
```
================================================================================
                               README.md
================================================================================
```
```
⚠️ DISCLAIMER
--------------
Tool ini dibuat untuk tujuan EDUKASI dan RISET KEAMANAN saja.
Penggunaan yang tidak bertanggung jawab sepenuhnya menjadi tanggung jawab pengguna.
Developer tidak bertanggung jawab atas penyalahgunaan, kerusakan sistem,
konsekuensi hukum, atau kehilangan data, pelajari dengan bijak sebelum menggunakan.

Gunakan HANYA pada sistem yang Anda miliki sendiri atau telah mendapat izin tertulis.
Sricpt ini di bawah lisensi zombie-vdp
```
```
⚠️ DISCLAIMER
--------------
Tool ini dibuat untuk tujuan EDUKASI dan RISET KEAMANAN saja.
Penggunaan yang tidak bertanggung jawab sepenuhnya menjadi tanggung jawab pengguna.
Developer tidak bertanggung jawab atas penyalahgunaan, kerusakan sistem,
konsekuensi hukum, atau kehilangan data, pelajari dengan bijak sebelum menggunakan.

Gunakan HANYA pada sistem yang Anda miliki sendiri atau telah mendapat izin tertulis.
Sricpt ini di bawah lisensi zombie-vdp
```
```
📁 STRUCTURE:
    ╔══════════════════════════════════════════════════════════════╗
    ║  SECTION 1  : IMPORTS & AUTO INSTALLER                                  ║
    ║  SECTION 2  : COLORAMA & LOGGING                                        ║
    ║  SECTION 3  : OS & DEVICE FINGERPRINTS                                  ║
    ║  SECTION 4  : LEGAL SCOPE GUARD                                   `     ║
    ║  SECTION 5  : CONFIGURATION                                             ║
    ║  SECTION 6  : IDENTITY SYSTEM                                           ║
    ║  SECTION 7  : DATABASE ENGINE                                           ║
    ║  SECTION 8  : DNA CLONER v2.0                                           ║
    ║  SECTION 9  : GHOST FLOOD v2.0                                          ║
    ║  SECTION 10 : WAF DETECTION                                             ║
    ║  SECTION 11 : SESSION MANAGER                                           ║
    ║  ⭐ SECTION 12 : PAYLOAD LIBRARY (ADD PATTERNS HERE)                    ║
    ║  SECTION 13 : RECON ENGINE                                              ║
    ║  SECTION 14 : DORKING ENGINE                                            ║
    ║  SECTION 15 : CRAWLER ENGINE                                            ║
    ║  SECTION 16 : VULNERABILITY SCANNERS                                    ║
    ║  SECTION 17 : SENSITIVE FILES SCANNER                                   ║
    ║  SECTION 18 : FUZZER ENGINE                                             ║
    ║  SECTION 19 : DEEP SCANNER                                              ║
    ║  SECTION 20 : FILTER PIPELINE                                           ║
    ║  SECTION 21 : MAIN ORCHESTRATOR                                         ║
    ║  SECTION 22 : ENTRY POINT                                               ║
    ╚══════════════════════════════════════════════════════════════╝
```
```
USAGE:
cd ~/Blood
python3 -m venv bloodghostblue_env
source bloodghostblue_env/bin/activate

# No-Root Mode — Semua fitur jalan, Ghost auto-disabled
python3 blood.py nasa.gov --fp-mode normal --rate 5.0 --deep --threads 2
```

```
🧬 OVERVIEW
--------------
Blood Ghost Zombie Fusion adalah framework bug bounty dan vulnerability
assessment otomatis dengan fitur lengkap untuk reconnaissance, scanning,
fuzzing, hingga pelaporan.
```
```
Target scope: domain bug bounty resmi (Google, NASA, HackerOne, Bugcrowd, dll).
```
```
🚀 FITUR UTAMA
--------------
| Modul                   | Deskripsi                                      |
|-------------------------|------------------------------------------------|
| Recon Engine            | crt.sh, Wayback, OTX, URLScan, DNS Brute       |
| Dorking Engine          | Bing, Yahoo, Yandex, DuckDuckGo, Brave         |
| Crawler Engine          | Crawling halaman + ekstrak URL internal        |
| Vulnerability Scanner   | XSS, SQLi, LFI, SSTI, SSRF, CMDI, Redirect,    |
|                         | CORS, Host Header, CRLF, IDOR                  |
| Fuzzer Engine           | Baseline-based fuzzing + anomaly detection     |
| Sensitive Files         | Deteksi file/endpoint sensitif                 |
| Deep Scanner            | Verifikasi findings dengan request kedua       |
| DNA Cloner v2.0         | Network device fingerprinting & cloning        |
| Ghost Flood             | Phantom device generator                       |
| Filter Pipeline Pro     | 5-stage false positive filter                  |
| Report Generator        | Output JSON, CSV, Markdown                     |
```
```
📋 PERSYARATAN SISTEM
--------------
- Python 3.8+
- OS: Linux, macOS, Windows (WSL direkomendasikan)
- Koneksi internet stabil
```
```
Dependencies (auto-install):
- aiohttp, colorama, beautifulsoup4, lxml, tldextract, requests
```
```
🔧 INSTALASI
--------------
  git clone https://github.com/pormes-90/Blood.git
  cd Blood
  pip install -r requirements.txt  # opsional, script auto-install
  python3 zombie.py <target>
```
```
🎮 PENGGUNAAN
--------------
  # Basic
  python3 blood.py nasa.gov

  # Stealth Mode
  python3 blood.py google.com --stealth --rate 3.5

  # Deep Scan
  python3 blood.py hackerone.com --deep --threads 8

  # Custom Output
  python3 blood.py bugcrowd.com --output ./reports

  # Disable Modules
  python3 blood.py example.com --no-dna --no-ghost --no-dork

  #Full Save
  python3 blood.py nasa.gov --fp-mode normal --rate 5.0 --deep --threads 2
```

OPTIONS:
  --stealth       Stealth mode (workers=2, rate=3.5)
  --deep          Deep scan mode (2x payloads, 2x workers)
  --rate <N>      Rate limit dalam detik (default: 2.0)
  --threads <N>   Jumlah workers (default: 5)
  --output <dir>  Output directory (default: ./fusion_results)
  --no-dna        Nonaktifkan DNA Cloner
  --no-ghost      Nonaktifkan Ghost Flood
  --no-dork       Nonaktifkan Dorking Engine
  --no-crawl      Nonaktifkan Crawler Engine
```
```
🏗️ ARSITEKTUR
--------------
BloodFusion (Orchestrator)
├── 🔐 Zombie Auth (password: bloodghost)
├── 🧬 DNA Cloner v2.0
│   ├── OUI MAC Generation (20 vendors)
│   ├── OS Fingerprinting (14 signatures)
│   ├── Port Probing (12 ports)
│   └── ARP Spoof Detection
├── 👻 Ghost Flood
│   ├── 7 Device Profiles
│   └── Phantom Generator
├── 🔍 Recon Engine
│   ├── crt.sh (Certificate Transparency)
│   ├── Wayback Machine (Internet Archive)
│   ├── AlienVault OTX (Passive DNS)
│   ├── URLScan.io
│   └── DNS Brute Force (50+ wordlist)
├── 🔎 Dorking Engine
│   ├── 5 Search Engines
│   ├── Smart Fallback
│   └── Early Stop (stall detection)
├── 🕷️ Crawler Engine
│   ├── Internal Link Extraction
│   └── Scope Filter
├── 💉 Vulnerability Scanners (11 types)
│   ├── XSS (Reflected)
│   ├── SQLi (Error + Time-based)
│   ├── LFI / Path Traversal
│   ├── SSTI (Jinja2, Freemarker, ERB, Pug)
│   ├── SSRF (Cloud Metadata)
│   ├── Command Injection
│   ├── Open Redirect
│   ├── CORS Misconfiguration
│   ├── Host Header Injection
│   ├── CRLF Injection
│   └── IDOR
├── 🧪 Fuzzer Engine
│   ├── Baseline Comparison
│   ├── Length Deviation
│   ├── Status Code Deviation
│   └── Error Keyword Detection
├── 📁 Sensitive Files Scanner
├── 🔬 Deep Scanner
├── 🛡️ Filter Pipeline Pro (5 Stages)
│   ├── Stage 1: Confidence ≥60%
│   ├── Stage 2: Immune Parameters (90+)
│   ├── Stage 3: Known FP Detection
│   ├── Stage 4: Quality Scoring (50-100)
│   └── Stage 5: Deduplication
└── 📊 Report Generator (JSON, CSV, MD)
```
```
🔐 KEAMANAN
- Anonymous identity + random User-Agent
```
```
🧬 DNA CLONER — OS FINGERPRINTS (14 signatures)
--------------
| OS                | Ports                          | TTL |
|-------------------|--------------------------------|-----|
| Windows 11        | 445,139,135,3389,5985,5986     | 128 |
| Windows 10        | 445,139,135,3389               | 128 |
| Windows Server    | 445,139,135,3389,1433,3306     | 128 |
| Ubuntu Desktop    | 22,111,631,5353                | 64  |
| Ubuntu Server     | 22,80,443,3306,5432            | 64  |
| macOS             | 22,548,5353,5900               | 64  |
| iOS               | 62078                          | 64  |
| Android           | 5555,8080                      | 64  |
| Cisco Router      | 22,23,80,443,161               | 255 |
| Printer           | 515,631,9100,161               | 64  |
| IoT Device        | 80,8080,23,554                 | 64  |
| VMware ESXi       | 22,80,443,902                  | 64  |
| Docker Host       | 22,2375,2376,80                | 64  |
| Kubernetes Node   | 22,6443,10250,10255            | 64  |
```
```
👻 GHOST FLOOD — DEVICE PROFILES
--------------
| Profile      | OS Examples                    | Distribution |
|--------------|--------------------------------|--------------|
| Workstation  | Windows 11/10, Ubuntu, macOS   | 30%          |
| Mobile       | Android 14, iOS 18, iPadOS     | 20%          |
| IoT          | Embedded Linux, Raspbian       | 15%          |
| Server       | Windows Server, Ubuntu Server  | 10%          |
| Network      | Cisco IOS, OpenWRT, pfSense    | 10%          |
| Printer      | Embedded Linux, Custom RTOS    | 8%           |
| VM           | VMware ESXi, Proxmox, Hyper-V  | 7%           |
```
```
🔎 DORKING ENGINE — SEARCH ENGINES
--------------
| Engine     | Method | Priority | Cooldown   |
|------------|--------|----------|------------|
| Bing       | GET    | 1        | 1.5-2.5s   |
| Yahoo      | GET    | 2        | 1.5-2.5s   |
| Yandex     | GET    | 3        | 2.0-3.0s   |
| DuckDuckGo | POST   | 4        | 2.0-3.5s   |
| Brave      | GET    | 5        | 2.5-4.0s   |
```
```
🛡️ FILTER PIPELINE — 5 STAGES
--------------
| Stage | Filter              | Description                           |
|-------|---------------------|---------------------------------------|
| 1     | Confidence Threshold | Remove <60% confidence                |
| 2     | Immune Parameters    | Remove safe params (90+ params)       |
| 3     | Known FP Detection   | Pattern-based false positive removal  |
| 4     | Quality Scoring      | Score 0-100 (6 factors)               |
| 5     | Deduplication        | Hash + URL/type dedup                 |
```
```
📊 OUTPUT FORMAT
--------------
fusion_results/
└── report_<target>_<timestamp>/
    ├── report.json      # Full JSON report
    ├── findings.csv     # CSV table
    └── README.md        # Human-readable report
```
```
🔄 ALUR KERJA (8 PHASES)
--------------
PHASE 1   🔍 RECONNAISSANCE    → Subdomain + URL discovery
PHASE 2   🧬 DNA CLONING       → Network device fingerprinting
PHASE 2.5 👻 GHOST FLOOD       → Phantom device generation
PHASE 3   🔎 DORKING           → Multi-engine search
PHASE 4   🕷️ CRAWLING          → Internal link extraction
PHASE 5   📁 SENSITIVE FILES   → Endpoint scanning
PHASE 6   💉 VULNERABILITY SCAN → 11 scan types + fuzzing
PHASE 7   🛡️ FP FILTER         → 5-stage pipeline
PHASE 8   🔬 DEEP VERIFICATION → Secondary request check
```
```
👤 IDENTITAS
--------------
- Hunter: Dikha Pormes
- Email: 418teapotbot@gmail.com
- Signal: BloodGhostZombie/Fusion-v3.0
- Anonymous Mode: Random identity rotation
```
````
📄 LISENSI
--------------
PROPRIETARY — ALL RIGHTS RESERVED
Hanya untuk ethical use: riset keamanan, bug bounty, pendidikan.
```
```
⭐ CREDITS
--------------
Dibuat oleh Dikha Pormes & 418teapot
"Untuk orang yang kusayangi — selamanya dalam kode ini."
```
```
================================================================================
                          END OF README.md
================================================================================
```
"""
