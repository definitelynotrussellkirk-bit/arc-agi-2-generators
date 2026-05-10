"""Generator for arc_additional_puzzle_bank_volume7:E45.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_lines, single_cell_lines, l_shaped_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7072db3091a"
VERSION = "1.1.0"
TASK_ID = "f7072db3091a"
SUMMARY = "Endpoints of straight blue lines are recolored orange."

INVARIANTS = [
    "background is 0",
    "blue components are straight horizontal or vertical lines",
    "line components have length at least two",
    "components are separated so endpoints are unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_lines", "single_cell_lines", "l_shaped_lines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "isolated_lines",
                       "valid": "isolated_lines"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        n_lines = ctx.draw_int("n_lines", 1, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 12, 16)
        n_lines = ctx.draw_int("n_lines", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_lines = ctx.draw_int("n_lines", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    horizontal = rng.choice([False, True])
    used: set[int] = set()
    made = 0
    for _ in range(200):
        if made >= n_lines:
            break
        if horizontal:
            choices = [r for r in range(h) if all(abs(r - rr) > 1 for rr in used)]
            if not choices:
                break
            r = rng.choice(choices)
            length = rng.randint(2, min(6, w))
            c = rng.randint(0, w - length)
            for dc in range(length):
                g[r][c + dc] = 1
            used.add(r)
        else:
            choices = [c for c in range(w) if all(abs(c - cc) > 1 for cc in used)]
            if not choices:
                break
            c = rng.choice(choices)
            length = rng.randint(2, min(6, h))
            r = rng.randint(0, h - length)
            for dr in range(length):
                g[r + dr][c] = 1
            used.add(c)
        made += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_lines":
        # Empty grid — rule has no endpoints to recolor.
        return g
    if name == "single_cell_lines":
        # Length-1 "lines" — endpoint == only cell, no body to leave behind.
        g[2][3] = 1; g[5][6] = 1
        return g
    if name == "l_shaped_lines":
        # Bent (L-shaped) blue components — not straight, ambiguous endpoints.
        g[2][2] = 1; g[2][3] = 1; g[2][4] = 1
        g[3][4] = 1; g[4][4] = 1
        return g
    return g
