"""Generator for arc_additional_puzzle_bank_volume20:M135 — reflect 7s across an 8 divider.

Rule: a full 8 row or column is a mirror line; 7 markers are copied
to the reflected side.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_seven, seven_on_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b6543be4517"
VERSION = "1.1.0"
TASK_ID = "8b6543be4517"
SUMMARY = "A full 8 row or column is a mirror line; 7 markers are copied to the reflected side."

INVARIANTS = [
    "there is exactly one full divider row or column of color 8",
    "7 cells lie off the divider and have in-bounds reflections",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_seven", "seven_on_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..17"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "str", "default": "rng row|col", "valid": "row|col"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "divider_with_marker_set",
                       "valid": "divider_with_marker_set"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 9, 13)
    orient = ctx.draw_choice("orientation", ["row", "col"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if orient == "col":
        mid = w // 2
        for r in range(h):
            g[r][mid] = 8
        for r, c in [(1, 1), (h - 3, 2), (h // 2, max(1, mid - 3))]:
            g[r][c] = 7
    else:
        mid = h // 2
        for c in range(w):
            g[mid][c] = 8
        for r, c in [(1, 1), (2, w - 3), (max(1, mid - 3), w // 2)]:
            g[r][c] = 7
    if rng.random() < 0.4:
        g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # 7 markers but no full 8-row/col → no mirror line defined
        g[2][1] = 7
        g[5][3] = 7
        g[7][8] = 7
        return g
    if name == "no_seven":
        # 8-divider exists but no 7 markers → nothing to reflect
        for c in range(w): g[5][c] = 8
        return g
    if name == "seven_on_divider":
        # 7 cells sit on the divider itself → reflection is the same cell (no copy)
        for c in range(w): g[5][c] = 8
        g[5][2] = 7   # on divider
        g[5][7] = 7   # on divider
        return g
    return g
