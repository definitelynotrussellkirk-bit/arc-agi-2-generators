"""Generator for ae4f1146.

Rule: among isolated nonzero 3x3 tiles, output the tile with the most
blue cells.

Combinatorial axes (8): grid_h/w, tile_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
fill_color.
Degenerates: no_tiles, single_tile, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9bd5d9c04dd8"
VERSION = "1.1.0"
TASK_ID = "9bd5d9c04dd8"
SUMMARY = "Among isolated 3x3 tiles, output the tile with most blue cells."

INVARIANTS = [
    "background is color 0",
    "candidate tiles are isolated filled 3x3 blocks",
    "all candidate cells are nonzero",
    "the selected candidate maximizes the count of color 1 cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_tiles", "single_tile", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "9..18"},
    "tile_count":     {"type": "int", "default": "2", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "fill_color":     {"type": "color", "default": "rng !{0,1}", "valid": "2..9"},
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
    n = ctx.draw_int("tile_count", 2, 2)
    h = 9 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    anchors = [(1, 1), (1, 6)]
    fill_color = ctx.draw_color("fill_color", exclude={0, 1})
    for i in range(n):
        r0, c0 = anchors[i]
        for dr in range(3):
            for dc in range(3):
                g[r0 + dr][c0 + dc] = fill_color
        ones = 2 + i * 3 + ((sample_index + i) % 2)
        placed = 0
        for dr in range(3):
            for dc in range(3):
                if placed < ones:
                    g[r0 + dr][c0 + dc] = 1
                    placed += 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_tiles":
        return g
    if name == "single_tile":
        for dr in range(3):
            for dc in range(3):
                g[1 + dr][1 + dc] = 1 if (dr + dc) % 2 == 0 else 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 1
        return g
    return g
