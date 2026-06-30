#!/usr/bin/env python3
"""
RSI handle availability checker — late 90s / early 2000s PC gaming list.
Prints the full URL for every check so results can be manually verified.
404 = available. 200 = profile exists (taken).
"""

import sys
import time
import requests
import json
from datetime import datetime

NAMES = [
    # ── Games & Franchises ───────────────────────────────────────────────
    "Quake",
    "QuakeWorld",
    "Unreal",
    "Counterstrike",
    "Dusttwo",
    "Halflife",
    "Starcraft",
    "BroodWar",
    "ZergRush",
    "WarcraftThree",
    "DotA",
    "EverQuest",
    "UltimaOnline",
    "Diablo2",
    "AgeOfEmpires",
    "CommandAndConquer",
    "RedAlert",
    "MaxPayne",
    "DeusEx",
    "SystemShock",
    "Baldursgate",
    "Morrowind",
    "Runescape",
    "Freespace",
    "Tribes",
    "UT99",
    "Homeworld",
    "TotalAnnihilation",

    # ── Characters & Icons ───────────────────────────────────────────────
    "GMAN",
    "Vortigaunt",
    "Headcrab",
    "Kerrigan",
    "DeckardCain",
    "Shodan",
    "Tommy",
    "Rayne",
    "JCDenton",
    "Pudge",
    "Invoker",
    "Fatality",
    "Thresh",

    # ── Tech / Culture / Platform ────────────────────────────────────────
    "Battlenet",
    "GameSpy",
    "LANParty",
    "Ventrilo",
    "TeamSpeak",
    "mIRC",
    "ICQ",
    "WinAMP",
    "Napster",
    "Kazaa",
    "Newgrounds",
    "Voodoo",
    "Pentium",
    "DirectX",
    "Xfire",
    "Fileplanet",
    "HLTV",
    "WON",
    "CDKey",

    # ── Slang & Moments ──────────────────────────────────────────────────
    "LeeroyJenkins",
    "AllYourBase",
    "AYBABTU",
    "Wololo",
    "L33t",
    "Warez",
    "RocketJump",
    "BunnyHop",
    "RailGun",
    "QuadDamage",
    "Frag",
    "Gib",
    "Spawn",
    "Camper",
    "Lagger",
    "Ping",
    "ROFL",
    "StayAwhile",
    "GG",
    "GLHF",
    "Smurf",
    "Zerg",
    "Rush",
    "Ninja",
    "Grief",
    "Gank",
    "Smurf",
    "WallHack",
    "Defrag",
    "BunnyHop",
    "CircleStrafe",
    "StrafejJump",
    "Gibbed",
    "Telefrag",
    "Respawned",
    "Fragged",
    "PubStomper",
    "ClipThrough",
    "LagComp",
]

# Deduplicate while preserving order
seen = set()
NAMES_DEDUPED = []
for n in NAMES:
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

DELAY = 1.5  # seconds between requests


def check(name: str, session: requests.Session) -> dict:
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
    print(f"Checking {total} RSI handles ...\n")
    print(f"{'#':>4}  {'CODE':>4}  {'RESULT':>10}  {'HANDLE':<25}  URL")
    print("-" * 100)

    available = []
    unavailable = []
    errors = []

    with requests.Session() as session:
        for i, name in enumerate(NAMES_DEDUPED, 1):
            r = check(name, session)

            if r["error"]:
                tag = "ERROR"
                errors.append(r)
            elif r["available"]:
                tag = "AVAILABLE"
                available.append(r)
            else:
                tag = "TAKEN"
                unavailable.append(r)

            code_str = str(r["status"]) if r["status"] else "ERR"
            print(f"[{i:>3}/{total}]  {code_str:>4}  {tag:<10}  {name:<25}  {r['url']}", flush=True)

            if i < total:
                time.sleep(DELAY)

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)

    print(f"\n✅  AVAILABLE ({len(available)}):")
    for r in available:
        print(f"   {r['name']:<30}  {r['url']}")

    print(f"\n❌  TAKEN ({len(unavailable)}):")
    for r in unavailable:
        print(f"   {r['name']:<30}  {r['url']}")

    if errors:
        print(f"\n⚠️  ERRORS ({len(errors)}):")
        for r in errors:
            print(f"   {r['name']:<30}  {r['error']}")

    output = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "total": total,
        "available": [{"name": r["name"], "url": r["url"]} for r in available],
        "unavailable": [{"name": r["name"], "url": r["url"]} for r in unavailable],
        "errors": errors,
    }
    with open("rsi_handle_results_v2.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nFull results saved to rsi_handle_results_v2.json")


if __name__ == "__main__":
    main()
