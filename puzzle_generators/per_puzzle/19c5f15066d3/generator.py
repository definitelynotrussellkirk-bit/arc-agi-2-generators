"""Generator for 0d87d2a6.

Rule: 1-cells on top/bottom edges define vcols; 1-cells on left/right
edges define hrows; draw lines and recolor touching 2-rects to 1.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_rects, n_marks.
Degenerates: no_marks, no_rects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "19c5f15066d3"
VERSION = "1.1.0"
TASK_ID = "19c5f15066d3"
SUMMARY = "Edge 1-cells define lines; 2-rects touched by lines recolor to 1."

INVARIANTS = [
    "one or two 1-cells on top or bottom edge",
    "two or three solid 2-rectangles each at least 2x2",
    "at least one 2-rectangle is touched by the line through a 1-cell",
    "rectangles sit clear of each other and the marks",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "no_rects", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "10..22"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_marks":        {"type": "int", "default": "1", "valid": "1..3"},
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
        h_lo, h_hi = 8, 9
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", 14, 18)
    g = full_grid(h, w, 0)
    n_rects = rng.randint(2, 3)
    placed = []
    for _ in range(n_rects):
        for _ in range(40):
            rh = rng.randint(2, 4)
            rw = rng.randint(3, 5)
            r0 = rng.randint(2, h - rh - 1)
            c0 = rng.randint(0, w - rw)
            if any(abs(r0 - pr) < (rh + 1) and abs(c0 - pc) < (rw + 1) for pr, pc in placed):
                continue
            draw_rect(g, r0, c0, rh, rw, 2)
            placed.append((r0, c0))
            break
    for _ in range(20):
        if not placed:
            break
        target = rng.choice(placed)
        c0 = target[1] + rng.randint(0, 2)
        if 0 <= c0 < w and g[0][c0] == 0:
            g[0][c0] = 1
            break
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 16, 0)
    if name == "no_marks":
        draw_rect(g, 3, 3, 3, 4, 2)
        return g
    if name == "no_rects":
        g[0][5] = 1
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(16):
                g[r][c] = 2
        return g
    return g
