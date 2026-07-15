#!/usr/bin/env python3
"""
RSI handle checker — batch 19.
The EXPERIENCE of PC gaming 1999-2006, not the content.
Hardware everyone talked about upgrading, competitive rituals,
the social fabric, the culture around gaming itself.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── CPU CODENAMES — the hardware everyone was upgrading to ─────────────
    # These were talked about constantly on forums; every gamer knew them.
    "Thunderbird",    # AMD Athlon Thunderbird — the CPU that made CS 1.6 run
                      # Sounds like a fighter jet. Sounds like a callsign. IS a callsign.
    "Barton",         # AMD Athlon XP Barton — the overclocker's dream chip
                      # "Did you get the Barton?" was said on every hardware forum
    "Palomino",       # AMD Athlon Palomino — the chip before Thoroughbred
    "Thoroughbred",   # AMD Athlon XP Thoroughbred — the stepping everyone wanted
    "Northwood",      # Intel Pentium 4 Northwood — the Intel equivalent
    "Coppermine",     # Intel Pentium III Coppermine — the chip that ran Quake beautifully
    "Newcastle",      # AMD Athlon 64 Newcastle — the 64-bit transition chip

    # ── GPU/DISPLAY ERA — what your rig could push ────────────────────────
    "Trinitron",      # Sony Trinitron CRT — THE gaming monitor of the late 90s/early 2000s
                      # "I have a Trinitron" was a flex. The flat screen CRT.
    "Diamondtron",    # Mitsubishi Diamondtron — the other premium CRT; Trinitron's rival
    "Aperture",       # Aperture Grille — the CRT technology behind Trinitron; the thin wires
    "Refresh",        # refresh rate — upgrading from 60Hz to 100Hz was life-changing
    "Overclock",      # the act of overclocking — pushing your hardware beyond spec
    "Benchmark",      # benchmarking your rig — 3DMark, Quake3 timedemo, etc.
    "Fraps",          # Fraps — THE recording/benchmarking software every PC gamer used
                      # "what's your Fraps score?" "record it in Fraps"
    "Vsync",          # vertical sync debate — on or off was a constant conversation
    "Antialiasing",   # AA settings — people spent hours debating 2x vs 4x vs 8x
    "Anisotropic",    # anisotropic filtering — the texture clarity setting
    "DirectX9",       # DirectX 9 — the graphics API of the era; SM2.0/SM3.0 debates
    "OpenGL",         # OpenGL — the alternative; CS ran on OpenGL by default
    "Shader",         # shader models — what your GPU could handle
    "Fillrate",       # fill rate — the GPU performance metric everyone quoted

    # ── THE COMPETITIVE GAMING FRAMEWORK ─────────────────────────────────
    # These words were used constantly in every competitive gaming community.
    "Ladder",         # the competitive ranking ladder; climbing the ladder
    "Bracket",        # the tournament bracket; single or double elimination
    "Seeded",         # being seeded in a tournament — earned by previous results
    "Qualifier",      # the qualifying round — to get into the main event
    "Playoff",        # the playoff stage — where it really counts
    "GrandFinal",     # the grand final — the biggest match
    "DoubleElim",     # double elimination — losers bracket gives a second chance
    "UpperBracket",   # upper bracket — staying in winners side
    "LowerBracket",   # lower bracket — losing once and fighting from behind
    "Tiebreaker",     # the tiebreaker match
    "Overtime",       # taken (checked)
    "Rematch",        # already confirmed available
    "Runback",        # running it back — asking for a rematch
    "Forfeit",        # forfeiting — conceding the match
    "Concede",        # conceding
    "Techdefeat",     # technical defeat — losing on a technicality
    "Walkover",       # opponent no-shows; you advance by default

    # ── THE GRIND / COMPETITIVE EXPERIENCE ───────────────────────────────
    # The emotional and practical experience of competitive online gaming.
    "Grind",          # the grind — hours of practice to improve; universal experience
    "Choke",          # choking — performing worse under pressure; "he choked"
    "Slump",          # being in a slump — extended period of poor performance
    "Comeback",       # the comeback — turning a losing match around
    "Clutchplay",     # making a clutch play — performing under maximum pressure
    "Onfire",         # "he's on fire" — consecutive good plays
    "Hotstreak",      # hot streak — multiple wins/kills in a row
    "Coldstreak",     # cold streak — multiple losses in a row
    "Plateau",        # hitting a skill plateau — no improvement despite practice
    "Breakthrough",   # the breakthrough — finally improving after a plateau
    "Tiltmode",       # being on tilt — tilted and playing badly
    "Ragemode",       # going into rage mode — tilted but aggressive
    "FocusMode",      # locked in, concentrated play

    # ── THE TEAM/CLAN EXPERIENCE ─────────────────────────────────────────
    # Being in a clan was one of the defining PC gaming experiences.
    "Clanleader",     # the leader of the clan — ultimate authority
    "Clanmates",      # your clan teammates
    "Raidleader",     # the raid leader in WoW — the voice giving orders
    "Guildmaster",    # the WoW guild master — above the raid leader
    "Guildofficer",   # guild officer — the middle management of WoW guilds
    "Trialmember",    # trial member — on probation before full membership
    "Shotcaller",     # the in-game caller — makes decisions in real time
    "Entryfragger",   # the entry fragger — first through the door in CS
    "Lurker",         # already taken (checked)
    "IGL",            # in-game leader — the tactical brain
    "Fragger",        # the fragger — the pure killing machine on the team
    "Support",        # the support player — setup plays, utility

    # ── THE DOWNLOAD / MOD CULTURE ───────────────────────────────────────
    "Filefront",      # FileFront.com — where you got mods, patches, maps before Steam
    "Gamefront",      # GameFront — FileFront's later rebrand
    "Modfolder",      # the mod folder — where custom content lived
    "Patchnotes",     # patch notes — reading what changed after every update
    "Hotpatch",       # hotfix/hotpatch — emergency fix deployed mid-day
    "Netcode",        # the netcode — how the game handled online connections
                      # "the netcode is broken" was said in every online game
    "Tickrate",       # server tick rate — 64 vs 128 tick was a CS debate
    "Hitbox",         # the hitbox — "the hitboxes are broken" was universal
    "Desync",         # desynchronization — when client and server disagree
    "Rubberbanding",  # rubber band lag — snapping back to a previous position
    "Rollback",       # rollback netcode — the modern solution; discussed historically

    # ── THE PERIPHERAL CULTURE ────────────────────────────────────────────
    # The gear people talked about constantly.
    "Intellimouse",   # Microsoft IntelliMouse — THE gaming mouse of 1999-2004
                      # "I use an IntelliMouse" was a respectable setup answer
    "MX518",          # Logitech MX518 — one of the most beloved gaming mice ever
                      # Released 2004, used by pros for a decade after
    "Qck",            # SteelSeries QcK — the iconic black cloth mousepad
                      # "What mousepad? QcK" — the default answer for years
    "Mousepad",       # the gaming mousepad — Artisan, QcK, Fata1ity — huge topic
    "Lowsens",        # low sensitivity — arm aiming; the purist approach
    "Highsens",       # high sensitivity — wrist aiming
    "MouseAccel",     # mouse acceleration — turning it off was a rite of passage
    "NegAccel",       # negative acceleration — the thing everyone feared

    # ── THE BROADER GAMING EXPERIENCE ────────────────────────────────────
    "MonthlyFee",     # the WoW monthly subscription — $15/month was the price of admission
    "NoSubscription", # free-to-play alternatives before F2P was common
    "ServerQueue",    # the WoW server queue — waiting 2 hours to log in during peak
    "Maintenance",    # the Tuesday maintenance window — servers down for 8 hours
    "Downtime",       # general downtime — when servers were unavailable
    "Rollout",        # the rollout of a patch — staged deployment
    "Megaserver",     # a mega-server consolidation (later MMO feature)
    "Realmmerge",     # realm merges — when low-pop servers combined
    "Layering",       # WoW Classic layering tech
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
    print(f"Checking {total} handles — the experience of PC gaming 1999-2006...\n")
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
    with open("rsi_handle_results_v19.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v19.json")


if __name__ == "__main__":
    main()
