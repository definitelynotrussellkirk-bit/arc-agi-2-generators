"""Generator for arc_puzzle_bank_thirteenth21:M91 — bbox-outline every blob.

Rule: replace each blob with its bbox-outline (in same color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_solid_rects, single_cell_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "cc8c719680e6"
VERSION = "1.1.0"
TASK_ID = "cc8c719680e6"
SUMMARY = "2-3 distinct-color blobs, non-rectangular, with non-overlapping bboxes."

INVARIANTS = [
    "background is 0",
    "blobs are non-rectangular (so bbox-outline differs from blob)",
    "blobs have distinct colors and non-overlapping bboxes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_solid_rects", "single_cell_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "non_rectangular_blobs",
                       "valid": "non_rectangular_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        n = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_blobs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        n = ctx.draw_int("n_blobs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=20)
            if cells is None:
                continue
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            bb_h = max(rs) - min(rs) + 1
            bb_w = max(cs) - min(cs) + 1
            if bb_h * bb_w == len(cells):
                continue
            bbox_cells = {(r, c) for r in range(min(rs), max(rs) + 1) for c in range(min(cs), max(cs) + 1)}
            if bbox_cells & used:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= bbox_cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blobs to outline
        return g
    if name == "all_solid_rects":
        # solid rects → bbox-outline = bbox border, but the blob fills the bbox already
        for r in range(2, 4):
            for c in range(2, 5): g[r][c] = 4
        for r in range(5, 7):
            for c in range(6, 9): g[r][c] = 6
        return g
    if name == "single_cell_blobs":
        # 1-cell blobs → bbox-outline is the cell itself, identity
        g[2][2] = 4; g[5][7] = 6
        return g
    return g
