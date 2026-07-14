# Restore in One Page

*Keep this current. If you cannot restore must-keep services from this page plus backups, the lab is folklore — shrink until this page is true.*

**Last updated:** _______________  
**Updated during stewardship on:** _______________

---

## Purpose (one sentence)

_________________________________________________________________________

---

## What runs (powered Keep)

| Host | Job (one breath) | IP / name | 24/7? | Location (U / shelf) |
|------|------------------|-----------|-------|----------------------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

**On-demand only (off when idle):**

| Host | Job | How to start / stop |
|------|-----|---------------------|
| | | |
| | | |

---

## Services map

| Service | URL / port | Runs on | Depends on | Who notices if down |
|---------|------------|---------|------------|---------------------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

---

## Network (boring)

| Item | Value |
|------|-------|
| Upstream router / WAN | |
| Rack switch | |
| VLANs (if any) | |
| DNS | |
| VPN (if any) | |
| Critical switch ports | |

---

## Storage & backups

| Dataset / share | Host | What it holds (charter class) | Backup target | Last verified restore |
|-----------------|------|-------------------------------|---------------|------------------------|
| | | | | |
| | | | | |
| | | | | |

**Backup rule in one line:** _______________________________________________

**Curated ISO / mirror path:** _______________________________________________  
**Allowlist lives in:** `01-lab-charter.md`

---

## Credentials & secrets

Do **not** put passwords on this page if it is taped to a door.

| Secret type | Where stored (password manager / sealed envelope / etc.) |
|-------------|----------------------------------------------------------|
| Host root / admin | |
| Service admins | |
| Backup encryption keys | |
| UPS / BMC / IPMI | |

---

## Cold start (power restored)

Order to bring the household up:

1. _______________________________________________________________________
2. _______________________________________________________________________
3. _______________________________________________________________________
4. _______________________________________________________________________
5. Verify: _______________________________________________________________

**UPS:** covers _______________ for ~_____ minutes. After that, graceful stop: _______________

---

## Rebuild a Keep host (skeleton)

| Step | Action |
|------|--------|
| 1 | Install media from curated mirror: _______________ |
| 2 | Config / infra-as-code / notes at: _______________ |
| 3 | Restore data from: _______________ |
| 4 | Re-join network / certs / DNS: _______________ |
| 5 | Smoke test: _______________ |

---

## Family contacts

| Role | Name | When to call |
|------|------|--------------|
| Steward | | |
| Household veto / partner | | |
| Someone who can power-cycle if you are away | | |

---

## Charter pointers

- Missions & caps: [`01-lab-charter.md`](01-lab-charter.md)  
- Ritual: [`06-stewardship-ritual.md`](06-stewardship-ritual.md)  
- Exit rules: [`05-gear-exit.md`](05-gear-exit.md)  

---

## Creed

> Keep the craft. Release the museum.  
> Empty U is a win.  
> The stack fits the life.
