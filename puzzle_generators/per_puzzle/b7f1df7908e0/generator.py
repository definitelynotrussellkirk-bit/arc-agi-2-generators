"""Generator for arc_puzzle_bank_sixth21:H36.

Rule: a full color-9 row and full color-9 column define quadrants; the
lower-left quadrant contains a hollow object whose enclosed hole is
filled.

Combinatorial axes (8): grid_h/w, palette_kind, frame_color,
palette_size, position_bias, n_distinct_colors, hole_size, texture.
Degenerates: no_dividers, solid_object, no_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "b7f1df7908e0"
VERSION = "1.1.0"
TASK_ID = "b7f1df7908e0"
SUMMARY = "Fill the enclosed hole of the object in the lower-left quadrant."

INVARIANTS = [
    "a full color-9 row and full color-9 column define the active quadrant",
    "the active lower-left quadrant contains one hollow object",
    "the object's enclosed zero region is strictly internal",
    "other quadrants are inert for this rule",
]

PALETTE_KINDS = ("default", "warm_frame", "cool_frame", "varied_frame")
DEGENERATE_TEXTURES = ("no_dividers", "solid_object", "no_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_color":    {"type": "color", "default": "rng", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "lower_left",
                       "valid": "lower_left"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "hole_size":      {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    color = ctx.draw_color("frame_color", exclude={0, 9})
    g = full_grid(10, 12, 0)
    for c in range(12):
        g[3][c] = 9
    for r in range(10):
        g[r][6] = 9
    if difficulty == "easy":
        top = 5
    elif difficulty == "hard":
        top = 6
    else:
        top = 5 + rng.randint(0, 1)
    draw_frame(g, top, 1, top + 3, 4, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_dividers":
        # hollow frame but no 9-row/9-col → no quadrant defined
        draw_frame(g, 5, 1, 8, 4, 4)
        return g
    if name == "solid_object":
        # 9-dividers + a SOLID block (no hole) → nothing to fill
        for c in range(12):
            g[3][c] = 9
        for r in range(10):
            g[r][6] = 9
        for r in range(5, 9):
            for c in range(1, 5):
                g[r][c] = 4
        return g
    if name == "no_object":
        # 9-dividers but lower-left quadrant is empty → no object
        for c in range(12):
            g[3][c] = 9
        for r in range(10):
            g[r][6] = 9
        return g
    return g
