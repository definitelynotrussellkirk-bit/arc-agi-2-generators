"""Generator for arc_puzzle_bank_21_set9_s:S9_H7.

Rule: three equal panels separated by 5-bars; cells occupied in at
least two panels merge to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_h, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, no_overlap_positions, single_panel_active.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8f10b83435aa"
VERSION = "1.1.0"
TASK_ID = "8f10b83435aa"
SUMMARY = "Three equal panels separated by 5-bars; cells occupied in at least two panels merge to 8."

INVARIANTS = [
    "background is 0",
    "two full-height color-5 divider columns split three equal panels",
    "panels share dimensions",
    "some positions are occupied in exactly two or three panels",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "no_overlap_positions", "single_panel_active")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "panel_w":        {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_positions":    {"type": "int", "default": "10", "valid": "1..40"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7"},
    "position_bias":  {"type": "str", "default": "three_panels_majority",
                       "valid": "three_panels_majority"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7"},
    "density":        {"type": "str", "default": "panels", "valid": "panels"},
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
        ph = ctx.draw_int("panel_h", 5, 5)
        pw = ctx.draw_int("panel_w", 5, 6)
    elif difficulty == "hard":
        ph = ctx.draw_int("panel_h", 6, 7)
        pw = ctx.draw_int("panel_w", 6, 7)
    else:
        ph = ctx.draw_int("panel_h", 5, 7)
        pw = ctx.draw_int("panel_w", 5, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(ph, 3 * pw + 2, 0)
    for r in range(ph):
        g[r][pw] = 5
        g[r][2 * pw + 1] = 5
    colors = [1, 2, 3, 4, 6, 7, 9]
    positions = rng.sample([(r, c) for r in range(ph) for c in range(pw)], min(10, ph * pw))
    for i, (r, c) in enumerate(positions):
        panels = [0, 1, 2] if i % 4 == 0 else rng.sample([0, 1, 2], 2)
        for panel in panels:
            offset = panel * (pw + 1)
            g[r][offset + c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    ph, pw = 5, 5
    g = full_grid(ph, 3 * pw + 2, 0)
    if name == "no_dividers":
        # cells without 5-divider columns → panel boundaries undefined
        for r, c in [(1, 1), (2, 8), (3, 12)]:
            g[r][c] = 4
        return g
    if name == "no_overlap_positions":
        # each position occupied in only one panel → no ≥2-panel merges, output empty
        for r in range(ph):
            g[r][pw] = 5; g[r][2 * pw + 1] = 5
        g[1][1] = 4         # panel 0 only
        g[2][pw + 2] = 6    # panel 1 only
        g[3][2 * pw + 3] = 7 # panel 2 only
        return g
    if name == "single_panel_active":
        # only panel 0 has any cells → no overlap ever, output empty
        for r in range(ph):
            g[r][pw] = 5; g[r][2 * pw + 1] = 5
        for r, c in [(1, 1), (2, 2), (3, 1)]:
            g[r][c] = 4
        return g
    return g
