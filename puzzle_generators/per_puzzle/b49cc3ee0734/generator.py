"""Generator for arc_additional_puzzle_bank_volume2:M11.

The red marker selects the side whose object is mirrored across a gray divider.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_divider, no_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b49cc3ee0734"
VERSION = "1.1.0"
TASK_ID = "b49cc3ee0734"
SUMMARY = "The red marker selects the side whose object is mirrored across a gray divider."

INVARIANTS = [
    "background is 0",
    "there is exactly one full gray divider row or column",
    "the red marker is on the source side",
    "source-side non-marker cells reflect in bounds and preserve color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_divider", "no_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "str", "default": "rng vertical|horizontal",
                       "valid": "vertical|horizontal"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "marker_plus_object_one_side",
                       "valid": "marker_plus_object_one_side"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    vertical = rng.choice([True, False])
    shape = [(0, 0), (0, 1), (1, 0)]
    if vertical:
        d = rng.randint(3, w - 4)
        for r in range(h):
            g[r][d] = 5
        c_min = max(1, 2 * d - (w - 1))
        r0 = rng.randint(1, h - 3)
        c0 = rng.randint(c_min, d - 3)
        g[r0][max(0, c0 - 1)] = 2
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = 7
    else:
        d = rng.randint(3, h - 4)
        for c in range(w):
            g[d][c] = 5
        r_min = max(1, 2 * d - (h - 1))
        r0 = rng.randint(r_min, d - 3)
        c0 = rng.randint(1, w - 3)
        g[max(0, r0 - 1)][c0] = 2
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # divider + object without red marker → which side is source ambiguous
        for r in range(h):
            g[r][4] = 5
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][1 + dc] = 7
        return g
    if name == "no_divider":
        # marker + object without gray divider → no axis to mirror across
        g[2][3] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][1 + dc] = 7
        return g
    if name == "no_object":
        # divider + marker but no object to mirror
        for r in range(h):
            g[r][4] = 5
        g[2][3] = 2
        return g
    return g
