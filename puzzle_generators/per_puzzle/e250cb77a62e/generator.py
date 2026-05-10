"""Generator for additional_scaffolded:H2.

Rule: a 1-frame holds a 4-pattern that should be stamped at isolated
7 seeds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seeds, seed_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "e250cb77a62e"
VERSION = "1.1.0"
TASK_ID = "e250cb77a62e"
SUMMARY = "A 1-frame holds a 4-pattern that should be stamped at isolated 7 seeds."

INVARIANTS = [
    "background is 0",
    "exactly one 1-colored rectangular frame contains the 4 prototype",
    "prototype cells do not touch the frame border",
    "7 seeds have enough room for the full prototype offsets",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seeds", "seed_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "10..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "frame_top_left",
                       "valid": "frame_top_left"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


PATTERN = [(1, 1), (1, 2), (2, 1), (3, 3)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 14, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    draw_frame(g, 1, 1, 7, 7, 1)
    for dr, dc in PATTERN:
        g[2 + dr][2 + dc] = 4
    anchors = [(9, 2), (9, 8), (h - 5, w - 5)]
    rng.shuffle(anchors)
    for r, c in anchors[:rng.randint(2, 3)]:
        if r + 3 >= h or c + 3 >= w:
            continue
        g[r][c] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 16
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # no 1-frame holding the prototype → stamp source undefined
        for r, c in [(9, 2), (9, 8)]:
            g[r][c] = 7
        return g
    if name == "no_seeds":
        # frame + prototype but no 7 seeds → nothing to stamp
        draw_frame(g, 1, 1, 7, 7, 1)
        for dr, dc in PATTERN:
            g[2 + dr][2 + dc] = 4
        return g
    if name == "seed_at_edge":
        # 7 seed too close to the right/bottom edge → stamp footprint clips out of bounds
        draw_frame(g, 1, 1, 7, 7, 1)
        for dr, dc in PATTERN:
            g[2 + dr][2 + dc] = 4
        g[h - 1][w - 1] = 7
        g[9][2] = 7
        return g
    return g
