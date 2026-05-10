"""Generator for puzzle 60c09cac — `(rule! (upscale g 2))`. Every cell
becomes a 2x2 block.

Concept membership: 2 puzzles share this rule.

Invariants:
  - input dims <=15 (so output stays within 30x30)
  - >=2 distinct colors (so the upscale produces a non-uniform output)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "0d6d64e90301"
VERSION = "1.1.0"
TASK_ID = "0d6d64e90301"
SUMMARY = "Small grid with mixed colors; rule upscales 2x to a larger grid."

INVARIANTS = [
    "input dims <= 15 (so 2x output is <= 30 — still ARC-legal)",
    ">=2 distinct colors in the input",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("tiny_grid", "monochrome")

AXES = {
    "grid_h":     {"type": "int",   "default": "rng 2..15", "valid": "2..15"},
    "grid_w":     {"type": "int",   "default": "rng 2..15", "valid": "2..15"},
    "fg_palette": {"type": "int",   "default": "rng 2..9",  "valid": "1..9"},
    "fill_ratio": {"type": "float", "default": "rng 0.2..0.9", "valid": "0.1..0.9"},
    "texture":    {"type": "str", "default": "rng helpful",
                   "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density": {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay": {"type": "float", "default": "rng 0..0.05", "valid": "0..0.5"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        lo, hi, p_lo, p_hi = 3, 6, 2, 3
    elif difficulty == "hard":
        lo, hi, p_lo, p_hi = 10, 15, 5, 9
    else:
        lo, hi, p_lo, p_hi = 2, 15, 2, 9

    h = ctx.draw_int("grid_h", lo, hi)
    w = ctx.draw_int("grid_w", lo, hi)
    palette_n = ctx.draw_int("fg_palette", p_lo, p_hi)
    palette = ctx.draw_distinct_colors("palette", n=palette_n, exclude={0})
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)

    if "texture" in overrides:
        texture = overrides["texture"]
    else:
        texture = ctx.draw_choice("texture", list(HELPFUL_TEXTURES))
    # palette[0] is one of the drawn fg colors; treat it as bg for textures.
    full_palette = [0, *palette]
    g = fill_texture(texture, h, w, full_palette, rng)

    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0.0:
        g = apply_bg_density(g, full_palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, full_palette, rng, no)

    # Invariant: ≥2 distinct colors visible (else upscale produces uniform).
    distinct = {v for row in g for v in row}
    if len(distinct) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else palette[0]
    return g


def _draw_from_degenerate(name, h, w, palette, rng):
    """Edge-case input where the upscale signature is hidden.

    tiny_grid  — 1×1 or 2×2 input; the 2x upscale signature is hard to
                 distinguish from "paste twice" or "paint a small block."
    monochrome — every fg cell shares one color; output looks like a
                 single-color block, less informative about the rule.
    """
    if name == "tiny_grid":
        # Force minimum size; the rule's effect is unambiguous but visually subtle.
        g = full_grid(2, 2, 0)
        g[0][0] = rng.choice(palette)
        g[1][1] = rng.choice(palette)
        return g
    if name == "monochrome":
        color = rng.choice(palette)
        g = full_grid(h, w, 0)
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = color
        # Ensure at least one cell is fg (else degenerate-degenerate).
        if all(g[r][c] == 0 for r in range(h) for c in range(w)):
            g[0][0] = color
        return g
    return full_grid(h, w, 0)
