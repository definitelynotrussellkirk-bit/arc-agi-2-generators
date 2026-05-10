# Canonical-Form Style Guide

> Companion to [`PUZZLE_GENERATOR_SPEC.md`](PUZZLE_GENERATOR_SPEC.md)
> and (when 0006 lands) `CANONICAL_VOCAB.md`. This file specifies
> the *style* a Racket rule must be in to be considered canonical
> — everything beyond "which primitives are allowed."

## Why this exists

The compactor (`scripts/compactor/`) makes style choices implicitly
through its rewrite passes. This doc makes them **explicit**, so:

1. A new rule written from scratch starts in canonical form.
2. Generators emit `RACKET_RULE` already-canonical so codex isn't
   re-running the compactor on every commit.
3. Future Claude / Codex / user can reach for a rule decision and
   find the answer in one place.

The bar for being in this doc: **every choice here is enforced by
at least one compactor pass**, so running a corpus rule through
the compactor is the executable version of "make this canonical."

## Hard rules

### 1. The body sits naked — no `(rule! …)` wrapper, no `(lambda (g) …)`

**Canonical:**
```scheme
(recolor-cells g (find-color g 5) 8)
```

**Not canonical:**
```scheme
(rule! (lambda (g) (recolor-cells g (find-color g 5) 8)))
```

**Why:** the runner re-applies the wrapper. Including it in the
canonical form duplicates context the model doesn't need to learn.

**Enforced by:** `scripts.compactor.passes.pass_strip_outer_rule_lambda`.

### 2. No re-binding of `g` / `h` / `w` to their auto-bound values

`g`, `h = (rows g)`, `w = (cols g)` are auto-bound by the runner.
Don't redeclare them.

**Canonical:**
```scheme
(grid-from-fn h w (lambda (r c) (at g r c)))
```

**Not canonical:**
```scheme
(let ((h (rows g)) (w (cols g)))
  (grid-from-fn h w (lambda (r c) (at g r c))))
```

**Why:** wastes 5 atomic tokens per rule and teaches the model a
preamble that's never useful.

**Enforced by:** `pass_strip_outer_rule_lambda` strips both the
`let*` form and the `(define h …)` form.

### 3. Always `(at g r c)`, never `(cell-at g r c)`

`at` is the canonical name; `cell-at` is a deprecated alias.

**Enforced by:** `pass_alias_cell_at`.

### 4. Always `(!= a b)`, never `(not (= a b))`

**Why:** 920+ corpus occurrences of `(not (= …))`. The shorter
form saves 2 atomic tokens per call and reads more directly.

**Enforced by:** `pass_not_eq`.

### 5. Always `(zero? x)`, never `(= x 0)` or `(= 0 x)`

`zero?` is a Racket built-in; canonical for the equality-with-zero
test.

**Enforced by:** `pass_zero_pred`.

### 6. `let*` over `let`; flatten nested lets

Always use `let*`. Always flatten nested let-with-single-body into
one `let*` with concatenated bindings.

**Canonical:**
```scheme
(let* ((a 1) (b 2) (c 3)) BODY)
```

**Not canonical:**
```scheme
(let ((a 1)) (let ((b 2)) (let ((c 3)) BODY)))
```

**Why:** a let where bindings don't cross-reference is semantically
equivalent to `let*`. Always-`let*` removes one degree of freedom
the model would otherwise have to learn.

**Enforced by:** `pass_flatten_let`.

### 7. `(unless X Y)` not `(when (not X) Y)`

**Enforced by:** `pass_when_not_to_unless`.

### 8. `(if X Y #f)` → `(and X Y)`; `(if (not X) Y Z)` → `(if X Z Y)`

Boolean-shape if-statements get peephole-rewritten.

**Enforced by:** `pass_if_to_and`, `pass_if_not_swap`.

## Idiom-level canonical forms

These are the "phrase words" — multi-token equivalents that all
collapse to a single primitive.

### Cell-list paint with one constant color

```scheme
(recolor-cells g cells COLOR)         ; canonical
```
Enforced by `pass_recolor_cells`. Replaces both `reduce` and
`foldl` variants of `(set-cell …)` over a cell list.

### Object-level paint by per-object color

```scheme
(paint-objects-by g objs (lambda (obj) COLOR-EXPR))   ; canonical
```
Enforced by `pass_paint_objects_by`. Handles direct, conditional-
skip (`#f` skips), and `let*`-prefixed forms.

### Cell-fill from per-cell function

```scheme
(cellmap g (r c v) BODY)              ; canonical (same-size out)
(build-grid H W (r c) BODY)           ; canonical (different size)
```
Enforced by `pass_cellmap`, `pass_map_grid`, `pass_build_grid`.
Replaces `(grid-from-fn (rows g) (cols g) …)` and `(map-grid g …)`.

### Color dispatch on a single cell value

```scheme
(casev v {0 X 1 Y 3 Z} default)       ; canonical
```
Enforced by `pass_casev`. Replaces `(cond ((= v 0) X) …)`. Only
fires when all RHS are atoms.

### Bbox destructure

```scheme
(with-bbox obj (r1 c1 r2 c2) BODY)    ; canonical
```
Enforced by `pass_with_bbox`. Replaces the 5-line
`(let* ((bb (obj-bbox obj)) (r1 …)))` preamble.

### Min/max of a mapped list

```scheme
(min-of FN LST)                       ; canonical
(max-of FN LST)
```
Enforced by `pass_min_max_of`. Replaces `(min-list (map FN LST))`.

### First/count over filter

```scheme
(find-first PRED LST)                 ; canonical
(count-if  PRED LST)
```
Enforced by `pass_first_filter`, `pass_count_if`. Replace
`(first (filter …))` and `(length (filter …))`.

## Lambda binder name conventions

These are not (yet) enforced by the compactor — they're authorial.
Style is to follow them when writing new rules so the model learns
one naming pattern per role.

| Idiom                           | Binder convention |
|---------------------------------|-------------------|
| `cellmap`                       | `(r c v)`         |
| `build-grid`                    | `(r c)`           |
| `paint-objects-by` color-fn     | `(obj)`           |
| `recolor-cells` / cell folds    | `p` (the cell)    |
| `for_each_object`-style fold    | `(obj acc)` (foldl order) |
| Generic accumulator             | `(acc x)` (reduce order) |
| Object loop variable            | `obj`             |
| Inner cell loop variable        | `cell` or `p`     |
| Coordinate components           | `r c` (row, col)  |
| Color value at a cell           | `v`               |
| Object's color                  | `oc`              |
| Object's bbox                   | `bb`              |

## Layout

### Whitespace

- **Source files** (`solvers/grounded_rules.py`, generator
  `RACKET_RULE`): pretty-print, multi-line, indented for human
  reading. Comments allowed.
- **Training data**: minified single-line, no comments. The
  compactor's `emit()` already produces single-line; the shard
  builder strips line comments via the runner's pipeline.

### Comments

- **Source comments are good.** Briefly describe the pattern (5–15
  words). They help future agents reading the prelude.
- **Training comments are bad.** They train the model to write
  comments — wasted token budget. The shard builder strips them
  unconditionally.

```scheme
;; recolor 5→8 inside the largest red object's bbox
(with-bbox (largest-object-of-color g 2) (r1 c1 r2 c2)
  (recolor-cells g (cells-in-rect r1 c1 r2 c2) 8))
```

In source: keep the leading comment.
In training data: emit only the s-expr.

## What the compactor does NOT enforce yet (future style work)

- **Binder name normalization.** Today the compactor preserves
  whatever the source used; it doesn't alpha-rename to canonical
  binders. If we want the model to see `(r c v)` *every* time and
  never `(i j x)`, add a pass.
- **Expression ordering for commutative ops.** `(+ a b)` vs
  `(+ b a)` — semantically identical but syntactically distinct.
  Current compactor preserves source order.
- **Number literal canonicalization.** `(/ 1 2)` vs `0.5` — pick
  one for the same value? Open question.

When one of these matters, the right move is: file a proposal in
`tasks/PROPOSALS/open/`, get sign-off, add the pass, update this
doc.

## Idempotency check

After running the compactor, running it AGAIN should produce zero
changes. If it doesn't, that's a bug — either the compactor is
non-deterministic or one pass is undoing another's work.

```bash
python3 -m scripts.compactor.run --quiet
# inspect data/derived/compactor_report.jsonl: every record's
# "passes_applied" should be empty on the second run.
```

(Today this isn't quite true — `strip_outer` for example fires
on the source form even after compactor has already produced the
naked-body form, because we re-load the source from
`solvers/grounded_rules.py` rather than the previously-compacted
output. A round-trip mode for the compactor would close this gap.
File when needed.)
