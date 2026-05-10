"""Generator for 87ab05b8.

Rule: find first 2-cell; determine quadrant (h/2, w/2); fill that
quadrant with 2, others with 6.

Combinatorial axes (8): grid_n, two_position, two_quadrant_bias,
n_decorations, decoration_palette_size, decoration_layout,
asymmetry_force, anchor_corner.
Degenerates: no_two, multiple_twos, all_two.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "637229802e6f"
VERSION = "1.1.0"
TASK_ID = "637229802e6f"
SUMMARY = "6-bg grid with one 2-cell; rule fills its quadrant with 2, rest with 6."

INVARIANTS = [
    "background is 6",
    "exactly 1 cell of color 2",
    "rest of cells are 6 or non-{2,6} decoration colors",
]

QUADRANT_BIAS = ("top_left", "top_right", "bottom_left", "bottom_right",
                 "spread", "center")
DECOR_LAYOUTS = ("scattered", "row", "col", "diag", "corners")
DEGENERATE_TEXTURES = ("no_two", "multiple_twos", "all_two")
HELPFUL_TEXTURES = QUADRANT_BIAS

AXES = {
    "grid_n":             {"type": "int", "default": "rng 4..10 even",
                           "valid": "4..14 even"},
    "two_quadrant_bias":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(QUADRANT_BIAS)},
    "two_position_bias":  {"type": "str", "default": "rng spread|center",
                           "valid": "spread|center"},
    "n_decorations":      {"type": "int", "default": "rng 1..4", "valid": "0..6"},
    "decoration_palette_size": {"type": "int", "default": "rng 1..3",
                                "valid": "1..7"},
    "decoration_layout":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(DECOR_LAYOUTS)},
    "anchor_corner":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for two_quadrant_bias",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_choices = [4, 6]
    elif difficulty == "hard":
        n_choices = [10, 12, 14]
    else:
        n_choices = [4, 6, 8, 10]
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        n = rng.choice(n_choices)
        return _draw_from_degenerate(overrides["texture"], n, rng)
    n = int(overrides.get("grid_n", rng.choice(n_choices)))
    if n % 2 == 1:
        n += 1
    n = max(4, min(14, n))
    quadrant_bias = (overrides.get("texture") or
                     overrides.get("two_quadrant_bias")
                     or ctx.draw_choice("two_quadrant_bias",
                                        list(QUADRANT_BIAS)))
    decor_layout = overrides.get("decoration_layout",
                                 ctx.draw_choice("decoration_layout",
                                                 list(DECOR_LAYOUTS)))
    n_decor = int(overrides.get("n_decorations",
                                ctx.draw_int("n_decorations", 1, 4)))
    n_palette = int(overrides.get("decoration_palette_size",
                                  ctx.draw_int("decoration_palette_size",
                                               1, 3)))
    pal_pool = [1, 3, 4, 5, 7, 8, 9]
    rng.shuffle(pal_pool)
    palette = pal_pool[:max(1, n_palette)]
    g = full_grid(n, n, 6)
    pr, pc = _pick_two_position(quadrant_bias, n, rng)
    g[pr][pc] = 2
    decor_cells = _decor_positions(decor_layout, n, n_decor, rng,
                                   exclude={(pr, pc)})
    for r, c in decor_cells:
        if g[r][c] == 6:
            g[r][c] = rng.choice(palette)
    if bool(overrides.get("anchor_corner", False)):
        if g[0][0] == 6:
            g[0][0] = palette[0]
    return g


def _pick_two_position(quad, n, rng):
    h2 = n // 2
    if quad == "top_left":
        return rng.randint(0, h2 - 1), rng.randint(0, h2 - 1)
    if quad == "top_right":
        return rng.randint(0, h2 - 1), rng.randint(h2, n - 1)
    if quad == "bottom_left":
        return rng.randint(h2, n - 1), rng.randint(0, h2 - 1)
    if quad == "bottom_right":
        return rng.randint(h2, n - 1), rng.randint(h2, n - 1)
    if quad == "center":
        return h2 - 1 + rng.randint(0, 1), h2 - 1 + rng.randint(0, 1)
    return rng.randint(0, n - 1), rng.randint(0, n - 1)


def _decor_positions(layout, n, k, rng, exclude):
    cells = [(r, c) for r in range(n) for c in range(n)
             if (r, c) not in exclude]
    if layout == "row":
        r = rng.randint(0, n - 1)
        chosen = [(r, c) for c in range(n) if (r, c) not in exclude]
        return chosen[:k]
    if layout == "col":
        c = rng.randint(0, n - 1)
        chosen = [(r, c) for r in range(n) if (r, c) not in exclude]
        return chosen[:k]
    if layout == "diag":
        diag = [(i, i) for i in range(n) if (i, i) not in exclude]
        return diag[:k]
    if layout == "corners":
        corners = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]
        corners = [c for c in corners if c not in exclude]
        return corners[:k]
    rng.shuffle(cells)
    return cells[:k]


def _draw_from_degenerate(name, n, rng):
    g = full_grid(n, n, 6)
    if name == "no_two":
        for _ in range(3):
            r = rng.randint(0, n - 1); c = rng.randint(0, n - 1)
            if g[r][c] == 6:
                g[r][c] = rng.choice([1, 3, 4, 5, 7, 8, 9])
        return g
    if name == "multiple_twos":
        g[1][1] = 2; g[n - 2][n - 2] = 2
        return g
    if name == "all_two":
        for r in range(n):
            for c in range(n):
                g[r][c] = 2
        return g
    return g
