"""Generator for ed98d772.

Rule: tile n×n into 2n×2n: TL=identity, TR=rot-ccw90, BL=rot-180,
BR=rot-cw90.

Combinatorial axes (8): grid_n, palette_size, texture, bg_density,
noise_overlay, asymmetry_force, anchor_corner, fg_density.
Degenerates: monochrome, full_4fold_sym, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "9db8deba5903"
VERSION = "1.1.0"
TASK_ID = "9db8deba5903"
SUMMARY = "n×n grid; rule tiles 2n×2n with 4 rotations."

INVARIANTS = [
    "square (h == w) in [3, 7]",
    "2n <= 30",
    ">=2 distinct colors so rotations are visible",
    "grid is NOT 4-fold symmetric (so rotations differ)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "full_4fold_sym", "single_cell")

AXES = {
    "grid_n":          {"type": "int", "default": "rng 3..7", "valid": "3..7"},
    "palette_size":    {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "texture":         {"type": "str", "default": "rng helpful",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":      {"type": "float", "default": "rng 0..0.4",
                        "valid": "0..0.7"},
    "noise_overlay":   {"type": "float", "default": "rng 0..0.05",
                        "valid": "0..0.2"},
    "asymmetry_force": {"type": "bool", "default": "true",
                        "valid": "true|false"},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "fg_density":      {"type": "float", "default": "rng 0.4..0.7",
                       "valid": "0.1..1"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        n_lo, n_hi = 6, 7
    else:
        n_lo, n_hi = 3, 7
    n = ctx.draw_int("grid_n", n_lo, n_hi)
    n_colors = ctx.draw_int("palette_size", 2, 4)
    palette = list(ctx.draw_distinct_colors("palette", n=n_colors))
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, palette, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, n, n, palette, rng)
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0:
        g = apply_noise_overlay(g, palette, rng, no)
    if bool(overrides.get("asymmetry_force", True)):
        if _is_4fold_sym(g, n) and len(palette) > 1:
            other = next((c for c in palette if c != g[0][0]), None)
            if other is not None and n >= 2:
                g[0][n - 1] = other
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = palette[0]
    if len({v for row in g for v in row}) < 2:
        g[0][n - 1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _is_4fold_sym(g, n):
    if n != len(g[0]):
        return False
    for r in range(n):
        for c in range(n):
            v = g[r][c]
            if g[c][n - 1 - r] != v:
                return False
            if g[n - 1 - r][n - 1 - c] != v:
                return False
            if g[n - 1 - c][r] != v:
                return False
    return True


def _draw_from_degenerate(name, n, palette, rng):
    g = full_grid(n, n, palette[0])
    if name == "monochrome":
        c = rng.choice(palette)
        return [[c] * n for _ in range(n)]
    if name == "full_4fold_sym":
        for r in range((n + 1) // 2):
            for c in range((n + 1) // 2):
                v = rng.choice(palette)
                g[r][c] = v
                g[c][n - 1 - r] = v
                g[n - 1 - r][n - 1 - c] = v
                g[n - 1 - c][r] = v
        return g
    if name == "single_cell":
        g[n // 2][n // 2] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
        return g
    return g
