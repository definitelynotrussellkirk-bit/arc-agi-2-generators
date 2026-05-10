"""Generator for arc_additional_puzzles_21_set8:M52 — Tile a small motif.

Rule: take the cropped non-bg content as a motif, then tile (cycle
through it) to fill the full grid via modulo on (r, c).

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: motif_at_origin_only, motif_fills_grid, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f84f23e456ac"
VERSION = "1.1.0"
TASK_ID = "f84f23e456ac"
SUMMARY = "Small motif in upper-left of an otherwise-bg grid; output tiles the motif."

INVARIANTS = [
    "motif is in the upper-left, dimensions 2..3 x 2..3",
    "motif has at least one non-bg cell on the bottom row AND right col so its bbox is well-defined",
    "rest of input grid is all bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("motif_at_origin_only", "motif_fills_grid", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_h":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_left",
                       "valid": "upper_left"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "motif_w":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        mh = ctx.draw_int("motif_h", 2, 2)
        mw = ctx.draw_int("motif_w", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        mh = ctx.draw_int("motif_h", 3, 3)
        mw = ctx.draw_int("motif_w", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
        mh = ctx.draw_int("motif_h", 2, 3)
        mw = ctx.draw_int("motif_w", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("motif")
    color_rng = ctx.draw_rng("colors")
    motif = [[0]*mw for _ in range(mh)]
    n_cells = rng.randint(2, max(2, mh*mw - 2))
    positions = [(r, c) for r in range(mh) for c in range(mw)]
    rng.shuffle(positions)
    placed = 0
    for r, c in positions:
        if placed >= n_cells: break
        motif[r][c] = color_rng.randint(1, 9)
        placed += 1
    if not any(motif[mh-1][c] != 0 for c in range(mw)):
        motif[mh-1][rng.randint(0, mw-1)] = color_rng.randint(1, 9)
    if not any(motif[r][mw-1] != 0 for r in range(mh)):
        motif[rng.randint(0, mh-1)][mw-1] = color_rng.randint(1, 9)
    for r in range(mh):
        for c in range(mw):
            g[r][c] = motif[r][c]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "motif_at_origin_only":
        # only (0,0) is non-bg → motif is 1x1 single cell, tiling is uniform fill
        g[0][0] = 5
        return g
    if name == "motif_fills_grid":
        # motif already spans whole grid → tiling is identity, no visible repetition
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r + c) % 5)
        return g
    if name == "no_motif":
        # empty grid → motif bbox undefined, rule has no input pattern to tile
        return g
    return g
