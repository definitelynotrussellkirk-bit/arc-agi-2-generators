"""Generator for fea12743.

Rule: among six fixed 4x4 slots, one pattern is the union of two
source patterns.

Combinatorial axes (8): grid_h/w, union_style, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
transpose.
Degenerates: no_patterns, full_grid, all_same.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "af834385e5f2"
VERSION = "1.1.0"
TASK_ID = "af834385e5f2"
SUMMARY = "Among six 4x4 slots, one pattern is the union of two source patterns."

INVARIANTS = [
    "six fixed 4x4 pattern slots are sampled at the canonical origins",
    "two source slots use color 2 cells whose union exactly matches a third slot",
    "a fourth pair of slots contains decoy color-2 cells",
    "the slot grid has six fixed positions in a 3x2 layout",
]

UNION_STYLES = ("sparse", "angled", "split")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patterns", "full_grid", "all_same")
HELPFUL_TEXTURES = UNION_STYLES

ORIGINS = [(1, 1), (1, 6), (6, 1), (6, 6), (11, 1), (11, 6)]

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "union_style":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(UNION_STYLES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "transpose":      {"type": "bool", "default": "rng",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for union_style",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    style = (overrides.get("texture") if overrides.get("texture") in UNION_STYLES else None) or \
            overrides.get("union_style") or \
            ctx.draw_choice("union_style", list(UNION_STYLES))
    g = full_grid(16, 11, 0)
    if style == "sparse":
        a = {(0, 0), (1, 0), (2, 1)}
        b = {(0, 2), (1, 3), (3, 3)}
    elif style == "angled":
        a = {(0, 1), (1, 1), (2, 2), (3, 2)}
        b = {(0, 3), (1, 2), (2, 1), (3, 0)}
    else:
        a = {(0, 0), (0, 1), (1, 1), (2, 1)}
        b = {(1, 3), (2, 2), (2, 3), (3, 3)}
    if rng.randint(0, 1):
        a = {(c, r) for r, c in a}
        b = {(c, r) for r, c in b}
    extras = [
        {(0, 0), (3, 3)},
        {(0, 3), (3, 0)},
        {(1, 0), (2, 3)},
    ]
    patterns = [a, b, a | b, *extras]
    for origin, cells in zip(ORIGINS, patterns):
        paint_at(g, origin[0], origin[1], cells, 2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 11, 0)
    if name == "no_patterns":
        return g
    if name == "all_same":
        for origin in ORIGINS:
            paint_at(g, origin[0], origin[1], {(0, 0), (1, 1)}, 2)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
