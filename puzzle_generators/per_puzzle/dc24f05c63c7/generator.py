"""Generator for arc_puzzle_bank_21_set22_s:S22_M3.

The source frame has a local color-8 motif. The rule fills the motif's local
bounding box in the target frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_basis, motif,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_target, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dc24f05c63c7"
VERSION = "1.1.0"
TASK_ID = "dc24f05c63c7"
SUMMARY = "Fill the source motif local bounding box at the target frame."

INVARIANTS = [
    "source frame colors are 2, 3, 4",
    "target frame colors are 5, 6, 7",
    "source motif color-8 cells define a nontrivial local bounding box",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_target", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_basis":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "source_frame_plus_target_frame_plus_motif",
                       "valid": "source_frame_plus_target_frame_plus_motif"},
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
    if difficulty == "easy":
        target_basis = _BASES[ctx.draw_int("target_basis", 0, 1)]
        motif = _MOTIFS[ctx.draw_int("motif", 0, 1)]
    elif difficulty == "hard":
        target_basis = _BASES[ctx.draw_int("target_basis", 2, 3)]
        motif = _MOTIFS[ctx.draw_int("motif", 1, 2)]
    else:
        target_basis = _BASES[ctx.draw_int("target_basis", 0, 3)]
        motif = _MOTIFS[ctx.draw_int("motif", 0, len(_MOTIFS) - 1)]
    source_origin = (6, 5)
    target_origin = (6, 13)
    source_basis = ((0, 1), (1, 0))
    g = full_grid(12, 18, 0)
    _place(g, source_origin, source_basis, [2, 3, 4])
    _place(g, target_origin, target_basis, [5, 6, 7])
    for u, v in motif:
        r, c = _global(source_origin, source_basis, u, v)
        g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 18, 0)
    source_origin = (6, 5)
    target_origin = (6, 13)
    source_basis = ((0, 1), (1, 0))
    target_basis = _BASES[0]
    if name == "no_source":
        # target frame + motif but no source frame → no source basis to read motif against
        _place(g, target_origin, target_basis, [5, 6, 7])
        for u, v in _MOTIFS[0]:
            r, c = _global(source_origin, source_basis, u, v)
            g[r][c] = 8
        return g
    if name == "no_target":
        # source + motif but no target frame → no destination to fill
        _place(g, source_origin, source_basis, [2, 3, 4])
        for u, v in _MOTIFS[0]:
            r, c = _global(source_origin, source_basis, u, v)
            g[r][c] = 8
        return g
    if name == "no_motif":
        # both frames present but no motif → no bounding box to copy
        _place(g, source_origin, source_basis, [2, 3, 4])
        _place(g, target_origin, target_basis, [5, 6, 7])
        return g
    return g
