"""Generator for 456873bc.

Rule: a self-similar tile pattern expands into matching macro blocks.

Combinatorial axes (8): grid_h/w, pattern, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_pattern, no_blocks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9a94379ed070"
VERSION = "1.1.0"
TASK_ID = "9a94379ed070"
SUMMARY = "Self-similar tile pattern expands into matching macro blocks."

INVARIANTS = [
    "a nonzero tile appears in the first separator-delimited block",
    "zero separator rows and columns define a block lattice",
    "the tile's occupied cells act both as macro-block selectors and micro-cell selectors",
]

PATTERNS = ("diag", "corner", "vee")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pattern", "no_blocks", "full_grid")
HELPFUL_TEXTURES = PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "pattern":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATTERNS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    pattern = (overrides.get("texture") if overrides.get("texture") in PATTERNS else None) or \
              overrides.get("pattern") or \
              ["diag", "corner", "vee"][sample_index % 3]
    color = ctx.draw_color("tile_color", exclude={0, 3})
    tile_size = 3
    blocks = 3
    h = blocks * tile_size + (blocks - 1)
    w = blocks * tile_size + (blocks - 1)
    g = full_grid(h, w, 0)
    cells = {
        "diag": [(0, 0), (1, 1), (2, 2)],
        "corner": [(0, 0), (0, 2), (2, 0)],
        "vee": [(0, 0), (1, 1), (0, 2), (2, 1)],
    }[pattern]
    for r, c in cells:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_pattern":
        return g
    if name == "no_blocks":
        g[5][5] = 4
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 4
        return g
    return g
