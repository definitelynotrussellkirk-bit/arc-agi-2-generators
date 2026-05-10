"""Generator for arc_puzzle_bank_21_set18_s:S18_H1 — sort/select panels by metric.

Rule: panels separated by full color-9 row. Each panel has a colored motif;
the rule sorts/selects them by a metric.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_markers, all_below_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b86607f34b8b"
VERSION = "1.1.0"
TASK_ID = "b86607f34b8b"

SUMMARY = "3-4 single-cell markers in distinct non-{0, 9} colors at distinct columns + 1 9-row divider."

INVARIANTS = [
    "background is 0",
    "exactly one full color-9 row (the divider)",
    "above the divider: 3-4 markers in distinct non-{0, 9} colors at distinct columns",
    "below the divider: a few colored cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_markers", "all_below_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "9row_divider_with_markers",
                       "valid": "9row_divider_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        n = ctx.draw_int("n", 3, 4)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    div = h // 2
    for c in range(w): g[div][c] = 9
    # markers above
    cols = rng.sample(range(w), n)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], n)
    for c, color in zip(cols, colors):
        r = rng.randint(0, div - 1)
        g[r][c] = color
    # cells below
    for _ in range(rng.randint(2, 4)):
        for _t in range(40):
            r = rng.randint(div + 1, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice(colors)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # markers but no 9-row divider → can't split above/below
        for r, c in [(1, 2), (1, 5), (5, 2)]: g[r][c] = 4
        return g
    if name == "no_markers":
        # only divider, no markers → nothing to sort or select
        for c in range(w): g[3][c] = 9
        return g
    if name == "all_below_divider":
        # markers all below divider → no above content to compare against
        for c in range(w): g[3][c] = 9
        for r, c in [(5, 2), (5, 5), (6, 2)]: g[r][c] = 4
        return g
    return g
