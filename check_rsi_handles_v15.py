#!/usr/bin/env python3
"""
RSI handle checker — batch 15.
Pulled directly from the r/pcgaming "Lost PC Gaming Vocabulary" thread
(4,298 upvotes, 162 comments). Every term in this batch was mentioned
by the community as a lost/iconic piece of gaming culture.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── FROM THE THREAD — mentioned by name ─────────────────────────────

    # QQ — "less QQ more pew pew" — the crying/quit taunt
    # Thread: 2nd most upvoted comment (565 points)
    # QQ = 2 chars (too short), but variations:
    "QQmore",         # "QQ more" — the full dismissal
    "LessQQ",         # "less QQ" — telling someone to stop crying
    "MorePewPew",     # "more pew pew" — the rest of the iconic phrase
    "PewPew",         # the laser sound; classic shorthand for shooting
    "QQnoob",         # compound taunt

    # SHAZBOT — from Starsiege: Tribes
    # Thread: Multiple comments with 60-172 points
    # The alien expletive in Tribes. The go-to cuss word of that game.
    "Shazbot",        # THE Tribes cuss word. "Shazbot!" Anyone who played Tribes knows it.
    "Shazbot2",       # unlikely to be needed

    # GOSU — Korean term for extremely skilled gamer
    # Huge in StarCraft culture. "That guy is gosu." 4 chars.
    "Gosu",           # highly skilled gamer; SC/Korean gaming culture term

    # IMBA — imbalanced; before "OP" took over
    # Thread: 66 points comment. "IMBA instead of OP"
    "Imba",           # "that's imba" — imbalanced but said as a compliment
    "Imbagon",        # the imba Paragon build from Guild Wars 1

    # DING — the WoW level-up sound/moment
    # Thread: "Ding!" mentioned multiple times
    "Ding",           # "DING!" — announcing you just leveled up in WoW
                      # Followed by "gratz!" from your guildmates
    "Dinged",         # past tense — "I just dinged 60"

    # GRATZ — WoW/MMO congratulations
    # Thread: mentioned in comments
    "Gratz",          # "GRATZ!" — the WoW congratulations on level up
    "Grats",          # alternate spelling
    "Gratzies",       # the even more enthusiastic version

    # WORT — Halo Grunt battle cry
    # Thread: "Wort. Wort? Wort!" — multiple comments
    "Wort",           # "Wort wort wort" — Halo Grunt incomprehensible war cry
                      # One of Halo's most beloved pieces of lore

    # LLAMA — early online gaming term for bad/cheating players
    # Thread: "llama" mentioned; from Tribes culture
    "Llama",          # a llama = a bad, annoying, or cheating player
                      # Tribes: "don't be a llama" was the community rule

    # KTHXBYE — "okay thanks bye" — the internet dismissal
    # Thread: mentioned as lost internet slang
    "Kthxbye",        # the ultimate one-word dismissal of 2000s internet
    "Kthx",           # shortened version

    # WTFBBQ — the escalated WTF
    # Thread: "OMGWTFBBQ" mentioned (from Something Awful)
    "Wtfbbq",         # "what the f*** BBQ" — the 2000s internet absurdism
    "Omgwtfbbq",      # the full version

    # GGNORE — "gg no re" combined
    # Thread: "gg no re" mentioned as lost vocabulary
    "Ggnore",         # "gg no re" = good game, no rematch — dismissive post-win
    "Ggnombre",       # variant?

    # LEEROYED — past tense verb
    # Thread: "Leeroyed" mentioned as a term for pulling everything
    "Leeroyed",       # "we just got Leeroyed" — someone pulled everything

    # NUBCAKES — the escalation of noob
    # Thread: mentioned in comments
    "Nubcakes",       # "nubcakes" — a more colorful version of noob/nub

    # TOASTY — Mortal Kombat Easter egg
    # Thread: mentioned
    "Toasty",         # the MK Easter egg where Dan Forden pops up and says "Toasty!"
                      # One of gaming's first Easter eggs. Everyone tried to trigger it.

    # UBER — "uber micro" from Pure Pwnage; "uber guild"
    # Thread: 557 points comment — "uber went to corporate re-education"
    "Uber",           # the gaming adjective — "uber micro", "uber leet"
                      # (note: Uber the company may make this hard to register)

    # BASSHUNTER — the DJ/musician who made the Dota/Vent song
    # Thread: multiple references to "Vi sitter här i Venten och spelar lite Dota"
    "Basshunter",     # the Swedish DJ whose song was the anthem of the Ventrilo/Dota era

    # DOLPHINDIVE — prone spam in old shooters
    # Thread: "dolphin diving" mentioned as lost term
    "Dolphindive",    # prone dive spam — going prone rapidly to avoid bullets
    "Dolphindiving",  # the act

    # ORLY — "Oh Really" owl meme
    # Thread: "ORLY Remember the ORLY owl?" — multiple comments
    "Orly",           # the ORLY owl — early 2000s image macro
    "Yarly",          # "Ya Rly" — the response to ORLY
    "Nowai",          # "No Way" — the third in the ORLY/YARLY/NOWAI meme chain

    # MOAR — internet intensifier for "more"
    # Thread implied; "moar dots" — more extreme than "more"
    "Moar",           # "MOAR" — internet-speak for wanting MORE of something intensely

    # BRB BIO — the bathroom break announcement
    # Thread: "BRB BIO" — 21 points, people still remember this
    "Brbbio",         # "brb bio" = be right back, bathroom break; pre-AFK culture

    # SAMMICH — internet-speak for sandwich
    # Thread: mentioned by MrPayDay
    "Sammich",        # "sammich" — leet speak for sandwich; "make me a sammich"

    # NUBLET — diminutive of nub/noob
    "Nublet",         # "you nublet" — an affectionate version of calling someone a noob

    # FACEPALM — the reaction
    "Facepalm",       # the facepalm — when someone does something obviously dumb
                      # Became a universal reaction before becoming an emoji

    # OMGWTF — the WTF expansion
    "Omgwtf",         # "omg wtf" — the double shock reaction

    # PLOX / PL0X — "please" in leet
    # Thread: mentioned ("plox" - meaning please)
    "Plox",           # "plox" — leet speak for "please"; "rush plox"
    "Pl0x",           # leet version with zero

    # LOWPINGER — a T1/cable connection player
    # Thread: "lowpinger" listed by xtrxrzr
    "Lowpinger",      # someone with a low ping — the privileged class in early online gaming

    # ZEROES AND ONES CULTURE
    "Leet",           # "leet" / "elite" - may be taken but try
    "Zomg",           # "zOMG" — mentioned in thread (66 points comment)

    # FLAMEBAIT — already confirmed available
    # From the thread: "getting flamed" - 366 points
    "Flamewar",       # a flame war — an online argument that escalates into insults

    # PKer — player killer; EQ/UO/RS term
    # Thread: "Is PKer ever used anymore?" at the end
    "PKer",           # player killer — someone who hunts other players
    "PKing",          # the act of player killing

    # TRAIN — an EverQuest term for accidentally pulling all enemies in a zone
    # Thread: "Train. AFK." from EQ days
    "Train",          # "TRAIN TO ZONE!" — the EQ warning when someone pulled an entire dungeon

    # MOB — mobile object; enemy in MMOs
    # Thread: "mob" mentioned as old MMO term
    "Mobbing",        # killing groups of mobs; mob farming

    # GRUE — from Zork; "It is pitch black. You are likely to be eaten by a grue."
    # Thread: "Eaten by a Grue" — mentioned
    "Grue",           # the Zork monster — "it is pitch black, you are likely to be eaten by a grue"
                      # One of the oldest gaming references; text adventure era
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
    print(f"Checking {total} handles from the 'Lost PC Gaming Vocabulary' Reddit thread...\n")
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
    with open("rsi_handle_results_v15.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v15.json")


if __name__ == "__main__":
    main()
