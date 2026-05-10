"""Generator for aee291af.

Rule: among maximal 2/8 rectangles, the unique content pattern is
extracted.

Combinatorial axes (8): grid_h/w, unique_position, unique_variant,
palette_kind, anchor_corner, asymmetry_force, palette_size,
position_bias.
Degenerates: no_rects, all_same, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a6f3147fe2e"
VERSION = "1.1.0"
TASK_ID = "5a6f3147fe2e"
SUMMARY = "Among maximal 2/8 rectangles, the unique content pattern is extracted."

INVARIANTS = [
    "background is color 0",
    "foreground rectangles contain only colors 2 and 8",
    "at least two rectangles share identical content",
    "exactly one maximal foreground rectangle has unique content",
]

UNIQUE_POSITIONS = ("right", "bottom")
UNIQUE_VARIANTS = ("a", "b", "c")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "all_same", "full_grid")
HELPFUL_TEXTURES = UNIQUE_VARIANTS

COMMON = [[2, 8, 2], [8, 2, 8], [2, 8, 2]]
UNIQUES = {
    "a": [[8, 8, 2], [2, 8, 2], [2, 2, 8]],
    "b": [[2, 2, 8], [8, 2, 8], [8, 2, 2]],
    "c": [[8, 2, 8], [8, 8, 2], [2, 2, 2]],
}

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "unique_position":{"type": "str", "default": "rng",
                       "valid": "|".join(UNIQUE_POSITIONS)},
    "unique_variant": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(UNIQUE_VARIANTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for unique_variant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _stamp(g, r0, c0, pattern):
    for r, row in enumerate(pattern):
        for c, value in enumerate(row):
            g[r0 + r][c0 + c] = value


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    pos = ctx.draw_choice("unique_position", list(UNIQUE_POSITIONS))
    variant = (overrides.get("texture") if overrides.get("texture") in UNIQUE_VARIANTS else None) or \
              overrides.get("unique_variant") or \
              ctx.draw_choice("unique_variant", list(UNIQUE_VARIANTS))
    row_shift = rng.randint(0, 1)
    col_shift = rng.randint(0, 1)
    g = full_grid(12, 12, 0)
    _stamp(g, 1 + row_shift, 1 + col_shift, COMMON)
    _stamp(g, 7, 1 + col_shift, COMMON)
    if pos == "right":
        _stamp(g, 1 + row_shift, 7, UNIQUES[variant])
    else:
        _stamp(g, 7, 7, UNIQUES[variant])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_rects":
        return g
    if name == "all_same":
        _stamp(g, 1, 1, COMMON)
        _stamp(g, 1, 7, COMMON)
        _stamp(g, 7, 1, COMMON)
        _stamp(g, 7, 7, COMMON)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
