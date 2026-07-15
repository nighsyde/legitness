#!/usr/bin/env python3
"""
RSI handle availability checker — batch 3.
Millennial PC gamer nostalgia names.
Prints full URL for every check so results can be manually verified.
404 = available. 200 = taken.
"""

import sys
import time
import requests
import json
from datetime import datetime

NAMES = [
    # ── Top 10 picks ─────────────────────────────────────────────────────
    "MankriksWife",
    "AltF4",
    "Motherlode",
    "AtLeastIHaveChicken",
    "ThirtyLives",
    "IDDQD",
    "GameShark",
    "FaceRoll",
    "InsertCoin",
    "Huntard",

    # ── Rest of the suggestion list ───────────────────────────────────────
    "KeyboardTurner",
    "Desync",
    "FatalError",
    "BlowTheCart",
    "AdminAbuse",
    "VACSecured",
    "NotResponding",
    "PleaseWait",
    "DialingUp",
    "BabyRage",
    "Kappa",
    "RubberBanding",
    "BigSmokesOrder",

    # ── New batch ─────────────────────────────────────────────────────────
    "BonziBuddy",
    "LimewireVirus",
    "Scoutzknivez",
    "TuesdayMaintenance",
    "RealmDown",
    "GuildDisbanded",
    "CtrlAltDelete",
    "BlueScreen",
    "DefragNow",
    "DontSend",
    "SurfMap",
    "GunGameKnife",
    "NotEnoughRam",
    "AskJeeves",
    "AOLCDRom",
    "WoWCrack",
    "NinjaRez",
    "PatchNotes",
    "Scoutzknivez",
    "TuesdayMaintenance",

    # ── A few more that just came to mind ─────────────────────────────────
    "MoreDots",
    "FiftyDKPMinus",
    "Godlike",
    "Impressive",
    "Thunderfury",
    "Kekeke",
    "GGnoRe",
    "AdditionalPylons",
    "NuclearLaunch",
    "Roflcopter",
    "LessDots",
    "DeepBreath",
    "IgnoreTheWhelps",
    "MonsterKill",
    "Unstoppable",
    "Rampage",
    "Dominating",
    "Excellent",
    "Humiliation",
    "Gauntlet",
    "PurePwnage",
    "TehPwnerer",
    "NoobPwner",
    "BarrensChat",
    "CorruptedBlood",
    "Naxxramas",
    "SeriousRaider",
    "DKPMinus",
    "BoxeR",
    "ZugZug",
    "FragMovie",
    "Pwnt",
    "GotFrag",
    "AllSeeingEye",
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
    print(f"Checking {total} RSI handles ...\n")
    print(f"{'#':>4}  {'CODE':>4}  {'RESULT':<10}  {'HANDLE':<28}  URL")
    print("-" * 110)

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
            print(f"[{i:>3}/{total}]  {code_str:>4}  {tag:<10}  {name:<28}  {r['url']}", flush=True)

            if i < total:
                time.sleep(DELAY)

    print("\n" + "=" * 110)
    print("SUMMARY")
    print("=" * 110)

    print(f"\n✅  AVAILABLE ({len(available)}):")
    for r in available:
        print(f"   {r['name']:<35}  {r['url']}")

    print(f"\n❌  TAKEN ({len(unavailable)}):")
    for r in unavailable:
        print(f"   {r['name']:<35}  {r['url']}")

    if errors:
        print(f"\n⚠️  ERRORS ({len(errors)}):")
        for r in errors:
            print(f"   {r['name']:<35}  {r['error']}")

    output = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "total": total,
        "available": [{"name": r["name"], "url": r["url"]} for r in available],
        "unavailable": [{"name": r["name"], "url": r["url"]} for r in unavailable],
        "errors": errors,
    }
    with open("rsi_handle_results_v3.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nFull results saved to rsi_handle_results_v3.json")


if __name__ == "__main__":
    main()
