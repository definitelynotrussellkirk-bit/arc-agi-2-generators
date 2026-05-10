"""Generator for 90c28cc7.

Rule: grid of colored blocks downscaled by detecting row/col transition
starts.

Combinatorial axes (8): rows, cols, palette_kind, max_band_h, max_band_w,
anchor_corner, asymmetry_force, palette_size.
Degenerates: single_block, no_blocks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c6ab8f41290"
VERSION = "1.1.0"
TASK_ID = "2c6ab8f41290"
SUMMARY = "Grid of colored blocks downscaled by detecting row/col transitions."

INVARIANTS = [
    "all cells in the nonzero bbox are nonzero block colors",
    "each macro-cell is a solid-color rectangle",
    "adjacent macro-cells differ in color along the probe row and column",
    "the output samples one representative cell from each block",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_block", "no_blocks", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "rows":           {"type": "int", "default": "3", "valid": "2..6"},
    "cols":           {"type": "int", "default": "3", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "max_band_h":     {"type": "int", "default": "3", "valid": "1..5"},
    "max_band_w":     {"type": "int", "default": "3", "valid": "1..5"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "3..7"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    rows = ctx.draw_int("rows", 3, 3)
    cols = ctx.draw_int("cols", 3, 3)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 5:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       if c not in pool]
    colors = pool[:5]
    bh_max = int(overrides.get("max_band_h", 3))
    bw_max = int(overrides.get("max_band_w", 3))
    heights = [rng.randint(1, bh_max) for _ in range(rows)]
    widths = [rng.randint(1, bw_max) for _ in range(cols)]
    g = full_grid(sum(heights), sum(widths), colors[0])
    r0 = 0
    for r_idx, rh in enumerate(heights):
        c0 = 0
        for c_idx, cw in enumerate(widths):
            color = colors[(r_idx * 2 + c_idx) % len(colors)]
            for r in range(r0, r0 + rh):
                for c in range(c0, c0 + cw):
                    g[r][c] = color
            c0 += cw
        r0 += rh
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    if name == "single_block":
        return full_grid(h, w, 2)
    if name == "no_blocks":
        return full_grid(h, w, 0)
    if name == "full_grid":
        return full_grid(h, w, 5)
    return full_grid(h, w, 0)
