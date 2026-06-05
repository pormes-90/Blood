🔴 MODE OPERASI LENGKAP

```bash
# ═══════════════════════════════════════════════════════════════
# 1. MODE NO-ROOT (DEFAULT) — Buat Bug Bounty Normal
# ═══════════════════════════════════════════════════════════════
# Tidak butuh root, semua scanner web berfungsi penuh
# Ghost modules auto-disabled

python3 blood.py target.com
python3 blood.py target.com --fp-mode aggressive
python3 blood.py target.com --deep --threads 10
python3 blood.py target.com --scope "*.target.com,api.target.com"


# ═══════════════════════════════════════════════════════════════
# 2. MODE ROOT — Full Power + Ghost Modules + Network Attacks
# ═══════════════════════════════════════════════════════════════
# Harus dijalankan dengan sudo
# Semua module aktif termasuk: Quantum Noise, Ghost Flood, 
# Dimensional Shift, Echo Locator, DNA Cloning, Mirror Mode

sudo python3 blood.py target.com --root-mode
sudo python3 blood.py target.com --root-mode --deep --ghost-all
sudo python3 blood.py target.com --root-mode --ghost-quantum --ghost-flood
sudo python3 blood.py target.com --root-mode --interface eth0 --target-network 192.168.1.0/24


# ═══════════════════════════════════════════════════════════════
# 3. MODE STEALTH — Ultra Slow Evasion (No-Root / Root)
# ═══════════════════════════════════════════════════════════════
# Rate sangat pelan, random delay, rotasi User-Agent
# Cocok untuk target yang punya WAF ketat

python3 blood.py target.com --stealth
sudo python3 blood.py target.com --stealth --root-mode


# ═══════════════════════════════════════════════════════════════
# 4. MENGGUNAKAN CONFIG YAML
# ═══════════════════════════════════════════════════════════════

python3 blood.py --config config.yaml
python3 blood.py --config config.yaml --target target.com
python3 blood.py --config config.yaml --target target.com --root-mode
```

---

📄 CONFIG YAML — config.yaml

```yaml
# ═══════════════════════════════════════════════════════════════
# BLOOD GHOST BLUE — CONFIGURATION FILE
# ═══════════════════════════════════════════════════════════════
# Letakkan di folder yang sama dengan blood.py
# Gunakan: python3 blood.py --config config.yaml
# Atau: python3 blood.py --config config.yaml --target target.com
# ═══════════════════════════════════════════════════════════════

# ─── Hunter Identity ──────────────────────────────────────
hunter:
  name: "418teapot"
  email: "418teapotbot@gmail.com"
  signal: "BloodGhostBlue/4.0"

# ─── Target Configuration ─────────────────────────────────
targets:
  # - target1.com
  # - target2.com
  # Biarkan kosong jika menggunakan --target dari CLI

# ─── Output Settings ──────────────────────────────────────
output:
  directory: "./bounty_results"
  database: "bounty_hunter.db"
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR

# ─── Performance ──────────────────────────────────────────
performance:
  workers: 5           # Concurrent threads
  rate_limit: 2.0      # Requests per second
  timeout: 15          # Request timeout (seconds)
  max_retries: 2       # Retry failed requests
  max_urls: 1000       # Max URLs to scan per target
  max_depth: 3         # Crawl depth

# ─── Scope Control ────────────────────────────────────────
scope:
  include:
    # - "*.target.com"
    # - "api.target.com"
    # - "target.com"
  exclude:
    # - "*.cdn.target.com"
    # - "static.target.com"
  strict: true  # Strict scope enforcement

# ─── Reconnaissance Modules ───────────────────────────────
recon:
  crtsh: true                    # Certificate transparency
  wayback: true                  # Wayback Machine
  otx: true                      # AlienVault OTX
  urlscan: true                  # URLScan.io
  dns_brute: true                # DNS subdomain brute
  dns_brute_wordlist_size: 5000  # Wordlist size
  subdomain_permutation: true    # Generate permutations
  zone_transfer: true            # Attempt zone transfer
  whois: true                    # WHOIS lookup
  shodan: false                  # Shodan (need API key)
  censys: false                  # Censys (need API key)

# ─── Scan Modules ────────────────────────────────────────
scan:
  xss: true                      # Cross-Site Scripting
  sqli: true                     # SQL Injection
  lfi: true                      # Local File Inclusion
  ssti: true                     # Server-Side Template Injection
  ssrf: true                     # Server-Side Request Forgery
  idor: true                     # Insecure Direct Object Reference
  cmdi: true                     # Command Injection
  open_redirect: true            # Open Redirect
  cors: true                     # CORS Misconfiguration
  crlf: true                     # CRLF Injection
  host_header: true              # Host Header Injection
  jwt: true                      # JWT Attacks
  graphql: true                  # GraphQL Attacks
  sensitive_files: true          # Sensitive File Discovery
  csrf: true                     # CSRF Detection
  subdomain_takeover: true       # Subdomain Takeover
  cve: true                      # CVE Detection

# ─── Advanced Payload Settings ────────────────────────────
payloads:
  xss_count: 50                  # Number of XSS payloads
  sqli_count: 30                 # Number of SQLi payloads
  waf_bypass: true               # Use WAF bypass techniques
  use_polyglots: true            # Use polyglot payloads
  use_obfuscation: true          # Use obfuscated payloads
  double_encode: true            # Double URL encoding

# ─── Ghost Modules (Requires ROOT) ───────────────────────
ghost:
  quantum_noise: false           # Generate noise traffic
  dimensional_shift: false       # MAC address spoofing
  dna_cloning: true              # Target fingerprinting
  ghost_flood: false             # ARP phantom flood
  mirror_mode: true              # Network host discovery
  echo_locator: false            # Passive network listening
  interface: "eth0"              # Network interface
  target_network: ""             # Target network for scanning

# ─── Anti False Positive ──────────────────────────────────
false_positive:
  enabled: true                  # Enable FP filter
  aggression: 2                  # 1=lenient, 2=normal, 3=aggressive
  verify_count: 2                # Verification attempts
  similarity_threshold: 0.85     # Response similarity threshold

# ─── Stealth Mode ────────────────────────────────────────
stealth:
  enabled: false                 # Stealth mode
  random_delay: true             # Random delays between requests
  random_user_agent: true        # Rotate User-Agent
  spoof_referer: true            # Spoof Referer header
  use_tor: false                 # Route through Tor

# ─── Reporting ───────────────────────────────────────────
reporting:
  json: true                     # JSON report
  csv: true                      # CSV report
  html: true                     # HTML report
  markdown: true                 # Markdown report
  burp_xml: false                # Burp Suite XML
  webhook: ""                    # Discord/Slack webhook URL

# ─── API Keys ────────────────────────────────────────────
api_keys:
  otx: ""                        # AlienVault OTX
  urlscan: ""                    # URLScan.io
  shodan: ""                     # Shodan
  censys_id: ""                  # Censys API ID
  censys_secret: ""              # Censys API Secret
  github: ""                     # GitHub Token

# ─── Notifications ───────────────────────────────────────
notifications:
  discord_webhook: ""            # Discord webhook
  slack_webhook: ""              # Slack webhook
  telegram_bot_token: ""         # Telegram bot token
  telegram_chat_id: ""           # Telegram chat ID
  email_smtp: ""                 # SMTP server
  email_port: 587                # SMTP port
  email_user: ""                 # SMTP username
  email_pass: ""                 # SMTP password
  notify_on_critical: true       # Notify on critical findings
  notify_on_high: true           # Notify on high findings
```

---

📖 README.py — README dalam bentuk Python (Mudah Dicopy)

```
AUTHOR: 418teapot
VERSION: 4.0 DARK EDITION
LICENSE: For authorized security testing only
STATUS: Production Ready — All Features 100% Functional

═══════════════════════════════════════════════════════════════════════════════════════
                            📋 QUICK START GUIDE
═══════════════════════════════════════════════════════════════════════════════════════

## 🚀 INSTALLATION

```bash
# Clone atau download script
git clone https://github.com/418teapot/blood-ghost-blue.git
cd blood-ghost-blue

# Install dependencies (auto-install saat pertama run)
python3 blood.py --setup

# Atau manual install
pip install -r requirements.txt
```

📖 USAGE

Mode 1: NO-ROOT (Bug Bounty Normal)

```bash
# Scan dasar
python3 blood.py target.com

# Scan agresif dengan FP filtering ketat
python3 blood.py target.com --fp-mode aggressive

# Deep scan dengan 10 workers
python3 blood.py target.com --deep --threads 10

# Custom scope
python3 blood.py target.com --scope "*.target.com,api.target.com"

# Multiple targets
python3 blood.py "target1.com,target2.com,target3.com"

# Dengan config file
python3 blood.py --config config.yaml
```

Mode 2: ROOT (Full Power + Ghost Modules)

```bash
# Root mode dasar
sudo python3 blood.py target.com --root-mode

# Root mode dengan semua ghost modules
sudo python3 blood.py target.com --root-mode --ghost-all

# Root mode dengan quantum noise
sudo python3 blood.py target.com --root-mode --ghost-quantum

# Root mode dengan internal network scan
sudo python3 blood.py target.com --root-mode --target-network 192.168.1.0/24

# Root mode custom interface
sudo python3 blood.py target.com --root-mode --interface wlan0
```

Mode 3: STEALTH (Ultra Slow Evasion)

```bash
# Stealth mode no-root
python3 blood.py target.com --stealth

# Stealth mode dengan root
sudo python3 blood.py target.com --stealth --root-mode

# Stealth dengan rate custom
python3 blood.py target.com --stealth --rate 5.0
```

⚙️ COMMAND LINE OPTIONS
```
Option Description Example
--config <file> Gunakan config YAML --config config.yaml
--target <domain> Override target di config --target target.com
--root-mode Aktifkan mode root (butuh sudo) --root-mode
--stealth Mode ultra-slow evasion --stealth
--deep Full recon + semua modules --deep
--scope <domains> Batasi scope scan --scope "*.target.com"
--out <domains> Exclude dari scope --out "*.cdn.target.com"
--fp-mode <mode> FP filter: lenient/normal/aggressive --fp-mode aggressive
--threads <N> Jumlah concurrent workers --threads 10
--rate <N> Requests per second --rate 3.0
--payloads <N> Jumlah payload per type --payloads 50
--output <dir> Output directory --output ./results
--ghost-all Aktifkan semua ghost modules --ghost-all
--ghost-quantum Aktifkan quantum noise --ghost-quantum
--ghost-flood Aktifkan ghost flood --ghost-flood
--ghost-mirror Aktifkan mirror mode --ghost-mirror
--ghost-dna Aktifkan DNA cloning --ghost-dna
--ghost-shift Aktifkan dimensional shift --ghost-shift
--ghost-echo Aktifkan echo locator --ghost-echo
--interface <iface> Network interface --interface eth0
--target-network <net> Target network (CIDR) --target-network 192.168.1.0/24
--setup Install dependencies --setup
--version Tampilkan versi --version
--help Tampilkan bantuan --help
```

📁 OUTPUT FILES

Setelah scan selesai, file berikut akan dibuat di folder output:

```
bounty_results/
├── bounty_report_20240605_143022.json     # JSON report (lengkap)
├── bounty_report_20240605_143022.csv      # CSV report (Excel-ready)
├── bounty_report_20240605_143022.md       # Markdown report
├── bounty_report_20240605_143022.html     # HTML report
├── evidence/                               # Evidence screenshots
├── logs/                                   # Scan logs
├── vdp_scan_20240605_143022.log           # Detailed scan log
└── bounty_hunter.db                        # SQLite database
```

🎯 CAPABILITIES

```
Reconnaissance

· ✅ CRT.sh Certificate Transparency (semua subdomain)
· ✅ Wayback Machine (semua URL historis)
· ✅ AlienVault OTX Passive DNS
· ✅ URLScan.io Search
· ✅ DNS Brute-force (5000+ wordlist)
· ✅ Subdomain Permutation Generator
· ✅ DNS Zone Transfer Attempt
· ✅ WHOIS Lookup
· ✅ Shodan/Censys Integration (dengan API key)

Vulnerability Scanning

· ✅ XSS (100+ payloads, polyglots, WAF bypass, DOM-aware)
· ✅ SQLi (Error-based, Blind, Time-based, Union, Stacked, OOB)
· ✅ LFI/RFI (Path Traversal, PHP Wrappers, Log Injection)
· ✅ SSTI (Jinja2, Twig, Freemarker, Velocity, ERB, Smarty, Mako)
· ✅ SSRF (Cloud Metadata AWS/GCP/Azure, Internal Ports)
· ✅ IDOR (Pattern Recognition, Sequential Forcing)
· ✅ Command Injection (40+ payloads, filter bypass)
· ✅ CORS Misconfiguration
· ✅ Open Redirect
· ✅ CRLF Injection
· ✅ Host Header Injection
· ✅ JWT Attacks (None Algorithm, Key Confusion)
· ✅ GraphQL Attacks (Introspection, Batching)
· ✅ Sensitive File Discovery (200+ paths)
· ✅ CSRF Detection
· ✅ Subdomain Takeover
· ✅ CVE Detection

Ghost Modules (Root Required)

· ✅ Quantum Noise (Traffic generation)
· ✅ Dimensional Shift (MAC spoofing)
· ✅ DNA Cloning (Target fingerprinting)
· ✅ Ghost Flood (ARP phantom flood)
· ✅ Mirror Mode (Network host discovery)
· ✅ Echo Locator (Passive network sniffing)

Advanced Features

· ✅ 50+ WAF Signatures Detection
· ✅ 5-Stage False Positive Elimination
· ✅ Adaptive Per-Domain Rate Limiting
· ✅ Response Caching & Retry Logic
· ✅ Stealth Mode (evasion)
· ✅ Multi-Format Reporting (JSON, CSV, MD, HTML)
· ✅ SQLite Database (all findings)
· ✅ YAML Configuration Support
· ✅ Discord/Slack/Telegram Notifications

```
🔧 CONFIGURATION

Config File (config.yaml)

```bash
# Generate default config
python3 blood.py --generate-config

# Edit config.yaml sesuai kebutuhan
nano config.yaml

# Jalankan dengan config
python3 blood.py --config config.yaml
```

Environment Variables

```bash
export BOUNTY_HUNTER="YourName"
export BOUNTY_EMAIL="your@email.com"
export OTX_API_KEY="your-otx-key"
export SHODAN_API_KEY="your-shodan-key"
export DISCORD_WEBHOOK="your-webhook-url"
```

⚠️ DISCLAIMER

```
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  WARNING — FOR AUTHORIZED TESTING ONLY                              ║
║                                                                         ║
║  This tool is designed for:                                             ║
║  • Bug Bounty Programs (with authorization)                             ║
║  • Penetration Testing (with written consent)                           ║
║  • Security Research (on own systems)                                   ║
║  • CTF Competitions                                                     ║
║                                                                         ║
║  DO NOT USE ON SYSTEMS WITHOUT EXPLICIT PERMISSION                      ║
║  The author is not responsible for misuse of this tool.                 ║
╚══════════════════════════════════════════════════════════════╝
```

📊 EXAMPLE OUTPUT

```
🩸 BLOOD GHOST BLUE — DARK EDITION v4.0
Bug Bounty Hunter • Real Exploitation Engine
Author: 418teapot
Session: a1b2c3d4
Targets: target.com
Workers: 5 | Rate: 2.0/s
FP Filter: ENABLED
Mode: NORMAL

══════════════════════════════════════════════════════════════
  🎯 TARGET: target.com
══════════════════════════════════════════════════════════════

[ PHASE 1: RECONNAISSANCE ]
  [CRT.sh] Searching certificate logs...
    → 47 subdomains
  [Wayback] Searching archives...
    → 1234 URLs
  [DNS Brute] Brute-forcing subdomains...
    → 23 subdomains
  [Permutation] Generating permutations...
    → 156 new permutations
  [Zone Transfer] Attempting zone transfer...
    → Failed (expected for most domains)
  [WHOIS] Looking up domain info...
    → Registrar: GoDaddy.com, LLC
  Total: 226 subdomains, 2478 URLs

[ PHASE 2: SENSITIVE FILE SCAN ]
  [!] https://dev.target.com/.env
  [!] https://staging.target.com/.git/config
  [!] https://api.target.com/phpinfo.php
  Sensitive files found: 8

[ PHASE 3: VULNERABILITY SCANNING ]
  [CRITICAL] SQL Injection — https://target.com/product?id=1
  [CRITICAL] SSRF — https://api.target.com/webhook?url=
  [HIGH] XSS — https://target.com/search?q=test
  [HIGH] IDOR — https://api.target.com/users/123 → 124
  [HIGH] SSTI (Jinja2) — https://target.com/profile?name=
  [MEDIUM] CORS — https://api.target.com/
  [MEDIUM] Open Redirect — https://target.com/logout?next=

[ HUNT SUMMARY ]
  Duration: 847.3s
  Total Findings: 23
  Critical: 2
  High: 7
  Medium: 9
  Low: 5
  Verified: 18
  False Positives Eliminated: 47

  Top Findings:
  [CRITICAL] SQL Injection — https://target.com/product?id=1
  [CRITICAL] SSRF — https://api.target.com/webhook?url=
  [HIGH] XSS — https://target.com/search?q=test
  ...

Reports Generated:
  📄 JSON: bounty_report_20240605_143022.json
  📊 CSV:  bounty_report_20240605_143022.csv
  📝 MD:   bounty_report_20240605_143022.md

══════════════════════════════════════════════════════════════
[ HUNT COMPLETE ]
══════════════════════════════════════════════════════════════
```

🤝 CONTRIBUTING

Pull requests welcome! Fokus area:

· Payload libraries (XSS, SQLi, SSTI, etc.)
· WAF signatures
· Recon sources
· FP detection patterns
· CVE detection modules

📝 LICENSE

MIT License — See LICENSE file for details.

═══════════════════════════════════════════════════════════════════════════════════════
🩸 HAPPY HUNTING — STAY LEGAL 🩸
═══════════════════════════════════════════════════════════════════════════════════════
"""

def show_readme():
"""Display README."""
print(doc)

def show_quickstart():
"""Display quick start guide."""
print("""
╔══════════════════════════════════════════════════════════════╗
║                    🩸 QUICK START GUIDE                                 ║
╚══════════════════════════════════════════════════════════════╝
```
1️⃣  NO-ROOT MODE (Bug Bounty Normal):
python3 blood.py target.com
python3 blood.py target.com --fp-mode aggressive
python3 blood.py target.com --deep --threads 10

2️⃣  ROOT MODE (Full Power + Ghost):
sudo python3 blood.py target.com --root-mode
sudo python3 blood.py target.com --root-mode --ghost-all

3️⃣  STEALTH MODE (Evasion):
python3 blood.py target.com --stealth
sudo python3 blood.py target.com --stealth --root-mode

4️⃣  CONFIG MODE (YAML):
python3 blood.py --config config.yaml

5️⃣  GENERATE CONFIG:
python3 blood.py --generate-config

6️⃣  INSTALL DEPENDENCIES:
python3 blood.py --setup

7️⃣  SHOW VERSION:
python3 blood.py --version

8️⃣  SHOW HELP:
python3 blood.py --help
python3 blood.py --readme
""")
```

def generate_config():
"""Generate default config.yaml."""
config_content = '''# ═══════════════════════════════════════════════════════════════

BLOOD GHOST BLUE — CONFIGURATION FILE

═══════════════════════════════════════════════════════════════

Generated by Blood Ghost Blue v4.0

Edit sesuai kebutuhan, lalu jalankan:

python3 blood.py --config config.yaml

═══════════════════════════════════════════════════════════════
```
hunter:
name: "418teapot"
email: "418teapotbot@gmail.com"
signal: "BloodGhostBlue/4.0"

targets: []

- target1.com

- target2.com

output:
directory: "./bounty_results"
database: "bounty_hunter.db"
log_level: "INFO"

performance:
workers: 5
rate_limit: 2.0
timeout: 15
max_retries: 2
max_urls: 1000
max_depth: 3

scope:
include: []
exclude: []
strict: true

recon:
crtsh: true
wayback: true
otx: true
urlscan: true
dns_brute: true
dns_brute_wordlist_size: 5000
subdomain_permutation: true
zone_transfer: true
whois: true
shodan: false
censys: false

scan:
xss: true
sqli: true
lfi: true
ssti: true
ssrf: true
idor: true
cmdi: true
open_redirect: true
cors: true
crlf: true
host_header: true
jwt: true
graphql: true
sensitive_files: true
csrf: true
subdomain_takeover: true
cve: true

payloads:
xss_count: 50
sqli_count: 30
waf_bypass: true
use_polyglots: true
use_obfuscation: true
double_encode: true

ghost:
quantum_noise: false
dimensional_shift: false
dna_cloning: true
ghost_flood: false
mirror_mode: true
echo_locator: false
interface: "eth0"
target_network: ""

false_positive:
enabled: true
aggression: 2
verify_count: 2
similarity_threshold: 0.85

stealth:
enabled: false
random_delay: true
random_user_agent: true
spoof_referer: true
use_tor: false

reporting:
json: true
csv: true
html: true
markdown: true
burp_xml: false
webhook: ""

api_keys:
otx: ""
urlscan: ""
shodan: ""
censys_id: ""
censys_secret: ""
github: ""

notifications:
discord_webhook: ""
slack_webhook: ""
telegram_bot_token: ""
telegram_chat_id: ""
email_smtp: ""
email_port: 587
email_user: ""
email_pass: ""
notify_on_critical: true
notify_on_high: true
'''

if name == "main":
import sys
from pathlib import Path

```

---

## 🎯 **RINGKASAN PERINTAH**

### **NO-ROOT (Bug Bounty Normal)**
```bash
python3 blood.py target.com
python3 blood.py target.com --fp-mode aggressive --deep
python3 blood.py target.com --scope "*.target.com" --threads 10
python3 blood.py --config config.yaml
```

ROOT MODE (Full Power)

```bash
sudo python3 blood.py target.com --root-mode
sudo python3 blood.py target.com --root-mode --ghost-all
sudo python3 blood.py target.com --root-mode --target-network 192.168.1.0/24
```

STEALTH MODE (Evasion)

```bash
python3 blood.py target.com --stealth
sudo python3 blood.py target.com --stealth --root-mode
```

CONFIG & SETUP

```bash
python3 blood.py --generate-config    # Buat config.yaml
python3 blood.py --setup              # Install dependencies
python3 blood.py --version            # Cek versi
python3 blood.py --readme             # Tampilkan README
python3 blood.py --quickstart         # Quick start guide
```

---

📂 FILE STRUCTURE

```
blood-ghost-blue/
├── blood.py              # Main scanner script
├── config.yaml           # Configuration file
├── README.py             # README dalam Python (ini)
├── requirements.txt      # Python dependencies
├── bounty_results/       # Output folder
│   ├── *.json
│   ├── *.csv
│   ├── *.md
│   └── *.db
└── logs/                 # Log files
```

---
