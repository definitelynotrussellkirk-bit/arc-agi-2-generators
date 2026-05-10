"""Generator for 20b:m134 — select legend-color blob, flip-lr.

Rule: at(0,0) = legend color. Pick the largest non-corner blob of
that color, crop, flip-lr.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_legend_blob, lr_symmetric_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "f7aca7ec2012"
VERSION = "1.1.0"
TASK_ID = "f7aca7ec2012"
SUMMARY = "Legend at (0,0) + a same-color non-LR-symmetric blob away from corner + 1-2 distractors."

INVARIANTS = [
    "background is 0",
    "(0,0) holds the legend color",
    "≥1 same-color blob away from corner, LR-asymmetric so flip changes it",
    "1-2 distractor blobs in different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_legend_blob", "lr_symmetric_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "legend_corner_blobs_inside",
                       "valid": "legend_corner_blobs_inside"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    legend = palette[0]
    g[0][0] = legend
    used = {(0, 0)}
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(3, 4), max_attempts=20)
        if cells is None: continue
        rs = sorted(r for r, _ in cells); cs = sorted(c for _, c in cells)
        cmin, cmax = cs[0], cs[-1]
        norm = {(r - rs[0], c - cmin) for r, c in cells}
        flipped = {(r, (cmax - cmin) - c) for r, c in norm}
        if norm == flipped: continue
        for r, c in cells: g[r][c] = legend
        used |= cells
        break
    for color in palette[1:]:
        b = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=40)
        if b:
            for r, c in b: g[r][c] = color
            used |= b
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Blobs but (0,0) is empty — rule's "color at (0,0)" lookup
        # returns no legend; can't pick a target color.
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 4
        for r, c in [(6, 6), (6, 7)]: g[r][c] = 6
        return g
    if name == "no_legend_blob":
        # Legend present but no body blob in the legend color — rule's
        # "pick largest non-corner blob of legend color" finds none.
        g[0][0] = 4
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 6
        for r, c in [(6, 6), (6, 7)]: g[r][c] = 7
        return g
    if name == "lr_symmetric_blob":
        # Legend blob is left-right symmetric — flip-lr is identity,
        # rule's effect is invisible.
        g[0][0] = 4
        for r, c in [(3, 3), (3, 4), (3, 5), (4, 4)]: g[r][c] = 4
        for r, c in [(6, 6), (6, 7)]: g[r][c] = 6
        return g
    return g
