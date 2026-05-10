"""Generator for arc_puzzle_bank_third_21_bundle:hard_15_make_transform_panel_from_single_template.

A single color-2 template is transformed according to a 2x2 control code grid.
Control colors 1, 3, 4, and 6 map to identity, rotate-cw, rotate-180, and
left-right flip, respectively.

Combinatorial axes (8): grid_h, grid_w, palette_kind, template_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_controls, square_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a215cef8bd1"
VERSION = "1.1.0"
TASK_ID = "5a215cef8bd1"
SUMMARY = "Build a 2x2 transform panel from one color-2 template and control codes."

INVARIANTS = [
    "there is exactly one connected color-2 template object",
    "control cells use colors 1, 3, 4, and 6",
    "control cells occupy exactly two distinct rows and two distinct columns",
    "the output panel contains transformed copies recolored to 7",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_controls", "square_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "template_variant": {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "template_with_2x2_controls",
                       "valid": "template_with_2x2_controls"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


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
    if difficulty == "easy":
        template = _TEMPLATES[ctx.draw_int("template_variant", 0, 0)]
    elif difficulty == "hard":
        template = _TEMPLATES[ctx.draw_int("template_variant", 0, len(_TEMPLATES) - 1)]
    else:
        template = _TEMPLATES[ctx.draw_int("template_variant", 0, len(_TEMPLATES) - 1)]
    controls = [1, 3, 4, 6]
    rng.shuffle(controls)
    g = full_grid(9, 10, 0)
    _paint(g, 1, 1, template, 2)
    positions = [(5, 5), (5, 8), (7, 5), (7, 8)]
    for (r, c), color in zip(positions, controls):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 10, 0)
    if name == "no_template":
        # controls without color-2 template → no shape to transform
        positions = [(5, 5), (5, 8), (7, 5), (7, 8)]
        controls = [1, 3, 4, 6]
        for (r, c), color in zip(positions, controls):
            g[r][c] = color
        return g
    if name == "no_controls":
        # template without controls → no transform dispatch
        _paint(g, 1, 1, _TEMPLATES[0], 2)
        return g
    if name == "square_template":
        # solid 2x2 template → all rotations/flips identical, no contrast
        for r in range(1, 3):
            for c in range(1, 3):
                g[r][c] = 2
        positions = [(5, 5), (5, 8), (7, 5), (7, 8)]
        controls = [1, 3, 4, 6]
        for (r, c), color in zip(positions, controls):
            g[r][c] = color
        return g
    return g
