"""Generator for arc_puzzle_bank_fourth_21_bundle:easy_28_mirror_singletons_across_horizontal_midline.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, markers_in_bottom, markers_on_midline.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b22fce018c84"
VERSION = "1.1.0"
TASK_ID = "b22fce018c84"
SUMMARY = "Color-7 singleton markers are mirrored across the horizontal midline."

INVARIANTS = [
    "background is 0",
    "all nonzero cells are color 7",
    "markers begin in the top half",
    "their horizontal mirror positions are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "markers_in_bottom", "markers_on_midline")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "top_half", "valid": "top_half"},
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
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n_markers = ctx.draw_int("n_markers", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        n_markers = ctx.draw_int("n_markers", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 8, 12)
        n_markers = ctx.draw_int("n_markers", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    top_rows = list(range(max(1, h // 2)))
    cells = [(r, c) for r in top_rows for c in range(w)]
    rng.shuffle(cells)
    for r, c in cells[:n_markers]:
        g[r][c] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # no markers → nothing to mirror, rule is no-op
        return g
    if name == "markers_in_bottom":
        # markers in bottom half → "begin in top half" invariant violated
        for r, c in [(5, 2), (6, 5), (7, 8)]:
            g[r][c] = 7
        return g
    if name == "markers_on_midline":
        # markers on the midline (or symmetric pre-image already filled) → mirror equals self
        for r, c in [(2, 3), (5, 3), (2, 6), (5, 6)]:
            g[r][c] = 7
        return g
    return g
