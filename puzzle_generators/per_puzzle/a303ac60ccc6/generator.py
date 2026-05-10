"""Generator for arc_puzzle_bank_21_set22_s:S22_M7 — copy max-distance motif points to target.

The source frame contains several local color-8 motif points. The rule
copies only the points with maximum local Manhattan distance into the
target frame.

Combinatorial axes (8): target_basis, motif, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, no_target_frame, all_equal_distance.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a303ac60ccc6"
VERSION = "1.1.0"
TASK_ID = "a303ac60ccc6"
SUMMARY = "Copy only farthest local motif points from source frame to target frame."

INVARIANTS = [
    "source frame colors are 2, 3, 4",
    "target frame colors are 5, 6, 7",
    "at least one color-8 source point has strictly maximal local distance",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "no_target_frame", "all_equal_distance")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "target_basis":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "two_frames_max_distance",
                       "valid": "two_frames_max_distance"},
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
    [(-1, 0), (1, 1), (2, -1), (0, 2)],
    [(-2, 0), (0, -1), (1, 1), (2, 1)],
    [(-1, -1), (0, 2), (2, 0), (1, -2)],
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
    if difficulty == "easy":
        target_basis = _BASES[ctx.draw_int("target_basis", 0, 0)]
        motif = _MOTIFS[ctx.draw_int("motif", 0, 0)]
    elif difficulty == "hard":
        target_basis = _BASES[ctx.draw_int("target_basis", 1, 3)]
        motif = _MOTIFS[ctx.draw_int("motif", 0, len(_MOTIFS) - 1)]
    else:
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
    if name == "no_motif":
        # Both frames present but no color-8 motif points — rule has
        # no points to filter for max distance.
        _place(g, (6, 5), ((0, 1), (1, 0)), [2, 3, 4])
        _place(g, (6, 13), ((0, 1), (1, 0)), [5, 6, 7])
        return g
    if name == "no_target_frame":
        # Source frame + motif present but target frame missing — rule
        # has no destination to copy to.
        _place(g, (6, 5), ((0, 1), (1, 0)), [2, 3, 4])
        for u, v in _MOTIFS[0]:
            r, c = _global((6, 5), ((0, 1), (1, 0)), u, v)
            g[r][c] = 8
        return g
    if name == "all_equal_distance":
        # All motif points sit at exactly the same local distance —
        # there's no strict max, the rule's selection is ambiguous.
        _place(g, (6, 5), ((0, 1), (1, 0)), [2, 3, 4])
        _place(g, (6, 13), ((0, 1), (1, 0)), [5, 6, 7])
        for u, v in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = _global((6, 5), ((0, 1), (1, 0)), u, v)
            g[r][c] = 8
        return g
    return g
