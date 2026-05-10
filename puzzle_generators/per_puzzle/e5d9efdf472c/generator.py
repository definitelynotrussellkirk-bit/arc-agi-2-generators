"""Generator for arc_additional_puzzle_bank_volume15:E103.

Rule: two aligned magenta markers are connected by cyan between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, axis_kind,
palette_size, position_bias, n_distinct_colors, gap_size, texture.
Degenerates: single_marker, three_markers, non_aligned_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e5d9efdf472c"
VERSION = "1.1.0"
TASK_ID = "e5d9efdf472c"
SUMMARY = "Two aligned magenta markers are connected by cyan between them."

INVARIANTS = [
    "background is 0",
    "there are exactly two magenta markers",
    "markers share one row or column",
    "the cells strictly between them start empty",
]

PALETTE_KINDS = ("default", "horiz_axis", "vert_axis", "mixed_axis")
DEGENERATE_TEXTURES = ("single_marker", "three_markers", "non_aligned_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..13", "valid": "3..20"},
    "grid_w":         {"type": "int", "default": "rng 7..13", "valid": "3..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "axis_kind":      {"type": "str", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "aligned", "valid": "aligned"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "gap_size":       {"type": "str", "default": "rng", "valid": "rng"},
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
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 13)
        w = ctx.draw_int("grid_w", 7, 13)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    if rng.choice([False, True]):
        r = rng.randint(0, h - 1)
        c1 = rng.randint(0, w - 4)
        c2 = rng.randint(c1 + 2, w - 1)
        g[r][c1] = 6
        g[r][c2] = 6
    else:
        c = rng.randint(0, w - 1)
        r1 = rng.randint(0, h - 4)
        r2 = rng.randint(r1 + 2, h - 1)
        g[r1][c] = 6
        g[r2][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "single_marker":
        # only one magenta cell → no second endpoint, no segment
        g[3][2] = 6
        return g
    if name == "three_markers":
        # 3 magenta cells → which pair to connect is ambiguous
        g[3][1] = 6; g[3][6] = 6; g[6][3] = 6
        return g
    if name == "non_aligned_markers":
        # 2 markers but they don't share a row OR column → axis undefined
        g[1][1] = 6
        g[5][6] = 6
        return g
    return g
