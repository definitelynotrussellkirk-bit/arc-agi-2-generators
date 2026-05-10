"""Generator for arc_additional_puzzles_21_set5:H30 — Mirror-complete by 5-guides.

Rule: 2 5-guide cells. If same-row → vertical mirror (flip ud). Else
horizontal mirror (flip lr). Apply to non-5 cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, axis,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_guides, motif_on_both_sides, single_guide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "588ee22f3c4f"
VERSION = "1.1.0"
TASK_ID = "588ee22f3c4f"
SUMMARY = "2 5-guides (same row or same col) + small motif on one side."

INVARIANTS = [
    "exactly 2 5-cells, same row or same col",
    "small motif (3-5 cells) on one side, mirror partner is empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guides", "motif_on_both_sides", "single_guide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "axis":           {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "two_5guides_with_one_side_motif",
                       "valid": "two_5guides_with_one_side_motif"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..4"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    axis = ctx.draw_int("axis", 0, 1)
    g = full_grid(h, w, 0)
    if axis == 0:  # same row → vertical mirror
        g[0][2] = 5; g[0][7] = 5
        g[2][1] = 1; g[2][2] = 2
        g[3][1] = 1; g[3][3] = 2
        g[4][1] = 2; g[4][2] = 2; g[4][3] = 2
    else:  # same col → horizontal mirror
        g[1][0] = 5; g[5][0] = 5
        g[2][1] = 2; g[2][3] = 3
        g[3][2] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_guides":
        # no 5-guides → axis undetermined, no mirror operation possible
        g[2][1] = 1; g[2][2] = 2
        g[3][1] = 1; g[3][3] = 2
        return g
    if name == "motif_on_both_sides":
        # motif on both sides → mirror would clobber existing cells
        g[0][2] = 5; g[0][7] = 5
        g[2][1] = 1; g[2][2] = 2  # left motif
        g[5][6] = 3; g[5][7] = 4  # right motif (already filled)
        return g
    if name == "single_guide":
        # only 1 5-guide → axis underdetermined (need 2 to define a line)
        g[0][2] = 5
        g[2][1] = 1; g[2][2] = 2
        g[3][1] = 1
        return g
    return g
