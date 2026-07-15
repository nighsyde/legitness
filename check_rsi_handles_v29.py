#!/usr/bin/env python3
"""
RSI handle checker — batch 29.
Two hunts:
1. Smithed devnull variants with numbers (unique strings RSI treats differently)
2. Developer error codes — Unix errno, HTTP status, magic hex, exception names
   that every developer has burned into their memory.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── SMITHED DEVNULL — leet versions that become unique strings ────────
    # RSI is case-insensitive on letters, but numbers make it unique
    "d3vnull",        # dev with leet 3 for e
    "devnu11",        # devnull with leet 11 for ll
    "devnul1",        # devnul with leet 1 for final l
    "d3vnu11",        # fully leet: d3vnu11
    "d3vnul1",        # partial leet
    "devnu1l",        # leet 1 for i/l
    "d3vNu11",        # mixed case leet
    "devnull0",       # devnull with 0 suffix
    "devnull1",       # devnull with 1 suffix (sequel)
    "devnull2",       # devnull2
    "DevNull2",       # devnull sequel
    "devnullx",       # devnull with x suffix
    "devnullv2",      # version 2

    # ── UNIX ERRNO VALUES — what you read when a syscall fails ────────────
    # Every C/Linux programmer knows these by heart.
    # They're not just error codes — they're identities.
    "EPERM",          # errno 1 — Operation not permitted. The first error.
    "ENOENT",         # errno 2 — No such file or directory
    "ESRCH",          # errno 3 — No such process
    "EINTR",          # errno 4 — Interrupted system call
    "EBADF",          # errno 9 — Bad file descriptor
    "EAGAIN",         # errno 11 — Try again / Resource temporarily unavailable
                      # the most common errno in non-blocking I/O
                      # "try again later" as an identity — patient, inevitable
    "ENOMEM",         # errno 12 — Out of memory
                      # when the kernel can't give you what you asked for
    "EACCES",         # errno 13 — Permission denied
                      # the wall. you hit it constantly.
    "EFAULT",         # errno 14 — Bad address
                      # your pointer is wrong. you're pointing at nothing valid.
    "EBUSY",          # errno 16 — Device or resource busy
                      # it's occupied. try again.
    "EEXIST",         # errno 17 — File exists (when it shouldn't)
    "ENODEV",         # errno 19 — No such device
    "EINVAL",         # errno 22 — Invalid argument
                      # what you gave me doesn't make sense
    "ENOSPC",         # errno 28 — No space left on device
    "EPIPE",          # errno 32 — Broken pipe
                      # the reader closed. you're writing into nothing.
    "ERANGE",         # errno 34 — Result too large (out of range)
    "ENOSYS",         # errno 38 — Function not implemented
                      # this doesn't exist here. great as a handle.
    "ENOTDIR",        # errno 20 — Not a directory
    "EISDIR",         # errno 21 — Is a directory (when you expected a file)
    "ECONNREFUSED",   # errno 111 — Connection refused. The door is closed.
    "ETIMEDOUT",      # errno 110 — Connection timed out
    "ECONNRESET",     # errno 104 — Connection reset by peer
    "ENETUNREACH",    # Network unreachable
    "EHOSTUNREACH",   # Host unreachable

    # ── HTTP STATUS CODES WITH MEANING ───────────────────────────────────
    "Http418",        # 418 I'm a teapot — RFC 2324; the joke RFC
                      # "Any attempt to brew coffee with a teapot should
                      # result in the error code 418 I'm a teapot"
                      # as a handle: I'm not what you expected
    "Teapot418",      # same reference with the status
    "ImaTeapot",      # "I'm a teapot" — the response body
    "Http404",        # 404 Not Found — as a handle
    "Error500",       # 500 Internal Server Error
    "Error403",       # 403 Forbidden
    "Error401",       # 401 Unauthorized
    "Error429",       # 429 Too Many Requests — being rate limited
    "Http451",        # 451 Unavailable For Legal Reasons — censored
                      # named after Fahrenheit 451; the book burning temperature
    "Http301",        # 301 Moved Permanently — redirected forever

    # ── MAGIC HEX CONSTANTS — the fingerprints developers leave behind ───
    # These are baked into compilers, file formats, debuggers.
    # Every developer who stared at a hex dump knows them.
    "DEADBEEF",       # 0xDEADBEEF — the classic debug fill pattern
                      # used to mark uninitialized memory; if you see this, it's a bug
                      # legendary in the C programming world
    "CAFEBABE",       # 0xCAFEBABE — Java .class file magic bytes
                      # every Java class file starts with these 4 bytes
    "CAFEF00D",       # 0xCAFEF00D — cafe food; used in some Android/ARM magic
    "BADF00D",        # 0xBADF00D — bad food; ARM memory fill
    "DEADC0DE",       # 0xDEADC0DE — dead code; used as debug marker
    "C0FFEE",         # 0xC0FFEE — coffee; IBM RS/6000 used this as boot ID
    "FEEDFACE",       # 0xFEEDFACE — Mach-O (macOS/iOS) binary magic bytes
    "BAADF00D",       # 0xBAADF00D — "bad food"; Windows HeapAlloc debug fill
    "D00DFEED",       # 0xD00DFEED — Core Data (Apple) file format magic
    "ABAD1DEA",       # 0xABAD1DEA — "a bad idea" — common debug marker

    # ── EXCEPTION AND ERROR NAMES ─────────────────────────────────────────
    "NullPtr",        # null pointer exception — the most common programming error
    "BadAlloc",       # std::bad_alloc — C++ out of memory exception
    "SegFault",       # (taken) — but try variants:
    "SegViolation",   # segmentation violation — the full name
    "AccessViolation",# the Windows equivalent of segfault
    "DivByZero",      # division by zero — the classic mathematical impossibility
    "StackOverflow",  # the recursive stack overflow — and the website
    "HeapCorrupt",    # heap corruption — memory has been corrupted
    "UseAfterFree",   # use-after-free vulnerability — freed memory accessed again
    "DoubleFree",     # already confirmed available
    "BufferOverrun",  # buffer overrun — writing past the end
    "IntOverflow",    # integer overflow — the number wrapped around
    "Undefined",      # undefined behavior in C/C++ — anything can happen
    "UndefinedBeh",   # UB — undefined behavior abbreviated
    "NotANumber",     # NaN — Not a Number
    "FloatNaN",       # float NaN value
    "InfinityErr",    # float infinity error
    "OutOfBounds",    # array out of bounds

    # ── THE DEVELOPER EXPERIENCE ──────────────────────────────────────────
    "ItWorks",        # "it works on my machine"
    "WorksOnMyMachine",# the full phrase
    "OnMyMachine",    # shortened
    "DidntTest",      # I didn't test this
    "ShipIt",         # "ship it" — push to production
    "PushToMain",     # the dangerous git command
    "BreakingChange", # a breaking change
    "TechDebt",       # technical debt — the accumulated shortcuts
    "TodoFix",        # TODO: fix this later
    "Revert",         # git revert — undoing a broken commit
]

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
    print(f"Checking {total} devnull variants + developer error codes...\n")
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
    with open("rsi_handle_results_v29.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v29.json")


if __name__ == "__main__":
    main()
