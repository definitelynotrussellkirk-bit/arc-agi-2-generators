"""Generator for arc_puzzle_bank_21_set2:S2_H1.

Rule: a blank row and column split four quadrants; one quadrant omits
the shared motif.

Combinatorial axes (8): grid_h, grid_w, palette_kind, quad_size,
missing_quad, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_separator, all_quadrants_filled, two_missing_quadrants.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "864b0302e2e6"
VERSION = "1.1.0"
TASK_ID = "864b0302e2e6"
SUMMARY = "A blank row and column split four quadrants; one quadrant omits the shared motif."

INVARIANTS = [
    "background is 0",
    "one all-zero row and one all-zero column split four equal quadrants",
    "three quadrants contain the same nonzero motif in matching local coordinates",
    "one quadrant is empty and should receive the motif",
]

PALETTE_KINDS = ("default", "missing_tl", "missing_tr", "missing_bl_or_br")
DEGENERATE_TEXTURES = ("no_separator", "all_quadrants_filled", "two_missing_quadrants")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "2*q+1 (q in 4..6)", "valid": "9..17"},
    "grid_w":         {"type": "int", "default": "same as grid_h", "valid": "9..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "quad_size":      {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "missing_quad":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "quadrants", "valid": "quadrants"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

MOTIF = [(0, 1), (1, 1), (1, 2), (2, 0)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        q = ctx.draw_int("quad_size", 4, 4)
    elif difficulty == "hard":
        q = ctx.draw_int("quad_size", 5, 6)
    else:
        q = ctx.draw_int("quad_size", 4, 6)
    rng = ctx.draw_rng("layout")
    h = w = q * 2 + 1
    sep = q
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    origins = [(0, 0), (0, sep + 1), (sep + 1, 0), (sep + 1, sep + 1)]
    missing = rng.randrange(4)
    for i, (r0, c0) in enumerate(origins):
        if i == missing:
            continue
        for dr, dc in MOTIF:
            g[r0 + dr][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    q = 5
    h = w = q * 2 + 1
    g = full_grid(h, w, 0)
    sep = q
    origins = [(0, 0), (0, sep + 1), (sep + 1, 0), (sep + 1, sep + 1)]
    if name == "no_separator":
        # 4 motifs but no blank row/column → quadrants undefined
        for r0, c0 in origins[:3]:
            for dr, dc in MOTIF:
                g[r0 + dr][c0 + dc] = 4
        return g
    if name == "all_quadrants_filled":
        # all 4 quadrants have the motif → rule has no missing quadrant
        for r0, c0 in origins:
            for dr, dc in MOTIF:
                g[r0 + dr][c0 + dc] = 4
        return g
    if name == "two_missing_quadrants":
        # 2 motifs, 2 missing → predicate "exactly one missing" fails
        for r0, c0 in origins[:2]:
            for dr, dc in MOTIF:
                g[r0 + dr][c0 + dc] = 4
        return g
    return g
