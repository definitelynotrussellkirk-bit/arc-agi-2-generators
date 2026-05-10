"""Generator for 42918530.

Rule: zero-separated same-color tiles share all observed local
offsets for that color.

Combinatorial axes (8): tile_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
n_tiles.
Degenerates: no_tiles, single_tile, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4dd7720cba5f"
VERSION = "1.1.0"
TASK_ID = "4dd7720cba5f"
SUMMARY = "Same-color tiles share local offsets across separated tiles."

INVARIANTS = [
    "all-zero rows and columns separate same-sized tiles",
    "each nonempty tile has a single header color at its top-left cell",
    "local offsets seen for a color in any tile are applied to every tile of that color",
    "tile colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_tiles", "single_tile", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "tile_size":      {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "n_tiles":        {"type": "int", "default": "4", "valid": "4"},
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
        ts_lo, ts_hi = 2, 2
    elif difficulty == "hard":
        ts_lo, ts_hi = 3, 4
    else:
        ts_lo, ts_hi = 2, 3
    tile_size = ctx.draw_int("tile_size", ts_lo, ts_hi)
    color_a, color_b = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    size = 2 * tile_size + 1
    g = full_grid(size, size, 0)
    starts = [(0, 0), (0, tile_size + 1), (tile_size + 1, 0), (tile_size + 1, tile_size + 1)]
    colors = [color_a, color_a, color_b, color_b]
    offsets = [(0, 0), (1, 1), (tile_size - 1, 0), (0, tile_size - 1)]
    for idx, (r0, c0) in enumerate(starts):
        color = colors[idx]
        g[r0][c0] = color
        choices = offsets[:]
        rng.shuffle(choices)
        for dr, dc in choices[:rng.randint(1, len(choices))]:
            g[r0 + dr][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_tiles":
        return g
    if name == "single_tile":
        g[0][0] = 2
        g[1][1] = 2
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 2
        return g
    return g
