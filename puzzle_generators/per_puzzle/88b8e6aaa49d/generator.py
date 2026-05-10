"""Generator for ARC task 6150a2bd: 180° rotation (`(flip-ud (flip-lr g))`).

Same concept as 3c9b0459 but a separate ARC task with a smaller / denser
input regime; we keep both generators independent so each task contributes
its own slice of input variety.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size (smaller bias than 3c9b0459)
  * palette_size        — number of distinct fg colors
  * texture             — pattern type (noise/sparse/blob/stripes/gradient/...)
  * bg_density          — bias toward more / fewer bg cells
  * noise_overlay       — perturb a few cells after the texture is laid
  * caller-opt-in degenerates: rot180_symmetric, single_cell
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "88b8e6aaa49d"
VERSION = "1.1.0"
TASK_ID = "88b8e6aaa49d"
SUMMARY = "Compact multicolor grid; rule rotates 180° (flip-ud(flip-lr g))."

INVARIANTS = [
    "input is a small rectangular grid",
    "input is not 180°-symmetric (else output equals input)",
    "colors are sampled from a small palette",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("rot180_symmetric", "single_cell")

AXES = {
    "grid_h":         {"type": "int",   "default": "rng 3..7",   "valid": "2..15"},
    "grid_w":         {"type": "int",   "default": "rng 3..7",   "valid": "2..15"},
    "palette_size":   {"type": "int",   "default": "rng 2..6",   "valid": "2..10"},
    "texture":        {"type": "str",   "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.3", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, c_lo, c_hi = 3, 5, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi = 6, 9, 4, 6
    else:
        h_lo, h_hi, c_lo, c_hi = 3, 7, 2, 6

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors)
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)

    texture = overrides.get(
        "texture",
        ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, palette, rng)

    bg_d = float(overrides.get(
        "bg_density",
        ctx.draw_rng("bg_density").uniform(0.0, 0.3)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get(
        "noise_overlay",
        ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)

    if _is_rot180_symmetric(g):
        # Force asymmetry by toggling a corner.
        g[0][0] = palette[1] if len(palette) > 1 else (g[0][0] + 1) % 10
        if _is_rot180_symmetric(g) and (h, w) != (1, 1):
            g[h - 1][w - 1] = palette[0]
    return g


def _is_rot180_symmetric(g):
    h, w = len(g), len(g[0])
    return all(g[r][c] == g[h - 1 - r][w - 1 - c]
               for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    """Edge-case input where 180° rotation is hidden.

    rot180_symmetric — already symmetric so output == input.
    single_cell      — one non-bg cell; rotation looks like "move dot"
                       with no other reference.
    """
    g = full_grid(h, w, palette[0])
    if name == "rot180_symmetric":
        for _ in range(rng.randint(2, max(2, h * w // 4))):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            color = rng.choice(palette[1:]) if len(palette) > 1 else palette[0]
            g[r][c] = color
            g[h - 1 - r][w - 1 - c] = color
        return g
    if name == "single_cell":
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if r == h - 1 - r and c == w - 1 - c:
            r = max(0, r - 1)
        g[r][c] = palette[1] if len(palette) > 1 else palette[0]
        return g
    return g
