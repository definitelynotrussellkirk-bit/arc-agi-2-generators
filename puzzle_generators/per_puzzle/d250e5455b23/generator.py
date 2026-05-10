"""Generator for arc_puzzle_bank_21_set17_bundle:easy_p04.

Isolated two-cell dominos grow into the full 2x2 square covering the domino.

Combinatorial axes (8): grid_h, grid_w, palette_kind, domino_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominos, single_cells, already_2x2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d250e5455b23"
VERSION = "1.1.0"
TASK_ID = "d250e5455b23"
SUMMARY = "Separated horizontal and vertical dominos with room to grow to 2x2."

INVARIANTS = [
    "background is 0",
    "all nonzero components are same-color dominos",
    "each domino's bounding 2x2 square is in bounds",
    "domino growth zones are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominos", "single_cells", "already_2x2")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "domino_count":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "isolated_dominos_with_room",
                       "valid": "isolated_dominos_with_room"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _zone(r, c):
    return {(rr, cc) for rr in range(r - 1, r + 3) for cc in range(c - 1, c + 3)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        domino_count = ctx.draw_int("domino_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        domino_count = ctx.draw_int("domino_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 11)
        domino_count = ctx.draw_int("domino_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=domino_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            horizontal = rng.choice([True, False])
            r = rng.randint(0, h - 2)
            c = rng.randint(0, w - 2)
            zone = _zone(r, c)
            if zone & occupied:
                continue
            if horizontal:
                g[r][c] = color
                g[r][c + 1] = color
            else:
                g[r][c] = color
                g[r + 1][c] = color
            occupied |= zone
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_dominos":
        # blank → no dominos to grow
        return g
    if name == "single_cells":
        # 1-cell components, not dominos → can't define a 2x2 to grow into
        g[2][2] = 4
        g[5][6] = 6
        return g
    if name == "already_2x2":
        # already 2x2 squares → grow rule is identity
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 4
                g[5 + dr][5 + dc] = 6
        return g
    return g
