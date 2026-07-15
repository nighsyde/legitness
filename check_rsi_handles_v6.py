#!/usr/bin/env python3
"""
RSI handle availability checker — batch 6.
WoW PvP + CS 1.6 trash talk, slang, and PvP terminology.
404 = available. 200 = taken.
"""

import sys
import time
import requests
import json
from datetime import datetime

NAMES = [
    # ── WoW PvP — arena & battleground culture ────────────────────────────
    "Stunlock",        # being chain CC'd with no ability to act; the most helpless WoW feeling
    "Globaled",        # killed so fast you had no time to react; "I got globaled"
    "SitBoy",          # trash talk typed after silencing a caster; pure cruelty
    "PillarHumper",    # the arena player who hides behind pillars and refuses to fight
    "RNGesus",         # praying to the god of random chance; "please RNGesus"
    "PillarHump",      # the act of hiding behind pillars
    "Stunbot",         # a Rogue who does nothing but stun repeatedly
    "Trinket",         # using your PvP CC-break trinket; also a noun and a verb in WoW
    "Vanished",        # a Rogue vanishing mid-fight; the most frustrating disappearing act
    "HighWarlord",     # the Horde Rank 14 PvP title; required insane grinding
    "GrandMarshal",    # the Alliance Rank 14; the other side of the same grind
    "Gladiator",       # the top seasonal arena rank; the WoW PvP dream
    "Duelist",         # arena rank just below Gladiator
    "HonorFarming",    # grinding honor points in battlegrounds
    "GraveyardCamp",   # camping enemies at their resurrection point; pure evil
    "CorpseCamp",      # same thing; killing someone repeatedly at their spawn
    "Turtling",        # the defensive strategy that refuses to push; "stop turtling"
    "NinjaCap",        # capturing an objective while nobody was watching
    "FlagCarrier",     # the person running with the flag in WSG
    "PvPTrinket",      # the on-use CC-break item every PvP player needed
    "Backpedaler",     # moving backward with S key instead of strafing; classic noob tell
    "Counterspell",    # the Mage interrupt; stopping a cast mid-channel
    "Sheeped",         # being polymorphed into a sheep by a Mage
    "Sapped",          # hit by the Rogue's Sap from stealth before the fight started
    "Cycloned",        # hit by the Druid's Cyclone CC; floating helplessly
    "Feared",          # running around in Fear with no control; the warlock special
    "Disoriented",     # various disorient effects; still CC'd just differently
    "Procced",         # a random effect triggered at a clutch moment; "I procced"
    "SwiftyMacro",     # Swifty's legendary one-shot warrior macro that crashed servers
    "Rerollhunter",    # "just reroll hunter" — telling someone to play the easiest class
    "LolRet",          # laughing at Ret Paladins before Wrath made them OP
    "FaceMelter",      # Shadow Priest "face melt" DPS burst
    "ShadowWeave",     # Shadow Priest mechanic
    "TwoShot",         # killing someone in exactly two hits
    "GlobalCd",        # the Global Cooldown — the 1.5s wait between abilities
    "HardSwap",        # instantly switching to a new kill target in arena
    "Peel",            # peeling — getting enemies off your teammate with CC
    "TradedKills",     # both players dying at the same moment; "we traded"
    "RmpComp",         # Rogue Mage Priest arena comp; the most feared 3v3 comp
    "GoGoGo",          # the signal to focus and kill a target NOW
    "Bursting",        # dumping all cooldowns to kill something fast
    "Tunneling",       # focusing one target while ignoring everything else
    "CleaveCleave",    # bringing an AoE composition to sweep multiple targets
    "DampeningWins",   # dampening was the healing reduction in long arena games

    # ── WoW PvP — class-specific trash talk ──────────────────────────────
    "StealthNoob",     # any stealth class who only attacked from stealth
    "Kitebot",         # a Hunter or Frost Mage who just ran and kited forever
    "HealBot",         # a healer who did nothing but heal (derogatory)
    "BubbleHearth",    # Paladin bubbling (Divine Shield) then hearthstoning home; cowardly escape
    "BubbleHearthstoner", # same, longer
    "IceBlock",        # Mage emergency survival cooldown; "he iceblocked"
    "Barkskinned",     # Druid using Barkskin to reduce damage
    "BearForm",        # Druid going bear in desperation when low health
    "ChickenForm",     # Moonkin/Balance Druid form; people called it chicken form

    # ── CS 1.6 PvP — trash talk & culture ────────────────────────────────
    "GGEZ",            # "good game easy" — the ultimate post-win taunt
    "ClutchOrKick",    # the pressure phrase every CS player has heard
    "OneTapper",       # the player who gets one-tap headshots; ScreaM's legacy
    "SpinBot",         # the cheat where your aim spins 360 constantly
    "Spinbotter",      # someone using spinbot
    "SkillIssue",      # the modern insult that perfectly fits retro gaming failures
    "GetRekt",         # the classic trash talk
    "AceRound",        # killing all 5 opponents in one round
    "HardCarry",       # one player carrying the whole team
    "EcoKill",         # killing someone with cheap weapons on an eco round
    "ForceRound",      # force buying when you shouldn't have the money
    "DropMe",          # asking a teammate to drop you a weapon
    "PlantIt",         # the bomb plant call
    "Retake",          # retaking a bombsite after the bomb is planted
    "Rushed",          # being rushed by the whole team
    "Peeked",          # being peeked — someone looked around a corner at you
    "PreAimed",        # they were already aiming at your head before you appeared
    "AngleHeld",       # holding a corner angle — the camper defense
    "WallBanged",      # being shot through a wall
    "FlashTraded",     # flashing your own teammate by accident
    "CycleKill",       # killing someone as they came through a cycle
    "TimeBuy",         # buying time for the bomb to explode
    "SmokeSpam",       # throwing smokes everywhere without knowledge of lineups
    "NadeStack",       # stacking grenades in a choke point
    "KnifeRound",      # the knife-only round to decide sides
    "PistolGod",       # someone who is insane with pistols
    "DeagleGod",       # the Deagle specialist; feared at close range
    "AimPunch",        # the screen shake when you take damage; throws off aim
    "Tapfire",         # tapping single shots for accuracy vs. spraying
    "Spraydown",       # spraying a whole clip at someone
    "HeadLevel",       # having your crosshair at head level at all times
    "PixelWalk",       # olofmeister's famous smoke pixel walk to see over geometry
    "JumpThrow",       # the grenade technique requiring precise timing
    "LineupSmoke",     # a perfectly lined-up smoke grenade
    "ThreeKKnife",     # getting a triple-kill with the knife; the ultimate disrespect
    "DinkShot",        # a shot that hits the helmet but doesn't kill; "dinked"
    "Dinked",          # being hit in the helmet without dying; humiliating
    "FullHPAce",       # getting an ace without taking any damage
    "SoloEntry",       # entering a bombsite alone as the first player
    "TradeKill",       # dying but your teammate kills the person who killed you
    "EcoRound",        # the round where you save money with cheap or no weapons
    "ForceGG",         # surrendering before the game is over; "just gg"
    "GoNext",          # "this game is lost, go next" — giving up
    "StartFreshRound", # resetting mentally after a bad round
    "ClanTag",         # the [CLAN] tag prefix that showed your affiliation
    "NoRecoil",        # accusation of cheating — "he has no recoil"
    "LagSwitch",       # the cheating device that caused artificial lag
    "LagSwitcher",     # the person using one
    "Warping",         # the visual effect of someone using a lag switch
    "Teleporting",     # same — the rubber-band teleport lag
    "PureRNG",         # blaming a loss on pure random chance
    "LuckNoskill",     # the accusation that someone just got lucky
    "TryHarder",       # telling someone to try harder as an insult
    "CasualPlayer",    # the CS insult implying you're not serious
    "PubStar",         # someone who's great in public servers but bad in scrims
    "ScrimGod",        # the opposite — only good in competitive practice matches
]

# Deduplicate
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
    print(f"Checking {total} PvP slang handles (WoW + CS 1.6)...\n")
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
    with open("rsi_handle_results_v6.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v6.json")


if __name__ == "__main__":
    main()
