"""Generator for puzzle 8ee62060.

Rule: column-pair-reversal. For each cell at col c:
  pair_start = c - (c % 2); offset = c % 2
  old_pair = w - 2 - pair_start; old_c = old_pair + offset
  output[r][c] = g[r][old_c]

Effectively: pairs of columns are reversed in order, but within each
pair the (left, right) order is preserved.

Combinatorial axes: grid_h, n_pairs (w = 2*n_pairs), fg_palette,
texture (per-pair pattern), pair_distinctness (force pairs to differ).
Degenerates: pair_palindrome (rule no-op), single_pair, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "997c17fd6870"
VERSION = "1.1.0"
TASK_ID = "997c17fd6870"
SUMMARY = "Even-width grid; rule reverses the order of column-pairs (preserves within-pair order)."

INVARIANTS = [
    "input width is even (2 × n_pairs)",
    "≥2 distinct pairs so the rule's pair-reversal is visible",
    "≥2 non-bg cells",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("pair_palindrome", "single_pair", "monochrome")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "n_pairs":        {"type": "int", "default": "rng 2..7", "valid": "2..7"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..10"},
    "texture":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, p_lo, p_hi, c_lo, c_hi = 4, 7, 2, 3, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, p_lo, p_hi, c_lo, c_hi = 11, 14, 5, 7, 5, 8
    else:
        h_lo, h_hi, p_lo, p_hi, c_lo, c_hi = 4, 14, 2, 7, 2, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    n_pairs = ctx.draw_int("n_pairs", p_lo, p_hi)
    w = 2 * n_pairs
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, palette, rng)
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)
    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    # Force ≥2 distinct pairs.
    pairs_seen = {tuple(g[r][i:i + 2]) for r in range(h) for i in range(0, w, 2)}
    if len(pairs_seen) < 2 and w >= 4:
        g[0][0] = palette[0]
        g[0][2] = palette[1] if len(palette) > 1 else palette[0]
    return g


def _draw_from_degenerate(name, h, w, palette, rng):
    g = full_grid(h, w, palette[0])
    if name == "pair_palindrome":
        # Each row is symmetric in pair order so the reversal yields
        # the same grid (rule no-op).
        for r in range(h):
            for i in range(0, w // 2, 2):
                a = rng.choice(palette); b = rng.choice(palette)
                # pair at i (left, right) = (a, b)
                g[r][i] = a; g[r][i + 1] = b
                # mirror pair at w-2-i = (a, b) — same as left
                g[r][w - 2 - i] = a; g[r][w - 1 - i] = b
        return g
    if name == "single_pair":
        # Single pair at the center; rest is bg.
        for r in range(h):
            g[r][w // 2] = palette[0]
            g[r][w // 2 + 1] = palette[1] if len(palette) > 1 else palette[0]
        return g
    if name == "monochrome":
        c0 = rng.choice(palette)
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    return g
