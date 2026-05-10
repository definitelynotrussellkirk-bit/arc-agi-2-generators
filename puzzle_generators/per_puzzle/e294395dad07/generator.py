"""Generator for arc_puzzle_bank_fourteenth_21_bundle:easy_98_stamp_pluses_at_markers.

Rule: each nonzero input cell expands into a same-color plus stamp.

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, markers_at_edge, dense_overlapping.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e294395dad07"
VERSION = "1.1.0"
TASK_ID = "e294395dad07"
SUMMARY = "Place separated interior markers that expand into same-color plus stamps."

INVARIANTS = [
    "background is 0",
    "each nonzero input cell is a marker",
    "markers are away from the grid border",
    "plus footprints do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "markers_at_edge", "dense_overlapping")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "interior_separated_markers",
                       "valid": "interior_separated_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _plus_cells(r: int, c: int) -> set[tuple[int, int]]:
    return {(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("markers", 2, 2), 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        target = min(ctx.draw_int("markers", 3, 4), 9)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        target = min(ctx.draw_int("markers", 2, 4), 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        cells = _plus_cells(r, c)
        guard = {
            (rr, cc)
            for pr, pc in cells
            for rr in range(max(0, pr - 1), min(h, pr + 2))
            for cc in range(max(0, pc - 1), min(w, pc + 2))
        }
        if guard & reserved:
            continue
        g[r][c] = colors[placed]
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blank → no markers, rule has nothing to stamp
        return g
    if name == "markers_at_edge":
        # markers on border → plus arms extend off-grid (clipped)
        g[0][3] = 4   # top edge — top arm clips
        g[4][0] = 6   # left edge — left arm clips
        g[h - 1][7] = 3  # bottom edge — bottom arm clips
        return g
    if name == "dense_overlapping":
        # markers placed adjacent → plus stamps overlap, output ambiguous
        g[3][3] = 4
        g[3][4] = 6   # plus-arms collide on (3,4)/(3,3)
        g[5][7] = 3
        g[5][8] = 7   # plus-arms collide on (5,7)/(5,8)
        return g
    return g
