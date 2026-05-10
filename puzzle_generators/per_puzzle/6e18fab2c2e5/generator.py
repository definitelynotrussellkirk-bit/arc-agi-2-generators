"""Generator for puzzle 50c07299.

Rule: bg=7, n red 2-cells in diagonal chain. Compute opposite step.
Erase old chain, place new (n+1)-cell chain shifted by n*step.

Combinatorial axes (8): grid_size, n_cells, diag_direction,
chain_position, anchor_corner, asymmetry_force, palette_size,
include_decoy.
Degenerates: single_cell, no_chain, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6e18fab2c2e5"
VERSION = "1.1.0"
TASK_ID = "6e18fab2c2e5"
SUMMARY = "bg=7 + diagonal 2-chain; rule shifts in opposite direction."

INVARIANTS = [
    "bg = 7",
    "h = w = 16 (or 12..20)",
    "2-4 cells of color 2 in contiguous diagonal chain",
    "chain's opposite-direction extension fits in-bounds",
]

DIAG_DIRECTIONS = ("nw", "ne", "sw", "se")
DEGENERATE_TEXTURES = ("single_cell", "no_chain", "full_grid")
HELPFUL_TEXTURES = DIAG_DIRECTIONS

AXES = {
    "grid_size":      {"type": "int", "default": "16", "valid": "12..20"},
    "n_cells":        {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "diag_direction": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIAG_DIRECTIONS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "chain_position": {"type": "str", "default": "rng",
                       "valid": "near_corner|spread"},
    "texture":        {"type": "str", "default": "alias for diag_direction",
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
        size = 12
    elif difficulty == "hard":
        size = 20
    else:
        size = int(overrides.get("grid_size", 16))
    size = max(12, min(20, size))
    h = w = size
    g = full_grid(h, w, 7)
    n = int(overrides.get("n_cells",
                          ctx.draw_int("n_cells", 2, 3)))
    n = max(2, min(5, n))
    direction = (overrides.get("texture") or
                 overrides.get("diag_direction")
                 or ctx.draw_choice("diag_direction",
                                    list(DIAG_DIRECTIONS)))
    if direction == "nw":
        dr, dc = -1, -1
    elif direction == "ne":
        dr, dc = -1, 1
    elif direction == "sw":
        dr, dc = 1, -1
    else:
        dr, dc = 1, 1
    margin = n + 2
    if dr == 1:
        start_r = rng.randint(margin + n + 1, h - margin - 1)
    else:
        start_r = rng.randint(margin, h - margin - n - 2)
    if dc == 1:
        start_c = rng.randint(margin + n + 1, w - margin - 1)
    else:
        start_c = rng.randint(margin, w - margin - n - 2)
    for i in range(n):
        r = start_r + i * dr
        c = start_c + i * dc
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h = w = 16
    g = full_grid(h, w, 7)
    if name == "single_cell":
        g[h // 2][w // 2] = 2
        return g
    if name == "no_chain":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
