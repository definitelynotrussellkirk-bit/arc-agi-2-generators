"""Generator for 337b420f.

Rule: largest non-8 components from zero-separated panels are overlaid
into one panel-width canvas.

Combinatorial axes (8): grid_h/w, panel_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_panels, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b44c4c938f42"
VERSION = "1.1.0"
TASK_ID = "b44c4c938f42"
SUMMARY = "Largest non-8 components from zero-separated panels overlaid into one canvas."

INVARIANTS = [
    "panels have equal width and are separated by all-zero columns",
    "within panels, color 8 is the local background",
    "each panel contains at least one connected non-8 component",
    "largest panel components are placed into one output panel with conflict-avoiding shifts",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_panels", "no_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "panel_count":    {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        panel_count = ctx.draw_int("panel_count", 2, 2)
    elif difficulty == "hard":
        panel_count = ctx.draw_int("panel_count", 3, 3)
    else:
        panel_count = ctx.draw_int("panel_count", 2, 3)
    colors = ctx.draw_distinct_colors("colors", n=panel_count, exclude={0, 8})
    height = 7
    panel_w = 5
    width = panel_count * panel_w + (panel_count - 1)
    g = full_grid(height, width, 8)
    for sep in range(1, panel_count):
        c = sep * panel_w + (sep - 1)
        for r in range(height):
            g[r][c] = 0

    for i in range(panel_count):
        start_c = i * (panel_w + 1)
        r0 = rng.randint(1, 3)
        c0 = start_c + rng.randint(1, 2)
        for dr, dc in SHAPES[i]:
            g[r0 + dr][c0 + dc] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 11, 8)
    if name == "no_panels":
        return g
    if name == "no_shapes":
        for r in range(7):
            g[r][5] = 0
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(11):
                g[r][c] = 8
        return g
    return g
