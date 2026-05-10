# Quickstart

A 5-minute tour of the corpus.

## 1. Verify your environment

```bash
python3 --version    # ≥ 3.10
racket --version     # ≥ 8.0
```

If Racket isn't on PATH, the runner will refuse to start. The Racket
prelude is a single self-contained file:
`arc_repl/racket_prelude/arc-prelude.rkt`.

## 2. Run a single generator

```python
from puzzle_generators import runner

# Task ecc04b33119c — "tile 3×3 with alternating LR mirror".
result = runner.run_one("ecc04b33119c", seed=42, sample_index=0)
print(f"{len(result['train'])} train pairs, {len(result['test'])} test")
```

The task_id is a 12-char content_hash. List available task_ids by
walking `puzzle_generators/per_puzzle/` or by reading the canonical
DB at `data/canonical/puzzle_db.jsonl`.

## 3. Inspect a generator's free axes

```python
from puzzle_generators.per_puzzle.ecc04b33119c.generator import AXES
import json
print(json.dumps(AXES, indent=2))
```

Output:

```json
{
  "grid_h":       {"type": "int", "valid": "1..10"},
  "grid_w":       {"type": "int", "valid": "1..10"},
  "palette_size": {"type": "int", "valid": "1..10"},
  "texture":      {"type": "str",
                   "valid": "noise|sparse|blob|stripes|gradient|..."},
  ...
}
```

Each axis has `type`, `default`, and `valid`. `valid` is the discrete
domain the combinatorial-reach calculator multiplies over.

## 4. The headline number

```bash
python3 scripts/combinatorial_reach.py
```

```
Combinatorial reach — 3889 generators
======================================================================
  total bounded configurations:  255,693,762,612
      (≈ 2.56e+11)
  with seed budget 1000:         255,693,762,612,000
      (≈ 2.56e+14)
  per-generator median:          48,384
  generators with unbounded axes: 3480
```

Per-bank breakdown and top-10-by-reach are also reported.

## 5. Look at one rule

Every puzzle ships a verified Racket rule. Two ways to find it:

```python
from puzzle_generators import runner
rule_src, rule_path = runner._load_rule("ecc04b33119c")
print(rule_src)
# (rule! (lambda (g)
#   (let ((h (rows g)) (w (cols g)))
#     (build-grid (* 3 h) (* 3 w) (r c)
#       (if (zero? (mod (/ r h) 2))
#           (at g (mod r h) (mod c w))
#           (at g (mod r h) (- (- w 1) (mod c w))))))))
print(f"loaded from: {rule_path}")
```

Or directly from the canonical jsonl:

```python
import json
for line in open("data/canonical/puzzles.jsonl"):
    row = json.loads(line)
    if row["task_id"] == "ecc04b33119c":
        print(row["program_solution"])
        break
```

## 6. Rebuild everything from sources

```bash
python3 scripts/regen_all.py
```

Runs (in order): `build_canonical_puzzles` → `build_puzzle_db` →
`regen_bank_manifests` → `puzzle_docs.py regen` → `lint_generators` →
`concept_inventory`. Final step is `lint_puzzles` (9 cross-checks).

`--no-lint` skips the final gate (dev-mode); `--skip-concepts` skips
the concept inventory. `lint_generators` dominates the wall-clock —
expect ~5–10 minutes end-to-end on a laptop.

**Caveat:** `build_canonical_puzzles` reads ARC raw data from
`data/raw/`, which the release does *not* ship (license — fetch it
via `python3 scripts/fetch_arc_data.py`). The release ships a
prebuilt canonical, so cold rebuild is only needed if you want to
verify the build from sources.

## 7. The DSL

The 374 Racket primitives are documented in
[docs/CANONICAL_VOCAB.md](docs/CANONICAL_VOCAB.md). The style guide
(naming, layout, idiom-level canonical forms) is
[docs/CANONICAL_STYLE.md](docs/CANONICAL_STYLE.md).

The full Racket prelude that backs them lives at
`arc_repl/racket_prelude/arc-prelude.rkt`. It's a single
`#lang racket` file, no external deps.

## 8. Generator anatomy

Open any one — they're all the same shape:

```python
# puzzle_generators/per_puzzle/ecc04b33119c/generator.py
GENERATOR_ID = "ecc04b33119c"
VERSION      = "1.1.0"
TASK_ID      = "ecc04b33119c"

SUMMARY    = "Small multicolor tile; rule tiles 3 × 3 vertically alternating with LR mirror."
INVARIANTS = ["input dims ≤ (10, 10)", "≥2 colors so the mirror is visible", ...]
AXES = {
    "grid_h": {"type": "int", "default": "rng 2..6", "valid": "1..10"},
    ...
}

HELPFUL_TEXTURES    = ("noise", "sparse", "blob", "stripes", ...)
DEGENERATE_TEXTURES = ("monochrome", "lr_symmetric", "single_pixel")

def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, ...)
    h = ctx.draw_int("grid_h", 2, 6)
    w = ctx.draw_int("grid_w", 2, 6)
    ...
    return grid
```

The runner pipes that grid through the puzzle's Racket rule and
validates the output before returning.

## 9. Lint your work

```bash
python3 scripts/lint_generator.py puzzle_generators/per_puzzle/<hash>/generator.py
python3 scripts/lint_puzzles.py     # canonical ↔ DB cross-check
```

Both are part of `regen_all.py`.

## Where to go next

- [docs/PUZZLE_GENERATOR_SPEC.md](docs/PUZZLE_GENERATOR_SPEC.md) — full module contract
- [docs/CANONICAL_VOCAB.md](docs/CANONICAL_VOCAB.md) — the DSL
- [docs/CANONICAL_STYLE.md](docs/CANONICAL_STYLE.md) — how to write a rule
- [docs/PUZZLE_BANK.md](docs/PUZZLE_BANK.md) — auto-generated index of all puzzles
- [docs/COMBINATORIAL_REACH.md](docs/COMBINATORIAL_REACH.md) — full reach report
