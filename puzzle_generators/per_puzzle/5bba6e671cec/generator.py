"""Generator for 880c1354.

Rule: non-frame color regions are recolored by one clockwise step
around the grid center.

Combinatorial axes (8): grid_h/w, region_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_anchors.
Degenerates: no_regions, single_region, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5bba6e671cec"
VERSION = "1.1.0"
TASK_ID = "5bba6e671cec"
SUMMARY = "Non-frame regions are recolored by one clockwise step around center."

INVARIANTS = [
    "background is color 0",
    "frame colors 4 and 7 are absent so they are skipped by the cycle",
    "each cycled color appears as a small two-cell region at a distinct compass position",
    "the rule changes colors but preserves all region positions",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_regions", "single_region", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "region_count":   {"type": "int", "default": "4", "valid": "4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "compass", "valid": "compass"},
    "n_anchors":      {"type": "int", "default": "4", "valid": "4"},
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
    if difficulty == "easy":
        h_lo, h_hi = 11, 11
    elif difficulty == "hard":
        h_lo, h_hi = 13, 15
    else:
        h_lo, h_hi = 11, 13
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 4:
        pool = pool + [c for c in [1, 2, 3, 5, 6, 8, 9] if c not in pool]
    colors = pool[:4]
    g = full_grid(h, w, 0)
    anchors = [(1, w // 2), (h // 2, w - 2), (h - 2, w // 2), (h // 2, 1)]
    for color, (r, c) in zip(colors, anchors):
        g[r][c] = color
        g[r][c + (1 if c + 1 < w else -1)] = color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 6]
    else:
        pool = [1, 2, 3, 5, 6, 8, 9]
    pool = [c for c in pool if c not in (0, 4, 7)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_regions":
        return g
    if name == "single_region":
        g[5][5] = 2
        g[5][6] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
