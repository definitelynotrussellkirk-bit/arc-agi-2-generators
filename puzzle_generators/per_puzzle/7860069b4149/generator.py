"""Generator for arc_puzzle_bank_tenth21:M64 — sweep blob away from 9-anchor.

Rule: a 9-cell sits adjacent to a colored blob. Extend the blob in the
direction away from the 9 until it hits a wall.

Combinatorial axes (8): grid_h, grid_w, palette_kind, anchor_side,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, anchor_not_adjacent, blob_at_far_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7860069b4149"
VERSION = "1.1.0"
TASK_ID = "7860069b4149"
SUMMARY = "9-anchor + a 2x2 colored blob 4-touching it on one side."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell, exactly one 2x2 (or rect) non-9 blob",
    "9 is 4-adjacent to one cell of the blob (so direction is well-defined)",
    "there's room in the away direction for at least 1 step of sweep",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "anchor_not_adjacent", "blob_at_far_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_side":    {"type": "str", "default": "left", "valid": "left"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "anchor_left_blob_with_room_right",
                       "valid": "anchor_left_blob_with_room_right"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    # Place 2x2 blob with 9 on its left side, so sweep goes right
    r1 = rng.randint(1, h - 3)
    c1 = rng.randint(2, w - 5)
    for r in range(r1, r1 + 2):
        for c in range(c1, c1 + 2):
            g[r][c] = color
    g[r1][c1 - 1] = 9  # anchor on the left
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # blob exists but no 9-anchor → direction undetermined, rule cannot fire
        for r in range(2, 4):
            for c in range(3, 5): g[r][c] = 4
        return g
    if name == "anchor_not_adjacent":
        # 9 exists but not adjacent to blob → no contact direction defined
        g[0][0] = 9   # far away
        for r in range(3, 5):
            for c in range(5, 7): g[r][c] = 4
        return g
    if name == "blob_at_far_wall":
        # blob already touches far wall → no room to sweep
        for r in range(2, 4):
            for c in range(w - 2, w): g[r][c] = 4
        g[2][w - 3] = 9   # anchor on left, but blob can't extend right
        return g
    return g
