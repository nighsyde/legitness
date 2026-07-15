#!/usr/bin/env python3
"""
RSI handle checker — batch 25.
Drawing from the actual underground:
- Real LOD/MOD/Phrack member handles (single word versions)
- Hacker Manifesto concepts ("My crime is that of curiosity")
- The BBS/EFnet naming philosophy: known but anonymous, feared but respected
- "You may stop this individual, but you can't stop us all"
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── REAL HANDLES FROM HISTORY (single-word versions) ──────────────────
    # These people were the actual underground. Real credibility.

    # Legion of Doom (LOD) — America's most legendary hacker group
    "Terminus",       # Terminus — an LOD member; "the endpoint" — final, absolute
    "Marauder",       # Marauder — LOD member; one who raids; took what wasn't his
    "Mentor",         # The Mentor — wrote The Hacker Manifesto in Phrack #7 (1986)
                      # "I am a hacker, and this is my manifesto"
    "Bloodaxe",       # Erik Bloodaxe — major LOD figure; edited Phrack for years
                      # One of the most respected names in the underground
    "LordDigital",    # Lord Digital — LOD member; the lord of digital spaces
    "Deadlord",       # Dead Lord — LOD member; the lord who is already dead
    "Kinison",        # Kinison — LOD member (named after Sam Kinison)
    "Leftist",        # Leftist — LOD member
    "Nightstalker",   # Nightstalker — from BBS era; one who stalks in the dark

    # Masters of Deception (MOD) — LOD's rival crew
    "PhibOptik",      # Phiber Optik (Mark Abene) — the most famous MOD member
                      # Served a year in prison; mentor to many NYC hackers
    "AcidPhreak",     # Acid Phreak — Elias Ladopoulos; MOD member

    # The Phrack authors who defined the technical canon
    "AlephOne",       # Aleph One — wrote "Smashing the Stack for Fun and Profit"
                      # Phrack #49 (1996). The most-read security paper of all time.
                      # Aleph (the first letter of the Hebrew alphabet) + One
    "Daemon9",        # daemon9 — Phrack contributor and security researcher
    "ReDragon",       # route/daemon9/ReDragon — the Phrack contributors

    # ── THE HACKER MANIFESTO — concepts from the text itself ──────────────
    # "My crime is that of curiosity."
    "TheMentor",      # The Mentor's full handle — the identity he chose
    "CrimeOfCuriosity",# "My crime is that of curiosity"
    "OutsmartYou",    # "My crime is that of outsmarting you"
    "WeAreAlike",     # "After all, we're all alike" — the closing line
    "EnterMyWorld",   # "I am a hacker, enter my world"
    "BeautyOfBaud",   # "the beauty of the baud" — the aesthetic of the manifesto
    "WorldElectron",  # "the world of the electron and the switch"
    "YouCallUsCriminals", # "you call us criminals" — the refrain
    "CannotStopUs",   # "You may stop this individual but you can't stop us all"

    # ── THE UNDERGROUND PHILOSOPHY — what drove the names ─────────────────
    # Being known in the underground while invisible to authorities.
    "Clandestine",    # completely secret; hidden operations
    "Subterranean",   # existing beneath the surface; underground
    "Specter",        # a ghost; present but untouchable; also an intel vulnerability
    "Chimera",        # an illusion; a monster from mythology; impossible to catch
    "Wraith",         # (already taken)
    "Umbra",          # the fully dark part of a shadow; the darkest point
    "Obscura",        # camera obscura; hidden; dark; mysterious
    "Penumbra",       # the partially shadowed region; between light and dark
    "Silhouette",     # the outline only; shape without substance; anonymous
    "Sigil",          # a magical symbol; a mark left to be recognized by those who know
    "Glyph",          # a carved symbol; a mark
    "Cipher",         # (taken) — but what about `Enciphered`
    "Enciphered",     # encrypted; converted to cipher
    "Redacted",       # information removed; the black bar over the truth
    "Expunged",       # records deleted; you were never there
    "Stricken",       # struck from the record
    "Nullified",      # made void; doesn't exist

    # ── THE "KNOWN BUT ANONYMOUS" PARADOX ─────────────────────────────────
    # The best handles suggested capability without proving it.
    # You were a legend before anyone could verify it.
    "Phantom",        # (already taken)
    "Revenant",       # (taken)
    "Specter",        # the unverifiable presence
    "Latency",        # (available, confirmed earlier)
    "Liminal",        # on the threshold; between states; neither inside nor outside
    "Interstitial",   # existing between things; in the gaps
    "Periphery",      # the edge; where oversight doesn't reach
    "Tangential",     # touching but not intersecting; adjacent to the target
    "Adjacent",       # next to, but not quite; one step from the center
    "Oblique",        # indirect; not straightforward; slanted
    "Lateral",        # sideways movement; lateral thinking; the pivot
    "Proximate",      # nearby but not the cause; close but removed
    "Distal",         # far from the center; at a remove
    "Remote",         # operating from distance; remote access
    "Vectored",       # having an attack vector; directed threat

    # ── WHAT THE OLD GUARD ACTUALLY VALUED ───────────────────────────────
    # Cleverness over force. Social engineering over brute force.
    # Reading the system. Knowing what nobody else knew.
    "Ingress",        # the way in; finding the entry point nobody saw
    "Egress",         # the way out; leaving without a trace
    "Siphon",         # drawing data out quietly; the subtle extraction
    "Intercept",      # catching the signal before it reaches its destination
    "Skimmer",        # reading without being seen; passing over the surface silently
    "Resonance",      # (taken)
    "Frequency",      # operating on a frequency nobody's monitoring
    "Carrier",        # the carrier signal; what hides the message
    "Steganography",  # hiding messages in plain sight; data inside data
    "Steg",           # steganography abbreviated; hiding in plain sight
    "Covert",         # (taken)
    "Subliminal",     # below the threshold of perception
    "Exponent",       # the power; the multiplying force
    "Logarithm",      # the inverse; finding the power from the result
    "Algorithm",      # the process; the method
    "Recursion",      # (took Recurse; let's check this variant)

    # ── BBS NAMING CONVENTIONS — the actual aesthetic ─────────────────────
    # Lords, Phantoms, Doctorsof things. The aristocracy of the underground.
    "LordChaos",      # Lord of Chaos — the classic BBS handle structure
    "DarkPrince",     # Dark Prince — another classic
    "SilverSpy",      # Silver Spy — another LOD-era naming convention
    "IronLungs",      # Iron Lungs — a classic absurdist hacker handle
    "Nightcrawler",   # Nightcrawler — one who moves through dark places
    "Darkforce",      # dark force
    "Blacklung",      # Black Lung — a classic handle energy
    "Grayzone",       # (checked before)
    "Duskfall",       # when darkness falls
    "Coldlight",      # cold light; the light that reveals but doesn't warm
    "Halflife",       # (taken)
    "Halflight",      # the half-light between day and night
    "Twilight",       # the transition between states
    "Dusk",           # the beginning of darkness
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
    print(f"Checking {total} underground legend handles...\n")
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
    with open("rsi_handle_results_v25.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v25.json")


if __name__ == "__main__":
    main()
