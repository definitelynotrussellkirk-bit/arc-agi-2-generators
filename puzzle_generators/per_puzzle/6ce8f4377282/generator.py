"""Generator for arc_additional_puzzles_21_set17_bundle:M115 — fill compartments with majority marker color.

Rule: 8-walls divide the grid into compartments. Each compartment's
0-cells get repainted with the majority non-0/non-8 color present in
that compartment.

Combinatorial axes (8): n_markers_per_compartment, palette_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_markers, all_compartments_same.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "6ce8f4377282"
VERSION = "1.1.0"
TASK_ID = "6ce8f4377282"
SUMMARY = "8-walled grid of 4 compartments, each containing 1-2 same-color markers."

INVARIANTS = [
    "background is 0",
    "the 8-walls form a 2x2 compartment layout (rows 0,4,8 + cols 0,5,10 are 8)",
    "each compartment contains 1-2 markers, all of the same non-0/non-8 color",
    "different compartments may use different marker colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "all_compartments_same")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_markers_per_compartment": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "2x2_compartments_8walls",
                       "valid": "2x2_compartments_8walls"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..6"},
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
        n_markers = ctx.draw_int("n_markers_per_compartment", 1, 1)
    elif difficulty == "hard":
        n_markers = ctx.draw_int("n_markers_per_compartment", 2, 3)
    else:
        n_markers = ctx.draw_int("n_markers_per_compartment", 1, 2)
    rng = ctx.draw_rng("layout")
    h, w = 9, 11
    g = full_grid(h, w, 0)
    fill_box(g, 0, 0, 0, w - 1, 8)
    fill_box(g, 4, 0, 4, w - 1, 8)
    fill_box(g, h - 1, 0, h - 1, w - 1, 8)
    fill_box(g, 0, 0, h - 1, 0, 8)
    fill_box(g, 0, 5, h - 1, 5, 8)
    fill_box(g, 0, w - 1, h - 1, w - 1, 8)
    compartments = [
        (1, 1, 3, 4),
        (1, 6, 3, 9),
        (5, 1, 7, 4),
        (5, 6, 7, 9),
    ]
    used_colors: set[int] = set()
    for r1, c1, r2, c2 in compartments:
        candidates = [c for c in (1, 2, 3, 4, 5, 6, 7, 9) if c not in used_colors]
        color = rng.choice(candidates)
        used_colors.add(color)
        cells = [(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]
        rng.shuffle(cells)
        for (r, c) in cells[:n_markers]:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # Markers but no 8-walls — compartment boundaries undefined.
        g[2][2] = 4; g[2][7] = 6; g[6][2] = 7; g[6][7] = 1
        return g
    if name == "no_markers":
        # Walls present but every compartment is empty — rule has
        # no marker color to paint with.
        fill_box(g, 0, 0, 0, w - 1, 8)
        fill_box(g, 4, 0, 4, w - 1, 8)
        fill_box(g, h - 1, 0, h - 1, w - 1, 8)
        fill_box(g, 0, 0, h - 1, 0, 8)
        fill_box(g, 0, 5, h - 1, 5, 8)
        fill_box(g, 0, w - 1, h - 1, w - 1, 8)
        return g
    if name == "all_compartments_same":
        # All compartments share the same marker color — rule's per-
        # compartment differentiation collapses to a single fill color.
        fill_box(g, 0, 0, 0, w - 1, 8)
        fill_box(g, 4, 0, 4, w - 1, 8)
        fill_box(g, h - 1, 0, h - 1, w - 1, 8)
        fill_box(g, 0, 0, h - 1, 0, 8)
        fill_box(g, 0, 5, h - 1, 5, 8)
        fill_box(g, 0, w - 1, h - 1, w - 1, 8)
        for r, c in [(2, 2), (2, 7), (6, 2), (6, 7)]:
            g[r][c] = 4
        return g
    return g
