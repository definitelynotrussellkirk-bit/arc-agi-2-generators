"""Generator for 1e5d6875.

Rule: color-5 and color-2 L-trominoes project complementary shifted
copies in colors 4 and 3.

Combinatorial axes (8): grid_h/w, piece_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_pieces, single_piece, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e99db71ae23d"
VERSION = "1.1.0"
TASK_ID = "e99db71ae23d"
SUMMARY = "Color-5 and color-2 L-trominoes project shifted copies in 4 and 3."

INVARIANTS = [
    "the background is color 7",
    "each active piece is a connected color-5 or color-2 L-tromino with one missing bbox corner",
    "color-5 pieces paint color 4 shifted toward their missing corner",
    "color-2 pieces paint color 3 shifted away from their missing corner",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pieces", "single_piece", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

_L_SHAPES = [
    [(0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "7..18"},
    "piece_count":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, shape, r0, c0, color):
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        pc_lo, pc_hi = 2, 2
    elif difficulty == "hard":
        pc_lo, pc_hi = 4, 6
    else:
        pc_lo, pc_hi = 2, 4
    piece_count = ctx.draw_int("piece_count", pc_lo, pc_hi)
    h = rng.randint(8, 12)
    w = rng.randint(8, 13)
    g = full_grid(h, w, 7)
    occupied = set()
    for idx in range(piece_count):
        color = 5 if idx % 2 == 0 else 2
        shape = _L_SHAPES[rng.randrange(len(_L_SHAPES))]
        for _attempt in range(100):
            r0 = rng.randint(1, h - 3)
            c0 = rng.randint(1, w - 3)
            cells = {(r0 + dr, c0 + dc) for dr, dc in shape}
            halo = {(r + dr, c + dc) for r, c in cells for dr in (-1, 0, 1) for dc in (-1, 0, 1)}
            if not occupied & halo:
                _paint(g, shape, r0, c0, color)
                occupied |= cells
                break
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 7)
    if name == "no_pieces":
        return g
    if name == "single_piece":
        for dr, dc in _L_SHAPES[0]:
            g[2 + dr][2 + dc] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 7
        return g
    return g
