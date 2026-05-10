"""Generator for 19b:m129 — apply upward gravity in each walled chamber.

Rule: an 8-rectangular border + 1-2 internal full-height 8-walls form
chambers. Inside each chamber, all non-bg cells fall upward.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_walls, all_at_top.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ed98575459d2"
VERSION = "1.1.0"
TASK_ID = "ed98575459d2"
SUMMARY = "Rectangular 8-frame + 1-2 internal vertical 8-walls + scattered pebbles."

INVARIANTS = [
    "background is 0",
    "outer rectangle is solid 8",
    "1-2 full-height internal vertical 8-walls span row 0 to row h-1",
    "each chamber has 1-3 scattered non-bg pebbles, none in row 1 (so input != output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_walls", "all_at_top")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "frame_with_internal_walls",
                       "valid": "frame_with_internal_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    # outer frame
    for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h): g[r][0] = 8; g[r][w - 1] = 8
    # internal walls
    n_walls = rng.randint(1, 2)
    walls = rng.sample(range(3, w - 3), n_walls)
    walls.sort()
    for c in walls:
        for r in range(h): g[r][c] = 8
    edges = [0] + walls + [w - 1]
    palette = [1, 2, 3, 4, 5, 6, 7, 9]
    for i in range(len(edges) - 1):
        c_lo, c_hi = edges[i] + 1, edges[i + 1] - 1
        if c_hi < c_lo: continue
        n = rng.randint(1, 3)
        placed = 0; attempts = 0
        while placed < n and attempts < 30:
            attempts += 1
            r = rng.randint(2, h - 2)
            c = rng.randint(c_lo, c_hi)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice(palette); placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # No outer 8-frame — chamber boundaries are undefined.
        g[3][3] = 4; g[5][7] = 5
        return g
    if name == "no_walls":
        # Frame but no internal walls — single chamber, no chamber-by-chamber gravity.
        for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h): g[r][0] = 8; g[r][w - 1] = 8
        g[4][3] = 4; g[5][7] = 5
        return g
    if name == "all_at_top":
        # Pebbles already at row 1 — gravity-up is a no-op (input == output).
        for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h): g[r][0] = 8; g[r][w - 1] = 8
        for r in range(h): g[r][6] = 8
        g[1][3] = 4; g[1][9] = 5
        return g
    return g
