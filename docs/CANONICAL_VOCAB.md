# Canonical Racket Vocabulary

> The closed primitive set the model trains on. Companion to
> [`CANONICAL_STYLE.md`](CANONICAL_STYLE.md) (which covers *how* to
> use these — variable names, layout, comment policy).

## Status

**Draft v1 — 2026-04-27.** The list below is the proposed frozen
set, derived from `data/derived/head_frequency.jsonl` (head counts
across all 5270 canonical rules — 924 training + 4347 bank). Bar
for inclusion: appears in **≥10 rules** AND has no clear shorter
canonical equivalent.

This list will be ratified through reviewer feedback (round 5
bundle when ready). Until ratified, treat it as the **target**
vocab — new rules should be writeable using only these heads, and
adding anything else should go through `tasks/PROPOSALS/`.

## How to read this list

Each section groups primitives by family. For each, we note:

- **name** — the canonical head spelling
- **type** — special form, arithmetic, list-op, grid-op, …
- **count** — corpus head count (rough, post-compactor when
  available)
- one-line semantics

When two equivalent forms exist, the **canonical** one is in this
list; the alias is in [`CANONICAL_STYLE.md`](CANONICAL_STYLE.md)'s
peephole rules section so the compactor knows to rewrite.

## Family: special forms (Racket / always allowed)

| name | semantics |
|------|-----------|
| `lambda` | function literal |
| `define` | top-level or internal definition |
| `let` | parallel bindings (allowed; compactor may rewrite to `let*`) |
| `let*` | sequential bindings (canonical) |
| `let-values` / `letrec` | rare; allowed for advanced needs |
| `loop` | named-let recursion: `(let loop ((i 0)) …)` |
| `in-range` / `in-list` / `in-naturals` | for-loop iterators |
| `if` | 3-arm conditional |
| `cond` / `else` | multi-arm dispatch |
| `when` | one-arm conditional (no else branch) |
| `unless` | when-not (canonical for `(when (not X))`) |
| `begin` | sequence multiple statements |
| `quote` / `'` | literal data |
| `set!` | mutation (rare; only for accumulator patterns) |
| `for` / `for*` / `for/list` / `for/sum` / `for/and` / `for/or` / `for/first` / `for/fold` | comprehensions |
| `match` | pattern dispatch (used in expert-algorithm rules) |

## Family: predicates / boolean

| name | semantics |
|------|-----------|
| `=` `!=` `<` `<=` `>` `>=` | numeric comparison |
| `and` / `or` / `not` | boolean combinators |
| `zero?` | `(= n 0)` — canonical |
| `null?` | empty list test |
| `empty?` | empty list/grid/sequence |
| `equal?` | structural equality |
| `eq?` | identity equality (rare) |
| `pair?` / `list?` | type predicates |
| `member` / `member?` | list containment |
| `any?` / `all?` | shortcut for ormap/andmap |
| `in-bounds?` | `(in-bounds? r c h w)` — corpus's grid bounds check |

## Family: arithmetic

| name | semantics |
|------|-----------|
| `+` `-` `*` `/` | basic ops (note: `/` is integer for ints, see CLAUDE.md gotchas) |
| `quotient` `remainder` `modulo` `mod` | integer division family |
| `abs` `min` `max` | scalar |
| `floor` `ceiling` `round` | rounding |
| `expt` `sqrt` | power / root |
| `inexact->exact` `exact->inexact` | type coercion |

## Family: list basics

| name | semantics |
|------|-----------|
| `list` | construct a list |
| `cons` | prepend / dotted-pair construct |
| `car` / `cdr` | destructure cons (canonical for cons cells) |
| `first` / `second` / `third` / `fourth` | indexed access (canonical for proper lists) |
| `nth` | `(nth lst i)` — list-ref alias |
| `rest` | tail of a list |
| `length` | list length |
| `append` | concatenate |
| `reverse` | reverse |
| `range` | `(range A B)` — half-open integer range |
| `map` | apply fn over list |
| `filter` | keep elements matching predicate |
| `reduce` | left fold (`(reduce fn init lst)`) |
| `foldl` | left fold (Racket-native; same as reduce with arg order swapped) |
| `apply` | apply fn to list-of-args |
| `sort` / `sort-by` | sort (canonical: `sort-by` for keyed) |
| `unique` | dedup |
| `flatmap` | `(flatmap fn lst)` — `(apply append (map fn lst))` |
| `find-first` | first element matching predicate (canonical for `(first (filter ...))`) |
| `find` | alias of `find-first` |
| `count-if` | count elements matching predicate |
| `min-list` / `max-list` | min/max of a list (canonical for `(apply min …)`) |
| `min-of` / `max-of` | `(min-of fn lst)` (canonical for `(min-list (map fn lst))`) |
| `index-of` | position of element in list |
| `take` / `drop` | prefix / suffix slicing |
| `last` | last element |

## Family: hash

| name | semantics |
|------|-----------|
| `make-hash` / `make-immutable-hash` | construct a hash |
| `hash-ref` | look up key (with optional default) |
| `hash-set!` | mutate (rare; use immutable when possible) |
| `hash-has-key?` | membership |

## Family: cell-level grid access

| name | semantics |
|------|-----------|
| `at` | `(at g r c)` — canonical (alias `cell-at` is rewritten) |
| `set-cell` | `(set-cell g r c v)` — functional update |
| `rows` / `cols` | grid dimensions |
| `cell-up` / `cell-down` / `cell-left` / `cell-right` | neighbor cell (with optional oob default) |
| `safe-at` | bounds-checked at |
| `grid-positions` | list of all (r c) lists in the grid |
| `positions-in-rect` | (r c) list for a rectangle |

## Family: per-cell construction

| name | semantics |
|------|-----------|
| `cellmap` | `(cellmap g (r c v) BODY)` — same-size per-cell map (canonical) |
| `map-grid` | alias of cellmap (rewritten) |
| `build-grid` | `(build-grid H W (r c) BODY)` — different-size construction |
| `grid-from-fn` | underlying function form (compactor rewrites to cellmap or build-grid) |
| `casev` | `(casev v {0 X 1 Y …} default)` — color/value dispatch |
| `empty-grid` | `(empty-grid h w fill)` — uniform grid |

## Family: color / palette queries

| name | semantics |
|------|-----------|
| `find-color` | `(find-color g c)` — list of (r . c) cons pairs |
| `count-color` | count cells of one color |
| `grid-colors` | distinct colors in grid |
| `mode` | most common value (excluding bg) |
| `mode-list` | most common value in a list |
| `recolor` | `(recolor g old new)` — replace one color |
| `recolor-map` | bulk remap via dict |
| `swap-colors` | swap two colors |
| `remove-color` | replace one color with bg |
| `keep-only` | inverse of remove-color |

## Family: cell-list mass paint

| name | semantics |
|------|-----------|
| `recolor-cells` | `(recolor-cells g cells C)` — paint cells with one color |
| `paint-cells` | accepts (r c) or (r c v) cells |
| `erase-cells` | paint to bg |
| `paint-cells-from` | paint a sub-region into another grid |

## Family: object-level

| name | semantics |
|------|-----------|
| `objects` | 4-connected components |
| `objects-8` | 8-connected components |
| `objects-multicolor` | multicolor connected components |
| `obj-bbox` | `(r1 c1 r2 c2)` |
| `obj-cells` | list of (r . c) cells |
| `obj-color` | dominant color |
| `obj-size` | cell count |
| `obj-r1` / `obj-c1` / `obj-r2` / `obj-c2` | bbox accessors |
| `obj-h` / `obj-w` | bbox dimensions |
| `obj-rs` / `obj-cs` | row / col coord lists |
| `with-bbox` | `(with-bbox obj (r1 c1 r2 c2) BODY)` — destructure macro |
| `paint-objects-by` | `(paint-objects-by g objs (lambda (obj) C-or-#f))` — per-object color paint with skip-on-#f |
| `paint-objects` | constant-color variant |
| `pick-max` / `pick-min` | argmax/argmin over a list by key fn |
| `largest-object` / `smallest-object` | shortcuts |
| `objects-where` / `objects-of-color` / `objects-by-color` | filter helpers |
| `same-shape?` | shape-equal (color-blind) |
| `bordering?` | object touches outer border |
| `obj-contact` | which side of obj1 touches obj2 |

## Family: geometric transforms

| name | semantics |
|------|-----------|
| `flip-lr` / `flip-ud` | mirror |
| `rotate-cw` / `rotate-ccw` / `rotate-180` | quarter-turn rotations |
| `transpose` | swap rows/cols |
| `crop` / `subgrid` | rectangular slice |
| `crop-to-content` | trim bg-only borders |
| `crop-object` | crop to one object's bbox |
| `pad-grid` / `pad-grid-asym` | add bg border |
| `upscale` / `downscale` | resize by integer factor |
| `tile` / `self-tile` | tiling |
| `kaleidoscope` | 4-fold reflection |

## Family: paint shapes / lines

| name | semantics |
|------|-----------|
| `paint-line` | line between two points |
| `paint-ray` | ray from a point in a direction |
| `ray-cells` | cell list along a ray |
| `connect-points` | path between two cells |
| `connect-same-color-pairs` | bulk paired connections |
| `line-cells` | cell list of a line |
| `draw-line` / `draw-rect` / `draw-cross` | shape drawing |

## Family: fill / flood

| name | semantics |
|------|-----------|
| `flood-fill` | bucket fill from seed |
| `bucket-fill` / `bucket-fill-8` | aliases for flood-fill |
| `fill-enclosed` / `fill-all-enclosed` | fill interior bg regions |
| `fill-holes` | fill holes in objects |
| `fill-frame-interiors` | bulk frame-interior fill |
| `fill-color` | replace one color globally |

## Family: physics / motion

| name | semantics |
|------|-----------|
| `gravity` | slide non-bg cells in a direction |
| `slide-color` / `slide-object` / `slide-until-contact` | targeted slides |
| `move-to-wall` | slide until edge |
| `smear-color` | `(smear-color g color dir)` — extend cells along a direction |

## Family: structural detection

| name | semantics |
|------|-----------|
| `full-rows` / `full-cols` | rows/cols entirely one non-bg color |
| `frontiers` | divider rows / cols |
| `internal-separators` | non-border all-bg rows/cols |
| `cell-grid` | decompose by separators |
| `detect-period` | translational period |
| `detect-translational-period` | tuple `(dr dc)` form |
| `detect-mirror-symmetry` | which axes are mirror-symmetric |
| `detect-rotational-symmetry` | 4 / 2 / 1 |
| `bbox-of-cells` | bbox of an arbitrary cell list |
| `holes-of-object` | bg cells inside an object's bbox |
| `solid-rect?` / `hollow-frame?` | shape tests |

## Family: pathfinding

| name | semantics |
|------|-----------|
| `bfs-path` | shortest path between two cells |
| `bfs-fill-path` | paint the path |
| `connected-region` | BFS expand by predicate |
| `flood-from` | bucket fill (alternate name) |

## Family: segments / runs

| name | semantics |
|------|-----------|
| `gap-runs` / `row-segments` / `col-segments` | run-length decomposition |

## Family: deltas / neighbors (shared constants)

| name | semantics |
|------|-----------|
| `cardinal-deltas` | `'((-1 0)(1 0)(0 -1)(0 1))` |
| `diagonal-deltas` | `'((-1 -1)(-1 1)(1 -1)(1 1))` |
| `all-8-deltas` | union |
| `neighbors-4` / `neighbors-8` | values at adjacent cells |

## Estimated total

Counting the entries above: roughly **~190 primitives + ~15 special
forms = ~205 vocabulary heads.** Inside the 12@200 budget the round-1
review proposed.

## What's NOT in this list (and why)

- **Aliases** that the compactor canonicalizes away:
  `cell-at` → `at`, `not-= → !=`, `(not (member …))` → `(not-member …)` if added,
  `(when (not X))` → `(unless X)`, `(if X Y #f)` → `(and X Y)`,
  `(if (not X) A B)` → `(if X B A)`. See `CANONICAL_STYLE.md`.
- **Local binders** (`r`, `c`, `v`, `p`, `acc`, `obj`, `bb`, `cur`, …)
  that show up in the head-frequency catalogue but are variable
  references, not primitives.
- **Niche helpers** used in <10 rules. Either inlined into the rule
  or filed as a proposal if they recur as the corpus grows.

## Procedure for additions

If you (claude or codex) need a primitive that's not on this list:

1. **Don't hack around it.** Add a `tasks/PROPOSALS/open/PNNNN-…md`
   per the proposal protocol (see `tasks/PROPOSALS/README.md`).
2. **Park the affected work** until decided — mark the task with
   "Parked-for-proposal: PNNNN".
3. **Bar for acceptance**: ≥3 puzzles' worth of evidence that the
   primitive is reusable, and the alternative-without-it is hacky
   (verbose / brittle / non-compositional / would teach the model
   bad style).

We want **GREAT** Racket, not vocabulary bloat.

## Procedure for removals

If a primitive on this list turns out to be redundant or too niche:

1. File a proposal: "Remove `<name>` because …".
2. List the rules that use it; show that they can be re-expressed
   with other primitives.
3. If accepted, update this doc + add a compactor pass that rewrites
   uses to the replacement.

## Open questions for round-5 reviewer

(For when this is bundled into a feedback round.)

1. **Are the family groupings clear enough**, or should we re-group
   (e.g., by skill: detection / synthesis / transformation) instead
   of by data type?
2. **Should aliases live in this doc** (with `→` arrows to canonical)
   so a reader can see the full surface area, or stay in
   CANONICAL_STYLE.md as we have it?
3. **What's the right cap?** Currently ~205. The reviewer's 12@200
   suggests aiming for fewer phrases on top of a 200-vocab. We're
   at the size; is this small enough?
4. **Compactor enforcement**: should the lint reject rules using
   out-of-vocab heads, or just warn? Hard reject means every new
   primitive needs a proposal cycle; warn means drift is possible.
   Lean towards: hard reject for grounded_rules.py + canonical
   bank rules, warn for in-flight code in feature branches.
