"""Generator for arc_puzzle_bank_21_set9_e:easy_i05.

Rule: each blank cell with four same-color diagonal neighbors is filled with
that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, partial_diagonals, mismatched_diagonals.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "251f7ac6780f"
VERSION = "1.1.0"
TASK_ID = "251f7ac6780f"

SUMMARY = "Fill the center of each same-color diagonal X."

INVARIANTS = [
    "background is 0",
    "each active center has four same-color diagonal neighbors",
    "active centers are initially zero",
    "diagonal X motifs are isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "partial_diagonals", "mismatched_diagonals")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motifs":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_x_corners",
                       "valid": "spaced_x_corners"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r, c):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - 2), min(h, r + 3)):
        for cc in range(max(0, c - 2), min(w, c + 3)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("motifs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("motifs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("motifs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(180):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if not _clear(g, r, c):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            g[r + dr][c + dc] = color
        placed += 1
    if placed == 0:
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            g[3 + dr][3 + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no diagonal corners, rule has no centers to fill
        return g
    if name == "partial_diagonals":
        # only 3 of 4 diagonal corners → predicate "all 4 same color" fails
        g[2][2] = 4; g[2][4] = 4; g[4][2] = 4  # missing BR
        g[5][6] = 6; g[5][8] = 6; g[7][8] = 6  # missing BL
        return g
    if name == "mismatched_diagonals":
        # all 4 diagonals present but in different colors → predicate fails
        g[2][2] = 4; g[2][4] = 6; g[4][2] = 3; g[4][4] = 8
        return g
    return g
