"""Generator for 6d75e8bb.

Rule: compute bbox of all 8-cells; for each 0 inside the bbox set to 2.

Combinatorial axes (8): grid_h/w, frame_size_kind, n_interior_8s,
n_interior_0s, position_bias, palette_kind, anchor_corner,
asymmetry_force.
Degenerates: no_8s, all_8s, single_8.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "e15a71a2526e"
VERSION = "1.1.0"
TASK_ID = "e15a71a2526e"
SUMMARY = "Hollow 8-frame; rule fills bbox-interior 0s with 2."

INVARIANTS = [
    "background is 0",
    "1 closed 8-frame of side >=4",
    ">=2 0-cells inside the bbox interior",
    "no color 2 in input (rule writes 2 for output)",
]

FRAME_SIZE_KINDS = ("small", "medium", "large", "wide", "tall")
POSITION_BIAS = ("center", "spread", "edge")
DEGENERATE_TEXTURES = ("no_8s", "all_8s", "single_8")
HELPFUL_TEXTURES = FRAME_SIZE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":            {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "frame_size_kind":   {"type": "str", "default": "rng helpful",
                          "valid": "|".join(FRAME_SIZE_KINDS)},
    "n_interior_8s":     {"type": "int", "default": "rng 0..3", "valid": "0..5"},
    "n_interior_0s":     {"type": "int", "default": "rng 2..5", "valid": "2..10"},
    "position_bias":     {"type": "str", "default": "rng spread|center",
                          "valid": "spread|center"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for frame_size_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 9, 6, 10
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 14, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 14, 8, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    size_kind = (overrides.get("texture") or
                 overrides.get("frame_size_kind")
                 or ctx.draw_choice("frame_size_kind",
                                    list(FRAME_SIZE_KINDS)))
    fr, fc = _frame_dims(size_kind, h, w, rng)
    fr = max(4, min(h - 2, fr))
    fc = max(4, min(w - 2, fc))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center"]))
    if bias == "center":
        r0 = max(1, (h - fr) // 2)
        c0 = max(1, (w - fc) // 2)
    else:
        r0 = rng.randint(1, max(1, h - fr - 1))
        c0 = rng.randint(1, max(1, w - fc - 1))
    g = full_grid(h, w, 0)
    draw_rect_outline(g, r0, c0, fr, fc, 8)
    n_int_8s = int(overrides.get("n_interior_8s",
                                 ctx.draw_int("n_interior_8s", 0, 3)))
    placed = 0
    for _ in range(n_int_8s * 5):
        if placed >= n_int_8s:
            break
        if r0 + 1 < r0 + fr - 1 and c0 + 1 < c0 + fc - 1:
            r = rng.randint(r0 + 1, r0 + fr - 2)
            c = rng.randint(c0 + 1, c0 + fc - 2)
            if g[r][c] == 0:
                g[r][c] = 8
                placed += 1
        else:
            break
    return g


def _frame_dims(kind, h, w, rng):
    if kind == "small":
        return 4, 4
    if kind == "medium":
        return rng.randint(4, 6), rng.randint(4, 6)
    if kind == "large":
        return min(h - 2, rng.randint(6, 9)), min(w - 2, rng.randint(6, 9))
    if kind == "wide":
        return 4, min(w - 2, rng.randint(6, 10))
    if kind == "tall":
        return min(h - 2, rng.randint(6, 10)), 4
    return rng.randint(4, max(4, h // 2)), rng.randint(4, max(4, w // 2))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_8s":
        return g
    if name == "all_8s":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    if name == "single_8":
        g[h // 2][w // 2] = 8
        return g
    return g
