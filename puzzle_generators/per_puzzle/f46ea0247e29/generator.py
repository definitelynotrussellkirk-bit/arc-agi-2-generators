"""Generator for puzzle 52364a65.

Rule: for each non-bg connected component, erase the two leftmost
columns of its bbox (replace with bg).

Combinatorial axes (8): grid_h/w, n_objs, object_shape_kind,
min_object_w, palette_size, inter_object_margin, decoy_density,
position_bias.
Degenerates: single_object, narrow_objects, full_grid_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "f46ea0247e29"
VERSION = "1.1.0"
TASK_ID = "f46ea0247e29"
SUMMARY = "Several non-bg objects ≥3 cols wide; rule trims 2 leftmost cols of each."

INVARIANTS = [
    "background is 0",
    ">=2 non-bg connected components",
    "each component is at least 3 columns wide",
    "components separated by margin >= 1",
]

OBJECT_SHAPES = ("rect", "L_shape", "T_shape", "U_shape", "tall_rect", "wide_rect")
DEGENERATE_TEXTURES = ("single_object", "narrow_objects", "full_grid_object")
HELPFUL_TEXTURES = OBJECT_SHAPES

AXES = {
    "grid_h":              {"type": "int", "default": "rng 10..16", "valid": "8..22"},
    "grid_w":              {"type": "int", "default": "rng 12..20", "valid": "10..28"},
    "n_objs":              {"type": "int", "default": "rng 2..4",   "valid": "2..5"},
    "object_shape_kind":   {"type": "str", "default": "rng helpful",
                            "valid": "|".join(OBJECT_SHAPES)},
    "min_object_w":        {"type": "int", "default": "3", "valid": "3..6"},
    "inter_object_margin": {"type": "int", "default": "1", "valid": "1..3"},
    "position_bias":       {"type": "str", "default": "rng spread|left|right",
                            "valid": "spread|left|right"},
    "palette_size":        {"type": "int", "default": "= n_objs", "valid": "2..7"},
    "texture":             {"type": "str", "default": "alias for object_shape_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 8, 12, 10, 14, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 14, 18, 18, 24, 3, 5
    else:
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 10, 16, 12, 20, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_objs = int(overrides.get("n_objs", ctx.draw_int("n_objs", n_lo, n_hi)))
    n_objs = max(2, min(5, n_objs))
    palette = list(ctx.draw_distinct_colors("palette", n=n_objs, exclude={0}))
    shape_kind = (overrides.get("texture") or overrides.get("object_shape_kind")
                  or ctx.draw_choice("object_shape_kind", list(OBJECT_SHAPES)))
    min_ow = int(overrides.get("min_object_w", 3))
    margin = int(overrides.get("inter_object_margin", 1))
    g = full_grid(h, w, 0)
    placed = 0
    for i in range(n_objs):
        cells = _shape_cells(shape_kind, h, w, min_ow, rng)
        if place_no_overlap(rng, g, cells, palette[i], bg=0,
                            margin=margin, max_tries=60):
            placed += 1
    if placed < 2:
        cells = normalize(rect_cells(2, 3))
        place_no_overlap(rng, g, cells, palette[0], bg=0, margin=1, max_tries=10)
        cells2 = normalize(rect_cells(2, 4))
        place_no_overlap(rng, g, cells2,
                         palette[1] if len(palette) > 1 else palette[0],
                         bg=0, margin=1, max_tries=10)
    return g


def _shape_cells(kind, h, w, min_ow, rng):
    rh = rng.randint(2, max(2, h // 4))
    rw = rng.randint(min_ow, max(min_ow, w // 3))
    if kind == "tall_rect":
        rh = rng.randint(3, max(3, h // 3))
        rw = rng.randint(min_ow, min_ow + 1)
    elif kind == "wide_rect":
        rh = rng.randint(2, 3)
        rw = rng.randint(max(min_ow, 4), max(min_ow + 1, w // 3))
    elif kind == "L_shape":
        cells = []
        for c in range(rw):
            cells.append((0, c))
        for r in range(1, rh):
            cells.append((r, 0))
        return normalize(cells)
    elif kind == "T_shape":
        cells = []
        for c in range(rw):
            cells.append((0, c))
        for r in range(1, rh):
            cells.append((r, rw // 2))
        return normalize(cells)
    elif kind == "U_shape":
        cells = []
        for r in range(rh):
            cells.append((r, 0))
            cells.append((r, rw - 1))
        for c in range(rw):
            cells.append((rh - 1, c))
        return normalize(cells)
    return normalize(rect_cells(rh, rw))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "single_object":
        for r in range(2, 5):
            for c in range(2, 7):
                g[r][c] = color
        return g
    if name == "narrow_objects":
        for r in range(2, 6):
            g[r][2] = color
        color2 = rng.choice([c for c in range(1, 10) if c != color])
        for r in range(2, 6):
            g[r][6] = color2
        return g
    if name == "full_grid_object":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
