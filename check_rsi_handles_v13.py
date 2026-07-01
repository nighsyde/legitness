#!/usr/bin/env python3
"""
RSI handle checker — batch 13.
Same energy as "Pwned": short, cross-game, universally understood 1999-2006.
Categories: leet speak terms, universal gaming slang, Pure Pwnage culture,
early internet gaming idioms, MMO mechanics terms that went cross-game.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── LEET SPEAK — the linguistic backbone of the era ─────────────────
    # These are the words that BECAME their own words, like pwned did.
    "Teh",            # leet for "the" — intentional typo that became its own thing
                      # "teh internetz" "teh_masterer" from Pure Pwnage
    "Pwnt",           # shorter/alternate spelling of pwned — "you got pwnt"
    "Noob",           # shortened from "newbie" — probably taken but check
    "N00b",           # leet version with zeros — the visual upgrade
    "Nub",            # further compressed noob; the dismissive form
    "Hax",            # short for hacks/cheats — "hax!" was the accusation
    "Suxxor",         # leet for "sucks" — "-xor" suffix was huge in leet speak
    "Roxxor",         # leet for "rocks" — "this roxxor your boxxor"
    "Pwnage",         # noun form of pwned — "pure pwnage"; the show name itself
    "Zomg",           # "Oh My God" with a Z instead of O; early internet intensifier
    "Lolwut",         # lol + what merged; the confusion reaction
    "Wtfpwned",       # compound: what the f + pwned; maximum reaction
    "Rofl",           # rolling on the floor laughing — the tier above lol
    "Roflstomp",      # completely dominated — combo of rofl + stomp
    "Roflcopter",     # the ASCII helicopter that was EVERYWHERE in early 2000s chat
                      # "ROFLCOPTER GO WHIRWHIRWHIR" — IRC, forums, game chat
    "Lmaoplane",      # the lmao variant of roflcopter — the plane

    # ── PURE PWNAGE — the web series (2004) that defined gamer culture ──
    # 2 million fans. Canada's most popular web series at the time.
    # User mentioned FPS Doug directly.
    "FPSDoug",        # THE character. "BOOM! Headshot!" Created the BoomHeadshot trope.
                      # Every CS 1.6 player from 2004 knows FPS Doug.
    "BoomHeadshot",   # FPS Doug's iconic catchphrase — the trope namer on TV Tropes
    "ImPumped",       # "I'm PUMPED!" — FPS Doug's other signature line before fragging

    # ── LOW PING BASTARD / HIGH PING BASTARD — Quake/early internet ──────
    "LPB",            # Low Ping Bastard — what dial-up players called T1/cable players
                      # Getting called an LPB was simultaneously an insult and a compliment
    "HPB",            # High Ping Bastard — you on dial-up losing to an LPB
    "T1Line",         # having a T1 internet line was the ultimate flex in early online gaming
    "Dialupper",      # someone still on dial-up when everyone else had broadband

    # ── CROSS-GAME UNIVERSAL MECHANICS SLANG (1999-2006) ─────────────────
    # Terms that crossed every game the user mentioned
    "Aggro",          # pulling aggro — WoW term that went universal across every MMO/RPG
                      # "you pulled aggro" — the raiding callout everyone knows
    "Proc",           # random item effect triggering — "my sword proc'd"
                      # WoW/D2 term that every serious gamer knew
    "Crit",           # critical hit — shortened from "critical"; universal across all games
    "Nerf",           # something being made weaker — "they nerfed paladins again"
                      # Became a universal gaming term; still used today
    "Buff",           # opposite of nerf — "they buffed warriors"
    "Kite",           # running away while dealing damage — WoW/D2/RTS tactic
    "Cheese",         # cheap/easy strategy that shouldn't work — "stop cheesing"
    "Turtle",         # playing ultra-defensive; turtling in RTS = camping your base
    "Stun",           # stun lock — getting stunlocked; a universal complaint
    "Snare",          # movement-slowing ability — snared in place
    "Root",           # rooting in place — "I'm rooted!"
    "Burst",          # burst damage phase — "save your burst for the boss"
    "Nuke",           # using all your big damage abilities at once — "nuke it down"
    "Wipe",           # the raid wipe — "we wiped" — one of the most universal WoW moments
    "Zerged",         # got hit by a zerg rush — SC term that went universal
    "Pubstomp",       # stomping in public games/servers (as an organized group)
    "Pubstomping",    # the act itself
    "Faceroll",       # rolling your face on the keyboard and winning — easy-mode class
    "Facerolled",     # past tense — "we facerolled them"

    # ── HALO LAN PARTY CULTURE ────────────────────────────────────────────
    "Teabag",         # crouching over a dead body repeatedly in Halo — defining early Xbox
                      # Live culture; the universal post-kill gesture
    "Teabagged",      # the victim — "I got teabagged by some random"
    "Splatter",       # running someone over with a Warthog in Halo — satisfying
    "Betrayal",       # team killing notification in Halo — "Betrayal!" in that voice
    "Noscope",        # sniper kill without scoping in — Halo/CoD skill shot
    "Oddball",        # the Halo game mode; carrying the skull
    "Juggernaut",     # the Halo game mode; the one player who has all the power

    # ── GENERAL EARLY 2000s INTERNET/GAMING ──────────────────────────────
    "Troll",          # internet troll — predates its current meaning; very early internet
    "Flamed",         # getting flamed in a forum — "I got flamed on GameFAQs"
    "Flamebait",      # posting something designed to start a flame war
    "Epic",           # "that was epic" — the adjective defined a generation of gaming moments
    "Legendary",      # "that was legendary" — the tier above epic
    "Clutch",         # clutch play — winning under pressure; the ultimate compliment
    "Noscoped",       # past tense of noscope
    "Stomped",        # got completely stomped — simple, universal
    "Dunked",         # dunked on — sports metaphor that entered gaming
    "Griefed",        # past tense of grief — "I got griefed the whole session"

    # ── SPECIFIC ERA TOOLS/SERVICES ──────────────────────────────────────
    "Hamachi",        # the VPN that let you play LAN games over internet
                      # "just download Hamachi" — launched a thousand gaming nights
    "Xfire",          # the gaming overlay before Steam — already checked, TAKEN
    "mIRC",           # the IRC client every CS player used for scrims
    "GameRanger",     # GameRanger — online gaming service; the LAN-over-internet solution

    # ── BATTLE.NET CULTURE ────────────────────────────────────────────────
    "USEast",         # US East server — the most populated Diablo 2 realm
    "BaalRun",        # the Diablo 2 Baal run — typing "baal run 1/8" to find a game
    "CowRun",         # the Diablo 2 cow level run
    "MephRun",        # the Mephisto run — fastest boss farm in D2
    "PinRun",         # the Pindleskin run — Act 5 Nihlathak's boss farm
    "RushPlz",        # "rush plz" — asking to be rushed through D2 acts; so common

    # ── CS 1.6 SPECIFIC SLANG ────────────────────────────────────────────
    "Rushb",          # "rush B" — the most iconic CS callout of all time
    "EcoRound",       # eco round — saving money round; everyone knows this
    "ForceRound",     # force buy when short on money
    "AntiEco",        # playing against an eco round
    "HalfBuy",        # half buy — buying what you can afford
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
    print(f"Checking {total} 'Pwned energy' handles — leet speak, cross-game slang, Pure Pwnage...\n")
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
    with open("rsi_handle_results_v13.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v13.json")


if __name__ == "__main__":
    main()
