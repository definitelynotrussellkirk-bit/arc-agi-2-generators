"""Generator for puzzle 3c9b0459 — `(rule! (flip-ud (flip-lr g)))`,
i.e. a 180° rotation.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * palette_size        — number of distinct fg colors
  * texture             — pattern type (noise/sparse/blob/stripes/gradient/...)
  * bg_density          — bias toward more / fewer bg cells
  * noise_overlay       — perturb a few cells after the texture is laid
  * caller-opt-in degenerates: rot180_symmetric, single_cell

Most textures already produce a 180°-asymmetric grid; we keep an
asymmetry guarantee so the rule's effect is visible.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "0a855288946a"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "0a855288946a"
SUMMARY = "Asymmetric input; rule rotates 180° (flip-lr then flip-ud)."

INVARIANTS = [
    "grid is not 180°-symmetric (else output equals input — runner rejects)",
    "≥2 non-bg cells",
    "grid dims ≤ 30 (ARC limit)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("rot180_symmetric", "single_cell")

AXES = {
    "grid_h":         {"type": "int",   "default": "rng 5..14",  "valid": "3..18"},
    "grid_w":         {"type": "int",   "default": "rng 5..14",  "valid": "3..18"},
    "palette_size":   {"type": "int",   "default": "rng 2..6",   "valid": "2..9"},
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
        h_lo, h_hi, c_lo, c_hi = 5, 8, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, c_lo, c_hi = 11, 14, 4, 6
    else:
        h_lo, h_hi, c_lo, c_hi = 5, 14, 2, 6

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

    # Force 180°-asymmetry so the rule has visible effect. If the texture
    # came back symmetric, perturb one off-center cell.
    if _is_rot180_symmetric(g):
        g[0][0] = (g[0][0] + 1) % 10
        if _is_rot180_symmetric(g):
            g[0][1 if w > 1 else 0] = (g[0][1 if w > 1 else 0] + 1) % 10
    return g


def _is_rot180_symmetric(g):
    h, w = len(g), len(g[0])
    return all(g[r][c] == g[h - 1 - r][w - 1 - c]
               for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    """Edge-case input where the 180° rotation is hidden.

    rot180_symmetric — input already equals its 180° rotation, so output
                       equals input; the rule is invisible.
    single_cell      — only one non-bg cell; visually the rotation is
                       just "the dot moved" with no other reference.
    """
    g = full_grid(h, w, palette[0])
    if name == "rot180_symmetric":
        # Stamp pairs of cells symmetric across the center.
        for _ in range(rng.randint(2, 5)):
            r = rng.randint(0, h - 1)
            c = rng.randint(0, w - 1)
            color = rng.choice(palette[1:]) if len(palette) > 1 else palette[0]
            g[r][c] = color
            g[h - 1 - r][w - 1 - c] = color
        return g
    if name == "single_cell":
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        # Keep it off-center so rotation is visible.
        if r == h - 1 - r and c == w - 1 - c:
            r = max(0, r - 1)
        g[r][c] = palette[1] if len(palette) > 1 else palette[0]
        return g
    return g
