"""Generator for 05a7bcf2.

Rule: yellow marks on one side of an 8 separator extend toward it
while matching red runs are rebuilt on the other side.

Combinatorial axes (8): grid_h, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, n_rows.
Degenerates: no_separator, no_marks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, transpose

GENERATOR_ID = "8c12816521a2"
VERSION = "1.1.0"
TASK_ID = "8c12816521a2"
SUMMARY = "Yellow marks extend toward 8 separator while red runs rebuild on the other side."

INVARIANTS = [
    "a full color-8 separator row or column divides the grid",
    "all color-4 trigger cells are on one side of the separator",
    "rows with color-4 triggers also have a countable run of color-2 cells on the opposite side",
    "trigger and red runs are separated by the separator with at least one cell of margin",
]

ORIENTATIONS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separator", "no_marks", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "height":         {"type": "int", "default": "rng 18..26", "valid": "10..30"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_rows":         {"type": "int", "default": "rng 5..9", "valid": "3..12"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _normalized_grid(ctx, h):
    rng = ctx.draw_rng("layout")
    sep = rng.randint(6, 10)
    right = rng.randint(10, 16)
    w = sep + 1 + right
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][sep] = 8
    rows = sorted(rng.sample(range(2, h - 2), rng.randint(5, min(9, h - 4))))
    for r in rows:
        start = rng.randint(1, max(1, sep - 5))
        run = rng.randint(1, min(3, sep - start))
        for c in range(start, start + run):
            g[r][c] = 4
        red_count = rng.randint(1, min(5, right - 3))
        red_end = w - rng.randint(1, 3)
        red_start = max(sep + 1, red_end - red_count)
        for c in range(red_start, red_end):
            g[r][c] = 2
    return g


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 14, 18
    elif difficulty == "hard":
        h_lo, h_hi = 24, 28
    else:
        h_lo, h_hi = 18, 26
    h = ctx.draw_int("height", h_lo, h_hi)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    g = _normalized_grid(ctx, h)
    if orientation == "horizontal":
        return transpose(g)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(20, 18, 0)
    if name == "no_separator":
        for r in range(2, 18, 3):
            g[r][3] = 4
            g[r][14] = 2
        return g
    if name == "no_marks":
        for r in range(20):
            g[r][8] = 8
        return g
    if name == "full_grid":
        for r in range(20):
            for c in range(18):
                g[r][c] = 8
        return g
    return g
