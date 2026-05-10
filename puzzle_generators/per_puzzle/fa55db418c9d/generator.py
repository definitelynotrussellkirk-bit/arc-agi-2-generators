"""Generator for arc_additional_puzzle_bank_volume21:M141 — Recolor 1-trominoes by orientation.

Rule: for each 1-blob with size 3 in 2x2 bbox (L-tromino), recolor based
on which corner is missing: 4 orientations → {2, 3, 4, 8}.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_Ls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_Ls, all_solid_squares, mixed_color_trominoes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "fa55db418c9d"
VERSION = "1.1.0"
TASK_ID = "fa55db418c9d"
SUMMARY = "Several L-trominoes of various orientations + decoration."

INVARIANTS = [
    "between 3 and 4 non-touching L-trominoes (1-blobs in 2×2 bbox)",
    "orientations vary",
    "decoration is a non-1 cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_Ls", "all_solid_squares", "mixed_color_trominoes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_Ls":           {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_L_trominoes",
                       "valid": "spaced_L_trominoes"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


L_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]



def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    placements = [(1, 1), (1, w - 4), (h - 4, 1), (h - 4, w - 4)]
    rng.shuffle(placements)
    n = rng.randint(3, 4)
    for top, left in placements[:n]:
        shape = rng.choice(L_SHAPES)
        for dr, dc in shape:
            g[top + dr][left + dc] = 1
            used.add((top + dr, left + dc))
    g[h - 1][0] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_Ls":
        # only single 1-cells, no L-trominoes → rule has nothing to recolor
        g[2][2] = 1
        g[5][6] = 1
        g[7][9] = 1
        g[h - 1][0] = 7
        return g
    if name == "all_solid_squares":
        # 2x2 solid 1-squares (4 cells, not 3) → "L-tromino" precondition fails
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 1
        for r in range(2):
            for c in range(2): g[5 + r][5 + c] = 1
        g[h - 1][0] = 7
        return g
    if name == "mixed_color_trominoes":
        # trominoes use mixed colors instead of pure 1 → "1-blob" fails
        g[1][1] = 1; g[1][2] = 4; g[2][1] = 1   # mixed
        g[5][5] = 1; g[5][6] = 1; g[6][5] = 6   # mixed
        g[h - 1][0] = 7
        return g
    return g
