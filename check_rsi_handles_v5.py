#!/usr/bin/env python3
"""
RSI handle availability checker — batch 5.
de_dust2 variations + Diablo 2 online era names.
404 = available. 200 = taken.
"""

import sys
import time
import requests
import json
from datetime import datetime

NAMES = [
    # ── de_dust2 / dust2 variations ───────────────────────────────────────
    "Dust2",           # the clean version
    "DeDust2",         # with the map prefix
    "DeDust",          # the original dust (before dust2 existed)
    "LongA",           # the long A corridor; every CS player has held this angle
    "ShortA",          # short A rush
    "BombsiteA",       # the A bombsite
    "BombsiteB",       # the B bombsite
    "MidDoors",        # the middle doors connecting mid to B; every CS player knows this
    "Tunnels",         # the B tunnels under dust2
    "Catwalk",         # the catwalk from mid to A
    "Goose",           # the Goose spot on A site dust2
    "Xbox",            # the Xbox box in the middle of dust2 mid
    "LongDoors",       # the long A doors where so many battles were fought
    "UpperTunnel",     # upper B tunnel
    "LowerTunnel",     # lower B tunnel
    "CTSpawn",         # counter-terrorist spawn
    "TSpawn",          # terrorist spawn
    "BananaInfoerno",  # banana on inferno (the approach to B)

    # ── Diablo 2 — bosses & locations ─────────────────────────────────────
    "Mephisto",        # Act 3 boss; the most farmed boss in D2 for items
    "Baal",            # the final boss; every endgame run was a Baal run
    "Andariel",        # Act 1 boss — Andy; spider-queen
    "Duriel",          # Act 2 boss; the Maggot Lair nightmare
    "Pindleskin",      # the undead boss everyone farmed for high rune drops
    "Tyrael",          # the Archangel of Justice who helped you
    "Izual",           # the corrupted angel boss you had to kill
    "Diablo2",         # the sequel specifically
    "Travincal",       # Act 3 — the Council location; best spot for high rune farming
    "ChaosSanctuary",  # Act 4 — star-shaped final dungeon before Diablo
    "MaggotLair",      # Act 2 — universally hated dungeon; tiny corridors
    "DuranceOfHate",   # Mephisto's lair; level 3 was where he waited
    "CowLevel",        # the Secret Cow Level — one of gaming's most beloved secrets
    "SecretCowLevel",  # the full name
    "MooMooFarm",      # what players called the cow level
    "TalRasha",        # the legendary Horadric mage; his tomb was Act 2's goal
    "Worldstone",      # the Worldstone Keep — the final Act 5 dungeon
    "Harrogath",       # the Act 5 town; the last bastion against Baal

    # ── Diablo 2 — classes & builds ───────────────────────────────────────
    "Hammerdin",       # the Blessed Hammer Paladin — the most OP build in D2
    "Necromancer",     # the skeleton summoner class
    "Sorceress",       # the fire/ice/lightning caster — most played class
    "Fishymancer",     # the summoner Necromancer build (skeleton army)
    "Bowazon",         # the Bow Amazon build
    "Javazon",         # the Javelin Amazon build
    "Whirlwind",       # the Barbarian's iconic spin-to-win ability
    "Smiter",          # the Smite Paladin used for Uber bosses
    "MFSorc",          # Magic Find Sorceress — running Meph/Andy for drops

    # ── Diablo 2 — items & economy ────────────────────────────────────────
    "Enigma",          # the most coveted runeword armor in D2; changed the entire meta
    "Shako",           # Harlequin Crest — the helmet everyone wanted
    "Annihilus",       # the Uber Diablo reward small charm — the most coveted item
    "StoneOfJordan",   # THE trade currency of original Diablo 2; finding one was an event
    "Windforce",       # the godly Amazon bow
    "Zod",             # the rarest rune; finding one was legendary
    "BerRune",         # Ber — the second rarest rune; needed for Enigma
    "ZodRune",         # Zod — the absolute rarest; perfect socket item
    "Hellfire",        # the Hellfire Torch unique charm
    "Stormshield",     # the elite Paladin shield
    "Oculus",          # the Sorceress orb
    "Thunderstroke",   # the Javazon's best javelin

    # ── Diablo 2 — culture & online life ──────────────────────────────────
    "BaalRun",         # the endgame Baal run; said and typed ten thousand times
    "MephRun",         # the Mephisto farm run
    "CowRun",          # running the cow level
    "Rushme",          # asking to be rushed through the game
    "LadderReset",     # the moment a D2 ladder season ended; everyone started fresh
    "Hardcore",        # permadeath mode — the most intense way to play D2
    "Softcore",        # normal mode — dying doesn't delete your character
    "HCDied",          # your hardcore character died; the pain
    "OpenBnet",        # open Battle.net — the unregulated wild west of D2
    "NineLives",       # the cat-like survival required in HC
    "SojTrade",        # trading with Stone of Jordans as currency
    "PacketTeleport",  # the D2 Sorceress teleport desyncing from packets; iconic bug
    "TheMuler",        # the mule character — only used to store items
    "HostileMe",       # the D2 option to flag as hostile to other players in your game; PK culture
    "PinLe",           # shorthand for Pindleskin runs
    "GrandCharm",      # the best charms in D2; getting perfect ones was huge
    "PerfectGem",      # perfectly chipped/flawed gems; used for Horadric Cube recipes
    "HoradricCube",    # the magical cube for combining items — core D2 mechanic
    "Transmute",       # putting items in the Horadric Cube and hitting Transmute
    "ThreePerfect",    # three perfect skulls in cube = something useful
]

# Deduplicate while preserving order
seen = set()
NAMES_DEDUPED = []
for n in NAMES:
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
    print(f"Checking {total} handles (dust2 variants + Diablo 2 era)...\n")
    print(f"{'#':>4}  {'CODE':>4}  {'RESULT':<10}  {'HANDLE':<25}  URL")
    print("-" * 110)

    available = []
    unavailable = []
    errors = []

    with requests.Session() as session:
        for i, name in enumerate(NAMES_DEDUPED, 1):
            r = check(name, session)

            if r["error"]:
                tag = "ERROR"
                errors.append(r)
            elif r["available"]:
                tag = "AVAILABLE"
                available.append(r)
            else:
                tag = "TAKEN"
                unavailable.append(r)

            code_str = str(r["status"]) if r["status"] else "ERR"
            print(f"[{i:>3}/{total}]  {code_str:>4}  {tag:<10}  {name:<25}  {r['url']}", flush=True)

            if i < total:
                time.sleep(DELAY)

    print("\n" + "=" * 110)
    print("SUMMARY")
    print("=" * 110)

    print(f"\n✅  AVAILABLE ({len(available)}):")
    for r in available:
        print(f"   {r['name']:<30}  {r['url']}")

    print(f"\n❌  TAKEN ({len(unavailable)}):")
    for r in unavailable:
        print(f"   {r['name']:<30}  {r['url']}")

    if errors:
        print(f"\n⚠️  ERRORS ({len(errors)}):")
        for r in errors:
            print(f"   {r['name']:<30}  {r['error']}")

    output = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "total": total,
        "available": [{"name": r["name"], "url": r["url"]} for r in available],
        "unavailable": [{"name": r["name"], "url": r["url"]} for r in unavailable],
        "errors": errors,
    }
    with open("rsi_handle_results_v5.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nFull results saved to rsi_handle_results_v5.json")


if __name__ == "__main__":
    main()
