"""Generator for 4612dd53.

Rule: scattered blue(1) cells; rule fills bbox of all blues with red(2)
on every empty cell whose row OR col has >=4 blue cells.

Combinatorial axes (8): grid_h/w, bbox_h, bbox_w, fat_row_count, n_extra,
position_bias, palette_kind, anchor_corner.
Degenerates: no_blues, single_blue, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c48ea6caa2e"
VERSION = "1.1.0"
TASK_ID = "2c48ea6caa2e"
SUMMARY = "Blue cells; rule fills bbox with red where row/col has >=4 blues."

INVARIANTS = [
    "background is 0",
    ">=2 blue (1) cells",
    "at least one row or column has >=4 blues",
    "bbox of blues is >= 5x5",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
DEGENERATE_TEXTURES = ("no_blues", "single_blue", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "bbox_h":         {"type": "int", "default": "rng 6..max", "valid": "5..h-2"},
    "bbox_w":         {"type": "int", "default": "rng 6..max", "valid": "5..w-2"},
    "fat_row_count":  {"type": "int", "default": "rng 4..bw", "valid": "4..bw"},
    "n_extra":        {"type": "int", "default": "rng 2..4", "valid": "0..6"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 10, 12
        ne_lo, ne_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        ne_lo, ne_hi = 3, 6
    else:
        h_lo, h_hi = 12, 16
        ne_lo, ne_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    bh = int(overrides.get("bbox_h", rng.randint(6, max(6, h - 2))))
    bw = int(overrides.get("bbox_w", rng.randint(6, max(6, w - 2))))
    bh = max(5, min(bh, h - 2))
    bw = max(5, min(bw, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    br, bc = _pick_pos(bias, h, w, bh, bw, rng)
    fat_row = rng.randint(br, br + bh - 1)
    n_in_row = int(overrides.get("fat_row_count",
                                 rng.randint(4, bw)))
    n_in_row = max(4, min(bw, n_in_row))
    cols_in_fat = rng.sample(range(bc, bc + bw), n_in_row)
    for c in cols_in_fat:
        g[fat_row][c] = 1
    g[br][bc] = 1
    g[br + bh - 1][bc + bw - 1] = 1
    n_extra = int(overrides.get("n_extra",
                                ctx.draw_int("n_extra", ne_lo, ne_hi)))
    n_extra = max(0, min(8, n_extra))
    for _ in range(n_extra):
        r = rng.randint(br, br + bh - 1)
        c = rng.randint(bc, bc + bw - 1)
        g[r][c] = 1
    return g


def _pick_pos(bias, h, w, bh, bw, rng):
    max_r = max(1, h - bh - 1)
    max_c = max(1, w - bw - 1)
    if bias == "centered":
        br = max(1, (h - bh) // 2)
        bc = max(1, (w - bw) // 2)
    elif bias == "corner":
        br = rng.choice([1, max_r])
        bc = rng.choice([1, max_c])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            br = rng.choice([1, max_r])
            bc = rng.randint(1, max_c)
        else:
            br = rng.randint(1, max_r)
            bc = rng.choice([1, max_c])
    else:
        br = rng.randint(1, max_r)
        bc = rng.randint(1, max_c)
    return br, bc


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_blues":
        return g
    if name == "single_blue":
        g[5][5] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
