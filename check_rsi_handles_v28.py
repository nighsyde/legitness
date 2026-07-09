#!/usr/bin/env python3
"""
RSI handle checker — batch 28.
The /dev/null universe: same concept, different forms.
Real /dev/ paths, old programmer slang, network null concepts,
and original 'dev' constructions with that same void/disappear energy.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── REAL /dev/ PATHS — each one is a file that represents something ──
    "DevMem",         # /dev/mem — raw physical memory; read/write actual RAM
                      # the most dangerous /dev/ entry; root only; exposed the whole machine
    "DevFull",        # /dev/full — writes always fail: "no space left on device"
                      # the anti-null; null accepts everything, full rejects everything
    "DevUrandom",     # /dev/urandom — unblocked entropy; fast, cryptographically usable
                      # "true randomness from the kernel" — every crypto app uses this
    "DevTun",         # /dev/net/tun — the TUN/TAP virtual network interface
                      # where VPNs and Tor live at the kernel level
    "DevShm",         # /dev/shm — shared memory filesystem; RAM-backed, gone on reboot
                      # multiple processes share this space; ephemeral by design
    "DevKmem",        # /dev/kmem — kernel memory; even more sensitive than /dev/mem
                      # reading this exposes the running kernel's address space
    "DevLoop",        # /dev/loop — loop devices; mount a file as a filesystem
                      # infinite loop, by design; also mounting ISO images
    "DevPtmx",        # /dev/ptmx — pseudo-terminal master; the controlling side
    "DevPts",         # /dev/pts — pseudo-terminal slave; your terminal window
    "DevStdin",       # /dev/stdin — standard input as a file descriptor
    "DevStdout",      # /dev/stdout — standard output as a file descriptor
    "DevStderr",      # /dev/stderr — standard error as a file descriptor
    "DevFd",          # /dev/fd — file descriptors as a directory
    "DevHda",         # /dev/hda — first IDE hard disk; the old naming before /dev/sda
    "DevSda",         # /dev/sda — first SCSI/SATA disk; the drive itself
    "DevSdb",         # /dev/sdb — second disk; often where you mount USB drives

    # ── THE ORIGINAL PROGRAMMER SLANG FOR /dev/null ──────────────────────
    "BitBucket",      # the "bit bucket" — where discarded bits go
                      # pre-Unix programmer slang; older than /dev/null itself
                      # "send it to the bit bucket" = throw it away
                      # the concept predates Linux; a ghost in the machine
    "NullSink",       # the null sink; absorbs all output
    "DataSink",       # where data goes to die
    "ErrorSink",      # where errors go (2>/dev/null)
    "OutputSink",     # the output sink
    "Discard",        # the discard protocol (TCP/UDP port 9)
                      # literally called "discard" — whatever you send is discarded
                      # /dev/null for the network stack

    # ── NETWORKING NULL CONCEPTS ──────────────────────────────────────────
    "NullRoute",      # a null route — packets silently dropped, never delivered
                      # ip route add blackhole X.X.X.X — traffic to that IP vanishes
    "Blackhole",      # black hole routing; traffic enters, nothing comes out
    "Sinkhole",       # DNS sinkhole — redirecting malicious domains to nothing
                      # security teams use these to kill botnets
    "Tarpit",         # a tarpit — deliberately slow responses to waste attacker time
                      # the honeypot's cousin; slows scanners down to nothing
    "Honeypot",       # a honeypot — a fake system designed to attract attackers
    "Darkspace",      # dark address space — IP addresses that should have no traffic
                      # monitoring these catches attackers scanning randomly
    "NullByte",       # the null byte — byte value 0x00; terminates C strings
                      # injecting a null byte can truncate filenames and bypass checks
    "NullChar",       # the null character — same thing, different name
    "NullTerm",       # null-terminated string — the C string convention
    "NullPtr",        # null pointer — the pointer that points to nothing
                      # dereferencing this causes a segfault (null dereference)

    # ── ORIGINAL 'dev' CONSTRUCTIONS — same energy as devnull ────────────
    "DevVoid",        # the void with a dev path; /dev/void — doesn't exist, feels right
    "DevGhost",       # a ghost device; it shows up in /dev but connects to nothing
    "DevBleed",       # bleeding edge dev; also a security vulnerability aesthetic
    "DevMode",        # developer mode; hidden capabilities; unlocked device
    "DevBox",         # a dev box/VM; the throwaway environment where anything goes
    "DevDrop",        # drop to dev; development access granted
    "DevSilent",      # a silent device; produces no output; swallows everything
    "DevHole",        # a hole in the dev tree; drops through to nowhere
    "DevSink",        # the development sink; absorbs all input
    "DevDead",        # a dead device; present but not connected to anything
    "DevPhantom",     # a phantom device; shows in the tree but doesn't exist
    "DevRoute",       # the development route; where dev traffic goes
    "DevFlux",        # in flux; the development state of constant change
    "DevStray",       # a stray device; unclaimed, unowned
    "DevCold",        # a cold device; offline but present
    "DevDark",        # a dark device; no activity, no light, no signal
    "DevLost",        # a lost device; in the tree but unreachable
    "DevMute",        # a mute device; receives but never transmits
    "DevBlank",       # a blank device; formatted but empty

    # ── THE /dev/null PHILOSOPHY AS IDENTITY ──────────────────────────────
    # What /dev/null represents as a personal philosophy:
    # I exist. I take input. I give nothing back. I leave no trace.
    "SendToNull",     # the command itself; the act of erasing
    "PipeToNull",     # piping to null; the redirection
    "RedirectNull",   # redirecting to null
    "OutputNull",     # output goes to null
    "NullOutput",     # the null output; nothing returned
    "NullInput",      # null input; nothing given
    "NullReturn",     # function returns null; nothing comes back
    "VoidReturn",     # void return; the function signature that promises nothing
    "NullResult",     # the result is null; no value
    "EmptyReturn",    # empty return; nothing
    "NullReply",      # null reply; no response
    "NoReply",        # no reply; silence
    "Unresponsive",   # not responding; present but silent
    "Unreachable",    # unreachable; the host is there but answers nothing
    "Devnul",         # /dev/nul — the Windows equivalent of /dev/null
                      # Windows uses 'nul' instead of 'null' — subtle difference
    "DevNul",         # same, capitalized
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
    print(f"Checking {total} /dev/null universe handles...\n")
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
    with open("rsi_handle_results_v28.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v28.json")


if __name__ == "__main__":
    main()
