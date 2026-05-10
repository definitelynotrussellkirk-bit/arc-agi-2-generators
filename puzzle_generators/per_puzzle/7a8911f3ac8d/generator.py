"""Generator for arc_puzzle_bank_twentieth21:M138 — reflect through 9-anchor.

Rule: 9-anchor + a single non-9 blob. Output: original blob + its
reflection through the anchor (point symmetry).

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, multiple_anchors, blob_through_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7a8911f3ac8d"
VERSION = "1.1.0"
TASK_ID = "7a8911f3ac8d"
SUMMARY = "9-anchor at center + a small blob in upper-left whose reflection lands in lower-right."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell at grid center",
    "non-9 blob fully on one side; reflection in-bounds and disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "multiple_anchors", "blob_through_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "centered_anchor_with_offset_blob",
                       "valid": "centered_anchor_with_offset_blob"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    ar = h // 2; ac = w // 2
    g[ar][ac] = 9
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    cells = []
    for _ in range(40):
        r = rng.randint(0, ar - 1)
        c = rng.randint(0, ac - 1)
        if (r, c) in cells:
            continue
        mr = 2 * ar - r; mc = 2 * ac - c
        if not (0 <= mr < h and 0 <= mc < w):
            continue
        cells.append((r, c))
        if len(cells) >= 3:
            break
    for r, c in cells:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    ar, ac = h // 2, w // 2
    if name == "no_anchor":
        # no 9-cell → rule has no point of symmetry to use
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        return g
    if name == "multiple_anchors":
        # two 9-cells → which one is the symmetry center?
        g[2][2] = 9
        g[5][5] = 9
        g[1][1] = 4; g[1][2] = 4
        return g
    if name == "blob_through_anchor":
        # blob cell coincides with anchor → reflection self-overlaps
        g[ar][ac] = 9
        # cell whose reflection is itself (the anchor)
        g[ar - 1][ac] = 4  # reflection at (ar+1, ac)
        g[ar][ac - 1] = 4  # reflection at (ar, ac+1)
        return g
    return g
