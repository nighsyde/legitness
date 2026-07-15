#!/usr/bin/env python3
"""
RSI handle availability checker — batch 4.
Nostalgic map names: CS, TF2/TFC, Halo 1 & 2, Quake, Unreal Tournament.
404 = available. 200 = taken.
"""

import sys
import time
import requests
import json
from datetime import datetime

NAMES = [
    # ── Counter-Strike maps ───────────────────────────────────────────────
    # (how players actually referred to them, no prefix)
    "Inferno",       # de_inferno — arguably CS's most beloved map
    "Nuke",          # de_nuke — the multi-level classic
    "Train",         # de_train — industrial, gritty, iconic
    "Aztec",         # de_aztec — the jungle temple
    "Cobblestone",   # de_cbble
    "Cache",         # de_cache — modern classic
    "Mirage",        # de_mirage — the rooftop village
    "Italy",         # cs_italy — hostage map everyone loved
    "Office",        # cs_office — the office hostage map
    "Assault",       # cs_assault — the warehouse
    "Militia",       # cs_militia — house + yard
    "Prodigy",       # de_prodigy — CS 1.6 classic
    "Tuscan",        # de_tuscan — beloved CS 1.6 community map
    "Piranesi",      # de_piranesi — ancient temple, CS 1.6
    "Chateau",       # de_chateau — the French castle
    "Tides",         # de_tides — CS 1.6 classic
    "Depot",         # de_depot — train depot
    "Season",        # de_season — community classic
    "Vertigo",       # de_vertigo — rooftop skyscraper
    "Overpass",      # de_overpass
    "Breach",        # de_breach

    # ── Team Fortress 2 / TFC maps ────────────────────────────────────────
    "TwoFort",       # 2fort — THE TF2 map; everyone has played this
    "Dustbowl",      # cp_dustbowl — attack/defend staple
    "Badlands",      # cp_badlands — competitive classic
    "Granary",       # cp_granary — the wheat silos map
    "Gravelpit",     # cp_gravelpit — TFC/TF2 classic
    "Goldrush",      # pl_goldrush — first payload map
    "Badwater",      # pl_badwater — payload staple
    "Upward",        # pl_upward — mountain payload
    "Hydro",         # cp_hydro — the hydro plant
    "Gorge",         # cp_gorge
    "Coldfront",     # cp_coldfront
    "Mercenary",     # mercenary park
    "Barnblitz",     # pl_barnblitz
    "Hightower",     # plr_hightower — the chaos map
    "Mannhattan",    # mannhattan — halloween map

    # ── Halo: Combat Evolved (CE) multiplayer maps ────────────────────────
    "BloodGulch",    # the most iconic Halo map; Red vs Blue was filmed here
    "HangEmHigh",    # the western-themed classic
    "Sidewinder",    # the snowy outdoor CTF map
    "Damnation",     # the classic multi-level indoor map
    "Longest",       # the two-platform bridge map; sniper duels forever
    "Prisoner",      # the pyramid-shaped map; everyone fell off the sides
    "BattleCreek",   # the valley with rocks; classic CTF
    "ChillOut",      # the indoor maze; extremely competitive
    "Wizard",        # the four-way symmetric map; chaotic and perfect
    "RatRace",       # the indoor race track map
    "Chiron",        # the test facility; confusing layout
    "Infinity",      # the outdoor river map with active camo
    "DeathIsland",   # the island; sniping across water
    "IceFields",     # the frozen outdoor CTF map
    "Gephyrophobia",  # bridge map; fear of bridges literally in the name
    "BoardingAction", # the two ships in space

    # ── Halo 2 multiplayer maps ───────────────────────────────────────────
    "Lockout",       # THE Halo 2 map for competitive; everyone has memories here
    "Midship",       # the curved ship interior; tight and lethal
    "Zanzibar",      # the beach base with the spinning wheel
    "Ascension",     # the dish antenna map; sniper haven
    "Headlong",      # the rooftop city; chaotic and huge
    "Coagulation",   # the Halo 2 Blood Gulch remake
    "Foundation",    # the symmetrical box; pure mayhem
    "IvoryTower",    # the vertical indoor map with the lift
    "Colossus",      # the symmetric two-base map
    "BurialMounds",  # the outdoor desert map
    "Terminal",      # the train station map; trains killed people
    "Sanctuary",     # the outdoor ruins map
    "BeaverCreek",   # Halo 2 remake of Battle Creek
    "Turf",          # the urban alleyway map
    "Waterworks",    # the huge outdoor water pipes map
    "Gemini",        # the two-tower symmetric map

    # ── Quake 3 / QuakeWorld maps ─────────────────────────────────────────
    "Aerowalk",      # legendary custom Quake map; played in every major tournament
    "Campgrounds",   # Q3DM6 nickname — the most-played Quake 3 map of all time
    "Toxicity",      # Quake 3 competitive map
    "Ztn",           # Ztn2dm3 — legendary Quake 3 duel map
    "Phrantic",      # Q3 map; name says it all
    "Cpm1a",         # CPMA competitive Quake map

    # ── Unreal Tournament 1999 / 2004 maps ───────────────────────────────
    "FacingWorlds",  # CTF-Face][ — the two-tower CTF map; most iconic UT map ever
    "Morpheus",      # DM-Morpheus — the skyscraper map with rocket jumps between buildings
    "DeckSixteen",   # DM-Deck16][ — the industrial catwalk deathmatch map
    "Phobos",        # DM-Phobos — the space station
    "Stalwart",      # DM-Stalwart
    "Rankin",        # DM-Rankin — UT2004 1v1 competitive staple
    "Asbestos",      # DM-Asbestos — UT2004
    "LavaGiant",     # CTF-LavaGiant — giant lava CTF map
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
    print(f"Checking {total} map names for RSI handle availability...\n")
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
    print("RESULTS BY GAME")
    print("=" * 110)

    cs_maps   = [r for r in available if r["name"] in [
        "Inferno","Nuke","Train","Aztec","Cobblestone","Cache","Mirage",
        "Italy","Office","Assault","Militia","Prodigy","Tuscan","Piranesi",
        "Chateau","Tides","Depot","Season","Vertigo","Overpass","Breach"]]
    tf_maps   = [r for r in available if r["name"] in [
        "TwoFort","Dustbowl","Badlands","Granary","Gravelpit","Goldrush",
        "Badwater","Upward","Hydro","Gorge","Coldfront","Mercenary",
        "Barnblitz","Hightower","Mannhattan"]]
    h1_maps   = [r for r in available if r["name"] in [
        "BloodGulch","HangEmHigh","Sidewinder","Damnation","Longest",
        "Prisoner","BattleCreek","ChillOut","Wizard","RatRace","Chiron",
        "Infinity","DeathIsland","IceFields","Gephyrophobia","BoardingAction"]]
    h2_maps   = [r for r in available if r["name"] in [
        "Lockout","Midship","Zanzibar","Ascension","Headlong","Coagulation",
        "Foundation","IvoryTower","Colossus","BurialMounds","Terminal",
        "Sanctuary","BeaverCreek","Turf","Waterworks","Gemini"]]
    q_maps    = [r for r in available if r["name"] in [
        "Aerowalk","Campgrounds","Toxicity","Ztn","Phrantic","Cpm1a"]]
    ut_maps   = [r for r in available if r["name"] in [
        "FacingWorlds","Morpheus","DeckSixteen","Phobos","Stalwart",
        "Rankin","Asbestos","LavaGiant"]]

    for label, group in [
        ("Counter-Strike", cs_maps),
        ("Team Fortress 2 / TFC", tf_maps),
        ("Halo CE", h1_maps),
        ("Halo 2", h2_maps),
        ("Quake", q_maps),
        ("Unreal Tournament", ut_maps),
    ]:
        if group:
            print(f"\n✅  {label} — AVAILABLE:")
            for r in group:
                print(f"   {r['name']:<25}  {r['url']}")

    print(f"\n\n✅  ALL AVAILABLE ({len(available)}):")
    for r in available:
        print(f"   {r['name']:<25}  {r['url']}")

    print(f"\n❌  TAKEN ({len(unavailable)}):")
    for r in unavailable:
        print(f"   {r['name']:<25}  {r['url']}")

    output = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "total": total,
        "available": [{"name": r["name"], "url": r["url"]} for r in available],
        "unavailable": [{"name": r["name"], "url": r["url"]} for r in unavailable],
        "errors": errors,
    }
    with open("rsi_handle_results_v4.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nFull results saved to rsi_handle_results_v4.json")


if __name__ == "__main__":
    main()
