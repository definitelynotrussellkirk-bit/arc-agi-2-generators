"""Generator for ARC task 48131b3c.

Rule: find first non-zero color (nz). Output is 2h × 2w where
output[r][c] = nz if input[r mod h][c mod w] == 0, else 0.
(Negative tiling — output is the complement of input, tiled 2×2.)

Combinatorial axes (8): grid_h/w, fg_color, fg_density, fg_layout,
texture, asymmetry, multi_color_input.
Degenerates: all_zero (output all nz, but no nz to read),
all_filled (output all 0), monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "11c53dabb028"
VERSION = "1.1.0"
TASK_ID = "11c53dabb028"
SUMMARY = "Small grid with non-zero cells; rule outputs 2h × 2w negative tiling."

INVARIANTS = [
    "input contains ≥1 non-zero cell (rule reads its color)",
    "input contains ≥1 zero cell (so output has ≥1 nz cell)",
    "input dims ≤ 7 (so 2× output ≤ 14)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("all_zero", "all_filled", "monochrome")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 2..7", "valid": "1..15"},
    "grid_w":         {"type": "int", "default": "rng 2..7", "valid": "1..15"},
    "fg_color":       {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "fg_density":     {"type": "float", "default": "rng 0.3..0.6", "valid": "0..1"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "multi_color":    {"type": "bool", "default": "false", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 2, 4
    elif difficulty == "hard":
        h_lo, h_hi = 5, 7
    else:
        h_lo, h_hi = 2, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    multi = bool(overrides.get("multi_color", False))
    palette = [fg]
    if multi:
        extras = list(ctx.draw_distinct_colors("extras", n=2, exclude={0, fg}))
        palette = [fg] + extras
    full_palette = [0] + palette
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, full_palette, rng)
    fill_d = float(overrides.get("fg_density",
                                 ctx.draw_rng("fg_density").uniform(0.3, 0.6)))
    if fill_d < 1.0:
        g = apply_bg_density(g, full_palette, rng, 1.0 - fill_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, full_palette, rng, no)
    if not any(g[r][c] != 0 for r in range(h) for c in range(w)):
        g[0][0] = fg
    if not any(g[r][c] == 0 for r in range(h) for c in range(w)):
        g[h - 1][w - 1] = 0
    return g


def _draw_from_degenerate(name, h, w, rng):
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g = full_grid(h, w, 0)
    if name == "all_zero":
        # Need ≥1 nz for rule to find color. Place 1 cell.
        g[0][0] = fg
        return g
    if name == "all_filled":
        for r in range(h):
            for c in range(w):
                g[r][c] = fg
        return g
    if name == "monochrome":
        # All cells same fg → output all 0.
        for r in range(h):
            for c in range(w):
                g[r][c] = fg
        return g
    return g
