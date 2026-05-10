"""Generator for arc_additional_puzzle_bank_volume18:M120 -- marker-vector move.

Rule: move the red object by the blue→green vector, erase source, recolor source to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, no_markers, zero_vector.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "91e59d47f6b5"
VERSION = "1.1.0"
TASK_ID = "91e59d47f6b5"
SUMMARY = "Move the red object by the blue-to-green vector, erase the source, and recolor it 8."

INVARIANTS = [
    "there is one 4-connected red object",
    "blue and green singleton markers define an in-bounds translation vector",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "no_markers", "zero_vector")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "delta":          {"type": "choice", "default": "rng small cardinal/diagonal",
                       "valid": "in-bounds vector"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "object_with_markers",
                       "valid": "object_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = (
    ((0, 0), (1, 0), (1, 1)),
    ((0, 0), (0, 1), (1, 1), (2, 1)),
    ((0, 1), (1, 0), (1, 1), (1, 2)),
)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 12, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    dr, dc = rng.choice([(0, 2), (2, 0), (1, 2), (-1, 2), (2, -1), (-2, 1)])
    cells = list(rng.choice(SHAPES))
    max_r = max(r for r, _ in cells)
    max_c = max(c for _, c in cells)
    min_r = max(1, 1 - dr)
    min_c = max(1, 1 - dc)
    max_top = min(h - max_r - 2, h - max_r - dr - 2)
    max_left = min(w - max_c - 2, w - max_c - dc - 2)
    if max_top < min_r or max_left < min_c:
        dr, dc = 1, 1
        min_r, min_c = 1, 1
        max_top = h - max_r - dr - 2
        max_left = w - max_c - dc - 2
    r0 = rng.randint(min_r, max_top)
    c0 = rng.randint(min_c, max_left)
    g = full_grid(h, w, 0)
    for rr, cc in cells:
        g[r0 + rr][c0 + cc] = 2

    br = rng.randint(1, h - abs(dr) - 2)
    bc = rng.randint(1, w - abs(dc) - 2)
    if dr < 0:
        br -= dr
    if dc < 0:
        bc -= dc
    g[br][bc] = 1
    g[br + dr][bc + dc] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_red":
        # Markers but no red object — rule has nothing to move.
        g[3][3] = 1; g[5][5] = 3
        return g
    if name == "no_markers":
        # Red object but no markers — vector undefined; rule's
        # translate step has no input.
        for r, c in [(3, 3), (4, 3), (4, 4)]: g[r][c] = 2
        return g
    if name == "zero_vector":
        # Markers coincide (delta = 0,0) — rule's translation is
        # identity; output equals input minus source erased to 8.
        g[3][3] = 1; g[3][3] = 3
        for r, c in [(6, 6), (7, 6), (7, 7)]: g[r][c] = 2
        return g
    return g
