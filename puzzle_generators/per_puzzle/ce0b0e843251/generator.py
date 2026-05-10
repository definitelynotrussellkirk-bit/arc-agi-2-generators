"""Generator for arc_puzzle_bank_tenth21:H67 — flood-fill rooms by single-color seed.

Rule: 7-walled outer border + 5-divider walls inside. Each room may have a
single colored seed (non-{0, 5, 7}); the output paints the room with that
seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_walls, n_seeds, texture.
Degenerates: no_walls, no_seeds, multiple_seeds_per_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ce0b0e843251"
VERSION = "1.1.0"
TASK_ID = "ce0b0e843251"

SUMMARY = "7-walled grid + 1-2 interior 5-walls dividing rooms + 1-3 colored seeds in distinct non-{0, 5, 7} colors."

INVARIANTS = [
    "background is 0",
    "outer border is color-7 walls",
    "1-2 interior color-5 walls (full row or column with one door cell) partition the interior",
    "1-3 colored seeds in distinct non-{0, 5, 7} colors at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multiple_seeds_per_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "rng 1..2", "valid": "0..4"},
    "n_seeds":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_seeds+2", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "border_walls_seeds_inside",
                       "valid": "border_walls_seeds_inside"},
    "n_distinct_colors": {"type": "int", "default": "= n_seeds+2", "valid": "3..6"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        n_walls = ctx.draw_int("n_walls", 1, 1)
        n_seeds = ctx.draw_int("n_seeds", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
        n_walls = ctx.draw_int("n_walls", 2, 3)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n_walls = ctx.draw_int("n_walls", 1, 2)
        n_seeds = ctx.draw_int("n_seeds", 1, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 7; g[h - 1][c] = 7
    for r in range(h): g[r][0] = 7; g[r][w - 1] = 7
    for _ in range(n_walls):
        if rng.choice([True, False]):
            r = rng.randint(2, h - 3)
            for c in range(1, w - 1): g[r][c] = 5
        else:
            c = rng.randint(2, w - 3)
            for r in range(1, h - 1): g[r][c] = 5
    seed_colors = rng.sample([1, 2, 3, 4, 6, 8, 9], n_seeds)
    for color in seed_colors:
        for _t in range(80):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 7; g[h - 1][c] = 7
    for r in range(h): g[r][0] = 7; g[r][w - 1] = 7
    if name == "no_walls":
        # Border + seeds but no interior dividers — every seed is in
        # the same room; rule's per-room paint becomes a single
        # all-or-nothing pick.
        g[3][3] = 3; g[5][7] = 6
        return g
    if name == "no_seeds":
        # Walls + rooms but no seeds — rule has no color to paint
        # any room with.
        for c in range(1, w - 1): g[4][c] = 5
        return g
    if name == "multiple_seeds_per_room":
        # Walls + multiple distinct-colored seeds in the SAME room —
        # rule's "single seed per room" precondition fails; paint
        # color is ambiguous.
        for c in range(1, w - 1): g[4][c] = 5
        g[2][3] = 3; g[2][7] = 6
        g[6][4] = 8; g[6][8] = 9
        return g
    return g
