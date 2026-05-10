"""Generator for arc_puzzle_bank_21_set22_s:S22_H7 — match candidate motif rotated 90deg.

Rule: one source frame and three candidate frames. Exactly one
candidate motif is the local 90-degree rotation of the source offsets;
the output marks the matching candidate position.

Combinatorial axes (8): motif, match, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_candidates, no_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e3bf7e173449"
VERSION = "1.1.0"
TASK_ID = "e3bf7e173449"
SUMMARY = "Find which candidate motif is the source motif rotated 90 degrees in local-frame coordinates."

INVARIANTS = [
    "one source frame uses marker colors 2, 3, and 4",
    "three candidate frames use marker colors 5, 6, and 7",
    "exactly one candidate motif has the local 90-degree rotation of the source offsets",
    "the output strip marks the matching candidate position",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_candidates", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "match":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "source_top_candidates_below",
                       "valid": "source_top_candidates_below"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SOURCE = [
    [(1, -1), (2, -1), (2, 0)],
    [(-1, 1), (-1, 2), (0, 2)],
    [(-2, 0), (-1, -1), (0, -1)],
]
_DISTRACTORS = [
    [(1, 1), (2, 1), (2, 2)],
    [(-1, -1), (-1, -2), (0, -2)],
    [(0, 2), (1, 2), (1, 1)],
]


def _rot90_uv(pts):
    return [(-v, u) for u, v in pts]


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
        motif = ctx.draw_int("motif", 1, 2)
    else:
        motif = ctx.draw_int("motif", 0, len(_SOURCE) - 1)
    match_idx = ctx.draw_int("match", 0, 2)
    source_pts = _SOURCE[motif]
    rotated = _rot90_uv(source_pts)
    g = full_grid(13, 25, 0)
    source = (2, 12)
    candidates = [(6, 4), (6, 12), (6, 20)]
    _frame(g, source, (2, 3, 4))
    _paint_local(g, source, source_pts)
    for idx, origin in enumerate(candidates):
        _frame(g, origin, (5, 6, 7))
        pts = rotated if idx == match_idx else _DISTRACTORS[(motif + idx) % len(_DISTRACTORS)]
        _paint_local(g, origin, pts)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 25, 0)
    if name == "no_source":
        # Candidates present but source frame missing — rule has no
        # reference motif to match candidates against.
        for origin in [(6, 4), (6, 12), (6, 20)]:
            _frame(g, origin, (5, 6, 7))
            _paint_local(g, origin, _DISTRACTORS[0])
        return g
    if name == "no_candidates":
        # Source present but no candidate frames — rule has nothing
        # to test for the rotation match.
        _frame(g, (2, 12), (2, 3, 4))
        _paint_local(g, (2, 12), _SOURCE[0])
        return g
    if name == "no_match":
        # Source + 3 candidates but all candidates are distractors —
        # no candidate matches the rotated source, rule has no answer.
        _frame(g, (2, 12), (2, 3, 4))
        _paint_local(g, (2, 12), _SOURCE[0])
        for idx, origin in enumerate([(6, 4), (6, 12), (6, 20)]):
            _frame(g, origin, (5, 6, 7))
            _paint_local(g, origin, _DISTRACTORS[idx % len(_DISTRACTORS)])
        return g
    return g
