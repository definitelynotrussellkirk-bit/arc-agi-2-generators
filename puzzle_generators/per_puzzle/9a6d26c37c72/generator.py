"""Generator for ARC task be03b35f.

Rule: `(rule! (lambda (g) (crop (rotate-cw g) 0 0 (- (quotient (rows g) 2) 1) (- (quotient (cols g) 2) 1))))`.
Rotate the grid 90° clockwise, then crop the top-left quadrant
(approximately h/2 × w/2 of the rotated grid).

Combinatorial axes:
  * side                 — odd square side (rule expects square input)
  * texture              — pattern: noise/sparse/blob/stripes/checker/...
  * palette_size         — distinct fg colors
  * fill_density         — coverage
  * cropped_kind         — what the rotated top-left quadrant looks like:
                            mixed / two_colors / palette
  * caller-opt-in degenerates: monochrome, single_pixel, all_bg
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "9a6d26c37c72"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "9a6d26c37c72"
SUMMARY = "An odd square grid; the rule rotates 90° CW and crops the top-left quadrant."

INVARIANTS = [
    "input is an odd square (side ∈ {5, 7, 9, 11, 13})",
    "background is 0",
    "≥2 fg colors so the cropped+rotated output has variety",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "single_pixel", "all_bg")

AXES = {
    "side":          {"type": "choice", "default": "rng odd 5..13",
                      "valid": "5|7|9|11|13"},
    "texture":       {"type": "str",    "default": "rng helpful",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "palette_size":  {"type": "int",    "default": "rng 2..5", "valid": "1..9"},
    "fill_density":  {"type": "float",  "default": "rng 0.3..0.7", "valid": "0.1..1.0"},
    "noise_overlay": {"type": "float",  "default": "rng 0..0.05", "valid": "0..0.3"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        side_choices = [5, 7]
    elif difficulty == "hard":
        side_choices = [11, 13]
    else:
        side_choices = [5, 7, 9, 11, 13]

    side = ctx.draw_choice("side", side_choices)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], side, rng)

    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 5)))
    palette = ctx.draw_distinct_colors("palette", n=n_palette, exclude={0})
    full_palette = [0, *palette]

    texture = overrides.get(
        "texture",
        ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, side, side, full_palette, rng)

    fill_d = float(overrides.get(
        "fill_density",
        ctx.draw_rng("fill_density").uniform(0.3, 0.7)))
    if fill_d < 1.0:
        g = apply_bg_density(g, full_palette, rng, 1.0 - fill_d)
    no = float(overrides.get(
        "noise_overlay",
        ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, full_palette, rng, no)

    if len({v for row in g for v in row}) < 2:
        g[0][side - 1] = palette[0]
        g[side - 1][0] = palette[-1]
    return g


def _draw_from_degenerate(name, side, rng):
    """Edge-case where the rotate+crop signal is hidden.

    monochrome   — uniform input → uniform output of half-size.
    single_pixel — one fg pixel; the rotated/cropped output may be
                    blank or one-pixel depending on placement.
    all_bg       — entirely bg; output is all bg of half-size.
    """
    g = full_grid(side, side, 0)
    palette = list(range(1, 10))
    rng.shuffle(palette)
    if name == "monochrome":
        c = palette[0]
        for r in range(side):
            for cc in range(side):
                g[r][cc] = c
        return g
    if name == "single_pixel":
        rr = rng.randint(0, side - 1); rc = rng.randint(0, side - 1)
        g[rr][rc] = palette[0]
        return g
    if name == "all_bg":
        return g
    return g
