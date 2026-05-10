# Puzzle-Instance Generator Spec

> Contract for `puzzle_generators/per_puzzle/<task_id>/generator.py`.
> Phase 2 of [`PUZZLE_GENERATOR_ROADMAP.md`](PUZZLE_GENERATOR_ROADMAP.md).

A **puzzle-instance generator** produces fresh `(input, output)` pairs
for one ARC puzzle. The output is *derived* — never stored — by piping
the generator's input through that puzzle's already-existing Racket
rule. One source of truth: `output = rule(generate(seed, axes))`.

## Module shape

Every generator module is a Python file at
`puzzle_generators/per_puzzle/<task_id>/generator.py` exporting:

| Symbol           | Type    | Meaning                                                                                                                              |
|------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------|
| `GENERATOR_ID`   | `str`   | Stable identifier. Conventionally equal to `TASK_ID`.                                                                                |
| `VERSION`        | `str`   | Semver (`"1.0.0"`). Bump when output distribution changes; downstream caches key on this.                                            |
| `TASK_ID`        | `str`   | The canonical puzzle this generator produces variants of. Must match a `task_id` in `data/base/solutions/`.                          |
| `CONCEPT_HASH`   | `str` (optional) | The canonical-rule hash from `concept_inventory.py`. Optional as of round-7 audit. Empty string `""` is **worse than absent** (looks filled, conveys nothing) — either fill via `concept_inventory.py` or omit the constant. |
| `SUMMARY`        | `str`   | One-sentence description of what the generator builds.                                                                               |
| `INVARIANTS`     | `list[str]` | Constraints the generator guarantees (used by the LLM author and as runtime asserts where cheap).                                |
| `AXES`           | `dict`  | Free axes the caller can override. Keys are kwarg names; values describe type, default, and validity. See **Axes** below.            |
| `generate(...)`  | `callable` | The actual function. See **Function signature** below.                                                                            |

A `meta.yaml` sibling holds free-form notes (invariant rationale, why
certain axes were chosen) that don't need to live in code. Optional —
the runner doesn't read it.

## Function signature

```python
def generate(
    seed: int,
    sample_index: int,
    *,
    difficulty: str | None = None,
    **overrides,
) -> list[list[int]]:
    """Build one input grid. Output comes from piping through the rule."""
```

- `seed`, `sample_index`: deterministic identity. Same `(seed,
  sample_index, version)` always produces the same grid.
- `difficulty`: `"easy" | "medium" | "hard" | None`. Optional hint;
  generators may ignore it. When set, narrows axis ranges (e.g., easy
  → smaller grids, fewer objects).
- `**overrides`: per-axis overrides (`bg=5, marker_color=2,
  grid_h=12, …`). Anything in `AXES` is a valid kwarg.
- **Returns** the input grid as `list[list[int]]` with values in
  `0..9`, height/width in `[1, 30]`. The runner derives the output by
  calling the puzzle's Racket rule.

The function MUST NOT compute or return the output. The runner owns
that step. This keeps the rule as the single source of truth.

## Axes

`AXES` is a documented contract for what's tweakable. Each entry:

```python
AXES = {
    "bg": {
        "type": "color",
        "default": "rng",
        "valid": "0..9",
        "doc": "Background color of the grid.",
    },
    "rect_color": {
        "type": "color",
        "default": "rng",
        "valid": "0..9 != bg",
        "doc": "Color of the single rectangle.",
    },
    "grid_h": {
        "type": "int",
        "default": "rng 10..14",
        "valid": "5..30",
        "doc": "Grid height.",
    },
    # ...
}
```

Type vocabulary:

| Type       | Meaning                                                |
|------------|--------------------------------------------------------|
| `color`    | A single integer in `0..9`.                            |
| `colors[N]`| Tuple of N distinct colors.                            |
| `int`      | A single integer.                                      |
| `shape`    | An `(h, w)` pair.                                      |
| `rc`       | An `(row, col)` position.                              |
| `bool`     | True/False knob.                                       |
| `enum`     | One of a fixed set of strings.                         |

`AXES` is the **machine-readable** description the LLM author and the
catalog read. The runner uses it to validate overrides ("rect_color is
declared as `0..9 != bg`, you passed 11 — reject").

## GenCtx — the keyed-draw discipline

All randomness goes through `GenCtx` from `puzzle_generators.base`:

```python
from puzzle_generators.base import gen_ctx

def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed, sample_index=sample_index,
        version=VERSION, task_id=TASK_ID,
        difficulty=difficulty, overrides=overrides,
    )
    bg          = ctx.draw_color("bg")
    rect_color  = ctx.draw_color("rect_color", exclude={bg})
    grid_h      = ctx.draw_int("grid_h", 10, 14)
    grid_w      = ctx.draw_int("grid_w", 10, 14)
    # ... build and return a grid
```

**Every random decision uses a label.** The label is hashed against
`(seed, version, task_id)` to seed an independent `random.Random`.
This means:

- Adding/removing/reordering draws cannot affect the values of *other*
  draws. Two generators that both call `ctx.draw_color("bg")` get the
  same `bg` for the same seed regardless of what other draws happen.
- Determinism is portable: `(seed=42, sample_index=3)` produces the
  same grid on any machine, any Python version.
- An override (`bg=5` in kwargs) short-circuits the draw and is
  recorded in `ctx.overrides_used` for provenance.

The `GenCtx` API:

| Method                                                | Returns           |
|-------------------------------------------------------|-------------------|
| `draw_int(label, lo, hi)`                             | `int` in `[lo, hi]` |
| `draw_choice(label, options)`                         | one element of `options` |
| `draw_color(label, *, exclude=set())`                 | `int` in `0..9 \ exclude` |
| `draw_distinct_colors(label, n, exclude=set())`       | `tuple[int, ...]` of length n |
| `draw_grid_size(label, lo, hi)`                       | `(h, w)` |
| `draw_rect_size(label, grid, margin, min_dim)`        | `(rh, rw)` fitting inside grid |
| `draw_rect_position(label, grid, size, margin)`       | `(rr, rc)` such that rect fits with margin |
| `draw_shape(label, options)`                          | one of a list of (rotated/flipped) cell-set shapes |
| `draw_rng(label)`                                     | a `random.Random` for ad-hoc draws inside helpers |

If `label` matches a key in `overrides`, the override value is used
verbatim (after passing the same validity check the random draw
applies). The override is recorded in `ctx.overrides_used`.

## Validation (runner-side)

Every grid the generator returns is validated by the runner before
being included in the batch:

1. **Type:** `list[list[int]]`.
2. **Dimensions:** `1 ≤ h ≤ 30`, `1 ≤ w ≤ 30`, all rows same length.
3. **Values:** every cell in `0..9`.
4. **Non-degenerate input:** at least two distinct colors. (A
   uniform-bg-only grid is almost always a generator bug.)
5. **Rule applies cleanly:** `bridge.eval_text(rule)` returns a grid;
   any error → reject.
6. **Non-degenerate output:** output is not all-bg, and not equal to
   input. (If the rule's purpose is to *not* change the input — rare
   — the generator declares `allow_identity_output: true` in
   `meta.yaml`.)

Rejected instances go to `data/generated/.rejected/<task_id>.jsonl`
with `{seed, sample_index, reason}`. The runner retries up to N times
per requested instance (default N=3) before giving up.

## Reproducibility contract

```python
generate(seed=42, sample_index=3) == generate(seed=42, sample_index=3)  # always True
```

Bitwise identical. Any failure of this contract is a bug — most
commonly caused by:
- Using bare `random.Random()` instead of `ctx.draw_rng(label)`.
- Iterating over a `set()` (Python preserves insertion order for
  dicts, not sets — sort before iterating if order matters).
- Calling external libraries that have their own RNG state.

## Worked example: `952a094c`

Concept: "Inside-corner cells of a single rectangle move diagonally
to opposite outside corners; clear the inside corners."

```python
# puzzle_generators/per_puzzle/952a094c/generator.py
from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "952a094c"
VERSION = "1.0.0"
TASK_ID = "952a094c"
CONCEPT_HASH = "fcd5c4e2d3e9"  # from data/derived/concepts.jsonl
SUMMARY = (
    "A single solid rectangle of one color in a uniform-color grid; "
    "the four inside-corner cells of the rectangle have four distinct "
    "non-rect colors."
)
INVARIANTS = [
    "exactly one solid rectangle of color rect_color",
    "the rectangle's 4 inside-corner cells have 4 distinct non-rect colors",
    "background is uniform color bg, distinct from rect_color and corner colors",
    "rectangle has at least 1 cell of margin from every grid edge",
    "rectangle dimensions: at least 5x5 (so inside corners exist)",
]
AXES = {
    "bg":            {"type": "color",     "default": "rng",            "valid": "0..9"},
    "rect_color":    {"type": "color",     "default": "rng",            "valid": "0..9 != bg"},
    "corner_colors": {"type": "colors[4]", "default": "rng_distinct",   "valid": "0..9 distinct, != bg, != rect_color"},
    "grid_h":        {"type": "int",       "default": "rng 10..14",     "valid": "10..18"},
    "grid_w":        {"type": "int",       "default": "rng 10..14",     "valid": "10..18"},
    "rect_h":        {"type": "int",       "default": "rng 5..h-3",     "valid": ">=5, <= h-2"},
    "rect_w":        {"type": "int",       "default": "rng 5..w-3",     "valid": ">=5, <= w-2"},
    "rect_rr":       {"type": "int",       "default": "rng with margin","valid": "1..h-rect_h-1"},
    "rect_rc":       {"type": "int",       "default": "rng with margin","valid": "1..w-rect_w-1"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    bg          = ctx.draw_color("bg")
    rect_color  = ctx.draw_color("rect_color", exclude={bg})
    corners     = ctx.draw_distinct_colors("corner_colors", n=4,
                                            exclude={bg, rect_color})
    h           = ctx.draw_int("grid_h", 10, 14)
    w           = ctx.draw_int("grid_w", 10, 14)
    rh          = ctx.draw_int("rect_h", 5, h - 3)
    rw          = ctx.draw_int("rect_w", 5, w - 3)
    rr          = ctx.draw_int("rect_rr", 1, h - rh - 1)
    rc          = ctx.draw_int("rect_rc", 1, w - rw - 1)

    g = full_grid(h, w, bg)
    draw_rect(g, rr, rc, rh, rw, rect_color)
    g[rr + 1     ][rc + 1     ] = corners[0]   # top-left inside
    g[rr + 1     ][rc + rw - 2] = corners[1]   # top-right inside
    g[rr + rh - 2][rc + 1     ] = corners[2]   # bottom-left inside
    g[rr + rh - 2][rc + rw - 2] = corners[3]   # bottom-right inside
    return g
```

To produce 50 instances:

```python
from puzzle_generators.runner import run_batch
batch = run_batch("952a094c", n=50, n_train=4, n_test=1)
# batch is a list of {"train": [...], "test": [...]} dicts
```

To produce instances with a fixed background:

```python
batch = run_batch("952a094c", n=50, bg=5)  # all use gray bg
```

## Helper library (`puzzle_generators/helpers/`)

The helpers are minimal — only what 2+ generators want. **Don't add a
helper preemptively.** Lazy growth keeps the API surface small.

### `grid.py`

| Function                              | Purpose                                  |
|---------------------------------------|------------------------------------------|
| `full_grid(h, w, color) -> grid`      | New `h*w` grid filled with `color`.      |
| `clone_grid(g) -> grid`               | Deep copy.                               |
| `draw_rect(g, r, c, rh, rw, color)`   | Mutate: solid rectangle (top-left + h/w). |
| `draw_rect_outline(g, r, c, rh, rw, color)` | Mutate: perimeter cells (top-left + h/w). |
| `fill_box(g, r1, c1, r2, c2, color)`  | Mutate: solid rectangle by **inclusive corners**. Mirrors Racket `(draw-rect-filled g r1 c1 r2 c2 color)`. |
| `draw_frame(g, r1, c1, r2, c2, color)`| Mutate: perimeter by **inclusive corners**. Mirrors Racket `(draw-rect-outline g r1 c1 r2 c2 color)`. |
| `paint_at(g, r0, c0, cells, color)`   | Mutate: stamp `cells` (relative offsets) at `(r0, c0)` with `color`. OOB cells silently skipped. |
| `paint_cells(g, cells, color)`        | Mutate: paint absolute `(r, c)` cells with `color`. |
| `paste(g, sub, r, c)`                 | Mutate: paste `sub` at `(r, c)` in `g`.  |
| `set_cell(g, r, c, v)`                | Mutate: assign one cell.                 |

**Convention.** Two coordinate idioms coexist by design:

- `(r, c, rh, rw)` — top-left + height/width. Used by `draw_rect`,
  `draw_rect_outline`, generator-side rectangle placement.
- `(r1, c1, r2, c2)` — inclusive corner pair. Used by `fill_box`,
  `draw_frame`, and **mirrors the Racket vocabulary** (`obj-bbox`,
  `draw-rect-*`, `subgrid`, `crop`). Prefer this when the calling code is
  parallel to a Racket rule that uses the same corners.

### `palette.py`

| Function                                       | Purpose                          |
|------------------------------------------------|----------------------------------|
| `random_palette(rng, n, exclude)`              | n distinct colors not in `exclude`. |
| `non_bg_colors(bg)`                            | All colors `0..9` except `bg`.   |

### `shape.py`

| Function                              | Purpose                              |
|---------------------------------------|--------------------------------------|
| `rect_cells(rh, rw)`                  | List of `(r, c)` for a solid rectangle (origin 0,0). |
| `rect_outline_cells(rh, rw)`          | Perimeter cells of an `rh × rw` rectangle. |
| `cross_cells(size)`                   | Plus-sign cells.                     |
| `normalize(cells)`                    | Translate so min `(r, c) == (0, 0)`. |

### `place.py`

| Function                                              | Purpose                          |
|-------------------------------------------------------|----------------------------------|
| `random_position(rng, h, w, margin)`                  | `(r, c)` with given margin from edges. |
| `random_free_cell(g, rng, *, bg, max_tries)`          | Random `(r, c)` where `g[r][c] == bg`, or `None`. |
| `place_no_overlap(rng, g, cells, color, *, padding, max_tries)`| Try to place a shape; `padding=1` enforces a 1-cell gap from existing non-bg content (so the new shape stays a separate component under 4-/8-conn). |

The helpers are **pure Python**, never call out to Racket. The Racket
side only sees the final grid via the runner.

## Anti-patterns

### Don't compute the output

```python
# BAD — the rule is the source of truth, not the generator.
def generate(seed, sample_index, **kwargs):
    g = build_input(...)
    out = my_python_reimplementation_of_the_rule(g)  # ← NO
    return {"input": g, "output": out}

# GOOD
def generate(seed, sample_index, **kwargs):
    return build_input(...)  # runner pipes through the Racket rule
```

### Don't bare-`random`

```python
# BAD
import random
n = random.randint(1, 10)  # ← non-reproducible

# GOOD
n = ctx.draw_int("n", 1, 10)
```

### Don't iterate over sets without sorting

```python
# BAD — set iteration order is implementation-defined
for color in {bg, rect_color, *corner_colors}:
    ...

# GOOD
for color in sorted({bg, rect_color, *corner_colors}):
    ...
```

### Don't read the description at runtime

The description is for the LLM author at code-write time. By the time
the generator runs, all that information is encoded as `INVARIANTS`,
`AXES`, and the function body. Never `import` the description.

### Don't re-parameterize the rule

```python
# BAD — the rule is fixed; generators only vary inputs.
def generate(seed, sample_index, **kwargs):
    rule_template = ...  # ← never modify the rule from the generator

# GOOD
def generate(seed, sample_index, **kwargs):
    return build_input_grid(...)
```

(The variant-via-color-substitution path uses `concept_template` to
re-instantiate the rule, but that happens at the **catalog/sampler
level**, not inside `generate`.)

## Authoring checklist

- [ ] `GENERATOR_ID`, `VERSION`, `TASK_ID`, `CONCEPT_HASH`, `SUMMARY` set.
- [ ] `INVARIANTS` lists every constraint the generator guarantees.
- [ ] `AXES` documents every kwarg, with type, default, and valid range.
- [ ] All randomness goes through `ctx.draw_*` — no bare `random.*`.
- [ ] `generate(seed=42, sample_index=3)` is bitwise reproducible.
- [ ] Returns a grid, not a `{train, test}` dict — the runner builds those.
- [ ] 50 instances at default axes: all distinct by `content_hash`.
- [ ] 50 instances: rule round-trips without error on each.
- [ ] Axis-override smoke test: passing `bg=5` produces grids using `bg=5`.

## Related docs

- [`PUZZLE_GENERATOR_ROADMAP.md`](PUZZLE_GENERATOR_ROADMAP.md) — phased plan.
- [`RACKET_DSL.md`](RACKET_DSL.md) — the Racket side (rules).
- [`RACKET_COMMENT_STYLE.md`](RACKET_COMMENT_STYLE.md) — how Racket rules document themselves.
