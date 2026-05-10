"""Generator for 14b:m93 — rotate object by top-row code.

Rule: row 0 has K non-zero cells (code = K mod 4). Below row 0, find
the (single) blob, crop it, rotate by code.

Combinatorial axes (8): grid_h, grid_w, palette_kind, k_code,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_code, no_blob, square_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "cf0dd146ab42"
VERSION = "1.1.0"
TASK_ID = "cf0dd146ab42"
SUMMARY = "Row 0 has K markers (K=1..3) + a non-rectangular blob below."

INVARIANTS = [
    "background is 0",
    "row 0 has 1-3 non-zero cells (rotation code)",
    "exactly one non-rectangular blob below row 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_code", "no_blob", "square_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "k_code":         {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_code_blob_below",
                       "valid": "row0_code_blob_below"},
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
    K = rng.randint(1, 3)
    code_color = 2
    for c in rng.sample(range(w), K):
        g[0][c] = code_color
    used = {(0, c) for c in range(w) if g[0][c] != 0}
    for c in range(w):
        used.add((1, c))
    color = rng.choice([3, 4, 5, 6, 7, 8])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 5), max_attempts=20)
        if cells is None:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        if bb == len(cells):
            continue
        for r, c in cells: g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_code":
        # blob without top-row markers → no rotation code
        for r, c in [(3, 3), (4, 3), (4, 4), (5, 4)]: g[r][c] = 4
        return g
    if name == "no_blob":
        # code without blob → nothing to rotate
        g[0][2] = 2; g[0][5] = 2
        return g
    if name == "square_blob":
        # solid 2x2 blob → all rotations identical
        g[0][2] = 2
        for r in range(3, 5):
            for c in range(3, 5):
                g[r][c] = 4
        return g
    return g
