#!/usr/bin/env python3
"""
RSI handle checker — batch 17.
Diamond-in-the-rough approach. Going deep into categories we haven't touched:
- SC Brood War unit names (iconic, alien-sounding, nobody thinks to check)
- D2 specific item names that aren't the famous ones (deep cuts)
- WoW ability names that sound genuinely cool as callsigns
- 3dfx/GPU era hardware (the actual technology of that gaming era)
- WoW server names (historical, specific)
- CS mechanical skill terms
- Halo lore deep cuts
- Korean SC player handles
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── STARCRAFT BROOD WAR UNITS — iconic, alien, nobody checks these ───
    # These units defined competitive gaming in Korea and worldwide.
    # They sound genuinely alien and cool as handles.
    "Mutalisk",       # the Zerg flying unit — the backbone of Zerg harassment
                      # "muta harass" was a core SC strategy; the unit sounds alien and fast
    "Lurker",         # Zerg burrowing unit — hidden spines under the ground
                      # "check for lurkers" — the paranoid callout every SC player knew
    "Defiler",        # Zerg caster — Dark Swarm and Plague; the unit that broke Terran
                      # Known by every BW player as the game-changing caster
    "Reaver",         # Protoss slow walker that fired Scarabs — devastating, explosive
                      # "Reaver drops" were a pinnacle of SC skill expression
    "Corsair",        # Protoss air fighter — Disruption Web locked down ground units
                      # Sounds like a space fighter callsign; that's because it is
    "Devourer",       # Zerg anti-air unit — Acid Spores stacked; the Carrier killer
    "Ultralisk",      # the massive Zerg ground unit — unstoppable late-game
    "Dragoon",        # Protoss ground ranged unit — "Dragoon stuck on corner" was a meme
    "Goliath",        # Terran mech walker — anti-air specialist
    "Valkyrie",       # Terran multi-target missile frigate — the anti-Mutalisk weapon
    "Battlecruiser",  # the Terran capital ship — "nuclear launch detected" vibes
    "Yamato",         # the Yamato Cannon on a Battlecruiser — one-shot ability
                      # "Yamato!" was a command every Terran player yelled
    "Medic",          # Terran medic — bio army healing; the unit that broke BW balance
    "Firebat",        # Terran close-range flame infantry — "bunker with Firebats"
    "Wraith",         # Terran cloaked fighter — the original invisible air unit
    "Overlord",       # Zerg supply/transport unit — the backbone of Zerg logistics
    "Larva",          # what Zerg buildings spawn from — the Zerg production mechanic
    "Hydralisk",      # Zerg ranged attacker — the core Zerg unit in most armies
    "Zergling",       # the classic Zerg melee unit — "zerg rush kekeke" came from this
    "Zealot",         # Protoss melee warrior — the tanky frontline fighter
    "Arbiter",        # Protoss caster with Recall and Stasis — the teleport unit
                      # (Also a Halo character — double meaning)

    # ── DIABLO 2 SPECIFIC ITEMS — deep cuts only serious players know ─────
    "Ravenfrost",     # Raven Frost ring — "Cannot be Frozen" — EVERY melee needed this
                      # First piece of advice ever given: "wear a Ravenfrost"
                      # Sounds dark, cold, powerful. Not something anyone would check.
    "Maras",          # Mara's Kaleidoscope — the best all-resist amulet in D2
                      # "Do you have a Mara's?" — every end-game character wanted one
    "Arachnid",       # Arachnid Mesh — best caster belt; every Sorceress wore one
    "Highlords",      # Highlord's Wrath — best amulet for lightning builds
    "Nosferatu",      # Nosferatu's Coil — the unique belt with life steal; vampire named
    "Verdungo",       # Verdungo's Hearty Cord — the best non-set belt for fighters
    "Ribcracker",     # the Ribcracker unique quarterstaff — elite Fury Druid weapon
    "Buriza",         # Buriza-Do Kyanon — the unique crossbow with pierce; Javazon staple
    "Razortail",      # Razortail belt — the pierce belt; Javazon's best friend
    "Nightwing",      # Nightwing's Veil — the cold skills helmet; Blizzard Sorc item
    "Lycander",       # Lycander's Aim/Lycander's Flank — Amazon bows; deep D2 knowledge
    "Titan",          # Titan's Revenge — the best Javazon javelin; threw endlessly
    "Shaftstop",      # Shaftstop armor — 30% damage reduce; every hardcore char wore it
    "Treachery",      # Treachery runeword — the best mercenary armor; Fade proc
    "Duress",         # Duress runeword — the tanky physical damage armor
    "Delirium",       # Delirium runeword helmet — random curses; unique and feared
    "Obedience",      # Obedience runeword — the best budget mercenary polearm
    "Exile",          # Exile runeword — the paladin shield with Life Tap on striking
    "Passion",        # Passion runeword — Zeal; the low-cost alternative

    # ── WoW ABILITIES THAT SOUND LIKE REAL CALLSIGNS ─────────────────────
    "Eviscerate",     # Rogue finishing move — sounds brutal and precise
    "Hemorrhage",     # Rogue ability — sounds visceral
    "Ambush",         # Rogue opener — the classic stealth attack
    "Thunderclap",    # Warrior AoE — sounds powerful
    "Bloodrage",      # Warrior self-rage generation — sounds aggressive
    "Hamstring",      # Warrior kiting ability — the slow that defined WoW PvP
    "Overpower",      # Warrior counter to dodges — precise, technical sounding
    "Intercept",      # Warrior charge at already-moving targets — sounds tactical
    "Shadowmeld",     # Night Elf racial — disappear into shadows
    "Combustion",     # Fire Mage cooldown — the burst damage amplifier
    "Counterspell",   # Mage interrupt — "CS!" was called every arena match
    "Polymorph",      # already checked, taken
    "Shadowform",     # Shadow Priest stance — the dark mode
    "Vampirictouch",  # Shadow Priest damage+healing spell
    "Mindblast",      # Shadow Priest nuke — the burst damage
    "Dispersion",     # Shadow Priest defensive — the bubble
    "Windfury",       # already checked, taken
    "Earthshock",     # Shaman interrupt — "ES!" was called in every arena
    "Frostnova",      # Mage AoE freeze — the root+burst combo
    "Fireblast",      # Mage instant cast — sounds like a callsign
    "Arcaneblast",    # Arcane Mage signature spell — stacking debuff
    "Lifebloom",      # TBC Druid HoT — the stacking rolling heal
    "Swiftmend",      # Druid instant heal — the clutch save
    "Cyclone",        # Druid CC — broken in arenas; "Cyclone the warrior"
    "Entangling",     # Entangling Roots — Druid CC
    "Faeriefire",     # Druid debuff — removes stealth, armor debuff
    "Barkskin",       # Druid damage reduce — sounds like natural armor
    "Lifeblood",      # not a WoW spell but sounds good
    "Soulfire",       # Warlock nuke — the big cast
    "Shadowbolt",     # Warlock primary spell
    "Conflagrate",    # Warlock fire finisher
    "Immolate",       # Warlock DoT
    "Corruption",     # Warlock instant DoT

    # ── 3DFX/GPU ERA — the actual hardware of the late 90s gaming era ────
    # The technology that made CS 1.6 and Quake possible.
    "Voodoo",         # 3dfx Voodoo — the GPU that defined late 90s PC gaming
                      # If you had a Voodoo 2 in 1998 you were god-tier
    "Voodoo2",        # the Voodoo 2 — SLI before SLI was a word
    "Glide",          # the 3dfx Glide API — smoother than OpenGL at the time
    "TNT2",           # Nvidia RIVA TNT2 — the budget Voodoo competitor
    "GeForce",        # the Nvidia GeForce brand — "just got a GeForce"
    "Radeon",         # the ATI Radeon — the AMD GPU line
    "SoundBlaster",   # Creative Sound Blaster — the sound card everyone had

    # ── WoW SERVER NAMES — historical, specific ───────────────────────────
    "Laughingskull",  # Laughing Skull — THE realm; where Leeroy Jenkins happened
    "Stormrage",      # Stormrage — one of the oldest and most populated WoW realms
    "Mannoroth",      # Mannoroth realm — named after the pit lord
    "Archimonde",     # Archimonde realm — named after the eredar lord
    "Medivh",         # Medivh realm — named after the last guardian; also a character
    "Dalvengyr",      # Dalvengyr — one of the original WoW realms

    # ── CS MECHANICAL SKILL TERMS ────────────────────────────────────────
    "Headglitch",     # standing at cover so only your head is visible; a CS technique
    "Dropshot",       # going prone while shooting to throw off enemy aim
    "Jumppeek",       # jumping to briefly peek over cover — risky, high-skill
    "Counterstraf",   # counter-strafing — tapping the opposite key to stop instantly
    "Prefire",        # already checked, taken
    "Spraycontrol",   # controlling spray pattern — the core rifling skill in CS

    # ── HALO LORE DEEP CUTS ───────────────────────────────────────────────
    "Gravemind",      # the Flood's central intelligence in Halo 2 — "I am a monument
                      # to all your sins" — one of gaming's best villains
    "GuiltyS",        # 343 Guilty Spark — "Oh, hello! I am 343 Guilty Spark"
    "Reclaimer",      # what 343 Guilty Spark calls Master Chief — iconic
    "Ringworld",      # the Halo ring itself — "Why would you build such a thing?"
    "Installation",   # Installation 04 — the first Halo ring
    "Forerunner",     # already taken
    "Monitor",        # the Forerunner AI designation — Guilty Spark is a Monitor
    "Index",          # the Activation Index — what Master Chief retrieves in Halo 1

    # ── KOREAN SC PLAYER HANDLES ──────────────────────────────────────────
    "Flash",          # Lee Young-ho — "The God of StarCraft"; most decorated SC player
    "Jaedong",        # Lee Jae-dong — "The Tyrant"; legendary Zerg player
    "Bisu",           # Kim Taek-yong — legendary Protoss; "The Revolutionist"
    "Boxer",          # Lim Yo-Hwan — "The Emperor"; the first SC celebrity
    "Nada",           # Lee Yoon-yeol — legendary Terran; "The Genius"
    "Yellow",         # Yoon Yeol — Zerg legend
    "Reach",          # Yoon Su — legendary Protoss player
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
    print(f"Checking {total} diamond-in-the-rough handles...\n")
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
    with open("rsi_handle_results_v17.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v17.json")


if __name__ == "__main__":
    main()
