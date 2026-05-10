"""Generator for arc_additional_puzzles_21_set6:E41.

Rule: take the 2-shape (normalized to bbox-origin); for each 3-cell
"anchor", paint the same shape in color 3 at that anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_anchors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_anchors, anchor_clips_off_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "70c6c02a44ac"
VERSION = "1.1.0"
TASK_ID = "70c6c02a44ac"
SUMMARY = "One 2-shape (template) and 1-2 3-anchors elsewhere."

INVARIANTS = [
    "exactly 1 2-shape (≥3 cells) somewhere on grid",
    "1-2 isolated 3-cells (anchors)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "anchor_clips_off_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "template_top_anchors_below",
                       "valid": "template_top_anchors_below"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape = rng.choice([
        [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 0)],
    ])
    sr = rng.randint(0, 1); sc = rng.randint(0, 1)
    paint_at(g, sr, sc, shape, 2)
    g[rng.randint(0, 2)][w - rng.randint(2, 3)] = 3
    g[h - rng.randint(1, 2)][rng.randint(2, 5)] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    shape = [(0, 0), (0, 1), (1, 0)]
    if name == "no_template":
        # only anchors, no 2-shape template → nothing to stamp
        g[2][7] = 3
        g[5][3] = 3
        return g
    if name == "no_anchors":
        # template only, no 3-anchors → nothing to stamp at
        paint_at(g, 1, 1, shape, 2)
        return g
    if name == "anchor_clips_off_grid":
        # anchor near bottom-right corner → stamp would extend off-grid
        paint_at(g, 1, 1, shape, 2)
        g[h - 1][w - 1] = 3
        return g
    return g
