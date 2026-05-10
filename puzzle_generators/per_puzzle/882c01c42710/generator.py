"""Generator for e21d9049.

Rule: center row + center col with colored seq; rule cycles each
across entire row/col.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_h, n_v.
Degenerates: no_rows, no_cols, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "882c01c42710"
VERSION = "1.1.0"
TASK_ID = "882c01c42710"
SUMMARY = "Center row + col with colored seqs; rule cycles each across entire row/col."

INVARIANTS = [
    "background is 0",
    "exactly one row has the most non-bg cells",
    "exactly one col has the most non-bg cells",
    "all non-bg cells lie on center_row OR center_col",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rows", "no_cols", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_h":            {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "n_v":            {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 12, 13
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0})
    g = full_grid(h, w, 0)
    cr = rng.randint(h // 3, 2 * h // 3)
    cc = rng.randint(w // 3, 2 * w // 3)
    n_h = rng.randint(3, 4)
    h_start = rng.randint(2, w - n_h - 2)
    for i in range(n_h):
        g[cr][h_start + i] = palette[i % len(palette)]
    n_v = rng.randint(3, 4)
    v_start = rng.randint(2, h - n_v - 2)
    for i in range(n_v):
        g[v_start + i][cc] = palette[i % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_rows":
        for r in range(2, 8):
            g[r][6] = 2
        return g
    if name == "no_cols":
        for c in range(2, 8):
            g[6][c] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
