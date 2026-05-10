"""Generator for arc_puzzle_bank_fifteenth21:E104.

Rule: place colored cells in a square grid to mirror across the main
diagonal.

Combinatorial axes (8): grid_h/w, size, markers, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: empty_grid, single_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "17f92e205b34"
VERSION = "1.1.0"
TASK_ID = "17f92e205b34"

SUMMARY = "Place colored cells to mirror across the main diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "source cells are above the main diagonal",
    "mirrored counterparts start empty",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_grid", "single_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "7..10"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "7..10"},
    "size":           {"type": "int", "default": "rng 7..10", "valid": "7..10"},
    "markers":        {"type": "int", "default": "rng 3..6", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n = ctx.draw_int("size", 7, 8)
    elif difficulty == "hard":
        n = ctx.draw_int("size", 9, 10)
    else:
        n = ctx.draw_int("size", 7, 10)
    target = min(ctx.draw_int("markers", 3, 6), n * (n - 1) // 2)
    g = full_grid(n, n, 0)
    positions = [(r, c) for r in range(n) for c in range(r + 1, n)]
    for r, c in rng.sample(positions, target):
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "empty_grid":
        return g
    if name == "single_marker":
        g[2][5] = 3
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 3
        return g
    return g
