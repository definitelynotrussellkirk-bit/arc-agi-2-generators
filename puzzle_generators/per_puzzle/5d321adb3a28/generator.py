"""Generator for arc_puzzle_bank_21_set18_bundle:easy_p07.

Zero cells between matching opposite neighbors are filled horizontally or
vertically.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, motif_already_solid, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d321adb3a28"
VERSION = "1.1.0"
TASK_ID = "5d321adb3a28"
SUMMARY = "Separated opposite-neighbor fill motifs."

INVARIANTS = [
    "background is 0",
    "each motif is color-zero-same-color horizontally or vertically",
    "motifs are separated to avoid conflicting fills",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "motif_already_solid", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_count":    {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_orthogonal_motifs",
                       "valid": "spaced_orthogonal_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        motif_count = ctx.draw_int("motif_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        motif_count = ctx.draw_int("motif_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        motif_count = ctx.draw_int("motif_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=motif_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(300):
            horizontal = rng.choice([True, False])
            if horizontal:
                r = rng.randrange(h)
                c = rng.randint(0, w - 3)
                band = [(r, cc) for cc in range(max(0, c - 1), min(w, c + 4))]
                endpoints = [(r, c), (r, c + 2)]
            else:
                r = rng.randint(0, h - 3)
                c = rng.randrange(w)
                band = [(rr, c) for rr in range(max(0, r - 1), min(h, r + 4))]
                endpoints = [(r, c), (r + 2, c)]
            if all(g[rr][cc] == 0 for rr, cc in band):
                for rr, cc in endpoints:
                    g[rr][cc] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no endpoints, rule has no effect
        return g
    if name == "motif_already_solid":
        # gap is already filled → fill is a no-op
        g[2][2] = 4; g[2][3] = 4; g[2][4] = 4
        g[5][6] = 6; g[5][7] = 6; g[5][8] = 6
        return g
    if name == "mismatched_endpoints":
        # endpoints have different colors → which color does the gap take?
        g[2][2] = 4; g[2][4] = 6
        g[5][6] = 3; g[5][8] = 8
        return g
    return g
