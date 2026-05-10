"""Generator for arc_puzzle_bank_21_set6_s:S6_H2 — paint best-turn-count wire path.

Rule: color-2 starts touch color-1 wires. The rule follows each wire
and paints the wire with the highest turn count in color 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, path_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_start, no_wire, straight_wire.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bd7b84c485b8"
VERSION = "1.1.0"
TASK_ID = "bd7b84c485b8"
SUMMARY = "Follow the color-1 wire from a color-2 start and paint the best path."

INVARIANTS = [
    "there is at least one color-2 start cell",
    "each start touches a non-branching color-1 wire",
    "the primary wire has one or more turns",
    "the selected wire path is recolored to 3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_start", "no_wire", "straight_wire")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "path_variant":   {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "single_2_start_with_turning_1_wire",
                       "valid": "single_2_start_with_turning_1_wire"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATHS = [
    [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6)],
    [(1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (4, 5), (5, 5)],
    [(3, 1), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4), (4, 4)],
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
        base_path = _PATHS[0]
    elif difficulty == "hard":
        base_path = _PATHS[ctx.draw_int("path_variant", 1, 2)]
    else:
        base_path = _PATHS[ctx.draw_int("path_variant", 0, len(_PATHS) - 1)]
    row_shift = rng.randint(0, 1)
    col_shift = rng.randint(0, 1)
    path = [(r + row_shift, c + col_shift) for r, c in base_path]
    g = full_grid(10, 11, 0)
    start_r, start_c = path[0]
    g[start_r][start_c - 1] = 2
    for r, c in path:
        g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 11, 0)
    path = _PATHS[0]
    if name == "no_start":
        # wire but no 2-start → no walker initiated, rule doesn't fire
        for r, c in path: g[r][c] = 1
        return g
    if name == "no_wire":
        # 2-start but no 1-wire → walker has nothing to follow
        g[3][1] = 2
        return g
    if name == "straight_wire":
        # straight wire (no turns) → turn-count = 0, no "best" path to highlight
        for c in range(2, 8): g[3][c] = 1
        g[3][1] = 2
        return g
    return g
