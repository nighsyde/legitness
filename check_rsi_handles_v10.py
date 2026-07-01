#!/usr/bin/env python3
"""
RSI handle availability checker — batch 10.
Broad sweep: WoW vanilla, Diablo 2, Warcraft 3 sounds, Ragnarok Online,
MapleStory, Flash gaming era, early 2000s online culture.
All names: 3+ chars, alphanumeric only.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── WORLD OF WARCRAFT — vanilla era (2004-2006) ──────────────────────
    # Zones — your first time in these stays with you
    "barrens",        # the zone + the infamous Barrens Chat (Chuck Norris jokes, Mr T jokes)
    "elwynn",         # Elwynn Forest — where every Alliance player began their adventure
    "westfall",       # the zone after Elwynn; Old Blanchy, Defias Brotherhood
    "duskwood",       # the creepy werewolf zone every player remembers
    "stranglethorn",  # Stranglethorn Vale — the PvP gank zone; most infamous leveling zone
    "tanaris",        # the desert zone; Gadgetzan, Zul'Farrak
    "ungoro",         # Un'Goro Crater — dinosaurs and devilsaurs
    "silithus",       # the bug zone at the end of the world
    "winterspring",   # the icy endgame zone; rare spawn hunting
    "felwood",        # the corrupted forest; gathering high-level herbs
    "ashenvale",      # early contested zone; Night Elf territory
    "redridge",       # the Alliance mid-level zone
    "lochmodan",      # the Dwarf zone
    "wetlands",       # the miserable run through crocolisks to get to Menethil

    # WoW instances — everyone has memories tied to specific dungeons
    "deadmines",      # the first Alliance dungeon; "WC? I know a shortcut" — the Van Cleef questline
    "wailing",        # Wailing Caverns — the first Horde dungeon; famous for getting lost
    "ragefire",       # Ragefire Chasm — tiny first Horde instance
    "scarlet",        # Scarlet Monastery — Cathedral, Library, Graveyard, Armory
    "stratholme",     # Strat — the undead city; Baron run for mount; the longest dungeon
    "scholomance",    # Scholo — the necromancer school; always confused with Strat
    "gnomeregan",     # the worst dungeon ever made — intentionally confusing, everyone got lost
    "uldaman",        # the archaeological dungeon no one wanted to run
    "mauradon",       # Maraudon — Horde-side instance, Princess Theradras
    "razorfen",       # Razorfen Kraul / Razorfen Downs
    "zulgurub",       # Zul'Gurub — the jungle troll 20-man raid; Hakkar the Soulflayer
    "moltencore",     # Molten Core — the first WoW 40-man raid; MC grind was legendary
    "blackwing",      # Blackwing Lair — Nefarian's raid; the hardest vanilla raid
    "onyxia",         # Onyxia's Lair — the dragon raid; famous wipe video "MOAR DOTS!"
    "naxxramas",      # Naxxramas — the original 40-man final raid; only 1% of players finished it
    "ahnqiraj",       # Ahn'Qiraj — the war effort raid; server-wide event to open it

    # WoW battlegrounds
    "warsong",        # Warsong Gulch — the classic capture the flag BG
    "arathibasin",    # Arathi Basin — 5-flag resource control BG
    "alterac",        # Alterac Valley — the 40v40 battleground that lasted for days

    # Famous WoW moments / culture
    "moardots",       # "MOAR DOTS! LESS DOTS!" — Onyxia wipe video; iconic raid leader meltdown
    "lessdots",       # the punchline from the same Onyxia wipe video
    "wipefest",       # a raid night of nothing but wiping; "we wiped 40 times tonight"
    "patchday",       # Tuesday patch days — servers down all morning, everyone anxious
    "realmdown",      # servers being down; the panic when your realm is offline
    "maintmode",      # maintenance mode; the WoW Tuesday ritual
    "donotagro",      # "don't agro!" — pulling too much and wiping the group

    # WoW classes (long shots but checking)
    "paladin",        # the class every teenager wanted; "pala" culture
    "warlock",        # the dark caster; demonic magic
    "druid",          # the shapeshifter; feral druid gankers
    "shaman",         # horde-only in vanilla; coveted for totem buffs
    "rogue",          # the ganker; cheap shot, kidney shot, vanish, repeat
    "hunter",         # "huntard" — the class with the reputation
    "warrior",        # the tank everyone wanted but nobody played correctly

    # ── WARCRAFT 3 — unit sounds / quotes ────────────────────────────────
    # Every WC3 player clicked their units obsessively until they complained
    "zugzug",         # Orc Peon affirmative — "zug zug" — clicked too many times
    "dabu",           # Orc grunt/thrall affirmative — "dabu" (I obey)
    "workwork",       # Orc Peon "work work" — the WC3 peon's resigned complaint
    "soisay",         # "so I say" — the Orc's sarcastic line when overclicked
    "unitready",      # "your unit is ready" — the notification sound
    "aiur",           # Protoss home world (StarCraft) — "My life for Aiur!"
    "whatyouwant",    # "What do you want?" — WC3 unit idle response

    # ── DIABLO 2 — builds, culture, bosses ───────────────────────────────
    "mephisto",       # the boss in Act 3 everyone farmed for set items
    "pindleskin",     # the easiest Ber rune farm boss; the "pindle run"
    "andariel",       # Act 1 boss "Maiden of Anguish" — farmed by low-level chars
    "duriel",         # the maggot lair Act 2 boss everyone hated on a hardcore char
    "hammerdin",      # the Hammerdin Paladin build — broken, overpowered, used by everyone
    "javzon",         # Javazon — the Amazon build using Lightning Fury
    "meteorb",        # the Meteorb Sorceress build — Fire/Cold hybrid
    "trapsin",        # the Trapsin Assassin — lightning traps build
    "winddruid",      # the Wind Druid — Tornado + Hurricane
    "mfrun",          # "Magic Find run" — farming for rare items
    "fullclear",      # clearing every monster on a map before moving on
    "hardcore",       # Hardcore mode — you die once, character deleted; the ultimate stakes
    "softcore",       # Normal/softcore — "you don't play HC? casual"
    "ladder",         # the D2 ladder season — fresh economy, race to top
    "nonladder",      # non-ladder characters (legacy, out of season economy)
    "bnetjoin",       # "join" on Battle.net — the game list with channel names like "cow run 1/8"

    # ── RAGNAROK ONLINE — the beloved Korean MMORPG ──────────────────────
    "prontera",       # the main hub city; the Times Square of Ragnarok Online
    "midgard",        # the world of Ragnarok Online
    "geffen",         # the magic city; where mage/wizard players hung out
    "payon",          # the archer town; peaceful forest town
    "aldebaran",      # the clock tower town; famous for Clock Tower dungeon

    # ── MAPLESTORY — the side-scrolling 2D MMORPG ────────────────────────
    "henesys",        # the bowman town; where new players met and trained
    "orbis",          # the sky island city; reached by boat or taxi
    "leafre",         # the dragon town; high-level zone
    "zakum",          # the Zakum boss — the first big group boss in MapleStory
    "ellinia",        # the magic forest town; where magicians trained

    # ── FLASH GAMING / NEWGROUNDS ERA ────────────────────────────────────
    "newgrounds",     # Newgrounds.com — the Flash animation/game hub of the early internet
    "miniclip",       # Miniclip.com — THE Flash gaming website of the early 2000s
    "addicting",      # AddictingGames.com — another huge Flash gaming portal
    "kongregate",     # Kongregate — the later Flash gaming site with achievements
    "shockwave",      # Shockwave.com — another Flash gaming portal
    "flashgame",      # a Flash game; the genre that defined browser gaming
    "stickdeath",     # StickDeath.com — stick figure violence animations; very early 2000s
    "xiao",           # Xiao Xiao — the famous stick figure fighting Flash series
    "tankgame",       # the classic tank Flash games

    # ── HABBO HOTEL — early virtual world ────────────────────────────────
    "habbo",          # Habbo Hotel — the virtual world with pixel avatars everyone used
    "furni",          # the Habbo furniture (in-game currency/items)
    "habbocoin",      # Habbo coins (the premium currency before microtransactions were common)

    # ── GENERAL EARLY 2000s ONLINE PC GAMING CULTURE ─────────────────────
    "wipeparty",      # a raid wipe night; "wipeparty tonight boys"
    "guildwars",      # Guild Wars 1 — the B2P MMO alternative to WoW
    "lineage",        # Lineage 2 — the hardcore Korean MMO
    "everquest",      # EverQuest — the first big 3D MMORPG, WoW's predecessor
    "norrath",        # the EverQuest world — "citizen of Norrath"
    "britannia",      # Ultima Online world — one of the first online RPG worlds
    "uo",             # Ultima Online abbreviated (2 chars... actually too short - just 2)
    "daoc",           # Dark Age of Camelot abbreviated (4 chars)

    # ── FUNNY RELATABLE ONLINE GAMING MOMENTS ────────────────────────────
    "spawncamp",      # spawn camping — killing players as soon as they respawn
    "teamkill",       # TK — team killing; the instant ban / vote kick trigger
    "votekick",       # vote to kick a player from the server
    "griefer",        # a griefer — someone who ruins the game for others
    "lurker",         # a lurker — someone who watches without participating
    "leech",          # a leech — leeching XP without contributing
    "lootwhore",      # someone who takes all the loot; "that guy is a loot whore"
    "ninjaloot",      # ninja looting — taking loot that wasn't yours
    "rollgreed",      # rolling Greed on items you don't need
    "rollneed",       # rolling Need on everything; the classic WoW drama
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
    print(f"Checking {total} handles — WoW/D2/WC3/RO/MS/Flash/early MMO culture...\n")
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
    with open("rsi_handle_results_v10.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v10.json")


if __name__ == "__main__":
    main()
