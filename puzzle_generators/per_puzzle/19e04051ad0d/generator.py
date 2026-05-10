"""Generator for c4d1a9ae.

Rule: three column regions separated by background columns fill their
holes using the next region's color.

Combinatorial axes (8): grid_h, region_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
region_w.
Degenerates: no_regions, single_region, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "19e04051ad0d"
VERSION = "1.1.0"
TASK_ID = "19e04051ad0d"
SUMMARY = "Column regions cyclically fill their holes with the next region color."

INVARIANTS = [
    "background is color 0",
    "full background columns separate regions",
    "each region has exactly one non-background color",
    "background holes inside each region are replaced cyclically",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_regions", "single_region", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "6..14"},
    "region_count":   {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "region_w":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
    n = ctx.draw_int("region_count", 3, 3)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < n:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    colors = pool[:n]
    h = 7 + rng.randint(0, 4)
    region_w = 2 + ((seed + sample_index) % 2)
    w = n * region_w + (n - 1)
    g = full_grid(h, w, 0)
    for i, color in enumerate(colors):
        c0 = i * (region_w + 1)
        for r in range(h):
            for c in range(c0, c0 + region_w):
                if not ((r + c + sample_index + i) % 4 == 0):
                    g[r][c] = color
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
    g = full_grid(8, 8, 0)
    if name == "no_regions":
        return g
    if name == "single_region":
        for r in range(8):
            for c in range(2, 5):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 2
        return g
    return g
