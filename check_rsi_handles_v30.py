#!/usr/bin/env python3
"""
RSI handle checker — batch 30.
Network error codes, DNS errors, C++ exceptions, Java NPE culture,
HTTP status codes with meaning, SSL/TLS errors, TCP attack names.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── DNS ERROR CODES — the DNS system's failure vocabulary ────────────
    # DNS errors are often more specific and less known than HTTP codes
    "NXDOMAIN",       # Non-Existent Domain — the DNS 404
                      # "You tried to look me up. I don't exist in the directory."
                      # 8 chars, clean, dark, exactly right
    "SERVFAIL",       # Server Failure — DNS lookup failed at the authority
                      # "I'm a failure to those who try to find me" — 8 chars
    "REFUSED",        # Query Refused — the server knows but won't answer
                      # not unreachable, just refusing. deliberate silence.
    "FORMERR",        # Format Error — your query was malformed
    "NOTIMP",         # Not Implemented — this query type doesn't exist here
    "NXRRSET",        # Non-Existent RR Set — the record type doesn't exist

    # ── HTTP STATUS CODES WITH IDENTITY ───────────────────────────────────
    "Http410",        # 410 Gone — resource permanently deleted
                      # not a 404 (might come back), a 410 means: gone forever
                      # "I am gone. Permanently." — the strongest statement
    "HttpGone",       # 410 Gone in words
    "Error410",       # the error itself
    "Http408",        # 408 Request Timeout — you took too long
    "Http409",        # 409 Conflict — there's a state conflict
    "Http502",        # 502 Bad Gateway — upstream server failed
    "Http503",        # 503 Service Unavailable
    "Http504",        # 504 Gateway Timeout
    "BadGateway",     # 502 in words
    "GatewayTimeout", # 504 in words
    "Http304",        # 304 Not Modified — nothing has changed
    "Http206",        # 206 Partial Content — you got part of what you wanted
    "Http101",        # 101 Switching Protocols — upgrading to WebSocket etc.
    "Http451",        # 451 Unavailable For Legal Reasons (Fahrenheit 451)

    # ── SSL / TLS ERRORS ─────────────────────────────────────────────────
    "SelfSigned",     # a self-signed certificate — not trusted by any CA
                      # what hackers, developers, and paranoid sysadmins use
                      # "I didn't ask for your permission to be legitimate"
    "CertExpired",    # the certificate has expired — trust window closed
    "HandshakeFail",  # TLS handshake failure — couldn't establish secure channel
    "CertRevoked",    # certificate revoked — explicitly distrusted
    "CertInvalid",    # invalid certificate
    "UnknownCA",      # unknown certificate authority — not in the trust store
    "BadCert",        # bad certificate
    "CipherMismatch", # the client and server can't agree on encryption
    "SslError",       # generic SSL error

    # ── TCP / NETWORK ATTACK NAMES ────────────────────────────────────────
    "SYNFlood",       # SYN flood DDoS — send thousands of SYNs, never ACK
                      # exhausts the server's connection table
    "SynFlood",       # lowercase s version
    "ARPSpoof",       # ARP spoofing — poisoning the ARP cache
                      # making yourself appear to be another machine on the network
    "ARPPoison",      # ARP poisoning — same concept
    "TTLExpired",     # TTL Exceeded — the packet ran out of hops in transit
                      # traceroute works by deliberately triggering this
                      # "I expired in transit" — beautiful as an identity
    "PortClosed",     # port is closed — RST sent back
    "HostUnreachable",# the host is unreachable
    "NetUnreachable", # the network itself is unreachable
    "PacketLoss",     # packets being dropped in transit
    "RSTPacket",      # the TCP RST — forcibly closing a connection
    "FINWait",        # the FIN_WAIT state — connection is closing
    "TimeWait",       # the TIME_WAIT state — lingering after close
    "CloseWait",      # the CLOSE_WAIT state — waiting to fully close
    "HalfOpen",       # a half-open TCP connection — the SYN was sent, no reply

    # ── C++ EXCEPTION TYPES ───────────────────────────────────────────────
    "NoExcept",       # noexcept — the C++ specifier promising no exceptions will throw
                      # "I make no exceptions." — as a personal philosophy
    "CatchAll",       # catch(...) in C++ — catching everything; nothing escapes
    "ThrowNew",       # throw new Exception() — creating and throwing
    "Unhandled",      # unhandled exception — the crash nobody prepared for
    "TryCatch",       # the try/catch block — attempting, prepared to fail
    "BadCast",        # std::bad_cast — failed dynamic_cast in C++
    "BadTypeid",      # std::bad_typeid — typeid on null pointer
    "BadWeakPtr",     # std::bad_weak_ptr — expired weak pointer
    "Rethrow",        # rethrowing a caught exception — caught but not handled
    "ExceptionPtr",   # std::exception_ptr — a pointer to a caught exception
    "Terminate",      # std::terminate() — called when exception handling fails
                      # the last resort; everything else has failed
    "Abort",          # abort() — abnormal termination; core dump; no cleanup
    "AssertFail",     # assert() failure — assumption violated; program stops

    # ── JAVA / C# NULL POINTER CULTURE ───────────────────────────────────
    "NullPtrEx",      # NullPointerException abbreviated — the most famous Java error
    "NullPointerEx",  # slightly longer
    "NullRef",        # NullReferenceException — the C# equivalent
    "NPException",    # NPE — the abbreviation every Java developer knows
    "ArrayBounds",    # ArrayIndexOutOfBoundsException — the second most common
    "ClassCast",      # ClassCastException — type mismatch at runtime
    "ConcurrentMod",  # ConcurrentModificationException — modifying while iterating
    "StackOverEx",    # StackOverflowError — infinite recursion
    "OutOfMemEx",     # OutOfMemoryError
    "IllegalState",   # IllegalStateException — the object is in a wrong state
    "UnsupOp",        # UnsupportedOperationException

    # ── PYTHON / JAVASCRIPT ERROR TYPES ──────────────────────────────────
    "TypeError",      # TypeError — the type is wrong; universal across languages
    "AttributeErr",   # AttributeError — the attribute doesn't exist
    "KeyError",       # KeyError — the key isn't in the dictionary
    "IndexError",     # IndexError — the index is out of range
    "RecursionErr",   # RecursionError — maximum recursion depth exceeded
    "ReferenceErr",   # ReferenceError — using a variable that doesn't exist
    "SyntaxErr",      # SyntaxError — the code isn't valid syntax
    "RangeErr",       # RangeError — value out of valid range
    "UncaughtEx",     # uncaught exception — nothing caught it; fatal

    # ── THE PHILOSOPHY OF ERRORS ──────────────────────────────────────────
    "GracefulFail",   # graceful failure — the ideal; fail without crashing
    "FailFast",       # fail fast — detect errors immediately and stop
    "FailSafe",       # fail-safe — when it fails, default to the safe state
    "ErrorFirst",     # error-first callback style in Node.js
    "Idempotent",     # idempotent — calling it multiple times has the same effect
    "Deterministic",  # deterministic — same input, always same output
    "NonDeterministic",# non-deterministic — random, unpredictable
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
    print(f"Checking {total} network errors / C++ / Java / DNS handles...\n")
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
    with open("rsi_handle_results_v30.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v30.json")


if __name__ == "__main__":
    main()
