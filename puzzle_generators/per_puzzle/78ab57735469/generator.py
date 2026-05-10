"""Generator for ARC task c48954c1.

Rule: input is N×N. Output is 3N × 3N where each block (br, bc) is the
tile, flipped vertically when br is even and horizontally when bc is
even.

Combinatorial axes (8): side, palette_size, texture, bg_density,
noise_overlay, asymmetry_force, anchor_corners, color_distribution.
Degenerates: monochrome, full_symmetric, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "78ab57735469"
VERSION = "1.1.0"
TASK_ID = "78ab57735469"
SUMMARY = "Square tile expanded into 3×3 arrangement with blockwise flips."

INVARIANTS = [
    "input is square (N in [2, 5])",
    "3N <= 30 (output fits 30×30 limit)",
    "tile is NOT both LR-symmetric and UD-symmetric (flipping must change something)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "full_symmetric", "single_cell")

AXES = {
    "side":           {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "2..7"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.3", "valid": "0..0.7"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.2"},
    "asymmetry_force": {"type": "bool", "default": "true", "valid": "true|false"},
    "anchor_corners": {"type": "bool", "default": "false", "valid": "true|false"},
    "color_distribution": {"type": "str", "default": "rng even|skewed",
                           "valid": "even|skewed"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi, c_lo, c_hi = 2, 3, 2, 3
    elif difficulty == "hard":
        n_lo, n_hi, c_lo, c_hi = 4, 5, 4, 7
    else:
        n_lo, n_hi, c_lo, c_hi = 2, 5, 2, 5
    n = ctx.draw_int("side", n_lo, n_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = list(ctx.draw_distinct_colors("palette", n=max(2, n_colors)))
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, palette, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, n, n, palette, rng)
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.3)))
    if bg_d > 0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0:
        g = apply_noise_overlay(g, palette, rng, no)
    if bool(overrides.get("asymmetry_force", True)):
        if _is_lr_sym(g) and _is_ud_sym(g):
            other = next((c for c in palette if c != g[0][0]), None)
            if other is not None and n >= 2:
                g[0][0] = other
    if bool(overrides.get("anchor_corners", False)):
        g[0][0] = palette[0]
        g[n - 1][n - 1] = palette[1] if len(palette) > 1 else palette[0]
    if len({v for row in g for v in row}) < 2:
        g[0][n - 1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _is_lr_sym(g):
    h, w = len(g), len(g[0])
    return all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))


def _is_ud_sym(g):
    h, w = len(g), len(g[0])
    return all(g[r][c] == g[h - 1 - r][c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, n, palette, rng):
    if name == "monochrome":
        c = rng.choice(palette)
        return [[c] * n for _ in range(n)]
    if name == "full_symmetric":
        g = full_grid(n, n, palette[0])
        for r in range(n // 2 + 1):
            for c in range(n // 2 + 1):
                v = rng.choice(palette)
                g[r][c] = v
                g[r][n - 1 - c] = v
                g[n - 1 - r][c] = v
                g[n - 1 - r][n - 1 - c] = v
        return g
    if name == "single_cell":
        g = full_grid(n, n, palette[0])
        g[n // 2][n // 2] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
        return g
    return full_grid(n, n, palette[0])
