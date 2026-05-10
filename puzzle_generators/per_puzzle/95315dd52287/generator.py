"""Generator for arc_puzzle_bank_fourteenth21:M92.

Rule: a multi-color blob (cells in 2 colors) + an 8-anchor. Output
is empty grid + blob moved so its top-left aligns with the anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_blob, anchor_no_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "95315dd52287"
VERSION = "1.1.0"
TASK_ID = "95315dd52287"
SUMMARY = "2-color blob in upper-left + 8-anchor in lower-right with room for the move."

INVARIANTS = [
    "background is 0",
    "exactly one 8-cell + one multi-color blob",
    "anchor's position has room for the blob's bbox",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_blob", "anchor_no_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "1", "valid": "1"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "blob_tl_anchor_br",
                       "valid": "blob_tl_anchor_br"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7], 2)
    g[0][0] = palette[0]
    g[0][1] = palette[1]
    g[1][1] = palette[0]
    ar = rng.randint(h - 3, h - 2)
    ac = rng.randint(w - 4, w - 3)
    g[ar][ac] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # blob present but no 8-anchor → no destination for the move
        g[0][0] = 2; g[0][1] = 3; g[1][1] = 2
        return g
    if name == "no_blob":
        # anchor present but no blob to move → rule has nothing to translate
        g[h - 2][w - 3] = 8
        return g
    if name == "anchor_no_room":
        # anchor at the bottom-right corner → blob bbox at that anchor goes out of bounds
        g[0][0] = 2; g[0][1] = 3; g[1][1] = 2
        g[h - 1][w - 1] = 8
        return g
    return g
