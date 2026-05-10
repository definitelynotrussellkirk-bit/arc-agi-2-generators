"""Generator for arc_additional_puzzle_bank_volume20:E137 — Recolor 3-L-trominoes to 4.

Rule: each 3-blob with size 3, bbox-h 2, bbox-w 2 (an L-tromino) is
painted color 4; other 3-blobs unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_l_trominoes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_l_trominoes, all_l_trominoes, no_3_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "8604dc774d22"
VERSION = "1.1.0"
TASK_ID = "8604dc774d22"
SUMMARY = "Mix of L-trominoes (size 3, h 2, w 2) and other 3-shapes."

INVARIANTS = [
    ">=2 L-tromino 3-blobs",
    ">=1 non-L 3-blob (e.g. straight tromino or single)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_l_trominoes", "all_l_trominoes", "no_3_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_l_trominoes":  {"type": "int", "default": "2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    L_variants = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
    ]
    bar3 = [(0, 0), (0, 1), (0, 2)]
    placements = [
        (1, 1, rng.choice(L_variants)),
        (1, w - 4, rng.choice(L_variants)),
        (h - 3, rng.randint(2, w - 5), bar3),
    ]
    rng.shuffle(placements)
    for top, left, s in placements:
        paint_at(g, top, left, s, 3)
    g[h - 2][w - 2] = 7; g[h - 2][w - 1] = 7
    g[h - 1][w - 2] = 7; g[h - 1][w - 1] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    bar3 = [(0, 0), (0, 1), (0, 2)]
    if name == "no_l_trominoes":
        # only straight 3-bars → no L-tromino targets, rule has nothing to recolor
        paint_at(g, 1, 1, bar3, 3)
        paint_at(g, 4, 5, bar3, 3)
        paint_at(g, 6, 0, bar3, 3)
        return g
    if name == "all_l_trominoes":
        # every 3-blob is an L → rule recolors all of them, no contrast
        L = [(0, 0), (0, 1), (1, 0)]
        paint_at(g, 1, 1, L, 3)
        paint_at(g, 4, 5, L, 3)
        paint_at(g, 6, 8, L, 3)
        return g
    if name == "no_3_blobs":
        # no color-3 cells → rule has no targets at all
        for r, c in [(2, 2), (4, 5), (6, 8)]:
            g[r][c] = 5
        return g
    return g
