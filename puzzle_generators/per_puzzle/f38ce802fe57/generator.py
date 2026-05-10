"""Generator for arc_additional_puzzle_bank_volume7:M45.

Rule: a colored seed flood-fills its reachable zero chamber inside gray
walls.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seed_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_walls, sealed_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f38ce802fe57"
VERSION = "1.1.0"
TASK_ID = "f38ce802fe57"
SUMMARY = "A colored seed flood-fills its reachable zero chamber inside gray walls."

INVARIANTS = [
    "background is 0",
    "gray cells form chamber walls",
    "there is exactly one non-wall colored seed",
    "the seed's chamber contains reachable background cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_walls", "sealed_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_color":     {"type": "int", "default": "rng 2..8", "valid": "2..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "left_chamber",
                       "valid": "left_chamber"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "walled", "valid": "walled"},
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
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    wall_c = rng.randint(3, w - 4)
    gap = rng.randint(2, h - 3)
    for r in range(1, h - 1):
        if r != gap:
            g[r][wall_c] = 5
    color = rng.choice([2, 3, 4, 6, 7, 8])
    seed_r = rng.randint(1, h - 2)
    seed_c = rng.randint(1, wall_c - 1)
    g[seed_r][seed_c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # walls but no seed → flood-fill has no source
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(1, h - 1):
            g[r][w // 2] = 5
        return g
    if name == "no_walls":
        # seed but no walls → flood-fill spreads to entire grid
        g[h // 2][w // 2] = 4
        return g
    if name == "sealed_chamber":
        # seed in a fully sealed chamber → fill is just the seed cell, no expansion possible
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(1, h - 1):
            g[r][3] = 5
        # fill the chamber completely with walls leaving only seed cell
        for r in range(1, h - 1):
            for c in range(1, 3):
                if r != 2 or c != 1:
                    g[r][c] = 5
        g[2][1] = 4
        return g
    return g
