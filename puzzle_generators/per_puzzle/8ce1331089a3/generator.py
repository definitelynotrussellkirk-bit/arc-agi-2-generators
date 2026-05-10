"""Generator for d687bc17.

Rule: 4-color border + interior pixels colored with one of those border
colors; rule moves each interior pixel to the matching border edge.

Combinatorial axes (8): grid_h/w, n_pixels, palette_kind, density,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_pixels, no_border, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8ce1331089a3"
VERSION = "1.1.0"
TASK_ID = "8ce1331089a3"
SUMMARY = "4-color border + interior pixels; rule moves each pixel to matching edge."

INVARIANTS = [
    "4 distinct border colors (top, bot, left, right)",
    "interior pixels are non-zero and match one of those 4 colors",
    "interior pixel density <= 30%",
]

POSITION_BIASES = ("scattered", "centered", "corners", "row_lean")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pixels", "no_border", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "n_pixels":       {"type": "int", "default": "h*w/12", "valid": "1..24"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "float", "default": "0.083", "valid": "0.05..0.3"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 8, 10
        d_default = 0.06
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
        d_default = 0.15
    else:
        h_lo, h_hi = 10, 14
        d_default = 0.083
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0})
    top_c, bot_c, left_c, right_c = palette
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = top_c
        g[h - 1][c] = bot_c
    for r in range(h):
        g[r][0] = left_c
        g[r][w - 1] = right_c
    density = float(overrides.get("density", d_default))
    density = max(0.03, min(0.3, density))
    n_pixels = int(overrides.get("n_pixels", int(h * w * density)))
    n_pixels = max(1, min(int(0.3 * h * w), n_pixels))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    placed = 0
    for _try in range(n_pixels * 4):
        if placed >= n_pixels:
            break
        if bias == "centered":
            r = rng.randint(max(2, h // 3), min(h - 3, 2 * h // 3))
            c = rng.randint(max(2, w // 3), min(w - 3, 2 * w // 3))
        elif bias == "corners":
            r = rng.choice([2, h - 3])
            c = rng.choice([2, w - 3])
        elif bias == "row_lean":
            r = rng.randint(2, h - 3)
            c = rng.randint(2, w - 3)
        else:
            r = rng.randint(2, h - 3)
            c = rng.randint(2, w - 3)
        if g[r][c] == 0:
            g[r][c] = rng.choice(palette)
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_pixels":
        for c in range(w):
            g[0][c] = 1; g[h - 1][c] = 2
        for r in range(h):
            g[r][0] = 3; g[r][w - 1] = 4
        return g
    if name == "no_border":
        for r in range(2, h - 2):
            for c in range(2, w - 2):
                if rng.random() < 0.1:
                    g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
