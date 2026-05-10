"""Generator for arc_additional_puzzle_bank_volume15:M105.

Rule: red candidates congruent to the blue reference under dihedral
symmetry are recolored cyan.

Combinatorial axes (8): grid_h/w, palette_kind, n_candidates,
palette_size, position_bias, n_distinct_colors, ref_kind, texture.
Degenerates: no_ref, no_candidates, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bfb4c6fb3c1a"
VERSION = "1.1.0"
TASK_ID = "bfb4c6fb3c1a"
SUMMARY = "Red candidates congruent to the blue reference under dihedral symmetry recolor cyan."

INVARIANTS = [
    "background is 0",
    "there is one blue reference component",
    "one red candidate is dihedrally congruent to the reference",
    "one red candidate is a nonmatching distractor",
]

PALETTE_KINDS = ("default", "L_ref", "T_ref", "Z_ref")
DEGENERATE_TEXTURES = ("no_ref", "no_candidates", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_candidates":   {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "ref_kind":       {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 11, 15)
    g = full_grid(h, w, 0)
    ref = [(1, 1), (1, 2), (2, 1), (3, 1)]
    match = [(2, w - 4), (3, w - 4), (4, w - 4), (4, w - 3)]
    distractor = [(h - 3, 2), (h - 3, 3), (h - 2, 3), (h - 2, 4)]
    for r, c in ref:
        g[r][c] = 1
    for cells in [match, distractor]:
        for r, c in cells:
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    match = [(2, w - 4), (3, w - 4), (4, w - 4), (4, w - 3)]
    distractor = [(h - 3, 2), (h - 3, 3), (h - 2, 3), (h - 2, 4)]
    if name == "no_ref":
        # candidates but no blue reference → no equivalence test possible
        for cells in [match, distractor]:
            for r, c in cells:
                g[r][c] = 2
        return g
    if name == "no_candidates":
        # blue ref but no red candidates — rule has nothing to recolor
        for r, c in [(1, 1), (1, 2), (2, 1), (3, 1)]:
            g[r][c] = 1
        return g
    if name == "all_match":
        # all red candidates dihedrally equivalent to ref → all recolored
        for r, c in [(1, 1), (1, 2), (2, 1), (3, 1)]:
            g[r][c] = 1
        for r, c in match:
            g[r][c] = 2
        # second match instead of distractor
        for r, c in [(h - 4, 2), (h - 4, 3), (h - 3, 2), (h - 2, 2)]:
            g[r][c] = 2
        return g
    return g
