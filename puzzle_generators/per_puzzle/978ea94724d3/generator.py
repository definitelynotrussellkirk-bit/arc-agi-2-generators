"""Generator for puzzle a416b8f3.

Rule: `(rule! (lambda (g) (build-grid h (* 2 w) (r c) (at g r (mod c w)))))`.
Output is the input concatenated horizontally with itself (h × 2w).

Combinatorial axes:
  * grid_h / grid_w     — input dims (output is 2× wider, must stay ≤ 30)
  * texture             — pattern: noise/sparse/blob/stripes/checker/...
  * palette_size        — distinct fg colors
  * bg_color            — bg color
  * lr_asymmetric       — bool: ensure input differs LR (so the
                          duplication is visible — otherwise output looks
                          like a single tiling)
  * caller-opt-in degenerates: monochrome (uniform output),
                               horizontal_periodic (input already
                               repeats, so output looks like 4 copies),
                               single_cell
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "978ea94724d3"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "978ea94724d3"
SUMMARY = "Any colored grid; rule duplicates input horizontally (h × 2w)."

INVARIANTS = [
    "input dims ≤ (30, 15) so doubled output fits within ARC limits",
    "≥2 distinct colors so the duplication is visible",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("monochrome", "horizontal_periodic", "single_cell")

AXES = {
    "grid_h":         {"type": "int",   "default": "rng 2..15", "valid": "1..30"},
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

    # Force LR-asymmetry so the duplicate is visibly two copies.
    require_asym = bool(overrides.get("lr_asymmetric", True))
    if require_asym and _is_lr_symmetric(g):
        g[0][0] = palette[1] if len(palette) > 1 else (g[0][0] + 1) % 10

    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _is_lr_symmetric(g):
    h = len(g); w = len(g[0])
    return all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    """Edge-case where the duplicate-horizontally signal is hidden.

    monochrome          — uniform input → uniform 2 × wider output;
                          could be confused with "stretch."
    horizontal_periodic — input is already periodic in width N=w; output
                          looks like more of the same tiling.
    single_cell         — single fg pixel; output has two pixels at
                          (r, c) and (r, c + w) — minimal signal.
    """
    g = full_grid(h, w, palette[0])
    if name == "monochrome":
        color = rng.choice(palette)
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "horizontal_periodic":
        period = max(1, w // 2)
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[(c % period) % len(palette)]
        return g
    if name == "single_cell":
        rr = rng.randint(0, h - 1)
        rc = rng.randint(0, w - 1)
        g[rr][rc] = palette[1] if len(palette) > 1 else palette[0]
        return g
    return g
