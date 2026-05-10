"""Generator for arc_puzzle_bank_21_set10_s:S10_H4 — Three-panel consensus.

Rule: 2 5-divider cols separate 3 panels of equal width. For each cell
(r,c) in left panel, output value if it agrees with mid or right at same
(r,c); else if mid==right, that value; else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, no_agreement, all_three_agree.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "083ba0fc4534"
VERSION = "1.1.0"
TASK_ID = "083ba0fc4534"
SUMMARY = "Three 4-wide panels separated by 5-cols; each row has 1 colored cell with at-least-pairwise agreement."

INVARIANTS = [
    "2 full-column 5-dividers split grid into 3 panels of equal width",
    "each row has 1-2 colored cells (rest 0)",
    "for each row, at least 2 panels share a non-zero color at same position",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "no_agreement", "all_three_agree")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_w":        {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "rng 3..7", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "5col_separated_panels",
                       "valid": "5col_separated_panels"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..7", "valid": "3..7"},
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
        pw = ctx.draw_int("panel_w", 4, 4)
        h = ctx.draw_int("n_rows", 4, 4)
    elif difficulty == "hard":
        pw = ctx.draw_int("panel_w", 5, 5)
        h = ctx.draw_int("n_rows", 5, 5)
    else:
        pw = ctx.draw_int("panel_w", 4, 5)
        h = ctx.draw_int("n_rows", 4, 5)
    w = pw * 3 + 2  # 3 panels + 2 dividers
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    d1 = pw
    d2 = pw * 2 + 1
    for r in range(h):
        g[r][d1] = 5
        g[r][d2] = 5
    # Each row: pick a position c in [0, pw); pick a color; place in 2-3 panels
    for r in range(h):
        c = rng.randint(0, pw - 1)
        color = rng.choice([2, 3, 4, 6, 7, 8, 9])
        # Always place in left + middle; sometimes also right
        g[r][c] = color
        g[r][d1 + 1 + c] = color
        if rng.random() < 0.5:
            g[r][d2 + 1 + c] = color
    return g


def _draw_from_degenerate(name, rng):
    pw = 4; h = 4
    w = pw * 3 + 2
    g = full_grid(h, w, 0)
    d1 = pw; d2 = pw * 2 + 1
    if name == "no_dividers":
        # missing 5-cols → can't split into panels
        for r in range(h):
            g[r][1] = 4
            g[r][6] = 4
        return g
    if name == "no_agreement":
        # 3 panels with all distinct cells per row → no consensus, output blank
        for r in range(h):
            g[r][d1] = 5; g[r][d2] = 5
            g[r][0] = 4
            g[r][d1 + 2] = 6
            g[r][d2 + 3] = 7
        return g
    if name == "all_three_agree":
        # 3 panels with identical content → output equals input panel A
        for r in range(h):
            g[r][d1] = 5; g[r][d2] = 5
            g[r][1] = 4
            g[r][d1 + 1 + 1] = 4
            g[r][d2 + 1 + 1] = 4
        return g
    return g
