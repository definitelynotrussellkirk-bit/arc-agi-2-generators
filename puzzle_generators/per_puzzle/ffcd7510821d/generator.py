"""Generator for arc_puzzle_bank_21_set19_bundle:medium_p05 — marker-count rotation.

Rule: count of 9s in row 0 = N (mod 4). Clear those 9s, crop the
remaining content, then rotate the result by N quarter-turns CW.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, four_markers, blob_already_solid_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ffcd7510821d"
VERSION = "1.1.0"
TASK_ID = "ffcd7510821d"
SUMMARY = "Row 0 has 1-3 9-markers + a single non-9 blob below."

INVARIANTS = [
    "background is 0",
    "row 0 contains 1-3 9-markers (so rotation count is 1-3 mod 4)",
    "exactly one non-9 blob (the content to rotate), placed at row >= 2",
    "the blob is non-rectangular (so rotation produces a different output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "four_markers", "blob_already_solid_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_markers_with_below_blob",
                       "valid": "row0_markers_with_below_blob"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_9 = rng.randint(1, 3)
    for c in rng.sample(range(w), n_9):
        g[0][c] = 9
    used = {(0, c) for c in range(w) if g[0][c] == 9}
    for c in range(w):
        used.add((1, c))
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(4, 6), max_attempts=20)
        if cells is None:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb_h = max(rs) - min(rs) + 1
        bb_w = max(cs) - min(cs) + 1
        if bb_h * bb_w == len(cells):
            continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # zero 9s in row 0 → N=0 (mod 4), rotation is identity
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4), (4, 5)]: g[r][c] = 4
        return g
    if name == "four_markers":
        # four 9s → N=0 (mod 4), rotation is identity (rule has no visible effect)
        g[0][1] = 9; g[0][3] = 9; g[0][5] = 9; g[0][7] = 9
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4), (4, 5)]: g[r][c] = 6
        return g
    if name == "blob_already_solid_rect":
        # solid rectangle → rotated 90° from a square or 1xN looks identical (or transposed)
        g[0][2] = 9; g[0][4] = 9
        for r in range(3, 6):
            for c in range(3, 6): g[r][c] = 4  # 3x3 solid square — 90° rotation is identical
        return g
    return g
