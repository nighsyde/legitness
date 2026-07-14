# Inventory Audit — Keep / Decide / Exit

*One evening of honesty beats a year of guilt. Do this before buying anything, cable-managing forever, or “organizing” piles into prettier piles.*

**Audit date:** _______________  
**Before photos taken:** [ ] Yes — stored at: _______________________________  
**After photos (day 90):** [ ] Yes — stored at: _______________________________

---

## Photo ritual

1. Stand at the door. Shoot wide: full room, rack front, rack rear, floor perimeter, bench, spare piles.
2. Name the album `lab-before-YYYY-MM-DD`.
3. Do **not** tidy before the photo. Evidence first.
4. On day 90, repeat as `lab-after-YYYY-MM-DD` and compare.

---

## Zone definitions

| Zone | Meaning | Physical home |
|------|---------|----------------|
| **Keep** | Named job + still used (or household depends on it) | Powered in rack / on allowlist |
| **Decide** | Unclear; gets a hard date | Single Decide tote only |
| **Exit** | Leaving via sell, gift, or recycle | Exit staging (one area or tote), then out of the room |

Tag every row below. Untagged gear is Decide by default.

---

## A. Services actually running

List every service/VM/container that is up. Kill candidates: no dependent + no use in 90 days.

| Service / VM | Host | Last real use | Who depends | Hrs/mo to keep | Outsource or delete cost | Zone: Keep / Decide / Exit | Decision |
|--------------|------|---------------|-------------|----------------|--------------------------|----------------------------|----------|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

**Services to kill this week (no dependent, stale >90 days):**

1. _______________________________________________________________________
2. _______________________________________________________________________
3. _______________________________________________________________________

---

## B. Powered gear (hosts, storage, network, UPS, PDU)

| Hostname / label | Role (one breath) | U / location | Powered 24/7? | Named job? | Last touched | Zone | Keep / power-off / Exit |
|------------------|-------------------|--------------|---------------|------------|--------------|------|-------------------------|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

**One-breath test:** If you cannot name the job in one breath, it is Decide or Exit.

**Power-off list (this week):**

| Host | Date powered off | Migrate services to | Kill-by date |
|------|------------------|---------------------|--------------|
| | | | |
| | | | |
| | | | |

---

## C. Cold / orphan hardware (not in daily use)

Cables, NICs, PSUs, old GPUs, switches, “spares,” half-built nodes, monitors, totes of mystery.

| Item | Qty | Approx value | Last use | “For parts”? | Zone | Exit path if not Keep |
|------|-----|--------------|----------|--------------|------|------------------------|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

**Parts rule:** “For parts” is only Keep if there is a **labeled parts bin** and a **written parts list**. Otherwise Exit.

---

## D. Storage & ISO / archive inventory

| Pool / array / shelf | Raw capacity | Used | What’s actually on it | Matches charter storage class? | Zone | Action |
|----------------------|--------------|------|------------------------|--------------------------------|------|--------|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

**ISO / collection honesty check**

| Question | Answer |
|----------|--------|
| Total ISO / mirror size today | _____ TB |
| Charter curated-mirror target | _____ TB |
| Would I re-download this in an afternoon if deleted? | Y / N per major tree |
| Is this a mission or a collection? | Mission / Collection |

If **Collection**: schedule collapse in [`04-minimal-stack.md`](04-minimal-stack.md). Do not defer past day 45.

---

## E. Zone summary (counts)

| Zone | Services | Powered hosts | Cold items | Storage pools |
|------|----------|---------------|------------|---------------|
| Keep | | | | |
| Decide | | | | |
| Exit | | | | |

**Brave default reminder:** Expect most perimeter clutter and a large fraction of powered gear to leave within 90 days. Empty U is a win.

---

## F. Door inventory sheet (copy to rack door)

After the cut phase, tape a short version on the door:

```
LAB INVENTORY — updated: __________
KEEP (powered):
  1.
  2.
  3.
DECIDE tote deadline: __________
EXIT staging clear-by: __________
Restore doc: reclaim-the-rack/07-restore-one-page.md
Charter missions: __________
```

---

## Done criteria for this todo

- [ ] Before photos saved  
- [ ] Every running service listed and zoned  
- [ ] Every powered host listed and zoned  
- [ ] Cold/orphan piles listed and zoned  
- [ ] Storage/ISO sized and honesty-checked  
- [ ] Kill / power-off lists dated  
- [ ] Ready for perimeter clear ([`03-perimeter-protocol.md`](03-perimeter-protocol.md))
