"""Generator for ARC task e9afcf9a.

Rule: `(rule! (lambda (g) (grid-from-fn (rows g) (cols g) (lambda (r c) (cell-at g (mod (+ r c) 2) 0)))))`.
For each output cell at (r, c): copy from input cell ((r + c) mod 2, 0).
i.e., the rule alternates between the two first-column colors in a
checker pattern; the rest of the input is decoy.

Combinatorial axes:
  * grid_w              — output width (input is 2 × w)
  * stripe_colors       — the two first-column colors that drive the output
  * decoy_palette_size  — how many distractor colors appear elsewhere
  * decoy_layout        — pattern of decoys: random / blob / stripes /
                          frame / matching_only (only stripe colors)
  * decoy_density       — how covered the non-first-column cells are
  * caller-opt-in degenerates: same_first_col_colors (output ambiguous),
                               empty_decoys (only first column populated),
                               full_decoy (output overrides everything)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9849988fda31"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "9849988fda31"
SUMMARY = "A two-row grid whose first-column colors define an alternating-stripe output."

INVARIANTS = [
    "input has exactly 2 rows",
    "the two first-column colors are distinct",
    "remaining cells are decoys (the rule only reads column 0)",
]

DECOY_LAYOUTS = ("random", "blob", "stripes", "frame", "matching_only", "diagonal")
DEGENERATE_TEXTURES = ("same_first_col_colors", "empty_decoys", "full_decoy")
HELPFUL_TEXTURES = DECOY_LAYOUTS

AXES = {
    "grid_w":            {"type": "int",   "default": "rng 4..15", "valid": "2..30"},
    "decoy_palette_size": {"type": "int",  "default": "rng 0..3",  "valid": "0..6"},
    "decoy_layout":      {"type": "str",   "default": "rng helpful",
                          "valid": "|".join(DECOY_LAYOUTS)},
    "decoy_density":     {"type": "float", "default": "rng 0.3..0.9", "valid": "0..1"},
    "texture":           {"type": "str",   "default": "alias for decoy_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        w_lo, w_hi, p_lo, p_hi = 4, 6, 0, 1
    elif difficulty == "hard":
        w_lo, w_hi, p_lo, p_hi = 12, 15, 2, 3
    else:
        w_lo, w_hi, p_lo, p_hi = 4, 15, 0, 3

    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], w, rng)

    stripe_colors = ctx.draw_distinct_colors(
        "stripe_colors", n=2, exclude={0})
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", p_lo, p_hi)))
    decoy_palette = list(ctx.draw_distinct_colors(
        "decoy_palette", n=max(0, n_decoy),
        exclude={0, stripe_colors[0], stripe_colors[1]}))
    layout = (overrides.get("texture")
              or overrides.get("decoy_layout")
              or ctx.draw_choice("decoy_layout", list(DECOY_LAYOUTS)))
    density = float(overrides.get(
        "decoy_density",
        ctx.draw_rng("decoy_density").uniform(0.3, 0.9)))

    g = full_grid(2, w, 0)
    g[0][0] = stripe_colors[0]
    g[1][0] = stripe_colors[1]

    available = list(decoy_palette) + list(stripe_colors)
    if layout == "random":
        for r in range(2):
            for c in range(1, w):
                if rng.random() < density:
                    g[r][c] = rng.choice(available)
    elif layout == "blob":
        # A solid blob of one decoy color in the middle.
        bw = max(1, int((w - 1) * density))
        c0 = rng.randint(1, max(1, w - bw))
        color = rng.choice(available)
        for r in range(2):
            for c in range(c0, min(w, c0 + bw)):
                g[r][c] = color
    elif layout == "stripes":
        for r in range(2):
            color = available[r % len(available)] if available else 0
            for c in range(1, w):
                if rng.random() < density:
                    g[r][c] = color
    elif layout == "frame":
        for c in range(1, w):
            if available:
                g[0][c] = available[0]
                g[1][c] = available[-1]
    elif layout == "matching_only":
        # Decoys must use the same two stripe colors (so column 0's signal
        # is harder to spot among matching cells elsewhere).
        for r in range(2):
            for c in range(1, w):
                if rng.random() < density:
                    g[r][c] = rng.choice(stripe_colors)
    elif layout == "diagonal":
        for c in range(1, w):
            g[(c) % 2][c] = (rng.choice(available) if available
                              else stripe_colors[c % 2])
    return g


def _draw_from_degenerate(name, w, rng):
    """Edge-case where the first-column-checker signal is hidden.

    same_first_col_colors — both first-column cells share a color, so
                            the output is uniform (no checker visible).
    empty_decoys          — only the first column is populated; rest is
                            bg. Output is the alternating stripe but the
                            decoys carried no information.
    full_decoy            — the rest of the grid is intentionally
                            misleading: rich pattern that the rule
                            ignores. Tests whether the model attends
                            only to column 0.
    """
    g = full_grid(2, w, 0)
    if name == "same_first_col_colors":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[0][0] = c; g[1][0] = c
        for r in range(2):
            for cc in range(1, w):
                g[r][cc] = rng.choice([0, c])
        return g
    if name == "empty_decoys":
        a, b = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
        g[0][0] = a; g[1][0] = b
        return g
    if name == "full_decoy":
        a, b = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
        decoys = [c for c in range(1, 10) if c not in {a, b}]
        rng.shuffle(decoys)
        g[0][0] = a; g[1][0] = b
        for r in range(2):
            for cc in range(1, w):
                g[r][cc] = rng.choice(decoys)
        return g
    return g
