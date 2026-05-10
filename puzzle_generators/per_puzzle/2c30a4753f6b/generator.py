"""Generator for puzzle c9e6f938.

Rule: `(rule! (lambda (g) (build-grid h (* 2 w) (r c) (if (< c w) (at g r c) (at g r (- (- (* 2 w) 1) c))))))`.
Output is h × 2w: left half is the input, right half is the input
flipped horizontally. (Mirror-stack horizontally.)

Combinatorial axes:
  * grid_h / grid_w     — input dims (output is h × 2w; must stay ≤ 30)
  * texture             — pattern: noise/sparse/blob/stripes/...
  * palette_size        — distinct colors
  * lr_asymmetric       — ensure input differs LR (else mirror is invisible)
  * caller-opt-in degenerates: monochrome, lr_symmetric (flip invisible),
                               single_col
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "2c30a4753f6b"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "2c30a4753f6b"
SUMMARY = "Any colored grid; rule outputs input + horizontal mirror side-by-side (h × 2w)."

INVARIANTS = [
    "2 × w ≤ 30 so output fits within ARC limits",
    "≥2 distinct colors so the mirror is visible",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "lr_symmetric", "single_col")

AXES = {
    "grid_h":         {"type": "int",   "default": "rng 2..15", "valid": "1..15"},
    "grid_w":         {"type": "int",   "default": "rng 2..12", "valid": "1..15"},
    "palette_size":   {"type": "int",   "default": "rng 2..6",  "valid": "1..10"},
    "texture":        {"type": "str",   "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "lr_asymmetric":  {"type": "bool",  "default": "true",      "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 5, 2, 5, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 12, 15, 9, 12, 5, 8
    else:
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 15, 2, 12, 2, 6

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
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
        ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get(
        "noise_overlay",
        ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)

    if bool(overrides.get("lr_asymmetric", True)) and _is_lr_symmetric(g):
        g[0][0] = palette[1] if len(palette) > 1 else (g[0][0] + 1) % 10

    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _is_lr_symmetric(g):
    h = len(g); w = len(g[0])
    return all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    """Edge-case where the mirror-stack signal is hidden.

    monochrome     — uniform input → uniform 2 × wider output (looks
                      like horizontal stretch).
    lr_symmetric   — input already mirrors LR; the flipped half looks
                      identical → output looks like "duplicate horizontally."
    single_col     — w=1; output is h × 2 with two identical columns.
    """
    g = full_grid(h, w, palette[0])
    if name == "monochrome":
        color = rng.choice(palette)
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "lr_symmetric":
        for r in range(h):
            for c in range(w // 2):
                v = rng.choice(palette)
                g[r][c] = v
                g[r][w - 1 - c] = v
        return g
    if name == "single_col":
        for r in range(h):
            v = rng.choice(palette)
            for c in range(w):
                g[r][c] = v
        return g
    return g
