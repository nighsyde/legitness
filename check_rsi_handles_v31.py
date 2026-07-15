#!/usr/bin/env python3
"""
RSI handle checker — batch 31.
Numbers unleashed:
- Pure number handles (404, 418, 500 are all 3+ chars)
- 0x hex prefix handles (0xDEAD, 0xCAFE, etc.)
- Leet speak of core concepts (n0cl1p, 3xpl01t, etc.)
- Port numbers as callsigns (Port4444, Port31337, Port666)
- Year references (1984, 2600, 31337)
- Number-enhanced devnull variants
- Number-enhanced hacker concepts
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── PURE NUMBER HANDLES — just the error code, nothing else ──────────
    # Clean. Understated. The number IS the identity.
    "404",            # Not Found — the most famous HTTP error; 3 chars
    "418",            # I'm a teapot — the joke RFC; 3 chars
    "500",            # Internal Server Error; 3 chars
    "403",            # Forbidden; 3 chars
    "401",            # Unauthorized; 3 chars
    "301",            # Moved Permanently; 3 chars
    "302",            # Found/Redirect; 3 chars
    "503",            # Service Unavailable; 3 chars
    "502",            # Bad Gateway; 3 chars
    "504",            # Gateway Timeout; 3 chars
    "429",            # Too Many Requests; 3 chars
    "410",            # Gone; 3 chars
    "451",            # Unavailable For Legal Reasons; 3 chars

    # ── HEX WITH 0x PREFIX — the programmer's notation ────────────────────
    "0xDEAD",         # 0xDEAD — dead; 6 chars
    "0xBEEF",         # 0xBEEF — beef; 6 chars
    "0xCAFE",         # 0xCAFE — cafe; 6 chars
    "0xFACE",         # 0xFACE — face; 6 chars
    "0xFEED",         # 0xFEED — feed; 6 chars
    "0xDEAF",         # 0xDEAF — deaf; 6 chars
    "0xBEAD",         # 0xBEAD — bead; 6 chars
    "0xFF",           # 0xFF — maximum byte value; 4 chars
    "0x00",           # 0x00 — null byte; 4 chars
    "0x0",            # 0x0 — zero; 3 chars
    "0x1337",         # 0x1337 — leet in hex; 6 chars
    "0xDEAD1",        # 0xDEAD + 1
    "0xBAD",          # 0xBAD — bad; 5 chars

    # ── LEET SPEAK OF CORE HACKER CONCEPTS ───────────────────────────────
    # With numbers, these become unique strings RSI treats separately
    "n0cl1p",         # noclip in leet — where this all started
    "n0clip",         # noclip with one number
    "nocl1p",         # noclip with one number at end
    "3xpl01t",        # exploit in leet
    "3xploit",        # exploit with one number
    "expl01t",        # exploit with two numbers
    "0wn3r",          # owner in leet — "I am the 0wner"
    "0wned",          # already checked — taken? let me recheck
    "r00t3d",         # rooted in leet
    "r00tkit",        # rootkit in leet (root + kit)
    "p0wn3d",         # pwned in leet
    "spl01t",         # sploit in leet
    "h4ck3d",         # hacked in leet
    "d3fac3d",        # defaced in leet
    "5hell",          # shell in leet (5 for S)
    "5h3ll",          # shell fully leet
    "5h311",          # shell fully leet variant
    "r3v3rse",        # reverse in leet
    "1nject",         # inject in leet
    "1njected",       # injected in leet
    "4ccess",         # access in leet
    "4cc3ss",         # access fully leet
    "3xfil",          # exfil in leet
    "p4yload",        # payload in leet
    "null0day",       # null + 0day compound
    "0dayh4x",        # 0day + hax

    # ── PORT NUMBERS AS CALLSIGNS ─────────────────────────────────────────
    # Every hacker knows their port numbers. These are identity markers.
    "Port22",         # SSH — the secure shell port; where you want access
    "Port80",         # HTTP — the web port
    "Port443",        # HTTPS — the secure web port
    "Port666",        # port 666 — the beast; doom ran here on some servers
    "Port1337",       # port 1337 — the leet port; elite services ran here
    "Port4444",       # port 4444 — Metasploit's default listener port
                      # if you got a shell on port 4444, you used msfconsole
    "Port31337",      # port 31337 — the super elite port
    "Port8080",       # alternate HTTP; proxy port
    "Port3306",       # MySQL — the database port
    "Port3389",       # RDP — Remote Desktop Protocol; Windows remote access
    "Port5900",       # VNC — the visual remote desktop
    "Port6666",       # IRC — the beast's IRC port
    "Port6667",       # IRC — standard IRC
    "Port6697",       # IRC over SSL

    # ── YEAR REFERENCES ───────────────────────────────────────────────────
    "1984",           # George Orwell's 1984 — Big Brother; surveillance; doublethink
                      # every hacker who cares about privacy knows this number
    "2600",           # 2600 Hz — the tone that opened Bell telephone systems
                      # also 2600: The Hacker Quarterly magazine
                      # the most meaningful number in phone phreaking history
    "31337",          # elite — the full number; 5 chars
    "1337",           # leet — already checked but let me try again
    "12345",          # the most common password ever; ironic as a handle

    # ── NUMBER-ENHANCED DEVNULL VARIANTS ─────────────────────────────────
    "dev0",           # /dev/0 — doesn't exist but sounds right; dev zero
    "dev1",           # /dev/1 — the first dev
    "dev42",          # /dev/42 — the answer; Douglas Adams
    "devErr",         # dev error — conceptual
    "dev404",         # dev not found
    "dev500",         # dev internal error
    "dev0x0",         # dev at address 0x0 — null

    # ── COMBINED NUMBERS + HACKER CONCEPTS ───────────────────────────────
    "null404",        # null + 404 — nothing was found
    "error404",       # error + 404 — classic
    "Error404",       # same with caps
    "null500",        # null + 500 — nothing, and it crashed
    "code404",        # code 404
    "code500",        # code 500
    "access403",      # access forbidden
    "gone410",        # 410 gone
    "1337speak",      # 1337 speak — leet speak itself as a handle
    "leet1337",       # leet + 1337
    "elite31337",     # elite + 31337
    "h4x1337",        # hax + 1337
    "null0",          # null zero — the most fundamental nothing
    "null1",          # null one — off by one of null
    "rootkit0",       # rootkit zero
    "rootkit1337",    # rootkit leet
    "shell1337",      # shell leet
    "h4x0r1337",      # hax0r + 1337
    "nmap1337",       # nmap + 1337
    "zero0day",       # zero + 0day
    "day0",           # day zero — short form of 0day
]

# Enforce 3+ chars, alphanumeric only, deduplicate case-insensitively
seen = set()
NAMES_DEDUPED = []
for n in NAMES:
    if len(n) < 3:
        continue
    if not re.match(r'^[a-zA-Z0-9]+$', n):
        continue
    key = n.lower()
    if key not in seen:
        seen.add(key)
        NAMES_DEDUPED.append(n)

BASE_URL = "https://robertsspaceindustries.com/en/citizens/{}"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}
DELAY = 1.5


def check(name, session):
    url = BASE_URL.format(name)
    try:
        resp = session.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        return {"name": name, "url": url, "status": resp.status_code,
                "available": resp.status_code == 404, "error": None}
    except requests.RequestException as exc:
        return {"name": name, "url": url, "status": None,
                "available": None, "error": str(exc)}


def main():
    total = len(NAMES_DEDUPED)
    print(f"Checking {total} number-enhanced handles...\n")
    print(f"{'#':>4}  {'CODE':>4}  {'RESULT':<10}  {'HANDLE':<25}  URL")
    print("-" * 110)

    available = []
    unavailable = []
    errors = []

    with requests.Session() as session:
        for i, name in enumerate(NAMES_DEDUPED, 1):
            r = check(name, session)
            if r["error"]:
                tag = "ERROR"; errors.append(r)
            elif r["available"]:
                tag = "AVAILABLE"; available.append(r)
            else:
                tag = "TAKEN"; unavailable.append(r)

            code_str = str(r["status"]) if r["status"] else "ERR"
            print(f"[{i:>3}/{total}]  {code_str:>4}  {tag:<10}  {name:<25}  {r['url']}", flush=True)

            if i < total:
                time.sleep(DELAY)

    print("\n" + "=" * 110)
    print(f"\n✅  AVAILABLE ({len(available)}):")
    for r in available:
        print(f"   {r['name']:<30}  {r['url']}")

    print(f"\n❌  TAKEN ({len(unavailable)}):")
    for r in unavailable:
        print(f"   {r['name']:<30}  {r['url']}")

    output = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "total": total,
        "available": [{"name": r["name"], "url": r["url"]} for r in available],
        "unavailable": [{"name": r["name"], "url": r["url"]} for r in unavailable],
        "errors": errors,
    }
    with open("rsi_handle_results_v31.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v31.json")


if __name__ == "__main__":
    main()
