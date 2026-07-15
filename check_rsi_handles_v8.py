#!/usr/bin/env python3
"""
RSI handle availability checker — batch 8.
Hunting for handles with the same energy as 'noclip':
  - Short, single-concept words
  - Console commands, config culture, deep CS/HL lore
  - Sounds cool even without context
  - 3+ chars, alphanumeric only
"""

import sys
import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── GoldSrc/HL/CS console commands WITHOUT underscores ──────────────────
    # (noclip lived in this category — these are its siblings)
    "notarget",      # makes AI enemies completely ignore you — noclip's sister command
    "timedemo",      # plays a demo at max FPS to benchmark your PC; every LAN gamer ran this
    "playdemo",      # play back a recorded .dem file; demo culture was huge in CS 1.6
    "developer",     # "developer 1" — turns on dev console spam; only nerds used this
    "unbindall",     # clears ALL your key bindings — the troll command people fell for
    "alias",         # create a command alias in config; every cs player made aliases
    "toggle",        # toggle a cvar in a single keybind; config nerd essential
    "getpos",        # get your exact map coordinates; used to make jump spot configs
    "setpos",        # teleport to exact coordinates; cheat server fun
    "heartbeat",     # sends a server heartbeat to master server; admin knowledge
    "listdemos",     # list .dem files in your cs folder
    "startdemos",    # start playing demos in a loop; HL startup culture
    "screenshot",    # take a screenshot via console — before F12 was a thing
    "record",        # start recording a .dem file: "record mydemo"
    "maps",          # list available maps on a server — typing it just to see
    "cvar",          # cvar = console variable; THE term for CS config settings
    "cfg",           # .cfg file extension — autoexec.cfg, config.cfg; iconic
    "buyscript",     # buy scripts that auto-purchased your loadout with one key
    "jumpscript",    # jump scripts for auto-bhop timing before bhop servers existed

    # ── CS 1.6 culture sites / tools ────────────────────────────────────────
    "fpsbanana",     # fpsbanana.com — where EVERY cs player downloaded custom maps/skins/sounds
    "fpsbananaa",    # just in case the main is taken — probably not worth it
    "cstrike",       # the actual folder name: steamapps/cstrike — the game itself
    "goldsrc",       # the Half-Life engine cs 1.6 runs on; deepest of cuts
    "goldsource",    # alternate GoldSrc spelling
    "hlss",          # Half-Life Sound Switcher — played custom sounds server-wide; everyone had it

    # ── Voice chat apps — "get on Vent" era ─────────────────────────────────
    "ventrilo",      # Ventrilo — THE voice chat app before TeamSpeak dominated; "get on vent"
    "teamspeak",     # TeamSpeak — the other VOIP; ts2/ts3 servers were everywhere
    "gamevox",       # GameVox — another VOIP client from the era
    "roger",         # Roger Wilco — one of the FIRST gaming voice chat apps

    # ── CS 1.6 / GoldSrc movement culture ───────────────────────────────────
    "strafejump",    # strafe jumping — directional air control movement
    "airstrafing",   # air strafing — changing direction mid-air
    "longstrafe",    # long strafes on surf ramps
    "walljump",      # jumping off walls in kz/climb maps
    "edgebug",       # the edgebug technique — crouching on an edge to negate fall damage
    "duckjump",      # duck jumping; crouching while jumping for extra height
    "circlejump",    # circle jump — the opening move of a bhop chain

    # ── CS 1.6 competitive / pro scene ──────────────────────────────────────
    "fragmovie",     # frag movie — the art form of CS 1.6; edited kill reels set to music
    "topfrag",       # top fragger — highest kill count in the match
    "prefire",       # pre-firing a corner before the enemy peeks it
    "wallbang",      # shooting through walls; knowing the wallbang spots was pro-tier
    "pixelwalk",     # pixel walking — standing on invisible pixel ledges in maps
    "skyboost",      # boosting through the skybox ceiling; a bug/technique
    "silent",        # silent aim; also "silentrun" style of peeking

    # ── Warcraft mod — the CS 1.6 level-up mod ──────────────────────────────
    "warcraftmod",   # the WC3 Warcraft 3 CS 1.6 mod — incredibly popular
    "wc3mod",        # shorter WC3 mod reference
    "chainlightning", # the chain lightning ability in the warcraft mod

    # ── CS 1.6 config/settings culture ──────────────────────────────────────
    "crosshair",     # crosshair settings — cs players spent hours on crosshair configs
    "sensitivity",   # mouse sensitivity — everyone had their "sens"
    "rawaccel",      # raw acceleration; mouse acceleration debate was legendary
    "rawinput",      # raw mouse input; turning off mouse accel was the holy grail
    "zoomratio",     # AWP zoom ratio settings
    "recoilscript",  # recoil compensation scripts; controversial

    # ── LAN party / internet cafe culture ───────────────────────────────────
    "lanparty",      # LAN party — playing cs in the same room as your friends
    "cybercafe",     # internet cafe — where many people first played cs 1.6
    "gameroom",      # the game room / LAN room at the back of a computer store
    "newegg",        # newegg.com — where everyone bought their LAN PC parts
    "frys",          # Fry's Electronics — the physical PC parts store of the era

    # ── Half-Life / Quake crossover (cs came from HL came from Quake) ───────
    "rocketjump",    # rocket jumping — the Quake technique that crossed into HL
    "railgun",       # the Quake railgun; most satisfying hitscan weapon in history
    "bunnytrack",    # the original name of KZ climb servers in HL
    "promode",       # Quake CPM/Challenge Promode — the competitive format

    # ── Other CS 1.6 terms that might have noclip energy ────────────────────
    "spraylogo",     # custom spray logos — every player had one
    "warmup",        # warmup round before a match
    "twoshot",       # two-shotting with a deagle or scout: style
    "flashedout",    # being fully flashed — unable to see
    "smokeout",      # using smokes to block vision
    "rushb",         # "RUSH B" — the most iconic CS callout; 5 chars
    "fullrush",      # full team rushing a site
    "econround",     # eco round — saving money
    "forceround",    # force buying when money is low

    # ── Steam/WON transition era (2003-2004) ─────────────────────────────────
    "wonnetwork",    # the WON (World Opponent Network) before Steam
    "steamapps",     # the SteamApps folder — where CS files lived
    "steamgames",    # Steam games directory
    "valveanti",     # Valve Anti-Cheat (VAC) nickname
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
    print(f"Checking {total} names — hunting for the next noclip...\n")
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
    with open("rsi_handle_results_v8.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v8.json")


if __name__ == "__main__":
    main()
