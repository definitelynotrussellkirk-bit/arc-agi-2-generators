"""Generator for arc_additional_puzzles_21_set19_bundle:E127 — Slide non-9 blob east to 9-dock.

Rule: dock = right column of 9s. Slide the non-{0,9} blob east until
it abuts the dock; output keeps 9s + slid blob.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_choice,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dock, no_blob, blob_already_at_dock.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bcb40bed1599"
VERSION = "1.1.0"
TASK_ID = "bcb40bed1599"
SUMMARY = "Right column of 9s (dock); a small blob on the left to slide east."

INVARIANTS = [
    "right column is fully 9 (dock)",
    "exactly 1 non-{0,9} blob with empty space to its right",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dock", "no_blob", "blob_already_at_dock")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_choice":    {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "left_blob_with_9_dock",
                       "valid": "left_blob_with_9_dock"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    for r in range(h):
        g[r][w - 1] = 9
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    shape = rng.choice([
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (2, 0)],
    ])
    top = rng.randint(0, max(0, h - 4))
    left = rng.randint(0, 1)
    for dr, dc in shape:
        if 0 <= top + dr < h and 0 <= left + dc < w - 1:
            g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 9
    g = full_grid(h, w, 0)
    if name == "no_dock":
        # blob but no right-9 dock → slide target undefined
        for (dr, dc) in [(0, 0), (1, 0), (2, 0)]: g[1 + dr][1 + dc] = 4
        return g
    if name == "no_blob":
        # dock but no blob → nothing to slide
        for r in range(h): g[r][w - 1] = 9
        return g
    if name == "blob_already_at_dock":
        # blob already abuts the dock → no slide motion (input == output)
        for r in range(h): g[r][w - 1] = 9
        for (dr, dc) in [(0, 0), (1, 0), (2, 0)]: g[1 + dr][w - 2 + dc] = 4
        return g
    return g
