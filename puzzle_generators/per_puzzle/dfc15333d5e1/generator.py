"""Generator for arc_puzzle_bank_sixteenth_21_bundle:easy_110_keep_centers_of_three_cell_lines.

Rule: each separated 3-cell horizontal/vertical line collapses to its
center cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, lines, texture.
Degenerates: no_lines, single_cells, four_plus_cell_line.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dfc15333d5e1"
VERSION = "1.1.0"
TASK_ID = "dfc15333d5e1"

SUMMARY = "Separated three-cell straight lines collapse to their center cells."

INVARIANTS = [
    "background is 0",
    "each component is a straight line of exactly three cells",
    "lines may be horizontal or vertical",
    "components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_lines", "single_cells", "four_plus_cell_line")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "lines":          {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "= lines", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_3_cell_lines",
                       "valid": "scattered_3_cell_lines"},
    "n_distinct_colors": {"type": "int", "default": "= lines", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("lines", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 16)
        w = ctx.draw_int("grid_w", 13, 18)
        target = ctx.draw_int("lines", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        target = ctx.draw_int("lines", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(500):
        if placed >= target:
            break
        vertical = rng.randrange(2) == 0
        if vertical:
            r0 = rng.randint(0, h - 3)
            c0 = rng.randrange(w)
            cells = [(r0 + i, c0) for i in range(3)]
        else:
            r0 = rng.randrange(h)
            c0 = rng.randint(0, w - 3)
            cells = [(r0, c0 + i) for i in range(3)]
        guard = {
            (rr, cc)
            for r, c in cells
            for rr in range(max(0, r - 1), min(h, r + 2))
            for cc in range(max(0, c - 1), min(w, c + 2))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r, c in cells:
            g[r][c] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_lines":
        # Empty grid — rule has no 3-cell lines to collapse.
        return g
    if name == "single_cells":
        # Components of size 1, not 3-cell lines — rule's
        # "exactly three cells" filter excludes them.
        g[2][2] = 4; g[5][7] = 6; g[7][3] = 7
        return g
    if name == "four_plus_cell_line":
        # 4-cell straight lines instead of 3-cell — rule's
        # length-3 filter excludes them; nothing collapses.
        for c in range(2, 6): g[3][c] = 4
        for r in range(5, 9): g[r][8] = 6
        return g
    return g
