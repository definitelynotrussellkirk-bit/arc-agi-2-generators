"""Generator for ARC task 67a3c6ac.

Rule: `(rule! flip-lr)`.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay, apply_border,
)

GENERATOR_ID = "c690e739e0ce"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "c690e739e0ce"
SUMMARY = "Random multicolor grid; the rule mirrors every row left-to-right."

INVARIANTS = [
    "input is a rectangular grid with at least two columns",
    "at least one row is horizontally asymmetric so the flip is visible",
    "colors are sampled from a small palette",
]

# Default sampling: a HELPFUL texture (rule's effect is visible — output != input).
# Caller can opt into a degenerate (output == input) via texture override; cap at
# at most one such call per multi-pair puzzle (otherwise rule becomes ambiguous).
#
# All 9 cell-fill textures from helpers.textures apply: flip-lr is rule-agnostic
# wrt cell content (it works on any grid), so each texture exposes a different
# aspect of the rule (gradient → axis-direction reveal; frame → frame preserved
# under flip; checkerboard → still checker after flip; etc.).
HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("lr_symmetric",)

AXES = {
    "grid_h":       {"type": "int",   "default": "rng 2..20", "valid": "2..30"},
    "grid_w":       {"type": "int",   "default": "rng 2..20", "valid": "2..30"},
    "palette_size": {"type": "int",   "default": "rng 2..9",  "valid": "2..10"},
    "texture":      {"type": "str",   "default": "rng helpful",
                     "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":   {"type": "float", "default": "rng 0..0.5",
                     "valid": "0.0..0.95 (post-texture bg-resample fraction)"},
    "noise_overlay": {"type": "float", "default": "rng 0..0.10",
                      "valid": "0..0.5 (random per-cell perturbation)"},
    "border_mode":  {"type": "str",   "default": "rng free|always_bg|always_fg",
                     "valid": "free|always_bg|always_fg"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    # Difficulty-aware narrowing; widen draw ranges otherwise.
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 6, 2, 6, 2, 4
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 10, 20, 10, 20, 5, 9
    else:
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 20, 2, 20, 2, 9

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors)
    rng = ctx.draw_rng("cells")

    # Degenerate path: caller-opt-in.
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)

    # Helpful path: pick texture (overridable), then optional modifiers.
    if "texture" in overrides:
        texture = overrides["texture"]
    else:
        texture = ctx.draw_choice("texture", list(HELPFUL_TEXTURES))
    g = fill_texture(texture, h, w, palette, rng)

    # bg_density: post-texture bg-resampling. Pulls more cells toward bg,
    # producing sparser variants of any base texture.
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.5)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)

    # noise_overlay: perturb a small fraction of cells with random colors.
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.10)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)

    # border_mode: optionally force border cells to a uniform color regime.
    bm = overrides.get(
        "border_mode",
        ctx.draw_choice("border_mode", ["free", "free", "free", "always_bg", "always_fg"]),
    )
    g = apply_border(g, palette, rng, bm)

    # Invariant: the flip must be visible — break exact lr-symmetry if the
    # texture+modifiers happened to produce a palindromic grid.
    if all(row == list(reversed(row)) for row in g):
        g[0][0] = palette[0]
        g[0][-1] = palette[1] if len(palette) > 1 else palette[0]
    return g


def _draw_from_degenerate(name, h, w, palette, rng):
    """Build an edge-case input where the rule's effect is hidden.

    Caller is responsible for capping at most one degenerate per
    multi-pair puzzle (more than one and the rule becomes unrecoverable
    from demonstrations).

    lr_symmetric — every row is a palindrome, so flip-lr leaves the grid
                   unchanged (output == input). Forces the model to
                   verify the rule rather than pattern-match.
    """
    g = full_grid(h, w, palette[0])
    if name == "lr_symmetric":
        # Build each row as a palindrome by sampling the left half and
        # mirroring onto the right.
        half = (w + 1) // 2
        for r in range(h):
            for c in range(half):
                color = rng.choice(palette)
                g[r][c] = color
                g[r][w - 1 - c] = color
        return g
    # Unknown name → fallback to noise.
    for r in range(h):
        for c in range(w):
            g[r][c] = rng.choice(palette)
    return g
