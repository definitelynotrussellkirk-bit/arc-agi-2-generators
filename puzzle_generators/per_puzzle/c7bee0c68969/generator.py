"""Generator for arc_puzzle_bank_fifteenth21:M101 — repeat body by 9-marker count.

Rule: top-row 9 markers give the repeat count. The nonzero object below
is cropped and repeated horizontally with one blank spacer column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, repeat_count, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_body, K_equals_one.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c7bee0c68969"
VERSION = "1.1.0"
TASK_ID = "c7bee0c68969"
SUMMARY = "Top-row 9-count repeats the cropped body object horizontally."

INVARIANTS = [
    "row 0 has two to four color-9 markers",
    "all nonzero body cells belong to one compact object",
    "the object crop is not empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_body", "K_equals_one")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "repeat_count":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "row0_9_markers_with_body",
                       "valid": "row0_9_markers_with_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0, 2), (1, 0, 2), (1, 1, 3), (2, 1, 3)],
    [(0, 1, 4), (1, 0, 4), (1, 1, 5), (1, 2, 5)],
    [(0, 0, 6), (0, 1, 6), (1, 1, 7), (2, 1, 7), (2, 2, 8)],
    [(0, 0, 3), (1, 0, 3), (2, 0, 4), (2, 1, 4)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        k = ctx.draw_int("repeat_count", 2, 2)
    elif difficulty == "hard":
        k = ctx.draw_int("repeat_count", 3, 4)
    else:
        k = ctx.draw_int("repeat_count", 2, 4)
    cells = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
    g = full_grid(9, 12, 0)
    for c in sorted(rng.sample(range(1, 11), k)):
        g[0][c] = 9
    top = rng.randint(3, 5)
    left = rng.randint(1, 6)
    for r, c, v in cells:
        g[top + r][left + c] = v
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    cells = _SHAPES[0]
    if name == "no_markers":
        # row 0 empty → K=0, no copies to make
        for r, c, v in cells: g[3 + r][3 + c] = v
        return g
    if name == "no_body":
        # markers but no body → K copies of nothing
        for c in [2, 5, 8]: g[0][c] = 9
        return g
    if name == "K_equals_one":
        # only 1 marker → output is single copy (no observable repetition)
        g[0][3] = 9
        for r, c, v in cells: g[3 + r][3 + c] = v
        return g
    return g
