"""Generator for arc_puzzle_bank_21_set22_s:S22_M4 — render motif bbox perimeter at target frame.

The source frame has a local color-8 motif. The rule renders only the
boundary of the motif's local bounding box in the target frame.

Combinatorial axes (8): target_basis, motif, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, no_target_frame, motif_at_origin.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "67aae675d447"
VERSION = "1.1.0"
TASK_ID = "67aae675d447"
SUMMARY = "Draw the source motif local bbox perimeter at the target frame."

INVARIANTS = [
    "source frame colors are 2, 3, 4",
    "target frame colors are 5, 6, 7",
    "source color-8 points define a local bounding box with an interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "no_target_frame", "motif_at_origin")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "target_basis":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "two_frames_basis",
                       "valid": "two_frames_basis"},
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
    [(-2, -1), (-1, 2), (1, 1), (2, -2)],
    [(-2, 0), (0, -2), (1, 2), (2, 1)],
    [(-1, -2), (0, 2), (2, -1), (2, 2)],
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
    target_origin = (6, 14)
    source_basis = ((0, 1), (1, 0))
    if difficulty == "easy":
        target_basis = _BASES[ctx.draw_int("target_basis", 0, 0)]
        motif = _MOTIFS[ctx.draw_int("motif", 0, 1)]
    elif difficulty == "hard":
        target_basis = _BASES[ctx.draw_int("target_basis", 1, 3)]
        motif = _MOTIFS[ctx.draw_int("motif", 0, len(_MOTIFS) - 1)]
    else:
        target_basis = _BASES[ctx.draw_int("target_basis", 0, 3)]
        motif = _MOTIFS[ctx.draw_int("motif", 0, len(_MOTIFS) - 1)]
    g = full_grid(13, 19, 0)
    _place(g, source_origin, source_basis, [2, 3, 4])
    _place(g, target_origin, target_basis, [5, 6, 7])
    for u, v in motif:
        r, c = _global(source_origin, source_basis, u, v)
        g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 19, 0)
    if name == "no_motif":
        # Both frames present but no color-8 motif points — rule has
        # no bbox to compute and render.
        _place(g, (6, 5), ((0, 1), (1, 0)), [2, 3, 4])
        _place(g, (6, 14), ((0, 1), (1, 0)), [5, 6, 7])
        return g
    if name == "no_target_frame":
        # Source frame + motif present but target frame missing — rule
        # has no destination to render the perimeter at.
        _place(g, (6, 5), ((0, 1), (1, 0)), [2, 3, 4])
        for u, v in _MOTIFS[0]:
            r, c = _global((6, 5), ((0, 1), (1, 0)), u, v)
            g[r][c] = 8
        return g
    if name == "motif_at_origin":
        # The motif consists of a single point coinciding with the
        # source origin — bbox is degenerate (single cell), perimeter
        # collapses to that one cell.
        _place(g, (6, 5), ((0, 1), (1, 0)), [2, 3, 4])
        _place(g, (6, 14), ((0, 1), (1, 0)), [5, 6, 7])
        g[6][5] = 8  # overwrite the origin with motif
        return g
    return g
