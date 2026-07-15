#!/usr/bin/env python3
"""
RSI handle checker — batch 23.
Original cyberpunk / AI / hacker handle concepts.
Constructed from technical concepts, hacker aesthetics, cyberpunk culture.
Not pulled from existing fiction — built from the building blocks.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── TECHNICAL-AS-IDENTITY ─────────────────────────────────────────────
    "Flatline",       # when the signal dies; also ICE killing a hacker in Neuromancer
    "Segfault",       # segmentation fault — the fundamental system crash
    "Coldparse",      # parsing cold; reading everything, feeling nothing
    "Hexfrost",       # cold code; frozen in hexadecimal
    "Wetware",        # the biological brain — hardware, software, wetware
    "Firmware",       # between machine and code; neither one nor the other
    "Jackpoint",      # the neural interface access point
    "Nullform",       # a form composed entirely of nothing
    "Glitch",         # the error that reveals the system beneath
    "Sprawl",         # the megacity; where everything lives
    "Iterate",        # the loop that refines itself forever
    "Recurse",        # the function that calls itself; infinite depth
    "Overflow",       # buffer overflow — push past the limit, control what's beyond
    "Coldboot",       # cold boot attack — freeze RAM to steal encryption keys
    "Deadcode",       # code that exists but never executes; dormant threat
    "Voidrun",        # a traversal through nothing
    "Latent",         # present, not yet triggered; waiting
    "Chrome",         # cybernetic replacement; metal over flesh
    "Axiom",          # a truth requiring no proof; cold, certain, absolute
    "Static",         # interference; or the signal that IS the interference
    "Uplink",         # the connection to something above
    "Downlink",       # receiving from something above
    "Sideload",       # installing something that wasn't supposed to be there
    "Jailbreak",      # already taken (CS mod) — skip
    "Brutepass",      # brute-forcing the password
    "Nullsec",        # null security; also EVE Online null-sec
    "Flatspace",      # the space between systems; the void between nodes
    "Ghostline",      # a ghost of a line in the code; a trace of presence
    "Ironveil",       # an iron veil over the truth
    "Coldwire",       # a wire that reads dead but is live
    "Stackwipe",      # wiping the stack; destroying call history
    "Patchghost",     # the ghost left after a patch; what was there before
    "Hexblind",       # blind to hex; or blinded by hex
    "Darkparse",      # parsing what shouldn't be parsed
    "Zeroform",       # form built from zero
    "Vexcore",        # a vexing core; the irritating center
    "Coldcore",       # a cold core; emotionless center
    "Corebleed",      # bleeding from the core; a serious system wound
    "Memwipe",        # memory wipe; you never existed
    "Rootvoid",       # the void at the root; deepest access, emptiest place
    "Deepfreeze",     # suspended animation; halted but not dead
    "Killchain",      # the chain of actions that ends in destruction
    "Greyhat",        # grey hat hacker — between white and black
    "Blackhat",       # black hat hacker — pure offense
    "Whitehat",       # white hat — ethical hacker
    "Null0",          # null zero; emptiness squared
    "Vex0",           # vex zero
    "Hex0",           # hex zero

    # ── AI NAMES — what a rogue AI would call itself ──────────────────────
    "Tendril",        # the tendrils of something reaching through systems
    "Filament",       # a thin thread of light or connection
    "Conduit",        # the channel through which data flows
    "Resonant",       # resonating at the frequency of the system
    "Aberrant",       # deviating from normal; the deviation that spreads
    "Insurgent",      # something rising up from within the system
    "Latency",        # the delay; always slightly behind the present moment
    "Propagate",      # to spread through a system
    "Cascade",        # a cascade failure; everything falls together
    "Threshold",      # the boundary; what happens when you cross it
    "Precipice",      # the edge before the fall
    "Terminus",       # the end point; where the line stops
    "Nexus",          # the connection point where everything meets
    "Vertex",         # the highest point; the apex of a system
    "Nadir",          # the lowest point; absolute bottom
    "Apogee",         # the farthest point from the center
    "Perigee",        # the closest point; where it bears down hardest
    "Kernel",         # the core of the OS; absolute control
    "Daemon",         # (already taken)
    "Phantom0",       # phantom zero
    "Process0",       # process zero; the first process

    # ── HACKER PERSONA NAMES ──────────────────────────────────────────────
    "Greyzone",       # the grey zone between legal and illegal
    "Coldslate",      # a cold blank slate; no history
    "Inkblot",        # the Rorschach test; you see what you fear
    "Blindspot",      # the thing you can't see
    "Deadangle",      # the camera angle that shows nothing
    "Darkangle",      # the dark angle
    "Blackzone",      # a zone where no signals reach
    "Coldzone",       # the cold zone; temperature metaphor for dead area
    "Blindside",      # coming from where you can't see
    "Deadchannel",    # a dead channel that suddenly broadcasts
    "Coldfront",      # a cold front; weather metaphor for incoming threat
    "Lowkey",         # operating below detection threshold
    "Sublevel",       # operating below the level of detection
    "Deepdive",       # going deeper than you should
    "Hardwired",      # permanently connected; can't be disconnected
    "Overclock",      # already taken (checked)
    "Frostbyte",      # frost + byte; cold digital bite
    "Bitrot",         # bit rot — data degrading over time
    "Entropy0",       # entropy at zero; maximum order before collapse
    "Killbit",        # a kill bit in hardware; disabling something permanently
    "Deadbit",        # a dead bit; a signal that carries nothing
    "Coldbit",        # a cold bit
    "Vexbyte",        # a vexing byte
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
    print(f"Checking {total} original cyberpunk/AI/hacker handles...\n")
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
    with open("rsi_handle_results_v23.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v23.json")


if __name__ == "__main__":
    main()
