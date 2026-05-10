"""Generator for arc_puzzle_bank_eighteenth21:E120.

Rule: each row header (column 0) recolors that row's single 1-marker
to the header's color; the header itself is cleared.

Combinatorial axes (8): grid_h/w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, marker_position, texture.
Degenerates: no_headers, no_markers, header_only_no_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "68b4181d35e1"
VERSION = "1.1.0"
TASK_ID = "68b4181d35e1"
SUMMARY = "Each row header color replaces that row's single marker 1."

INVARIANTS = [
    "background is 0",
    "active rows have one header in column 0",
    "active rows have exactly one marker cell with value 1",
    "header cells are cleared after painting their marker",
]

PALETTE_KINDS = ("default", "warm_headers", "cool_headers", "rainbow")
DEGENERATE_TEXTURES = ("no_headers", "no_markers", "header_only_no_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "uniform", "valid": "uniform"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5",
                          "valid": "1..8"},
    "marker_position": {"type": "str", "default": "rng",
                        "valid": "interior|right_edge"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        target_max = 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        target_max = 5
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 9)
        target_max = 5
    active = min(ctx.draw_int("active_rows", 3, target_max), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 5, 6, 7, 8, 9]
    for r, color in zip(rng.sample(range(h), active), rng.sample(colors, active)):
        g[r][0] = color
        g[r][rng.randint(2, w - 1)] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_headers":
        # 1-markers without row headers — no source color to recolor with
        g[1][3] = 1
        g[3][5] = 1
        return g
    if name == "no_markers":
        # headers without 1-markers — rule has nothing to recolor
        g[1][0] = 4
        g[3][0] = 7
        g[5][0] = 2
        return g
    if name == "header_only_no_marker":
        # one row has header but no 1-marker — that row is silently un-recolored
        g[1][0] = 4
        g[1][3] = 1
        g[3][0] = 7
        return g
    return g
