"""Generator for arc_puzzle_bank_21_set6_s:S6_H4 — stamp template at wire turns.

Rule: a color-4 template is stamped at every turn along the color-1
wire followed from a color-7 start.

Combinatorial axes (8): grid_h, grid_w, palette_kind, path_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_wire, straight_wire_no_turns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9a7579840f41"
VERSION = "1.1.0"
TASK_ID = "9a7579840f41"
SUMMARY = "Stamp the normalized color-4 template at each turn of a color-1 wire."

INVARIANTS = [
    "there is one connected color-4 template object",
    "one color-7 start touches a non-branching color-1 wire",
    "the wire has at least one turn",
    "template stamps at turn cells remain in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_wire", "straight_wire_no_turns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "path_variant":   {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "template_with_wire",
                       "valid": "template_with_wire"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATE = [(0, 0), (0, 1), (1, 0)]
_PATHS = [
    [(3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 6)],
    [(2, 4), (3, 4), (4, 4), (4, 5), (4, 6), (5, 6)],
    [(4, 2), (4, 3), (5, 3), (6, 3), (6, 4), (6, 5)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        base_path = _PATHS[ctx.draw_int("path_variant", 0, 0)]
    elif difficulty == "hard":
        base_path = _PATHS[ctx.draw_int("path_variant", 1, 2)]
    else:
        base_path = _PATHS[ctx.draw_int("path_variant", 0, len(_PATHS) - 1)]
    row_shift = rng.randint(0, 1)
    col_shift = rng.randint(0, 1)
    path = [(r + row_shift, c + col_shift) for r, c in base_path]
    g = full_grid(10, 12, 0)
    for dr, dc in _TEMPLATE:
        g[0 + dr][0 + dc] = 4
    start_r, start_c = path[0]
    g[start_r][start_c - 1] = 7
    for r, c in path:
        g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_template":
        # wire + start but no color-4 template → nothing to stamp
        g[3][2] = 7
        for c in range(3, 7): g[3][c] = 1
        for r in range(4, 6): g[r][6] = 1
        return g
    if name == "no_wire":
        # template + start but no color-1 wire → no turns to find
        for dr, dc in _TEMPLATE: g[dr][dc] = 4
        g[5][5] = 7
        return g
    if name == "straight_wire_no_turns":
        # wire is a straight line with NO turns → rule has no stamps to place
        for dr, dc in _TEMPLATE: g[dr][dc] = 4
        g[5][2] = 7
        for c in range(3, 9): g[5][c] = 1
        return g
    return g
