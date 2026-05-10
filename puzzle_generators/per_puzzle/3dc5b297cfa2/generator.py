"""Generator for fc4aaf52.

Rule: 2-color shape: top-half shifts right (color-swapped), bottom-half
stays.

Combinatorial axes (8): grid_h/w, palette_kind, bbox_h, bbox_w,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_color, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3dc5b297cfa2"
VERSION = "1.1.0"
TASK_ID = "3dc5b297cfa2"
SUMMARY = "2-color shape: top-half shifts right (color-swapped), bottom-half stays (color-swapped)."

INVARIANTS = [
    "background is 0",
    "exactly 2 distinct non-bg colors",
    "bbox right edge + shift <= w-1",
    "both halves of bbox have at least one non-bg cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_color", "no_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bbox_h":         {"type": "int", "default": "rng 4..h-3", "valid": "4..h-3"},
    "bbox_w":         {"type": "int", "default": "rng 3..w/2-1", "valid": "3..w/2"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered|left|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
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
        h_lo, h_hi, w_lo, w_hi = 8, 10, 12, 14
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 14, 18, 18, 22
    else:
        h_lo, h_hi, w_lo, w_hi = 10, 14, 14, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    palette = ctx.draw_distinct_colors("palette", n=2, exclude={0})
    c1, c2 = palette
    g = full_grid(h, w, 0)
    bh = rng.randint(4, h - 3)
    bw = rng.randint(3, max(3, (w - 2) // 2))
    rr = rng.randint(1, h - bh - 1)
    rc = rng.randint(0, w - 2 * bw - 1)
    rmid = rr + bh // 2
    for dr in range(bh):
        for dc in range(bw):
            if rng.random() < 0.5:
                g[rr + dr][rc + dc] = c1 if rng.random() < 0.5 else c2
    g[rr][rc] = c1
    g[rr + bh - 1][rc + bw - 1] = c2
    g[rr][rc + bw - 1] = c2
    g[rr + bh - 1][rc] = c1
    if bh >= 2:
        top_r = rng.randint(rr, rmid)
        bot_r = rng.randint(rmid + 1, rr + bh - 1)
        top_c = rng.randint(rc, rc + bw - 1)
        bot_c = rng.randint(rc, rc + bw - 1)
        g[top_r][top_c] = c1
        g[bot_r][bot_c] = c2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "same_color":
        for r in range(2, 8):
            for c in range(2, 6):
                g[r][c] = 2
        return g
    if name == "no_shape":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
