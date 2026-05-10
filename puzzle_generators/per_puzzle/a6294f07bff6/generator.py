"""Generator for ARC task 68b16354.

Rule: `(rule! flip-ud)`.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay, apply_border,
)

GENERATOR_ID = "a6294f07bff6"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "a6294f07bff6"
SUMMARY = "Random multicolor grid; the rule mirrors row order top-to-bottom."

INVARIANTS = [
    "input is a rectangular grid with at least two rows",
    "top and bottom rows differ so the vertical flip is visible",
    "colors are sampled from a small palette",
]

# All 9 helpful textures apply (flip-ud is rule-agnostic wrt content).
# Each exposes a different aspect: gradient → axis-direction visible;
# frame → frame preserved; checkerboard → still checker; etc.
HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("ud_symmetric",)

AXES = {
    "grid_h":       {"type": "int",   "default": "rng 2..20", "valid": "2..30"},
    "grid_w":       {"type": "int",   "default": "rng 1..20", "valid": "1..30"},
    "palette_size": {"type": "int",   "default": "rng 2..9",  "valid": "2..10"},
    "texture":      {"type": "str",   "default": "rng helpful",
                     "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":   {"type": "float", "default": "rng 0..0.5",  "valid": "0..0.95"},
    "noise_overlay": {"type": "float", "default": "rng 0..0.10", "valid": "0..0.5"},
    "border_mode":  {"type": "str",   "default": "rng free|always_bg|always_fg",
                     "valid": "free|always_bg|always_fg"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 6, 1, 6, 2, 4
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 10, 20, 8, 20, 5, 9
    else:
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 20, 1, 20, 2, 9

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)

    if "texture" in overrides:
        texture = overrides["texture"]
    else:
        texture = ctx.draw_choice("texture", list(HELPFUL_TEXTURES))
    g = fill_texture(texture, h, w, palette, rng)

    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.5)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.10)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)
    bm = overrides.get(
        "border_mode",
        ctx.draw_choice("border_mode", ["free", "free", "free", "always_bg", "always_fg"]),
    )
    g = apply_border(g, palette, rng, bm)

    # Invariant: top and bottom rows must differ so the flip is visible.
    if g[0] == g[-1]:
        g[0][0] = palette[0]
        g[-1][0] = palette[1] if len(palette) > 1 else palette[0]
    return g


def _draw_from_degenerate(name, h, w, palette, rng):
    """Edge-case input where the rule's effect is hidden.

    ud_symmetric — every column is a palindrome top-to-bottom, so flip-ud
                   leaves the grid unchanged (output == input).
    """
    g = full_grid(h, w, palette[0])
    if name == "ud_symmetric":
        half = (h + 1) // 2
        for r in range(half):
            row = [rng.choice(palette) for _ in range(w)]
            g[r] = list(row)
            g[h - 1 - r] = list(row)
        return g
    for r in range(h):
        for c in range(w):
            g[r][c] = rng.choice(palette)
    return g
