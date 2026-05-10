"""Generator for arc_additional_puzzles_21_set12_bundle:M79 — Pick k-th object, transform by cmd.

Rule: k = at(0,0); cmd = at(0, w-1). Sort body objects by (size desc,
color asc); take k-th; crop bbox; apply cmd: 1=cw, 2=180, 3=flip-lr, else=flip-ud.

Combinatorial axes (8): grid_h, grid_w, palette_kind, k,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_k, no_cmd, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import L_TROMINO_SE, SQUARE_2X2

GENERATOR_ID = "e0680a673043"
VERSION = "1.1.0"
TASK_ID = "e0680a673043"
SUMMARY = "k at (0,0) + cmd at (0,w-1) + 3 distinct-size, distinct-color blobs."

INVARIANTS = [
    "(0,0) is k ∈ 1..3",
    "(0,w-1) is cmd ∈ 1..4",
    "exactly 3 non-touching blobs of distinct sizes and colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_k", "no_cmd", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "k":              {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "cmd":            {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "k_plus_cmd_plus_blobs",
                       "valid": "k_plus_cmd_plus_blobs"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        k = ctx.draw_int("k", 1, 1)
        cmd = ctx.draw_int("cmd", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
        k = ctx.draw_int("k", 2, 3)
        cmd = ctx.draw_int("cmd", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
        k = ctx.draw_int("k", 1, 3)
        cmd = ctx.draw_int("cmd", 1, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = k
    g[0][w - 1] = cmd
    palette = list(range(2, 10)); rng.shuffle(palette)
    paint_at(g, 3, 1, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], palette[0])
    paint_at(g, 3, w // 2, SQUARE_2X2, palette[1])
    paint_at(g, h - 3, 2, L_TROMINO_SE, palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_k":
        # cmd + blobs but no k at (0,0) → no rank to pick by
        g[0][w - 1] = 2
        paint_at(g, 3, 1, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 4)
        paint_at(g, 3, w // 2, SQUARE_2X2, 6)
        paint_at(g, h - 3, 2, L_TROMINO_SE, 7)
        return g
    if name == "no_cmd":
        # k + blobs but no cmd at (0, w-1) → no transform specified
        g[0][0] = 2
        paint_at(g, 3, 1, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 4)
        paint_at(g, 3, w // 2, SQUARE_2X2, 6)
        paint_at(g, h - 3, 2, L_TROMINO_SE, 7)
        return g
    if name == "tied_sizes":
        # 2 blobs share size → "distinct sizes" precondition fails
        g[0][0] = 2; g[0][w - 1] = 2
        paint_at(g, 3, 1, SQUARE_2X2, 4)
        paint_at(g, 3, w // 2, SQUARE_2X2, 6)  # also size 4
        paint_at(g, h - 3, 2, L_TROMINO_SE, 7)
        return g
    return g
