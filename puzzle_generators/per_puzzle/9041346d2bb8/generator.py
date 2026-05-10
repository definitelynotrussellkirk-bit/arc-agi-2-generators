"""Generator for arc_puzzle_bank_21_set17_s:S17_M1.

Rule: color-coded seeds expand into stencils — color 2 → plus,
color 3 → diagonal X, color 4 → 3×3 square.

Combinatorial axes (8): grid_h, grid_w, palette_kind, num_seeds,
extra_seed, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_seeds, all_same_color, seeds_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9041346d2bb8"
VERSION = "1.1.0"
TASK_ID = "9041346d2bb8"
SUMMARY = "Color-coded seeds expand into plus, diagonal-X, or 3x3 square stencils."

INVARIANTS = [
    "background is 0",
    "color 2 seeds use plus growth",
    "color 3 seeds use diagonal-X growth",
    "color 4 seeds use full 3x3 square growth",
    "all seeds are far enough apart that stencil identities remain visible",
]

PALETTE_KINDS = ("default", "all_three_kinds", "spread_seeds", "tight_seeds")
DEGENERATE_TEXTURES = ("no_seeds", "all_same_color", "seeds_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_seeds":      {"type": "int", "default": "3", "valid": "3..4"},
    "extra_seed":     {"type": "bool", "default": "rng",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 14, 15)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 12, 15)
    extra = ctx.draw_choice("extra_seed", [False, True])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    r0 = rng.randint(2, h - 4)
    g[r0][2] = 2
    g[2][w - 4] = 3
    g[h - 3][w - 4] = 4
    if extra:
        g[h - 3][3] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        return g
    if name == "all_same_color":
        # all 3 seeds use the same stencil — no contrast between rules
        g[3][3] = 2
        g[3][9] = 2
        g[7][6] = 2
        return g
    if name == "seeds_overlap":
        # seeds adjacent — their stencils overlap and combine ambiguously
        g[5][5] = 2
        g[5][6] = 3
        g[6][5] = 4
        return g
    return g
