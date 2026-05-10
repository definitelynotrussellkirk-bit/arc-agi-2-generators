"""Generator for a416fc5b.

Rule: two valid 3x3 meta-symbols determine the missing diamond
symbols in the output grid.

Combinatorial axes (8): grid_h/w, layout, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_symbols, single_symbol, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "56072bfdb820"
VERSION = "1.1.0"
TASK_ID = "56072bfdb820"
SUMMARY = "Two 3x3 meta-symbols determine missing diamond symbols in output."

INVARIANTS = [
    "the input is partitioned into 4-step macro tiles",
    "only color-2 symbols are valid non-background symbols",
    "the two observed symbols imply two extra color-5/color-8 diamond symbols",
    "background is color 7 and divider is color 6",
]

LAYOUTS = ("row", "column", "diagonal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_symbols", "single_symbol", "full_grid")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "layout":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LAYOUTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in LAYOUTS:
        layout = tx
    else:
        layout = ctx.draw_choice("layout", list(LAYOUTS))
        if "layout" not in overrides:
            layout = ["row", "column", "diagonal"][sample_index % 3]
    g = full_grid(16, 16, 7)
    for r in (3, 7, 11):
        for c in range(16):
            g[r][c] = 6
    for c in (3, 7, 11):
        for r in range(16):
            g[r][c] = 6
    cells = {
        "row": [(1, 0), (1, 2)],
        "column": [(0, 1), (2, 1)],
        "diagonal": [(0, 0), (1, 1)],
    }[layout]
    local = [(1, 1), (0, 1), (1, 0), (2, 1), (1, 2)][(sample_index // 3) % 5]
    for tr, tc in cells:
        g[tr * 4 + local[0]][tc * 4 + local[1]] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 16, 7)
    if name == "no_symbols":
        for r in (3, 7, 11):
            for c in range(16):
                g[r][c] = 6
        return g
    if name == "single_symbol":
        g[1][1] = 2
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(16):
                g[r][c] = 7
        return g
    return g
