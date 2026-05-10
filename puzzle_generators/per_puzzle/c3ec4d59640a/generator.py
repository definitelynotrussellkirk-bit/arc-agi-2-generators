"""Generator for arc_puzzle_bank_ninth_21_bundle:easy_62_markers_to_keyed_shapes.

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, marker_at_border, unknown_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c3ec4d59640a"
VERSION = "1.1.0"
TASK_ID = "c3ec4d59640a"

SUMMARY = "Color-keyed markers expand to horizontal bars, vertical bars, or pluses."

INVARIANTS = [
    "background is 0",
    "marker colors are only 2, 3, and 4",
    "all markers are interior enough for their keyed shape",
    "shape footprints are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "marker_at_border", "unknown_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "color_keyed_markers",
                       "valid": "color_keyed_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = {
    2: [(0, -1), (0, 0), (0, 1)],
    3: [(-1, 0), (0, 0), (1, 0)],
    4: [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("markers", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("markers", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("markers", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        color = rng.choice([2, 3, 4])
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        footprint = {(r + dr, c + dc) for dr, dc in _SHAPES[color]}
        guard = {
            (rr, cc)
            for fr, fc in footprint
            for rr in range(max(0, fr - 1), min(h, fr + 2))
            for cc in range(max(0, fc - 1), min(w, fc + 2))
        }
        if guard & reserved:
            continue
        g[r][c] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blank → no markers to expand
        return g
    if name == "marker_at_border":
        # markers within 1 of border → expanded shapes go OOB
        g[0][3] = 2  # horizontal bar would go off the top? actually OK; row 0 is fine, but cols
        g[2][0] = 3  # vertical bar OK; but a "left arm" would be at col -1 if bar were horiz
        g[h - 1][6] = 4  # plus would have arms OOB
        return g
    if name == "unknown_color":
        # markers of color outside {2,3,4} → no shape mapping defined
        g[3][3] = 5
        g[5][7] = 6
        return g
    return g
