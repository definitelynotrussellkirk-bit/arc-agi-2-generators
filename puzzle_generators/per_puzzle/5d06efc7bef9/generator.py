"""Generator for 16b:hard_107 — build scale-normalized shape equivalence matrix.

Rule: 3 panels at cols [0, 7, 14] (6 wide each, full rows). Output 3x3:
8 if scale-normalized shape signatures match, else 0.

Combinatorial axes (8): panel_density, palette_kind, n_panels,
palette_size, position_bias, n_distinct_colors, scale_diversity, texture.
Degenerates: empty_panel, all_identical, no_scale_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d06efc7bef9"
VERSION = "1.1.0"
TASK_ID = "5d06efc7bef9"
SUMMARY = "3 panels at cols [0, 7, 14] (6 wide each) with binary content."

INVARIANTS = [
    "background is 0",
    "grid is 5 rows tall and 20 cols wide",
    "3 panels each holding 3-7 non-bg cells in a single color",
]

PALETTE_KINDS = ("default", "sparse", "dense", "balanced")
DEGENERATE_TEXTURES = ("empty_panel", "all_identical", "no_scale_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_density":  {"type": "str", "default": "mixed", "valid": "mixed"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_panels":       {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "scale_diversity": {"type": "str", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    h = 5; w = 20
    starts = [0, 7, 14]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    g = full_grid(h, w, 0)
    if difficulty == "easy":
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        n_lo, n_hi = 5, 7
    else:
        n_lo, n_hi = 3, 7
    for c0, color in zip(starts, palette):
        cells = [(r, c0 + dc) for r in range(5) for dc in range(6)]
        n = rng.randint(n_lo, n_hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 20
    g = full_grid(h, w, 0)
    starts = [0, 7, 14]
    if name == "empty_panel":
        # one panel empty — scale signature undefined
        for r, c in [(0, 0), (1, 1), (2, 2)]:
            g[r][c] = 1
        # middle panel empty
        for r, c in [(0, 14), (1, 15)]:
            g[r][c] = 3
        return g
    if name == "all_identical":
        # all 3 panels same shape at same scale — full match (trivial)
        for c0, color in zip(starts, [1, 2, 3]):
            for r, dc in [(0, 0), (1, 0), (1, 1)]:
                g[r][c0 + dc] = color
        return g
    if name == "no_scale_match":
        # 3 panels with totally different normalized shapes
        for r, dc in [(0, 0), (1, 0), (2, 0)]:
            g[r][0 + dc] = 1
        for r, dc in [(0, 0), (0, 1), (0, 2), (0, 3)]:
            g[r][7 + dc] = 2
        for r, dc in [(0, 0), (1, 1), (2, 2), (3, 3), (1, 0)]:
            g[r][14 + dc] = 3
        return g
    return g
