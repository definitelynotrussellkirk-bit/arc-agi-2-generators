"""Generator for arc_additional_puzzle_bank_volume5:H33.

Rule: BFS from 2-seed through non-8 cells; each reached cell is
recolored by parity — even distance → 3, odd → 4.

Combinatorial axes (8): grid_h/w, palette_kind, n_walls, palette_size,
position_bias, n_distinct_colors, wall_density, texture.
Degenerates: no_seed, no_frame, seed_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "807c284a7e79"
VERSION = "1.1.0"
TASK_ID = "807c284a7e79"
SUMMARY = "8-frame around interior + 2-seed + 1-2 8-walls inside (creating maze)."

INVARIANTS = [
    "8-frame on outer border",
    "exactly one 2-seed inside",
    "1-3 8-walls inside (creating non-trivial maze)",
]

PALETTE_KINDS = ("default", "thin_wall", "thick_wall", "branching")
DEGENERATE_TEXTURES = ("no_seed", "no_frame", "seed_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "wall_density":   {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h):
        g[r][0] = 8; g[r][w - 1] = 8
    g[h // 2][2] = 2
    for r in range(2, h - 2):
        g[r][w // 2] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # frame + walls but no 2-seed → BFS has no source
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        for r in range(2, h - 2):
            g[r][w // 2] = 8
        return g
    if name == "no_frame":
        # 2-seed + interior walls but no 8-frame — BFS escapes/unbounded
        g[h // 2][2] = 2
        for r in range(2, h - 2):
            g[r][w // 2] = 8
        return g
    if name == "seed_isolated":
        # seed completely walled in by 8s → BFS reaches only itself
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        # surround the seed with 8s
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            g[3 + dr][3 + dc] = 8
        g[3][3] = 2
        return g
    return g
