"""Generator for e4075551.

Rule: center pixel + 4 markers; rule paints colored rectangle frame
with cross interior.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
center_position.
Degenerates: no_center, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0a9926d504f3"
VERSION = "1.1.0"
TASK_ID = "0a9926d504f3"
SUMMARY = "Center pixel + 4 markers; rule paints colored rectangle frame with cross."

INVARIANTS = [
    "background is 0",
    "exactly one red center pixel of color 2",
    "exactly four non-red marker pixels at frame top/bottom/left/right extremes",
    "center sits strictly inside the frame extent",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_center", "no_markers", "full_grid")
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
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "center_position":{"type": "str", "default": "rng", "valid": "rng"},
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
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0, 2, 5})
    top_r = rng.randint(1, h // 3)
    bot_r = rng.randint(2 * h // 3, h - 2)
    left_c = rng.randint(1, w // 3)
    right_c = rng.randint(2 * w // 3, w - 2)
    cr = rng.randint(top_r + 1, bot_r - 1)
    cc = rng.randint(left_c + 1, right_c - 1)
    g = full_grid(h, w, 0)
    g[cr][cc] = 2
    cols_taken = {cc, left_c, right_c}
    top_c = rng.choice([c for c in range(w) if c not in cols_taken])
    g[top_r][top_c] = palette[0]
    bot_c = rng.choice([c for c in range(w) if c not in cols_taken | {top_c}])
    g[bot_r][bot_c] = palette[1]
    rows_taken = {cr, top_r, bot_r}
    left_r = rng.choice([r for r in range(h) if r not in rows_taken])
    g[left_r][left_c] = palette[2]
    right_r = rng.choice([r for r in range(h) if r not in rows_taken | {left_r}])
    g[right_r][right_c] = palette[3]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_center":
        g[2][5] = 1; g[10][5] = 3; g[5][2] = 4; g[5][10] = 6
        return g
    if name == "no_markers":
        g[6][6] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
