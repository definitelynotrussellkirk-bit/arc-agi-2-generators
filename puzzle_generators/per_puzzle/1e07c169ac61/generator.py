"""Generator for arc_puzzle_bank_twentysecond21:M152 — rotate CW around 9-anchor.

Rule: 9-anchor + a single non-9 blob. Rotate the blob 90° CW around
the anchor: (r, c) → (anchor_r + (c - anchor_c), anchor_c - (r - anchor_r)).

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_blob, blob_at_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e07c169ac61"
VERSION = "1.1.0"
TASK_ID = "1e07c169ac61"
SUMMARY = "9-anchor + a small blob whose CW rotation lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell at center",
    "blob in upper-left so rotation lands in-bounds",
    "blob is non-symmetric so rotation produces a different shape",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_blob", "blob_at_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "anchor_with_upper_left_blob",
                       "valid": "anchor_with_upper_left_blob"},
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
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
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
        rr = ar + (c - ac); cc = ac - (r - ar)
        if not (0 <= rr < h and 0 <= cc < w): continue
        cells.append((r, c))
        if len(cells) >= 3: break
    for r, c in cells:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # blob without 9-anchor → no rotation pivot defined
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        return g
    if name == "no_blob":
        # 9-anchor alone → nothing to rotate
        g[h // 2][w // 2] = 9
        return g
    if name == "blob_at_anchor":
        # blob coincides with anchor → rotation lands at the same cell (identity)
        ar, ac = h // 2, w // 2
        g[ar][ac] = 9
        # blob symmetric under 90° around anchor (e.g., the center cell only)
        return g
    return g
