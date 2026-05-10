"""Generator for arc_additional_puzzle_bank_volume6:M39.

Colored objects slide rightward until they pack against a gray wall.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_wall, no_objects, objects_at_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e5ead55c33e7"
VERSION = "1.1.0"
TASK_ID = "e5ead55c33e7"
SUMMARY = "Colored objects slide rightward until they pack against a gray wall."

INVARIANTS = [
    "background is 0",
    "there is a full-height gray wall column",
    "movable objects are colors 2, 3, or 4 and start left of the wall",
    "objects have clear space to move right before settling",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_wall", "no_objects", "objects_at_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "wall_with_left_objects",
                       "valid": "wall_with_left_objects"},
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
        w = ctx.draw_int("grid_w", 9, 11)
        n_objects = ctx.draw_int("n_objects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        n_objects = ctx.draw_int("n_objects", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 15)
        n_objects = ctx.draw_int("n_objects", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    wall = w - 1
    for r in range(h):
        g[r][wall] = 5
    rows = list(range(0, h, 2))
    rng.shuffle(rows)
    colors = [2, 3, 4]
    for i, r in enumerate(rows[:n_objects]):
        color = colors[i % len(colors)]
        c = rng.randint(0, max(0, wall - 5))
        shape = [(r, c)]
        if r + 1 < h and i % 2 == 0:
            shape.append((r + 1, c))
        elif c + 1 < wall - 1:
            shape.append((r, c + 1))
        for rr, cc in shape:
            g[rr][cc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    wall = w - 1
    if name == "no_wall":
        # objects without gray wall → nothing to pack against
        g[1][2] = 2; g[1][3] = 2
        g[3][1] = 3
        return g
    if name == "no_objects":
        # wall alone → nothing to slide
        for r in range(h):
            g[r][wall] = 5
        return g
    if name == "objects_at_wall":
        # objects already touching wall → slide is identity
        for r in range(h):
            g[r][wall] = 5
        g[1][wall - 1] = 2; g[1][wall - 2] = 2
        g[3][wall - 1] = 3
        return g
    return g
