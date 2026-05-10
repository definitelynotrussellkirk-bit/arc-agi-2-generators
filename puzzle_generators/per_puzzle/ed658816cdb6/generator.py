"""Generator for arc_puzzle_bank_fifteenth21:M102 — keep nearest blob to 9-anchor.

Rule: a 9-anchor + multiple non-9 blobs. Keep only the blob whose
center is closest to the anchor (Manhattan distance, distinct distances).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_blobs, all_equidistant.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ed658816cdb6"
VERSION = "1.1.0"
TASK_ID = "ed658816cdb6"
SUMMARY = "9-anchor + 3 distinct-color blobs at strictly distinct distances from anchor."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell (the anchor)",
    "3 distinct-color blobs at strictly distinct Manhattan distances (no ties)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_blobs", "all_equidistant")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "anchor_plus_distinct_distance_blobs",
                       "valid": "anchor_plus_distinct_distance_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _man(p, cells):
    return min(abs(p[0] - r) + abs(p[1] - c) for r, c in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    anchor = (rng.randint(2, h - 3), rng.randint(2, w - 3))
    g[anchor[0]][anchor[1]] = 9
    used = {anchor}
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8], 3)
    distances = set()
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
            if cells is None:
                continue
            d = _man(anchor, cells)
            if d in distances or d == 0:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            distances.add(d)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # blobs but no 9-anchor → no reference point for nearest selection
        g[2][2] = 4; g[2][3] = 4
        g[6][7] = 6; g[6][8] = 6
        return g
    if name == "no_blobs":
        # anchor only → nothing to keep or remove
        g[5][5] = 9
        return g
    if name == "all_equidistant":
        # all blobs at same distance from anchor → ambiguous nearest
        g[5][5] = 9
        g[2][5] = 4  # distance 3
        g[5][2] = 6  # distance 3
        g[5][8] = 7  # distance 3
        return g
    return g
