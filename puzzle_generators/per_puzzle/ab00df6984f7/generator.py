"""Generator for arc_puzzle_bank_twentieth_21_bundle:easy_140_crop_tight_nonzero_bbox.

Rule: crop to the tight nonzero bounding box.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ph, pw,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_object, multiple_objects, object_at_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ab00df6984f7"
VERSION = "1.1.0"
TASK_ID = "ab00df6984f7"

SUMMARY = "The tight bounding box around all nonzero cells is emitted as the output."

INVARIANTS = [
    "background is 0",
    "all nonzero cells lie inside one offset bounding box",
    "colors are preserved exactly by the crop",
    "the source object may contain holes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_object", "multiple_objects", "object_at_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ph":             {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "pw":             {"type": "int", "default": "rng 4..7", "valid": "2..10"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "centered_framed_object",
                       "valid": "centered_framed_object"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
    "density":        {"type": "str", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
    rng = ctx.draw_rng("layout")
    ph = rng.randint(3, min(5, h - 2))
    pw = rng.randint(4, min(7, w - 2))
    r0 = rng.randint(1, h - ph)
    c0 = rng.randint(1, w - pw)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    g = full_grid(h, w, 0)
    for c in range(pw):
        g[r0][c0 + c] = colors[0]
        g[r0 + ph - 1][c0 + c] = colors[1]
    for r in range(ph):
        g[r0 + r][c0] = colors[0]
        g[r0 + r][c0 + pw - 1] = colors[1]
    for r in range(1, ph - 1):
        g[r0 + r][c0 + 1 + ((r + sample_index) % (pw - 2))] = colors[2]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_object":
        # blank → no nonzero bbox, rule undefined
        return g
    if name == "multiple_objects":
        # two separated objects → bbox spans both
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[7][9] = 6; g[8][9] = 6; g[8][10] = 6
        return g
    if name == "object_at_border":
        # object touches grid edges → bbox = full grid, crop is identity
        for c in range(w): g[0][c] = 4
        for c in range(w): g[h - 1][c] = 4
        for r in range(h): g[r][0] = 4
        for r in range(h): g[r][w - 1] = 4
        return g
    return g
