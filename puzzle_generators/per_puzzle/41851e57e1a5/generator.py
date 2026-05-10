"""Generator for 9b:m58 — fill bbox overlap by key.

Rule: red = color-2 cells; blue = color-1 cells. key = the first
non-{0,1,2} color in scan order. Output is a same-size grid with the
red-bbox ∩ blue-bbox rectangle painted in `key`, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_overlap (red-bbox and blue-bbox disjoint → rule's
intersection rectangle is empty, output is all bg), missing_red
(red shape absent → rule's selector finds no red bbox, intersection
undefined), no_key (no non-{0,1,2} cell → rule's `first non-{0,1,2}`
selector returns nothing, paint color undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "41851e57e1a5"
VERSION = "1.1.0"
TASK_ID = "41851e57e1a5"

SUMMARY = "1 red shape (color 2) + 1 blue shape (color 1) with overlapping bboxes + 1 key marker."

INVARIANTS = [
    "background is 0",
    "exactly one color-2 multi-cell shape and one color-1 multi-cell shape",
    "their bboxes have a non-empty intersection (≥1 cell overlap)",
    "exactly one isolated key cell with color in {3..9}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_overlap", "missing_red", "no_key")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "red_blue_overlap_plus_key",
                          "valid": "red_blue_overlap_plus_key"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]


def _too_close(g, r, c) -> bool:
    h, w = len(g), len(g[0])
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")
    for outer in range(40):
        g = full_grid(h, w, 0)
        red_shape = rng.choice(_SHAPES)
        blue_shape = rng.choice(_SHAPES)
        rh = max(r for r, _ in red_shape) + 1
        rw = max(c for _, c in red_shape) + 1
        bh = max(r for r, _ in blue_shape) + 1
        bw = max(c for _, c in blue_shape) + 1
        red_r0 = rng.randint(0, h - rh); red_c0 = rng.randint(0, w - rw)
        ok = False
        for _ in range(80):
            d_r = rng.randint(-(bh - 1), rh - 1)
            d_c = rng.randint(-(bw - 1), rw - 1)
            blue_r0 = red_r0 + d_r
            blue_c0 = red_c0 + d_c
            if blue_r0 < 0 or blue_c0 < 0: continue
            if blue_r0 + bh > h or blue_c0 + bw > w: continue
            red_cells = {(red_r0 + dr, red_c0 + dc) for dr, dc in red_shape}
            blue_cells = {(blue_r0 + dr, blue_c0 + dc) for dr, dc in blue_shape}
            if red_cells & blue_cells: continue
            ok = True; break
        if not ok: continue
        for r, c in red_cells: g[r][c] = 2
        for r, c in blue_cells: g[r][c] = 1
        placed_key = False
        key_color = rng.choice([3, 4, 5, 6, 7, 8, 9])
        for _ in range(60):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0 or _too_close(g, r, c): continue
            g[r][c] = key_color
            placed_key = True; break
        if placed_key:
            return g
    raise ValueError("could not realize red+blue overlap + key in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_overlap":
        # Red and blue bboxes are disjoint — rule's intersection
        # rectangle is empty; output is all bg.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[7 + dr][8 + dc] = 1
        g[5][5] = 4
        return g
    if name == "missing_red":
        # No red shape — rule's red-bbox selector finds nothing;
        # intersection is undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 1)]:
            g[3 + dr][4 + dc] = 1
        g[6][6] = 4
        return g
    if name == "no_key":
        # No non-{0,1,2} cell — rule's `first non-{0,1,2}` selector
        # returns nothing; paint color is undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 2
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[2 + dr][4 + dc] = 1
        return g
    return g
