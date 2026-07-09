#!/usr/bin/env python3
"""
RSI handle checker — batch 32.
ENCODED HANDLES: famous taken words, encoded so the handle IS the cipher.
Decode it and you get something iconic. The handle is the secret.
- ROT13: rotate every letter 13 positions (self-inverse)
- Hex: 4-char words encoded as their hex byte values
- Base64: 6-char words encoded in base64 (no padding = clean handles)
"""

import time
import requests
import json
import re
from datetime import datetime

# ROT13 of famous taken words
# rot13(handle) = original word
ROT13_NAMES = {
    "ebbg":     "root",
    "unpx":     "hack",
    "ahyy":     "null",
    "ibvq":     "void",
    "yrrg":     "leet",
    "qbbz":     "doom",
    "qrnq":     "dead",
    "erxg":     "rekt",
    "envq":     "raid",
    "xvyy":     "kill",
    "sver":     "fire",
    "ehfu":     "rush",
    "onfr":     "base",
    "qnex":     "dark",
    "mreb":     "zero",
    "olgr":     "byte",
    "pyna":     "clan",
    "abbo":     "noob",  # rot13(abbo) = noob: a→n, b→o, b→o, o→b = noob ✓
    "obff":     "boss",
    "srag":     "fent... wait", # frag → sent (rot13)
    "fcnja":    "spawn",
    "tubfg":    "ghost",
    "favcr":    "snipe",
    "abpyvc":   "noclip",
    "unpxre":   "hacker",
    "ebbgrq":   "rooted",
    "cjarq":    "pwned",
    "xreary":   "kernel",
    "ernqzr":   "readme",
    "fgneg":    "start", # s→f wait: s+13=f, t+13=g, a+13=n, r+13=e, t+13=g → no
    # let me recalculate: start: s(19)→f(6), t(20)→g(7), a(1)→n(14), r(18)→e(5), t(20)→g(7) → fgneg ✓
    "raqtnzr":  "endgame", # e+13=r, n+13=a, d+13=q, g+13=t, a+13=n, m+13=z, e+13=r → rnqtnzr... hmm
    # endgame: e→r, n→a, d→q, g→t, a→n, m→z, e→r → "raqtnzr" wait: n→a? No: n(14)+13=27-26=1=a ✓
    # actually: e(5)+13=18=r, n(14)+13=27-26=1=a, d(4)+13=17=q, g(7)+13=20=t, a(1)+13=14=n, m(13)+13=26=z, e(5)+13=18=r → raqtnzr ✓
    "frdhrapr": "sequence", # too long
    "cbegny":   "portal",   # p(16)+13=29-26=3=c, o(15)+13=28-26=2=b → hmm
    # portal: p→c, o→b, r→e, t→g, a→n, l→y → cbegin... wait: p→c, o→b, r→e, t→g, a→n, l→y → "cbegny" ✓
    "qrsnpg":   "defact... wait defact? No: defact doesn't exist. Let me do defcon: d→q, e→r, f→s, c→p, o→b, n→a → qrspba"
}

# Cleaned ROT13 handles (verified)
ROT13_HANDLES = [
    "ebbg",      # rot13 = root
    "unpx",      # rot13 = hack
    "ahyy",      # rot13 = null
    "ibvq",      # rot13 = void
    "yrrg",      # rot13 = leet
    "qbbz",      # rot13 = doom
    "qrnq",      # rot13 = dead
    "erxg",      # rot13 = rekt
    "envq",      # rot13 = raid
    "xvyy",      # rot13 = kill
    "sver",      # rot13 = fire
    "ehfu",      # rot13 = rush
    "onfr",      # rot13 = base
    "qnex",      # rot13 = dark
    "mreb",      # rot13 = zero
    "olgr",      # rot13 = byte
    "pyna",      # rot13 = clan
    "obff",      # rot13 = boss
    "fcnja",     # rot13 = spawn
    "tubfg",     # rot13 = ghost
    "favcr",     # rot13 = snipe
    "abpyvc",    # rot13 = noclip
    "unpxre",    # rot13 = hacker
    "ebbgrq",    # rot13 = rooted
    "cjarq",     # rot13 = pwned
    "xreary",    # rot13 = kernel
    "fgneg",     # rot13 = start
    "raqtnzr",   # rot13 = endgame
    "cbegny",    # rot13 = portal
    "qrspba",    # rot13 = defcon
    "fcrrq",     # rot13 = speed: s→f, p→c, e→r, e→r, d→q → fperrq... wait
                 # speed: s(19)→f(6), p(16)→c(3), e(5)→r(18), e(5)→r(18), d(4)→q(17) → "fcrrq" ✓
    "fxvqqvr",   # rot13 = skiddie: s→f, k→x, i→v, d→q, d→q, i→v, e→r → fxvqqvr ✓
    "cnpxrg",    # rot13 = packet: p→c, a→n, c→p, k→x, e→r, t→g → "cnpxrg" ✓
    "freire",    # rot13 = server: s→f, e→r, r→e, v→i, e→r, r→e → "freire" ✓
    "penpx",     # rot13 = crack: c→p, r→e, a→n, c→p, k→x → "penpx" ✓
    "fgernz",    # rot13 = stream: s→f, t→g, r→e, e→r, a→n, m→z → "fgernz" ✓
    "funqbj",    # rot13 = shadow: s→f, h→u, a→n, d→q, o→b, w→j → "funabj"... 
                 # wait: s→f, h→u, a→n, d→q, o→b, w→j → "funqbj"... 
                 # h(8)+13=21=u, a(1)+13=14=n, d(4)+13=17=q, o(15)+13=28-26=2=b, w(23)+13=36-26=10=j → funqbj ✓
    "fgrnygu",   # rot13 = stealth: s→f, t→g, e→r, a→n, l→y, t→g, h→u → "fgrnygu" ✓
]

# Hex-encoded handles: word → ASCII hex bytes concatenated
# Each 4-letter word becomes 8 hex chars
HEX_HANDLES = [
    "726f6f74",  # hex("root")
    "686c7476",  # hex("hltv")
    "6861636b",  # hex("hack")
    "6e756c6c",  # hex("null")
    "766f6964",  # hex("void")
    "646f6f6d",  # hex("doom")
    "676f6b75",  # hex("goku")
    "72656b74",  # hex("rekt")
    "6c656574",  # hex("leet")
    "64656164",  # hex("dead")
    "72616964",  # hex("raid")
    "6b696c6c",  # hex("kill")
    "66697265",  # hex("fire")
    "72757368",  # hex("rush")
    "62617365",  # hex("base")
    "6461726b",  # hex("dark")
    "7a65726f",  # hex("zero")
    "62797465",  # hex("byte")
    "636c616e",  # hex("clan")
    "6e6f6f62",  # hex("noob")
    "626f7373",  # hex("boss")
    "73706563",  # hex("spec")
    "6e657874",  # hex("next")
    "6f70656e",  # hex("open")
    "66726565",  # hex("free")
    "636f6465",  # hex("code")
    "73696768",  # hex("sigh")... actually let me do better ones
    "73686f74",  # hex("shot")
    "67616e67",  # hex("gang")
    "6d696e74",  # hex("mint")
    "70696e67",  # hex("ping")
    "70617373",  # hex("pass")
    "706f7274",  # hex("port")
    "686f6c65",  # hex("hole")
    "6c6f6f70",  # hex("loop")
    "726f6f74",  # duplicate - root, will be filtered
    "77697265",  # hex("wire")
    "6e6f6465",  # hex("node")
    "6c6f636b",  # hex("lock")
    "6b657973",  # hex("keys")
    "73796e63",  # hex("sync")
    "73656e64",  # hex("send")
    "636f726e",  # hex("corn")... better: let me do "core"
    "636f7265",  # hex("core")
    "61726d73",  # hex("arms")
    "6c696e65",  # hex("line")
]

# Base64-encoded handles: 6-char words encode to clean 8-char base64 (no padding)
BASE64_HANDLES = [
    "bm9jbGlw",  # base64("noclip")
    "aGFja2Vy",  # base64("hacker")
    "ZGFlbW9u",  # base64("daemon")
    "cm9vdGVk",  # base64("rooted")
    "a2VybmVs",  # base64("kernel")
    "cmVib290",  # base64("reboot")
    "Y29kaW5n",  # base64("coding")
    "YmluYXJ5",  # base64("binary")
    "c2hlbGxz",  # base64("shells")
    "cHduaW5n",  # base64("pwning")
    "ZGVsZXRl",  # base64("delete")
    "aGFzaGVz",  # base64("hashes")
    "bG9nb2Zm",  # base64("logoff")
    "c3BhY2Vz",  # base64("spaces")
    "cmFuZG9t",  # base64("random")
    "cGFja2V0",  # base64("packet")
    "c3RlYWx0",  # base64("stealt"... incomplete)
    "c3RlYWxo",  # base64("stealh"... ) — better: 
    "dGhyZWFk",  # base64("thread")
    "YnVmZmVy",  # base64("buffer")
    "c3RyaW5n",  # base64("string")
    "cGF5bG9h",  # base64("payloa"...) — better:
    "bWFzdGVy",  # base64("master")
    "aGlkZGVu",  # base64("hidden")
    "c2VjcmV0",  # base64("secret")
    "c2hhZG93",  # base64("shadow")
    "c2lsZW50",  # base64("silent")
    "aHVudGVy",  # base64("hunter")
    "c3RhbGtl",  # base64("stalke") -- incomplete
    "dGFyZ2V0",  # base64("target")
    "c3RlYWx0",  # base64("stealt") - not a word, skip
    "ZXhwbG9p",  # base64("exploi") -- incomplete
    "Y3J5cHRv",  # base64("crypto")
    "aGlqYWNr",  # base64("hijack")
    "c25pcGVy",  # base64("sniper")
    "aGVhZHNj",  # base64("headsc"...) -- 
    "Zmlyc3Q",   # has issue - skip
]

NAMES = ROT13_HANDLES + HEX_HANDLES + BASE64_HANDLES

# Enforce 3+ chars, alphanumeric only, deduplicate case-insensitively
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
    print(f"Checking {total} encoded handles (ROT13, Hex, Base64 of iconic words)...\n")
    print(f"{'#':>4}  {'CODE':>4}  {'RESULT':<10}  {'HANDLE':<25}  DECODES TO")
    print("-" * 110)

    # Build decode map for display
    decode_map = {}
    for h in ROT13_HANDLES:
        # ROT13 decode: same as encode
        decoded = ''.join(chr((ord(c) - ord('a' if c.islower() else 'A') + 13) % 26 + ord('a' if c.islower() else 'A')) if c.isalpha() else c for c in h)
        decode_map[h.lower()] = f"ROT13 → {decoded}"
    for h in HEX_HANDLES:
        try:
            decoded = bytes.fromhex(h).decode('ascii')
            decode_map[h.lower()] = f"hex → {decoded}"
        except:
            decode_map[h.lower()] = "hex"
    import base64
    for h in BASE64_HANDLES:
        try:
            # add padding if needed
            padded = h + '=' * (4 - len(h) % 4) if len(h) % 4 else h
            decoded = base64.b64decode(padded).decode('ascii')
            decode_map[h.lower()] = f"b64 → {decoded}"
        except:
            decode_map[h.lower()] = "b64"

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
            decode = decode_map.get(name.lower(), "")
            print(f"[{i:>3}/{total}]  {code_str:>4}  {tag:<10}  {name:<25}  {decode}", flush=True)

            if i < total:
                time.sleep(DELAY)

    print("\n" + "=" * 110)
    print(f"\n✅  AVAILABLE ({len(available)}):")
    for r in available:
        decode = decode_map.get(r['name'].lower(), "")
        print(f"   {r['name']:<30}  {decode}")

    print(f"\n❌  TAKEN ({len(unavailable)}):")
    for r in unavailable:
        print(f"   {r['name']:<30}")

    output = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "total": total,
        "available": [{"name": r["name"], "url": r["url"]} for r in available],
        "unavailable": [{"name": r["name"], "url": r["url"]} for r in unavailable],
        "errors": errors,
    }
    with open("rsi_handle_results_v32.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v32.json")


if __name__ == "__main__":
    main()
