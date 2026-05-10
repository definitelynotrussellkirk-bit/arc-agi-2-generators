"""Generator for arc_puzzle_bank_21_set17_bundle:easy_p03.

Rule: four equal diagonal neighbors around a zero center fill that center.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, partial_diagonals, mismatched_diagonals.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04400a6b6096"
VERSION = "1.1.0"
TASK_ID = "04400a6b6096"
SUMMARY = "Separated X-corner motifs with agreed diagonal colors."

INVARIANTS = [
    "background is 0",
    "each motif has four same-color diagonal neighbors",
    "motif centers are zero",
    "3x3 neighborhoods are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "partial_diagonals", "mismatched_diagonals")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_count":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_x_corners",
                       "valid": "spaced_x_corners"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _block(r, c):
    return {(rr, cc) for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        motif_count = ctx.draw_int("motif_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        motif_count = ctx.draw_int("motif_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 11)
        motif_count = ctx.draw_int("motif_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=motif_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            r = rng.randint(1, h - 2)
            c = rng.randint(1, w - 2)
            block = _block(r, c)
            if block & occupied:
                continue
            for rr, cc in [(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]:
                g[rr][cc] = color
            occupied |= block
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no diagonal corners, rule has no centers to fill
        return g
    if name == "partial_diagonals":
        # only 3 of 4 diagonal corners present → predicate "all 4 same color" fails
        # cavity at (3,3) — TL, TR, BL but missing BR
        g[2][2] = 4; g[2][4] = 4; g[4][2] = 4
        # cavity at (6,7) — TL, TR, BR but missing BL
        g[5][6] = 6; g[5][8] = 6; g[7][8] = 6
        return g
    if name == "mismatched_diagonals":
        # all 4 diagonals present but in different colors → predicate fails
        g[2][2] = 4; g[2][4] = 6; g[4][2] = 3; g[4][4] = 8
        return g
    return g
