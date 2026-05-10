"""Generator for arc_puzzle_bank_21_set18_s:S18_E3 — corner marker picks closure axis.

Rule: a corner marker chooses row or column closure for the remaining
cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, axis,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_pairs, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fda98b5c7670"
VERSION = "1.1.0"
TASK_ID = "fda98b5c7670"
SUMMARY = "A corner marker chooses row or column closure for the remaining cells."

INVARIANTS = [
    "cell (0,0) is the axis marker",
    "marker 2 means row closure; any other marker means column closure",
    "source endpoints never use the marker cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_pairs", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "axis":           {"type": "str", "default": "rng row|col", "valid": "row|col"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "marker_with_three_pairs",
                       "valid": "marker_with_three_pairs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    axis = ctx.draw_choice("axis", ["row", "col"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = 2 if axis == "row" else 3
    if axis == "row":
        rows = rng.sample(range(1, h), 3)
        for idx, r in enumerate(rows):
            c1 = rng.randint(1, w - 4)
            c2 = rng.randint(c1 + 2, w - 1)
            g[r][c1] = 4 + idx
            g[r][c2] = 4 + idx
    else:
        cols = rng.sample(range(1, w), 3)
        for idx, c in enumerate(cols):
            r1 = rng.randint(1, h - 4)
            r2 = rng.randint(r1 + 2, h - 1)
            g[r1][c] = 4 + idx
            g[r2][c] = 4 + idx
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # endpoint pairs but (0,0) is bg → no axis specified
        g[2][1] = 4; g[2][6] = 4
        g[5][2] = 6; g[5][7] = 6
        return g
    if name == "no_pairs":
        # marker but no endpoint pairs → nothing to close
        g[0][0] = 2
        return g
    if name == "mismatched_endpoints":
        # row pairs use different colors → "same color" precondition fails
        g[0][0] = 2
        g[2][1] = 4; g[2][6] = 6
        g[5][2] = 7; g[5][7] = 8
        return g
    return g
