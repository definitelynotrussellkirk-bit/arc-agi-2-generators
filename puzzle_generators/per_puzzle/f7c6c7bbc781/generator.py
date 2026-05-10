"""Generator for puzzle 85c4e7cd.

Rule: read diagonal cells g[d][d] for d in 0..max_d. For each output
cell, compute distance to nearest edge d_min; output color = nth(diag,
max_d - d_min). Effect: concentric rings with swapped (innermost↔outermost)
colors from the diagonal.

Combinatorial axes (8): grid_h/w, palette_size, diagonal_pattern (random/
gradient/banded/repeat), texture, ring_uniqueness (whether diag colors
are unique → distinct rings), edge_decoy, multi_color_seed.
Degenerates: monochrome, single_diag, all_distinct.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "f7c6c7bbc781"
VERSION = "1.1.0"
TASK_ID = "f7c6c7bbc781"
SUMMARY = "Diagonal-cell colors define concentric rings; rule outputs swapped (innermost↔outermost) rings."

INVARIANTS = [
    "h ≥ 4 and w ≥ 4 so there are ≥2 ring layers",
    "≥2 distinct diagonal colors so the ring pattern is visible",
]

DIAGONAL_PATTERNS = ("random", "gradient", "banded", "repeat", "alternating")
HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring",
)
DEGENERATE_TEXTURES = ("monochrome", "single_diag", "all_same_diag")

AXES = {
    "grid_h":            {"type": "int", "default": "rng 4..14", "valid": "2..18"},
    "grid_w":            {"type": "int", "default": "rng 4..14", "valid": "2..18"},
    "palette_size":      {"type": "int", "default": "rng 3..6", "valid": "1..10"},
    "diagonal_pattern":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(DIAGONAL_PATTERNS)},
    "texture":           {"type": "str", "default": "rng helpful",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "edge_decoy":        {"type": "float", "default": "rng 0..0.3", "valid": "0..0.7"},
    "ring_count_min":    {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "noise_overlay":     {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, c_lo, c_hi = 4, 6, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi = 11, 14, 5, 8
    else:
        h_lo, h_hi, c_lo, c_hi = 4, 14, 3, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", c_lo, c_hi)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(2, n_palette)))
    diag_pattern = overrides.get("diagonal_pattern",
                                 ctx.draw_choice("diagonal_pattern",
                                                 list(DIAGONAL_PATTERNS)))
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    edge_decoy = float(overrides.get("edge_decoy",
                                     ctx.draw_rng("edge_decoy").uniform(0.0, 0.3)))
    g = fill_texture(texture, h, w, palette, rng)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)
    # Set diagonal cells per pattern
    max_d = (min(h, w) // 2) - 1
    if max_d < 1:
        max_d = 1
    diag_colors = _make_diagonal_colors(diag_pattern, max_d + 1, palette, rng)
    for d in range(max_d + 1):
        if d < h and d < w:
            g[d][d] = diag_colors[d]
    return g


def _make_diagonal_colors(pattern, n, palette, rng):
    if pattern == "random":
        return [rng.choice(palette) for _ in range(n)]
    if pattern == "gradient":
        return [palette[i * len(palette) // max(1, n)] for i in range(n)]
    if pattern == "banded":
        block = max(1, n // 3)
        return [palette[(i // block) % len(palette)] for i in range(n)]
    if pattern == "repeat":
        return [palette[0] if i % 2 == 0 else palette[-1] for i in range(n)]
    if pattern == "alternating":
        return [palette[i % len(palette)] for i in range(n)]
    return [rng.choice(palette) for _ in range(n)]


def _draw_from_degenerate(name, h, w, rng):
    palette = list(range(0, 10))
    rng.shuffle(palette)
    g = full_grid(h, w, palette[0])
    if name == "monochrome":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "single_diag":
        for d in range((min(h, w) // 2)):
            g[d][d] = palette[1]
        return g
    if name == "all_same_diag":
        for d in range((min(h, w) // 2)):
            g[d][d] = palette[1]
        return g
    return g
