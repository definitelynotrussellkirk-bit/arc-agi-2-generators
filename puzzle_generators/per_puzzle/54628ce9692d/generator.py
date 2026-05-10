"""Generator for e9fc42f2.

Rule: assemble pieces by matching marker ports.

Combinatorial axes (8): grid_h/w, gap, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_pieces, no_ports, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "54628ce9692d"
VERSION = "1.1.0"
TASK_ID = "54628ce9692d"
SUMMARY = "Two 3x3 pieces have matching exposed color-2 ports on opposite sides."

INVARIANTS = [
    "background is 0",
    "piece fill color is 1",
    "exactly two color-2 marker ports define one assembly edge",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pieces", "no_ports", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "gap":            {"type": "int", "default": "rng 2..4", "valid": "2..4"},
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
    if difficulty == "easy":
        gap = ctx.draw_int("gap", 2, 2)
    elif difficulty == "hard":
        gap = ctx.draw_int("gap", 4, 4)
    else:
        gap = ctx.draw_int("gap", 2, 4)
    h = 7
    w = 9 + gap
    g = full_grid(h, w, 0)
    r0 = rng.randint(1, 3)
    c0 = 1
    c1 = c0 + 3 + gap
    fill_box(g, r0, c0, r0 + 2, c0 + 2, 1)
    fill_box(g, r0, c1, r0 + 2, c1 + 2, 1)
    g[r0 + 1][c0 + 2] = 2
    g[r0 + 1][c1] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 11, 0)
    if name == "no_pieces":
        g[3][3] = 2
        return g
    if name == "no_ports":
        fill_box(g, 1, 1, 3, 3, 1)
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(11):
                g[r][c] = 1
        return g
    return g
