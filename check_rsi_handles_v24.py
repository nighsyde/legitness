#!/usr/bin/env python3
"""
RSI handle checker — batch 24.
Early 2000s dark web, newsgroups, mIRC, hacker and underground culture.
Real scene terminology, Phrack/2600/cDc culture, actual tools,
warez scene, OpSec concepts, the Hackers (1995) movie generation.
What would show cred in #elite on EFnet at 2am in 2002.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── THE REAL UNDERGROUND ZINES / CULTURE ──────────────────────────────
    "Phrack",         # Phrack magazine — THE hacker zine since 1985
                      # If you cited Phrack articles you weren't a skiddie
                      # "Smashing the Stack for Fun and Profit" was in Phrack #49
    "L0pht",          # L0pht Heavy Industries — the legendary hacker collective
                      # They testified before Congress in 1998 that they could take down
                      # the internet in 30 minutes. That credibility was real.
    "Mudge",          # Peiter "Mudge" Zatko — the most famous L0pht member
                      # Later worked at DARPA and Google; one of the most respected hackers
    "cDc",            # Cult of the Dead Cow — the hacker group that created Back Orifice
                      # The original political hacktivists; coined the term "hacktivism"
    "Def0n",          # Defcon — the annual hacker conference; attendees were the elite
    "EFnet",          # EFnet — the original IRC network; #hak, #warez, all lived here
    "Undernet",       # Undernet — another major IRC network for underground channels
    "QuakeNet",       # QuakeNet — the IRC network that hosted gaming and hacking channels

    # ── HACKERS (1995) — the movie that defined a generation's aesthetic ──
    # Every script kiddie from 1998-2005 referenced this movie.
    # Ironically, it's now considered a time capsule of that culture.
    "ZeroCool",       # Hack the Planet's lead — Dade Murphy's first handle at age 11
                      # "Zero Cool" — the handle that crashed 1507 systems in one day
    "CrashOverride",  # Dade's grown-up handle — "Crash Override"
    "AcidBurn",       # Kate's handle — the rival who became the love interest
    "ThePlague",      # The villain — the corrupt hacker working for the corporation
    "CerealKiller",   # the paranoid hacker in Hackers; "Cereal Killer"
    "PhantomPhreak",  # the phone phreaker in the movie
    "HackThePlanet",  # "HACK THE PLANET!" — the rallying cry of the movie
    "GibsonHack",     # Hacking the Gibson — the mainframe they were trying to breach

    # ── REAL HACKING CONCEPTS — what showed you knew the scene ──────────
    "Sploit",         # exploit abbreviated — "got a new sploit for IIS 5.0"
                      # Not "exploit" — that was how civilians said it. Sploit.
    "0wned",          # the alternative spelling; past tense of owning a system
    "GoingDark",      # going dark — evading surveillance; the fed term for losing a target
    "GoRoot",         # getting root — the goal of any serious compromise
    "GotShell",       # the moment — "I got shell on that box"
    "Deface",         # website defacement — leaving your mark on a compromised server
    "Pivot",          # pivoting through a compromised network to reach deeper systems
    "Dropper",        # first-stage malware that delivers the actual payload
    "Crypter",        # encrypting malware to evade antivirus detection
    "Packer",         # packing/obfuscating an executable to evade AV signature scanning
    "Shellcode",      # the code that runs after a successful buffer overflow
    "Stacksmash",     # smashing the stack — the buffer overflow exploit technique
    "HeapSpray",      # heap spray — the technique of spraying shellcode into the heap
    "ReturnToLibc",   # bypassing stack protection by returning into libc functions
    "FreeKevin",      # "Free Kevin Mitnick" — the movement after the most famous hacker
                      # was arrested; rallying cry of the underground in the late 90s

    # ── OPSEC / ANONYMITY CONCEPTS ────────────────────────────────────────
    # Operational security — not getting caught
    "VHost",          # virtual host — cloaking your IP on IRC behind a hostname
    "Bouncer",        # IRC bouncer — staying connected while hiding your real IP
    "ProxyChain",     # chaining proxies to hide origin; "I was behind 7 proxies"
    "SevenProxies",   # the "I'm behind 7 proxies" meme from early Anonymous era
    "Proxied",        # behind a proxy; protected
    "Torified",       # routing through Tor; the anonymity network
    "Darkened",       # going dark; hidden from surveillance
    "Cloaked",        # IP-cloaked on IRC
    "Covert",         # covert access; hidden channels
    "Exfiltrate",     # to exfiltrate data — taking information out of a compromised system
    "Exfil",          # abbreviated
    "CoverTrack",     # covering your tracks — deleting logs after a compromise

    # ── WAREZ SCENE ───────────────────────────────────────────────────────
    "Warez",          # pirated software; the underground economy
    "0day",           # zero-day warez — software released the same day as retail
    "Topsite",        # the elite private FTP sites; where warez lived before public trackers
    "Courier",        # the people who distributed warez between topsites
    "Ratio",          # upload/download ratio on warez FTP sites; 1:3 ratio or banned
    "Leecher",        # someone who only downloaded, never contributed; the lowest rung
    "Nfo",            # the .NFO file — the hacker/warez group's calling card
    "RARpass",        # the RAR password on protected warez archives
    "XDCC",           # XDCC file serving on IRC — the way to get files from bots
    "FServe",         # file server on IRC — another way to share files
    "Nuker",          # a nuker — nuking an IRC connection; disruption tool
    "FloodBot",       # a flood bot — used to kick users off IRC channels

    # ── IRC CULTURE SPECIFIC ───────────────────────────────────────────────
    "WarDrive",       # war driving — driving around scanning for open WiFi with a laptop
    "Stumbler",       # NetStumbler — the war driving tool; the app that found the WiFi
    "Wardial",        # war dialing — scanning phone numbers for modems (WarGames)
    "Phreaker",       # phone phreaker — the older art of hacking phone systems
    "BlueBox",        # the Blue Box — device that generated phone company tones
                      # Steve Wozniak and Jobs built one before Apple. Deep history.
    "RedBox",         # the Red Box — device simulating coin tones for payphones
    "ToneLoc",        # ToneLoc — the war dialing tool named after the rapper
    "ScanLine",       # the scanning tool; scanning a range of IPs

    # ── SCRIPT KIDDIE TERMS (worn ironically as badges) ───────────────────
    "Skiddie",        # script kiddie — using others' tools without understanding them
                      # Wearing this ironically shows you're above it
    "Scriptkid",      # same
    "LamEr",          # lamer — the worst insult in early hacker culture
    "Newbie",         # newbie — just arrived, don't know anything yet
    "Rootless",       # no root; still working to get there; pre-compromise identity

    # ── THE TOOLS EVERYONE KNEW ──────────────────────────────────────────
    "SubSeven",       # Sub7 — the most widely used RAT in 2001-2003
                      # If you were a teenager in 2002, you ran Sub7 on someone
    "NetBus",         # NetBus — the predecessor RAT; same category
    "BackOrifice",    # Back Orifice — the cDc's famous Windows remote admin tool
    "Nessus",         # Nessus — the vulnerability scanner; the professional tool
    "Nmapr",          # nmap user — the port scanner everyone used
    "Nikto",          # Nikto — the web vulnerability scanner
    "Hydrar",         # Hydra — the brute force tool
    "THC",            # The Hacker's Choice — the group behind many famous tools
    "Metasploit",     # Metasploit — the exploitation framework; the pro tool
    "Armitage",       # Armitage — the GUI for Metasploit

    # ── THE MOMENT EVERYONE RECOGNIZED ───────────────────────────────────
    "AccessDenied",   # "Access Denied" — what you saw before you broke through
    "Unauthorized",   # "Unauthorized Access" — the error before the breach
    "Logging0ut",     # logging out — the last act before going dark
    "Connected",      # the moment the shell connected; "connection established"
    "Rooted",         # you got root; past tense of the goal
    "Compromised",    # the system is compromised — it belongs to someone else now
    "Backdoored",     # a backdoor was left; you can always return
    "Persistent",     # persistent access — you survived a reboot
]

# Enforce 3+ chars, alphanumeric only, deduplicate
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
    print(f"Checking {total} early 2000s underground/hacker culture handles...\n")
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
    with open("rsi_handle_results_v24.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v24.json")


if __name__ == "__main__":
    main()
