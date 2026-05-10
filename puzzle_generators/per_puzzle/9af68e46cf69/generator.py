"""Generator for b2862040.

Rule: bg=9. For each 1-object, if any 9-region is fully inside its
bbox interior, recolor 1→8.

Combinatorial axes (8): grid_h/w, n_holey, n_solid, frame_size_kind,
solid_shape_kind, position_bias, palette_bg, inter_object_padding.
Degenerates: all_holey, all_solid, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap
from puzzle_generators.helpers.shape import PLUS_5, rect_outline_cells

GENERATOR_ID = "9af68e46cf69"
VERSION = "1.1.0"
TASK_ID = "9af68e46cf69"
SUMMARY = "bg=9; 1-objects with internal holes recolor to 8."

INVARIANTS = [
    "background is 9",
    ">=1 1-object that's a hollow frame (has fully-enclosed 9-region)",
    ">=1 1-object solid or no-hole",
    "objects don't overlap",
    "no color 8 in input (rule writes 8 for output)",
]

FRAME_SIZE_KINDS = ("small", "medium", "large", "rect_3x3",
                    "rect_4x4", "rect_5x5")
SOLID_SHAPE_KINDS = ("plus", "hline", "vline", "block_2x2", "diag")
DEGENERATE_TEXTURES = ("all_holey", "all_solid", "no_objects")
HELPFUL_TEXTURES = FRAME_SIZE_KINDS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":              {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_holey":             {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "n_solid":             {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "frame_size_kind":     {"type": "str", "default": "rng helpful",
                            "valid": "|".join(FRAME_SIZE_KINDS)},
    "solid_shape_kind":    {"type": "str", "default": "rng helpful",
                            "valid": "|".join(SOLID_SHAPE_KINDS)},
    "position_bias":       {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "inter_object_padding": {"type": "int", "default": "1", "valid": "1..3"},
    "texture":             {"type": "str", "default": "alias for frame_size_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 16, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_holey = int(overrides.get("n_holey",
                                ctx.draw_int("n_holey", 1, 2)))
    n_solid = int(overrides.get("n_solid",
                                ctx.draw_int("n_solid", 2, 3)))
    n_holey = max(1, min(4, n_holey))
    n_solid = max(1, min(5, n_solid))
    frame_kind = (overrides.get("texture") or
                  overrides.get("frame_size_kind")
                  or ctx.draw_choice("frame_size_kind",
                                     list(FRAME_SIZE_KINDS)))
    solid_kind = overrides.get("solid_shape_kind",
                               ctx.draw_choice("solid_shape_kind",
                                               list(SOLID_SHAPE_KINDS)))
    padding = int(overrides.get("inter_object_padding", 1))
    g = full_grid(h, w, 9)
    placed_holey = 0
    for _ in range(n_holey * 4):
        if placed_holey >= n_holey:
            break
        fh, fw = _frame_dims(frame_kind, rng)
        if place_no_overlap(rng, g, rect_outline_cells(fh, fw), 1,
                            bg=9, padding=padding, max_tries=40):
            placed_holey += 1
    placed_solid = 0
    for _ in range(n_solid * 4):
        if placed_solid >= n_solid:
            break
        shape = _solid_shape(solid_kind, rng)
        if place_no_overlap(rng, g, shape, 1, bg=9,
                            padding=padding, max_tries=40):
            placed_solid += 1
    if placed_holey < 1:
        place_no_overlap(rng, g, rect_outline_cells(3, 3), 1,
                         bg=9, padding=1, max_tries=20)
    if placed_solid < 1:
        place_no_overlap(rng, g, [(0, 0)], 1, bg=9,
                         padding=1, max_tries=20)
    return g


def _frame_dims(kind, rng):
    if kind == "small":
        return 3, 3
    if kind == "medium":
        return rng.randint(3, 4), rng.randint(3, 4)
    if kind == "large":
        return rng.randint(4, 5), rng.randint(4, 5)
    if kind == "rect_3x3":
        return 3, 3
    if kind == "rect_4x4":
        return 4, 4
    if kind == "rect_5x5":
        return 5, 5
    return rng.randint(3, 5), rng.randint(3, 5)


def _solid_shape(kind, rng):
    if kind == "plus":
        return PLUS_5
    if kind == "hline":
        return [(0, c) for c in range(rng.randint(2, 4))]
    if kind == "vline":
        return [(r, 0) for r in range(rng.randint(2, 4))]
    if kind == "block_2x2":
        return [(0, 0), (0, 1), (1, 0), (1, 1)]
    if kind == "diag":
        n = rng.randint(2, 3)
        return [(i, i) for i in range(n)]
    return [(0, 0)]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 9)
    if name == "all_holey":
        for _ in range(3):
            place_no_overlap(rng, g, rect_outline_cells(3, 3), 1,
                             bg=9, padding=1, max_tries=20)
        return g
    if name == "all_solid":
        for _ in range(4):
            place_no_overlap(rng, g, [(0, 0)], 1, bg=9,
                             padding=1, max_tries=20)
        return g
    if name == "no_objects":
        return g
    return g
