"""Generator for 11b:hard_73 — choose most holes, scale2, recolor.

Rule: a single-cell marker provides a target color. Among multi-cell
shapes, find the one with the most bbox-interior bg cells (holes).
Output: that shape cropped, scaled 2x, recolored to marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker (no isolated single-cell marker → rule's
target-color selector returns nothing), tied_holes (≥2 shapes share
max hole-count → "most holes" is ambiguous, tie-break decides),
all_solid (every shape has 0 holes → rule's hole-rank is uniform,
no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5df4d341f399"
VERSION = "1.1.0"
TASK_ID = "5df4d341f399"
SUMMARY = "1 single-cell marker + 2-3 shapes with strictly distinct hole counts."

INVARIANTS = [
    "background is 0",
    "exactly one isolated single-cell marker",
    "2-3 multi-cell shapes, distinct colors, with strictly distinct hole counts",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "tied_holes", "all_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "grid_w":            {"type": "int", "default": "rng 14..17", "valid": "13..20"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "marker_plus_distinct_hole_shapes",
                          "valid": "marker_plus_distinct_hole_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_HOLES = {
    0: [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
    ],
    1: [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    ],
    2: [
        [(0, 0), (0, 1), (0, 2), (0, 3),
         (1, 0), (1, 3),
         (2, 0), (2, 3),
         (3, 0), (3, 1), (3, 2), (3, 3)],
    ],
    3: [
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
         (1, 0), (1, 4),
         (2, 0), (2, 4),
         (3, 0), (3, 4),
         (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
    ],
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 13, 13)
        w = ctx.draw_int("grid_w", 14, 15)
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 16, 17)
        n_lo, n_hi = 3, 3
    else:
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 14, 17)
        n_lo, n_hi = 2, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_shapes = rng.randint(n_lo, n_hi)
    palette = rng.sample([2, 3, 4, 6, 7, 8, 9], n_shapes + 1)
    marker_color = palette[0]
    shape_colors = palette[1:]
    keys = rng.sample([0, 1, 2, 3], n_shapes)
    for k, color in zip(keys, shape_colors):
        shapes = _BY_HOLES[k]
        _place(g, rng, rng.choice(shapes), color)
    for _ in range(60):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        bad = False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                    bad = True; break
            if bad: break
        if bad: continue
        g[r][c] = marker_color; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 15
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # No isolated single-cell marker — rule's target-color selector
        # returns nothing.
        for c in range(1, 4): g[1][c] = 4; g[3][c] = 4
        g[2][1] = 4; g[2][3] = 4
        for r in range(7, 10):
            for c in range(8, 11): g[r][c] = 6
        return g
    if name == "tied_holes":
        # Two shapes share max hole-count (both 1-hole rings) — "most"
        # is ambiguous.
        for c in range(1, 4): g[1][c] = 4; g[3][c] = 4
        g[2][1] = 4; g[2][3] = 4
        for c in range(8, 11): g[1][c] = 6; g[3][c] = 6
        g[2][8] = 6; g[2][10] = 6
        g[10][12] = 7   # marker
        return g
    if name == "all_solid":
        # Every shape has 0 holes — rule's hole-rank is uniform.
        for r in range(1, 3):
            for c in range(1, 3): g[r][c] = 4
        for r in range(6, 9):
            for c in range(6, 9): g[r][c] = 6
        for r in range(11, 13):
            for c in range(11, 14): g[r][c] = 8
        g[1][13] = 7   # marker
        return g
    return g
