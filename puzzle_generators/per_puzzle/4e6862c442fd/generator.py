"""Generator for arc_puzzle_bank_21_set22_s:S22_M1.

Two colored local frames define coordinate bases. Color-8 source motif cells
near the 2/3/4 frame are copied into the 5/6/7 frame's local coordinates.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_source_frame, no_target_frame, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4e6862c442fd"
VERSION = "1.1.0"
TASK_ID = "4e6862c442fd"
SUMMARY = "Copy local color-8 motif coordinates from a source frame to a target frame."

INVARIANTS = [
    "source frame colors are 2 at origin, 3 on local u, and 4 on local v",
    "target frame colors are 5 at origin, 6 on local u, and 7 on local v",
    "motif cells are color 8 within local radius three of the source frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source_frame", "no_target_frame", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "target_basis":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "two_local_frames",
                       "valid": "two_local_frames"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BASES = [
    ((0, 1), (1, 0)),
    ((1, 0), (0, -1)),
    ((0, -1), (-1, 0)),
    ((-1, 0), (0, 1)),
]
_MOTIFS = [
    [(-1, 0), (1, 1), (2, -1)],
    [(-2, 0), (0, -2), (1, 1), (2, 0)],
    [(-1, -1), (0, 2), (2, 1)],
]


def _place(g, origin, basis, colors):
    vx, vy = basis
    r, c = origin
    g[r][c] = colors[0]
    g[r + vx[0]][c + vx[1]] = colors[1]
    g[r + vy[0]][c + vy[1]] = colors[2]


def _global(origin, basis, u, v):
    vx, vy = basis
    return origin[0] + u * vx[0] + v * vy[0], origin[1] + u * vx[1] + v * vy[1]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    source_origin = (6, 5)
    target_origin = (6, 13)
    source_basis = ((0, 1), (1, 0))
    target_basis = _BASES[ctx.draw_int("target_basis", 0, 3)]
    motif = _MOTIFS[ctx.draw_int("motif", 0, len(_MOTIFS) - 1)]
    g = full_grid(12, 18, 0)
    _place(g, source_origin, source_basis, [2, 3, 4])
    _place(g, target_origin, target_basis, [5, 6, 7])
    for u, v in motif:
        r, c = _global(source_origin, source_basis, u, v)
        g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 18, 0)
    src = (6, 5); tgt = (6, 13)
    src_basis = ((0, 1), (1, 0))
    tgt_basis = ((0, 1), (1, 0))
    if name == "no_source_frame":
        # Only target frame — rule's source-coordinate readout
        # fails; nothing to copy.
        _place(g, tgt, tgt_basis, [5, 6, 7])
        g[5][5] = 8
        return g
    if name == "no_target_frame":
        # Only source frame — rule has no target basis to paint
        # into; copy step is undefined.
        _place(g, src, src_basis, [2, 3, 4])
        g[5][5] = 8
        return g
    if name == "no_motif":
        # Both frames present but no color-8 cells — rule has
        # nothing to copy; output identical to input.
        _place(g, src, src_basis, [2, 3, 4])
        _place(g, tgt, tgt_basis, [5, 6, 7])
        return g
    return g
