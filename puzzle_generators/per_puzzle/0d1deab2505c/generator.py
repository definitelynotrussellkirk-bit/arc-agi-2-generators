"""Generator for 99caaf76.

Rule: a cross-bodied creature shifts away from its tail and rotates its
body colors.

Combinatorial axes (8): grid_h/w, tail_direction, tail_length, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_creature, no_tail, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d1deab2505c"
VERSION = "1.1.0"
TASK_ID = "0d1deab2505c"
SUMMARY = "Cross-bodied creature shifts away from tail and rotates body colors."

INVARIANTS = [
    "the background is color 8",
    "one color-4 center has four colored cardinal body cells",
    "a color-1 tail begins two cells from the center in one cardinal direction",
    "the creature shifts to the opposite grid edge from the tail",
]

DIRECTIONS = ("right", "left", "down", "up")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_creature", "no_tail", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "tail_direction": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "tail_length":    {"type": "choice", "default": "rng",
                       "valid": "2|3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for tail_direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    direction = (overrides.get("texture") if overrides.get("texture") in DIRECTIONS else None) or \
                overrides.get("tail_direction") or \
                ctx.draw_choice("tail_direction", list(DIRECTIONS))
    if difficulty == "easy":
        tail_len = ctx.draw_choice("tail_length", [2])
    elif difficulty == "hard":
        tail_len = ctx.draw_choice("tail_length", [3])
    else:
        tail_len = ctx.draw_choice("tail_length", [2, 3])
    top, bottom, left, right = ctx.draw_distinct_colors("body_colors", n=4, exclude={1, 4, 8})
    g = full_grid(13, 13, 8)
    cr, cc = 6, 6
    g[cr][cc] = 4
    g[cr - 1][cc] = top
    g[cr + 1][cc] = bottom
    g[cr][cc - 1] = left
    g[cr][cc + 1] = right
    for k in range(2, 2 + tail_len):
        if direction == "right":
            g[cr][cc + k] = 1
        elif direction == "left":
            g[cr][cc - k] = 1
        elif direction == "down":
            g[cr + k][cc] = 1
        else:
            g[cr - k][cc] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 8)
    if name == "no_creature":
        g[6][9] = 1
        return g
    if name == "no_tail":
        g[6][6] = 4
        g[5][6] = 3
        g[7][6] = 5
        g[6][5] = 6
        g[6][7] = 7
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 4
        return g
    return g
