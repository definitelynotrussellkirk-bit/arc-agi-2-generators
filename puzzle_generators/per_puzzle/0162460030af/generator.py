"""Generator for ARC task 817e6c09.

Rule: separate same-color objects, sort by leftmost column, recolor in
alternating 8 / 2 from left to right.

Combinatorial axes (8): grid_h/w, source_color, object_count,
object_shape_kind, column_spacing, vertical_jitter,
include_decoy_pixels, alt_orientation.
Degenerates: single_object, all_same_left_edge, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0162460030af"
VERSION = "1.1.0"
TASK_ID = "0162460030af"
SUMMARY = "Separated objects sorted by left edge; rule recolors alternating 8 and 2."

INVARIANTS = [
    "background is 0",
    ">=2 objects, all the same source color (≠0,2,8)",
    "objects have distinct leftmost columns",
    "objects are 4-connectivity separated",
]

OBJECT_SHAPES = ("L", "vertical_2", "block_2x2", "T", "diagonal", "single")
DEGENERATE_TEXTURES = ("single_object", "all_same_left_edge", "no_objects")
HELPFUL_TEXTURES = OBJECT_SHAPES

AXES = {
    "grid_h":             {"type": "int", "default": "rng 5..9", "valid": "4..14"},
    "object_count":       {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "source_color":       {"type": "color", "default": "rng (≠0,2,8)", "valid": "1..9 (≠2,8)"},
    "object_shape_kind":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(OBJECT_SHAPES)},
    "column_spacing":     {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "vertical_jitter":    {"type": "bool", "default": "true",  "valid": "true|false"},
    "include_decoy_pixels": {"type": "bool", "default": "false", "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for object_shape_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi, h_lo, h_hi = 2, 3, 5, 6
    elif difficulty == "hard":
        n_lo, n_hi, h_lo, h_hi = 5, 6, 8, 10
    else:
        n_lo, n_hi, h_lo, h_hi = 3, 5, 5, 9
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    count = int(overrides.get("object_count", ctx.draw_int("object_count", n_lo, n_hi)))
    count = max(2, min(6, count))
    color = int(overrides.get("source_color",
                              ctx.draw_color("source_color", exclude={0, 2, 8})))
    shape_kind = (overrides.get("texture") or overrides.get("object_shape_kind")
                  or ctx.draw_choice("object_shape_kind", list(OBJECT_SHAPES)))
    spacing = int(overrides.get("column_spacing", ctx.draw_int("column_spacing", 2, 4)))
    spacing = max(2, min(5, spacing))
    jitter = bool(overrides.get("vertical_jitter", True))
    include_decoy = bool(overrides.get("include_decoy_pixels", False))
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = max(spacing * count + 1, 3 * count + 1)
    g = full_grid(h, w, 0)
    for i in range(count):
        c0 = i * spacing + 1
        r0 = (1 + (i % max(1, h - 3))) if jitter else 1
        _stamp_shape(g, shape_kind, r0, c0, color, h, w, rng)
    if include_decoy:
        decoy = rng.choice([c for c in range(1, 10) if c not in (0, 2, 8, color)])
        for _ in range(rng.randint(1, 3)):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = decoy
    return g


def _stamp_shape(g, kind, r0, c0, color, h, w, rng):
    def _set(rr, cc):
        if 0 <= rr < h and 0 <= cc < w:
            g[rr][cc] = color
    if kind == "L":
        _set(r0, c0); _set(r0 + 1, c0); _set(r0 + 1, c0 + 1)
    elif kind == "vertical_2":
        _set(r0, c0); _set(r0 + 1, c0)
    elif kind == "block_2x2":
        _set(r0, c0); _set(r0, c0 + 1); _set(r0 + 1, c0); _set(r0 + 1, c0 + 1)
    elif kind == "T":
        _set(r0, c0); _set(r0, c0 + 1); _set(r0 + 1, c0)
    elif kind == "diagonal":
        _set(r0, c0); _set(r0 + 1, c0 + 1)
    else:  # single
        _set(r0, c0)


def _draw_from_degenerate(name, rng):
    if name == "single_object":
        h, w = 5, 6
        g = full_grid(h, w, 0)
        color = rng.choice([1, 3, 4, 5, 6, 7, 9])
        g[1][1] = color; g[2][1] = color
        return g
    if name == "all_same_left_edge":
        h, w = 7, 5
        g = full_grid(h, w, 0)
        color = rng.choice([1, 3, 4, 5, 6, 7, 9])
        g[1][1] = color; g[3][1] = color; g[5][1] = color
        return g
    if name == "no_objects":
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    return [[0]]
