"""Generator for arc_puzzle_bank_twelfth21:M79 — reflect across vertical 9-axis.

Rule: a full vertical 9-line at some column acts as the mirror axis.
Each non-9 cell is reflected across the axis (keeping original).

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, both_sides_filled, no_left_content.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "caffd29045bc"
VERSION = "1.1.0"
TASK_ID = "caffd29045bc"
SUMMARY = "Full vertical 9-axis + a blob on one side whose reflection lands in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one full vertical 9-line at some col c",
    "non-9 content is on one side; reflected positions stay in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "both_sides_filled", "no_left_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "vertical_9_axis_plus_left_blob",
                       "valid": "vertical_9_axis_plus_left_blob"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    axis_c = w // 2
    for r in range(h):
        g[r][axis_c] = 9
    used = {(r, axis_c) for r in range(h)}
    for r in range(h):
        for c in range(axis_c, w):
            used.add((r, c))
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
        if cells is None:
            continue
        if not all(0 <= 2 * axis_c - c < w for _, c in cells):
            continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # blob without 9-axis → no mirror axis to reflect across
        g[2][2] = 4; g[3][2] = 4; g[3][3] = 4
        return g
    if name == "both_sides_filled":
        # content on both sides → "one side only" precondition fails
        for r in range(h):
            g[r][5] = 9
        g[2][2] = 4
        g[3][8] = 4  # also right side
        return g
    if name == "no_left_content":
        # axis alone with no content → nothing to reflect
        for r in range(h):
            g[r][5] = 9
        return g
    return g
