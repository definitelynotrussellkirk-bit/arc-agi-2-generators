"""Generator for ARC task 74dd1130.

Rule: `(rule! transpose)`.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay, apply_border,
)

GENERATOR_ID = "19a48004b265"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "19a48004b265"
SUMMARY = "Random multicolor grid; the rule swaps rows and columns."

INVARIANTS = [
    "input is a rectangular grid",
    "examples may be square or rectangular",
    "colors are sampled from a small palette",
]

# All 9 helpful textures apply. Transpose is rule-agnostic wrt content;
# different textures expose different aspects (gradient axis-swap,
# frame preserved, checkerboard preserved, plus inverted, etc.).
HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("transpose_symmetric",)

AXES = {
    "grid_h":       {"type": "int",   "default": "rng 2..18", "valid": "1..30"},
    "grid_w":       {"type": "int",   "default": "rng 2..18", "valid": "1..30"},
    "palette_size": {"type": "int",   "default": "rng 2..9",  "valid": "1..10"},
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
        h_lo, h_hi, c_lo, c_hi = 2, 6, 2, 4
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi = 10, 18, 5, 9
    else:
        h_lo, h_hi, c_lo, c_hi = 2, 18, 2, 9

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
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
    return g


def _draw_from_degenerate(name, h, w, palette, rng):
    """Build a degenerate (edge-case) input grid for the transpose rule.

    Caller opts in by passing `texture=<name>` and is responsible for
    capping at most one degenerate per multi-pair puzzle. More than one
    degenerate makes the rule unrecoverable from demonstrations.

    Currently supported names:
      transpose_symmetric  — input g satisfies transpose(g) == g, so
                             output equals input. Forces the model to
                             verify the rule rather than pattern-match.
    """
    g = full_grid(h, w, palette[0])
    if name == "transpose_symmetric":
        # Build a symmetric grid: g[r][c] = g[c][r].
        # Only meaningful when h == w (transpose-symmetric requires square).
        n = min(h, w)
        for r in range(n):
            for c in range(r, n):
                color = rng.choice(palette)
                g[r][c] = color
                if r != c:
                    g[c][r] = color
        return g
    # Unknown degenerate name → safe fallback to a noise grid.
    for r in range(h):
        for c in range(w):
            g[r][c] = rng.choice(palette)
    return g
