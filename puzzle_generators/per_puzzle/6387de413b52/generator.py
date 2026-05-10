"""Generator for arc_puzzle_bank_tenth21:M68 — bbox row × col cross-product.

Rule: collect all blob bbox rows (every r covered by some bbox) and
bbox cols. Output paints 8 at every (r, c) where r is a bbox-row AND c
is a bbox-col.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, overlapping_bboxes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "6387de413b52"
VERSION = "1.1.0"
TASK_ID = "6387de413b52"
SUMMARY = "2-3 distinct-color blobs at non-overlapping bbox rows AND cols."

INVARIANTS = [
    "background is 0",
    "blobs at strictly disjoint bbox row ranges",
    "blobs at strictly disjoint bbox col ranges",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "overlapping_bboxes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "disjoint_bboxes",
                       "valid": "disjoint_bboxes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n)
    used: set[tuple[int, int]] = set()
    placed_rows: set[int] = set()
    placed_cols: set[int] = set()
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=20)
            if cells is None:
                continue
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            if any(r in placed_rows for r in range(min(rs), max(rs) + 1)):
                continue
            if any(c in placed_cols for c in range(min(cs), max(cs) + 1)):
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            for r in range(min(rs), max(rs) + 1):
                placed_rows.add(r)
            for c in range(min(cs), max(cs) + 1):
                placed_cols.add(c)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no bboxes to compute the cross-product
        # over; output is empty.
        return g
    if name == "single_blob":
        # Only one blob — rule's cross-product is just the blob's bbox
        # interior; lacks the multi-blob signal the rule typifies.
        for r, c in [(2, 3), (2, 4), (3, 3)]: g[r][c] = 4
        return g
    if name == "overlapping_bboxes":
        # Two blobs whose bboxes share rows/cols — rule's cross-product
        # fires intersections; bbox-row sets overlap, defeating the
        # "disjoint bbox" invariant.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        for r, c in [(2, 6), (3, 6), (3, 7)]: g[r][c] = 6
        return g
    return g
