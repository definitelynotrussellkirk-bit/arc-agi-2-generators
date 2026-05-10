"""Generator for arc_puzzle_bank_21_set20_bundle:medium_p07 — marker-count scale.

Rule: count of 1s in row 0 = K. Clear those 1s, crop the rest, then
upscale by K (each cell → KxK block).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, blob_already_solid_rect, single_cell_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "486794347a11"
VERSION = "1.1.0"
TASK_ID = "486794347a11"
SUMMARY = "2-3 1-markers in row 0 + a non-1 blob below."

INVARIANTS = [
    "background is 0",
    "row 0 contains 2-3 1-cells (so scale factor is 2 or 3)",
    "exactly one non-1 blob (the content to upscale), placed below row 0",
    "blob is non-rectangular (so upscale produces a more interesting output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "blob_already_solid_rect", "single_cell_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_markers_with_blob_below",
                       "valid": "row0_markers_with_blob_below"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_1 = rng.randint(2, 3)
    for c in rng.sample(range(w), n_1):
        g[0][c] = 1
    used = {(0, c) for c in range(w) if g[0][c] == 1}
    for c in range(w):
        used.add((1, c))
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=20)
        if cells is None:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        if bb == len(cells):
            continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # row 0 blank → K=0, scale factor undefined (or 0)
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4), (4, 5)]: g[r][c] = 4
        return g
    if name == "blob_already_solid_rect":
        # solid rectangle → upscaled output is just a bigger rectangle
        g[0][2] = 1; g[0][4] = 1
        for r in range(3, 5):
            for c in range(3, 5): g[r][c] = 4
        return g
    if name == "single_cell_blob":
        # 1-cell blob → upscale produces a KxK monochrome square (no shape signal)
        g[0][2] = 1; g[0][4] = 1
        g[3][4] = 4
        return g
    return g
