"""Live-regenerating documentation for the puzzle bank.

The docs live in `docs/PUZZLE_BANK.md`, BUT that file is REGENERATED
from `data/canonical/puzzles.jsonl` — it's never hand-edited. Running
this script on a cron (hourly) means the doc can never drift from the
ground truth.

What the doc shows (all derived from the data, nothing hardcoded):

  - Totals by source (training / augmented / custom / custom_bank)
  - Totals by difficulty (for sources that carry one)
  - Tag cloud (how many puzzles touch each capability)
  - Per-section table: id, name, difficulty, train/test counts
  - Per-task detail pages (input/output grids as ASCII,
    written rule, program solution)

CLI modes:

  regen                      # rebuild canonical, regen doc, exit
  query --difficulty HARD    # print matching tasks
  query --tag containment    # tag filter
  watch --interval 3600      # loop: regen every N seconds
  list-sources               # sections + counts

Install hourly cron entry (paste into `crontab -e`):

  0 * * * * cd /path/to/repo && \\
      /usr/bin/python3 scripts/puzzle_docs.py regen \\
      >> /tmp/puzzle_docs.cron.log 2>&1

Install systemd user timer (preferred on modern Linux):

  python3 scripts/puzzle_docs.py install-systemd-timer
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import textwrap
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "data" / "canonical" / "puzzles.jsonl"
DOC_OUT = ROOT / "docs" / "PUZZLE_BANK.md"
BUILD_SCRIPT = ROOT / "scripts" / "build_canonical_puzzles.py"


# =====================================================================
# Data loading
# =====================================================================

def load_bank() -> list[dict]:
    if not CANONICAL.exists():
        raise SystemExit(
            f"canonical dataset missing: {CANONICAL}\n"
            f"run: python3 {BUILD_SCRIPT.relative_to(ROOT)}"
        )
    with CANONICAL.open() as f:
        return [json.loads(line) for line in f if line.strip()]


# =====================================================================
# Doc generation
# =====================================================================

def _grid_to_ascii(grid: list[list[int]]) -> str:
    if not grid or not isinstance(grid[0], list):
        return "(empty)"
    return "\n".join("".join(str(v) for v in row) for row in grid)


def _render_task_detail(entry: dict) -> str:
    """Expandable details block for one task — ASCII grids + rule."""
    lines = []
    tid = entry["task_id"]
    title = entry.get("title") or ""
    src = entry["source"]
    diff = entry.get("difficulty", "")
    skills = entry.get("skills", []) or []
    written = entry.get("written_solution", "")
    rule_racket = entry.get("program_solution", "")
    needs_conv = bool(entry.get("needs_conversion"))

    header = (f"### `{tid}` — {title or src}" if title
              else f"### `{tid}`")
    lines.append(header)
    meta = []
    if src: meta.append(f"source=**{src}**")
    if diff: meta.append(f"difficulty=**{diff}**")
    if skills: meta.append(f"skills=`{', '.join(skills)}`")
    n_train = len(entry.get("train", []))
    n_test = len(entry.get("test", []))
    meta.append(f"train={n_train}  test={n_test}")
    if needs_conv:
        meta.append("**needs_conversion**")
    lines.append(" · ".join(meta))
    lines.append("")
    if written:
        lines.append(f"**Rule:** {written}")
        lines.append("")

    # Show the first train pair as ASCII
    train = entry.get("train") or []
    if train:
        lines.append("<details><summary>Example pair</summary>")
        lines.append("")
        lines.append("```")
        lines.append("input:")
        lines.append(_grid_to_ascii(train[0]["input"]))
        lines.append("")
        lines.append("output:")
        lines.append(_grid_to_ascii(train[0]["output"]))
        lines.append("```")
        lines.append("</details>")
        lines.append("")

    if rule_racket:
        lines.append("<details><summary>Program solution (Racket)</summary>")
        lines.append("")
        lines.append("```scheme")
        # Truncate extremely long rules in the doc
        preview = rule_racket if len(rule_racket) < 2000 else \
                  rule_racket[:2000] + "\n;; ... (truncated)"
        lines.append(preview)
        lines.append("```")
        lines.append("</details>")
        lines.append("")

    lines.append("---")
    return "\n".join(lines)


def generate_doc(bank: list[dict]) -> str:
    by_source: defaultdict[str, list] = defaultdict(list)
    for e in bank:
        by_source[e["source"]].append(e)

    difficulty_counts: Counter = Counter()
    skill_counts: Counter = Counter()
    for e in bank:
        if e.get("difficulty"):
            # Normalize casing — custom_examples uses HARD/MEDIUM, bank_21
            # uses hard/medium. Collapse so the summary table agrees.
            difficulty_counts[e["difficulty"].lower()] += 1
        for t in e.get("skills", []) or []:
            skill_counts[t] += 1

    generated_at = time.strftime("%Y-%m-%d %H:%M:%S %z") or \
                   time.strftime("%Y-%m-%d %H:%M:%S")
    size_mb = CANONICAL.stat().st_size / 1e6

    sections: list[str] = []
    sections.append(f"# Puzzle Bank")
    sections.append("")
    sections.append(
        f"*Generated {generated_at} from "
        f"`{CANONICAL.relative_to(ROOT)}` "
        f"({size_mb:.1f} MB, {len(bank)} entries). "
        f"**Do not hand-edit — run `python3 "
        f"{Path(__file__).relative_to(ROOT)} regen` to refresh.***"
    )
    sections.append("")

    # Totals table
    sections.append("## Totals by source")
    sections.append("")
    sections.append("| source | count | unique task_ids |")
    sections.append("|---|---:|---:|")
    for src in sorted(by_source):
        entries = by_source[src]
        n_unique = len({e["task_id"] for e in entries})
        sections.append(f"| `{src}` | {len(entries)} | {n_unique} |")
    sections.append(f"| **total** | **{len(bank)}** | "
                    f"**{len({e['task_id'] for e in bank})}** |")
    sections.append("")

    # Difficulty
    if difficulty_counts:
        sections.append("## Difficulty (custom + bank_21 only)")
        sections.append("")
        sections.append("| difficulty | count |")
        sections.append("|---|---:|")
        for d, n in sorted(difficulty_counts.items(),
                           key=lambda kv: (-kv[1], kv[0])):
            sections.append(f"| {d} | {n} |")
        sections.append("")

    # Skill cloud
    if skill_counts:
        sections.append("## Skills")
        sections.append("")
        sections.append("| skill | count |")
        sections.append("|---|---:|")
        for t, n in sorted(skill_counts.items(),
                           key=lambda kv: (-kv[1], kv[0])):
            sections.append(f"| `{t}` | {n} |")
        sections.append("")

    # Per-section detailed listings — small human-authored sections
    # (custom + every bank:*). Training + augmented are too many to
    # list individually; summary table + collapsed task_id dump.
    detail_sources = ["custom"] + sorted(
        s for s in by_source if s.startswith("bank:"))
    for src in detail_sources:
        entries = by_source.get(src, [])
        if not entries:
            continue
        sections.append(f"## Section: `{src}` — {len(entries)} tasks")
        sections.append("")
        # Summary table
        sections.append("| id | title | difficulty | skills | train/test | needs_conv |")
        sections.append("|---|---|---|---|---|---|")
        for e in sorted(entries, key=lambda x: (
                str(x.get("difficulty", "")), str(x.get("title", "")))):
            title = e.get("title", "")
            diff = e.get("difficulty", "")
            skills = ", ".join(e.get("skills", []) or [])
            nt = len(e.get("train", []))
            ntt = len(e.get("test", []))
            nc = "yes" if e.get("needs_conversion") else ""
            sections.append(
                f"| `{e['task_id']}` | {title} | {diff} | {skills} | "
                f"{nt}/{ntt} | {nc} |"
            )
        sections.append("")

        # Per-task detail expandables
        for e in sorted(entries, key=lambda x: (
                str(x.get("difficulty", "")), str(x.get("title", "")))):
            sections.append(_render_task_detail(e))

    # Training + augmented one-line-per-task summary at the end
    for src in ("training", "augmented"):
        entries = by_source.get(src, [])
        if not entries:
            continue
        sections.append(f"## Section: `{src}` — {len(entries)} tasks")
        sections.append("")
        sections.append(
            f"<details><summary>All {len(entries)} task_ids (click to expand)"
            f"</summary>"
        )
        sections.append("")
        sections.append("```")
        for e in sorted(entries, key=lambda x: x["task_id"]):
            nt = len(e.get("train", []))
            ntt = len(e.get("test", []))
            sections.append(f"{e['task_id']}  train={nt}  test={ntt}")
        sections.append("```")
        sections.append("</details>")
        sections.append("")

    return "\n".join(sections)


# =====================================================================
# Operations
# =====================================================================

def op_regen(rebuild_canonical: bool = True) -> None:
    """Rebuild canonical (optional) + regen doc."""
    if rebuild_canonical:
        print(f"→ building canonical …", flush=True)
        r = subprocess.run([sys.executable, str(BUILD_SCRIPT)],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print(r.stdout)
            print(r.stderr, file=sys.stderr)
            raise SystemExit("canonical build failed")
        print(r.stdout.strip())
    bank = load_bank()
    doc = generate_doc(bank)
    DOC_OUT.parent.mkdir(parents=True, exist_ok=True)
    DOC_OUT.write_text(doc)
    print(f"→ {DOC_OUT}  ({len(doc)/1024:.1f} KB)")


def op_query(args) -> None:
    bank = load_bank()
    results = []
    for e in bank:
        if args.source and e.get("source") != args.source:
            continue
        if args.difficulty and e.get("difficulty", "").lower() != \
                args.difficulty.lower():
            continue
        if args.tag and args.tag not in (e.get("skills", []) or []):
            continue
        if args.name and args.name.lower() not in e.get("title", "").lower():
            continue
        results.append(e)
    for e in results[:args.limit]:
        print(f"[{e['source']:<12}] [{e.get('difficulty') or '-':<6}] "
              f"{e['task_id']:<12} {e.get('title','')}")
        if e.get("skills"):
            print(f"    skills: {', '.join(e['skills'])}")
        if e.get("written_solution"):
            print(f"    rule: {e['written_solution'][:120]}")
    print(f"\n{len(results)} matches (showing {min(len(results), args.limit)})")


def op_list_sources() -> None:
    bank = load_bank()
    by_src = Counter(e["source"] for e in bank)
    print("source counts:")
    for s, n in sorted(by_src.items(), key=lambda kv: -kv[1]):
        print(f"  {s:<14} {n}")


def op_watch(interval: int) -> None:
    """Regenerate every `interval` seconds. Simple alternative to cron."""
    print(f"watching: regen every {interval}s (Ctrl-C to stop)", flush=True)
    while True:
        try:
            op_regen(rebuild_canonical=True)
        except SystemExit as e:
            print(f"  ! {e}", flush=True)
        except Exception as e:
            print(f"  ! regen raised {type(e).__name__}: {e}", flush=True)
        time.sleep(interval)


def op_install_systemd_timer() -> None:
    """Generate a user-level systemd timer that runs regen hourly."""
    unit_dir = Path.home() / ".config" / "systemd" / "user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    service_path = unit_dir / "arcagi2-puzzle-docs.service"
    timer_path = unit_dir / "arcagi2-puzzle-docs.timer"

    service = textwrap.dedent(f"""\
        [Unit]
        Description=Regenerate ARCagi2 puzzle bank documentation

        [Service]
        Type=oneshot
        WorkingDirectory={ROOT}
        ExecStart={sys.executable} {Path(__file__)} regen
        """)

    timer = textwrap.dedent(f"""\
        [Unit]
        Description=Run arcagi2-puzzle-docs hourly

        [Timer]
        OnBootSec=5min
        OnUnitActiveSec=1h
        Unit=arcagi2-puzzle-docs.service

        [Install]
        WantedBy=timers.target
        """)

    service_path.write_text(service)
    timer_path.write_text(timer)
    print(f"wrote {service_path}")
    print(f"wrote {timer_path}")
    print()
    print("To activate:")
    print("  systemctl --user daemon-reload")
    print("  systemctl --user enable --now arcagi2-puzzle-docs.timer")
    print("  systemctl --user list-timers arcagi2-puzzle-docs.timer")


# =====================================================================
# CLI
# =====================================================================

def main():
    ap = argparse.ArgumentParser(prog="puzzle_docs")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("regen", help="rebuild canonical + regen doc")
    sp.add_argument("--no-canonical", action="store_true",
                    help="skip canonical rebuild, just regen doc")

    sp = sub.add_parser("query", help="filter bank by difficulty/tag/name")
    sp.add_argument("--source")
    sp.add_argument("--difficulty")
    sp.add_argument("--tag")
    sp.add_argument("--name")
    sp.add_argument("--limit", type=int, default=50)

    sub.add_parser("list-sources", help="count by source")

    sp = sub.add_parser("watch", help="regen on a fixed interval")
    sp.add_argument("--interval", type=int, default=3600)

    sub.add_parser("install-systemd-timer",
                   help="write user-level systemd .timer + .service")

    args = ap.parse_args()
    if args.cmd == "regen":
        op_regen(rebuild_canonical=not args.no_canonical)
    elif args.cmd == "query":
        op_query(args)
    elif args.cmd == "list-sources":
        op_list_sources()
    elif args.cmd == "watch":
        op_watch(args.interval)
    elif args.cmd == "install-systemd-timer":
        op_install_systemd_timer()


if __name__ == "__main__":
    main()
