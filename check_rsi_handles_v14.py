#!/usr/bin/env python3
"""
RSI handle checker — batch 14.
Inspired by "lost PC gaming vocabulary" — terms that were everywhere
in 1999-2006 that younger gamers have never heard. Things that instantly
transport you back. Quake-era FPS, WoW PvP ranks, D2 lore, raid addons,
forgotten internet gaming culture.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── QUAKE / ARENA FPS — the "lost" vocabulary of movement and kills ──
    "Telefrag",       # killing someone by teleporting directly onto them in Quake
                      # "You were telefragged by Player X" — the most humiliating death
    "Telefragged",    # past tense — "I got telefragged three times"
    "Airshot",        # hitting an airborne target with a rocket; the ultimate skill shot
                      # UT/Quake/TF2 culture; a sign of true mastery
    "Shafted",        # hit by the Shaft (lightning gun) in Quake — also slang for screwed
    "Railed",         # hit by the railgun — "I got railed across the map"
    "Jumpad",         # jump pad in UT/Quake — launching yourself off a pad
    "Strafe",         # strafing movement — side-to-side while shooting; the core FPS skill
    "Strafed",        # past tense — "I strafed around the corner and fragged two"
    "Deathmatch",     # the original FPS game mode — every kill counts, free for all
    "Fragfest",       # a session of nothing but fragging — a frag-heavy match
    "Fraglimit",      # the kill limit to end a deathmatch — "first to 30 frags wins"
    "Overtime",       # when a match goes to overtime — tense, high stakes
    "Railwhore",      # someone who ONLY uses the railgun; a specific derogatory compliment
    "Rocketwhore",    # only uses rocket launcher; similarly specific insult/compliment
    "Rocketjumped",   # past tense of rocket jumping — "he rocketjumped to the top ledge"

    # ── WoW PvP RANKS — the vanilla honor system ─────────────────────────
    # Getting Grand Marshal or High Warlord required 50-60 hours PvP/week.
    # The most dedicated players in WoW history had these titles.
    "GrandMarshal",   # the highest Alliance PvP rank — below only GM, basically God tier
    "HighWarlord",    # the highest Horde PvP rank — the Horde equivalent
    "FieldMarshal",   # the second-highest Alliance rank — still insane to achieve
    "BloodGuard",     # Horde PvP rank — sounds legitimately badass
    "Legionnaire",    # Horde PvP rank — military, sounds great as a handle
    "Stoneguard",     # Horde PvP rank — solid and tough
    "Challenger",     # the WoW arena season achievement rank
    "Gladiator",      # the highest WoW arena rank — required top 0.5% of the ladder
                      # Getting Gladiator meant you were elite. Still respected today.
    "Duelist",        # arena rank just below Gladiator
    "Rival",          # arena rank below Duelist

    # ── WoW RAID ADDONS — the software every serious player ran ──────────
    # These addon names were spoken as often as spell names.
    "Recount",        # the DPS/HPS meter addon — "link Recount" after every boss
    "Omen",           # Omen Threat Meter — if Omen went red, you were pulling aggro
    "BigWigs",        # Big Wigs Bossmods — the raid timer addon (alternative to DBM)
    "Decursive",      # the addon that auto-removed curses/diseases — essential in MC
    "Bartender",      # Bartender action bar addon — everyone customized their bars
    "Questhelper",    # the quest tracking addon that showed you where to go
    "Gatherer",       # tracked herb/ore node positions on the map
    "Auctioneer",     # the auction house addon — essential for making gold
    "Atlasloot",      # AtlasLoot — showed what items dropped from every boss
    "Deadlyboss",     # Deadly Boss Mods (DBM) — the must-have raid timer addon
    "Bigwigs",        # (duplicate, filtered)
    "Decursed",       # past tense: having been decursed

    # ── WoW RAID CALLOUTS — things said in voice chat every raid night ───
    "Readycheck",     # "/readycheck" — the command before every pull; "READY CHECK"
    "Softenrage",     # soft enrage — boss becomes stronger over time but doesn't reset
    "Hardenrage",     # hard enrage — boss kills everything if you don't kill it in time
    "Pullcount",      # the pull countdown: "pull in 3... 2... 1..."
    "Soulstone",      # Warlock ability — pre-place a soulstone on a healer for a ress
    "Innervate",      # (already confirmed available) Druid mana restore on healer
    "Rebirth",        # Druid combat resurrection — the only in-combat ress in vanilla
    "Ankh",           # Shaman self-resurrection totem — "ankhing" back to life
    "Layonhands",     # Paladin emergency heal — full heal, 1 hour cooldown in vanilla
    "Tranquility",    # Druid group heal — panic button for heavy AoE damage
    "Stampeding",     # Stampeding Roar — Druid group speed buff

    # ── D2 ULTRA-SPECIFIC LORE — beyond what most people checked ─────────
    "Horadric",       # the Horadric Cube — the crafting item central to D2's story
    "Annihilus",      # Annihilus — the best small charm in D2, dropped by Uber Diablo
    "HellforTorch",   # Hellfire Torch — from Uber Tristram; best large charm
    "Hellfire",       # Hellfire Torch abbreviated context
    "Tristram",       # Old Tristram — the town from Diablo 1; in D2 as a secret level
    "Catacombs",      # the Catacombs in D1/D2 — the dungeon beneath Tristram
    "Arreat",         # Mount Arreat — the Barbarian homeland in D2 Act 5; the summit
    "Worldstone",     # the Worldstone — the artifact at the center of D2's lore
    "StonneOfJordan", # Stone of Jordan — was THE D2 economy currency (abbreviated SoJ)
    "SoJTrade",       # trading with SoJs — the D2 economy backbone
    "Runeword",       # D2 runewords — inserting runes in order to create powerful items
    "Enigma",         # Enigma runeword — the most powerful D2 runeword (teleport for all)
    "Grief",          # Grief runeword — the best melee weapon runeword
    "Insight",        # Insight runeword — infinite mana for your mercenary
    "Infinity",       # Infinity runeword — conviction aura, broke the game for elementalists
    "Fortitude",      # Fortitude runeword — life leech, damage, the warrior's best armor
    "Breath",         # Breath of the Dying — the strongest melee weapon runeword
    "Zod",            # Zod rune — the rarest rune in D2 (indestructible)
    "Ber",            # Ber rune — 2nd rarest; "do you have a Ber?"
    "Jah",            # Jah rune — 3rd rarest; Jah Ith Ber = Enigma
    "Vex",            # Vex rune — high rune
    "Ohm",            # Ohm rune — high rune
    "Lo",             # Lo rune — high rune (too short at 2 chars)
    "Sur",            # Sur rune — high rune
    "Gul",            # Gul rune — high rune

    # ── EARLY INTERNET GAMING CULTURE — forgotten terms ──────────────────
    "Twinking",       # twinking a character — equipping a low-level alt with top gear
                      # WoW 19/29/39 twink brackets were their own subculture
    "Corpsecamp",     # camping an enemy's corpse so they can't recover after dying
    "Gravecamp",      # camping the WoW graveyard so enemies can't resurrect safely
    "Ganksquad",      # a group organized specifically for ganking — a hit squad
    "Swiftmend",      # Druid instant heal spell — the clutch save
    "Lifebloom",      # the rolling Druid HoT spell in TBC — the stacking heal
    "Vampiric",       # Vampiric Embrace — Priest spell; healing from shadow damage
    "Shadowweave",    # Shadowweave crafted set — the Shadow Priest gear
    "Shadowpriest",   # the Shadow Priest spec — damage dealer disguised as a healer

    # ── NICHE BUT SPECIFIC ────────────────────────────────────────────────
    "Roguelike",      # a roguelike game (permadeath, procedural) — pre-Rogue 2010s
    "Permadeath",     # dying once means starting over — the hardcore gaming mechanic
    "Ironman",        # self-imposed challenge: Ironman mode (no deaths, no healing items)
    "Speedrun",       # completing a game as fast as possible — early speedrun culture
    "TASrun",         # Tool-Assisted Speedrun — using tools to achieve perfect play
    "Deathless",      # completing something without dying — the achievement
    "Zerohour",       # C&C Zero Hour — one of the most played online RTS games 2003-2006
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
    print(f"Checking {total} 'lost vocabulary' handles...\n")
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
    with open("rsi_handle_results_v14.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v14.json")


if __name__ == "__main__":
    main()
