"""Generator for 18b:hard_124 — build pairwise xor gallery.

Rule: input is split into 3 fixed 4x4 panels (cols 0-3, 5-8, 10-13).
Output is a 3x3 gallery (with 1-row/col gaps) of pairwise XORs (color 7
where exactly one panel has a non-bg cell at that position).

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: blank_panels, identical_panels, missing_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "907bb29fbac5"
VERSION = "1.1.0"
TASK_ID = "907bb29fbac5"
SUMMARY = "4x14 input with 3 4x4 panels (cols 0-3, 5-8, 10-13) of color 6."

INVARIANTS = [
    "background is 0",
    "grid is 4 rows tall and 14 cols wide",
    "3 panels at cols [0..3], [5..8], [10..13]; each holds 3-7 non-bg cells of color 6",
    "panels are mutually distinct (no two are the same shape)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("blank_panels", "identical_panels", "missing_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..4"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_cell_count": {"type": "int", "default": "rng 3..7 per panel",
                         "valid": "1..16"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "three_4x4_panels",
                       "valid": "three_4x4_panels"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        cmin, cmax = 3, 4
    elif difficulty == "hard":
        cmin, cmax = 5, 7
    else:
        cmin, cmax = 3, 7
    h = 4; w = 14
    starts = [0, 5, 10]
    for _ in range(40):
        g = full_grid(h, w, 0)
        masks = []
        for c0 in starts:
            cells = [(r, c0 + dc) for r in range(4) for dc in range(4)]
            n = rng.randint(cmin, cmax)
            slots = rng.sample(cells, n)
            mask = [[0] * 4 for _ in range(4)]
            for r, c in slots:
                g[r][c] = 6
                mask[r][c - c0] = 1
            masks.append(tuple(tuple(row) for row in mask))
        if len(set(masks)) == 3:
            return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 14
    g = full_grid(h, w, 0)
    starts = [0, 5, 10]
    if name == "blank_panels":
        # all 3 panels empty → XOR gallery is all zeros
        return g
    if name == "identical_panels":
        # all 3 panels have the same shape → pairwise XORs are all empty
        cells = [(0, 0), (1, 1), (2, 2)]
        for c0 in starts:
            for r, dc in cells:
                g[r][c0 + dc] = 6
        return g
    if name == "missing_panel":
        # one panel completely empty → "3 distinct" precondition fails
        for r, dc in [(0, 0), (1, 1), (2, 2)]:
            g[r][0 + dc] = 6
        for r, dc in [(0, 1), (1, 0), (2, 1), (3, 2)]:
            g[r][5 + dc] = 6
        return g
    return g
