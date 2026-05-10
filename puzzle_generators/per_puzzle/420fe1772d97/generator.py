"""Generator for arc_puzzle_bank_21_set19_s:S19_M6.

A top template is stamped at each color-3 marker in the lower panel.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_markers, no_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "420fe1772d97"
VERSION = "1.1.0"
TASK_ID = "420fe1772d97"
SUMMARY = "A top template is stamped at each color-3 marker in the lower panel."

INVARIANTS = [
    "a full color-9 row separates template and marker panels",
    "template occupied cells normalize from their top-left occupied cell",
    "all color-3 markers are anchors inside the 5x5 marker panel",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_markers", "no_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "5", "valid": "5..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "n_markers":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "template_plus_markers",
                       "valid": "template_plus_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def _size(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        shape = _SHAPES[ctx.draw_int("shape", 0, 0)]
        n_markers = ctx.draw_int("n_markers", 2, 2)
    elif difficulty == "hard":
        shape = _SHAPES[ctx.draw_int("shape", 1, 3)]
        n_markers = ctx.draw_int("n_markers", 3, 4)
    else:
        shape = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
        n_markers = ctx.draw_int("n_markers", 2, 4)
    shape_h, shape_w = _size(shape)
    g = full_grid(11, 5, 0)
    for r, c in shape:
        g[r][c] = 2
    for c in range(5):
        g[5][c] = 9
    anchors = [(r, c) for r in range(0, 6 - shape_h) for c in range(0, 6 - shape_w)]
    rng.shuffle(anchors)
    for r, c in anchors[:n_markers]:
        g[6 + r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 5, 0)
    if name == "no_template":
        # markers without template → no shape to stamp
        for c in range(5):
            g[5][c] = 9
        g[7][1] = 3
        g[8][3] = 3
        return g
    if name == "no_markers":
        # template alone, no markers in lower panel → nothing to stamp around
        for r, c in _SHAPES[0]:
            g[r][c] = 2
        for c in range(5):
            g[5][c] = 9
        return g
    if name == "no_divider":
        # template + markers but no 9-divider → no panel separation
        for r, c in _SHAPES[0]:
            g[r][c] = 2
        g[7][1] = 3
        g[8][3] = 3
        return g
    return g
