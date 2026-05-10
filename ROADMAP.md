# Roadmap

What's done, what's next, and what kinds of help would move things
forward fastest. **Use this as the entry point for picking up a
contribution thread.**

## Done

- 3,889 per-puzzle generators, one per canonical puzzle.
- Verified Racket rules: 4,349 / 4,350 puzzles (one residual in the
  conversion backlog).
- Runner pipes generator output through Racket and validates every
  produced (input, output) pair.
- Combinatorial-reach calculator: **2.56 × 10¹¹** bounded
  configurations, **2.56 × 10¹⁴** with seed budget 1,000.
- 9 lint passes (canonical ↔ DB consistency, schema, solver
  output, vocab, racket style, descriptions, …) — all green.
- Closed primitive vocabulary (374 grid ops in a single Racket
  prelude) + style guide + compactor.
- Per-puzzle metadata DB (`data/canonical/puzzle_db.jsonl`) with
  difficulty tags, primitive sets, content hashes, slugs.

## Open work, by impact

### High impact (each is a multi-day workstream)

1. **Tighten axis `valid` strings.** Across the corpus, ~5,500 axes
   carry free-form descriptive tokens (`"sparse"`, `"varied"`, etc.)
   that the reach calculator can't parse as cardinality. Replacing
   them with enumerable ranges or pipe-list choices would raise the
   combinatorial-reach lower bound by an estimated 1–2 orders of
   magnitude. See the `unparsed:*` distribution in
   [docs/COMBINATORIAL_REACH.md](docs/COMBINATORIAL_REACH.md).
   *Bottleneck: per-generator manual review with a small amount of
   judgment per generator.*

2. **Deepen older generators (v1.0.0 → v1.1.0+).** A subset still
   ships with narrow default draw ranges relative to their declared
   `valid`. Bumping default ranges + adding texture variety
   (`HELPFUL_TEXTURES` / `DEGENERATE_TEXTURES`) deepens the per-
   generator combinatorial space without changing the rule.
   *Bottleneck: same as above, but with a clearer
   what-to-do-per-generator pattern.*

3. **Concept canonicalization.** 86% of canonical concepts (under
   the current canonicalizer) are singletons. The real concept
   count is likely 10–100× lower. Better canonicalization (under
   symmetry group, behavioral hashing, rule rewriting equivalences)
   would expose meaningful clusters and let us sample training
   mixes that hit unique concepts rather than over-represented
   ones.

4. **SFT / training pipeline release.** Currently scoped out of this
   release. The full SFT corpus build + training scripts are
   internal. Repackaging them as a follow-up release would let
   teams reproduce a baseline trained on this corpus.

### Medium impact

5. **The 1 conversion-backlog puzzle.** One canonical row still
   ships with a Python-only solution (`needs_conversion: true`).
   Hand-port to Racket; verify with `lint_puzzles.py`.

6. **Difficulty calibration.** ELO is currently 0 for every row;
   we have rough easy/medium/hard tags from puzzle sources, but
   no data-driven difficulty signal. Adding one would let
   training mixes be sampled by difficulty.

7. **Augmentation breadth.** 461 augmented variants today (one per
   ARC training task that has them). Generator runner is bottlenecked
   only by Racket throughput; the practical limit is much higher.
   Mass-augmentation runs that respect each generator's
   `DEGENERATE_TEXTURES` cap-at-one rule would yield a much larger
   training set.

### Low-hanging cleanup

8. `lint_generators.py` is slow (~5+ minutes for full corpus).
   Speed-up opportunities: caching parsed AXES, parallelizing the
   per-file checks, or tightening the smoke-test radius.

9. README/docs polish — standard pre-paper-submission pass: figures,
   citations, related-work section.

## What kind of teammate would help most

In rough priority:

- **Strong on training / SFT / RL.** You know how to take a corpus
  this size and turn it into a model that scores on ARC-AGI-2.
  You'd own the training-pipeline side.

- **Strong on inference scaffolding.** Test-time RL, MCTS over the
  Racket DSL, swarm orchestration, candidate dihedral-vote selection.
  You'd own how the model uses its training to score on test inputs.

- **Strong writer / experimentalist for the paper.** You'd own
  the paper-track submission, figure design, and ablations against
  RE-ARC / ARC-GEN.

- **Strong Racket / DSL person.** You'd own further rule
  canonicalization, vocab tightening, the compactor, and the
  primitive set itself.

If you're interested, see [README.md](README.md) for project
overview and contact info.
