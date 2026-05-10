"""Generator for arc_puzzle_bank_fifth21:M35 — point-reflect blob about 9-anchor.

Rule: 9-anchor + a single non-9 blob. The blob's reflection through
the anchor is added; original blob stays.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, blob_at_anchor, reflection_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "324e3e599c28"
VERSION = "1.1.0"
TASK_ID = "324e3e599c28"
SUMMARY = "9-anchor + a small blob whose reflection lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell at center area",
    "non-9 blob in upper-left, reflection in lower-right (both in-bounds, disjoint)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "blob_at_anchor", "reflection_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "ul_blob_with_central_9",
                       "valid": "ul_blob_with_central_9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    ar = h // 2; ac = w // 2
    g[ar][ac] = 9
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    cells = []
    for _ in range(40):
        r = rng.randint(0, ar - 1)
        c = rng.randint(0, ac - 1)
        if (r, c) in cells: continue
        mr = 2 * ar - r; mc = 2 * ac - c
        if not (0 <= mr < h and 0 <= mc < w): continue
        cells.append((r, c))
        if len(cells) >= 4: break
    for r, c in cells:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    ar, ac = h // 2, w // 2
    if name == "no_anchor":
        # blob but no 9-anchor → no reflection center
        g[1][1] = 4; g[2][1] = 4; g[2][2] = 4
        return g
    if name == "blob_at_anchor":
        # blob cell at the anchor → cell's reflection coincides with itself
        g[ar][ac] = 9
        g[ar][ac] = 4   # blob overwrites anchor (semantic clash)
        g[1][1] = 4
        return g
    if name == "reflection_oob":
        # anchor near a corner → reflection of cells lands out of bounds for half of them
        g2 = full_grid(h, w, 0)
        g2[1][1] = 9   # anchor near corner
        g2[3][3] = 4   # reflection at (-1, -1), out of bounds
        return g2
    return g
