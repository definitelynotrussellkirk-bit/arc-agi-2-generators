"""Generator for ARC task 00576224.

Rule: output is 3h × 3w. For tile row block (r // h): if even, use
input as-is; else, use input's LR mirror. Effect: 3-row vertical
tiling with alternating LR mirror.

Combinatorial axes: grid_h/w, palette_size, texture, lr_asymmetric.
Degenerates: monochrome, lr_symmetric (mirror invisible), single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "ecc04b33119c"
VERSION = "1.1.0"
TASK_ID = "ecc04b33119c"
SUMMARY = "Small multicolor tile; rule tiles 3 × 3 vertically alternating with LR mirror."

INVARIANTS = [
    "input dims ≤ (10, 10) so 3 × output fits",
    "≥2 colors so the mirror is visible",
    "input is not LR-symmetric (else the mirror has no effect)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "lr_symmetric", "single_pixel")

AXES = {
    "grid_h":         {"type": "int",   "default": "rng 2..6", "valid": "1..10"},
    "grid_w":         {"type": "int",   "default": "rng 2..6", "valid": "1..10"},
    "palette_size":   {"type": "int",   "default": "rng 2..6", "valid": "1..10"},
    "texture":        {"type": "str",   "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "lr_asymmetric":  {"type": "bool",  "default": "true", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, c_lo, c_hi = 2, 3, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi = 5, 6, 5, 8
    else:
        h_lo, h_hi, c_lo, c_hi = 2, 6, 2, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, palette, rng)
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)
    if bool(overrides.get("lr_asymmetric", True)) and _is_lr_sym(g):
        g[0][0] = palette[1] if len(palette) > 1 else (g[0][0] + 1) % 10
    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _is_lr_sym(g):
    h = len(g); w = len(g[0])
    return all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    g = full_grid(h, w, palette[0])
    if name == "monochrome":
        c0 = rng.choice(palette)
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "lr_symmetric":
        for r in range(h):
            for c in range(w // 2):
                v = rng.choice(palette)
                g[r][c] = v
                g[r][w - 1 - c] = v
        return g
    if name == "single_pixel":
        rr = rng.randint(0, h - 1); rc = rng.randint(0, w - 1)
        g[rr][rc] = palette[1] if len(palette) > 1 else palette[0]
        return g
    return g
