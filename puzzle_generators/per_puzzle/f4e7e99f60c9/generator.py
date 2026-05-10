"""Generator for arc_additional_puzzles_21_set16_bundle:M112.

Rule: 5-walls divide grid into compartments. For each compartment, if
it has exactly one non-{0,5} marker color, fill empty cells with it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_compartments,
palette_size, position_bias, n_distinct_colors, marker_kind, texture.
Degenerates: no_walls, no_markers, two_markers_one_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f4e7e99f60c9"
VERSION = "1.1.0"
TASK_ID = "f4e7e99f60c9"
SUMMARY = "5-walls divide grid into 4 compartments; each has exactly one marker."

INVARIANTS = [
    "5-walls form a 2x2 grid of compartments",
    "each compartment has exactly one marker of distinct non-{0,5} color",
]

PALETTE_KINDS = ("default", "warm_markers", "cool_markers", "varied_markers")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "two_markers_one_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_compartments": {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "compartment_centers",
                       "valid": "compartment_centers"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "marker_kind":    {"type": "str", "default": "single", "valid": "single"},
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
    h, w = 9, 11
    g = full_grid(h, w, 5)
    for ri, r0 in enumerate([1, 5]):
        for ci, c0 in enumerate([1, 6]):
            for r in range(r0, r0 + 3):
                for c in range(c0, c0 + 4):
                    if r < h - 1 and c < w - 1: g[r][c] = 0
    palette = [2, 3, 4, 6, 7, 8, 9]; rng.shuffle(palette)
    spots = [(2, 2), (2, 7), (6, 2), (6, 8)]
    rng.shuffle(spots)
    for i, (sr, sc) in enumerate(spots):
        g[sr][sc] = palette[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    if name == "no_walls":
        # markers but no 5-walls → chambers undefined; flood reaches everywhere
        g = full_grid(h, w, 0)
        for sr, sc, v in [(2, 2, 4), (2, 7, 6), (6, 2, 7), (6, 8, 9)]:
            g[sr][sc] = v
        return g
    if name == "no_markers":
        # walled chambers but no markers → fill source undefined
        g = full_grid(h, w, 5)
        for ri, r0 in enumerate([1, 5]):
            for ci, c0 in enumerate([1, 6]):
                for r in range(r0, r0 + 3):
                    for c in range(c0, c0 + 4):
                        if r < h - 1 and c < w - 1:
                            g[r][c] = 0
        return g
    if name == "two_markers_one_chamber":
        # one chamber holds two distinct markers → "exactly one" predicate fails
        g = full_grid(h, w, 5)
        for ri, r0 in enumerate([1, 5]):
            for ci, c0 in enumerate([1, 6]):
                for r in range(r0, r0 + 3):
                    for c in range(c0, c0 + 4):
                        if r < h - 1 and c < w - 1:
                            g[r][c] = 0
        g[2][2] = 4; g[2][3] = 6
        g[2][7] = 7
        g[6][2] = 8
        g[6][8] = 9
        return g
    return full_grid(h, w, 0)
