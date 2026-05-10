"""Generator for arc_puzzle_bank_fourteenth21:E95.

Rule: blank cells with four same-color diagonal neighbors are filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, partial_diagonals, mismatched_diagonals.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9f74cf8633e5"
VERSION = "1.1.0"
TASK_ID = "9f74cf8633e5"

SUMMARY = "Place four same-color diagonal neighbors around blank centers."

INVARIANTS = [
    "background is 0",
    "each active motif has a zero center",
    "the four diagonal neighbors around the center share one color",
    "motif footprints are disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "partial_diagonals", "mismatched_diagonals")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motifs":         {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_diagonal_x",
                       "valid": "spaced_diagonal_x"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_DIAGS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("motifs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("motifs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
        target = ctx.draw_int("motifs", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(250):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        footprint = {(r + dr, c + dc) for dr, dc in _DIAGS} | {(r, c)}
        if footprint & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for dr, dc in _DIAGS:
            g[r + dr][c + dc] = color
        reserved.update(footprint)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no diagonal corners, rule has no centers to fill
        return g
    if name == "partial_diagonals":
        # 3 of 4 diagonals → predicate fails
        g[2][2] = 4; g[2][4] = 4; g[4][2] = 4
        g[5][6] = 6; g[5][8] = 6; g[7][8] = 6
        return g
    if name == "mismatched_diagonals":
        # 4 diagonals in different colors → predicate fails
        g[2][2] = 4; g[2][4] = 6; g[4][2] = 3; g[4][4] = 8
        return g
    return g
