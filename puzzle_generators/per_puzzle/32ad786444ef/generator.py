"""Generator for arc_puzzle_bank_twelfth21:M83 — point-reflect by 9-anchor.

Rule: 9 = anchor. Each non-{0,9} cell is duplicated at its reflection
through the anchor. Both original and reflected cells appear in output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, multiple_anchors, blob_at_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "32ad786444ef"
VERSION = "1.1.0"
TASK_ID = "32ad786444ef"
SUMMARY = "9-anchor at center + a small blob in upper-left whose reflection lands in lower-right."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell at grid center",
    "non-9 blob is fully on one side; its reflection is in-bounds and disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "multiple_anchors", "blob_at_anchor")
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
        if (r, c) in cells: continue
        cells.append((r, c))
        if len(cells) >= 3: break
    for r, c in cells:
        mr = 2 * ar - r; mc = 2 * ac - c
        if 0 <= mr < h and 0 <= mc < w:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # no 9-cell → rule has no center to reflect through
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        return g
    if name == "multiple_anchors":
        # two 9-cells → ambiguous which one is the reflection center
        g[2][2] = 9
        g[5][5] = 9
        g[1][1] = 4; g[1][2] = 4
        return g
    if name == "blob_at_anchor":
        # blob cell coincides with anchor → reflection of (ar,ac) = (ar,ac), overlaps with 9
        ar, ac = h // 2, w // 2
        g[ar][ac] = 9
        # blob cell at anchor itself is impossible (already 9), but a cell whose reflection lands at anchor
        # plus crossed-on-anchor blob
        g[ar - 1][ac] = 4; g[ar + 1][ac] = 4  # reflections land on each other
        return g
    return g
