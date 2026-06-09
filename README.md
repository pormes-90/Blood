--------------
| Engine     | Method | Priority | Cooldown   |
|------------|--------|----------|------------|
| Bing       | GET    | 1        | 1.5-2.5s   |
| Yahoo      | GET    | 2        | 1.5-2.5s   |
| Yandex     | GET    | 3        | 2.0-3.0s   |
| DuckDuckGo | POST   | 4        | 2.0-3.5s   |
| Brave      | GET    | 5        | 2.5-4.0s   |

🛡️ FILTER PIPELINE — 5 STAGES
--------------
| Stage | Filter              | Description                           |
|-------|---------------------|---------------------------------------|
| 1     | Confidence Threshold | Remove <60% confidence                |
| 2     | Immune Parameters    | Remove safe params (90+ params)       |
| 3     | Known FP Detection   | Pattern-based false positive removal  |
| 4     | Quality Scoring      | Score 0-100 (6 factors)               |
| 5     | Deduplication        | Hash + URL/type dedup                 |

📊 OUTPUT FORMAT
--------------
fusion_results/
└── report_<target>_<timestamp>/
    ├── report.json      # Full JSON report
    ├── findings.csv     # CSV table
    └── README.md        # Human-readable report

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

👤 IDENTITAS
--------------
- Hunter: Dikha Pormes
- Email: 418teapotbot@gmail.com
- Signal: BloodGhostZombie/Fusion-v3.0
- Anonymous Mode: Random identity rotation

📄 LISENSI
--------------
PROPRIETARY — ALL RIGHTS RESERVED
Hanya untuk ethical use: riset keamanan, bug bounty, pendidikan.

⭐ CREDITS
--------------
Dibuat oleh Dikha Pormes & 418teapot
"Untuk orang yang kusayangi — selamanya dalam kode ini."

================================================================================
                          END OF README.md
================================================================================
"""
