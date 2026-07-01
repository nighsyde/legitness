#!/usr/bin/env python3
"""
RSI handle availability checker — batch 7.
CS 1.6 console culture, server commands, mods, config culture,
weapons, voice lines, and general CS 1.6 DNA.
All names: 3+ chars, no punctuation.
404 = available. 200 = taken.
"""

import sys
import time
import requests
import json
from datetime import datetime

NAMES = [
    # ── Console commands — the ~ key culture ─────────────────────────────
    "Rcon",           # remote console — how admins managed servers; everyone knew this word
    "Autoexec",       # autoexec.cfg — the startup config every serious CS player customised
    "Impulse101",     # the Half-Life/CS cheat for all weapons; typed on every LAN server
    "Retry",          # reconnecting to a server after lag; typed constantly
    "Status",         # "status" in console to see who was on the server and their pings
    "Connect",        # "connect IP:port" — how you joined a server before Steam made it easy
    "ListMaps",       # listing available maps on a server
    "Changelevel",    # the admin command to change the map
    "Exec",           # executing a config file; "exec autoexec.cfg"
    "NetGraph",       # net_graph — the network overlay that showed ping and packet loss
    "Condump",        # condump.txt — dumping the console output to a file

    # ── CS 1.6 game mods — the custom server culture ──────────────────────
    "Jailbreak",      # the hugely popular mod — T's are prisoners, CTs are guards
    "GunGame",        # weapon progression mod — kill with each weapon to advance
    "ZombieMod",      # zombie mode — infected players chase survivors
    "DeathRun",       # obstacle course mod — one player triggers traps, others run
    "Surf",           # surf mod — sliding down ramps at speed; its own subculture
    "Furien",         # Furien mod — Ts have supernatural speed/powers, CTs try to stop them
    "Bhop",           # bunny hop — the movement technique and bhop-only servers
    "KZClimb",        # Kreedz Climbing — the CS climbing/parkour mod
    "HideNSeek",      # hide and seek mod
    "ScoutKnivez",    # the scout + knives low gravity map/mode (TAKEN from earlier but try clean)
    "MultiMod",       # multi-mod servers that ran different modes
    "AimMap",         # aim training maps — aim_headshot, aim_ak_colt
    "KnifeArena",     # knife fight arenas
    "PistolOnly",     # pistol only servers
    "AWPOnly",        # AWP sniper rifle only servers
    "HeadshotOnly",   # headshot only servers

    # ── CS 1.6 maps beyond dust2 ──────────────────────────────────────────
    "IceWorld",       # fy_iceworld — the chaotic fun map everyone ran to between serious games
    "PoolDay",        # fy_pool_day — pool area fun map; a classic
    "KnifeMap",       # generic knife map
    "Iceworld",       # lowercase variation

    # ── CS 1.6 weapons (as handles) ───────────────────────────────────────
    "Deagle",         # Desert Eagle — the skill-gap pistol (checking again, might differ)
    "USP",            # CT starting pistol — accurate and iconic
    "Glock",          # T starting pistol — full auto burst
    "AK47",           # the T rifle — most iconic weapon in CS
    "M4A1",           # CT rifle — the AK equivalent
    "Famas",          # CT French assault rifle — cheaper M4 alternative
    "Galil",          # T Israeli assault rifle — cheaper AK alternative
    "SG552",          # the scoped CT rifle — controversial and powerful
    "AWP",            # already checked but... the sniper
    "Scout",          # the cheap sniper — skill weapon, counter to AWP
    "Krieg",          # the SG552's other name
    "MAC10",          # the T submachine gun
    "MP5Navy",        # the CT submachine gun
    "TMP",            # the CT small SMG
    "P90",            # the spray-and-pray SMG
    "UMP45",          # the UMP — underrated SMG
    "HEGrenade",      # the explosive grenade
    "Flashbang",      # the flashbang (already checked — TAKEN)
    "SmokeGrenade",   # smoke grenade
    "Molotov",        # in later CS versions but culturally known
    "KevlarHelmet",   # the armour + helmet buy — "kevlar helmet"

    # ── CS 1.6 voice lines & audio ────────────────────────────────────────
    "BombPlanted",    # "The bomb has been planted" — one of the most recognisable game sounds
    "BombDefused",    # "The bomb has been defused" — relief
    "FireInHole",     # "Fire in the hole!" — the grenade callout
    "EnemySpotted",   # the voice command
    "CantSeeAnyone",  # another voice command
    "SniperMade",     # "Sniper made!" voice command
    "GetOutOfThere",  # voice command
    "NeedBackup",     # voice command
    "TerroristsWin",  # "Terrorists win" — the round end call
    "CTsWin",         # "Counter-Terrorists win"
    "RoundDraw",      # round draw
    "OvertimeStart",  # overtime

    # ── CS 1.6 server infrastructure ──────────────────────────────────────
    "HLStats",        # the Half-Life stats plugin that ranked players on servers
    "AMXMod",         # the AMX Mod X admin plugin that ran almost every server
    "Metamod",        # the Metamod plugin loader
    "VACBanned",      # getting hit with a VAC ban
    "SteamID",        # your Steam identification number
    "PunkBuster",     # the anti-cheat used by other games; CS players knew it from enemies
    "WonServer",      # the old WON (World Opponent Network) server era
    "DedicatedServer",# running your own dedicated server
    "ListenServer",   # a listen server (host also plays)
    "ServerBrowser",  # the in-game server browser
    "AllSeeingEye",   # the third party server browser app (already checked — AVAILABLE)
    "Gamespy",        # GameSpy server browser (already TAKEN)
    "Gotv",           # GOTV — the broadcast system

    # ── CS 1.6 player culture ─────────────────────────────────────────────
    "LeetClan",       # having a clan tag [LEET]
    "ClanWar",        # clan vs clan match
    "Scrim",          # scrimmage — competitive practice match
    "Pcw",            # pick up clan war — competitive practice term
    "PugMatch",       # pick up game match
    "FiveOnFive",     # 5v5 — the proper CS format
    "OneOnOne",       # 1v1 aim duel
    "KnifeDuel",      # settling disputes with a knife 1v1
    "HalfTime",       # the halftime team switch
    "OvertimeRound",  # overtime
    "MatchPoint",     # having match point
    "MapVeto",        # the map veto process in competitive matches
    "SideVeto",       # choosing CT or T side after winning knife round
    "TimeoutCall",    # calling a tactical timeout
]

# Deduplicate, enforce 3+ chars, no non-alphanumeric
import re
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
    print(f"Checking {total} CS 1.6 culture handles (3+ chars, alphanumeric only)...\n")
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
    with open("rsi_handle_results_v7.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v7.json")


if __name__ == "__main__":
    main()
