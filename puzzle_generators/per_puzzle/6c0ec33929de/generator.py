"""Generator for a48eeaf7.

Rule: gray pixels move in straight lines toward red block, stopping one
cell outside its bbox.

Combinatorial axes (8): grid_h/w, gray_count, palette_kind, block_h,
block_w, position_bias, anchor_corner, asymmetry_force.
Degenerates: no_block, no_grays, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "6c0ec33929de"
VERSION = "1.1.0"
TASK_ID = "6c0ec33929de"
SUMMARY = "Gray pixels move toward red block, stopping one cell outside its bbox."

INVARIANTS = [
    "background is color 0",
    "red cells form one solid rectangular block",
    "gray cells lie outside the block in straight or diagonal directions",
    "the output keeps the red block and places grays on the one-cell perimeter reached from each source gray",
]

POSITION_BIASES = ("centered", "scattered", "near_corner", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_block", "no_grays", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..15", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "10..20"},
    "gray_count":     {"type": "int", "default": "4", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "block_h":        {"type": "int", "default": "2", "valid": "2..4"},
    "block_w":        {"type": "int", "default": "2", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 10, 12
        gc_lo, gc_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        gc_lo, gc_hi = 5, 8
    else:
        h_lo, h_hi = 13, 15
        gc_lo, gc_hi = 4, 5
    h = rng.randint(h_lo, h_hi)
    w = rng.randint(h_lo, h_hi)
    g = full_grid(h, w, 0)
    gc = ctx.draw_int("gray_count", gc_lo, gc_hi)
    gc = max(1, min(8, gc))
    bh = int(overrides.get("block_h", 2))
    bw = int(overrides.get("block_w", 2))
    bh = max(2, min(bh, 4))
    bw = max(2, min(bw, 4))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        r1 = max(4, (h - bh) // 2)
        c1 = max(4, (w - bw) // 2)
    elif bias == "near_corner":
        r1 = rng.choice([4, max(4, h - bh - 4)])
        c1 = rng.choice([4, max(4, w - bw - 4)])
    else:
        r1 = 4 + rng.randint(0, max(0, h - bh - 7))
        c1 = 4 + rng.randint(0, max(0, w - bw - 7))
    r2 = r1 + bh - 1
    c2 = c1 + bw - 1
    fill_box(g, r1, c1, r2, c2, 2)
    grays = [(r1 - 4, c1), (r2 + 4, c2), (r1, c1 - 4), (r1 - 3, c1 - 3)]
    for i, (r, c) in enumerate(grays[:gc]):
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_block":
        for r, c in [(2, 2), (5, 8), (8, 3)]:
            g[r][c] = 5
        return g
    if name == "no_grays":
        fill_box(g, 6, 6, 7, 7, 2)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
