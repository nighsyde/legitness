# Minimal Stack — Collapse Compute & ISO Archive

*Days 15–45. Aim: one quiet primary (or small cluster), one storage node sized to policy, boring labeled network, zero floor sprawl. Empty U is success.*

**Cut start date:** _______________  
**Target end (≤ day 45):** _______________

---

## Target topology

```text
[ WAN / home router ]
         |
[ rack switch — labeled, boring ]
         |
    +----+----+
    |         |
[ primary ] [ storage — policy-sized ]
    |
[ optional on-demand craft/play host — OFF when idle ]
```

| Role | Keep criteria | Default |
|------|---------------|---------|
| Primary compute | Runs Keep services from audit | One box or tight HA pair only if household utility demands it |
| Storage | Holds must-keep + curated mirror + working media within charter TB target | One node; no second array “for growth” without charter revision |
| Network | Connectivity + maybe DNS/VPN | Lowest complexity that works |
| On-demand host | Named craft/play job in charter | Powers off; not 24/7 identity |
| Everything else | — | Power off → migrate → Exit |

---

## A. Collapse powered footprint

### 1. Freeze the Keep list

Copy Keep services/hosts from [`02-inventory-audit.md`](02-inventory-audit.md). Nothing else stays powered 24/7.

| Keep service | Moves to (primary / storage / other) | Done? |
|--------------|--------------------------------------|-------|
| | | [ ] |
| | | [ ] |
| | | [ ] |
| | | [ ] |
| | | [ ] |

### 2. Migration order (safe default)

1. Document current access (IPs, URLs, credentials location) on [`07-restore-one-page.md`](07-restore-one-page.md) *before* moves.
2. Back up configs and must-keep data.
3. Stand up / confirm primary + storage.
4. Move one service at a time; verify; only then retire the old host.
5. Power off emptied hosts for 7 days (soak). If nothing breaks → Exit path.

### 3. Power-off ledger

| Host | Powered off | Soak until | Outcome (Keep off / Exit) | Notes |
|------|-------------|------------|---------------------------|-------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

### 4. Post-collapse powered inventory

| Hostname | Job (one breath) | 24/7 or on-demand | Watts idle (approx) |
|----------|------------------|-------------------|---------------------|
| | | | |
| | | | |
| | | | |

Compare to Lab Charter caps. If over: cut again before buying quieter gear.

---

## B. Shrink the ISO / archive (collection → policy)

100TB of Linux ISOs is almost never a mission. It is a collection.

### Retention policy (align with charter)

| Keep | Do not keep |
|------|-------------|
| Current LTS of distros you actually install | Every historical point release “just in case” |
| Previous major of the same (optional, if charter says) | Mirrors you have not used in 12 months |
| Tools you rebuild from (netboot, firmware you flash) | Duplicate ISOs across pools |
| Checksums / a short manifest of what you keep | Unlabeled folders named `old`, `misc`, `temp` |

### Collapse procedure

1. **Write the allowlist** in [`01-lab-charter.md`](01-lab-charter.md) (curated mirror table).
2. **Copy allowlist** to a new `curated-mirror/` tree (or dedicated dataset).
3. **Verify checksums** for what you keep.
4. **Delete or cold-archive offsite** the rest. Prefer delete if re-downloadable in an afternoon.
5. **Record size before/after** below.
6. **Free or Exit** emptied shelves/chassis that existed only for the collection.

| Metric | Before | After (target) | After (actual) |
|--------|--------|----------------|----------------|
| ISO / mirror TB | | (charter target) | |
| Disks / chassis dedicated to collection | | | |
| Hours to re-download curated set | | | |

**Honesty gate:** If you will not re-download it in an afternoon and it is not on the allowlist, it does not deserve rack power.

---

## C. Compute power — named jobs only

| Host / GPU | Named job | Last run | Keep powered? | Else |
|------------|-----------|----------|---------------|------|
| | | | Y / N | Power off / Exit |
| | | | Y / N | |
| | | | Y / N | |

“I might train a model” is not a job.  
“Transcode the family library every Sunday” is a job.  
“One game server for friends, starts Friday” is a job with a start/stop ritual.

---

## D. Blanking, labels, boredom

- [ ] Blanking panels in freed U  
- [ ] Cable labels on primary links  
- [ ] Switch ports documented on restore one-pager  
- [ ] Door inventory updated  

Boredom is a feature. If the stack cannot survive looking boring, it will be abandoned right before it works.

---

## Done criteria for this todo

- [ ] Powered 24/7 hosts ≤ charter max  
- [ ] All Keep services running on the minimal footprint  
- [ ] Soak completed (or scheduled) for powered-off hosts  
- [ ] ISO/archive at or under charter TB target  
- [ ] Curated allowlist written  
- [ ] Restore one-pager updated with new topology
