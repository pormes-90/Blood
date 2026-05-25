```markdown
# 🧟‍♂️ Zombie VDP – Hive Mind Edition

> **"Ethical. Passive. Relentless."**  
> Alat bantu *bug bounty* yang beroperasi secara **100% pasif**, mematuhi pedoman **NASA VDP**, dan dilengkapi **Triple Filter** serta **Fury Ethical Guardian**.

[![PyPI version](https://img.shields.io/pypi/v/zombie-vdp)](https://pypi.org/project/zombie-vdp/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/pormes-90/ZOMBIE)](https://github.com/pormes-90/ZOMBIE/releases)

---

## ⚠️ **PENTING – ETIKA & LEGALITAS**

Zombie VDP **hanya** boleh digunakan untuk:

- Program **Vulnerability Disclosure Program (VDP)** yang sah.
- Pengujian pada domain yang **secara eksplisit mengizinkan** riset keamanan.
- Kegiatan **bug bounty** dengan izin tertulis dari pemilik sistem.

**DILARANG KERAS** menggunakan alat ini untuk aktivitas ilegal, eksploitasi tanpa izin, atau melanggar hukum yang berlaku.  
Pengguna bertanggung jawab penuh atas penggunaan alat ini.

---

## 🚀 **Cara Mengunduh & Menjalankan**

### 📥 **Unduh Binary Executable**
Binary tersedia di halaman [Releases](https://github.com/pormes-90/ZOMBIE/releases).  
Pilih versi terbaru, lalu unduh file `zombie_vdp`.

### 🔧 **Beri Izin Eksekusi (Linux/macOS/Termux)**
```bash
chmod +x zombie_vdp
```

▶️ Jalankan

```bash
./zombie_vdp
```

Atau, jika kamu menginstal dari PyPI:

```bash
pip install zombie-vdp
zombie
```

---

🧠 Fitur Utama

🔍 Recon Pasif (Zero Footprint)

· Wayback Machine, Common Crawl, crt.sh, DNS enumeration
· Tidak menyentuh server target sama sekali

🕷️ Crawler & Dork Scanner

· BFS Crawler dengan rotasi User‑Agent (150+ template)
· 1000+ pola dork untuk mendeteksi file sensitif

🔐 Secret Scanner

· 34 pola spesifik (AWS, GCP, GitHub, Stripe, dll.)
· Deteksi high‑entropy string dengan entropi Shannon

⚡ Vulnerability Checks

· XSS, SQLi (Error, Boolean, Blind), LFI, SSTI, Command Injection
· Open Redirect, CRLF Injection, Host Header, CORS, Rate Limit

🎯 High‑Impact Hunters

· IDOR (Insecure Direct Object Reference)
· SSRF (Server‑Side Request Forgery)
· Auth Bypass (Unauthenticated Access + Header Manipulation)
· Business Logic Flaws (Price, Quantity, Discount, Role, Step)

🌀 Fuzzer

· 8 kategori payload, confidence ≥ 95%
· Analisis baseline, similarity, time anomaly, error keyword

🛡️ Triple Filter Pipeline

· 🥷 Ninja – presisi tinggi, hanya bukti nyata
· ⚔️ Samurai – tebas false positive, cari dampak nyata
· 👻 Ghost – deteksi blind/OOB, confidence ≥ 98%

🔬 Deep Scanner

· Konfirmasi ulang dengan payload asli
· Time‑based SQLi detection (MySQL, PostgreSQL, MSSQL, Oracle, SQLite)
· Math test SSTI, LFI depth test

🔒 Evidence Locker

· Enkripsi AES‑256 (Fernet) + kompresi GZip
· Verifikasi integritas SHA‑256
· Ekspor ZIP terproteksi

📄 PoC Generator & Professional Report

· Multi‑format: curl, Python, HTML
· Laporan HTML profesional dengan Executive Summary, CWE, CVSS, Remediation

🛡️ Fury – The Ethical Guardian

· Verifikasi legalitas target
· Header etis transparan (identitas peneliti tercantum)
· Rate‑limit super sopan (1 req / 5 detik)
· Auto‑stop jika target menunjukkan penolakan

---

📋 Persyaratan Sistem

· Python 3.9+ (jika menginstal dari PyPI)
· Koneksi internet untuk recon pasif
· Terminal dengan dukungan UTF‑8 (untuk animasi & jam digital)

---

🔧 Build dari Source (Untuk Pengembang)

⚠️ Kode sumber TIDAK disertakan dalam repositori ini untuk mencegah penyalahgunaan.
Jika kamu pengembang yang sah dan ingin berkontribusi, hubungi penulis.

---

👤 Penulis

Dikha Pormes
📧 pormesdikha90@gmail.com
🐙 github.com/pormes-90

---

📜 Lisensi

Proyek ini dilisensikan di bawah MIT License – lihat file LICENSE untuk detail.

---

🙏 Ucapan Terima Kasih

Terima kasih kepada seluruh komunitas bug bounty yang menjunjung tinggi etika dan tanggung jawab.
Zombie VDP lahir dari semangat untuk membuat internet lebih aman, satu laporan pada satu waktu.

---

🧟‍♂️ "Mereka mungkin lambat, tapi ledakannya luar biasa."
– Fury, The Ethical Guardian

```

---

### ✅ **Langkah Selanjutnya**

Setelah file ini Tuan simpan di folder `~/ZOMBIE_PUBLIC`, lakukan commit dan dorong ulang ke repositori:

```bash
cd ~/ZOMBIE_PUBLIC
git add README.md
git commit -m "Update README with full documentation"
git push origin main
```
|         FITUR          |                            DETAIL                                |
|------------------------|------------------------------------------------------------------|
| **IDOR Hunter**        | Insecure Direct Object References (8+ parameter patterns)        |
| **SSRF Hunter**        | Server-Side Request Forgery (cloud metadata, internal services)  |
| **Auth Bypass Hunter** | Broken authentication (15+ sensitive paths, header manipulation) |
| **Logic Flaw Hunter**  | Business logic flaws (price/quantity/step manipulation)          |
| **Command Injection**  | RCE detection via timing analysis                                |
| **Subdomain Takeover** | CNAME analysis for cloud services                                |

### 🛡️ Core Scanners
- **XSS Detection** – reflected & DOM-based with HTML encoding verification
- **SQLi Detection** – error-based, boolean-based, and blind (timing) techniques
- **LFI Detection** – multi-depth path traversal testing
- **SSTI Detection** – template injection with math verification
- **Open Redirect** – header and meta refresh analysis
- **CORS Misconfiguration** – origin reflection testing
- **CRLF Injection** – header injection detection
- **Rate Limit Testing** – basic rate limiting verification

### 🔧 Advanced Features
- **Zombie Dork Scanner** – 1000+ sensitive pattern regexes
- **Zombie Secret Scanner** – 30+ API key/token patterns with entropy analysis
- **Zombie Fuzzer** – adaptive payload delivery with response analysis
- **Zombie Deep Scanner** – multi-stage verification (re-request, timing, DBMS detection)
- **Zombie Evidence Locker** – AES-256 encrypted evidence storage with integrity verification
- **Zombie Auto-PoC** – automatic curl/Python proof-of-concept generation
- **Professional HTML Report** – detailed findings with CWE/OWASP/CVSS info

### 🕵️ Stealth & Ethics
- **Configurable rate limiting** with jitter (default: 1 request/2 seconds)
- **Automatic cooling down** when blocked (60-120 second pauses)
- **Ethical User-Agent** with researcher identification
- **Respects robots.txt** (optional)
- **Time-slice scheduling** for off-peak operation
- **100% passive** – no exploitation, no brute force

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Linux/macOS/Windows (binary available for Linux aarch64)

### Installation
```bash
pip install zombie-vdp
```

Or download the pre-built binary from GitHub Releases:

```bash
./zombie_vdp
```

Configuration

Create a config.yaml file in the same directory:

```yaml
target_domains:
  - "nasa.gov"
  - "*.nasa.gov"

researcher_name: "Your Name"
researcher_email: "your@email.com"

password: "zombie"          # optional

max_workers: 1              # 1 request at a time
rate_limit: 0.5             # 1 request every 2 seconds
crawl_delay: [60.0, 120.0]  # 1-2 minutes between pages
```

Run

```bash
zombie
# or
python zombie_vdp/zombie.py
```

---

📊 Output Structure

```
output/
├── evidence/          ← Encrypted evidence files (.zombie)
├── poc/               ← Auto-generated PoC scripts
├── reports/           ← Professional HTML vulnerability reports
└── zombie.db          ← SQLite findings database
```

---

⚠️ Disclaimer

This tool is for authorized security testing only.

· Only test systems you own or have explicit written permission to test
· Do not exploit discovered vulnerabilities
· Report findings responsibly through official VDP channels
· Follow all program rules and scope limitations

The author assumes no liability for misuse of this tool.

---

📄 License

MIT License – see LICENSE file for details.

---

👤 Author

Dikha Pormes

· Email: pormesdikha90@gmail.com
· GitHub: pormes-90

---

🙏 Acknowledgments

Built with love for the bug bounty community. Special thanks to NASA for their commitment to security through responsible disclosure.

---

"Zombie VDP – because the best hunters move slowly and strike precisely." 🧟‍♂️💖

```
🧟‍♂️💖
