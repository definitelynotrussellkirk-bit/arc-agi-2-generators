"""Generator for ARC task ed36ccf7.

Rule: `(rule! rotate-ccw)`.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay, apply_border,
)

GENERATOR_ID = "864eaaac6503"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "864eaaac6503"
SUMMARY = "Random compact grid; the rule rotates it 90 degrees counterclockwise."

INVARIANTS = [
    "input is a rectangular grid",
    "at least two colors appear",
    "grid size is kept small enough that rotation output remains compact",
]

# All 9 helpful textures apply. rotate-ccw is rule-agnostic wrt content;
# different textures expose different aspects of the 90° rotation
# (gradient direction, frame preservation, etc.).
HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("rot4_symmetric",)

AXES = {
    "grid_h":       {"type": "int",   "default": "rng 2..18", "valid": "2..30"},
    "grid_w":       {"type": "int",   "default": "rng 2..18", "valid": "2..30"},
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
        lo, hi, c_lo, c_hi = 2, 6, 2, 4
    elif difficulty == "hard":
        lo, hi, c_lo, c_hi = 10, 18, 5, 9
    else:
        lo, hi, c_lo, c_hi = 2, 18, 2, 9

    h = ctx.draw_int("grid_h", lo, hi)
    w = ctx.draw_int("grid_w", lo, hi)
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

    # Invariant: at least two colors must appear so the rotation is visible.
    if len({v for row in g for v in row}) == 1:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else palette[0]
    return g


def _draw_from_degenerate(name, h, w, palette, rng):
    """Edge-case input where the rule's effect is hidden.

    rot4_symmetric — square grid invariant under 90° rotation, so output
                     equals input. Forces the model to verify that
                     rotate-ccw is actually applied rather than to assume
                     identity.
    """
    g = full_grid(h, w, palette[0])
    if name == "rot4_symmetric":
        # Need square grid to support 90° rotational symmetry.
        n = min(h, w)
        # Pick colors for one quadrant of an n×n grid; mirror under 4 rotations.
        for r in range((n + 1) // 2):
            for c in range((n + 1) // 2):
                color = rng.choice(palette)
                # Place into all 4 rotated positions.
                positions = {(r, c), (c, n - 1 - r),
                             (n - 1 - r, n - 1 - c), (n - 1 - c, r)}
                for rr, cc in positions:
                    if 0 <= rr < n and 0 <= cc < n:
                        g[rr][cc] = color
        return g
    for r in range(h):
        for c in range(w):
            g[r][c] = rng.choice(palette)
    return g
