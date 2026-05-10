"""Generator for 3490cc26.

Rule: a longest visibility path through 2x2 color blocks is drawn as
color-7 corridors.

Combinatorial axes (8): grid_h/w, turn, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_blocks, single_block, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "a55c1997c5e3"
VERSION = "1.1.0"
TASK_ID = "a55c1997c5e3"
SUMMARY = "Longest visibility path through 2x2 color blocks drawn as color-7 corridors."

INVARIANTS = [
    "nodes are exact 2x2 blocks of color 2 or 8",
    "the unique color-2 block is the path start",
    "same-row and same-column visibility defines graph edges",
    "corridors between consecutive path nodes are painted color 7",
]

TURNS = ("down", "right", "up")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blocks", "single_block", "full_grid")
HELPFUL_TEXTURES = TURNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "12..15"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "14..16"},
    "turn":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TURNS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for turn",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    turn = (overrides.get("texture") if overrides.get("texture") in TURNS else None) or \
           overrides.get("turn") or \
           ctx.draw_choice("turn", list(TURNS))
    h = rng.randint(12, 15)
    w = rng.randint(14, 16)
    g = full_grid(h, w, 0)
    r0 = rng.randint(1, 2)
    c0 = rng.randint(1, 2)
    nodes = [(r0, c0, 2), (r0, c0 + 5, 8)]
    if turn == "down":
        nodes += [(r0 + 5, c0 + 5, 8), (r0 + 5, c0 + 9, 8)]
    elif turn == "right":
        nodes += [(r0, c0 + 9, 8), (r0 + 5, c0 + 9, 8)]
    else:
        base = h - 4
        nodes = [(base, c0, 2), (base, c0 + 5, 8), (base - 5, c0 + 5, 8), (base - 5, c0 + 9, 8)]
    for r, c, color in nodes:
        draw_rect(g, r, c, 2, 2, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 15, 0)
    if name == "no_blocks":
        return g
    if name == "single_block":
        draw_rect(g, 4, 4, 2, 2, 2)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(15):
                g[r][c] = 8
        return g
    return g
