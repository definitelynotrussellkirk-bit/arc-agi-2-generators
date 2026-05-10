"""Generator for bbc9ae5d.

Rule: input is single row, even width w, with init non-zero cells in
color C. Output is (w/2)×w grid where row r has cells with c<init+r
filled with C.

Combinatorial axes (8): grid_w, color, init_count, fill_layout,
left_anchor, decoy_palette_size, decoy_density, asymmetry.
Degenerates: empty_row, full_row, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c0aac14eef4d"
VERSION = "1.1.0"
TASK_ID = "c0aac14eef4d"
SUMMARY = "Single row, even width, with init colored cells; rule builds triangular fill."

INVARIANTS = [
    "1×w grid with w even and >=4",
    "exactly one non-zero color C used",
    "init non-zero cells with init in [2, w-2] (so output has both filled and bg)",
    "no zero color in the row mixes with the rule's color C",
]

FILL_LAYOUTS = ("contiguous_left", "contiguous_right", "scattered",
                "alternating", "edges")
DEGENERATE_TEXTURES = ("empty_row", "full_row", "single_cell")
HELPFUL_TEXTURES = FILL_LAYOUTS

AXES = {
    "grid_w":             {"type": "int", "default": "rng 6..16 even", "valid": "4..22"},
    "color":              {"type": "color", "default": "rng (≠0)",
                           "valid": "1..9"},
    "init_count":         {"type": "int", "default": "rng 2..w-2",
                           "valid": "2..w-2"},
    "fill_layout":        {"type": "str", "default": "rng helpful",
                           "valid": "|".join(FILL_LAYOUTS)},
    "left_anchor":        {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "right_anchor":       {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "decoy_palette_size": {"type": "int", "default": "0", "valid": "0..0"},
    "texture":            {"type": "str", "default": "alias for fill_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        w_lo, w_hi = 4, 8
    elif difficulty == "hard":
        w_lo, w_hi = 14, 22
    else:
        w_lo, w_hi = 6, 16
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    if w % 2 == 1:
        w -= 1
    w = max(4, w)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], w, rng)
    color = int(overrides.get("color",
                              ctx.draw_color("color", exclude={0})))
    init = int(overrides.get("init_count",
                             ctx.draw_int("init_count", 2, w - 2)))
    init = max(2, min(w - 2, init))
    layout = (overrides.get("texture") or overrides.get("fill_layout")
              or ctx.draw_choice("fill_layout", list(FILL_LAYOUTS)))
    g = full_grid(1, w, 0)
    cols = _layout_cols(layout, w, init, rng)
    for c in cols[:init]:
        g[0][c] = color
    return g


def _layout_cols(layout, w, init, rng):
    if layout == "contiguous_left":
        return list(range(init))
    if layout == "contiguous_right":
        return list(range(w - init, w))
    if layout == "alternating":
        cols = [c for c in range(w) if c % 2 == 0]
        if len(cols) >= init:
            return cols[:init]
        return list(range(init))
    if layout == "edges":
        left = init // 2
        right = init - left
        return list(range(left)) + list(range(w - right, w))
    cols = list(range(w))
    rng.shuffle(cols)
    return cols[:init]


def _draw_from_degenerate(name, w, rng):
    g = full_grid(1, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "empty_row":
        return g
    if name == "full_row":
        for c in range(w):
            g[0][c] = color
        return g
    if name == "single_cell":
        g[0][rng.randint(0, w - 1)] = color
        return g
    return g
