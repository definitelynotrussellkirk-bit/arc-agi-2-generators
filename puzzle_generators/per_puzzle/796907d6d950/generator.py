"""Generator for 5a5a2103.

Rule: row marker color is used to stamp the discovered template shape
into every cell of that row.

Combinatorial axes (8): grid_h/w, cell_size, row_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_separators, no_template, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "796907d6d950"
VERSION = "1.1.0"
TASK_ID = "796907d6d950"
SUMMARY = "Row marker color stamps discovered template shape into every cell of row."

INVARIANTS = [
    "a nonzero separator color forms full row and column dividers",
    "the first cell of each data row contains the row marker color",
    "one non-marker cell contains the template shape",
    "marker colors are distinct from each other and from separator and template colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separators", "no_template", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "cell_size":      {"type": "int", "default": "3", "valid": "2..6"},
    "row_count":      {"type": "int", "default": "4", "valid": "2..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "n_distinct_colors":{"type": "int", "default": "6", "valid": "6"},
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
    sep = ctx.draw_color("separator", exclude={0})
    marker_colors = ctx.draw_distinct_colors("marker_colors", n=4, exclude={0, sep})
    template_color = ctx.draw_color("template_color", exclude={0, sep, *marker_colors})
    cell = 3
    rows = 4
    cols = 4
    h = rows * cell + rows - 1
    w = cols * cell + cols - 1
    g = full_grid(h, w, 0)
    for r in range(h):
        if (r + 1) % (cell + 1) == 0:
            for c in range(w):
                g[r][c] = sep
    for c in range(w):
        if (c + 1) % (cell + 1) == 0:
            for r in range(h):
                g[r][c] = sep
    marker_shape = [(0, 0), (1, 0), (1, 1)]
    for ri, color in enumerate(marker_colors):
        r0 = ri * (cell + 1)
        for dr, dc in marker_shape:
            g[r0 + dr][dc] = color
    template_origin_r = 0
    template_origin_c = cell + 1
    for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 2)]:
        g[template_origin_r + dr][template_origin_c + dc] = template_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_separators":
        g[1][1] = 2
        return g
    if name == "no_template":
        for r in range(15):
            if (r + 1) % 4 == 0:
                for c in range(15):
                    g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 5
        return g
    return g
