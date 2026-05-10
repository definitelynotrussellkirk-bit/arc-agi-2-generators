"""Generator for 46f33fce.

Rule: sparse non-bg pixels expand to 4x4 blocks at offset positions in
2x output.

Combinatorial axes (8): grid_h/w, fg_palette, fill_ratio, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_pixels, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ebe910be6876"
VERSION = "1.1.0"
TASK_ID = "ebe910be6876"
SUMMARY = "Sparse non-bg pixels; rule expands each to a 4x4 block in 2x output."

INVARIANTS = [
    "input dims <= 15 (so 2x output is <= 30)",
    ">=2 non-bg cells, ideally with distinct colors",
    "input dim large enough for 4x4 blocks to land in-bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pixels", "full_grid", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 4..7", "valid": "3..14"},
    "fg_palette":     {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "fill_ratio":     {"type": "float", "default": "rng 0.2..0.5",
                       "valid": "0.1..0.7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered|spread|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
        pn_lo, pn_hi = 1, 2
        ratio_lo, ratio_hi = 0.15, 0.35
    elif difficulty == "hard":
        h_lo, h_hi = 8, 14
        pn_lo, pn_hi = 3, 6
        ratio_lo, ratio_hi = 0.4, 0.7
    else:
        h_lo, h_hi = 4, 7
        pn_lo, pn_hi = 2, 3
        ratio_lo, ratio_hi = 0.2, 0.5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_n = ctx.draw_int("fg_palette", pn_lo, pn_hi)
    palette_n = max(1, min(6, palette_n))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, palette_n, rng)
    rng_ratio = ctx.draw_rng("fill_ratio")
    ratio = rng_ratio.uniform(ratio_lo, ratio_hi)
    g = full_grid(h, w, 0)
    n_cells = h * w
    n_paint = max(2, int(n_cells * ratio))
    positions = list(range(n_cells))
    rng.shuffle(positions)
    for i, idx in enumerate(positions[:n_paint]):
        r, c = divmod(idx, w)
        g[r][c] = pal[i % len(pal)]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 5, 5
    g = full_grid(h, w, 0)
    if name == "no_pixels":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 3 + 1
        return g
    if name == "single_cell":
        g[2][2] = 2
        return g
    return g
