"""Generator for arc_puzzle_bank_21_set22_s:S22_M6.

Several 5/6/7 candidate frames are present. Only the candidate with the same
oriented basis as the 2/3/4 source frame receives the copied motif.

Combinatorial axes (8): matching_slot, motif, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_candidates, no_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8df5d7bf679c"
VERSION = "1.1.0"
TASK_ID = "8df5d7bf679c"
SUMMARY = "Copy the source motif only into target frames with matching orientation."

INVARIANTS = [
    "source frame colors are 2, 3, 4",
    "candidate frames use colors 5, 6, 7",
    "exactly one candidate frame has the source frame's oriented basis",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_candidates", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "matching_slot":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "7", "valid": "6..8"},
    "position_bias":  {"type": "str", "default": "fixed_origins",
                       "valid": "fixed_origins"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "6..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SOURCE_BASIS = ((0, 1), (1, 0))
_OTHER_BASES = [
    ((1, 0), (0, -1)),
    ((0, -1), (-1, 0)),
    ((-1, 0), (0, 1)),
]
_TARGET_ORIGINS = [(3, 12), (7, 18), (9, 12)]
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
    matching_slot = ctx.draw_int("matching_slot", 0, 2)
    motif = _MOTIFS[ctx.draw_int("motif", 0, len(_MOTIFS) - 1)]
    source_origin = (7, 4)
    g = full_grid(13, 25, 0)
    _place(g, source_origin, _SOURCE_BASIS, [2, 3, 4])
    for u, v in motif:
        r, c = _global(source_origin, _SOURCE_BASIS, u, v)
        g[r][c] = 8
    other_idx = 0
    for i, origin in enumerate(_TARGET_ORIGINS):
        if i == matching_slot:
            basis = _SOURCE_BASIS
        else:
            basis = _OTHER_BASES[other_idx]
            other_idx += 1
        _place(g, origin, basis, [5, 6, 7])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 25, 0)
    if name == "no_source":
        # No 2/3/4 source frame — rule has no orientation reference.
        for i, origin in enumerate(_TARGET_ORIGINS):
            basis = _SOURCE_BASIS if i == 0 else _OTHER_BASES[i - 1]
            _place(g, origin, basis, [5, 6, 7])
        return g
    if name == "no_candidates":
        # Source present but no candidate frames — rule has nowhere to copy to.
        _place(g, (7, 4), _SOURCE_BASIS, [2, 3, 4])
        for u, v in _MOTIFS[0]:
            r, c = _global((7, 4), _SOURCE_BASIS, u, v)
            g[r][c] = 8
        return g
    if name == "no_match":
        # All candidates use rotated bases — no orientation match exists.
        _place(g, (7, 4), _SOURCE_BASIS, [2, 3, 4])
        for u, v in _MOTIFS[0]:
            r, c = _global((7, 4), _SOURCE_BASIS, u, v)
            g[r][c] = 8
        for origin, basis in zip(_TARGET_ORIGINS, _OTHER_BASES):
            _place(g, origin, basis, [5, 6, 7])
        return g
    return g
