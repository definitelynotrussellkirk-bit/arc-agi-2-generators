"""Generator for ARC task ccd554ac.

Rule: `(rule! (lambda (g) (let* ((n (rows g))) (build-grid (* n n) (* n n) (r c) (at g (mod r n) (mod c n))))))`.
For an n × n input, output is n² × n² where each (r, c) = input[r mod n][c mod n].
i.e., tile the input into an n × n grid of itself.

Combinatorial axes:
  * side                — square side (n must satisfy n² ≤ 30)
  * texture             — pattern of input cells: noise/sparse/blob/checker/...
  * fg_color            — main fg color (canonical: one fg color, but
                          axis lets palette_size > 1)
  * palette_size        — distinct fg colors (1..3)
  * fill_density        — fraction of cells that take fg
  * caller-opt-in degenerates: monochrome (output uniform),
                               single_pixel (output is one fg cell on
                               vast bg), all_bg
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "fcac68386147"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "fcac68386147"
SUMMARY = "Small square grid with a foreground pattern; rule tiles it n × n into n² × n² output."

INVARIANTS = [
    "input is a square of side n in {2, 3, 4, 5} (so n² ≤ 25)",
    "≥1 fg cell so the tiled output is not all-bg",
    "palette uses fg colors (canonical bg is 0)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "single_pixel", "all_bg")

AXES = {
    "side":          {"type": "int",   "default": "rng 2..5", "valid": "2..5"},
    "texture":       {"type": "str",   "default": "rng helpful",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "palette_size":  {"type": "int",   "default": "rng 1..3", "valid": "1..5"},
    "fill_density":  {"type": "float", "default": "rng 0.3..0.7", "valid": "0.1..1.0"},
    "noise_overlay": {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        side_choices = [2, 3]
    elif difficulty == "hard":
        side_choices = [4, 5]
    else:
        side_choices = [2, 3, 4, 5]

    n = ctx.draw_choice("side", side_choices)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, rng)

    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 1, 3)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0}))
    full_palette = [0, *palette]

    texture = overrides.get(
        "texture",
        ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, n, n, full_palette, rng)

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

    # Pin a fg cell so output is not all-bg.
    if all(g[r][c] == 0 for r in range(n) for c in range(n)):
        g[0][0] = palette[0]
    return g


def _draw_from_degenerate(name, n, rng):
    """Edge-case where the self-tile signal is hidden.

    monochrome    — uniform fg input → uniform fg n²×n² output;
                     ambiguous with "fill with X."
    single_pixel  — one fg cell; output has just n² evenly-spaced fg
                     pixels — looks like "stamp at grid points."
    all_bg        — all-bg input; output is all-bg of n²×n² (rule no-op).
    """
    palette = list(range(1, 10))
    rng.shuffle(palette)
    g = full_grid(n, n, 0)
    if name == "monochrome":
        for r in range(n):
            for c in range(n):
                g[r][c] = palette[0]
        return g
    if name == "single_pixel":
        rr = rng.randint(0, n - 1); rc = rng.randint(0, n - 1)
        g[rr][rc] = palette[0]
        return g
    if name == "all_bg":
        return g
    return g
