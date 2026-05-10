"""Generator for arc_puzzle_bank_third_21_bundle:hard_20_boolean_combine_two_templates_by_key.

Two binary templates in colors 1 and 2 are combined by a singleton control
color: 3 for union, 4 for intersection, and 6 for xor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, op_key,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_template_a, no_template_b.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0f6ba01fa18c"
VERSION = "1.1.0"
TASK_ID = "0f6ba01fa18c"
SUMMARY = "Combine color-1 and color-2 templates by the singleton key color."

INVARIANTS = [
    "there is one connected color-1 template object",
    "there is one connected color-2 template object",
    "exactly one of colors 3, 4, or 6 appears as a singleton control",
    "the selected boolean operation has a nonempty support",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_template_a", "no_template_b")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "op_key":         {"type": "int", "default": "rng 3|4|6", "valid": "3|4|6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_templates_with_key",
                       "valid": "two_templates_with_key"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_A = [(0, 0), (1, 0), (1, 1), (2, 1)]
_B = [(0, 1), (1, 0), (1, 1), (2, 0)]


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
        key = ctx.draw_choice("op_key", [3])
    elif difficulty == "hard":
        key = ctx.draw_choice("op_key", [4, 6])
    else:
        key = ctx.draw_choice("op_key", [3, 4, 6])
    row_shift = rng.randint(0, 1)
    g = full_grid(8, 10, 0)
    _paint(g, 1 + row_shift, 1, _A, 1)
    _paint(g, 1 + row_shift, 5, _B, 2)
    g[6][rng.randint(2, 7)] = key
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_key":
        # both templates exist but no 3/4/6 control → no operation defined
        _paint(g, 1, 1, _A, 1)
        _paint(g, 1, 5, _B, 2)
        return g
    if name == "no_template_a":
        # color-2 template + key but no color-1 template → operation has no LHS
        _paint(g, 1, 5, _B, 2)
        g[6][3] = 4
        return g
    if name == "no_template_b":
        # color-1 template + key but no color-2 template → operation has no RHS
        _paint(g, 1, 1, _A, 1)
        g[6][6] = 4
        return g
    return g
