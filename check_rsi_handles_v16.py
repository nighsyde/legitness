#!/usr/bin/env python3
"""
RSI handle checker — batch 16.
Pre/post-game rituals, shorthand, callouts, trash talk, etiquette terms,
Pure Pwnage references, and anything adjacent from 1999-2006 online gaming.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── PRE/POST GAME RITUALS ─────────────────────────────────────────────
    "glhfnore",       # good luck have fun no rematch — the full dismissal
    "glglhf",         # exaggerated "gl gl hf" — ironic over-wishing
    "gg2u",           # "good game to you" — the slightly formal version
    "ggnr",           # "gg no re" abbreviated to 4 chars
    "ggnoob",         # the compound post-win taunt
    "ggout",          # "gg, out" — I'm done, I won, leaving
    "rekt",           # "get rekt" — probably taken but check
    "welpgg",         # "welp, gg" — the resigned acceptance

    # ── MID-GAME SHORTHAND ────────────────────────────────────────────────
    "omw",            # "on my way" — 3 chars, cross-game
    "oom",            # "out of mana" — every healer's panic call
    "rdy",            # "ready" — pre-pull confirmation
    "inv",            # "invite me" — MMO group request
    "pst",            # "please send tell" — whisper me in MMO
    "inc",            # "incoming" — warning call
    "healme",         # "heal me!" — the constant healer demand
    "needheal",       # "need heal" — variation
    "pullnow",        # "pull now!" — impatient raid member
    "gotime",         # "go time" — it's happening

    # ── MMO TRADE CHAT / ECONOMY ──────────────────────────────────────────
    "wtb",            # want to buy — MMO trade shorthand
    "wts",            # want to sell
    "wtt",            # want to trade
    "lfg",            # looking for group
    "lfm",            # looking for more
    "lf1m",           # looking for 1 more
    "lf2m",           # looking for 2 more
    "lf3m",           # looking for 3 more
    "lf4m",           # looking for 4 more

    # ── TRASH TALK ────────────────────────────────────────────────────────
    "l2p",            # learn to play — the classic dismissal
    "l2aim",          # learn to aim — FPS specific
    "l2farm",         # learn to farm — RTS/MMO insult
    "uninstall",      # the ultimate insult: "just uninstall"
    "getgud",         # "get gud" — play better
    "gitgud",         # "git gud" — the dark souls era variant
    "stadhis",        # "stay there, hiding is skill" — CS camper taunt? no...
    "camper",         # the CS insult (already checked, taken)
    "hacker",         # accusing someone of hacking
    "cheater",        # "cheater!" — the accusation
    "reported",       # "reported" — threatening to report
    "aimbot",         # "you're using aimbot"
    "wallhack",       # wallhack accusation
    "triggerbot",     # triggerbot accusation
    "scripted",       # "you're scripted" — using scripts

    # ── PURE PWNAGE REFERENCES (unchecked) ───────────────────────────────
    "PurePwnage",     # the show name itself
    "TehMasterer",    # Jeremy's actual in-game handle in the show
    "Lanageddon",     # episode 8 — the LAN party episode; "Lanageddon" is a great word
    "Imapwnu",        # Jeremy's WoW character from ep 6 "Imapwnu of Azeroth"
    "DanceAllDay",    # FPS Doug: "I can dance all day! I can dance all day!"
    "FasterKnife",    # "you run faster with a knife, everyone knows that"
    "PwnOrBePwned",   # episode 4 title — the law of online gaming
    "PwnedHard",      # "I pwn you like pretty hard and stuff"
    "ProGamer",       # what Jeremy always calls himself
    "Progamer",       # lowercase variation

    # ── HALO ERA TERMS ────────────────────────────────────────────────────
    "Spartans",       # "Spartans never die" — Halo universe
    "MasterChief",    # the Spartan — probably taken
    "Cortana",        # the AI — probably taken
    "BobJohnson",     # the generic Halo multiplayer name
    "SgtJohnson",     # Sgt. Johnson — "I know what the ladies like"
    "Arbiter",        # the Elite/Arbiter — Halo 2
    "Forerunner",     # the ancient Halo civilization
    "Covenant",       # the alien empire
    "Flood",          # the parasite
    "Banshee",        # the Covenant aircraft
    "Scorpion",       # the UNSC tank
    "Warthog",        # the Warthog jeep — the most iconic Halo vehicle
    "Mongoose",       # the Mongoose ATV — added in Halo 3
    "Mantis",         # Halo 4 mech
    "Needler",        # the crystalline alien weapon
    "Plasma",         # plasma pistol/rifle
    "Sniper",         # the sniper rifle (probably taken)
    "Rockets",        # the rocket launcher

    # ── XBOX LIVE EARLY ERA ───────────────────────────────────────────────
    "Gamertag",       # your Xbox Live identity
    "Modchip",        # Xbox mod chip
    "XBConnect",      # the service for Halo LAN over internet
    "Xlink",          # Xlink Kai — the other Halo LAN tunneling service
    "Systemlink",     # system link — LAN cable play
    "Bridged",        # network bridged for system link
    "Tunneled",       # using a VPN/tunnel to play LAN over internet

    # ── CS SPECIFIC CALLOUTS (unchecked) ─────────────────────────────────
    "goA",            # "go A" — attack A site
    "goB",            # "go B" — attack B site
    "longA",          # long A — the long A corridor
    "shortA",         # short A
    "midPit",         # mid pit on de_dust2
    "catWalk",        # catwalk — map position
    "Tspawn",         # T spawn
    "CTspawn",        # CT spawn
    "pistolRound",    # pistol round — the first round of a half
    "knifeRound",     # knife round — determining sides at the start

    # ── EARLY ONLINE GAMING ETIQUETTE ────────────────────────────────────
    "rematch",        # "rematch?" — asking for a do-over
    "norematch",      # "no rematch" — the dismissal
    "surrender",      # surrendering the match
    "forfeit",        # forfeiting
    "ragequit",       # already checked, taken
    "dooragequit",    # compound variation
    "allin",          # going all in
    "noobcheck",      # checking if someone is a noob
    "clutchtime",     # clutch time
    "lastbullet",     # last bullet kill

    # ── BATTLE.NET SPECIFIC ───────────────────────────────────────────────
    "iccup",          # ICCUP — the SC1 ladder platform
    "progamers",      # the collective noun
    "pgamers",        # shortened
    "clanpk",         # clan player kill — D2 hostile button culture
    "openlobby",      # open game lobby — D2 open games anyone could join
    "closedlobby",    # closed game — password protected
    "gamelobby",      # the game lobby itself
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
    print(f"Checking {total} handles — gg/glhf era, Pure Pwnage, Halo, Xbox Live, callouts...\n")
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
    with open("rsi_handle_results_v16.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v16.json")


if __name__ == "__main__":
    main()
