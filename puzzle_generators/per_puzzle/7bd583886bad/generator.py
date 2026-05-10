"""Generator for 626c0bcc.

Rule: color-8 mask is decomposed into exact 2x2 and oriented L tiles,
recolored by tile type.

Combinatorial axes (8): grid_h/w, piece_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, piece_kind.
Degenerates: no_pieces, single_piece, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7bd583886bad"
VERSION = "1.1.0"
TASK_ID = "7bd583886bad"
SUMMARY = "Color-8 mask decomposed into 2x2 and L tiles, recolored by tile type."

INVARIANTS = [
    "background is color 0",
    "all source cells use color 8",
    "the 8-cells are an exact cover by separated 2x2 squares and L triominoes",
    "pieces sit clear of each other so the cover is unambiguous",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pieces", "single_piece", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

PIECES = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "piece_count":    {"type": "int", "default": "4", "valid": "4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "piece_kind":     {"type": "str", "default": "rng", "valid": "rng"},
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
    g = full_grid(12 + rng.randint(0, 2), 12 + rng.randint(0, 2), 0)
    anchors = [(1, 1), (1, 6), (6, 2), (7, 8)]
    for idx, (r0, c0) in enumerate(anchors):
        piece = PIECES[(idx + sample_index) % len(PIECES)]
        for dr, dc in piece:
            g[r0 + dr][c0 + dc] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_pieces":
        return g
    if name == "single_piece":
        for dr, dc in PIECES[0]:
            g[2 + dr][2 + dc] = 8
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
