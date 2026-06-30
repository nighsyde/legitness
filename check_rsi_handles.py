#!/usr/bin/env python3
"""
Check RSI (Roberts Space Industries) handle availability.
A 404 response means the name is available.
A 200 response means the name is taken (profile exists).
"""

import sys
import time
import requests
import json
from datetime import datetime

# ─── Iconic gaming names ────────────────────────────────────────────────────
# Characters, locations, games, slang, companies — things anyone will
# instantly recognise in 20 years.

NAMES = [
    # ── Halo ──────────────────────────────────────────────────────────────
    "MasterChief", "Cortana", "Arbiter", "Spartan", "UNSC",

    # ── Doom ──────────────────────────────────────────────────────────────
    "DoomGuy", "DoomSlayer", "Doomguy",

    # ── Half-Life / Portal ────────────────────────────────────────────────
    "Gordon", "GordonFreeman", "GLaDOS", "Chell", "Wheatley",

    # ── Minecraft ─────────────────────────────────────────────────────────
    "Herobrine", "Creeper", "Enderman", "Notch", "Pickaxe",

    # ── Pokémon ───────────────────────────────────────────────────────────
    "Pikachu", "Charizard", "Mewtwo", "Eevee", "Bulbasaur",
    "Squirtle", "Gengar", "Snorlax", "Lucario", "Greninja",

    # ── The Legend of Zelda ───────────────────────────────────────────────
    "Link", "Zelda", "Ganondorf", "Ganon", "Hyrule", "Triforce",
    "Midna", "Navi",

    # ── Mario universe ────────────────────────────────────────────────────
    "Mario", "Luigi", "Bowser", "Peach", "Yoshi", "Wario",
    "Waluigi", "DonkeyKong", "Toad", "Rosalina",

    # ── Metroid / F-Zero / Star Fox ──────────────────────────────────────
    "Samus", "Ridley", "CaptainFalcon", "FoxMcCloud", "Falco",

    # ── Kirby / Smash Bros ────────────────────────────────────────────────
    "Kirby", "KingDedede", "MetaKnight",

    # ── Sonic the Hedgehog ────────────────────────────────────────────────
    "Sonic", "Tails", "Knuckles", "ShadowTheHedgehog", "Eggman",
    "Robotnik", "Rouge",

    # ── Final Fantasy ─────────────────────────────────────────────────────
    "Sephiroth", "CloudStrife", "Aerith", "Tifa", "Barret",
    "Lightning", "Tidus", "Yuna", "Vivi", "Kefka", "Terra",
    "Chocobo", "Midgar",

    # ── Metal Gear Solid ──────────────────────────────────────────────────
    "SolidSnake", "BigBoss", "LiquidSnake", "Raiden", "Otacon",
    "Meryl", "Codec",

    # ── World of Warcraft / Warcraft ──────────────────────────────────────
    "Arthas", "LichKing", "Thrall", "Illidan", "Ragnaros",
    "Sylvanas", "Jaina", "Anduin", "Gul'dan", "Guldan",
    "Azeroth", "Orgrimmar", "Stormwind",

    # ── Diablo ────────────────────────────────────────────────────────────
    "Diablo", "Tristram", "Sanctuary", "Deckard",

    # ── StarCraft ─────────────────────────────────────────────────────────
    "Kerrigan", "Raynor", "Zergling", "Protoss", "Zerg",

    # ── Street Fighter ────────────────────────────────────────────────────
    "Ryu", "Ken", "ChunLi", "Akuma", "Guile", "Blanka",
    "Zangief", "Hadouken",

    # ── Mortal Kombat ─────────────────────────────────────────────────────
    "Scorpion", "SubZero", "LiuKang", "Shang", "Raiden",
    "Kitana", "Fatality",

    # ── Overwatch ─────────────────────────────────────────────────────────
    "Tracer", "Genji", "Hanzo", "Widowmaker", "Reaper",
    "Reinhardt", "Mercy", "Pharah", "McCree", "Cassidy",

    # ── League of Legends ─────────────────────────────────────────────────
    "Teemo", "Yasuo", "Jinx", "Lux", "Thresh", "Faker",
    "Ahri", "Vayne", "Zed", "Yone",

    # ── Counter-Strike ────────────────────────────────────────────────────
    "CounterTerrorist", "Defuse", "Flashbang",

    # ── Grand Theft Auto ──────────────────────────────────────────────────
    "NikoBellic", "TrevorPhilips", "MichaelDeSanta",
    "CarlJohnson", "ViceCity", "LibertyCity",

    # ── Red Dead Redemption ───────────────────────────────────────────────
    "ArthurMorgan", "JohnMarston", "DutchVanDerLinde",

    # ── The Elder Scrolls / Skyrim ────────────────────────────────────────
    "Dovahkiin", "Dragonborn", "Alduin", "Tamriel", "Skyrim",
    "FusRoDah", "Whiterun",

    # ── Fallout ───────────────────────────────────────────────────────────
    "VaultBoy", "Wasteland", "Brotherhood", "PipBoy", "Ghoul",

    # ── BioShock ──────────────────────────────────────────────────────────
    "Rapture", "AndrewRyan", "BigDaddy", "LittleSister",
    "BioShock", "Columbia",

    # ── Assassin's Creed ─────────────────────────────────────────────────
    "Ezio", "Altair", "Desmond", "Bayek", "Eivor",

    # ── Resident Evil ─────────────────────────────────────────────────────
    "LeonKennedy", "JillValentine", "ChrisRedfield",
    "ClairRedfield", "Nemesis", "Umbrella",

    # ── Tomb Raider ───────────────────────────────────────────────────────
    "LaraCroft",

    # ── Borderlands ───────────────────────────────────────────────────────
    "HandsomeJack", "Claptrap", "Lilith", "Vault",

    # ── Undertale ─────────────────────────────────────────────────────────
    "Sans", "Papyrus", "Toriel", "Undyne", "Alphys",
    "Flowey", "Asgore", "Frisk", "Chara",

    # ── NieR: Automata ────────────────────────────────────────────────────
    "YorHa", "Emil",

    # ── Persona ───────────────────────────────────────────────────────────
    "Joker", "Morgana", "Ryuji", "Makoto",

    # ── Chrono Trigger ────────────────────────────────────────────────────
    "Crono", "Lavos", "Lucca", "Frog", "Magus",

    # ── EarthBound / Mother ───────────────────────────────────────────────
    "Ness", "Giygas", "PK", "Onett",

    # ── Mass Effect ───────────────────────────────────────────────────────
    "Shepard", "Garrus", "Liara", "Wrex", "Normandy",

    # ── Destiny ───────────────────────────────────────────────────────────
    "Cayde", "Zavala", "Ikora", "Guardian", "Drifter",

    # ── Dark Souls / Elden Ring ───────────────────────────────────────────
    "Tarnished", "Melina", "Ranni", "Malenia", "Estus",
    "Solaire", "Gwyn", "Artorias",

    # ── Animal Crossing ───────────────────────────────────────────────────
    "TomNook", "Isabelle", "KKSlider",

    # ── Stardew Valley / indie icons ─────────────────────────────────────
    "Pelican", "Stardew",

    # ── Among Us ─────────────────────────────────────────────────────────
    "Impostor", "Crewmate", "Amogus", "Vented",

    # ── Fortnite ─────────────────────────────────────────────────────────
    "BattleBus", "BuildMode", "Tilted",

    # ── RuneScape legends ────────────────────────────────────────────────
    "Zezima",

    # ── Locations / worlds ────────────────────────────────────────────────
    "Pandaria", "Lordaeron", "Icewind",

    # ── Companies / brands ────────────────────────────────────────────────
    "Blizzard", "Rockstar", "Bungie", "Naughty", "Valve",

    # ── Gaming slang ──────────────────────────────────────────────────────
    "Respawn", "Headshot", "Speedrun", "Noclip", "GodMode",
    "Pwned", "Frag", "Aimbot", "Teabag", "Camper",
    "Ragequit", "OneShot", "Tryhard", "Clutch", "Wombo",
    "LastHit", "GankLane", "BattlePass", "LootBox",
    "NoScope", "Quickscope", "PentaKill",
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

DELAY_BETWEEN_REQUESTS = 1.5  # seconds — be polite to their servers


def check_handle(name: str, session: requests.Session) -> dict:
    url = BASE_URL.format(name)
    try:
        resp = session.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        status = resp.status_code
        available = status == 404
        return {"name": name, "status": status, "available": available, "error": None}
    except requests.RequestException as exc:
        return {"name": name, "status": None, "available": None, "error": str(exc)}


def main():
    print(f"Checking {len(NAMES_DEDUPED)} RSI handles ...\n")

    available = []
    unavailable = []
    errors = []

    with requests.Session() as session:
        for i, name in enumerate(NAMES_DEDUPED, 1):
            result = check_handle(name, session)
            status_str = str(result["status"]) if result["status"] else "ERR"

            if result["error"]:
                tag = "ERROR"
                errors.append(result)
            elif result["available"]:
                tag = "AVAILABLE"
                available.append(result)
            else:
                tag = "TAKEN   "
                unavailable.append(result)

            print(f"[{i:>3}/{len(NAMES_DEDUPED)}] {status_str:>3}  {tag}  {name}", flush=True)

            if i < len(NAMES_DEDUPED):
                time.sleep(DELAY_BETWEEN_REQUESTS)

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    print(f"\n✅  AVAILABLE ({len(available)} names):")
    for r in available:
        print(f"   {r['name']}")

    print(f"\n❌  TAKEN ({len(unavailable)} names):")
    for r in unavailable:
        print(f"   {r['name']}")

    if errors:
        print(f"\n⚠️  ERRORS ({len(errors)} names):")
        for r in errors:
            print(f"   {r['name']}  —  {r['error']}")

    # ── Save JSON ─────────────────────────────────────────────────────────
    output = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "total": len(NAMES_DEDUPED),
        "available": [r["name"] for r in available],
        "unavailable": [r["name"] for r in unavailable],
        "errors": errors,
    }
    with open("rsi_handle_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nFull results saved to rsi_handle_results.json")


if __name__ == "__main__":
    main()
