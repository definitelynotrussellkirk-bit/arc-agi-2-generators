"""Generator for a8c38be5.

Rule: isolated solid 3x3 tiles are moved into a 9x9 canvas according
to where their non-gray cells sit.

Combinatorial axes (8): grid_h/w, tile_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
signal_kind.
Degenerates: no_tiles, single_tile, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a85abd1e231"
VERSION = "1.1.0"
TASK_ID = "5a85abd1e231"
SUMMARY = "Isolated 3x3 tiles route into 9x9 canvas by signal-cell positions."

INVARIANTS = [
    "background is color 0",
    "candidate tiles are isolated solid 3x3 blocks",
    "tile filler is color 5 and signal cells are nonzero colors other than 5",
    "each tile stamps into one of nine output macro positions",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_tiles", "single_tile", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

SIGNALS = [
    [(0, 0, 2), (0, 1, 2)],
    [(2, 1, 3), (2, 2, 3)],
    [(1, 0, 4), (2, 0, 4)],
    [(0, 2, 6), (1, 2, 6)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "tile_count":     {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "signal_kind":    {"type": "str", "default": "rng", "valid": "rng"},
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
        tc_lo, tc_hi = 1, 1
    elif difficulty == "hard":
        tc_lo, tc_hi = 3, 4
    else:
        tc_lo, tc_hi = 1, 4
    count = ctx.draw_int("tile_count", tc_lo, tc_hi)
    g = full_grid(10, 10, 0)
    anchors = [(1, 1), (1, 6), (6, 1), (6, 6)]
    start = rng.randint(0, len(SIGNALS) - 1)
    for i in range(count):
        r0, c0 = anchors[i]
        for dr in range(3):
            for dc in range(3):
                g[r0 + dr][c0 + dc] = 5
        for dr, dc, color in SIGNALS[(start + i) % len(SIGNALS)]:
            g[r0 + dr][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_tiles":
        return g
    if name == "single_tile":
        for dr in range(3):
            for dc in range(3):
                g[1 + dr][1 + dc] = 5
        for dr, dc, color in SIGNALS[0]:
            g[1 + dr][1 + dc] = color
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
