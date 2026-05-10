"""Generator for arc_additional_puzzles_21_set17_bundle:M119.

Rule: cell (0, 0) selects one of the body panels; cell (0, 1) is the
transform command applied to that panel.

Combinatorial axes (8): grid_h/w, palette_kind, select_idx, command,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_select, no_command, no_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c868b0210c96"
VERSION = "1.1.0"
TASK_ID = "c868b0210c96"
SUMMARY = "A selected blank-separated panel is cropped and transformed by the command cells."

INVARIANTS = [
    "cell (0,0) selects one of the body panels",
    "cell (0,1) gives the transform command",
    "panels live below row 0 and are separated by blank columns",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_select", "no_command", "no_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "select_idx":     {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "command":        {"type": "int", "default": "rng 1..5", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_starts",
                       "valid": "fixed_starts"},
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
        select_idx = ctx.draw_int("select_idx", 1, 1)
    elif difficulty == "hard":
        select_idx = ctx.draw_int("select_idx", 2, 3)
    else:
        select_idx = ctx.draw_int("select_idx", 1, 3)
    cmd = 1 + (sample_index % 5)
    color = ctx.draw_color("color", exclude={0})
    g = full_grid(7, 14, 0)
    g[0][0] = select_idx
    g[0][1] = cmd
    starts = [0, 5, 10]
    shapes = [
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
    ]
    for start, cells in zip(starts, shapes):
        for dr, dc in cells:
            g[2 + dr][start + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 14, 0)
    starts = [0, 5, 10]
    shapes = [
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
    ]
    if name == "no_select":
        # command but no panel selector — which panel to transform is undefined
        g[0][1] = 2
        for start, cells in zip(starts, shapes):
            for dr, dc in cells:
                g[2 + dr][start + dc] = 7
        return g
    if name == "no_command":
        # selector but no transform — operation undefined
        g[0][0] = 2
        for start, cells in zip(starts, shapes):
            for dr, dc in cells:
                g[2 + dr][start + dc] = 7
        return g
    if name == "no_panels":
        # both controls but nothing to transform
        g[0][0] = 2
        g[0][1] = 3
        return g
    return g
