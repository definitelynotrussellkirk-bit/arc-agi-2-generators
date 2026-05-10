"""Generator for arc_additional_puzzle_bank_volume3:E19 — Recolor 1-cell to 4 if it has 3 cardinal 1-neighbors.

Rule: cell (r,c) with value 1 and exactly 3 cardinal neighbors of
value 1 → becomes 4 (a T-shape center).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_Ts,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_T_centers, only_lines, full_plus.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "ae1648cd669b"
VERSION = "1.1.0"
TASK_ID = "ae1648cd669b"
SUMMARY = "2 T-shaped 1-blobs (center + 3 cardinal arms) plus distractors of color 1."

INVARIANTS = [
    "≥2 T-shaped 1-shapes (center has 3 cardinal 1-neighbors)",
    "≥1 distractor 1-blob that is not a T (e.g. straight line)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_T_centers", "only_lines", "full_plus")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_Ts":           {"type": "int", "default": "2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread",
                       "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    Ts = [
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (0, 1)],
    ]
    placements = [
        (rng.randint(0, 2), rng.randint(0, 3), rng.choice(Ts)),
        (rng.randint(3, h - 4), rng.randint(w - 5, w - 4), rng.choice(Ts)),
    ]
    rng.shuffle(placements)
    for top, left, s in placements:
        paint_at(g, top, left, s, 1)
    bar = [(0, 0), (0, 1), (0, 2)]
    paint_at(g, h - 2, rng.randint(0, w - 4), bar, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_T_centers":
        # only color-1 cells with ≤2 cardinal 1-neighbors → no T-center exists, rule fires zero times
        # singletons + a 2-cell pair
        g[2][2] = 1
        g[5][7] = 1
        g[6][2] = 1; g[6][3] = 1
        return g
    if name == "only_lines":
        # straight 4-cell lines → endpoints have 1 neighbor, middles have 2; never 3
        for c in range(1, 5): g[2][c] = 1
        for r in range(3, 7): g[r][8] = 1
        return g
    if name == "full_plus":
        # +-shape (5 cells: center + 4 arms) → center has 4 neighbors (not 3) → predicate fails
        cr, cc = 4, 5
        g[cr][cc] = 1
        g[cr - 1][cc] = 1; g[cr + 1][cc] = 1
        g[cr][cc - 1] = 1; g[cr][cc + 1] = 1
        return g
    return g
