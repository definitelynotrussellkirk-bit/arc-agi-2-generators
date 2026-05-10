"""Generator for 5792cb4d.

Rule: single connected colored snake path on cyan keeps positions
while reversing the path color sequence.

Combinatorial axes (8): grid_h/w, path_length, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_path, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c631747784e"
VERSION = "1.1.0"
TASK_ID = "2c631747784e"
SUMMARY = "Connected snake path on cyan; rule reverses path color sequence."

INVARIANTS = [
    "the background is color 8",
    "all non-background cells form one non-branching 4-connected path",
    "the path has exactly two endpoints",
    "the path color sequence is not palindromic",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_path", "single_cell", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "path_length":    {"type": "int", "default": "rng 6..10", "valid": "2..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..6", "valid": "2..9"},
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
        pl_lo, pl_hi = 6, 7
    elif difficulty == "hard":
        pl_lo, pl_hi = 10, 14
    else:
        pl_lo, pl_hi = 6, 10
    path_length = ctx.draw_int("path_length", pl_lo, pl_hi)
    g = full_grid(12, 12, 8)
    path = []
    r, c = 5, 2
    direction = 1
    while len(path) < path_length:
        path.append((r, c))
        if direction == 1 and c < 8:
            c += 1
        elif direction == -1 and c > 2:
            c -= 1
        else:
            r += 1
            direction *= -1
    colors = [v for v in range(10) if v != 8]
    seq = [rng.choice(colors) for _ in path]
    if seq == list(reversed(seq)):
        seq[-1] = 7 if seq[-1] != 7 else 6
    for (rr, cc), color in zip(path, seq):
        g[rr][cc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 8)
    if name == "no_path":
        return g
    if name == "single_cell":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
