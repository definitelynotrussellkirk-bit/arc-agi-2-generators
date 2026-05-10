"""Generator for 4347f46a.

Rule: for each non-bg object, erase the strictly-interior cells of its
bbox (keep the frame).

Combinatorial axes (8): grid_h/w, n_objects, palette_size,
object_size_range, object_shape_kind, position_bias,
inter_object_margin, decoy_density.
Degenerates: single_object, no_objects, all_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "b570c79ec730"
VERSION = "1.1.0"
TASK_ID = "b570c79ec730"
SUMMARY = "Solid rectangles ≥3×3; rule erases bbox interior, keeps frame."

INVARIANTS = [
    "background is 0",
    ">=1 solid rectangle of side >=3 (so interior is non-empty)",
    "rectangles don't touch (4-conn separation)",
    "each rectangle is filled with a single non-bg color",
]

OBJECT_SHAPES = ("solid_rect", "tall_rect", "wide_rect", "block_3x3",
                 "block_4x4", "block_5x5")
DEGENERATE_TEXTURES = ("single_object", "no_objects", "all_filled")
HELPFUL_TEXTURES = OBJECT_SHAPES

AXES = {
    "grid_h":              {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":              {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "n_objects":           {"type": "int", "default": "rng 1..3",  "valid": "1..4"},
    "palette_size":        {"type": "int", "default": "= n_objects",
                            "valid": "1..7"},
    "object_shape_kind":   {"type": "str", "default": "rng helpful",
                            "valid": "|".join(OBJECT_SHAPES)},
    "position_bias":       {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "inter_object_margin": {"type": "int", "default": "1", "valid": "1..3"},
    "decoy_density":       {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":             {"type": "str", "default": "alias for object_shape_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 5, 8, 6, 9, 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 11, 18, 14, 20, 2, 4
    else:
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 7, 12, 8, 14, 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_objs = int(overrides.get("n_objects", ctx.draw_int("n_objects", n_lo, n_hi)))
    n_objs = max(1, min(4, n_objs))
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=max(1, n_objs), exclude={0}))
    while len(palette) < n_objs:
        palette.append(palette[0])
    shape_kind = (overrides.get("texture") or overrides.get("object_shape_kind")
                  or ctx.draw_choice("object_shape_kind", list(OBJECT_SHAPES)))
    margin = int(overrides.get("inter_object_margin", 1))
    g = full_grid(h, w, 0)
    placed = 0
    for i in range(n_objs):
        rh, rw = _shape_dims(shape_kind, h, w, rng)
        cells = normalize(rect_cells(rh, rw))
        if place_no_overlap(rng, g, cells, palette[i],
                            bg=0, margin=margin, max_tries=40):
            placed += 1
    if placed < 1:
        rh = min(3, h - 2); rw = min(3, w - 2)
        if rh >= 3 and rw >= 3:
            draw_rect(g, 1, 1, rh, rw, palette[0])
    return g


def _shape_dims(kind, h, w, rng):
    max_h = max(3, h // 2)
    max_w = max(3, w // 2)
    if kind == "block_3x3":
        return 3, 3
    if kind == "block_4x4":
        return min(4, h - 2), min(4, w - 2)
    if kind == "block_5x5":
        return min(5, h - 2), min(5, w - 2)
    if kind == "tall_rect":
        return rng.randint(4, max_h), rng.randint(3, 4)
    if kind == "wide_rect":
        return rng.randint(3, 4), rng.randint(4, max_w)
    return rng.randint(3, max_h), rng.randint(3, max_w)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "single_object":
        rh = min(3, max(3, h // 2))
        rw = min(3, max(3, w // 2))
        draw_rect(g, 1, 1, rh, rw, color)
        return g
    if name == "no_objects":
        return g
    if name == "all_filled":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
