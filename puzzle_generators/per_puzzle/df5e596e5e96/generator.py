"""Generator for 19b:hard_132 — build dihedral relation matrix.

Rule: 3 fixed 5-wide panels, split row-fixed. Output 3x3:
  - i==j: 8
  - panel j == panel i: 1
  - panel j ∈ rotation(panel i): 2
  - panel j ∈ dihedral(panel i): 3
  - else: 0

Combinatorial axes (8): panel_density, palette_kind, n_panels,
palette_size, position_bias, n_distinct_colors, panel_diversity, texture.
Degenerates: empty_panel, all_identical, no_dihedral_relations.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "df5e596e5e96"
VERSION = "1.1.0"
TASK_ID = "df5e596e5e96"
SUMMARY = "3 5-wide panels at cols [0..4, 6..10, 12..16] with binary content."

INVARIANTS = [
    "background is 0",
    "grid is 5 rows tall and 17 cols wide",
    "3 panels each holding 3-7 non-bg cells in a single color",
]

PALETTE_KINDS = ("default", "sparse", "dense", "balanced")
DEGENERATE_TEXTURES = ("empty_panel", "all_identical", "no_dihedral_relations")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_density":  {"type": "str", "default": "mixed", "valid": "mixed"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_panels":       {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "panel_diversity": {"type": "str", "default": "varied", "valid": "varied"},
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
    h = 5; w = 17
    starts = [0, 6, 12]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    g = full_grid(h, w, 0)
    if difficulty == "easy":
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        n_lo, n_hi = 5, 7
    else:
        n_lo, n_hi = 3, 7
    for c0, color in zip(starts, palette):
        cells = [(r, c0 + dc) for r in range(5) for dc in range(5)]
        n = rng.randint(n_lo, n_hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 17
    g = full_grid(h, w, 0)
    if name == "empty_panel":
        # one panel empty — relation row/col is trivially undefined
        for r, c in [(0, 0), (1, 1), (2, 2)]:
            g[r][c] = 1
        # middle panel left empty
        for r, c in [(0, 12), (1, 13)]:
            g[r][c] = 3
        return g
    if name == "all_identical":
        # all 3 panels identical → all '1' off-diagonal, no rotation/dihedral signal
        for c0, color in zip([0, 6, 12], [1, 2, 3]):
            for r, dc in [(0, 0), (1, 0), (2, 1)]:
                g[r][c0 + dc] = color
        return g
    if name == "no_dihedral_relations":
        # 3 panels with totally distinct shapes (no shared rotation orbit)
        for r, dc in [(0, 0), (1, 1), (2, 2)]:
            g[r][0 + dc] = 1
        for r, dc in [(0, 0), (0, 1), (1, 2)]:
            g[r][6 + dc] = 2
        for r, dc in [(2, 0), (2, 1), (1, 2), (0, 3)]:
            g[r][12 + dc] = 3
        return g
    return g
