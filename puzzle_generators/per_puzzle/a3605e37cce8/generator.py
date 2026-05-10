"""Generator for 6b:m40 — drop whole blobs to bottom.

Rule: each blob slides down as a unit until its bbox bottom row hits
the grid bottom.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, blobs_at_bottom, overlapping_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "a3605e37cce8"
VERSION = "1.1.0"
TASK_ID = "a3605e37cce8"
SUMMARY = "2-3 distinct-color blobs in upper rows (gravity-down by whole blob)."

INVARIANTS = [
    "background is 0",
    "blobs all in upper half, bottom row is empty",
    "blobs occupy disjoint col ranges (so dropping doesn't collide)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "blobs_at_bottom", "overlapping_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_half_disjoint_columns",
                       "valid": "upper_half_disjoint_columns"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_blobs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_blobs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    for r in range(max(0, h - 3), h):
        for c in range(w):
            used.add((r, c))
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    cols_used: list[range] = []
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
            if cells is None: continue
            cs = [c for _, c in cells]; cmin, cmax = min(cs), max(cs)
            if any(set(range(cmin, cmax + 1)) & set(cu) for cu in cols_used):
                continue
            for r, c in cells: g[r][c] = color
            used |= cells
            cols_used.append(range(cmin, cmax + 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → nothing to drop, identity
        return g
    if name == "blobs_at_bottom":
        # blobs already at bottom → drop is identity
        g[h - 2][2] = 4; g[h - 1][2] = 4
        g[h - 1][7] = 6; g[h - 2][7] = 6
        return g
    if name == "overlapping_columns":
        # two blobs share the same column → drop would collide / stack ambiguously
        g[1][3] = 4; g[1][4] = 4
        g[2][3] = 6; g[2][4] = 6
        return g
    return g
