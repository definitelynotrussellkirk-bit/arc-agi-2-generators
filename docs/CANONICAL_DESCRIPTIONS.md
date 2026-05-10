# Canonical Rule Descriptions

> The closed style + vocabulary for the natural-language rule
> descriptions that ship with every puzzle. Companion to
> [`CANONICAL_VOCAB.md`](CANONICAL_VOCAB.md) (Racket primitives) and
> [`CANONICAL_STYLE.md`](CANONICAL_STYLE.md) (Racket layout).

## Status

**Draft v1 — 2026-04-30.** Derived from auditing ~35 sampled
descriptions across `data/base/solutions/banks/.../description_target.target_text`
and `data/canonical/puzzles.jsonl`'s `written_solution` field. The
existing corpus does **not** uniformly follow this guide — it is the
target form for new descriptions and the migration target for old
ones (separate task).

## Why this matters

The `describe_rule` SFT task type trains the model to produce these
descriptions. Inconsistent style + vocabulary forces the model to
learn many surface forms of the same content, wasting capacity on
phrasing variance instead of the underlying transformation. Mixed
color references (`blue` vs `1` vs `blue(1)`) are the worst offender:
the model can't tell whether `red(2)` and `2` mean the same thing
without re-deriving it every time.

## Core principles

1. **Every description is a function of the puzzle.** The same image
   maps to *exactly one* canonical description. This is what makes
   `describe_rule` a learnable SFT target: the model's loss is well-
   defined only when the target is a deterministic function of the
   input.

2. **Many puzzles → one description.** Two puzzles that implement the
   same rule (e.g. one bank's `recolor blue→red` and another bank's
   `recolor blue→red` with different grid sizes) **must** receive the
   same description. The describe-pass is many-to-one. Surface
   variation in puzzles should collapse to identical canonical text.

3. **Descriptions describe transformations, not pixels.** Two puzzles
   with different pixel layouts but the same rule share a description.
   Two puzzles with identical pixels but different rules (rare —
   essentially never happens in this corpus) would split.

4. **No ambiguity.** A description that admits multiple Racket
   implementations is malformed. If you find yourself writing "or
   equivalently …", the description is doing two jobs — pick the
   simpler form and rewrite.

## The five-slot template

Every description is composed from up to five slots, **in this fixed
order**:

| slot | purpose | when to include |
|------|---------|-----------------|
| `SCENE`  | What's in the grid (structures, layout, separators). Not actions. | Whenever the layout is non-trivial. Skip for "find every X" rules where the scene is just "objects on a black background". |
| `KEY`    | Header/legend region encoding parameters (markers, codes, lookup tables). | Only if such a region exists. |
| `SELECT` | Which object(s) or region the action operates on. | Whenever the action targets a subset. |
| `ACTION` | The transform. Numbered steps if more than one. | Always. |
| `OUTPUT` | What's preserved/discarded. | Only if non-default (default = "leave non-affected cells unchanged" for in-place rules; "blank grid otherwise" for build-from-scratch rules). |

### Tiny rules collapse

A rule that only does one thing is `ACTION` only:

> ACTION: rotate the entire square grid 90° clockwise

A rule that does one thing to one set of cells is `SELECT` + `ACTION`:

> SELECT: every all-zero row
> ACTION: delete; keep remaining rows in original order

### Multi-step rules use numbered ACTION

> ACTION:
> 1) normalize each component to its bbox top-left
> 2) rotate the blue(1) component per cell[1]
> 3) combine with op per cell[0]

### Slot labels in the output text

The shipped description does **not** literally contain the labels
`SCENE:`, `KEY:`, etc. — those are an authoring scaffold. The final
text is just clean prose, **in the slot order**. The labels are
restored only when the description is graded by the consistency
linter (see `scripts/lint_descriptions.py`, future work).

Example final form:

> Top row has two control cells; below it a red(2) shape and a blue(1)
> shape. cell[0] is op (3 → union, 4 → intersection, 6 → xor, 7 →
> red-minus-blue; default xor). cell[1] is rotation (1 → none, 2 → 90°
> cw, 3 → 180°, 4 → 270° cw; default none). Take the first red(2) and
> first blue(1) component in row-major order. Normalize to bbox top-
> left, rotate the blue shape per cell[1], combine with op per
> cell[0]. Output the result on a minimal cyan(8) grid.

## Canonical vocabulary

**The vocabulary itself lives in [`ARC_REFERENCE.md`](ARC_REFERENCE.md)
(generated from `docs/arc_reference.jsonl`).** Look terms up there. The
linter (`scripts/lint_descriptions.py`) reads the same DB, so any
vocabulary added to the JSONL becomes a lint rule on the next run with
no Python changes.

The shape of this section used to be a full set of inline tables —
colors, transforms, lookup-arrow, distance metrics, etc. — duplicating
the DB. Those tables have been removed; everything you would have
looked up here has a corresponding entry in the reference. Specifically:

- **Colors** — every color has its own entry under [Colors](ARC_REFERENCE.md#colors). Always use `name(N)` form (`blue(1)`, `red(2)`, …).
- **Transforms** — the dihedral group of 8 transforms is under [Transforms (dihedral)](ARC_REFERENCE.md#transforms-dihedral). Canonical names: `identity`, `90° clockwise`, `90° counter-clockwise`, `180°`, `flip horizontal`, `flip vertical`, `transpose`, `anti-transpose`.
- **Lookup / key encoding** — use arrow form `1 → identity, 2 → 90° clockwise, …` (entries under [Phrases](ARC_REFERENCE.md#phrases)).
- **Distance metrics** — under [Distance metrics](ARC_REFERENCE.md#distance-metrics): `Manhattan distance`, `Chebyshev distance`, `Euclidean distance`, `BFS step count`.
- **Object / structural vocabulary** — [Objects / components](ARC_REFERENCE.md#objects-components) for `component`, `multicolor component`, `frame`, `solid rectangle`, `exemplar`, `template`, `instance`, etc.
- **Quantifiers** — [Selection & quantification](ARC_REFERENCE.md#selection-quantification) for `every`, `the unique`, `the largest by <measure>`.
- **Directions** — [Directions](ARC_REFERENCE.md#directions). `up`/`down`/`left`/`right` only.
- **Symmetry & axes** — [Symmetry](ARC_REFERENCE.md#symmetry).
- **Periodicity** — [Periodicity & tiling](ARC_REFERENCE.md#periodicity-tiling).
- **Geometric primitives, set operations, search algorithms, color operations** — each has its own section in the reference.
- **Output framing** — [Output framing](ARC_REFERENCE.md#output-framing).
- **Mazes & enclosed regions** — [Mazes & enclosed regions](ARC_REFERENCE.md#mazes-enclosed-regions).

When in doubt: open `ARC_REFERENCE.md` in your editor (or grep
`docs/arc_reference.jsonl`) and look up the term. If a term you need
isn't there, add an entry — that one edit becomes both a doc update
and a lint rule.

The remainder of this file covers *how* to assemble vocabulary terms
into a description: the slot template, examples, length budget, and
migration notes. <!-- old vocabulary tables removed in favor of the DB
on 2026-04-30; see commit history for the prior content. -->

## Worked examples

### Tiny rule

Bad: `Output only the smallest rectangle that contains all nonzero cells.`

Canonical:
> Crop to the bbox of all non-background cells.

(Replaces `smallest rectangle that contains all nonzero` → `bbox of
all non-background cells`.)

### Find-and-recolor

Bad: `Find every blue connected component that forms a solid filled
rectangle. Recolor exactly its four corner cells to red(2) and leave
all other cells unchanged.`

Canonical:
> Every blue(1) component that is a solid rectangle. Recolor its four
> corner cells to red(2). Leave the rest unchanged.

(Reorders to SELECT → ACTION → OUTPUT. Drops "exactly", which is
implied. Uses `solid rectangle` from vocab.)

### Control-encoded

Bad (445 chars): `Sort the blue(1) components by size from smallest to
largest. The number of red(2) markers chooses which rank to take. The
number of green(3) markers chooses the transform: 1 = identity, 2 =
90° rotation, 3 = 180° rotation, 4 = left-right mirror. Normalize the
chosen component to its own bounding box, apply the selected
transform, then stamp it with its top-left corner at the cyan(8)
target. Output only the stamped orange(7) shape.`

Canonical:
> Sort blue(1) components by size, smallest first. The number of red(2)
> markers picks the rank; the number of green(3) markers picks the
> transform (1 → identity, 2 → 90° clockwise, 3 → 180°, 4 → flip
> horizontal). Normalize the chosen component to its bbox top-left,
> apply the transform, then stamp it at the cyan(8) target,
> recolored to orange(7). Output the stamped shape on a blank grid.

(`KEY` is now a single line with arrow form; `ACTION` is a clear
sequence; `OUTPUT` is one terse phrase.)

### Multi-step

Bad: `Read the two nonzero key colors from the first row and find the
components of those colors below. Crop both components to their
bounding boxes, rotate the second crop 90° clockwise, and align the
two crops at the same top-left corner on a canvas large enough for
both.`

Canonical:
> First row holds two key colors. Find the component below for each.
> ACTION:
> 1) crop both components to their bbox
> 2) rotate the second crop 90° clockwise
> 3) align both at the same top-left on a canvas big enough for both
> 4) cells from only the first → first color; only the second → second
>    color; overlap → cyan(8).

(Numbered steps for >2 actions. Final step encodes the cell-mixing
rule cleanly.)

### Many-to-one — worked example

These three puzzles are the same rule on different grid sizes /
colors / object counts. They MUST share a canonical description:

- Puzzle A: 5×5 grid, two blue(1) cells, output two red(2) cells at
  the mirrored positions across the vertical axis.
- Puzzle B: 12×12 grid, fifteen blue(1) cells, same operation.
- Puzzle C: 7×7 grid, three magenta(6) cells, recolored to green(3)
  at mirrored positions.

Canonical (shared):
> Every non-background cell is mirrored across the vertical axis and
> recolored to the rule's output color. Leave the original cells
> unchanged.

Surface details (grid size, count of cells, exact in/out colors) are
**not** in the description — the model reads them off the image. The
description encodes the *function*. If two puzzles differ only in
those surface details, their descriptions are byte-identical.

When two puzzles share a canonical description, generators may produce
many image instances per description — that is the desired ratio.

## Length budget

Target: **≤ 280 tokens** for ~90% of descriptions. Multi-step
control-encoded puzzles can run to ~450 tokens. Strict cap: **600
tokens** — anything longer is a sign of either nested structure that
should be flattened or repetition that should be shared via vocab.

Tokens are counted with `tiktoken.cl100k_base`, the same encoding
used by the corpus length lint (`scripts/lint_descriptions.py`). It
is a stable, model-independent proxy.

## Migration

This guide is the target. Existing 2,889 descriptions in the corpus
were authored before it. Migration is a separate task — proposed:

1. Write `scripts/lint_descriptions.py` that grades each description
   against the rules above (color form, transform names, lookup
   arrow, slot order). Report-only, no edits.
2. Use the linter's coverage to triage: which descriptions are
   already close, which need full rewrites.
3. Migrate per-bank, per-batch, with smoke comparing the
   `describe_rule` SFT outputs before vs after.

The model trained on the **current** corpus inherits its
inconsistency. Re-training after migration should reduce phrasing
variance and improve generalization.

## Where this guide lives

Source: `docs/CANONICAL_DESCRIPTIONS.md` (this file).
Referenced from:
- `swarm/prompts/sft/describe_rule.md` (the SFT prompt — should
  eventually instruct the model to follow this guide).
- `swarm/prompts/sft/write_solution.md` (`{{description}}` is the
  canonical-form description being consumed).
- `scripts/lint_descriptions.py` (future).

When this guide changes, bump the `Status` line's version + date.
