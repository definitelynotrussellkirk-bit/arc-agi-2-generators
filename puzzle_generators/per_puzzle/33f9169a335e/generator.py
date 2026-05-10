"""Generator for 54d82841.

Rule: find each col c with row r having (c-1, c, c+1) non-zero and
row r+1 having (c-1, c+1) non-zero with c=0 (gap). Place 4 at (h-1, c).

Combinatorial axes (8): grid_h/w, n_us, palette_size, palette_kind,
position_bias, U_height, anchor_corner, asymmetry_force.
Degenerates: no_us, all_us, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "33f9169a335e"
VERSION = "1.1.0"
TASK_ID = "33f9169a335e"
SUMMARY = "Grid with inverted-U shapes; rule marks col of gap on bottom row with 4."

INVARIANTS = [
    "background is 0",
    ">=1 inverted-U shape (3-wide × 2-tall, gap in middle of bottom row)",
    "each U has gap row < h-1 (so bottom mark fits)",
    "U shapes don't share columns",
    "no color 4 in input (rule writes 4 for output)",
]

POSITION_BIAS = ("center", "spread", "edge")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_us", "all_us", "single_row")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 5..10", "valid": "5..14"},
    "grid_w":            {"type": "int", "default": "rng 5..14", "valid": "5..18"},
    "n_us":              {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":      {"type": "int", "default": "= n_us",
                          "valid": "1..7"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIAS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for position_bias",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 7, 5, 8
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 12, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 10, 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_us = int(overrides.get("n_us",
                             ctx.draw_int("n_us", 1, max(1, w // 4))))
    n_us = max(1, min(5, n_us))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size", n_us))
    palette = pool[:max(1, n_palette)]
    while len(palette) < n_us:
        palette.append(palette[0])
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    g = full_grid(h, w, 0)
    used_cols = set()
    placed = 0
    for i in range(n_us * 4):
        if placed >= n_us:
            break
        for _try in range(20):
            c0 = _pick_c0(bias, w, rng)
            r0 = _pick_r0(bias, h, rng)
            cols = {c0, c0 + 1, c0 + 2}
            if cols & used_cols:
                continue
            if c0 + 2 >= w or r0 + 1 >= h - 1:
                continue
            color = palette[placed % len(palette)]
            g[r0][c0] = color
            g[r0][c0 + 1] = color
            g[r0][c0 + 2] = color
            g[r0 + 1][c0] = color
            g[r0 + 1][c0 + 2] = color
            used_cols |= cols
            placed += 1
            break
    if placed < 1:
        # Force one
        if h >= 4 and w >= 4:
            color = palette[0]
            g[0][0] = color; g[0][1] = color; g[0][2] = color
            g[1][0] = color; g[1][2] = color
    return g


def _pick_c0(bias, w, rng):
    if bias == "center":
        return max(0, (w - 3) // 2)
    if bias == "edge":
        return rng.choice([0, w - 3])
    return rng.randint(0, w - 3)


def _pick_r0(bias, h, rng):
    if bias == "center":
        return max(0, (h - 4) // 2)
    if bias == "edge":
        return 0
    return rng.randint(0, h - 4)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
    if name == "no_us":
        return g
    if name == "all_us":
        for c0 in range(0, w - 2, 4):
            r0 = 0
            if r0 + 1 < h - 1 and c0 + 2 < w:
                g[r0][c0] = color
                g[r0][c0 + 1] = color
                g[r0][c0 + 2] = color
                g[r0 + 1][c0] = color
                g[r0 + 1][c0 + 2] = color
        return g
    if name == "single_row":
        for c in range(min(3, w)):
            g[0][c] = color
        return g
    return g
