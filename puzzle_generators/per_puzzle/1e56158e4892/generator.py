"""Generator for hard_137_build_rotation_relation_matrix.

Rule: 4 fixed 5×5 panels at columns [0, 6, 12, 18]. Output 4×4 matrix:
8 on diagonal; 1 if normalized panels equal; 2 if rotation-equivalent;
0 otherwise.

Combinatorial axes (8): grid_h/w, palette_kind, num_panels, panel_density,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_panels_equivalent, all_panels_unique, empty_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e56158e4892"
VERSION = "1.1.0"
TASK_ID = "1e56158e4892"
SUMMARY = "4 5-wide panels at cols [0, 6, 12, 18] with binary content."

INVARIANTS = [
    "background is 0",
    "grid is 5 rows tall and 23 cols wide",
    "4 panels each holding 3-7 non-bg cells in a single color",
]

PALETTE_KINDS = ("default", "sparse_panels", "dense_panels", "varied")
DEGENERATE_TEXTURES = ("all_panels_equivalent", "all_panels_unique", "empty_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "23", "valid": "23"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_panels":     {"type": "int", "default": "4", "valid": "4"},
    "panel_density":  {"type": "str", "default": "rng 3..7",
                       "valid": "3..7"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed_cols",
                       "valid": "fixed_cols"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_STARTS = [0, 6, 12, 18]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        density_lo, density_hi = 3, 4
    elif difficulty == "hard":
        density_lo, density_hi = 5, 7
    else:
        density_lo, density_hi = 3, 7
    h = 5
    w = 23
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    g = full_grid(h, w, 0)
    for c0, color in zip(_STARTS, palette):
        cells = [(r, c0 + dc) for r in range(5) for dc in range(5)]
        n = rng.randint(density_lo, density_hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 23, 0)
    palette = [3, 4, 5, 6]
    base_pattern = [(0, 0), (0, 1), (1, 0), (2, 2), (4, 4)]
    if name == "all_panels_equivalent":
        # all panels are exact rotations of one shape — relation matrix is mostly 1s/2s
        for c0, color in zip(_STARTS, palette):
            for dr, dc in base_pattern:
                g[dr][c0 + dc] = color
        return g
    if name == "all_panels_unique":
        # all panels distinct under rotation — diagonal-only matrix
        patterns = [
            [(0, 0), (1, 0), (2, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
        ]
        for c0, color, pat in zip(_STARTS, palette, patterns):
            for dr, dc in pat:
                g[dr][c0 + dc] = color
        return g
    if name == "empty_panels":
        return g
    return g
