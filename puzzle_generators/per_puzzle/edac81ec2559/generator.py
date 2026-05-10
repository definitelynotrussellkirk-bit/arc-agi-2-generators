"""Generator for arc_puzzle_bank_eighth21:E53.

Rule: overlay the image with its reflection across the horizontal midline.

Combinatorial axes (8): grid_h/w, palette_kind, marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_symmetric, no_marks, marks_in_lower.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "edac81ec2559"
VERSION = "1.1.0"
TASK_ID = "edac81ec2559"
SUMMARY = "Overlay the image with its reflection across the horizontal midline."

INVARIANTS = [
    "background is 0",
    "input marks are in the upper half",
    "output keeps originals and adds reflected lower-half copies",
    "height may be odd or even",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("already_symmetric", "no_marks", "marks_in_lower")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marks":          {"type": "int", "default": "rng 4..7", "valid": "1..20"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "upper_half",
                       "valid": "upper_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..7",
                          "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target_max = 5
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target_max = 7
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target_max = 7
    marks = ctx.draw_int("marks", 4, target_max)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    source_rows = list(range(max(1, h // 2)))
    cells = [(r, c) for r in source_rows for c in range(w) if r != h - 1 - r]
    for r, c in rng.sample(cells, min(marks, len(cells))):
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "already_symmetric":
        # both halves filled — rule output equals input
        for r, c, v in [(1, 2, 4), (6, 2, 4), (2, 5, 7), (5, 5, 7)]:
            g[r][c] = v
        return g
    if name == "no_marks":
        return g
    if name == "marks_in_lower":
        # marks in lower half instead of upper — rule reflects them up, but the
        # invariant says marks should be upper-only
        g[5][2] = 4
        g[6][3] = 7
        return g
    return g
