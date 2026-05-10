"""Generator for arc_puzzle_bank_21_set23_s:S23_H5.

Three visible 3x3 tiles in a 2x2 lattice determine the missing tile by
cellwise odd parity. The separators are color 9; the bottom-right tile is
blank in the input.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_zero, no_separators, full_tiles.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8e9c04b8fdfb"
VERSION = "1.1.0"
TASK_ID = "8e9c04b8fdfb"
SUMMARY = "2x2 3x3 tile lattice with the bottom-right tile inferred by odd parity."

INVARIANTS = [
    "the grid is a 2x2 lattice of 3x3 tiles separated by color 9",
    "the top-left, top-right, and bottom-left tiles contain nonzero masks",
    "the bottom-right tile is blank",
    "the output marks cells with odd occupancy among the three visible tiles",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_zero", "no_separators", "full_tiles")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "density":        {"type": "float", "default": "rng choice .35|.45|.55", "valid": "0.2..0.8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "2x2_tile_lattice",
                       "valid": "2x2_tile_lattice"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density_label":  {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _random_tile(rng, color, density):
    return [
        [color if rng.random() < density else 0 for _ in range(3)]
        for _ in range(3)
    ]


def _odd_count(a, b, c, r, col):
    return (
        (1 if a[r][col] else 0)
        + (1 if b[r][col] else 0)
        + (1 if c[r][col] else 0)
    ) % 2


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
        density = ctx.draw_choice("density", [0.30, 0.35])
    elif difficulty == "hard":
        density = ctx.draw_choice("density", [0.45, 0.55, 0.65])
    else:
        density = ctx.draw_choice("density", [0.35, 0.45, 0.55])
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 3)

    a = _random_tile(rng, colors[0], density)
    b = _random_tile(rng, colors[1], density)
    c = _random_tile(rng, colors[2], density)
    if not any(_odd_count(a, b, c, r, col) for r in range(3) for col in range(3)):
        a[0][0] = colors[0]

    g = full_grid(7, 7, 0)
    for i in range(7):
        g[3][i] = 9
        g[i][3] = 9
    for r in range(3):
        for col in range(3):
            g[r][col] = a[r][col]
            g[r][4 + col] = b[r][col]
            g[4 + r][col] = c[r][col]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "all_zero":
        # All visible tiles empty — rule's parity over zero cells
        # yields zero output; effect is invisible.
        for i in range(7):
            g[3][i] = 9
            g[i][3] = 9
        return g
    if name == "no_separators":
        # No color-9 dividers — rule's tile-lattice precondition
        # fails; tile boundaries undefined.
        for r in range(3):
            for c in range(3):
                if (r + c) % 2: g[r][c] = 1
                if (r + c) % 2: g[r][4 + c] = 2
                if (r + c) % 2: g[4 + r][c] = 3
        return g
    if name == "full_tiles":
        # All three tiles fully filled — rule's odd-parity reduces
        # to constant 1 everywhere; output trivial.
        for i in range(7):
            g[3][i] = 9
            g[i][3] = 9
        for r in range(3):
            for col in range(3):
                g[r][col] = 1
                g[r][4 + col] = 2
                g[4 + r][col] = 3
        return g
    return g
