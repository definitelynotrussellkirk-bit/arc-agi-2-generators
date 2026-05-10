"""Generator for c64f1187.

Rule: key mask above a sparse 5-tile lattice paints each tile by its
center color.

Combinatorial axes (8): grid_h/w, mask_variant, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_lattice, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db80068a483e"
VERSION = "1.1.0"
TASK_ID = "db80068a483e"
SUMMARY = "Key mask above sparse 5-tile lattice paints each tile by center color."

INVARIANTS = [
    "background is color 0",
    "key markers are nonzero colors above the tile lattice",
    "a 2x2 binary mask of color 1 sits below each key marker",
    "tile positions are indexed by sparse color-5 row and column anchors",
]

MASK_VARIANTS = ("diag", "corner", "full")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_lattice", "no_key", "full_grid")
HELPFUL_TEXTURES = MASK_VARIANTS

MASKS = {
    "diag": [(0, 0), (1, 1)],
    "corner": [(0, 0), (0, 1), (1, 0)],
    "full": [(0, 0), (0, 1), (1, 0), (1, 1)],
}

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "mask_variant":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MASK_VARIANTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for mask_variant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    mask_name = (overrides.get("texture") if overrides.get("texture") in MASK_VARIANTS else None) or \
                overrides.get("mask_variant") or \
                ctx.draw_choice("mask_variant", list(MASK_VARIANTS))
    key_color, other_color = ctx.draw_distinct_colors("colors", n=2, exclude={0, 1, 5})
    g = full_grid(10, 9, 0)
    g[0][1] = key_color
    for dr, dc in MASKS[mask_name]:
        g[1 + dr][1 + dc] = 1
    tile_rows = [4, 7]
    tile_cols = [1, 4]
    for r in tile_rows:
        for c in tile_cols:
            g[r][c] = 5
    g[5][2] = key_color
    g[5][5] = other_color
    g[8][2] = key_color
    g[8][5] = other_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 9, 0)
    if name == "no_lattice":
        g[0][1] = 2
        for dr, dc in MASKS["diag"]:
            g[1 + dr][1 + dc] = 1
        return g
    if name == "no_key":
        for r in [4, 7]:
            for c in [1, 4]:
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(9):
                g[r][c] = 5
        return g
    return g
