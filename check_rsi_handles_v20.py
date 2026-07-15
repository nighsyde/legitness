#!/usr/bin/env python3
"""
RSI handle checker — batch 20.
The IRONIC parts of early 2000s gaming culture.
Archetypes everyone recognized. Excuses everyone made. 
The cringe that's now nostalgia. Taken seriously then, funny now.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── WoW ARCHETYPES — the player types everyone recognized ─────────────
    "Huntard",        # the Hunter who stood in fire, pulled wrong mobs, forgot to dismiss pet
                      # "Don't be a Huntard" was said to every new Hunter
                      # The class had a reputation. The handle IS the reputation.
    "Retadin",        # Retribution Paladin — mocked as useless in vanilla WoW
                      # "Ret is for PvE scrubs" was the prevailing opinion
                      # Pure irony: they became dominant later
    "Facemelter",     # Shadow Priest — "I'm going to melt your face off"
                      # Their damage was called face-melting. The nickname stuck.
    "Healbot",        # the healer who used the HealBot addon and just clicked green bars
                      # "You're just a HealBot" was a WoW insult
    "Standinfire",    # the act of standing in Ragnaros's fire — the cardinal WoW sin
                      # "MOVE OUT OF THE FIRE" was yelled in every raid
    "Tradechat",      # the WoW trade channel — the internet comment section of its time
                      # Everyone complained about it. Everyone read it.
    "Barrenschat",    # Barrens Chat — the zone chat that spawned a thousand memes
                      # Chuck Norris jokes, Mr. T references, absolute chaos
    "Ninjarogue",     # the rogue who ninja-looted and vanished before anyone could react
    "GoldFarmer",     # the gold farmer — buying WoW gold was a moral debate
    "EpicMount",      # getting your epic mount at 60 — the $1000g grind everyone suffered
    "GnomePunt",      # the Gnome punt — a WoW running joke about kicking the small race
    "Soulstoned",     # having a warlock soulstone — "who has the soulstone?"
    "Innervateme",    # begging a Druid for Innervate — the healer plea
    "PallyPower",     # the Paladin giving blessings — PallyPower addon and culture
    "WorldFirst",     # world first kill — the guilds that raced to kill bosses first
    "ServerFirst",    # server first — the local version of world first

    # ── THE UNIVERSAL GAMING EXCUSES — taken totally seriously at the time ─
    "IWasLagging",    # "I was lagging" — the #1 excuse in online gaming history
    "MyMouseSlipped", # "my mouse slipped" — the classic mechanical failure excuse
    "Iwasntrying",    # "I wasn't even trying" — after losing
    "LetYouWin",      # "I let you win" — the sore loser's final word
    "MyTeamBad",      # "my team was bad" — never your fault
    "CampersWin",     # "camping is a valid strategy" — the camper's defense
    "HitboxBroke",    # "the hitboxes are broken" — blaming the game engine
    "NoclientsideHit",# "the server didn't register the hit" — classic CS excuse
    "PingExcuse",     # "I had 300 ping" — the connection excuse
    "IHaventPlayed",  # "I haven't played in months" — explaining rust
    "CouldGoPro",     # "I could go pro if I tried" — every teenager's claim
    "UsedToBeBetter", # "I used to be way better at this game"

    # ── THE CRINGE NAMING CULTURE — handles people actually had ───────────
    "xXxSniper",      # the xXx naming convention — the most mocked handle format
    "xXxProxXx",      # the full xXx wrapper — the peak of 2002 naming culture
    "ItzYaBoi",       # the later evolution of this naming style
    "MLGpro",         # claiming MLG status before MLG was MLG
    "1337Sniper",     # combining leet speak with a role claim
    "Pr0Player",      # "pro player" in leet speak
    "EliteGamer",     # calling yourself an elite gamer
    "ProGamer9000",   # the number suffix to a self-important title
    "UberPro",        # combining uber with pro
    "TrueLegend",     # "I am a true legend"

    # ── CLAN CULTURE IRONY — taking digital hierarchies very seriously ─────
    "ClanLeader",     # taken (confirmed) — but checking variants
    "SubLeader",      # sub-leader — the clan's middle management
    "ClansAreLife",   # the dedication to clan above all
    "Clanhopper",     # someone who kept jumping between clans
    "Disband",        # the clan disbanding — drama every CS team went through
    "Internal",       # internal clan drama — "we have internal issues"
    "Tryout",         # the clan tryout — performing under pressure for randoms
    "Probation",      # the clan probation period
    "Votemute",       # vote muting a teammate on Ventrilo
    "Votekick",       # already checked, taken
    "DKPminus",       # 50 DKP Minus — the Onyxia wipe video; the raid leader punishment
    "FiftyDKP",       # the specific amount — "FIFTY DKP MINUS"

    # ── XBOX LIVE EARLY ERA IRONY — voice chat before filters ─────────────
    "ScreamingKid",   # the screaming child on Xbox Live
    "OpenMic",        # someone with an open mic picking up background noise
    "MomCalled",      # "my mom called me for dinner" — the sudden disconnect
    "RouterUnplug",   # "my mom unplugged the router" — the most relatable quit
    "TVdisconnect",   # the family TV unplugging the router
    "GotGrounded",    # "I'm grounded, can't play tonight"
    "Bedtime",        # having a bedtime that interrupted gaming

    # ── PURE IRONIC GAMING MOMENTS EVERYONE EXPERIENCED ──────────────────
    "AllinQueue",     # being all-in on a queue and going offline
    "DadUsedPhone",   # "my dad picked up the phone" — the dial-up disconnection
    "Permabanned",    # getting permanently banned — the ultimate punishment
    "Softbanned",     # soft ban — shadowbanned from matchmaking
    "Falsereport",    # being falsely reported by salty players
    "Ruinedgame",     # "you ruined the game" — the accusation after every loss
    "IntentFeed",     # intentionally feeding — the ultimate grief
    "JustHavingFun",  # "I'm just having fun" — said while playing terribly
    "CasualGamer",    # claiming to be casual while playing 12 hours a day
    "Nolifegamer",    # "no life" as an identity — wearing it as a badge

    # ── THE FPS IRONY — the contradictions of competitive shooters ─────────
    "KeyboardTurner", # turning with arrow keys instead of mouse — the tell
    "BackPedaler",    # running backward with S key instead of strafing
    "Bunnyhopper",    # accused of bunnyhopping — everyone tried it
    "WallBanger",     # shooting through walls — "that was through the wall!"
    "SprayNPray",     # spraying and praying — no recoil control
    "OnetrIck",       # the one-trick — only playing one character/weapon
    "Bodyshotonly",   # only hitting body shots, never headshots
    "Awpwhore",       # only using the AWP — already checked awponly
    "Knifeonly",      # knife-only servers and challenges
    "Doublejump",     # the instinct to double jump from other games; forgetting CS doesn't have it
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
    print(f"Checking {total} ironic gaming culture handles...\n")
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
    with open("rsi_handle_results_v20.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v20.json")


if __name__ == "__main__":
    main()
