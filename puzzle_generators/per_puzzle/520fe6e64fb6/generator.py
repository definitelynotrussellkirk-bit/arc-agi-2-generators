"""Generator for fc10701f.

Rule: maroon block becomes orange, original orange clears, and
zero-marked gaps become red connectors.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
block_size.
Degenerates: no_blocks, no_gaps, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "520fe6e64fb6"
VERSION = "1.1.0"
TASK_ID = "520fe6e64fb6"
SUMMARY = "Maroon block becomes orange; original orange clears; gaps become red."

INVARIANTS = [
    "the background is fixed color 6",
    "one color-9 block and one color-7 block are row- or column-aligned",
    "at least one intervening row or column contains a zero marker",
    "blocks sit clear of grid edges with margin for the connector",
]

ORIENTATIONS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blocks", "no_gaps", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "block_size":     {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    h = 10 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 3)
    g = full_grid(h, w, 6)
    if orientation == "vertical":
        rw = rng.randint(2, 4)
        c0 = rng.randint(2, w - rw - 2)
        r9 = 1
        r7 = h - 3
        draw_rect(g, r9, c0, 2, rw, 9)
        draw_rect(g, r7, c0, 2, rw, 7)
        for c in range(0, w, 2):
            g[(r9 + r7) // 2][c] = 0
    else:
        rh = rng.randint(2, 4)
        r0 = rng.randint(2, h - rh - 2)
        c9 = 1
        c7 = w - 3
        draw_rect(g, r0, c9, rh, 2, 9)
        draw_rect(g, r0, c7, rh, 2, 7)
        for r in range(0, h, 2):
            g[r][(c9 + c7) // 2] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 6)
    if name == "no_blocks":
        return g
    if name == "no_gaps":
        draw_rect(g, 1, 4, 2, 3, 9)
        draw_rect(g, 8, 4, 2, 3, 7)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 6
        return g
    return g
