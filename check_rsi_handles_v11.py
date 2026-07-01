#!/usr/bin/env python3
"""
RSI handle availability checker — batch 11.
Expanding on what worked: WoW bosses/zones/culture, UT/Q3 announcer words,
Half-Life, Morrowind, Baldur's Gate, C&C Red Alert, Deus Ex, more MMO culture.
All names: 3+ chars, alphanumeric only.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── WoW vanilla — iconic bosses & NPCs ───────────────────────────────
    "ragnaros",       # Molten Core boss — "BY FIRE BE PURGED!" — one of WoW's most iconic moments
    "nefarian",       # Blackwing Lair boss — taunted the raid throughout the fight
    "hakkar",         # Zul'Gurub boss; also caused the Corrupted Blood incident (2005)
    "hogger",         # the elite gnoll near Goldshire that killed low-level players; a running joke
    "murloc",         # the amphibious creatures; "mrglglgl" — beloved/hated WoW meme creature
    "mrglglgl",       # the murloc battle cry/panic sound — every WoW player knows this sound
    "defias",         # the Defias Brotherhood — the Deadmines crime organization
    "vankleef",       # Edwin VanCleef — the Deadmines final boss; memorable villain
    "quilboar",       # the pig-men in Barrens that early players fought constantly
    "kobold",         # "You no take candle!" — the kobold mining creatures in early zones

    # ── WoW vanilla — capital cities ────────────────────────────────────
    "orgrimmar",      # Horde capital — where the auction house was and pvp queued
    "ironforge",      # Alliance/Dwarf capital — the big AH hub in vanilla
    "stormwind",      # Human/Alliance capital — the iconic castle city
    "undercity",      # Undead Forsaken capital — underground, eerie, unique
    "darnassus",      # Night Elf capital — only accessible by boat or flight
    "goldshire",      # the small Human town near Stormwind; infamous for the Lion's Pride Inn

    # ── WoW vanilla — zone nostalgia ────────────────────────────────────
    "darkshore",      # Night Elf leveling zone — the coast with the long run
    "dustwallow",     # Dustwallow Marsh — the swamp zone with Onyxia's lair entrance
    "hillsbrad",      # Hillsbrad Foothills — major Alliance vs Horde contested zone
    "azshara",        # the ancient Night Elf ruins zone at the top of the map; remote
    "moonglade",      # the druid sanctuary; only druids could teleport here
    "feralas",        # the dense jungle zone in southern Kalimdor
    "arathi",         # Arathi Highlands — neutral zone, classic PvP leveling

    # ── WoW vanilla — dungeons (more) ───────────────────────────────────
    "shadowfang",     # Shadowfang Keep — Horde-side early dungeon; classic undead castle
    "stockades",      # The Stockades — tiny Alliance dungeon inside Stormwind
    "zulfarrak",      # Zul'Farrak — the sand troll pyramid dungeon in Tanaris
    "diremaul",       # Dire Maul — the later-added dungeon in Feralas; had unique lore
    "blackrock",      # Blackrock Mountain — home of BRD, BRS, LBRS, UBRS; a whole zone itself

    # ── WoW spells/abilities that became memes ───────────────────────────
    "moonfire",       # Druid's instant damage spell — "moonfire spam" was a playstyle and meme
    "polymorph",      # Mage CC spell "Sheep!" — turning enemies into sheep mid-fight
    "pyroblast",      # the Mage's big nuke — the satisfying 3-second cast for massive damage
    "windfury",       # Windfury Totem — the Shaman buff that was game-breakingly powerful
    "innervate",      # Druid spell that restored a healer's mana — coveted by every raid healer
    "bubble",         # Divine Shield (Paladin) — "bubble and run" was the worst thing a paladin could do

    # ── WoW loot/raid culture ────────────────────────────────────────────
    "dkp",            # Dragon Kill Points — the loot currency system used in raid guilds
    "maintank",       # the main tank (MT) — the most important role in a raid
    "offtank",        # the off-tank (OT) — the backup tank
    "raidnight",      # "it's raid night boys" — the Tuesday/Thursday ritual
    "softres",        # soft reserve — telling the raid leader which item you want to roll on
    "reroll",         # rerolling to a new class/server; a huge decision in vanilla
    "greedroll",      # rolling greed on an item you can't use; the polite roll

    # ── UT99 / Q3 announcer words — the kill streak callouts ─────────────
    # These were THE voice lines of early 2000s FPS gaming
    "godlike",        # Quake 3 / UT99 highest tier rank — "GODLIKE!" announcer shout
    "rampage",        # UT99 killing spree tier — "RAMPAGE!" at 5 consecutive kills
    "dominating",     # UT99/Q3 kill streak — "DOMINATING!"
    "impressive",     # Quake 3 railgun accuracy compliment — "IMPRESSIVE!"
    "excellent",      # Quake 3 kill rate — "EXCELLENT!"
    "monsterkill",    # UT99 multi-kill tier — "MONSTER KILL!" at 6 consecutive kills
    "ultrakill",      # UT99 multi-kill tier — "ULTRA KILL!" at 4 simultaneous kills
    "wickedsick",     # UT99 highest killing spree — "WICKED SICK!"
    "firstblood",     # "FIRST BLOOD!" — the first kill of the match; universally known
    "killingspree",   # UT99 base killing spree call — the beginning of a streak

    # ── HALF-LIFE / HL2 — Gordon Freeman's world ─────────────────────────
    "halflife",       # Half-Life — the game that changed PC gaming forever; CS's parent
    "crowbar",        # Gordon Freeman's crowbar — the symbol of HL; the first weapon
    "blackmesa",      # the Black Mesa Research Facility — where it all began
    "lambda",         # the Lambda logo — symbol of the resistance in HL
    "freeman",        # Gordon Freeman — the silent protagonist; the iconic scientist
    "resonance",      # the Resonance Cascade — the accident that started the alien invasion
    "xenworld",       # Xen — the border world/alien dimension
    "nihilanth",      # the Nihilanth — the final boss of HL1; the alien ruler
    "alyx",           # Alyx Vance — the HL2 companion; one of gaming's best characters
    "combine",        # the Combine — the alien empire occupying Earth in HL2
    "gravgun",        # Gravity Gun — the iconic HL2 physics weapon; changed gaming

    # ── SYSTEM SHOCK ─────────────────────────────────────────────────────
    "shodan",         # SHODAN — the malevolent AI from System Shock; "Insect..."
                      # One of gaming's greatest villains

    # ── DEUS EX ──────────────────────────────────────────────────────────
    "jcdenton",       # JC Denton — Deus Ex (2000) protagonist; flat voice acting became iconic
    "deus",           # Deus Ex — the RPG/stealth game that defined PC gaming in 2000
    "augmented",      # the augmentation mechanic central to Deus Ex
    "nanotrite",      # nano-augmented agent — core to Deus Ex lore

    # ── C&C RED ALERT 2 — iconic RTS of 2000 ────────────────────────────
    "kirov",          # "Kirov reporting!" — the Soviet airship unit voice line; legendary
    "prismtower",     # the Allied laser defense tower; melted anything that got close
    "teslatower",     # the Soviet electric defense tower; "bzzzzt"
    "chronosphere",   # the Allied superweapon that teleported units across the map
    "yuri",           # Yuri's Revenge — the expansion villain; mind control mechanic
    "soviets",        # the Soviet faction in Red Alert 2
    "ironguard",      # not real specifically
    "tengu",          # Yuri's Revenge enemy unit

    # ── THE ELDER SCROLLS 3: MORROWIND (2002) ────────────────────────────
    "balmora",        # the main starting city; where every player's journey truly began
    "vivec",          # the floating city AND one of the three living gods
    "dagothur",       # Dagoth Ur — the final antagonist; "Come, Nerevarine..."
    "telvanni",       # House Telvanni — the wizard faction living in giant mushroom towers
    "dunmer",         # Dark Elf — the native race of Morrowind
    "outlander",      # what every NPC calls you in Morrowind if they don't know you
    "nerevarine",     # the player's title/identity — the reincarnation of the hero Nerevar
    "almsivi",        # the three tribunal gods: Almalexia, Sotha Sil, Vivec
    "almalexia",      # one of the three divine tribunal gods; final boss of Tribunal DLC
    "sotha",          # Sotha Sil — the silent clockwork god; Clockwork City
    "seyda",          # Seyda Neen — the first town every Morrowind player entered
    "redoran",        # House Redoran — the warrior noble house in Morrowind
    "hlaalu",         # House Hlaalu — the merchant/political house
    "indoril",        # House Indoril — the priestly house of the tribunal

    # ── BALDUR'S GATE ────────────────────────────────────────────────────
    "minsc",          # Minsc — the beloved berserker ranger; "Go for the eyes, Boo!"
    "boo",            # Boo — Minsc's hamster; the "miniature giant space hamster"
    "jaheira",        # Jaheira — the half-elf druid; tough, sarcastic companion
    "imoen",          # Imoen — the thief; your childhood friend and constant companion

    # ── NFS / RACING ─────────────────────────────────────────────────────
    "busted",         # "BUSTED!" — the NFS screen when cops caught you; pure nostalgia
    "nitrous",        # nitrous oxide boost; NFS Underground culture
    "pursuit",        # police pursuit mode in NFS; high-tension cop chases
    "infernus",       # the Infernus — GTA's iconic sports car; everyone drove it

    # ── MISC PC GAMING CULTURE early 2000s ───────────────────────────────
    "moonglow",       # Ultima Online city; also Ragnarok reference
    "norrath",        # EverQuest's world — "A Citizen of Norrath"
    "luclin",         # EverQuest: The Shadows of Luclin — the moon expansion
    "velious",        # EverQuest: The Scars of Velious — the ice expansion
    "kunark",         # EverQuest: The Ruins of Kunark — the first expansion; iconic
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
    print(f"Checking {total} handles — WoW bosses, Q3 callouts, Morrowind, BG, HL, C&C...\n")
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
    with open("rsi_handle_results_v11.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v11.json")


if __name__ == "__main__":
    main()
