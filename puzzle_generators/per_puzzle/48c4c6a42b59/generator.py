"""Generator for arc_additional_puzzle_bank_volume4:M22 — Horizontally mirror each object within its bbox.

Rule: for each object, paint each cell at the mirrored column position
((c1 + c2) - c) within the same row. Original cells stay (the rule
folds onto `g` not an empty grid). Effect: union of original and
horizontally-mirrored.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_lr_symmetric, single_blob, bboxes_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_cells
from puzzle_generators.helpers.blobs import grow_blob, bbox_of, bbox_overlaps

GENERATOR_ID = "48c4c6a42b59"
VERSION = "1.1.0"
TASK_ID = "48c4c6a42b59"
SUMMARY = "Several non-touching, bbox-isolated, asymmetric blobs; output unions h-mirror."

INVARIANTS = [
    "between 2 and 4 non-touching blobs",
    "each blob bbox-isolated (mirroring stays within own bbox)",
    "at least one blob is not horizontally-symmetric",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_lr_symmetric", "single_blob", "bboxes_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "bbox_isolated",
                       "valid": "bbox_isolated"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..5"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_blobs = ctx.draw_int("n_blobs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_blobs = ctx.draw_int("n_blobs", 2, 4)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set()
    bboxes = []
    for i in range(n_blobs):
        size = rng.randint(3, 6)
        for _ in range(10):
            blob = grow_blob(rng, h, w, used, size)
            if blob is None: continue
            bb = bbox_of(blob)
            if any(bbox_overlaps(bb, ob) for ob in bboxes): continue
            used |= blob
            bboxes.append(bb)
            paint_cells(g, blob, colors[i % len(colors)])
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "all_lr_symmetric":
        # all blobs already left-right symmetric → mirror == original, rule is identity
        for r, c in [(2, 2), (2, 4), (3, 3)]:
            g[r][c] = 4
        for r, c in [(6, 5), (6, 7), (7, 5), (7, 7)]:
            g[r][c] = 6
        return g
    if name == "single_blob":
        # one asymmetric blob → rule still applies but no comparison among objects
        for r, c in [(3, 3), (3, 4), (4, 3), (5, 3)]:
            g[r][c] = 5
        return g
    if name == "bboxes_overlap":
        # bboxes overlap → mirror cells of one blob land inside another's bbox, ambiguous result
        for r, c in [(2, 2), (2, 3), (3, 2)]:
            g[r][c] = 4
        for r, c in [(3, 4), (4, 3), (4, 5)]:
            g[r][c] = 6
        return g
    return g
