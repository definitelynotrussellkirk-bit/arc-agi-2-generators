"""SQLite-backed catalog of puzzle-instance generators.

Mirrors rack's catalog pattern (~/Desktop/rack/catalog.py) — the DB is
a discoverable registry; it can be rebuilt from the filesystem at any
time via `scan`. Don't commit the DB; the source of truth is the
generator modules + the rule files.

CLI verbs (all idempotent):
    scan      -- walk puzzle_generators/per_puzzle/, register everything
    list      -- show registered generators (optional filters)
    info ID   -- detailed info for one generator
    validate  -- run 20 instances per generator, record pass rate
    generate  -- produce N instances; write JSONL; record the batch
    stats     -- aggregates (count, avg pass rate, total instances)
    coverage  -- which concepts have generators, which don't
    export    -- dump catalog to JSONL

Schema (two tables):
    generators(task_id PRIMARY KEY, module_path, version, concept_hash,
               summary, invariants_json, axes_json, origin,
               first_seen, last_scanned, last_validated,
               validation_pass_rate, validation_error)
    batches(batch_id PRIMARY KEY, task_id, n_requested, n_produced,
            n_rejected, seed_start, axes_overrides_json, output_path,
            created_at)
"""
from __future__ import annotations

import argparse
import contextlib
import importlib
import json
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PER_PUZZLE_DIR = ROOT / "puzzle_generators" / "per_puzzle"
DB_PATH = ROOT / "puzzle_generators" / ".catalog.db"
GENERATED_DIR = ROOT / "data" / "generated"

GREEN = "\033[32m"; RED = "\033[31m"; YELLOW = "\033[33m"; RESET = "\033[0m"


# ---------------------------------------------------------------------------
# DB schema and connection
# ---------------------------------------------------------------------------

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS generators (
    task_id              TEXT PRIMARY KEY,
    module_path          TEXT NOT NULL,
    version              TEXT NOT NULL DEFAULT '',
    concept_hash         TEXT NOT NULL DEFAULT '',
    summary              TEXT NOT NULL DEFAULT '',
    invariants_json      TEXT NOT NULL DEFAULT '[]',
    axes_json            TEXT NOT NULL DEFAULT '{}',
    origin               TEXT NOT NULL DEFAULT 'hand',
    first_seen           TEXT NOT NULL DEFAULT (datetime('now')),
    last_scanned         TEXT NOT NULL DEFAULT (datetime('now')),
    last_validated       TEXT,
    validation_pass_rate REAL,
    validation_error     TEXT
);

CREATE TABLE IF NOT EXISTS batches (
    batch_id              TEXT PRIMARY KEY,
    task_id               TEXT NOT NULL,
    n_requested           INTEGER NOT NULL,
    n_produced            INTEGER NOT NULL,
    n_rejected            INTEGER NOT NULL,
    seed_start            INTEGER NOT NULL,
    axes_overrides_json   TEXT NOT NULL DEFAULT '{}',
    output_path           TEXT NOT NULL,
    created_at            TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS batches_task ON batches(task_id);
CREATE INDEX IF NOT EXISTS gen_concept ON generators(concept_hash);
"""


@contextlib.contextmanager
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA_SQL)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Discovery — walk per_puzzle/ and import generator modules
# ---------------------------------------------------------------------------

def _discover_generator_dirs() -> list[Path]:
    if not PER_PUZZLE_DIR.exists():
        return []
    out = []
    for d in sorted(PER_PUZZLE_DIR.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith("_") or d.name.startswith("."):
            continue
        if (d / "generator.py").is_file():
            out.append(d)
    return out


def _import_generator(d: Path):
    """Import puzzle_generators.per_puzzle.<dirname>.generator. Returns
    the module or raises."""
    pkg = f"puzzle_generators.per_puzzle.{d.name}.generator"
    return importlib.import_module(pkg)


def _gather_meta(mod) -> dict:
    """Read the contract symbols from a generator module."""
    return {
        "task_id":      getattr(mod, "TASK_ID",      getattr(mod, "GENERATOR_ID", "")),
        "version":      getattr(mod, "VERSION",      ""),
        "concept_hash_claimed": getattr(mod, "CONCEPT_HASH", ""),
        "summary":      getattr(mod, "SUMMARY",      ""),
        "invariants":   list(getattr(mod, "INVARIANTS", [])),
        "axes":         dict(getattr(mod, "AXES",       {})),
        "origin":       getattr(mod, "ORIGIN",       "hand"),
    }


def _canonical_concept_hash(task_id: str) -> tuple[str, str]:
    """Compute the concept_hash for a task by canonicalizing its rule.
    Returns (hash, error). One of them is always empty."""
    from puzzle_generators.runner import _load_rule
    from scripts.canonicalize_rule import canonicalize_rule
    try:
        src, _ = _load_rule(task_id)
    except Exception as e:
        return "", f"rule_load_failed: {e}"
    info = canonicalize_rule(src)
    if not info["concept_hash"]:
        return "", f"canonicalize_failed: {info.get('reason', 'unknown')}"
    return info["concept_hash"], ""


# ---------------------------------------------------------------------------
# Verbs
# ---------------------------------------------------------------------------

def cmd_scan(args) -> int:
    """Walk per_puzzle/, import each generator, upsert into the catalog."""
    dirs = _discover_generator_dirs()
    if not dirs:
        print(f"{YELLOW}no generators found under {PER_PUZZLE_DIR.relative_to(ROOT)}{RESET}")
        return 0
    n_ok = n_err = 0
    with _connect() as conn:
        for d in dirs:
            try:
                mod = _import_generator(d)
                meta = _gather_meta(mod)
            except Exception as e:
                n_err += 1
                print(f"  {RED}FAIL{RESET} {d.name}: {type(e).__name__}: {e}")
                continue
            # Sanity: dir name must match TASK_ID (with `:` ↔ `__` mangling).
            expected_dirname = meta["task_id"].replace(":", "__").replace("/", "__").replace("-", "_")
            if d.name != expected_dirname:
                n_err += 1
                print(f"  {RED}FAIL{RESET} {d.name}: TASK_ID={meta['task_id']!r} does not match directory name "
                      f"(expected {expected_dirname!r}). Rename the directory or fix TASK_ID.")
                continue
            # Compute the real concept_hash from the rule itself — the
            # generator's CONCEPT_HASH constant is documentation only.
            real_hash, err = _canonical_concept_hash(meta["task_id"])
            note = ""
            if real_hash:
                if (meta["concept_hash_claimed"]
                        and meta["concept_hash_claimed"] != real_hash):
                    note = (f"  {YELLOW}(claimed {meta['concept_hash_claimed']}, "
                            f"actual {real_hash}){RESET}")
            else:
                note = f"  {YELLOW}({err}){RESET}"
                real_hash = meta["concept_hash_claimed"]  # fall back
            mp = str((d / "generator.py").relative_to(ROOT))
            conn.execute(
                """
                INSERT INTO generators
                  (task_id, module_path, version, concept_hash, summary,
                   invariants_json, axes_json, origin, last_scanned)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                ON CONFLICT(task_id) DO UPDATE SET
                  module_path=excluded.module_path,
                  version=excluded.version,
                  concept_hash=excluded.concept_hash,
                  summary=excluded.summary,
                  invariants_json=excluded.invariants_json,
                  axes_json=excluded.axes_json,
                  origin=excluded.origin,
                  last_scanned=datetime('now')
                """,
                (meta["task_id"], mp, meta["version"], real_hash,
                 meta["summary"],
                 json.dumps(meta["invariants"], ensure_ascii=False),
                 json.dumps(meta["axes"], ensure_ascii=False),
                 meta["origin"]),
            )
            n_ok += 1
            print(f"  {GREEN}OK  {RESET} {meta['task_id']:<16} v{meta['version']}  "
                  f"concept={real_hash}{note}")
    print(f"\nscanned: {n_ok} ok, {n_err} errors")
    return 0 if n_err == 0 else 1


def cmd_list(args) -> int:
    with _connect() as conn:
        q = "SELECT * FROM generators"
        params: list = []
        clauses: list[str] = []
        if args.concept:
            clauses.append("concept_hash = ?"); params.append(args.concept)
        if args.origin:
            clauses.append("origin = ?"); params.append(args.origin)
        if clauses:
            q += " WHERE " + " AND ".join(clauses)
        q += " ORDER BY task_id"
        rows = list(conn.execute(q, params))
    if not rows:
        print("(no rows)")
        return 0
    print(f"{'task_id':<25} {'version':>8}  {'concept_hash':<14}  {'origin':<6}  summary")
    for r in rows:
        s = (r["summary"] or "").replace("\n", " ")
        if len(s) > 60:
            s = s[:57] + "..."
        print(f"{r['task_id']:<25} {r['version']:>8}  {r['concept_hash']:<14}  {r['origin']:<6}  {s}")
    print(f"\n{len(rows)} generators")
    return 0


def cmd_info(args) -> int:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM generators WHERE task_id = ?", (args.task_id,)
        ).fetchone()
        if not row:
            print(f"{RED}no generator for task_id {args.task_id}{RESET}", file=sys.stderr)
            return 1
        print(f"task_id:        {row['task_id']}")
        print(f"module:         {row['module_path']}")
        print(f"version:        {row['version']}")
        print(f"concept_hash:   {row['concept_hash']}")
        print(f"origin:         {row['origin']}")
        print(f"first_seen:     {row['first_seen']}")
        print(f"last_scanned:   {row['last_scanned']}")
        print(f"last_validated: {row['last_validated'] or '(never)'}")
        if row["validation_pass_rate"] is not None:
            print(f"pass_rate:      {row['validation_pass_rate']:.1%}")
        if row["validation_error"]:
            print(f"validate_error: {row['validation_error'][:200]}")
        print()
        print(f"summary:        {row['summary']}")
        print()
        print("invariants:")
        for inv in json.loads(row["invariants_json"] or "[]"):
            print(f"  - {inv}")
        print()
        print("axes:")
        for k, spec in json.loads(row["axes_json"] or "{}").items():
            print(f"  {k:<20} {spec}")
        # Show recent batches
        batches = list(conn.execute(
            "SELECT * FROM batches WHERE task_id = ? ORDER BY created_at DESC LIMIT 5",
            (args.task_id,)
        ))
        if batches:
            print()
            print("recent batches:")
            for b in batches:
                print(f"  {b['batch_id']:<35} produced={b['n_produced']}/{b['n_requested']} "
                      f"rej={b['n_rejected']}  {b['output_path']}")
    return 0


def cmd_validate(args) -> int:
    """Run 20 instances per generator, record pass rate. Sets
    validation_pass_rate and validation_error in the catalog."""
    from puzzle_generators.runner import run_batch

    with _connect() as conn:
        rows = list(conn.execute(
            "SELECT task_id FROM generators"
            + (" WHERE task_id = ?" if args.task else "")
            + " ORDER BY task_id",
            (args.task,) if args.task else (),
        ))
    if not rows:
        print("(no generators registered — run `scan` first)")
        return 0

    n = args.n or 20
    for r in rows:
        tid = r["task_id"]
        t0 = time.time()
        try:
            batch = run_batch(tid, n=n, n_train=4, n_test=1)
            pass_rate = len(batch) / n
            err = ""
        except Exception as e:
            pass_rate = 0.0
            err = f"{type(e).__name__}: {str(e)[:300]}"
        elapsed = time.time() - t0
        with _connect() as conn:
            conn.execute(
                """UPDATE generators SET last_validated=datetime('now'),
                          validation_pass_rate=?, validation_error=? WHERE task_id=?""",
                (pass_rate, err, tid)
            )
        color = GREEN if pass_rate >= 0.9 else (YELLOW if pass_rate >= 0.5 else RED)
        verdict = "OK  " if pass_rate >= 0.9 else ("WARN" if pass_rate >= 0.5 else "FAIL")
        print(f"  {color}{verdict}{RESET} {tid:<25} pass_rate={pass_rate:.0%}  ({elapsed:.1f}s){'  '+err if err else ''}")
    return 0


def cmd_generate(args) -> int:
    """Run a generator, write a batch JSONL, record metadata."""
    from puzzle_generators.runner import run_batch

    with _connect() as conn:
        if args.all:
            tids = [r["task_id"] for r in conn.execute(
                "SELECT task_id FROM generators ORDER BY task_id"
            )]
        else:
            tids = [args.task_id]
            if not conn.execute(
                "SELECT 1 FROM generators WHERE task_id = ?", (args.task_id,)
            ).fetchone():
                print(f"{RED}task_id {args.task_id} not registered (run scan){RESET}",
                      file=sys.stderr)
                return 1

    overrides = {}
    for kv in (args.set or []):
        if "=" not in kv:
            print(f"{RED}bad --set: {kv}{RESET}"); return 1
        k, v = kv.split("=", 1)
        try:
            overrides[k] = int(v)
        except ValueError:
            try:
                overrides[k] = float(v)
            except ValueError:
                overrides[k] = v

    for tid in tids:
        ts = time.strftime("%Y%m%dT%H%M%S")
        batch_id = f"{ts}_{tid.replace(':', '__')}_{args.n}"
        out_dir = GENERATED_DIR / "by_task" / tid.replace(":", "__")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{batch_id}.jsonl"
        t0 = time.time()
        try:
            batch = run_batch(tid, n=args.n, n_train=args.n_train, n_test=args.n_test,
                              seed_start=args.seed, **overrides)
        except Exception as e:
            print(f"  {RED}FAIL{RESET} {tid}: {type(e).__name__}: {str(e)[:200]}")
            continue
        elapsed = time.time() - t0
        with out_path.open("w") as f:
            for inst in batch:
                f.write(json.dumps(inst, ensure_ascii=False) + "\n")
        with _connect() as conn:
            conn.execute(
                """INSERT INTO batches
                   (batch_id, task_id, n_requested, n_produced, n_rejected,
                    seed_start, axes_overrides_json, output_path)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (batch_id, tid, args.n, len(batch),
                 args.n - len(batch), args.seed,
                 json.dumps(overrides), str(out_path.relative_to(ROOT))),
            )
        print(f"  {GREEN}OK  {RESET} {tid:<25} produced={len(batch)}/{args.n}  "
              f"({elapsed:.1f}s)  → {out_path.relative_to(ROOT)}")
    return 0


def cmd_stats(args) -> int:
    with _connect() as conn:
        n_gens = conn.execute("SELECT COUNT(*) FROM generators").fetchone()[0]
        n_batches = conn.execute("SELECT COUNT(*) FROM batches").fetchone()[0]
        n_inst = conn.execute("SELECT COALESCE(SUM(n_produced),0) FROM batches").fetchone()[0]
        n_validated = conn.execute(
            "SELECT COUNT(*) FROM generators WHERE last_validated IS NOT NULL"
        ).fetchone()[0]
        avg_pass = conn.execute(
            "SELECT AVG(validation_pass_rate) FROM generators WHERE validation_pass_rate IS NOT NULL"
        ).fetchone()[0]
        n_concepts = conn.execute(
            "SELECT COUNT(DISTINCT concept_hash) FROM generators WHERE concept_hash != ''"
        ).fetchone()[0]
    print(f"generators registered:  {n_gens}")
    print(f"distinct concepts:      {n_concepts}")
    print(f"batches recorded:       {n_batches}")
    print(f"instances generated:    {n_inst}")
    print(f"validated:              {n_validated}/{n_gens}"
          + (f"  avg pass = {avg_pass:.1%}" if avg_pass is not None else ""))
    return 0


def cmd_coverage(args) -> int:
    """Coverage: which concepts in concepts.jsonl have a generator? Which don't?"""
    cf = ROOT / "data" / "derived" / "concepts.jsonl"
    if not cf.exists():
        print(f"{YELLOW}{cf.relative_to(ROOT)} missing — run scripts/concept_inventory.py{RESET}")
        return 1
    concepts = [json.loads(l) for l in cf.read_text().splitlines() if l.strip()]
    with _connect() as conn:
        gen_concepts = {
            r["concept_hash"] for r in conn.execute(
                "SELECT DISTINCT concept_hash FROM generators WHERE concept_hash != ''"
            )
        }
    covered = sum(1 for c in concepts if c["concept_hash"] in gen_concepts)
    total = len(concepts)
    print(f"concepts with generators:  {covered}/{total}  ({covered/total*100:.1f}%)")
    if args.show_uncovered:
        uncovered = [c for c in concepts if c["concept_hash"] not in gen_concepts]
        # Show the largest uncovered concepts first — they're best candidates
        # for next generators (more downstream value per generator authored).
        uncovered.sort(key=lambda c: -c["n_puzzles"])
        for c in uncovered[: args.show_uncovered]:
            print(f"  {c['concept_hash']}  n={c['n_puzzles']:>3}  first={c['first_seen']}")
    return 0


def cmd_export(args) -> int:
    out = Path(args.output)
    with _connect() as conn:
        rows = list(conn.execute("SELECT * FROM generators ORDER BY task_id"))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for r in rows:
            d = {k: r[k] for k in r.keys()}
            d["invariants"] = json.loads(d.pop("invariants_json"))
            d["axes"]       = json.loads(d.pop("axes_json"))
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"wrote {out} ({len(rows)} rows)")
    return 0


# ---------------------------------------------------------------------------
# Argparse glue
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="catalog", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("scan", help="discover and register generators")
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("list", help="list registered generators")
    p.add_argument("--concept", help="filter by concept_hash")
    p.add_argument("--origin", choices=("hand", "llm"), help="filter by origin")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("info", help="detailed info for one generator")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_info)

    p = sub.add_parser("validate", help="run instances per generator, record pass rate")
    p.add_argument("--task", help="single task only")
    p.add_argument("--n", type=int, help="instances per generator (default 20)")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("generate", help="produce instances; record batch")
    p.add_argument("task_id", nargs="?", help="task to generate (or use --all)")
    p.add_argument("--all", action="store_true", help="generate for every registered task")
    p.add_argument("--n", type=int, default=50, help="instances per task")
    p.add_argument("--n-train", type=int, default=4)
    p.add_argument("--n-test", type=int, default=1)
    p.add_argument("--seed", type=int, default=0, help="seed_start for the batch")
    p.add_argument("--set", action="append", help="axis override, e.g. --set bg=5")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("stats", help="aggregate stats")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("coverage", help="concept coverage by generators")
    p.add_argument("--show-uncovered", type=int, default=0,
                    metavar="N", help="show top-N uncovered concepts")
    p.set_defaults(func=cmd_coverage)

    p = sub.add_parser("export", help="dump catalog to JSONL")
    p.add_argument("--output", "-o", required=True)
    p.set_defaults(func=cmd_export)

    return ap


def main(argv: Optional[list[str]] = None) -> int:
    ap = _build_parser()
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
