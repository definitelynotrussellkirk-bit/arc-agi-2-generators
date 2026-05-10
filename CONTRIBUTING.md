# Contributing

Whether you're sharpening one generator, adding a primitive, or
rewriting a Racket rule — this is a corpus, and contributions need
to be locally correct *and* not break the global invariants
(everything has a verified rule, every line of canonical jsonl has
the same fields, etc.).

## Quick local check

```bash
python3 scripts/audit_artifact.py     # release-readiness gate
python3 scripts/lint_puzzles.py       # 9 cross-checks on canonical
python3 scripts/regen_all.py --no-lint   # full pipeline rebuild
```

`scripts/audit_artifact.py` should print `STATUS: PASS` before any
PR. `lint_puzzles.py` should report `9/9 checks passed`.

## Editing one generator

```bash
# Edit, then lint just that file:
python3 scripts/lint_generator.py puzzle_generators/per_puzzle/<hash>/generator.py
```

Module contract is in [docs/PUZZLE_GENERATOR_SPEC.md](docs/PUZZLE_GENERATOR_SPEC.md):

- `GENERATOR_ID`, `VERSION`, `TASK_ID`, `SUMMARY`, `INVARIANTS`,
  `AXES` are required module constants.
- `generate(seed, sample_index, *, difficulty=None, **overrides)` is
  the entry point. Pure: same args → same output.
- `GENERATOR_ID` and `TASK_ID` are equal to the directory name (the
  12-char content_hash).

When changing input distributions (new texture, widened range, etc.)
bump `VERSION` (e.g. `1.1.0 → 1.2.0`) so consumers can pin.

## Editing a Racket rule

Rules live in two places that must stay in sync:

- `solvers/grounded_rules.py` — `GROUNDED_RULES[<content_hash>] =
  "(rule! (lambda (g) ...))"`. This is the rule the runner falls
  back to when no per-puzzle solution JSON is present.
- `data/base/solutions/<bank>/<id>__<hash>.json` — the per-puzzle
  solution JSON. The `racket_target.raw_code` field is the
  authoritative source.

`scripts/sync_bank_solutions.py` reconciles the two. After editing
either, run `regen_all.py` and confirm `lint_puzzles.py` 9/9.

The closed primitive vocabulary is documented in
[docs/CANONICAL_VOCAB.md](docs/CANONICAL_VOCAB.md). Style rules
(naming, layout, idiom-level canonical forms) are in
[docs/CANONICAL_STYLE.md](docs/CANONICAL_STYLE.md).

## Adding a new puzzle generator

1. Pick a `task_id` (12-char content_hash for new puzzles, or the
   ARC-original hash for existing ones).
2. `python3 scripts/scaffold_generator.py <task_id>` to create the
   skeleton.
3. Fill in `INVARIANTS`, `AXES`, `HELPFUL_TEXTURES`,
   `DEGENERATE_TEXTURES`, and the `generate()` body.
4. Run `python3 scripts/lint_generator.py
   puzzle_generators/per_puzzle/<task_id>/generator.py`.
5. End-to-end smoke: `python3 -c "from puzzle_generators import
   runner; print(runner.run_one('<task_id>', seed=0,
   sample_index=0))"`.

## What kinds of contributions are most useful

In rough priority:

1. **Tightening axis `valid` strings** in existing generators. Many
   generators ship `valid: "sparse"` or other free-form descriptive
   tokens that don't parse as cardinality. Replacing them with
   enumerable ranges (e.g. `valid: "1..6"`) tightens the
   combinatorial-reach lower bound — see the
   `unparsed:*` distribution in
   [docs/COMBINATORIAL_REACH.md](docs/COMBINATORIAL_REACH.md).
2. **Deepening generator combinatorial axes**. Many older generators
   (still at `VERSION = "1.0.0"`) have narrow draw ranges relative
   to their declared `valid`. Bumping to `1.1.0+` with widened
   ranges expands reach.
3. **Verified Racket solutions** for the 1 puzzle still in
   `data/derived/conversion_backlog.jsonl`.
4. **Better concept canonicalization** — 86% of canonical concepts
   are singletons under the current canonicalizer; a smarter
   equivalence (under symmetry group, behavioral hashing, etc.)
   would significantly reduce that.

## Code style

- Python: standard library only; no third-party deps in the runner
  path.
- Racket: see `docs/CANONICAL_STYLE.md`. The compactor under
  `scripts/compactor/passes.py` enforces idiom-level forms.
- No unconditional debug prints; use `CallRecorder.record_event` if
  you need traceability inside the runner.

## License

Contributions are accepted under the same terms as the repo:
MIT for code, with attribution to ARC-Prize / upstream sources for
puzzle data. See `LICENSE` and `LICENSES/ARC-AGI-2.md`.
