"""Generator for arc_puzzle_bank_fourth21:E28 — singletons expand into horizontal bars.

Rule: place separated singleton markers that expand into horizontal
bars.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, multi_cell_blobs, markers_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e06cc4c752b2"
VERSION = "1.1.0"
TASK_ID = "e06cc4c752b2"

SUMMARY = "Place separated singleton markers that expand into horizontal bars."

INVARIANTS = [
    "background is 0",
    "every nonzero cell is an isolated singleton",
    "each singleton has empty left and right neighbors",
    "singleton expansion footprints are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "multi_cell_blobs", "markers_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_interior_singletons",
                       "valid": "spaced_interior_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("n_markers", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("n_markers", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("n_markers", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randrange(h)
        c = rng.randint(1, w - 2)
        cells = {(r, c - 1), (r, c), (r, c + 1)}
        guard = {
            (rr, cc)
            for rr in range(max(0, r - 1), min(h, r + 2))
            for cc in range(max(0, c - 2), min(w, c + 3))
        }
        if guard & reserved:
            continue
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        reserved.update(cells | guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blank → no bars to grow
        return g
    if name == "multi_cell_blobs":
        # markers form blobs (not singletons) → "isolated" precondition fails
        g[2][2] = 4; g[2][3] = 4
        g[4][5] = 6; g[5][5] = 6
        return g
    if name == "markers_at_edge":
        # markers at left/right edge → bar arm runs out of bounds
        g[2][0] = 3
        g[4][w - 1] = 7
        return g
    return g
