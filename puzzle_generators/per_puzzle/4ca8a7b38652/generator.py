"""Generator for puzzle b91ae062.

Rule: small fully-colored grid. Output is upscaled by n where n =
number of distinct non-bg colors in the grid.

Combinatorial axes (8): grid_h/w, n_colors, palette_choice, texture,
color_balance, anchor_origin, frame_force, asymmetry_force.
Degenerates: monochrome, two_color_uniform, single_color_dominates.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "4ca8a7b38652"
VERSION = "1.1.0"
TASK_ID = "4ca8a7b38652"
SUMMARY = "Fully colored small grid; rule upscales by number of distinct colors."

INVARIANTS = [
    "every cell is non-bg (no 0 in input)",
    ">=2 distinct colors so the upscale factor is meaningful",
    "n_colors * h <= 30 and n_colors * w <= 30 (output fits)",
    "each chosen color appears at least once in the grid",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "two_color_uniform", "single_color_dominates")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "grid_w":         {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "n_colors":       {"type": "int", "default": "rng 2..max", "valid": "2..9"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "color_balance":  {"type": "str", "default": "rng even|skewed",
                       "valid": "even|skewed"},
    "anchor_origin":  {"type": "bool", "default": "false", "valid": "true|false"},
    "asymmetry_force": {"type": "bool", "default": "false", "valid": "true|false"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.2"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi = 4, 5
    else:
        h_lo, h_hi = 2, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    max_n = min(h * w, 9, 30 // max(h, w))
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", 2, max(2, max_n))))
    n_colors = max(2, min(max_n, n_colors))
    palette = list(ctx.draw_distinct_colors("palette", n=n_colors, exclude={0}))
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, palette, rng)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0:
        g = apply_noise_overlay(g, palette, rng, no)
    balance = overrides.get("color_balance",
                            ctx.draw_choice("color_balance", ["even", "skewed"]))
    if balance == "even":
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        for i in range(min(n_colors, len(cells))):
            r, c = cells[i]
            g[r][c] = palette[i]
    if bool(overrides.get("anchor_origin", False)):
        g[0][0] = palette[0]
    if bool(overrides.get("asymmetry_force", False)) and len(palette) > 1:
        if _is_lr_sym(g):
            g[0][0] = palette[1]
    cells_present = {v for row in g for v in row}
    if 0 in cells_present:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    g[r][c] = palette[0]
    for color in palette:
        if color not in cells_present:
            empty = [(r, c) for r in range(h) for c in range(w)
                     if not _color_required(g, r, c, palette)]
            if empty:
                r, c = rng.choice(empty)
                g[r][c] = color
            else:
                g[h - 1][w - 1] = color
    distinct_now = len({v for row in g for v in row})
    if distinct_now != n_colors:
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        idx = 0
        for color in palette:
            if idx < len(cells):
                r, c = cells[idx]
                g[r][c] = color
                idx += 1
    return g


def _color_required(g, r, c, palette):
    counts = {p: 0 for p in palette}
    for rr in range(len(g)):
        for cc in range(len(g[0])):
            if g[rr][cc] in counts:
                counts[g[rr][cc]] += 1
    return counts.get(g[r][c], 0) <= 1


def _is_lr_sym(g):
    h, w = len(g), len(g[0])
    return all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, rng):
    palette = list(range(1, 10))
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
    if name == "single_color_dominates":
        c1 = palette[0]
        c2 = palette[1]
        g = full_grid(h, w, c1)
        g[0][0] = c2
        return g
    return [[1] * w for _ in range(h)]
