"""Generator for ARC task 68b67ca3.

Rule: `(rule! (lambda (g) (downscale g 2)))`. The output keeps the cell
at every (2r, 2c) position; everything at odd r or odd c is dropped.

Combinatorial axes:
  * sample_h / sample_w     — output (downscaled) dims; input is 2× this
  * palette_size            — number of distinct fg colors
  * texture                 — pattern at the EVEN positions (the keepers)
  * odd_cell_mode           — what fills the odd positions (dropped by rule):
                              "all_bg" / "noise" / "decoy_pattern" /
                              "match_neighbor"
  * fill_density            — fraction of even positions that are non-bg
  * noise_overlay           — perturb a few even cells (rule still defined)
  * caller-opt-in degenerates: monochrome, tiny_grid
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "a3aafc2fb148"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "a3aafc2fb148"
SUMMARY = "Sparse even-row/even-column samples; the rule keeps every second cell."

INVARIANTS = [
    "input dimensions are even",
    "informative cells sit at even row and column coordinates",
    "odd rows and columns are dropped by the downscale; their content is decorative",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
ODD_MODES = ("all_bg", "noise", "decoy_pattern", "match_neighbor")
DEGENERATE_TEXTURES = ("monochrome", "tiny_grid")

AXES = {
    "sample_h":      {"type": "int", "default": "rng 2..8",  "valid": "1..15"},
    "sample_w":      {"type": "int", "default": "rng 2..8",  "valid": "1..15"},
    "palette_size":  {"type": "int", "default": "rng 2..6",  "valid": "2..9"},
    "texture":       {"type": "str", "default": "rng helpful",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "odd_cell_mode": {"type": "str", "default": "rng all_bg|noise|decoy_pattern|match_neighbor",
                      "valid": "|".join(ODD_MODES)},
    "fill_density":  {"type": "float", "default": "rng 0.45..0.95", "valid": "0.10..1.0"},
    "noise_overlay": {"type": "float", "default": "rng 0..0.05",    "valid": "0..0.2"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        s_lo, s_hi, p_lo, p_hi = 2, 4, 2, 3
    elif difficulty == "hard":
        s_lo, s_hi, p_lo, p_hi = 6, 8, 4, 6
    else:
        s_lo, s_hi, p_lo, p_hi = 2, 8, 2, 6

    sh = ctx.draw_int("sample_h", s_lo, s_hi)
    sw = ctx.draw_int("sample_w", s_lo, s_hi)
    n_colors = ctx.draw_int("palette_size", p_lo, p_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors, exclude={0})
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], sh, sw, palette, rng)

    # Build the inner (downscaled) image first so it has clean structure.
    full_palette = [0, *palette]
    if "texture" in overrides:
        texture = overrides["texture"]
    else:
        texture = ctx.draw_choice("texture", list(HELPFUL_TEXTURES))
    inner = fill_texture(texture, sh, sw, full_palette, rng)

    density = float(overrides.get(
        "fill_density",
        ctx.draw_rng("fill_density").uniform(0.45, 0.95)))
    # If density < 1.0, dropout some inner cells back to bg.
    if density < 1.0:
        for r in range(sh):
            for c in range(sw):
                if inner[r][c] != 0 and rng.random() > density:
                    inner[r][c] = 0

    no = float(overrides.get(
        "noise_overlay",
        ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        inner = apply_noise_overlay(inner, full_palette, rng, no)

    # Embed inner cells at (2r, 2c) of an enlarged 2sh × 2sw grid.
    h, w = sh * 2, sw * 2
    g = full_grid(h, w, 0)
    for r in range(sh):
        for c in range(sw):
            g[r * 2][c * 2] = inner[r][c]

    odd_mode = overrides.get(
        "odd_cell_mode",
        ctx.draw_choice("odd_cell_mode", list(ODD_MODES)))
    _fill_odd_cells(g, odd_mode, full_palette, rng)

    # Invariant: at least one non-bg cell at an even coordinate so the
    # downscaled output is not entirely bg.
    if all(g[r * 2][c * 2] == 0 for r in range(sh) for c in range(sw)):
        g[0][0] = palette[0]
    return g


def _fill_odd_cells(g, mode, palette, rng):
    """Decorate odd rows/cols. Whatever we put here is discarded by downscale."""
    h, w = len(g), len(g[0])
    if mode == "all_bg":
        return  # already bg from full_grid(0)
    for r in range(h):
        for c in range(w):
            if r % 2 == 0 and c % 2 == 0:
                continue  # protected even-cell content
            if mode == "noise":
                if rng.random() < 0.4:
                    g[r][c] = rng.choice(palette)
            elif mode == "decoy_pattern":
                # Solid color on odd rows OR odd cols — looks like real signal.
                if r % 2 == 1 or c % 2 == 1:
                    g[r][c] = palette[1] if len(palette) > 1 else palette[0]
            elif mode == "match_neighbor":
                # Copy the nearest even neighbor so the odd cells "extend"
                # the visible pattern (visually misleading).
                er = r - (r % 2)
                ec = c - (c % 2)
                g[r][c] = g[er][ec]


def _draw_from_degenerate(name, sh, sw, palette, rng):
    """Edge-case input where the downscale signature is hidden.

    monochrome — every even-cell is the same non-bg color, so the
                 downscaled output is a solid block — easy to confuse
                 with "fill with X" rules.
    tiny_grid  — sample dims 1×1: input is 2×2, output is 1×1; the
                 rule is technically applied but the demonstration is
                 visually trivial.
    """
    if name == "tiny_grid":
        g = full_grid(2, 2, 0)
        g[0][0] = rng.choice(palette)
        return g
    if name == "monochrome":
        color = rng.choice(palette)
        g = full_grid(sh * 2, sw * 2, 0)
        for r in range(sh):
            for c in range(sw):
                g[r * 2][c * 2] = color
        return g
    return full_grid(sh * 2, sw * 2, 0)
