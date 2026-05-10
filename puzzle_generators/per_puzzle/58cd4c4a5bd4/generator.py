"""Generator for arc_additional_puzzles_21_set8:E50.

Rule: find the full-height 5-column (or full-width 5-row); mirror each
non-{0, 5} cell across that divider.

Combinatorial axes (8): grid_h, grid_w, palette_kind, num_marks,
divider_col, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_divider, divider_partial, no_marks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "58cd4c4a5bd4"
VERSION = "1.1.0"
TASK_ID = "58cd4c4a5bd4"
SUMMARY = "Full-height 5-col divider in middle; left side has scattered non-5 cells."

INVARIANTS = [
    "exactly 1 full-height col of 5s",
    "left side has 2-3 isolated non-{0,5} cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_divider", "divider_partial", "no_marks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_marks":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "divider_col":    {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "left_half",
                       "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3",
                          "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
    w = 9
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    gc = 4
    for r in range(h):
        g[r][gc] = 5
    palette = [1, 2, 3, 4, 6, 7, 8, 9]
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, gc - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # marks but no 5-line — rule has no axis to mirror over
        g[1][2] = 4
        g[2][1] = 7
        g[3][3] = 6
        return g
    if name == "divider_partial":
        # 5-column has gaps — not a full-height divider
        for r in [0, 2, 4]:
            g[r][4] = 5
        g[1][2] = 4
        g[3][1] = 7
        return g
    if name == "no_marks":
        # divider but no marks to mirror — rule has nothing to do
        for r in range(h):
            g[r][4] = 5
        return g
    return g
