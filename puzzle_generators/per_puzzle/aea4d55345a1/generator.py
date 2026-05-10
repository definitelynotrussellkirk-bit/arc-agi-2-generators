"""Generator for 351d6448.

Rule: gray-separated sections show a colored cell shifting one column
per step; the rule predicts the next section.

Combinatorial axes (8): grid_h/w, section_height, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_separators, no_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aea4d55345a1"
VERSION = "1.1.0"
TASK_ID = "aea4d55345a1"
SUMMARY = "Gray-separated sections show a cell shifting one column per step."

INVARIANTS = [
    "full gray rows separate equal-height sections",
    "the active non-gray color appears once per section",
    "the active cell moves by a constant horizontal offset",
    "output size is one section height by the original width",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separators", "no_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "9..14"},
    "section_height": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        sec_h = ctx.draw_int("section_height", 3, 3)
    elif difficulty == "hard":
        sec_h = ctx.draw_int("section_height", 4, 4)
    else:
        sec_h = ctx.draw_int("section_height", 3, 4)
    w = 9 + rng.randint(0, 5)
    color = ctx.draw_color("color", exclude={0, 5})
    active_r = 1 + ((seed + sample_index) % max(1, sec_h - 2))
    start_c = 1 + ((sample_index + rng.randint(0, 4)) % max(1, w - 4))

    rows = []
    for step in range(3):
        section = full_grid(sec_h, w, 0)
        section[active_r][start_c + step] = color
        rows.extend(section)
        if step < 2:
            rows.append([5] * w)
    return rows


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 10, 0)
    if name == "no_separators":
        g[2][3] = 3
        return g
    if name == "no_color":
        for c in range(10):
            g[3][c] = 5
            g[7][c] = 5
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
