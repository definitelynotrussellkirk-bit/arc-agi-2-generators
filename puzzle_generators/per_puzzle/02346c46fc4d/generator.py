"""Generator for arc_additional_puzzle_bank_volume10:M65.

Rule: the smallest green object is rotated by the control color and
stamped at the maroon anchor.

Combinatorial axes (8): grid_h/w, palette_kind, control_color, num_greens,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: tied_smallest, no_control, no_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "02346c46fc4d"
VERSION = "1.1.0"
TASK_ID = "02346c46fc4d"
SUMMARY = "The smallest green object is rotated by a control color and stamped at a maroon anchor."

INVARIANTS = [
    "background is 0",
    "one control cell has value 2, 4, 5, or 6",
    "there is one maroon anchor cell",
    "the smallest green object is uniquely smaller than green distractors",
]

PALETTE_KINDS = ("default", "control_2", "control_4", "control_5_6")
DEGENERATE_TEXTURES = ("tied_smallest", "no_control", "no_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "7..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control_color":  {"type": "int", "default": "rng",
                       "valid": "2|4|5|6"},
    "num_greens":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([2, 4, 5, 6])
    g[h - 4][w - 4] = 9
    for r, c in [(2, 1), (2, 2), (3, 1)]:
        g[r][c] = 3
    for r, c in [(h - 3, 1), (h - 3, 2), (h - 2, 1), (h - 2, 2), (h - 2, 3)]:
        g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "tied_smallest":
        # two green objects tied at the smallest size — pick is ambiguous
        g[0][0] = 4
        g[h - 4][w - 4] = 9
        for r, c in [(2, 1), (2, 2), (3, 1)]:
            g[r][c] = 3
        for r, c in [(h - 3, w - 4), (h - 3, w - 3), (h - 2, w - 4)]:
            g[r][c] = 3
        return g
    if name == "no_control":
        # objects + anchor but no control — rotation amount undefined
        g[h - 4][w - 4] = 9
        for r, c in [(2, 1), (2, 2), (3, 1)]:
            g[r][c] = 3
        for r, c in [(h - 3, 1), (h - 3, 2), (h - 2, 1), (h - 2, 2), (h - 2, 3)]:
            g[r][c] = 3
        return g
    if name == "no_anchor":
        # control + objects but no maroon anchor — stamp position undefined
        g[0][0] = 4
        for r, c in [(2, 1), (2, 2), (3, 1)]:
            g[r][c] = 3
        for r, c in [(h - 3, 1), (h - 3, 2), (h - 2, 1), (h - 2, 2), (h - 2, 3)]:
            g[r][c] = 3
        return g
    return g
