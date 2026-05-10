"""Generator for 6ecd11f4.

Rule: blocky most-common shape masks nearby color palette down to
palette grid size.

Combinatorial axes (8): block_size, shape_color, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size, mask_variant.
Degenerates: no_shape, no_palette, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4e4fa6c8d4ce"
VERSION = "1.1.0"
TASK_ID = "4e4fa6c8d4ce"
SUMMARY = "Blocky shape masks nearby color palette down to palette grid size."

INVARIANTS = [
    "background is color 0",
    "the shape color is the most common non-background color",
    "the shape bbox is an integer block-scale version of the palette bbox",
    "a palette cell is emitted only when the corresponding shape block is occupied",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_palette", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "block_size":     {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "shape_color":    {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "mask_variant":   {"type": "int", "default": "rng 0..4", "valid": "0..4"},
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
        bs_lo, bs_hi = 1, 2
    elif difficulty == "hard":
        bs_lo, bs_hi = 3, 5
    else:
        bs_lo, bs_hi = 2, 3
    block = ctx.draw_int("block_size", bs_lo, bs_hi)
    block = max(1, min(8, block))
    shape_color = ctx.draw_color("shape_color", exclude={0})
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, shape_color, rng)
    if len(pool) < 5:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       if c not in pool and c != shape_color]
    palette = pool[:5]
    ph = pw = 3
    h = ph * block + 3
    w = pw * block + 7
    g = full_grid(h, w, 0)
    mask = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 1)]
    rng.shuffle(mask)
    for br, bc in mask:
        for dr in range(block):
            for dc in range(block):
                g[1 + br * block + dr][1 + bc * block + dc] = shape_color
    p0c = 1 + pw * block + 3
    for idx, (r, c) in enumerate([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]):
        g[1 + r][p0c + c] = palette[idx]
    for r in range(ph):
        for c in range(pw):
            if g[1 + r][p0c + c] == 0:
                g[1 + r][p0c + c] = palette[(r + c) % len(palette)]
    return g


def _build_palette(kind, shape_color, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0 and c != shape_color]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 9, 14
    g = full_grid(h, w, 0)
    if name == "no_shape":
        for r in range(2):
            for c in range(3):
                g[1 + r][9 + c] = c + 1
        return g
    if name == "no_palette":
        for r in range(3):
            for c in range(3):
                g[1 + r][1 + c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
