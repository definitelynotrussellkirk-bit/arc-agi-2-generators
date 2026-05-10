"""Generator for 332202d5.

Rule: horizontal color stripes interpolate row fills while a vertical
8/1 stripe marks stripe rows.

Combinatorial axes (8): height, width, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, stripe_count.
Degenerates: no_stripes, no_vstripe, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "823621e5aa1f"
VERSION = "1.1.0"
TASK_ID = "823621e5aa1f"
SUMMARY = "Horizontal stripes interpolate rows; vertical 8/1 column marks stripe rows."

INVARIANTS = [
    "one column contains only colors 8 and 1",
    "an adjacent scan column contains sparse horizontal stripe colors",
    "rows between stripe markers inherit or split neighboring stripe colors",
    "stripe colors are distinct and avoid colors 1, 7 and 8",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_stripes", "no_vstripe", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 9..13", "valid": "5..30"},
    "width":          {"type": "int", "default": "rng 5..8", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "stripe_count":   {"type": "int", "default": "3", "valid": "3"},
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
        h_lo, h_hi = 9, 11
    elif difficulty == "hard":
        h_lo, h_hi = 13, 16
    else:
        h_lo, h_hi = 9, 13
    h = ctx.draw_int("height", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [2, 3, 4, 5, 6, 9] if c not in pool]
    stripe_colors = pool[:3]
    w = rng.randint(5, 8)
    vc = 1
    g = full_grid(h, w, 7)
    for r in range(h):
        g[r][vc] = 8 if rng.choice([True, False]) else 1
    rows = sorted({1, h // 2, h - 2})
    for i, r in enumerate(rows):
        g[r][0] = stripe_colors[i % len(stripe_colors)]
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 9]
    pool = [c for c in pool if c not in (0, 1, 7, 8)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 6, 7)
    if name == "no_stripes":
        for r in range(10):
            g[r][1] = 1
        return g
    if name == "no_vstripe":
        g[1][0] = 2
        g[5][0] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(6):
                g[r][c] = 7
        return g
    return g
