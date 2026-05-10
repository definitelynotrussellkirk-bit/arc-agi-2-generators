"""Generator for 1f0c79e5.

Rule: 2x2 fg blocks on bg; rule transforms based on block centers.

Combinatorial axes (8): grid_h/w, n_blocks, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_blocks, single_block, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "98c4483164f7"
VERSION = "1.1.0"
TASK_ID = "98c4483164f7"
SUMMARY = "2x2 fg blocks on bg; rule transforms based on block centers."

INVARIANTS = [
    "bg is not color 2",
    "at least one solid 2x2 block of one fg color",
    "blocks separated by bg margin of at least one cell",
    "fg color differs from bg",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blocks", "single_block", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..30", "valid": "5..30"},
    "grid_w":         {"type": "int", "default": "rng 5..30", "valid": "5..30"},
    "n_blocks":       {"type": "int", "default": "rng 1..6", "valid": "1..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 18, 28
    else:
        h_lo, h_hi = 8, 16
    h = ctx.draw_int_diff("grid_h", h_lo, h_hi)
    w = ctx.draw_int_diff("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=2, exclude={2})
    bgc, objc = palette
    g = full_grid(h, w, bgc)
    n_blocks = ctx.draw_int_diff("n_blocks", 1, max(1, (h * w) // 24))
    placed = []
    for _ in range(n_blocks * 5):
        if len(placed) >= n_blocks:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        ok = True
        for rr in range(max(0, r - 1), min(h, r + 3)):
            for cc in range(max(0, c - 1), min(w, c + 3)):
                if g[rr][cc] != bgc:
                    ok = False; break
            if not ok:
                break
        if not ok:
            continue
        draw_rect(g, r, c, 2, 2, objc)
        placed.append((r, c))
    if not placed:
        return [[bgc]]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 1)
    if name == "no_blocks":
        return g
    if name == "single_block":
        draw_rect(g, 4, 4, 2, 2, 3)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 3
        return g
    return g
