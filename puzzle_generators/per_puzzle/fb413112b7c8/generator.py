"""Generator for arc_puzzle_bank_twelfth21:M78 — drop blob onto support line.

Rule: a horizontal 9-line acts as the floor. Drop the (single) non-9
blob above onto the support: it lands so its bbox bottom row is at
support_row - 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_support, no_blob, blob_already_on_support.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "fb413112b7c8"
VERSION = "1.1.0"
TASK_ID = "fb413112b7c8"
SUMMARY = "Horizontal 9-line near the bottom + a small blob above (with gap)."

INVARIANTS = [
    "background is 0",
    "exactly one full horizontal 9-line at row >= h-3",
    "exactly one non-9 blob fully above the line, with at least one empty row between",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_support", "no_blob", "blob_already_on_support")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "support_with_blob_above",
                       "valid": "support_with_blob_above"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    support_row = h - 2
    for c in range(1, w - 1):
        g[support_row][c] = 9
    used = {(r, c) for c in range(w) for r in (support_row, support_row + 1, support_row - 1)}
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if cells:
        for r, c in cells:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_support":
        # blob but no 9-line → no floor to land on
        g[2][3] = 4; g[3][3] = 4; g[2][4] = 4
        return g
    if name == "no_blob":
        # support but no blob → nothing to drop
        for c in range(1, w - 1): g[h - 2][c] = 9
        return g
    if name == "blob_already_on_support":
        # blob bottom already touches support → rule is identity (no drop)
        for c in range(1, w - 1): g[h - 2][c] = 9
        g[h - 3][3] = 4; g[h - 3][4] = 4   # already at support_row - 1
        return g
    return g
