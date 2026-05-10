# Paper outline — ARC-AGI-2 Puzzle Generators

Working title: **A Combinatorial Corpus of 3,889 Verified Generators
for ARC-AGI-2**.

Target venue: ARC Prize 2026 paper track.

## Headline claim

We release a corpus of **3,889 deterministic input generators**, each
paired with a **verified Racket program** that maps generator output
to the canonical puzzle output. The corpus has a **bounded combinatorial
reach of 2.56 × 10¹¹** unique configurations (without seeds), and
**2.56 × 10¹⁴** with a per-generator seed budget of 1,000 — three to
six orders of magnitude beyond the 1,000 ARC training tasks alone.

Every (input, output) pair the corpus produces is **guaranteed to obey
the puzzle's canonical rule** because the output is computed by piping
the generated input through the rule rather than authored alongside it.

## 1. Motivation

- ARC-AGI-2 ships 1,000 training tasks. Models that overfit to the exact
  grids generalize poorly. Effective training needs *more inputs that
  exercise the same rule*.
- Re-authoring inputs by hand is slow and error-prone (rule drift).
- Re-rolling inputs procedurally is fast and rule-correct *iff* the
  output is computed from the rule, not authored.
- We want **breadth × depth**: many puzzles, each with a wide
  combinatorial space.

## 2. Method

### 2.1 The generator/runner contract

A generator is a single Python module with:

- `GENERATOR_ID`, `TASK_ID` — same content_hash; doubles as the
  directory name.
- `SUMMARY` (one-line) and `INVARIANTS` (constraints inputs must
  obey).
- `AXES` — declared free parameters (`type`, `default`, `valid`).
- `HELPFUL_TEXTURES` and `DEGENERATE_TEXTURES` — input distributions
  that respectively expose and obscure the rule's effect.
- `generate(seed, sample_index, *, difficulty=None, **overrides)` —
  pure function returning a 2D grid.

The runner pipes the generated grid through the puzzle's Racket rule
in a real `#lang racket` subprocess, validates well-formedness, and
returns a `{train: [...], test: [...]}` bundle. Rejected outputs
(crashes, ill-formed grids, identity outputs) are written to
`data/generated/.rejected/<task_id>.jsonl` for diagnosis.

### 2.2 The DSL

374 grid primitives in a single Racket prelude, organized by family
(geometric / color / object / fill / structural / …). Closed
vocabulary — see `docs/CANONICAL_VOCAB.md` for the full set and the
inclusion bar (≥10 corpus uses, no shorter canonical equivalent).

Style guide (`docs/CANONICAL_STYLE.md`) names variables, layout, and
8 idiom-level canonical forms; every form is enforced by a compactor
pass under `scripts/compactor/passes.py`.

### 2.3 Verification gates

- **`scripts/lint_generator.py`** — per-generator structural lint
  (required constants, `generate` signature, AXES well-formedness).
- **`scripts/lint_generators.py`** — bulk lint with smoke test.
- **`scripts/lint_puzzles.py`** — 9 cross-checks on the canonical
  corpus (bank manifests ↔ counts, grid validity, solver output
  matches expected, canonical ↔ DB task_id agreement, …).
- **`scripts/audit_artifact.py`** — release-readiness gate.

## 3. Combinatorial reach

We define a generator's *bounded reach* as the product of cardinalities
across its discrete `AXES`. Float ranges are discretized to 100
buckets; descriptive free-form axes contribute 1 (so the reported
number is a **lower bound**).

Across the corpus:

| metric | value |
|---|---|
| generators | 3,889 |
| total bounded configurations | 2.56 × 10¹¹ |
| with seed budget 1,000 | 2.56 × 10¹⁴ |
| per-generator median | 4.84 × 10⁴ |
| top-1 reach | 8.71 × 10¹⁰ |
| generators with ≥1 unbounded axis | 3,480 / 3,889 |

Reproduce: `python3 scripts/combinatorial_reach.py`.

### 3.1 Per-bank totals (top 5)

| bank | n | total reach |
|---|--:|---:|
| training (ARC) | 539 | 2.17 × 10¹¹ |
| augmented | 461 | 3.52 × 10¹⁰ |
| custom | 30 | 9.59 × 10⁸ |
| arc_puzzle_bank_seventh_21_bundle | 21 | 2.39 × 10⁸ |
| arc_puzzle_bank_nineteenth_21_bundle | 21 | 1.80 × 10⁸ |

(Updated numbers in `docs/COMBINATORIAL_REACH.md`.)

## 4. Identity and provenance

Every puzzle is identified by a 12-character `content_hash` — a
SHA-256 prefix over (train, test). Two puzzles with identical grids
collide on hash by design (dedup signal); the three known collisions
in the corpus are resolved by appending `_2` to the alphabetically-
second pair member. Augmented variants share their parent task's
hash. Bank directories are identified by 12-character hashes of the
bank's canonical name.

## 5. Discussion

### 5.1 Why Racket?

- The rule layer is a small enough DSL that we can fix the vocabulary
  and verify every primitive's semantics. Python rules drift; Racket
  rules don't.
- Real `#lang racket` evaluation gives us `match`, `for/fold`, `hash`,
  the whole standard library, and native compilation under Chez
  Scheme — orders of magnitude faster than a Python S-expression
  interpreter for non-trivial rules.
- A single subprocess per batch amortizes startup; per-pair cost is
  millisecond-scale.

### 5.2 Why generators-not-just-data?

- Static datasets cap at the size you ship. A generator of equivalent
  weight ships the **family**, not a sample.
- Generators expose the *axes that matter* (grid size, palette,
  texture). Models trained over the family learn invariances; models
  trained over a sample memorize.
- Verification is local: run the rule on the generator's output, no
  human in the loop.

### 5.3 Open questions

- **Concept de-duplication.** 86% of canonical concepts have only one
  member under the current canonicalizer. Real concept count is
  lower; better canonicalization would drop singletons substantially.
  Future work: behavioral hashing, equivalence under symmetry group,
  rule rewriting.
- **Difficulty calibration.** ELO is currently 0 for every row; we
  have rough easy/medium/hard tags from puzzle sources. A real
  difficulty signal would let us sample better training mixes.
- **Augmentation breadth.** 461 augmented variants today; the
  generator runner is bottlenecked only by Racket throughput, so the
  practical limit is much higher.

## 6. Reproducibility

```bash
git clone https://github.com/<you>/arc-agi-2-generators
cd arc-agi-2-generators
python3 scripts/regen_all.py    # rebuilds canonical, db, manifests, lint
python3 scripts/combinatorial_reach.py    # the headline number
```

`scripts/audit_artifact.py` prints the release-readiness summary.

## 7. Figures (TBD)

- F1: a worked example — generator code, sample input, Racket rule,
  output grid, with axes annotated.
- F2: per-bank reach distribution (log-log scatter).
- F3: per-generator axis-count histogram.
- F4: rejection-cause breakdown across a 10k-sample run.

## 8. Limitations

- The corpus is a snapshot. Generators are at v1.x; many are
  combinatorially shallow (default ranges narrower than the documented
  `valid` range).
- Reach numbers are bounded — descriptive `valid` strings (e.g.
  `"varied"`, `"sparse"`) contribute 1 instead of their semantic
  cardinality. A small number of hand-fixes would shift the headline
  by ~1–2 orders of magnitude.
- 1 puzzle still ships in the conversion backlog (Python solution
  pending Racket conversion; see `data/derived/conversion_backlog.jsonl`).
