"""Generator for arc_puzzle_bank_21_set22_s:S22_H1.

Mark the single candidate whose local-frame motif differs from the other candidates.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, all_same, all_distinct.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c7a821733003"
VERSION = "1.1.0"
TASK_ID = "c7a821733003"
SUMMARY = "Mark the single candidate whose local-frame motif differs from the other candidates."

INVARIANTS = [
    "one source frame uses marker colors 2, 3, and 4",
    "three candidate frames use marker colors 5, 6, and 7",
    "two candidate motifs share identical local offsets",
    "one candidate motif has a unique local-offset signature and is marked in the output strip",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "all_same", "all_distinct")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "25", "valid": "25..25"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "source_plus_3_candidates",
                       "valid": "source_plus_3_candidates"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_COMMON = [
    [(1, -1), (2, -1), (2, 0)],
    [(-1, 1), (-1, 2), (0, 2)],
    [(-2, 0), (-1, 0), (-1, 1)],
]
_ODD = [
    [(1, 1), (1, 2), (2, 2)],
    [(-1, -1), (-2, -1), (-2, 0)],
    [(0, -2), (1, -2), (1, -1)],
]


def _frame(g, origin, colors):
    r, c = origin
    g[r][c] = colors[0]
    g[r][c + 1] = colors[1]
    g[r + 1][c] = colors[2]


def _paint_local(g, origin, pts):
    r0, c0 = origin
    for u, v in pts:
        g[r0 + v][c0 + u] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        motif = ctx.draw_int("motif", 0, 0)
    elif difficulty == "hard":
        motif = ctx.draw_int("motif", 0, len(_COMMON) - 1)
    else:
        motif = ctx.draw_int("motif", 0, len(_COMMON) - 1)
    odd_idx = ctx.draw_int("odd", 0, 2)
    g = full_grid(13, 25, 0)
    source = (2, 12)
    candidates = [(6, 4), (6, 12), (6, 20)]
    _frame(g, source, (2, 3, 4))
    _paint_local(g, source, _COMMON[motif])
    for idx, origin in enumerate(candidates):
        _frame(g, origin, (5, 6, 7))
        _paint_local(g, origin, _ODD[motif] if idx == odd_idx else _COMMON[motif])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 25, 0)
    candidates = [(6, 4), (6, 12), (6, 20)]
    if name == "no_source":
        # candidates without source motif → no template to compare against
        for origin in candidates:
            _frame(g, origin, (5, 6, 7))
            _paint_local(g, origin, _COMMON[0])
        return g
    if name == "all_same":
        # 3 candidates all match common → no odd one out
        _frame(g, (2, 12), (2, 3, 4))
        _paint_local(g, (2, 12), _COMMON[0])
        for origin in candidates:
            _frame(g, origin, (5, 6, 7))
            _paint_local(g, origin, _COMMON[0])
        return g
    if name == "all_distinct":
        # 3 candidates each unique → no shared pair, ambiguous
        _frame(g, (2, 12), (2, 3, 4))
        _paint_local(g, (2, 12), _COMMON[0])
        _frame(g, candidates[0], (5, 6, 7))
        _paint_local(g, candidates[0], _COMMON[0])
        _frame(g, candidates[1], (5, 6, 7))
        _paint_local(g, candidates[1], _COMMON[1])
        _frame(g, candidates[2], (5, 6, 7))
        _paint_local(g, candidates[2], _ODD[0])
        return g
    return g
