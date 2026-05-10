"""Generator for ARC task d4b1c2b1.

Rule: count distinct colors n. If n ≤ 1 → output = input. Else output
is (h*n) × (w*n) where output[r][c] = input[r/n][c/n]. (Upscale by n.)

Combinatorial axes (8): grid_h/w, color_count (n), texture, palette,
color_distribution, fg_density, bg_density, n_target_unique
(forces exactly n distinct colors).
Degenerates: monochrome (n=1, output==input), max_colors,
all_distinct_per_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "7a37505e7bd0"
VERSION = "1.1.0"
TASK_ID = "7a37505e7bd0"
SUMMARY = "Small multicolor grid; rule upscales by n = number of distinct colors."

INVARIANTS = [
    "≥1 distinct color (n ≥ 1; if n == 1, output == input)",
    "(h*n, w*n) ≤ 30 so output fits within ARC bounds",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "max_colors", "all_distinct_per_cell")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 2..6", "valid": "1..7"},
    "grid_w":         {"type": "int", "default": "rng 2..6", "valid": "1..7"},
    "color_count":    {"type": "choice", "default": "rng 2|3|4|5",
                       "valid": "1|2|3|4|5"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "force_n_unique": {"type": "bool", "default": "true", "valid": "true|false"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false (anchor each color to a corner)"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, c_choices = 2, 4, [2, 3]
    elif difficulty == "hard":
        h_lo, h_hi, c_choices = 5, 6, [4, 5]
    else:
        h_lo, h_hi, c_choices = 2, 6, [1, 2, 3, 4, 5]
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n = ctx.draw_choice("color_count", c_choices)
    while h * n > 30 or w * n > 30:
        n -= 1
    if n < 1:
        n = 1
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, n, rng)
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n)))
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
    if bool(overrides.get("force_n_unique", True)):
        # Force exactly n distinct colors (place each at corners or anchors).
        if bool(overrides.get("anchor_corner", False)):
            corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
            for i, color in enumerate(palette[:n]):
                g[corners[i % len(corners)][0]][corners[i % len(corners)][1]] = color
        else:
            for i, color in enumerate(palette[:n]):
                rr = i % h; rc = (i // h) % w
                g[rr][rc] = color
        # Trim distinct colors down to n if there are more.
        actual = {v for row in g for v in row}
        if len(actual) > n:
            keep = set(palette[:n])
            extras = actual - keep
            for r in range(h):
                for c in range(w):
                    if g[r][c] in extras:
                        g[r][c] = palette[0]
    return g


def _draw_from_degenerate(name, h, w, n, rng):
    palette = list(range(0, 10))
    rng.shuffle(palette)
    g = full_grid(h, w, palette[0])
    if name == "monochrome":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "max_colors":
        # Use 5 colors → output is (h*5, w*5). Cap dims to fit.
        if h * 5 > 30 or w * 5 > 30:
            h, w = 5, 5
        used = palette[:5]
        for i, color in enumerate(used):
            rr = i % h; rc = (i // h) % w
            g_row = rr if rr < len(g) else rr % len(g)
            g_col = rc if rc < len(g[0]) else rc % len(g[0])
            g[g_row][g_col] = color
        return g
    if name == "all_distinct_per_cell":
        # Each cell a different color (capped at 9).
        cells = [(r, c) for r in range(h) for c in range(w)]
        for i, (r, c) in enumerate(cells[:9]):
            g[r][c] = palette[i]
        return g
    return g
