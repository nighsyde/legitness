#!/usr/bin/env python3
"""
RSI handle checker — batch 18.
FPS deep dive: Quake/UT pro players, Doom 2 monsters, Tribes culture,
Battlefield 1942, Medal of Honor, Day of Defeat, UT99 maps/weapons,
Quake maps, Rainbow Six, and the FPS mechanics that defined the era.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── QUAKE PRO PLAYERS — the legends of competitive FPS ───────────────
    # Thresh and Fatal1ty are checked. These are the next tier.
    "Cooller",        # Anton Singov — dominant Russian Quake player; won everything for years
    "Cypher",         # Daniil Islamov — the Macedonian Quake genius; "The Terminator"
    "Toxjq",          # Johan Quick — Swedish Quake pro; one of the cleanest players ever
    "ZeRo4",          # Eric Lafleur — Canadian Quake pro; hugely respected
    "Strenx",         # Filip Lundqvist — Quake Live legend; aggressive playstyle
    "Rapha",          # Sean Plott — wait, rapha is Shane Hendrixson; Quake World Champ
    "Vo0",            # Sander Kaasjager — UT legend; 2 World Cyber Games UT golds
    "Socrates",       # the legendary FPS player handle

    # ── QUAKE MAP NAMES — the arenas that defined competitive FPS ────────
    "Aerowalk",       # THE most famous competitive Quake 1v1 map; by Preacher (1998)
                      # Played at every major Quake tournament for 20+ years
    "Bloodrun",       # Blood Run — the Q3/QL map; also one of the greats
    "Campgrounds",    # DM6: "The Campgrounds" — the original Quake deathmatch classic
    "Longestyard",    # DM17: "Longest Yard" — the gravity-reduced Q3 map
    "Phrantic",       # the Quake map by Preacher; same creator as Aerowalk

    # ── UNREAL TOURNAMENT — weapons, maps, modes ─────────────────────────
    "ShockRifle",     # the UT Shock Rifle — primary/secondary combo was skill-defining
    "ShockCombo",     # the Shock Combo — hitting your own orb with the beam; instakill
    "LinkGun",        # the UT Link Gun — healed teammates, linked fire with allies
    "Translocator",   # the UT teleportation device — used for movement and map control
    "FacingWorlds",   # CTF-Face (Facing Worlds) — THE iconic UT CTF map with two spires
    "Morpheus",       # DM-Morpheus — rooftop battle between three skyscrapers; iconic
    "Deck16",         # DM-Deck16 — one of the most played UT deathmatch maps
    "Phobos2",        # DM-Phobos2 — classic UT level
    "Biolauncher",    # the Bio Rifle — organic projectile weapon; underrated
    "Ripper",         # the Ripper — circular saw blade launcher; iconic to UT
    "Pulsegun",       # the Pulse Gun — short-range arc weapon

    # ── DOOM 2 MONSTERS — iconic enemies that defined FPS culture ────────
    # Doom/Doom 2 monsters are ingrained in FPS history
    "Archvile",       # the Arch-Vile — the most feared Doom 2 enemy; resurrects dead
                      # monsters and blasts you with fire; every speedrunner's nightmare
    "Revenant",       # skeleton with shoulder-mounted homing missiles; pure menace
                      # the screaming rocket skeleton; universally hated/respected
    "Cacodemon",      # the round floating demon with one eye; iconic Doom design
                      # appears in virtually every Doom list as a fan favorite
    "Mancubus",       # the fat demon with twin flamethrowers; walls of fire
    "Cyberdemon",     # the final boss of Doom — rocket launcher + cybernetic legs
    "Arachnotron",    # spider-like robot with plasma gun; basically a mini-Spider Mastermind
    "Chaingunner",    # the heavy weapon dude with the chaingun; can shred you instantly
    "Painelemental",  # Pain Elemental — floats and spawns Lost Souls; hated
    "Hellknight",     # the green Baron of Hell variant; tougher than Imps

    # ── TRIBES — the jetpack FPS with skiing movement ────────────────────
    # Multiple references in the "lost vocabulary" Reddit thread
    "Skiing",         # the Tribes movement mechanic — sliding down slopes to gain speed
                      # skiing culture was its own world; "real Tribes players ski"
    "Spinfusor",      # the Disc Launcher in Tribes 2/Ascend — the primary weapon
                      # hitting a moving target mid-air with a disc was the skill ceiling
    "Flagcapper",     # the flag runner in Tribes CTF; the most important role
    "Bioderm",        # the player character type in Starsiege: Tribes
    "Elf",            # the ELF Gun (Energy Rifle) in Tribes — the jamming weapon
    "Pathfinder",     # the light armor class in Tribes — speed over armor

    # ── BATTLEFIELD 1942 / WWII FPS ERA ──────────────────────────────────
    # BF1942 was a major LAN party game; multiplayer on local area networks
    "BF1942",         # Battlefield 1942 abbreviated — a classic LAN staple
    "Conquest",       # the Battlefield game mode — capturing control points
    "Ticketbleed",    # the Battlefield ticket system — losing tickets by dying or losing flags
    "WakeIsland",     # Wake Island — the most iconic BF1942 map
    "Guadalcanal",    # the BF1942 Pacific island map
    "ElAlamein",      # the BF1942 North Africa map
    "Omaha",          # Omaha Beach — the D-Day map in MOHAA and BF

    # ── MEDAL OF HONOR ALLIED ASSAULT (MOHAA) ────────────────────────────
    # Released 2002; predated CoD; the go-to WWII multiplayer FPS
    "MOHAA",          # the game abbreviation; anyone who played it knows
    "OmahaBeach",     # the legendary D-Day mission in MOHAA; impossibly hard
    "Spearhead",      # Medal of Honor: Spearhead — the expansion pack

    # ── DAY OF DEFEAT ────────────────────────────────────────────────────
    # The WWII HL mod that ran alongside CS 1.6 on the same servers
    "DayofDefeat",    # Day of Defeat — the WWII HL mod
    "DoD",            # abbreviated (3 chars)
    "Avalanche",      # dod_avalanche — one of the iconic DoD maps
    "Anzio",          # dod_anzio — the Italian map

    # ── AMERICA'S ARMY ────────────────────────────────────────────────────
    # Free-to-play US Army recruitment FPS; massive in the early 2000s
    "AmericasArmy",   # the game; "AA" was what everyone called it
    "SFQualify",      # the Special Forces qualification course in AA

    # ── RAINBOW SIX ──────────────────────────────────────────────────────
    "RainbowSix",     # Tom Clancy's Rainbow Six — the tactical FPS that preceded Siege
    "Rogue Spear",    # Rogue Spear — the R6 sequel/spinoff
    "RogueSpear",     # one word version

    # ── OPERATION FLASHPOINT ─────────────────────────────────────────────
    # The hardcore military sim FPS from 2001; predecessor to ARMA
    "Flashpoint",     # Operation Flashpoint — the realistic military FPS
    "Resistance",     # Operation Flashpoint: Resistance — the expansion

    # ── COUNTERSTRIKE SOURCE / CSS ────────────────────────────────────────
    "cstrikesource",  # CS: Source — the Source engine version
    "cssource",       # abbreviated
    "surfmap",        # surf maps in CS:S — the surfing mod; its own culture
    "bhopping",       # bunny hopping — the main surf skill

    # ── FPS MECHANICS / TECHNIQUES WE HAVEN'T CHECKED ────────────────────
    "Strafe50",       # CPMA strafe jumping to 50 speed — Quake challenge mode term
    "AirStrafe",      # air strafing — directional control in the air; Quake movement
    "WallStrafe",     # wall strafing — bouncing off walls for speed
    "Bhopchain",      # bunny hop chain — a series of successful bhops
    "Walljumping",    # wall jumping — off walls in KZ maps
    "PerfectStrafe",  # the perfect strafe jump; maximum speed
    "Doubletap",      # double tapping a key — a technique
    "Flicking",       # flick shot — fast snap aim
    "Prefiring",      # pre-firing a corner before peeking

    # ── SPECIFIC CS 1.6 PLAYER HANDLES (real pros) ───────────────────────
    "SpawN",          # the legendary SweeperN — wait it's SpawN — Abdisamad Mohamed
    "Fisker",         # Patrik Ljungberg — the swedish CS player
    "Potti",          # Ola Lindqvist — Swedish CS legend
    "cArn",           # Patrik Sättermon — NiP's in-game leader
    "Walle",          # Emil Christensen — Swedish CS pro
    "Hyper",          # Christopher Lund Nygaard — Norwegian CS pro
    "Ave",            # Arpad Vadkerti — Hungarian CS pro
    "Zonic",          # Finn Björnvig — CS player turned coach
    "Elemenoopy",     # a famous early CS handle

    # ── ESPORTS ORGANIZATIONS FROM THAT ERA ──────────────────────────────
    "Fnatic",         # Fnatic — the CS/UT team that became one of gaming's biggest orgs
    "Compexity",      # compLexity Gaming — abbreviated
    "EvilGeniuses",   # Evil Geniuses — one of the oldest NA esports orgs
    "mousesports",    # the German esports org
    "Virtuspro",      # Virtus.pro — the European esports org
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
    print(f"Checking {total} FPS-focused handles...\n")
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
    with open("rsi_handle_results_v18.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v18.json")


if __name__ == "__main__":
    main()
