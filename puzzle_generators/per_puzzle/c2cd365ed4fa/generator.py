"""Generator for puzzle aaecdb9a.

Rule: count 8-connected components of each color on bg=7. Output
histogram with fixed col mapping {5:0, 2:1, 8:2, 9:3, 6:4}, stacked
from bottom.

Combinatorial axes (8): grid_h/w, n_colors, n_comp_min, n_comp_max,
comp_size_min, comp_size_max, position_bias, anchor_corner.
Degenerates: no_components, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "c2cd365ed4fa"
VERSION = "1.1.0"
TASK_ID = "c2cd365ed4fa"
SUMMARY = "Color components on bg=7; rule outputs histogram per fixed col map."

INVARIANTS = [
    "background is 7",
    "2-5 colors from {2, 5, 6, 8, 9}",
    "each color forms 1-4 distinct 8-conn components",
    "components non-overlapping with margin >=1",
]

POSITION_BIASES = ("scattered", "row_aligned", "clustered", "diagonal")
DEGENERATE_TEXTURES = ("no_components", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_colors":       {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "n_comp_min":     {"type": "int", "default": "1", "valid": "1..3"},
    "n_comp_max":     {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "comp_size_min":  {"type": "int", "default": "1", "valid": "1..3"},
    "comp_size_max":  {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", 2, 4)))
    n_colors = max(2, min(5, n_colors))
    n_comp_min = int(overrides.get("n_comp_min", 1))
    n_comp_max = int(overrides.get("n_comp_max",
                                   ctx.draw_int("n_comp_max", 2, 4)))
    cs_min = int(overrides.get("comp_size_min", 1))
    cs_max = int(overrides.get("comp_size_max",
                               ctx.draw_int("comp_size_max", 1, 2)))
    available = [2, 5, 6, 8, 9]
    rng.shuffle(available)
    colors = available[:n_colors]
    g = full_grid(h, w, 7)
    for color in colors:
        n_comps = rng.randint(n_comp_min, max(n_comp_min, n_comp_max))
        for _ in range(n_comps):
            sz = rng.randint(cs_min, max(cs_min, cs_max))
            cells = normalize(rect_cells(sz, sz))
            place_no_overlap(rng, g, cells, color, bg=7,
                             margin=1, max_tries=30)
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 7)
    if name == "no_components":
        return g
    if name == "single_color":
        for r in range(2, 5):
            g[r][2] = 5
            g[r + 4][6] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
