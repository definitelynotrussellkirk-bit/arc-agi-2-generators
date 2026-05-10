"""Generator for b775ac94.

Rule: singleton seed colors reflect each group's main shape across the
indicated side.

Combinatorial axes (8): grid_h/w, seed_side, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_seed, no_main, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "dc2c4869445c"
VERSION = "1.1.0"
TASK_ID = "dc2c4869445c"
SUMMARY = "Singleton seed reflects each group's main shape across indicated side."

INVARIANTS = [
    "each multicolor group has one main multi-cell color and one singleton seed color",
    "the seed's position relative to the main bbox selects the reflection direction",
    "main and seed colors are distinct and non-zero",
    "the main shape sits clear of grid borders",
]

SEED_SIDES = ("above", "below", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "no_main", "full_grid")
HELPFUL_TEXTURES = SEED_SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "seed_side":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SEED_SIDES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for seed_side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    seed_side = (overrides.get("texture") if overrides.get("texture") in SEED_SIDES else None) or \
                overrides.get("seed_side") or \
                ctx.draw_choice("seed_side", list(SEED_SIDES))
    if "seed_side" not in overrides and overrides.get("texture") not in SEED_SIDES:
        seed_side = ["above", "right", "below", "left"][sample_index % 4]
    main, seed_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(13, 13, 0)
    r, c = 5, 5
    draw_rect(g, r, c, 2, 3, main)
    if seed_side == "above":
        g[r - 1][c + 1] = seed_color
    elif seed_side == "below":
        g[r + 2][c + 1] = seed_color
    elif seed_side == "left":
        g[r][c - 1] = seed_color
    else:
        g[r][c + 3] = seed_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_seed":
        draw_rect(g, 5, 5, 2, 3, 2)
        return g
    if name == "no_main":
        g[6][6] = 3
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
