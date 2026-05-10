"""Generator for arc_additional_puzzle_bank_volume13:E86 — line endpoints recolor red.

Rule: endpoints of straight green lines (length ≥3) are recolored red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_lines, length_2, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22ee9e5c3a9a"
VERSION = "1.1.0"
TASK_ID = "22ee9e5c3a9a"
SUMMARY = "Endpoints of straight green lines are recolored red."

INVARIANTS = [
    "background is 0",
    "target green components are straight horizontal or vertical lines of length at least 3",
    "line components are separated so endpoints are unambiguous",
    "optional non-line green fragments are not targets",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_lines", "length_2", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1 (green)", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "axis_aligned_lines",
                       "valid": "axis_aligned_lines"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_lines = ctx.draw_int("n_lines", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 13, 18)
        n_lines = ctx.draw_int("n_lines", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_lines = ctx.draw_int("n_lines", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    used_rows: set[int] = set()
    used_cols: set[int] = set()
    made = 0
    horizontal = rng.choice([False, True])
    for _ in range(200):
        if made >= n_lines:
            break
        if horizontal and len(used_rows) < h:
            r = rng.choice([x for x in range(h) if x not in used_rows])
            length = rng.randint(3, min(6, w))
            c = rng.randint(0, w - length)
            for dc in range(length):
                g[r][c + dc] = 3
            used_rows.add(r)
            made += 1
        elif len(used_cols) < w:
            c = rng.choice([x for x in range(w) if x not in used_cols])
            length = rng.randint(3, min(6, h))
            r = rng.randint(0, h - length)
            for dr in range(length):
                g[r + dr][c] = 3
            used_cols.add(c)
            made += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_lines":
        # Empty grid — no green line, no endpoints to recolor.
        return g
    if name == "length_2":
        # Length-2 green segments — too short for the rule's length-3+
        # filter, no endpoints distinguishable from interior.
        for dc in range(2):
            g[2][2 + dc] = 3
        for dc in range(2):
            g[5][6 + dc] = 3
        return g
    if name == "single_cell":
        # Length-1 segments — even shorter, no line at all.
        g[2][2] = 3; g[5][7] = 3; g[8][3] = 3
        return g
    return g
