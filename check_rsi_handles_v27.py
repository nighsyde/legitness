#!/usr/bin/env python3
"""
RSI handle checker — batch 27.
Early 4chan culture (2003-2008): /b/, Anonymous, the raid culture,
original meme language, image board slang, the operations,
combined with hacker/Linux for the full underground picture.
"We are Anonymous. We are Legion. We do not forgive. We do not forget."
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── CORE /b/ CULTURE — the original chaos engine ─────────────────────
    "Topkek",         # the highest form of approval on 4chan; "top kek"
                      # kek = lol (from WoW's cross-faction translation)
                      # topkek = you've earned maximum laughs
    "Lurkmor",        # "lurk more" — posted to newcomers who reveal ignorance
                      # the oldest lesson: observe before you speak
    "Lurkmore",       # same, alternate spelling
    "Greentext",      # the >implying storytelling format; > makes text green
                      # ">be me" — the opening of every 4chan story
    "Copypasta",      # text copied and pasted endlessly across the internet
                      # before "meme" was the word, this was the word
    "Anonsaid",       # "Anonymous said" — the entire identity
    "WeLegion",       # "We are Legion" — the Anonymous rallying cry
    "WeAnon",         # "We are Anonymous" — the declaration
    "ExpectUs",       # "Expect us" — the threat at the end of Anonymous statements
    "NorForgive",     # "We do not forgive" — the creed
    "NorForget",      # "We do not forget" — the other half
    "ForTheLulz",     # the entire motivation of early /b/; do it for the laughs
    "LulzSec",        # Lulz Security — the hacker group that hit Sony, FBI, CIA
                      # born from Anonymous; operated 2011; "hacking for the lulz"
    "ForLulz",        # shortened version
    "Lulzcorp",       # the imaginary corporation of lulz

    # ── THE ANONYMOUS OPERATIONS ───────────────────────────────────────────
    "Chanology",      # Project Chanology — Anonymous vs. Scientology (2008)
                      # the most organized raid Anonymous ever ran; real protest
    "OpPayback",      # Operation Payback — DDoS attacks on RIAA, MPAA etc.
    "OpDarknet",      # Operation Darknet — Anonymous vs. child abuse on darknet
    "OpSony",         # the Sony hack operation
    "WeFromNet",      # "We're from the internet" — the raid announcement
    "Internet Hate Machine", # Fox News called Anonymous the "Internet Hate Machine"

    # ── THE /b/ RAIDS ─────────────────────────────────────────────────────
    "PoolsClosed",    # "Pool's closed" — the Habbo Hotel raid phrase
                      # 4channers filled Habbo Hotel with Guy Fawkes avatars
                      # blocking the pool: "Pool's closed due to AIDS"
    "DueToAids",      # the second half of the Habbo phrase
    "HabboRaid",      # the Habbo Hotel raid itself
    "NoSwimming",     # "No swimming" — the pool's closed
    "GuyFawkes",      # the mask; V for Vendetta → Anonymous symbol
    "VforVendetta",   # the source material

    # ── THE MEME ORIGINS — pre-"meme" era ─────────────────────────────────
    "Longcat",        # Longcat is long — one of the first viral image memes
                      # a stretched white cat photo; the original meme format
    "Tacgnol",        # the dark mirror of Longcat; reverse + black
                      # an internet villain born from image board lore
    "Wojak",          # the feels guy; the bald crying man
                      # "I know that feel bro" — the original Wojak use
    "FeelsGuy",       # what Wojak was originally called
    "RageFace",       # the rage comic faces; FU face
    "TrollFace",      # the Trollface; "problem?"
    "CoolFace",       # the cool face
    "ForeverAlone",   # the forever alone meme face; loneliness as identity
    "PicRelated",     # "pic related" — the image is relevant to the post
    "SauceNeeded",    # "sauce?" — asking for the source

    # ── IMAGE BOARD VOCABULARY ────────────────────────────────────────────
    "OPisaFag",       # "OP is a fag" — the standard /b/ greeting
                      # (the entire culture of that era's insult structure)
    "SagePoster",     # someone who sages (marks posts to not bump threads)
    "NameFag",        # someone who posts with a name; despised on /b/
    "TripFag",        # someone who uses a tripcode; also despised on /b/
    "DrawFag",        # someone who draws for the board; actually respected
    "WriteFag",       # someone who writes stories; greentext writefags
    "SummerFag",      # new users who arrive in summer; "eternal september"
    "Oldfag",         # a veteran; "I was there when..."
    "Newfag",         # a new arrival; knows nothing; hasn't lurked
    "Samefag",        # one person posting as multiple people
    "Lolcow",         # someone who provides entertainment through being upset
                      # you poke the cow; it produces lol milk

    # ── THE GAME — the internet's first universal meme ────────────────────
    "TheGame",        # a game you lose when you think about it
                      # you just lost The Game. we all did.
    "JustLostIt",     # "I just lost The Game" — the announcement
    "YouJustLost",    # "you just lost The Game" — telling someone

    # ── BOXXY AND THE QUEEN ERA ───────────────────────────────────────────
    "Boxxy",          # Catherine Wayne; the YouTube girl who became 4chan's queen
                      # the Boxxy wars split /b/ into factions
    "IAmBoxxy",       # "I am Boxxy, you see" — her opening line
    "GoddesBoxxy",    # the Boxxy worship

    # ── TRIPCODES AND POST NUMBERS ────────────────────────────────────────
    "CheckedDubs",    # checking doubles; acknowledging matched post numbers
    "Blessed",        # "blessed" trips/dubs/quads
    "HolyTrips",      # getting three matching digits in your post number
    "QuadGod",        # rolling quads; divine post numbers
    "Dubsman",        # the man who gets the dubs
    "Rollan",         # "rollan for X" — rolling for a random result

    # ── 4CHAN CROSSOVER WITH HACKING ──────────────────────────────────────
    # When Anonymous moved from trolling to actual hacktivism
    "Hacktivist",     # the term cDc invented; Anonymous popularized
    "DigitalGhost",   # the digital ghost; Anonymous as identity
    "AnonMask",       # wearing the anonymous mask
    "Legion",         # "We are Legion" — the unit, not the individual
    "Collective",     # the Anonymous collective
    "Hivemind",       # the 4chan hive mind; collective action without leadership
    "Chanops",        # chan operations; the raids/operations

    # ── THE LANGUAGE BLEND: 4CHAN + LINUX ─────────────────────────────────
    "SudoAnon",       # sudo as anon; elevated anonymous action
    "DevAnon",        # dev/anon; the anonymous developer
    "NullAnon",       # null anonymous; nobody in the void
    "RootAnon",       # root anon; the highest privilege anonymous actor
    "GhostRoot",      # root access by a ghost; invisible escalation
    "ClearLog",       # already confirmed available — cleaning the auth log
    "Authless",       # without authentication; unauthorized but present
    "Unchecked",      # unchecked; no verification; wild
    "Unlogged",       # not logged; invisible in the system
    "Traceless",      # leaving no trace
    "Ghostwrite",     # writing anonymously; ghost writing for the lulz

    # ── EARLY INTERNET/4CHAN PHILOSOPHY ──────────────────────────────────
    "AutumnalOne",    # the autumnal one; eternal autumn (eternal september)
    "EternalSep",     # Eternal September — when the internet opened to everyone
                      # September 1993: AOL users flooded Usenet; it never recovered
    "Netizen",        # a citizen of the internet
    "Lurker",         # (already taken)
    "Pilgrim",        # new to the internet; a pilgrim
    "Observer",       # observing but not posting; the lurker identity
    "Spectator",      # watching without participating
    "Witness",        # I was there when...
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
    print(f"Checking {total} early 4chan/underground/Linux handles...\n")
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
    with open("rsi_handle_results_v27.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v27.json")


if __name__ == "__main__":
    main()
