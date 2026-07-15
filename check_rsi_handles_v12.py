#!/usr/bin/env python3
"""
RSI handle availability checker — batch 12.
The curated shortlist: genuinely legendary handles from the era.
No filler. Every name here has a real story.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── THE ONE ───────────────────────────────────────────────────────────
    "Thresh",         # Dennis Fong. World's first pro gamer (Guinness WR). Won Carmack's
                      # Ferrari at Quake Red Annihilation 1997. Co-founded Xfire.
                      # Riot named a LoL champion after him. 6 chars. THE handle.

    # ── WoW vanilla legendaries — still discussed on Reddit/forums in 2026 ──
    "Thunderfury",    # THE WoW meme. "Did someone say Thunderfury, Blessed Blade of the
                      # Windseeker?" Still being spammed in trade chat today. Also just
                      # sounds legitimately badass.
    "Benediction",    # The iconic priest staff. Required one of the hardest quests in
                      # vanilla WoW. Called "undeniably the most iconic staff to ever exist."
                      # Still used as transmog 20 years later.
    "Anathema",       # The shadow form of Benediction — same staff, transforms in combat.
                      # Deep vanilla priest lore.
    "Sulfuras",       # Hand of Ragnaros. The other MC legendary alongside Thunderfury.
                      # "Sulfuras" sounds like a proper name.
    "Ashkandi",       # Ashkandi, Greatsword of the Brotherhood — BWL warrior legendary.
                      # "Simple and elegant yet so sinister." — forums, 2025.
    "Judgement",      # The T2 Paladin armor set. Considered by the community the most
                      # iconic-looking armor set in WoW history. Still the #1 transmog.
    "Shadowmourne",   # The ICC legendary axe. "Shadowmourne hungers." Post-Naxx endgame.
    "Dreadnaught",    # T3 Warrior set from Naxxramas. The pinnacle of vanilla achievement.
                      # Only 1% of players ever saw it in 2006.
    "Cryptstalker",   # T3 Hunter set from Naxx. Sounds incredible as a handle.
    "Plagueheart",    # T3 Warlock set from Naxx. Dark and menacing.
    "Bonescythe",     # T3 Rogue set from Naxx. Deadly and specific.
    "Bloodfang",      # T2 Rogue set. Wolves. Fast. Deadly. Also just a dope handle.
    "Netherwind",     # T2 Mage set. Arcane winds. Sounds elemental and cool.
    "Frostmourne",    # Arthas's runeblade. "Frostmourne hungers." The Wrath cinematic.
                      # One of gaming's most dramatic item names.
    "Thunderaan",     # Prince of Air — the lightning elemental at the end of the
                      # Thunderfury quest chain. Extremely niche. Maximum WoW cred.
    "Atiesh",         # Atiesh, Greatstaff of the Guardian — the Naxx legendary staff.
                      # So rare that most players never saw one in 2006.

    # ── WoW characters that transcend WoW ────────────────────────────────
    "Arthas",         # The Lich King. "Arthas, my son..." Wrath cinematic. WC3.
                      # One of gaming's greatest villain arcs.
    "Illidan",        # "You are not prepared!" TBC's iconic villain. WC3 tragedy arc.
                      # One of gaming's most quoted lines.
    "Frostmourne",    # (duplicate filtered)
    "Kerrigan",       # Queen of Blades. StarCraft's greatest character. The protoss/zerg
                      # hybrid villain. Still discussed as one of gaming's best characters.
    "Deathwing",      # The corrupted dragon aspect. The Cataclysm destroyer.
                      # "DEATHWING JUST FLEW OVER MY ZONE" was a server-wide event.
    "Sylvanas",       # Sylvanas Windrunner — the Banshee Queen. WC3, WoW.
                      # One of the most debated WoW characters.
    "Cenarius",       # The demigod of the forest. Ancient WC3/WoW druid lore.

    # ── Competitive gaming legends — real players ─────────────────────────
    "Heaton",         # Christopher "HeatoN" Alesund — Swedish CS 1.6 legend.
                      # Considered one of the greatest CS players of all time.
                      # NiP co-founder. Thousands of hours of VOD proof.
    "Carmack",        # John Carmack — id Software. Made Doom. Made Quake.
                      # The man who invented the modern FPS engine. A god.
    "Romero",         # John Romero — Carmack's creative partner. Doom. Quake.
                      # "John Romero's about to make you his bitch." — the infamous ad.
    "Fatal1ty",       # Johnathan "Fatal1ty" Wendel — legendary Quake/UT/CS pro gamer.
                      # One of the most dominant FPS pros ever. Had his own CPU cooler line.

    # ── D2 items that sound like real handles ─────────────────────────────
    "Windforce",      # The Hydra Bow unique in Diablo 2. One of the most coveted bows.
                      # Sounds incredible. 9 chars.
    "Doombringer",    # The unique Champion Sword in D2. "Doombringer" is just a great name.
    "Grandfather",    # The unique Colossus Blade in D2. The godly sword. Menacing handle.
    "Stormshield",    # The unique Monarch shield in D2. Coveted. Sounds powerful.
    "Tyrael",         # Archangel of Justice in Diablo. Appears in D1, D2, D3.
                      # Gave up his wings. One of gaming's best supporting characters.

    # ── The Xfire connection ──────────────────────────────────────────────
    "Xfire",          # Xfire — THE gaming overlay before Steam. Co-founded by Thresh.
                      # Every serious PC gamer in 2003-2009 had it.
                      # Tracked your hours, showed what friends were playing.
                      # The Steam friends list before Steam had one.

    # ── Things that just sound legendary ────────────────────────────────
    "Frostbrand",     # Frostbrand Weapon — Shaman enchant. Frost damage proc. Sounds great.
    "Stormcaller",    # Generic but epic — fits the era's naming conventions perfectly.
    "Deathcoil",      # Death Coil — Warlock spell in WoW. Also Arthas's WC3 ability.
    "Coldblood",      # Cold Blood — Rogue finisher ability in WoW. Increases crit chance.
                      # "Coldblood" as a handle: calculated, precise, deadly.
    "Shadowstep",     # Rogue ability — teleport behind target. Clean, badass handle.
    "Vendetta",       # Rogue ability in later WoW. Also just a phenomenal handle.
    "Adrenaline",     # Adrenaline Rush — Rogue cooldown. Also a state of being. Feels right.
    "Preparation",    # Prep — the Rogue's ability to reset cooldowns. Deep rogue culture.
    "Vanish",         # Rogue ability — disappear from combat. Clean. Mysterious. 6 chars.
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
    print(f"Checking {total} curated legendary handles...\n")
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
    with open("rsi_handle_results_v12.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v12.json")


if __name__ == "__main__":
    main()
