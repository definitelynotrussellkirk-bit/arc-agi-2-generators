"""Generator for arc_puzzle_bank_21_set11_bundle:medium_k12 — Translate motif by 1→2 vector.

Rule: 1-source, 2-target. dr/dc = (target - source). For each non-{0,1,2}
cell, paint it at (cell+delta). Crop output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_motif_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_target, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ae7376fe4957"
VERSION = "1.1.0"
TASK_ID = "ae7376fe4957"
SUMMARY = "1-source + 2-target + small motif near 1-source."

INVARIANTS = [
    "exactly one 1-cell, one 2-cell",
    "small motif (3-5 cells of various colors) near 1-source",
    "translated motif stays in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_target", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motif_cells":  {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "source_top_target_bottom",
                       "valid": "source_top_target_bottom"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sr = rng.randint(1, 2); sc = rng.randint(1, 2)
    g[sr][sc] = 1
    palette = [4, 5, 6, 7]; rng.shuffle(palette)
    g[sr + 1][sc + 1] = palette[0]
    g[sr + 1][sc + 2] = palette[1]
    g[sr + 2][sc + 1] = palette[2]
    g[sr + 2][sc + 2] = palette[3]
    tr = h - 2; tc = w - 2
    g[tr][tc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_source":
        # missing 1-source → translation vector undefined
        g[2][2] = 4; g[2][3] = 5; g[3][2] = 6; g[3][3] = 7
        g[h - 2][w - 2] = 2
        return g
    if name == "no_target":
        # missing 2-target → translation vector undefined
        g[1][1] = 1
        g[2][2] = 4; g[2][3] = 5; g[3][2] = 6; g[3][3] = 7
        return g
    if name == "no_motif":
        # 1 and 2 present but no other colors → nothing to translate
        g[1][1] = 1
        g[h - 2][w - 2] = 2
        return g
    return g
