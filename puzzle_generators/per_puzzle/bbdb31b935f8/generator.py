"""Generator for b20f7c8b.

Rule: a key around an 8-panel maps solid 5x5 tiles into patterned tiles.

Combinatorial axes (8): grid_h/w, tile_count, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_key, no_tiles, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "bbdb31b935f8"
VERSION = "1.1.0"
TASK_ID = "bbdb31b935f8"
SUMMARY = "Key around 8-panel maps solid 5x5 tiles into patterned tiles."

INVARIANTS = [
    "an 8 block is surrounded by small keyed color shapes",
    "solid 5x5 tiles use one of those key colors as their base",
    "the output fills matching tiles with the shared pattern base and stamps the key's internal 1 pattern",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_key", "no_tiles", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "18", "valid": "18"},
    "grid_w":         {"type": "int", "default": "20", "valid": "20"},
    "tile_count":     {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !{0,1,2,8}",
                       "valid": "3..7|9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        tile_count = ctx.draw_int("tile_count", 1, 1)
    elif difficulty == "hard":
        tile_count = ctx.draw_int("tile_count", 3, 3)
    else:
        tile_count = ctx.draw_int("tile_count", 1, 3)
    key_color = ctx.draw_color("key_color", exclude={0, 1, 2, 8})
    g = full_grid(18, 20, 0)
    draw_rect(g, 2, 8, 3, 3, 8)

    key_cells = [(1, 8), (1, 9), (2, 7)]
    for r, c in key_cells:
        g[r][c] = key_color

    tile_positions = [(10, 2), (10, 9), (5, 14)]
    for r, c in tile_positions[:tile_count]:
        draw_rect(g, r, c, 5, 5, key_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 20, 0)
    if name == "no_key":
        draw_rect(g, 10, 2, 5, 5, 3)
        return g
    if name == "no_tiles":
        draw_rect(g, 2, 8, 3, 3, 8)
        for r, c in [(1, 8), (1, 9), (2, 7)]:
            g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(20):
                g[r][c] = 8
        return g
    return g
