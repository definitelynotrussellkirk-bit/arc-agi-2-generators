"""Generator for puzzle 8d5021e8.

Rule: any colored grid. Output is 3h × 2w of mirrored copies (vertical
mirror + alternating row blocks of flip-ud).

Combinatorial axes (8): grid_h/w, palette_size, bgc, texture,
fg_density, bg_density, noise_overlay, asymmetry_force.
Degenerates: monochrome, lr_symmetric, ud_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "1a259ef9a7e7"
VERSION = "1.1.0"
TASK_ID = "1a259ef9a7e7"
SUMMARY = "Any colored grid; rule outputs 3h × 2w mirrored stack."

INVARIANTS = [
    "3*h <= 30",
    "2*w <= 30",
    ">=2 distinct colors so the mirrored copies are visible",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "lr_symmetric", "ud_symmetric")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 2..10", "valid": "1..10"},
    "grid_w":         {"type": "int", "default": "rng 2..15", "valid": "1..15"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "bgc":            {"type": "color", "default": "rng", "valid": "0..9"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "asymmetry_force": {"type": "bool", "default": "true", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 4, 2, 5, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 7, 10, 10, 15, 4, 7
    else:
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 10, 2, 15, 2, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = list(ctx.draw_distinct_colors("palette", n=max(2, n_colors)))
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, palette, rng)
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0:
        g = apply_noise_overlay(g, palette, rng, no)
    if bool(overrides.get("asymmetry_force", True)):
        if h >= 1 and w >= 2 and len(palette) > 1 and _is_lr_sym(g):
            g[0][0] = palette[1]
        if h >= 2 and len(palette) > 1 and _is_ud_sym(g):
            g[0][0] = palette[1] if g[0][0] != palette[1] else palette[0]
    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _is_lr_sym(g):
    h, w = len(g), len(g[0])
    return all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))


def _is_ud_sym(g):
    h, w = len(g), len(g[0])
    return all(g[r][c] == g[h - 1 - r][c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    g = full_grid(h, w, palette[0])
    if name == "monochrome":
        c = rng.choice(palette)
        return [[c] * w for _ in range(h)]
    if name == "lr_symmetric":
        for r in range(h):
            for c in range(w // 2):
                v = rng.choice(palette)
                g[r][c] = v
                g[r][w - 1 - c] = v
        if w % 2 == 1:
            for r in range(h):
                g[r][w // 2] = rng.choice(palette)
        return g
    if name == "ud_symmetric":
        for r in range(h // 2):
            for c in range(w):
                v = rng.choice(palette)
                g[r][c] = v
                g[h - 1 - r][c] = v
        if h % 2 == 1:
            for c in range(w):
                g[h // 2][c] = rng.choice(palette)
        return g
    return g
