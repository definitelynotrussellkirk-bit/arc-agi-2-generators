# ARC-AGI-2 Puzzle Generators

> **v0.1, work in progress.** Things work end-to-end (audit + lint
> pass, runner produces validated pairs), but the rough edges are
> stated, not hidden — see [ROADMAP.md](ROADMAP.md) for what's open.

**The basic idea:**

An ARC-AGI-2 puzzle is implicitly a function `f: [array] → [array]`.
A few training pairs are observations of that function. They don't
*give* you `f`; you have to infer it.

This repo flips the asymmetry: for each puzzle, we **describe `f`
explicitly** as a small Racket program in a 374-primitive DSL. The
program *is* the answer.

Then — and this is the load-bearing part — we ask the second question:

> *Given this rule, what kinds of input arrays make the rule's
> behavior visible? What kinds make it invisible or trivially
> satisfied?*

That second question is what the generator answers. Each per-puzzle
generator declares two distributions over inputs:

- **`HELPFUL_TEXTURES`** — inputs that show off the rule. If the rule
  is "fill enclosed regions with yellow," helpful inputs include
  noisy grids with clear enclosures, sparse grids with one or two
  rooms, multi-frame grids with nested boundaries.
- **`DEGENERATE_TEXTURES`** — inputs that hide the rule. For the same
  rule: a grid with no enclosed regions (rule has no effect), a fully
  filled grid (already satisfied), a single pixel (degenerate).

Combine the explicit `f` (Racket program) with this *intentional*
input distribution (Python generator) and you get
**combinatorially many `(input, output)` pairs per puzzle, each
chosen to make the rule either maximally observable or
deliberately edge-case**. Outputs are never authored — they're
*computed* by running `f` on the generated input.

Across the 3,889-puzzle corpus the bounded reach is currently
**2.56 × 10¹¹** distinct configurations (lower bound — see
[docs/COMBINATORIAL_REACH.md](docs/COMBINATORIAL_REACH.md)); the seed
dimension is unbounded on top of that.

## Combinatorial reach

```
generators:                    3,889
total bounded configurations:  2.56 × 10¹¹
with seed budget 1,000:        2.56 × 10¹⁴
per-generator median:          48,384 distinct configurations
generators with unbounded axes: 3,480 of 3,889
```

Numbers are a **lower bound** — the calculator only counts axes whose
`valid` field parses as an enumerable range or set; descriptive
free-form axes (e.g. `valid: "varied"`) contribute 1 instead of their
true cardinality. Rerun yourself with:

```bash
python3 scripts/combinatorial_reach.py
```

## What's in the box

| Path | What |
|------|------|
| `puzzle_generators/per_puzzle/<hash>/generator.py` | 3,889 generators, one per canonical puzzle |
| `puzzle_generators/runner.py` | Loads generator + rule, runs Racket, validates output |
| `puzzle_generators/helpers/` | Reusable texture / blob / palette / grid primitives |
| `arc_repl/racket_prelude/arc-prelude.rkt` | The Racket DSL (374 grid primitives) |
| `arc_repl/racket_bridge.py` | Python ↔ Racket subprocess bridge |
| `data/canonical/puzzles.jsonl` | 4,350 canonical puzzle rows (4,349 with verified Racket rules; 1 still in `data/derived/conversion_backlog.jsonl`) |
| `data/canonical/puzzle_db.jsonl` | Per-puzzle metadata (difficulty tags, primitives used, content hashes; ELO field is reserved but currently 0 for every row) |
| `data/base/solutions/` | Per-puzzle solution JSONs (rule text + descriptions; grid arrays are intentionally not shipped) |
| `solvers/grounded_rules.py` | 1,000 Racket rules covering ARC-AGI-2 training tasks |
| `scripts/combinatorial_reach.py` | Reach calculator (lower-bound, prints the headline) |
| `scripts/regen_all.py` | Rebuild canonical, db, manifests, docs, lint |
| `scripts/lint_*.py` | Lint passes (canonical ↔ DB consistency, schema, vocab, racket style, descriptions). Some checks were relaxed when grid arrays were stripped — see [ROADMAP.md](ROADMAP.md). |
| `docs/CANONICAL_VOCAB.md` | The closed primitive set |
| `docs/CANONICAL_STYLE.md` | How to write a rule |
| `docs/PUZZLE_GENERATOR_SPEC.md` | Generator module contract |

## Identifiers

Every puzzle's `task_id` is a 12-char `content_hash` — a SHA-256 prefix
over (train, test). The directory name is the `task_id`. Bank
directories (under `data/custom_puzzles/banks/` and
`data/base/solutions/banks/`) are also identified by 12-char hashes.

Augmented variants (multiple input grids exercising the same rule)
share their parent's `task_id` and live in the same generator
directory.

## Install

Requires Python ≥ 3.10 and Racket ≥ 8.0 on PATH.

```bash
git clone https://github.com/<you>/arc-agi-2-generators
cd arc-agi-2-generators
pip install -r requirements.txt    # (none yet — pure stdlib)

# Confirm Racket is on PATH:
racket --version

# Optional: download ARC-Prize 2026 raw data (used for cold-rebuilds
# of canonical/puzzles.jsonl from upstream sources). The release
# already ships a built canonical, so this is only needed if you
# want to rebuild from scratch.
python3 scripts/fetch_arc_data.py
```

## Quickstart

```python
from puzzle_generators import runner

# Generate a fresh (input, output) instance for a puzzle, by task_id.
result = runner.run_one("ecc04b33119c", seed=42, sample_index=0)

print(f"{len(result['train'])} train pairs, {len(result['test'])} test")
for pair in result['train'][:1]:
    for row in pair['input']:
        print(row)
    print("→")
    for row in pair['output']:
        print(row)
```

See [QUICKSTART.md](QUICKSTART.md) for a longer tour.

## License

Code: MIT (see `LICENSE`).

The `data/canonical/` and `data/base/solutions/` directories contain
puzzles derived from the ARC-AGI-2 competition, additional
hand-authored bank puzzles, and verified Racket solutions authored by
this project's contributors. ARC-original puzzles inherit the upstream
ARC-AGI-2 license; see `LICENSES/ARC-AGI-2.md`.

## Citation

```bibtex
@misc{arc-agi-2-generators-2026,
  title  = {{ARC-AGI-2 Puzzle Generators: A Corpus of 3,889
            Combinatorial Generators with Verified Racket Solutions}},
  year   = {2026},
  url    = {https://github.com/<you>/arc-agi-2-generators}
}
```
