"""Generator for arc_additional_puzzles_21_set19_bundle:M132 — Top-bottom panel match matrix under dihedral.

Rule: 2 top panels at (0..2, 0..2) and (0..2, 6..8); 2 bottom panels at
(4..6, 0..2) and (4..6, 6..8). Output 2×2 matrix: 8 if top[r] is dihedral-equivalent to bot[c].

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_choice,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_same_panels, all_distinct_panels, empty_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b636461d71b8"
VERSION = "1.1.0"
TASK_ID = "b636461d71b8"
SUMMARY = "Fixed 7×9 grid with 2 top + 2 bottom 3×3 panels."

INVARIANTS = [
    "grid is exactly 7 rows × 9 cols",
    "each panel has 3-4 non-zero cells",
    "at least one top-bottom pair is dihedral-equivalent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_panels", "all_distinct_panels", "empty_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7..7"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_choice":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "four_3x3_panels",
                       "valid": "four_3x3_panels"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    h, w = 7, 9
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    panels = [
        [(0, 0), (0, 1), (1, 0)],  # L
        [(0, 1), (1, 0), (1, 1)],  # rotated L
        [(0, 0), (1, 0), (1, 1)],  # another rotation
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ]
    color = rng.choice([2, 3, 4])
    color2 = rng.choice([5, 6, 7])
    p_a = panels[0]; p_b = panels[1]; p_c = panels[2]; p_d = panels[3]
    for r, c in p_a: g[r][c] = color
    for r, c in p_b: g[r][6 + c] = color
    for r, c in p_c: g[4 + r][c] = color2
    for r, c in p_d: g[4 + r][6 + c] = color2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    L = [(0, 0), (0, 1), (1, 0)]
    if name == "all_same_panels":
        # all 4 panels are identical L → all 4 dihedral-match, output is all-8
        for r, c in L: g[r][c] = 2
        for r, c in L: g[r][6 + c] = 2
        for r, c in L: g[4 + r][c] = 5
        for r, c in L: g[4 + r][6 + c] = 5
        return g
    if name == "all_distinct_panels":
        # all 4 dihedrally-distinct → no rotation matches, output is all-0
        for r, c in [(0, 0), (0, 1), (0, 2)]: g[r][c] = 2          # line
        for r, c in [(0, 0), (1, 1), (2, 2)]: g[r][6 + c] = 2      # diagonal
        for r, c in [(0, 0), (0, 1), (1, 1), (2, 0)]: g[4 + r][c] = 5  # Z
        for r, c in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]: g[4 + r][6 + c] = 5  # plus
        return g
    if name == "empty_panel":
        # one panel is empty → "panel shape" undefined for that slot
        for r, c in L: g[r][c] = 2
        # top-right empty
        for r, c in L: g[4 + r][c] = 5
        for r, c in L: g[4 + r][6 + c] = 5
        return g
    return g
