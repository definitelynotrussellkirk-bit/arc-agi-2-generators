"""Generator for 4b:m28 — fill bboxes with key color.

Rule: a single key cell at corner. Each blob's bbox is filled with
the key color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_blobs, all_solid_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "1ff8b33b4e5f"
VERSION = "1.1.0"
TASK_ID = "1ff8b33b4e5f"
SUMMARY = "Single key cell + 2-3 distinct-color non-rectangular blobs."

INVARIANTS = [
    "background is 0",
    "exactly one isolated key cell at a corner",
    "2-3 non-rectangular blobs in different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_blobs", "all_solid_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "key_corner_plus_blobs",
                       "valid": "key_corner_plus_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    g[0][w - 1] = palette[0]
    used = {(0, w - 1), (0, w - 2), (1, w - 1)}
    for color in palette[1:]:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=20)
            if cells is None: continue
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            bb_h = max(rs) - min(rs) + 1; bb_w = max(cs) - min(cs) + 1
            if bb_h * bb_w == len(cells): continue
            bbox = {(r, c) for r in range(min(rs), max(rs) + 1) for c in range(min(cs), max(cs) + 1)}
            if bbox & used: continue
            for r, c in cells: g[r][c] = color
            used |= bbox
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blobs but no key cell → no fill color defined
        g[3][3] = 4; g[3][4] = 4; g[4][4] = 4
        g[6][7] = 6; g[7][7] = 6
        return g
    if name == "no_blobs":
        # key only → nothing to fill
        g[0][w - 1] = 5
        return g
    if name == "all_solid_rects":
        # blobs are already solid rects → bbox-fill is identity-recolor
        g[0][w - 1] = 5
        for r in range(2, 4):
            for c in range(1, 4): g[r][c] = 4
        for r in range(5, 7):
            for c in range(6, 9): g[r][c] = 6
        return g
    return g
