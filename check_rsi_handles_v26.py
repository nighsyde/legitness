#!/usr/bin/env python3
"""
RSI handle checker — batch 26.
ORIGINAL handles constructed from:
- Linux primitives and concepts
- Hacker/exploit terminology
- Dark web culture
- Script kiddie era slang
- Real worm/malware names from 2001-2004 that every sysadmin/hacker remembers
Alphanumeric only, 3+ chars.
"""

import time
import requests
import json
import re
from datetime import datetime

NAMES = [
    # ── LINUX PRIMITIVES AS IDENTITY ─────────────────────────────────────
    "Sudoer",         # one who has sudo privileges — earned or escalated to
                      # in early 2000s Linux, having sudo was an indicator you mattered
    "ForkBomb",       # :(){ :|:& };: — the bash command that recursively forks
                      # crashes the system by exhausting process table entries
                      # every Linux nerd ran it once, always on someone else's machine
    "DevNull",        # /dev/null — the void that swallows all output
                      # "send it to /dev/null" — erase it completely
    "DevZero",        # /dev/zero — infinite source of null bytes; used to wipe disks
    "DevRandom",      # /dev/random — entropy from the kernel; true randomness
    "ProcSelf",       # /proc/self — your own process's information
                      # self-referential; introspective; the file system of identity
    "EtcPasswd",      # /etc/passwd — the file everyone tried to read
    "EtcShadow",      # /etc/shadow — the hashed passwords; the real target
    "Orphaned",       # an orphan process — its parent died; now runs under init
                      # a process with no parent; floating, uncollected
    "ZombieProc",     # a zombie process — dead but not yet reaped by the parent
                      # shows up in ps output as Z; haunts the system
    "SuidRoot",       # SUID root binary — executes as root regardless of who runs it
                      # the single most dangerous permission combination
    "Chmod777",       # chmod 777 — world-readable, world-writable, world-executable
                      # the first mistake; the insecure permission every admin warned about
    "Chmod000",       # chmod 000 — no permissions for anyone; locked out of existence
    "Ptrace",         # ptrace() — the syscall for process tracing
                      # used by debuggers AND by exploits to inject code
    "Strace",         # strace — traces every system call a program makes
                      # the all-seeing tool; reveals what a binary really does
    "Ltrace",         # ltrace — traces library calls; one level up from strace
    "Objdump",        # objdump — disassembles object files; reverse engineering start
    "ShellDrop",      # dropping a shell — the moment you get command execution
                      # "I got a shell drop on that box" — the phrase of that era
    "PrivEsc",        # privilege escalation — going from user to root
                      # the art of finding the gap between what you are and what you need
    "CoreDump",       # a core dump — a dead process writes its entire memory to disk
                      # forensic gold; contains stack, heap, everything
    "KernelOops",     # a kernel oops — the non-fatal kernel error message
                      # Linux says "oops" when it messes up but doesn't die
    "KernelPanic",    # the fatal one — "kernel panic: not syncing"
                      # the Linux equivalent of the Blue Screen of Death
    "NullDeref",      # null pointer dereference — following a null pointer
                      # the most common crash; sometimes weaponizable
    "OffByOne",       # the off-by-one error — the fence-post mistake
                      # the elegant vulnerability hiding in an array bound
    "DoubleFree",     # freeing the same memory allocation twice
                      # classic heap corruption; leads to code execution
    "UserLand",       # userland — the user space as opposed to kernel space
                      # "this runs in userland" — unprivileged; sandboxed
    "RingZero",       # Ring 0 — kernel privilege level; the most privileged mode
                      # Ring 3 is user space; Ring 0 is where the OS lives
    "RingThree",      # Ring 3 — where user applications run; limited access
    "Shellspawn",     # spawning a shell — the goal of most exploits
    "BindShell",      # a bind shell — listening for connections; reverse of reverse shell
    "RevShell",       # reverse shell — connecting back to attacker's machine

    # ── WORMS AND MALWARE — real names from 2001-2004 ────────────────────
    # Every sysadmin and hacker of that era has these burned in their memory.
    "Nimda",          # Nimda — "admin" spelled backward; the 2001 worm
                      # spread via email, web, network shares simultaneously
                      # went from zero to internet-wide saturation in 22 minutes
    "Slammer",        # SQL Slammer — January 2003; fastest-spreading malware ever
                      # doubled in size every 8.5 seconds; took down South Korea's internet
                      # the entire payload was 376 bytes — fit in a single UDP packet
    "Blaster",        # Blaster worm — August 2003; contained the message:
                      # "billy gates why do you make this possible? Stop making money"
                      # launched a DDoS against windowsupdate.com
    "CodeRed",        # Code Red — July 2001; infected 359,000 machines in 14 hours
                      # defaced web pages with "HELLO! Welcome to http://www.worm.com!"
    "Sasser",         # Sasser — April 2004; spread through Windows LSASS vulnerability
                      # caused systems to crash and reboot; took down Delta Airlines
    "Sobig",          # Sobig.F — August 2003; fastest-spreading email worm of its time
    "Mydoom",         # MyDoom — January 2004; fastest email worm ever at the time
    "Santy",          # Santy — December 2004; used Google to find targets to deface
    "Welchia",        # Welchia — the "good" worm that tried to patch Blaster victims

    # ── DARK WEB / TOR CULTURE ───────────────────────────────────────────
    "OnionSkin",      # the layers of Tor encryption; peeling the onion
    "ExitNode",       # where anonymized traffic re-enters the regular internet
    "Clearnet",       # what dark web users call the normal internet
    "HiddenSvc",      # Tor hidden service — reachable only through Tor
    "CircuitHop",     # hopping through Tor circuits to obscure origin
    "GuardNode",      # the entry guard node in Tor; first hop
    "Rendezvous",     # the rendezvous point in Tor's hidden service protocol
    "Onioned",        # wrapped in onion routing; anonymized

    # ── SCRIPT KIDDIE SLANG (the culture, worn with irony) ────────────────
    "Nimda",          # (duplicate — will be filtered)
    "Crackme",        # a crackme — a program designed to be cracked; the challenge
    "KeyGenMe",       # a keygenme — write a key generator for this program
    "PatchMe",        # a patchme — patch this binary to bypass the check
    "Trainerhack",    # a game trainer — memory editing tool for cheating
    "GameTrainer",    # the game trainer
    "Debugme",        # debug this; reverse engineer this
    "NoCD",           # no-CD crack — removing the disc check
    "Keygen",         # key generator — the piracy tool
    "NFOscene",       # the NFO file scene — the warez scene's identity documents
    "Topsite",        # (already confirmed available)

    # ── CONSTRUCTED ORIGINALS: Linux + dark ──────────────────────────────
    "Rootjail",       # jailed root — chroot jail; locked in a directory as root
    "ChrootEsc",      # escaping a chroot jail — the more advanced technique
    "PidKill",        # killing by PID — the administrative act that ends a process
    "KillSignal",     # sending a KILL signal — SIGKILL; can't be caught or ignored
    "SigKill",        # SIGKILL itself — the unblockable kill
    "SigTerm",        # SIGTERM — the polite kill; can be caught and handled
    "SigZero",        # signal 0 — exists; used to check if a process exists
    "Dmesg",          # dmesg — the kernel ring buffer; messages from the system itself
    "Syslog",         # syslog — the system log; where everything is recorded
    "Authlog",        # /var/log/auth.log — authentication log; the break-in record
    "Wtmpfix",        # wtmp — login records; fixwtmp — the tool to clean them
    "Lastlog",        # last log — record of recent logins; first thing cleaned after root
    "ClearLog",       # clearing the logs — post-exploitation first step
    "Cronjob",        # cron job — a scheduled task; used for persistence
    "Crontab",        # crontab — the cron table; where persistence lives
    "Bashhistory",    # .bash_history — the command history file hackers delete first
    "Histkill",       # killing the history — `unset HISTFILE` or `history -c`
    "Netstat",        # netstat — showing network connections; the detection tool
    "Lsof",           # lsof — list open files; see what a process is doing
    "Nohup",          # nohup — no hangup; keep running after logout
    "Disown",         # disown — detach a process from the shell; another persistence trick
    "Tmuxsplit",      # tmux split — the tool every sysadmin and hacker used
    "Screenrc",       # .screenrc — the GNU screen config; old school multiplexer
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
    print(f"Checking {total} Linux/hacker/darkweb original handles...\n")
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
    with open("rsi_handle_results_v26.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to rsi_handle_results_v26.json")


if __name__ == "__main__":
    main()
