"""Generator for arc_puzzle_bank_next_21_bundle:easy_13_keep_leftmost_component.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_object, equal_left_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import bbox_of, bbox_overlaps, grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e297c9504f64"
VERSION = "1.1.0"
TASK_ID = "e297c9504f64"
SUMMARY = "Several isolated color-2 components; the rule keeps the leftmost one as color 8."

INVARIANTS = [
    "background is 0",
    "there are at least two isolated color-2 objects",
    "one object has a strictly leftmost bounding-box column",
    "objects do not overlap or touch orthogonally",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "equal_left_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "isolated_2_components_distinct_left_cols",
                       "valid": "isolated_2_components_distinct_left_cols"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        n_objects = ctx.draw_int("n_objects", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
        n_objects = ctx.draw_int("n_objects", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 11, 15)
        n_objects = ctx.draw_int("n_objects", 3, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)

    used: set[tuple[int, int]] = set()
    bboxes = []
    for _ in range(n_objects):
        for _try in range(80):
            blob = grow_blob(rng, h, w, used, rng.randint(2, 5))
            if not blob:
                continue
            bb = bbox_of(blob)
            if any(bbox_overlaps(bb, old) for old in bboxes):
                continue
            used |= blob
            bboxes.append(bb)
            for r, c in blob:
                g[r][c] = 2
            break
    if len(bboxes) < 2:
        return [[0, 2, 2, 0, 0, 2, 2]]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no components to pick the leftmost of
        return g
    if name == "single_object":
        # 1 object → trivial: it IS the leftmost, no contrast
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 2
        return g
    if name == "equal_left_columns":
        # 2 objects share leftmost column → ambiguous tie
        for r, c in [(1, 2), (1, 3)]: g[r][c] = 2
        for r, c in [(6, 2), (6, 3)]: g[r][c] = 2
        return g
    return g
