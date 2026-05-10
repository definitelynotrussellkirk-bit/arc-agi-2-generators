"""Generator for ARC task 973e499e.

Rule: input is N×N. Output is N²×N²: cell (r,c) keeps input(br,bc) if
input(sr,sc) == input(br,bc), else 0 (where (br,bc) = block coord
(r/N,c/N), (sr,sc) = inner coord (r%N,c%N)).

Combinatorial axes (8): side, palette_size, fg_color, fg_density,
texture, balanced, lr_diversity, anchor_corner.
Degenerates: monochrome, two_color_diag, all_unique_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "7efd5fabc951"
VERSION = "1.1.0"
TASK_ID = "7efd5fabc951"
SUMMARY = "Square tile; output N²×N² keeps cells matching block's source color."

INVARIANTS = [
    "input is square (side N in [2,5])",
    "output N² × N² stays within ARC limits (so N ≤ 5)",
    "≥2 distinct colors appear (so the rule has a visible effect)",
    "at least one cell DIFFERS from corresponding source so output is non-trivial",
]

DEGENERATE_TEXTURES = ("monochrome", "two_color_diag", "all_unique_cells")
HELPFUL_TEXTURES = ("noise", "sparse", "blob", "stripes",
                    "gradient", "checkerboard", "frame", "ring", "plus")

AXES = {
    "side":         {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "palette_size": {"type": "int", "default": "rng 2..5", "valid": "2..6"},
    "texture":      {"type": "str", "default": "rng helpful",
                     "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":   {"type": "float", "default": "rng 0..0.2", "valid": "0..0.5"},
    "noise_overlay": {"type": "float", "default": "rng 0..0.05", "valid": "0..0.2"},
    "lr_diversity": {"type": "bool", "default": "true", "valid": "true|false"},
    "anchor_corner": {"type": "bool", "default": "true", "valid": "true|false"},
    "balanced":     {"type": "bool", "default": "false", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi, c_lo, c_hi = 2, 3, 2, 2
    elif difficulty == "hard":
        n_lo, n_hi, c_lo, c_hi = 4, 5, 4, 6
    else:
        n_lo, n_hi, c_lo, c_hi = 2, 5, 2, 5
    n = ctx.draw_int("side", n_lo, n_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, min(c_hi, n * n))
    palette = list(ctx.draw_distinct_colors("palette", n=max(2, n_colors), exclude={0}))
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, palette, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, n, n, palette, rng)
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.2)))
    if bg_d > 0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0:
        g = apply_noise_overlay(g, palette, rng, no)
    if bool(overrides.get("anchor_corner", True)):
        g[0][0] = palette[0]
        g[n - 1][n - 1] = palette[1] if len(palette) > 1 else palette[0]
    if len({v for row in g for v in row}) < 2:
        g[0][n - 1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _draw_from_degenerate(name, n, palette, rng):
    if name == "monochrome":
        return full_grid(n, n, palette[0])
    if name == "two_color_diag":
        g = full_grid(n, n, palette[0])
        c2 = palette[1] if len(palette) > 1 else 1
        for i in range(n):
            g[i][i] = c2
        return g
    if name == "all_unique_cells":
        full = list(range(1, 10))
        rng.shuffle(full)
        g = full_grid(n, n, palette[0])
        idx = 0
        for r in range(n):
            for c in range(n):
                g[r][c] = full[idx % len(full)]
                idx += 1
        return g
    return full_grid(n, n, palette[0])
