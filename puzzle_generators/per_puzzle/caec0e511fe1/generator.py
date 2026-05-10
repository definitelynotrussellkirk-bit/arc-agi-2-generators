"""Generator for puzzle 49d1d64f.

Rule: fully colored grid; rule extends with 1-cell border that mirrors
outer rows/cols (corners stay 0).

Combinatorial axes (8): grid_h/w, palette_size, texture, bg_density,
noise_overlay, fully_colored, palette_skew, edge_uniqueness.
Degenerates: monochrome, two_color_uniform, single_row_or_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "caec0e511fe1"
VERSION = "1.1.0"
TASK_ID = "caec0e511fe1"
SUMMARY = "Fully colored grid; rule adds 1-cell mirrored border (corners 0)."

INVARIANTS = [
    "every cell non-zero (fully colored)",
    "2+h <= 30 and 2+w <= 30",
    ">=2 distinct colors so border is non-trivial",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "two_color_uniform", "single_row_or_col")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..14", "valid": "2..28"},
    "grid_w":         {"type": "int", "default": "rng 3..14", "valid": "2..28"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "0", "valid": "0..0.3"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.2"},
    "palette_skew":   {"type": "str", "default": "rng even|skewed",
                       "valid": "even|skewed"},
    "edge_uniqueness": {"type": "bool", "default": "false", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, c_lo, c_hi = 2, 4, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi = 12, 22, 5, 9
    else:
        h_lo, h_hi, c_lo, c_hi = 3, 14, 2, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=max(2, n_colors), exclude={0}))
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, palette, rng)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0:
        g = apply_noise_overlay(g, palette, rng, no)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 0:
                g[r][c] = palette[0]
    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else palette[0]
    if bool(overrides.get("edge_uniqueness", False)) and len(palette) >= 4:
        g[0][0] = palette[0]
        g[0][w - 1] = palette[1]
        g[h - 1][0] = palette[2]
        g[h - 1][w - 1] = palette[3]
    return g


def _draw_from_degenerate(name, h, w, rng):
    palette = [c for c in range(1, 10)]
    rng.shuffle(palette)
    if name == "monochrome":
        c = palette[0]
        return [[c] * w for _ in range(h)]
    if name == "two_color_uniform":
        c1, c2 = palette[0], palette[1]
        g = full_grid(h, w, c1)
        for r in range(h):
            for c in range(w):
                g[r][c] = c1 if (r + c) % 2 == 0 else c2
        return g
    if name == "single_row_or_col":
        if rng.random() < 0.5 and h >= 2:
            row_color = palette[0]
            other = palette[1]
            g = full_grid(h, w, other)
            for c in range(w):
                g[0][c] = row_color
            return g
        col_color = palette[0]
        other = palette[1]
        g = full_grid(h, w, other)
        for r in range(h):
            g[r][0] = col_color
        return g
    return [[1] * w for _ in range(h)]
