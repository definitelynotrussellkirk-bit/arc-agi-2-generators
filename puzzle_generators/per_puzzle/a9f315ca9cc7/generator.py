"""Generator for ARC task 007bbfb7.

Rule: `(rule! (lambda (g) (self-tile g)))`
  Result is a (3h × 3w) tiling where each cell of the input determines
  whether the tile at that position is a copy of the input (non-zero) or
  blank (zero).

Invariants:
  - Input is small (3x3 to 5x5) — self-tile produces 9x to 25x cells.
  - At least one non-zero cell (else output would be all zeros, degenerate).
  - At least one zero cell (else self-tile produces a uniform grid).

Free axes — see AXES below.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "a9f315ca9cc7"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "a9f315ca9cc7"

SUMMARY = "Small grid with mixed bg/non-bg cells; self-tile triples its dimensions."

INVARIANTS = [
    "input dims in [3, 9] x [3, 9] so the 3×-tiled output stays within 30×30",
    "at least one zero cell (else output is uniform)",
    "at least one non-zero cell (else output is all-zero)",
    "non-zero cells share one color (typical ARC self-tile presentation)",
]

# All 9 helpful textures apply. self-tile is a structural rule that uses
# the bg/fg pattern of cells regardless of color identity, so any texture
# (sparse, blob, checkerboard, plus, frame, etc.) gives a different
# tiling-of-the-input output to learn from.
HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("dense_fg", "single_fg")

AXES = {
    "grid_h":      {"type": "int",   "default": "rng 3..9",  "valid": "3..9"},
    "grid_w":      {"type": "int",   "default": "rng 3..9",  "valid": "3..9"},
    "fg_color":    {"type": "color", "default": "rng",       "valid": "1..9"},
    "fill_ratio":  {"type": "float", "default": "rng 0.20..0.80",
                    "valid": "0.05..0.95 (fraction of cells that are fg)"},
    "texture":     {"type": "str", "default": "rng helpful",
                    "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":  {"type": "float", "default": "rng 0..0.4",  "valid": "0..0.95"},
    "noise_overlay": {"type": "float", "default": "rng 0..0.05", "valid": "0..0.5"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        s_lo, s_hi = 3, 4
    elif difficulty == "hard":
        s_lo, s_hi = 6, 9
    else:
        s_lo, s_hi = 3, 9

    h = ctx.draw_int("grid_h", s_lo, s_hi)
    w = ctx.draw_int("grid_w", s_lo, s_hi)
    fg = ctx.draw_color("fg_color", exclude={0})
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, fg, rng)

    # Choose texture; on small self-tile grids any texture is meaningful.
    if "texture" in overrides:
        texture = overrides["texture"]
    else:
        texture = ctx.draw_choice("texture", list(HELPFUL_TEXTURES))

    # Build the grid using the texture (palette = [bg=0, fg]).
    palette = [0, fg]
    g = fill_texture(texture, h, w, palette, rng)

    # bg_density / noise_overlay biases.
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)

    # Invariant: at least one fg AND at least one bg cell (else self-tile output is uniform).
    flat = [v for row in g for v in row]
    if all(v == 0 for v in flat):
        g[0][0] = fg
    elif all(v != 0 for v in flat):
        g[h - 1][w - 1] = 0
    return g


def _draw_from_degenerate(name, h, w, fg, rng):
    """Edge-case input where the self-tile signature is hidden.

    dense_fg  — almost every cell is fg, so output is mostly a uniform
                fg grid with one or two zero tiles. The "tiling" structure
                isn't visible from one example.
    single_fg — exactly one fg cell. Output places a tiny tile somewhere;
                visually subtle, easy to mistake for upscale or paste.
    """
    g = full_grid(h, w, 0)
    if name == "dense_fg":
        # All-fg except one cell.
        for r in range(h):
            for c in range(w):
                g[r][c] = fg
        bg_r = rng.randrange(h)
        bg_c = rng.randrange(w)
        g[bg_r][bg_c] = 0
        return g
    if name == "single_fg":
        rr = rng.randrange(h)
        rc = rng.randrange(w)
        g[rr][rc] = fg
        return g
    return g
