"""Generator for aab50785.

Rule: 2x2 cyan bookends per row; rule extracts content strips and
stacks them.

Combinatorial axes (8): grid_h/w, n_groups, block_w, palette_kind,
left_c, right_c, anchor_corner, palette_size.
Degenerates: no_bookends, single_group, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "6b88648ff0e0"
VERSION = "1.1.0"
TASK_ID = "6b88648ff0e0"
SUMMARY = "2x2 cyan bookends per row; rule extracts content strips and stacks them."

INVARIANTS = [
    ">=1 row groups, each with 2 cyan bookend blocks at same top row",
    "bookends span same column range across rows",
    "content between bookends has uniform width",
    "row groups separated vertically",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bookends", "single_group", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "n_groups":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "block_w":        {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "left_c":         {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "right_c":        {"type": "int", "default": "rng w-4..w-2", "valid": "w-6..w-2"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        ng_lo, ng_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        ng_lo, ng_hi = 3, 4
    else:
        h_lo, h_hi = 12, 16
        ng_lo, ng_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 3, rng)
    g = full_grid(h, w, 0)
    n_groups = int(overrides.get("n_groups",
                                 ctx.draw_int("n_groups", ng_lo, ng_hi)))
    n_groups = max(1, min(4, n_groups))
    block_w = int(overrides.get("block_w",
                                rng.randint(2, 4)))
    block_w = max(2, min(5, block_w))
    left_c = int(overrides.get("left_c", rng.randint(0, 2)))
    right_c = int(overrides.get("right_c",
                                w - 2 - rng.randint(0, 2)))
    if right_c - (left_c + 2) - 2 < 1:
        return _draw_from_degenerate("no_bookends", rng)
    placed = 0
    for gi in range(n_groups):
        top_r = gi * 3 + 1
        if top_r + 1 >= h:
            break
        draw_rect(g, top_r, left_c, 2, 2, 8)
        draw_rect(g, top_r, right_c, 2, 2, 8)
        for r in range(top_r, top_r + 2):
            for c in range(left_c + 2, right_c):
                g[r][c] = rng.choice(palette)
        placed += 1
    if placed == 0:
        return _draw_from_degenerate("no_bookends", rng)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 8)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_bookends":
        for r in range(2):
            for c in range(8):
                g[2 + r][2 + c] = rng.choice([1, 2, 3])
        return g
    if name == "single_group":
        draw_rect(g, 2, 1, 2, 2, 8)
        draw_rect(g, 2, w - 3, 2, 2, 8)
        for r in range(2, 4):
            for c in range(3, w - 3):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
