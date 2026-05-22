# 🧟‍♂️ Zombie VDP — Ultimate Bug Bounty Framework

[![PyPI version](https://img.shields.io/pypi/v/zombie-vdp?color=informational&label=PyPI)](https://pypi.org/project/zombie-vdp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

**Zombie VDP** adalah kerangka kerja bug bounty pribadi yang menggabungkan seluruh pipeline pengujian keamanan dalam satu nafas.  
Dirancang khusus untuk program **Vulnerability Disclosure Program (VDP)** seperti NASA, alat ini bekerja secara **100% pasif**, tidak meninggalkan jejak bot, dan hanya melaporkan temuan dengan confidence **90–100%**.

> **Identitas Zombie**: Semua fitur menggunakan nama `zombie_*` — bukan meniru, melainkan menciptakan ciri khas sendiri.

---

## 🔥 Fitur Utama

### 🔍 Zombie Recon (Pengintaian Pasif)
- **Wayback Machine** — arsip historis URL
- **Common Crawl** — indeks web publik
- **crt.sh** — certificate transparency log
- **AlienVault OTX** — database ancaman (perlu API key)
- **urlscan.io** — tangkapan layar & URL lama (perlu API key)
- **DNS Enumeration** — subdomain umum & zone transfer

### 🕸️ Zombie Crawler
- Perayapan halaman target dengan kedalaman terbatas
- Delay antar permintaan yang dapat dikonfigurasi (default 5–10 detik)
- Menghindari file binary & protokol non-HTTP

### 🧲 Zombie Dorking (Internal)
- Menyaring URL dari hasil recon & crawl menggunakan pola regex
- Tanpa search engine → **100% pasif, tidak terdeteksi**

### 🛡️ Zombie Scanner
| Kerentanan | Metode |
|-----------|--------|
| **XSS** (Reflected) | Payload injection + verifikasi Selenium (opsional) |
| **SQL Injection** | Error-based detection |
| **LFI** (Local File Inclusion) | Path traversal `/etc/passwd` |
| **Open Redirect** | Header `Location` injection |
| **SSTI** (Server-Side Template Injection) | `{{7*7}}` payload |
| **Missing Security Headers** | Pengecekan header HSTS, CSP, dll. |

### ⚡ Zombie Fuzzer (Adaptif)
- Analisis perbedaan respons (panjang, hash, kemiripan teks, waktu, error keyword)
- Hanya anomali dengan skor ≥ 0.9 yang dilaporkan

### 🔑 Zombie Secrets Scanner (TruffleHog Style)
- Pola regex:
  - AWS Access Key
  - GitHub Token
  - Slack Webhook
  - Generic JWT
- Deteksi di halaman web target, bukan hanya repositori

### ⚔️ Triple Filter (Ninja · Samurai · Ghost)
| Filter | Aturan |
|--------|--------|
| 🥷 **Ninja** | Hanya temuan dengan bukti (`evidence`) tidak kosong |
| ⚔️ **Samurai** | Hanya `HIGH`/`CRITICAL` & `response_length > 0` |
| 👻 **Ghost** | Hanya confidence ≥ 98% atau metode `timing`/`oob` |

### 🧪 Zombie Deep Scan
- Validasi lanjutan setelah filter: **timing attack** untuk konfirmasi SQLi

### 🔒 Zombie Evidence Locker
- Setiap temuan lolos filter disimpan sebagai **file terenkripsi** (format `.zombie`)
- Hanya bisa dibuka dengan kunci di folder `./output/evidence/`

### ⏳ Zombie Time Slice
- Zombie hanya beroperasi pada jam yang diizinkan (default nonaktif)
- Contoh: hanya pukul 02:00–05:00 UTC

### ⚡ Zombie Auto-PoC Generator
- Setiap temuan langsung dilengkapi skrip `curl` dan Python
- Tim triase tinggal menjalankan `bash reproduce.sh`

### 🧠 Zombie Memory
- State pemindaian disimpan di `zombie_memory.json`
- Pemindaian terhenti? Zombie bisa melanjutkan dari titik terakhir

### 📊 Zombie Report
- **HTML** — laporan profesional siap kirim ke VDP
- **CSV** — ekspor ke spreadsheet
- **JSON** — integrasi dengan alat lain

---

## 🧬 Arsitektur & Alur Kerja
