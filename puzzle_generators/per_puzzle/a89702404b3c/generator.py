"""Generator for ARC task a6953f00.

Rule: if w is even → output is g[0:1, w-2:w] (top-right 1×2); else →
output is g[0:1, 0:1] (top-left 1×1). Effectively width-parity selects
the corner-crop position.

Combinatorial axes: side, parity (even or odd), texture, palette_size,
top-row decoration. Degenerates: monochrome, sides_match (both corners
look identical), single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "a89702404b3c"
VERSION = "1.1.0"
TASK_ID = "a89702404b3c"
SUMMARY = "Square grid; even widths crop top-right 1×2, odd widths crop top-left 1×1."

INVARIANTS = [
    "input is at least 3 × 3",
    "the relevant top-row corner is meaningful (top-right for even, top-left for odd)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "sides_match", "single_pixel")

AXES = {
    "side":           {"type": "int", "default": "rng 3..15", "valid": "3..18"},
    "parity":         {"type": "str", "default": "rng even|odd", "valid": "even|odd|any"},
    "palette_size":   {"type": "int", "default": "rng 3..7", "valid": "2..10"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        s_lo, s_hi = 3, 6
    elif difficulty == "hard":
        s_lo, s_hi = 11, 15
    else:
        s_lo, s_hi = 3, 15
    n = ctx.draw_int("side", s_lo, s_hi)
    parity = overrides.get("parity",
                           ctx.draw_choice("parity", ["even", "odd", "any"]))
    if parity == "even" and n % 2 != 0:
        n = max(4, n + 1)
    elif parity == "odd" and n % 2 == 0:
        n = max(3, n - 1)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, rng)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 3, 7)))
    palette = list(ctx.draw_distinct_colors("palette", n=n_palette))
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, n, n, palette, rng)
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    return g


def _draw_from_degenerate(name, n, rng):
    palette = list(range(0, 10))
    rng.shuffle(palette)
    g = full_grid(n, n, palette[0])
    if name == "monochrome":
        c0 = palette[0]
        for r in range(n):
            for c in range(n):
                g[r][c] = c0
        return g
    if name == "sides_match":
        # Make top-left 1×1 and top-right 1×2 identical so output is ambiguous.
        c0 = palette[1]
        g[0][0] = c0
        g[0][n - 2] = c0
        g[0][n - 1] = c0
        for r in range(n):
            for c in range(n):
                if g[r][c] == 0:
                    g[r][c] = palette[0]
        return g
    if name == "single_pixel":
        rr = rng.randint(0, n - 1); rc = rng.randint(0, n - 1)
        g[rr][rc] = palette[1] if len(palette) > 1 else palette[0]
        return g
    return g
