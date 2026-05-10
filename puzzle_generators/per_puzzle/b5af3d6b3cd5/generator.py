"""Generator for arc_puzzle_bank_eighteenth_21_bundle:medium_122_apply_gravity_in_each_walled_chamber.

Rule: 5-walls divide the grid into rectangular chambers. Each
chamber's non-0/non-5 markers gravity-down to the chamber's bottom
row, packed left-to-right (preserving order top-to-bottom).

Combinatorial axes (8): n_markers_per_chamber, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_markers, single_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "b5af3d6b3cd5"
VERSION = "1.1.0"
TASK_ID = "b5af3d6b3cd5"
SUMMARY = "5-walled grid (2x2 layout of chambers, each ~3x3) with 2-3 colored markers per chamber."

INVARIANTS = [
    "background is 0",
    "5-walls form a 2×2 chamber layout (rows 0,4,8 + cols 0,4,8/10 are 5)",
    "each chamber holds 2-3 markers in distinct non-0/non-5 colors",
    "markers don't fill the chamber's bottom row already",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "single_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_markers_per_chamber": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "2x2_chambers_5walls",
                       "valid": "2x2_chambers_5walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..4"},
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
        n_markers = ctx.draw_int("n_markers_per_chamber", 2, 2)
    elif difficulty == "hard":
        n_markers = ctx.draw_int("n_markers_per_chamber", 3, 4)
    else:
        n_markers = ctx.draw_int("n_markers_per_chamber", 2, 3)
    rng = ctx.draw_rng("layout")
    h, w = 9, 11
    g = full_grid(h, w, 0)
    fill_box(g, 0, 0, 0, w - 1, 5)
    fill_box(g, 4, 0, 4, w - 1, 5)
    fill_box(g, h - 1, 0, h - 1, w - 1, 5)
    fill_box(g, 0, 0, h - 1, 0, 5)
    fill_box(g, 0, 4, h - 1, 4, 5)
    fill_box(g, 0, w - 1, h - 1, w - 1, 5)
    chambers = [
        (1, 1, 3, 3),
        (1, 5, 3, 9),
        (5, 1, 7, 3),
        (5, 5, 7, 9),
    ]
    for r1, c1, r2, c2 in chambers:
        cells = [(r, c) for r in range(r1, r2) for c in range(c1, c2 + 1)]
        rng.shuffle(cells)
        for (r, c), color in zip(cells[:n_markers],
                                  rng.sample([1, 2, 3, 4], n_markers)):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # Markers but no 5-walls — chamber layout undefined, rule's gravity
        # has no chamber bottom row to settle on.
        g[2][2] = 1; g[2][6] = 2
        g[6][2] = 3; g[6][6] = 4
        return g
    if name == "no_markers":
        # Walls present but every chamber is empty — rule gravity has
        # nothing to drop.
        fill_box(g, 0, 0, 0, w - 1, 5)
        fill_box(g, 4, 0, 4, w - 1, 5)
        fill_box(g, h - 1, 0, h - 1, w - 1, 5)
        fill_box(g, 0, 0, h - 1, 0, 5)
        fill_box(g, 0, 4, h - 1, 4, 5)
        fill_box(g, 0, w - 1, h - 1, w - 1, 5)
        return g
    if name == "single_chamber":
        # Outer 5-frame only (no internal walls) — just one chamber, so
        # no per-chamber comparison is possible.
        fill_box(g, 0, 0, 0, w - 1, 5)
        fill_box(g, h - 1, 0, h - 1, w - 1, 5)
        fill_box(g, 0, 0, h - 1, 0, 5)
        fill_box(g, 0, w - 1, h - 1, w - 1, 5)
        g[2][3] = 1; g[3][6] = 2
        return g
    return g
