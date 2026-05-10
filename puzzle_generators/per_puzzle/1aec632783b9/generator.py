"""Generator for 4b:m25 — rotate template by key, center.

Rule: corner key + a non-rectangular blob → rotate by key, center on grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_blob, rectangular_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "1aec632783b9"
VERSION = "1.1.0"
TASK_ID = "1aec632783b9"
SUMMARY = "Single corner key + 1 non-rectangular blob."

INVARIANTS = [
    "background is 0",
    "exactly one corner key cell",
    "exactly one non-rectangular blob away from corner",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_blob", "rectangular_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "corner_key_plus_blob",
                       "valid": "corner_key_plus_blob"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    g[0][w - 1] = palette[0]
    used = {(0, w - 1), (0, w - 2), (1, w - 1)}
    color = palette[1]
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=20)
        if cells is None: continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        if bb == len(cells): continue
        for r, c in cells: g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_key":
        # blob without corner key → no rotation count specified
        for r, c in [(4, 3), (4, 4), (4, 5), (5, 4)]:
            g[r][c] = 5
        return g
    if name == "no_blob":
        # corner key without blob → nothing to rotate
        g[0][w - 1] = 3
        return g
    if name == "rectangular_blob":
        # blob is exact bbox-fill rectangle → rotation under any key looks the same
        g[0][w - 1] = 3
        for r in range(4, 6):
            for c in range(3, 6):
                g[r][c] = 5
        return g
    return g
