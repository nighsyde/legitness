#!/usr/bin/env python3
"""
RSI handle availability checker — batch 9.
Broad sweep: early 2000s online PC multiplayer culture.
Cheat codes, memes, gaming slang, games, platforms, trash talk,
leet speak, download culture, RS, AoE, UT, Doom, SC, Quake.
All names: 3+ chars, alphanumeric only.
"""

import sys
import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── DOOM cheat codes — the OG of cheat culture ───────────────────────
    # These are the most iconic cheat codes in gaming history
    "iddqd",          # DOOM god mode — typed by every PC gamer in the 90s/early 2000s
    "idkfa",          # DOOM all weapons + keys + full ammo — the loadout cheat
    "idclip",         # DOOM noclip — the GRANDFATHER of noclip; walk through walls in Doom
    "idspispopd",     # DOOM 1 original noclip — ultra obscure, maximum cred
    "idchoppers",     # DOOM chainsaw cheat — gives you the chainsaw
    "iddt",           # DOOM automap reveal — shows all map secrets
    "idbeholds",      # DOOM berserk cheat — one-shot fists
    "idbeholdv",      # DOOM invincibility cheat

    # ── CLASSIC GAME cheat codes ──────────────────────────────────────────
    "hesoyam",        # GTA San Andreas — health, armor, money cheat; everyone used it
    "rocketman",      # GTA SA jetpack cheat; or just the general 'rocket man'
    "lxgiwyl",        # GTA SA weapons tier 1 cheat
    "motherlode",     # The Sims — the $50,000 money cheat; even non-gamers know this one
    "rosebud",        # The Sims 1 — the original $1,000 cheat; followed by !;!;!;!;
    "klapaucius",     # The Sims 1 original money cheat before rosebud patched it
    "moveobjects",    # The Sims — "moveobjects on" — god tier cheat for placing furniture
    "boolprop",       # The Sims 2 testing cheats prefix — unlocks hidden game options

    # ── AGE OF EMPIRES cheat codes ────────────────────────────────────────
    "wololo",         # AoE monk conversion sound — became one of gaming's most iconic memes
    "bigdaddy",       # AoE 1 — spawns the sports car with a rocket launcher; incredible
    "photonman",      # AoE 1 — spawns the laser guy unit; amazing for a 1997 game
    "diediedie",      # AoE 1 — kills all animals/units; pure chaos
    "coinage",        # AoE 1 — gives gold
    "aegis",          # AoE — enables instant building; everything builds in a second
    "pepperoni",      # AoE 2 — gives food ("PEPPERONI PIZZA")
    "woodstock",      # AoE 2 — gives wood
    "lumberjack",     # AoE 2 — gives 1000 wood; known by every AoE 2 player
    "robin",          # AoE 2 wood cheat ("robin hood")
    "robinhood",      # AoE 2 — gives gold and wood

    # ── STARCRAFT culture ─────────────────────────────────────────────────
    "zergrush",       # THE StarCraft meme — "zerg rush kekeke" — one of the first gaming memes
    "kekeke",         # the Zerg player's laugh/taunt sound — pure nostalgia
    "terran",         # the Terran race in StarCraft
    "protoss",        # the Protoss race — "you must construct additional pylons"
    "broodwar",       # StarCraft: Brood War — the expansion that defined competitive gaming
    "scbw",           # short for StarCraft Brood War
    "noglues",        # StarCraft cheat — gives money; very specific
    "ophelia",        # StarCraft cheat — skip to any mission
    "stickyrice",     # StarCraft cheat — gives Terran minerals+gas

    # ── ALL YOUR BASE ARE BELONG TO US (2001) ────────────────────────────
    # THE defining internet gaming meme of 2001; from Zero Wing (1992)
    "allurbase",      # "All your base are belong to us"
    "zerowing",       # the game the AYB meme came from
    "movezig",        # "For great justice. Move ZIG." — the iconic AYB line
    "somebodyset",    # "Somebody set up us the bomb"

    # ── Leet speak / early internet gaming slang ─────────────────────────
    "1337",           # leet / elite in number form — the entire subculture
    "leet",           # elite in leet speak
    "haxxor",         # hacker in leet speak — "haxxor!"
    "h4x0r",          # another leet spelling of hacker
    "w00t",           # the early internet celebration — "w00t!" = woot
    "woot",           # cleaned-up version; still sounds era-correct
    "roflmao",        # ROFL + LMAO combined — a classic from AIM/MSN Messenger era
    "lulz",           # plural of "lol" — used to mean laughs/chaos; "for the lulz"

    # ── Gaming slang from early 2000s multiplayer ────────────────────────
    "ownage",         # being owned — "pure ownage"; also the web series
    "ragequit",       # leaving the game in anger — universal term
    "tryhard",        # playing too seriously in a casual game
    "griefing",       # deliberately ruining a teammate's game
    "smurfing",       # high-skill player on a low-level account
    "ganked",         # ambushed by multiple enemies; WoW PvP/DOTA term
    "ganking",        # the act of ganking
    "killsteal",      # stealing a kill from a teammate
    "feeding",        # dying so much you feed the enemy resources
    "fragged",        # killed (from Quake/Doom fraggin')
    "gibbed",         # blown up so hard you left gibs; Quake/Doom specific
    "respawned",      # coming back after death
    "camping",        # sitting in one spot to get kills (already checked)
    "deranked",       # losing rank/MMR; competitive gaming term
    "smurf",          # the smurf account itself
    "salty",          # being bitter after a loss — "he's so salty"
    "tilted",         # on tilt; playing badly due to frustration

    # ── 4-char internet gaming shorthands ────────────────────────────────
    "ggez",           # "gg easy" — the ultimate post-win trash talk
    "glhf",           # "good luck have fun" — pre-game ritual
    "ggwp",           # "good game well played" — the sportsmanlike version
    "brb",            # "be right back" — AIM era into gaming (3 chars)
    "afk",            # "away from keyboard" — (3 chars)
    "ftw",            # "for the win" — (3 chars)
    "kek",            # WoW cross-faction "lol" — Horde typing LOL showed as KEK to Alliance
    "kekw",           # the evolved Twitch emote form of kek

    # ── QUAKE / id Software culture ───────────────────────────────────────
    "quad",           # Quad Damage — the power-up that makes you 4x damage; iconic
    "gibs",           # the bloody pieces left after a massive explosion in Quake
    "instagib",       # one-hit-kill game mode from UT/Quake — pure adrenaline
    "railgun",        # the Quake railgun — most satisfying weapon in FPS history
    "rocketjump",     # rocket jumping — the technique that defined FPS movement

    # ── UNREAL TOURNAMENT culture ─────────────────────────────────────────
    "redeemer",       # UT's nuclear rocket — the most satisfying weapon in UT
    "flakcannon",     # UT's close-range devastator — the shredder
    "udamage",        # UT's damage amplifier powerup — "U-Damage"

    # ── RUNESCAPE — the browser MMORPG of the early 2000s ────────────────
    "phat",           # "party hat" — the rarest RS item; owning a phat was everything
    "partyhat",       # the full name; dropped during 2001 Xmas event never repeated
    "barrows",        # Barrows minigame — the dungeon with armor sets named after brothers
    "wildy",          # the Wilderness — the PvP zone where you could lose everything
    "varrock",        # the main city; first place most players went after tutorial island
    "lumbridge",      # the starting city; where you spawned when you died
    "edgeville",      # the last town before the Wilderness; pkers gathered here
    "rune",           # rune equipment — the best F2P gear; "full rune" was the dream
    "trimmed",        # trimmed armor — cosmetic upgrade that showed you were a member
    "whip",           # the Abyssal Whip — the best training weapon for years
    "scimitar",       # the rune scimitar — best F2P weapon, fastest attack speed
    "lobster",        # the lobster — best F2P food; "I only eat lobbies"
    "dds",            # Dragon Dagger (s) — the spec weapon everyone used for PvP
    "firecape",       # the Fire Cape — reward from TzTok-Jad fight; the ultimate flex
    "tokkul",         # the TzHaar currency; "selling firecape for tokkul"
    "skillcape",      # 99 skill cape — the max-level achievement; huge flex
    "falador",        # the white knight city in RS
    "guthix",         # the god of balance in RS
    "zamorak",        # the god of chaos in RS
    "saradomin",      # the god of order in RS

    # ── DOWNLOAD / GAMING CULTURE SITES from early 2000s ─────────────────
    "fileplanet",     # fileplanet.com — you waited in a QUEUE to download game demos/mods
    "kazaa",          # Kazaa — the P2P file sharing app everyone used (and got viruses from)
    "napster",        # Napster — the OG music piracy site; shut down in 2001
    "limewire",       # LimeWire — Kazaa's successor; downloaded music with extra viruses
    "bearshare",      # BearShare — another P2P client
    "gotfrag",        # GotFrag.com — the CS/esports news and demo site
    "gamespy",        # GameSpy — the gaming network/server browser (probably taken)

    # ── LEEROY JENKINS (2005 WoW video, but defining early internet era) ──
    "leeroy",         # "LEEEEROYYYY JENKINS" — the most famous WoW video
    "jenkins",        # the last name; often used alone to reference the meme

    # ── MISC EARLY 2000s MULTIPLAYER ─────────────────────────────────────
    "lagswitch",      # using a physical device to cause lag spikes and escape death
    "lagfest",        # a server so laggy everyone suffered
    "packetloss",     # packet loss — the bane of early broadband gaming
    "dialup",         # dial-up internet — the era before broadband; the modem sound
    "clanbase",       # ClanBase — the European competitive CS/UT/Q3 ladder
    "esreality",      # ESReality — the Quake/esports forum and news site
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
    print(f"Checking {total} early-2000s PC multiplayer culture handles...\n")
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
    with open("rsi_handle_results_v9.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v9.json")


if __name__ == "__main__":
    main()
