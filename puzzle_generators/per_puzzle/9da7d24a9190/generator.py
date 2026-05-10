"""Generator for arc_additional_puzzles_21_set17_bundle:E113.

Rule: legend colors remap the sorted symbols inside a 3x3 template
(rows 2-4, cols 1-3); row 0 holds the legend in output order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pattern,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_legend, single_symbol, empty_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9da7d24a9190"
VERSION = "1.1.0"
TASK_ID = "9da7d24a9190"
SUMMARY = "Legend colors remap the sorted symbols inside a 3x3 template."

INVARIANTS = [
    "row 0 contains the nonzero legend colors in output order",
    "the 3x3 template is read from rows 2-4 and columns 1-3",
    "nonzero template symbols are sorted and replaced by the corresponding legend entries",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_legend", "single_symbol", "empty_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "5", "valid": "5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pattern":        {"type": "str", "default": "rng diag|cross",
                       "valid": "diag|cross"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "template_3x3", "valid": "template_3x3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    pattern = ctx.draw_choice("pattern", ["diag", "cross"])
    if "pattern" not in overrides:
        pattern = "diag" if sample_index % 2 == 0 else "cross"
    a, b = ctx.draw_distinct_colors("legend", n=2, exclude={0, 2, 4})
    g = full_grid(5, 5, 0)
    g[0][0] = a
    g[0][1] = b
    if pattern == "diag":
        cells = [(0, 0, 2), (1, 1, 4), (2, 2, 2)]
    else:
        cells = [(0, 1, 2), (1, 0, 4), (1, 1, 2), (1, 2, 4), (2, 1, 2)]
    for dr, dc, color in cells:
        g[2 + dr][1 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 5, 0)
    if name == "missing_legend":
        # row 0 has no legend → no mapping for the template symbols
        for dr, dc, color in [(0, 0, 2), (1, 1, 4), (2, 2, 2)]:
            g[2 + dr][1 + dc] = color
        return g
    if name == "single_symbol":
        # template uses only 1 distinct symbol → second legend slot is unused
        g[0][0] = 3; g[0][1] = 6
        for dr, dc in [(0, 0), (1, 1), (2, 2)]:
            g[2 + dr][1 + dc] = 2
        return g
    if name == "empty_template":
        # template is empty → no symbols to remap, legend is purely decorative
        g[0][0] = 3; g[0][1] = 6
        return g
    return g
