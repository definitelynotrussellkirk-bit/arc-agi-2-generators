"""Generator for arc_additional_puzzles_21_set8:H54 — Tile motif and rotate-cw alternately.

Rule: motif = crop-to-content of input. Tile the grid with checkerboard
pattern of motif and motif rotated-cw.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_n,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: rotation_invariant_motif, motif_too_large, blank_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "bdde17915298"
VERSION = "1.1.0"
TASK_ID = "bdde17915298"
SUMMARY = "Small square motif in upper-left; output tiles motif and its rotation in checkerboard."

INVARIANTS = [
    "motif is square (n x n) and placed in the upper-left",
    "motif has at least one non-bg cell on the bottom row AND right col",
    "output tile dimension n divides the grid edges (else result truncates)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("rotation_invariant_motif", "motif_too_large", "blank_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_n":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_left_motif",
                       "valid": "upper_left_motif"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("motif_n", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("motif_n", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 6, 9)
        n = ctx.draw_int("motif_n", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("motif")
    color_rng = ctx.draw_rng("colors")
    motif = [[0]*n for _ in range(n)]
    n_cells = rng.randint(max(2, n), n*n - 1)
    positions = [(r, c) for r in range(n) for c in range(n)]
    rng.shuffle(positions)
    for r, c in positions[:n_cells]:
        motif[r][c] = color_rng.randint(1, 9)
    if not any(motif[n-1][c] != 0 for c in range(n)):
        motif[n-1][rng.randint(0, n-1)] = color_rng.randint(1, 9)
    if not any(motif[r][n-1] != 0 for r in range(n)):
        motif[rng.randint(0, n-1)][n-1] = color_rng.randint(1, 9)
    paste(g, motif, 0, 0)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "rotation_invariant_motif":
        # 2x2 solid square is invariant under cw rotation → tile and rotated tile are identical
        g[0][0] = 4; g[0][1] = 4
        g[1][0] = 4; g[1][1] = 4
        return g
    if name == "motif_too_large":
        # motif larger than grid → tiling can't repeat, output truncated
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r * w + c) % 8) + 1
        return g
    if name == "blank_motif":
        # blank motif → tiling produces all-zero grid, rule effect invisible
        return g
    return g
