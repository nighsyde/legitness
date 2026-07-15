#!/usr/bin/env python3
"""
RSI handle checker — batch 21.
90s/early 2000s cartoon characters, TV shows, video game characters,
iconic locations. Capturing the era: Toonami, DBZ, Cartoon Network,
Nickelodeon, classic gaming characters, anime.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── TOONAMI / CARTOON NETWORK ─────────────────────────────────────────
    "Toonami",        # Cartoon Network's action programming block — THE after-school ritual
    "TOM",            # TOM — the Toonami robot host who introduced every show
    "SaraTV",         # Sara — TOM's AI companion on the Absolution
    "Absolution",     # the Absolution — the ship TOM and Sara flew through space
    "Moltar",         # the original Toonami host before TOM
    "DextersLab",     # Dexter's Laboratory — "omelette du fromage"
    "Dexters",        # Dexter's shortened
    "MandarkLab",     # Mandark — Dexter's rival
    "Mandark",        # Dexter's nemesis
    "DeedeeDexter",   # "Dee Dee! Get out of my laboratory!"
    "SamuraiJack",    # Samurai Jack — "and then, I saw IT... the Aku"
    "Aku",            # the shapeshifting master of darkness; "FOOL!"
    "JohnnyBravo",    # Johnny Bravo — the self-obsessed muscleman
    "CourageCoward",  # Courage the Cowardly Dog
    "Muriel",         # Muriel — Courage's owner
    "Eustace",        # Eustace — "Stupid dog! You make me look bad!"
    "Nowhere",        # Nowhere — the town Courage lives in, middle of nowhere
    "PowerpuffGirls", # Powerpuff Girls
    "Blossom",        # the leader Powerpuff
    "Bubbles",        # the cute Powerpuff
    "Buttercup",      # the tough Powerpuff
    "MojoJojo",       # the main villain — "I, Mojo Jojo, shall..."
    "Townsville",     # the city the Powerpuff Girls protect
    "SpaceGhost",     # Space Ghost Coast to Coast — proto-Adult Swim
    "Zorak",          # Zorak — Space Ghost's villain turned bandleader
    "Brak",           # Brak — the loveable idiot villain
    "SwatKats",       # SWAT Kats: The Radical Squadron — the underground favorite

    # ── NICKELODEON ERA ───────────────────────────────────────────────────
    "Rugrats",        # Rugrats — the babies show; Angelica, Tommy, Chuckie
    "Angelica",       # Angelica Pickles — the villain of Rugrats
    "Reptar",         # Reptar — the dinosaur toy all the babies loved
    "CatDog",         # CatDog — the conjoined cat/dog
    "Rocko",          # Rocko's Modern Life — the Australian wallaby
    "HeyArnold",      # Hey Arnold — the football-head kid
    "Helga",          # Helga Pataki — secretly in love with Arnold
    "InvaderZim",     # Invader Zim — "ZIM!" cult classic
    "Zim",            # the alien invader
    "GIR",            # GIR — Zim's defective robot; "I love this show!"
    "Dib",            # Dib — the human who knows about Zim
    "Tallests",       # the Almighty Tallests — Zim's leaders
    "Catdog",         # alternate casing

    # ── DRAGONBALL Z — the crown jewel of Toonami ─────────────────────────
    "Goku",           # THE protagonist — almost certainly taken
    "Vegeta",         # the Prince of all Saiyans — probably taken
    "Piccolo",        # the Namekian mentor — probably taken
    "Gohan",          # Goku's son — probably taken
    "Frieza",         # the galactic emperor — probably taken
    "Trunks",         # future Trunks — probably taken
    "Krillin",        # the best human fighter
    "Yamcha",         # the desert bandit; later the meme
    "Tien",           # Tien Shinhan — three-eyed warrior
    "Nappa",          # Nappa — Vegeta's partner; "VEGETA! What does the scouter say?"
    "Raditz",         # Goku's evil brother; the start of Z
    "Bardock",        # Goku's father; the prequel special
    "Broly",          # the Legendary Super Saiyan
    "Cell",           # the bio-android villain
    "Beerus",         # God of Destruction
    "Saiyan",         # the warrior race
    "Namekian",       # Piccolo's race
    "Scouter",        # the power level device; "IT'S OVER 9000!"
    "Kamehameha",     # the iconic energy blast
    "Kakarot",        # Goku's Saiyan birth name — "KAKAROT!"
    "Bulma",          # Bulma Brief — the genius inventor
    "Majin",          # Majin — the magic word; Majin Buu, Majin Vegeta
    "Babidi",         # the wizard who controlled Majin Vegeta
    "OverNineThousand", # the meme before memes were called memes

    # ── SAILOR MOON — also on Toonami ────────────────────────────────────
    "Usagi",          # Sailor Moon's real name
    "Mamoru",         # Tuxedo Mask's real name
    "Rini",           # Chibiusa / Rini — the future daughter
    "Darien",         # Tuxedo Mask's dubbed name

    # ── GUNDAM WING ──────────────────────────────────────────────────────
    "HeeroYuy",       # the main pilot — "I'll kill you"
    "Heero",          # shortened
    "Duo",            # Duo Maxwell — the Shinigami pilot
    "Deathscythe",    # Duo's Gundam — Gundam Deathscythe
    "Trowa",          # Trowa Barton — the circus performer pilot
    "Quatre",         # Quatre Raberba Winner
    "WuFei",          # Chang WuFei
    "Treize",         # Treize Khushrenada — the OZ leader
    "ZecsMerquise",   # Zechs Merquise — the Lightning Count
    "Zechs",          # shortened
    "Epyon",          # the Gundam Epyon
    "OZsoldier",      # the OZ military organization
    "Tallgeese",      # the legendary prototype mobile suit

    # ── POKEMON (early era) ───────────────────────────────────────────────
    "Mewtwo",         # the most powerful Pokemon; the movie star
    "Mew",            # the mythical original
    "Charizard",      # "Charizard, I choose you" — the fan favorite
    "Blastoise",      # the water starter final form
    "Venusaur",       # the grass starter final form
    "Pikachu",        # probably taken
    "Gengar",         # the ghost Pokemon fan favorite
    "Snorlax",        # the sleeping giant
    "Eevee",          # the evolution Pokemon
    "Vaporeon",       # Eevee's water evolution
    "Jolteon",        # Eevee's lightning evolution
    "Flareon",        # Eevee's fire evolution
    "Alakazam",       # the psychic spoon Pokemon
    "Machamp",        # the four-armed fighting Pokemon
    "Dragonite",      # the dragon master Pokemon
    "Aerodactyl",     # the fossil Pokemon
    "Haunter",        # the ghost evolution
    "Clefairy",       # the pink fairy Pokemon
    "Cubone",         # the lonely skull Pokemon; secretly deep lore
    "Lavender",       # Lavender Town — infamous for the creepypasta
    "Cerulean",       # Cerulean City — Misty's gym
    "Cinnabar",       # Cinnabar Island
    "Pallet",         # Pallet Town — where it all began
    "ViridianCity",   # Viridian City
    "Pewter",         # Pewter City — Brock's gym
    "GaryOak",        # Gary Oak — the rival who was always a step ahead
    "Brock",          # the rock gym leader
    "Misty",          # the water gym leader
    "OakLab",         # Professor Oak's lab
    "Pokecenter",     # the Pokemon Center

    # ── YUGIOH ───────────────────────────────────────────────────────────
    "Yugi",           # Yugi Muto — the main character
    "Yami",           # Yami Yugi — the pharaoh spirit
    "Kaiba",          # Seto Kaiba — the rival; "I will not lose to you"
    "BluEyes",        # Blue-Eyes White Dragon — Kaiba's ace
    "DarkMagician",   # Yugi's ace card
    "Exodia",         # Exodia the Forbidden One — automatic win
    "Joey",           # Joey Wheeler — the best friend
    "Tristan",        # Tristan Taylor
    "Pegasus",        # Maximillion Pegasus — the Millennium Eye villain
    "Bakura",         # Yami Bakura — the tomb robber

    # ── VIDEO GAME CHARACTERS — 90s/early 2000s ──────────────────────────
    "Samus",          # Samus Aran — Metroid; one of gaming's first female heroes
    "Ridley",         # the Meta-Ridley — Metroid villain
    "Kraid",          # Kraid — Metroid boss
    "Spyro",          # Spyro the Dragon — the purple dragon
    "Sparx",          # Sparx — Spyro's dragonfly companion
    "CrashBandicoot", # Crash Bandicoot — the PlayStation mascot
    "Crash",          # shortened
    "Cortex",         # Neo Cortex — Crash's villain
    "AkuAku",         # Aku Aku — the friendly mask
    "ClayCrash",      # the clay Crash from the commercials

    # ── LOCATIONS FROM 90S GAMING ─────────────────────────────────────────
    "LavaZone",       # generic lava zone — every 90s game had one
    "IceZone",        # generic ice zone
    "GreenHill",      # Green Hill Zone — Sonic's iconic first stage
    "CarnivalNight",  # Carnival Night Zone — Sonic 3; the barrel puzzle
    "Emerald",        # the Chaos Emeralds
    "DeathEgg",       # Death Egg — Sonic's version of the Death Star
    "MarbleGarden",   # Marble Garden Zone
    "Metroville",     # the Incredibles city
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
    print(f"Checking {total} 90s/early 2000s cartoon/TV/game handles...\n")
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
    with open("rsi_handle_results_v21.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v21.json")


if __name__ == "__main__":
    main()
