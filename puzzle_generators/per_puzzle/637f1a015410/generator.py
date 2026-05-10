"""Generator for arc_puzzle_bank_21_set4:S4_E7 — diagonal red dominoes recolor cyan.

Rule: red diagonal domino components are recolored cyan; axis-aligned
dominoes stay red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, diagonal_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_diagonals, all_diagonals, no_dominoes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "637f1a015410"
VERSION = "1.1.0"
TASK_ID = "637f1a015410"

SUMMARY = "Red diagonal domino components are recolored cyan; axis-aligned dominoes stay red."

INVARIANTS = [
    "background is 0",
    "all input objects are red dominoes",
    "some dominoes are diagonal under 8-connectivity",
    "horizontal and vertical dominoes remain red",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_diagonals", "all_diagonals", "no_dominoes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "diagonal_count": {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "diag_with_axis_distractors",
                       "valid": "diag_with_axis_distractors"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_DIAGONALS = [
    [(0, 0), (1, 1)],
    [(0, 1), (1, 0)],
]

_AXIS = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        diagonal_count = ctx.draw_int("diagonal_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        diagonal_count = ctx.draw_int("diagonal_count", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        diagonal_count = ctx.draw_int("diagonal_count", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [rng.choice(_DIAGONALS) for _ in range(diagonal_count)]
    shapes.extend(rng.choice(_AXIS) for _ in range(rng.randint(1, 2)))
    rng.shuffle(shapes)
    for cells in shapes:
        if place_no_overlap(rng, g, cells, 2, padding=1, max_tries=400) is None:
            raise ValueError("could not place red domino")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_diagonals":
        # only axis-aligned dominoes → rule has nothing to recolor
        g[1][1] = 2; g[1][2] = 2   # horizontal
        g[5][5] = 2; g[6][5] = 2   # vertical
        return g
    if name == "all_diagonals":
        # only diagonals → all recolored, no axis-aligned distractor for contrast
        g[1][1] = 2; g[2][2] = 2
        g[5][6] = 2; g[6][7] = 2
        return g
    if name == "no_dominoes":
        # blank → no objects at all
        return g
    return g
