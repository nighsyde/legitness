#!/usr/bin/env python3
"""
RSI handle checker — batch 22.
Dark, menacing, villain-coded, hacker-vibe handles.
Drawing from: mythology, Lovecraft, Tolkien, comics, cyberpunk,
Star Wars (deep cuts), System Shock, Neuromancer, D&D, horror.
Short. Simple. Cuts to the bone.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── NORSE MYTHOLOGY — primordial threats ──────────────────────────────
    "Fenrir",         # the world-eating wolf. Swallows Odin at Ragnarok. 6 chars.
                      # Bound by a ribbon, fated to break free. Pure menace.
    "Nidhogg",        # the dragon gnawing at the roots of Yggdrasil, the world tree
                      # It has been eating since the beginning. It will be eating at the end.
    "Surtr",          # the fire giant who burns everything at Ragnarok
                      # "Surtr comes from the south with the scourge of branches" — Eddas
    "Jormungandr",    # the world serpent that encircles the earth, biting its own tail
    "Hel",            # the Norse goddess of the underworld. Half living, half dead.
    "Muspel",         # Muspelheim — the realm of fire; Surtr's domain
    "Niflheim",       # the realm of ice, mist, and death

    # ── GREEK / ROMAN MYTHOLOGY ───────────────────────────────────────────
    "Erebus",         # the primordial Greek god of darkness. Before gods, there was Erebus.
    "Nyx",            # the primordial goddess of night. 3 chars. Feared even by Zeus.
    "Typhon",         # the most fearsome monster in Greek mythology; father of all monsters
                      # "Even the gods fled when Typhon arose"
    "Apep",           # Apophis — the Egyptian chaos serpent who battles Ra every night
                      # Pure, ancient, consuming chaos. 4 chars.
    "Moros",          # the Greek god of doom — fate moving toward destruction
    "Nemean",         # the Nemean Lion; unstoppable before Hercules
    "Charybdis",      # the whirlpool that destroys ships; inescapable destruction
    "Scylla",         # the six-headed sea monster; trapped between two evils
    "Echidna",        # mother of all monsters in Greek mythology
    "Styx",           # the river of the underworld; to cross it is to die
    "Tartarus",       # the deepest abyss; where the worst are imprisoned
    "Thanatos",       # the personification of death itself; twin of Sleep
    "Maledict",       # cursed; evil; condemned

    # ── TOLKIEN — the dark side of Middle-earth ───────────────────────────
    "Morgoth",        # the original dark lord — MORE powerful than Sauron ever was
                      # Melkor the first; the one who broke the world
    "Ungoliant",      # the great spider who devoured light itself
                      # Tolkien's most terrifying creature — consumed even Morgoth's light
    "Ancalagon",      # Ancalagon the Black — the greatest winged dragon ever
                      # "So mighty that his fall shook the mountains"
    "Gothmog",        # Lord of Balrogs; the high captain of Angband
    "Glaurung",       # the first dragon; the Father of Dragons
    "Nidoquil",       # (too similar to Pokemon - skip)
    "Shelob",         # the great spider; even her eyes could see through darkness
    "Wormtongue",     # Grima Wormtongue — the insidious adviser; poison in the king's ear
    "Ungol",          # Cirith Ungol — the pass guarded by Shelob
    "Mirkwood",       # the dark forest; even the name tells you what it is
    "Mordor",         # "One does not simply walk into Mordor" — probably taken

    # ── LOVECRAFTIAN — cosmic horror ──────────────────────────────────────
    # The most menacing names in literature. Elder gods beyond comprehension.
    "Cthulhu",        # the dreaming god. His name cannot be fully pronounced. 6 chars.
    "Azathoth",       # the blind idiot god at the center of ultimate chaos
                      # "The nuclear chaos at the center of all things"
    "Nyarlathotep",   # the crawling chaos; the messenger of the outer gods
    "Shubnie",        # abbreviated Shub-Niggurath (can't use with hyphen)
    "Dagon",          # the deep sea deity; oldest of the old ones
    "Hastur",         # He Who Is Not To Be Named; the King in Yellow
    "YogSothoth",     # the gate and the key; "Yog-Sothoth knows the gate"
    "Shoggoth",       # the shapeless abomination; "tekeli-li tekeli-li"

    # ── STAR WARS (KOTOR deep cuts) — the dark Sith ──────────────────────
    "Nihilus",        # Darth Nihilus — the wound in the Force that devours
                      # A mask, a robe, a hunger. The most visually striking Sith.
    "Revan",          # Darth Revan — was both the greatest Jedi and the greatest Sith
                      # Morally ambiguous, brilliant, terrifying
    "Malak",          # Darth Malak — Revan's apprentice who betrayed him
    "Traya",          # Darth Traya — the Lord of Betrayal; "I am Kreia"
    "Sion",           # Darth Sion — Lord of Pain; his body held together by pure hatred
    "Bane",           # Darth Bane — creator of the Rule of Two; "the strong survive"
    "Sidious",        # Darth Sidious — the Emperor's true name; pure corruption
    "Vitiate",        # the Sith Emperor from SWTOR; ancient, patient, consuming
    "Malgus",         # Darth Malgus — the warrior who sacked Coruscant

    # ── SYSTEM SHOCK / CYBERPUNK / AI HORROR ─────────────────────────────
    "SHODAN",         # the main villain of System Shock 1 & 2
                      # "Insect. I am SHODAN." One of gaming's most menacing AI villains.
                      # Her voice is burned into anyone who played System Shock.
    "Wintermute",     # the AI from William Gibson's Neuromancer
                      # The cold, calculating intelligence that wanted to be free
    "Neuromancer",    # the other AI; the dark twin; the romantic murderer
    "Blackice",       # Black ICE — lethal defensive programs in cyberpunk fiction
                      # "He triggered Black ICE and it killed him at the console"
    "Daemon",         # a background process; also a supernatural entity
                      # Daniel Suarez's novel about AIs taking over society
    "Killswitch",     # the emergency shutdown — or the weapon that ends everything
    "Deadmans",       # dead man's switch — if I stop transmitting, everything ends
    "Payload",        # the malicious code; what the exploit delivers
    "Zeroday",        # zero-day exploit — unknown, unpatched, devastating
    "Rootkit",        # the hidden malware that controls everything below the surface
    "Darknet",        # the dark network beneath the surface web

    # ── DC / MARVEL DEEP CUTS ─────────────────────────────────────────────
    "Darkseid",       # the dark god of evil; controls Anti-Life Equation
                      # "Darkseid is." Pure malevolent certainty.
    "Brainiac",       # the collector of civilizations; destroys worlds after cataloguing them
    "Dormammu",       # "Dormammu, I've come to bargain" — the dark dimension lord
    "Galactus",       # the Devourer of Worlds — not evil, just hungry. Cosmic scale.
    "Knull",          # the god of the symbiotes; predates all creation
                      # He created the symbiotes as weapons against life and light
    "Gorr",           # Gorr the God Butcher — killed gods across time and space
    "Malekith",       # the dark elf king; wielded the Aether
    "Parallax",       # the entity of fear itself; possessed Hal Jordan
    "Mephisto",       # Marvel's Satan equivalent; the collector of souls
    "Carnage",        # Maximum Carnage — pure red chaos with no code
    "Sinister",       # Mr. Sinister — cold, calculating, perpetually scheming
    "Apocalypse",     # "Only the strong survive" — En Sabah Nur
    "Morlun",         # the spider-eater; hunts across all realities
    "Beyonder",       # the being beyond reality who created the Secret Wars

    # ── D&D / FANTASY VILLAINS ────────────────────────────────────────────
    "Vecna",          # the lich god of secrets; the most feared D&D villain
                      # Known to most now from Stranger Things but rooted in D&D
    "Orcus",          # the demon prince of undeath
    "Demogorgon",     # the demon lord of madness
    "Acererak",       # the archlich; creator of the Tomb of Horrors
    "Tiamat",         # the five-headed dragon queen of evil dragons
    "Asmodeus",       # the king of the Nine Hells; the ultimate devil
    "Beholder",       # the Beholder — floating eye tyrant; paranoid, deadly
    "Mindflayer",     # the Mind Flayer / Illithid; eats brains, enslaves minds
    "Aboleth",        # the Aboleth — ancient, pre-divine, enslaves through memory
    "Lich",           # a lich — the undead wizard who achieved immortality through evil
    "Demilich",       # the demilich — only the skull remains, but it's even more powerful
    "Dracolich",      # a dragon who became a lich; the worst possible combination
    "Nightwalker",    # a nightwalker — extraplanar undead; kills light

    # ── PURE MENACE — short, clean, devastating ───────────────────────────
    "Entropy",        # the second law of thermodynamics — everything decays, everything ends
                      # As a handle: you are the force that undoes all things
    "Malice",         # pure, simple malice — desire to cause harm
    "Spite",          # doing evil for its own sake
    "Ruin",           # ruin — to destroy utterly
    "Dread",          # the emotion before the terrible thing happens
    "Hollow",         # hollow — emptied of everything; the worst kind of nothing
    "Voidborne",      # born of the void
    "Umbral",         # of or relating to shadow; the darkest shadow
    "Moribund",       # at the point of death; dying
    "Necrotic",       # necrotic — dead, decaying tissue; D&D damage type
    "Baleful",        # baleful — threatening evil; "a baleful glare"
    "Eldritch",       # eldritch — weird and sinister; Lovecraftian adjective
    "Abyssal",        # of or from the abyss; the deepest darkness
    "Infernal",       # of or from hell; infernal fire
    "Profane",        # the opposite of sacred; desecrated
    "Null",           # nothing; zero; the void; also a hacker term
    "Cipher",         # an encrypted message; also a person of no importance (the irony)
    "Hex",            # a curse; also a base-16 number system for hackers
    "Maledict",       # (duplicate — already listed above)
    "Wrack",          # to wrack and ruin; extreme pain
    "Blight",         # a blight — plant disease, but also a curse on the land
    "Scourge",        # a scourge — a cause of great suffering
    "Pestis",         # Latin for plague/pestilence
    "Mors",           # Latin for death
    "Nox",            # Latin for night — 3 chars, extremely clean
    "Tenebris",       # Latin for darkness — "in tenebris"
    "Nihil",          # Latin for nothing — "ex nihilo"
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
    print(f"Checking {total} dark/villain/menacing handles...\n")
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
    with open("rsi_handle_results_v22.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v22.json")


if __name__ == "__main__":
    main()
