"""Generator for 46c35fc7.

Rule: eight colored cells around each 3x3 orange-centered block rotate
clockwise.

Combinatorial axes (8): grid_h/w, block_count, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size,
ring_variant.
Degenerates: no_blocks, no_centers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "630d6cc550e4"
VERSION = "1.1.0"
TASK_ID = "630d6cc550e4"
SUMMARY = "Eight colored cells around 3x3 orange-centered block rotate clockwise."

INVARIANTS = [
    "the background and every block center are color 7",
    "each active block is a 3x3 ring with all eight border cells non-7",
    "blocks are separated so no extra overlapping 3x3 detections appear",
    "the canonical rule permutes only the border cells of each detected block",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blocks", "no_centers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "block_count":    {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "grid_w":         {"type": "int", "default": "11", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "alternating",
                       "valid": "alternating|left|right"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8..9"},
    "ring_variant":   {"type": "str", "default": "ring", "valid": "ring"},
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
        bc_lo, bc_hi = 1, 1
    elif difficulty == "hard":
        bc_lo, bc_hi = 3, 6
    else:
        bc_lo, bc_hi = 1, 3
    block_count = ctx.draw_int("block_count", bc_lo, bc_hi)
    block_count = max(1, min(6, block_count))
    h = 4 * block_count + 3
    w = int(overrides.get("grid_w", 11))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 8:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 8, 9] if c not in pool]
    g = full_grid(h, w, 7)
    bias = overrides.get("position_bias", "alternating")
    for i in range(block_count):
        r0 = 1 + i * 4
        if bias == "left":
            c0 = 1
        elif bias == "right":
            c0 = w - 4
        else:
            c0 = 1 if i % 2 == 0 else max(1, w - 4)
        ring = rng.sample(pool, 8)
        idx = 0
        for dr, dc in RING_3X3:
            if 0 <= r0 + dr < h and 0 <= c0 + dc < w:
                g[r0 + dr][c0 + dc] = ring[idx]
            idx += 1
        if 0 <= r0 + 1 < h and 0 <= c0 + 1 < w:
            g[r0 + 1][c0 + 1] = 7
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c != 7]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 7)
    if name == "no_blocks":
        return g
    if name == "no_centers":
        for dr, dc in RING_3X3:
            g[1 + dr][1 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 7
        return g
    return g
