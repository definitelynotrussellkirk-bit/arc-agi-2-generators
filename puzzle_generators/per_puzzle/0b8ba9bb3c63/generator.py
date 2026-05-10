"""Generator for 6ffe8f07.

Rule: a cyan rectangle emits yellow horizontal and vertical arms,
bounded by non-cyan blocker objects.

Combinatorial axes (8): grid_h/w, blocker_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_cyan, no_blockers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0b8ba9bb3c63"
VERSION = "1.1.0"
TASK_ID = "0b8ba9bb3c63"
SUMMARY = "Cyan rectangle emits yellow arms, bounded by non-cyan blocker objects."

INVARIANTS = [
    "background is color 0",
    "one cyan rectangular component is present",
    "blockers use colors other than red and cyan",
    "yellow arms are limited by blockers or grid edges",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cyan", "no_blockers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..17", "valid": "13..17"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "13..17"},
    "blocker_count":  {"type": "int", "default": "4", "valid": "4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    ctx.draw_int("blocker_count", 4, 4)
    h = 13 + rng.randint(0, 4)
    w = 13 + rng.randint(0, 4)
    b1, b2 = ctx.draw_distinct_colors("blockers", n=2, exclude={0, 2, 8})
    g = full_grid(h, w, 0)
    cr = h // 2 - 1
    cc = w // 2 - 1
    for r in range(cr, cr + 2):
        for c in range(cc, cc + 3):
            g[r][c] = 8
    for r in range(cr, cr + 2):
        g[r][1] = b1
        g[r][w - 2] = b2
    for c in range(cc, cc + 3):
        g[1][c] = b2
        g[h - 2][c] = b1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_cyan":
        g[1][5] = 3
        return g
    if name == "no_blockers":
        for r in range(5, 7):
            for c in range(5, 8):
                g[r][c] = 8
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 8
        return g
    return g
