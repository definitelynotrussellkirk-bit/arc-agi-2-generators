"""Sync Racket solutions from `data/base/solutions/banks/<bank>/<id>__<hash>.json`
(the codex-authored per-puzzle format with `racket_target.raw_code`) into
`data/custom_puzzles/banks/<bank>/puzzles.json` (the legacy format with
`program_solution` per entry).

The canonical builder reads from the latter; codex writes to the former.
This script keeps them in sync.

Idempotent: skips entries whose `program_solution` already starts with
`(rule!`. Idempotent across multiple `puzzles.json` shapes:
  - flat list of entries
  - {metadata: {…}, puzzles: [...]}
  - {id: entry, ...} dict

Usage:
  python3 scripts/sync_bank_solutions.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_BANKS = ROOT / "data" / "custom_puzzles" / "banks"
NEW_BANKS = ROOT / "data" / "base" / "solutions" / "banks"


def get_entries(puz):
    """Extract puzzle entries (mutable in place) and the form tag."""
    if isinstance(puz, list):
        return puz, "list"
    if isinstance(puz, dict):
        if "puzzles" in puz and isinstance(puz["puzzles"], list):
            return puz["puzzles"], "wrapped"
        return list(puz.values()), "dict"
    return [], "unknown"


def collect_new_solutions(bank_new_dir: Path) -> dict[str, str]:
    """Read every <id>__<hash>.json in a new-format bank directory and
    return {original_id → racket_source} for entries with a `(rule!` body."""
    out: dict[str, str] = {}
    if not bank_new_dir.is_dir():
        return out
    for f in os.listdir(bank_new_dir):
        if not f.endswith(".json"):
            continue
        try:
            d = json.loads((bank_new_dir / f).read_text())
        except Exception:
            continue
        oid = d.get("original_id")
        rt = d.get("racket_target") or {}
        code = rt.get("raw_code") or ""
        if oid and code.lstrip().startswith("(rule!"):
            out[oid] = code
    return out


def sync_bank(bank_name: str) -> int:
    """Sync one bank. Returns the count of entries updated."""
    old_dir = OLD_BANKS / bank_name
    new_dir = NEW_BANKS / bank_name
    puz_path = old_dir / "puzzles.json"
    if not puz_path.exists():
        return 0
    new_by_id = collect_new_solutions(new_dir)
    if not new_by_id:
        return 0

    old_puz = json.loads(puz_path.read_text())
    entries, _form = get_entries(old_puz)

    n_synced = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        eid = entry.get("id")
        if not eid or eid not in new_by_id:
            continue
        old_sol = entry.get("program_solution") or ""
        if old_sol.lstrip().startswith("(rule!"):
            continue  # already synced
        new_sol = new_by_id[eid]
        if old_sol.strip() == new_sol.strip():
            continue
        entry["program_solution"] = new_sol
        n_synced += 1

    if n_synced:
        puz_path.write_text(json.dumps(old_puz, indent=2))
    return n_synced


def main() -> int:
    if not OLD_BANKS.is_dir():
        print(f"missing {OLD_BANKS}", file=sys.stderr)
        return 1
    total_synced = 0
    n_banks_modified = 0
    for bank_name in sorted(p.name for p in OLD_BANKS.iterdir() if p.is_dir()):
        n = sync_bank(bank_name)
        if n:
            n_banks_modified += 1
            total_synced += n
            print(f"  {bank_name}: +{n}")
    print(f"synced {total_synced} entries across {n_banks_modified} banks.")
    print("Run `python3 scripts/regen_all.py` to refresh canonical/DB/docs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
