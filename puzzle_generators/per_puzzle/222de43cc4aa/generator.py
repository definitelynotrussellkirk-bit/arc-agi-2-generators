"""Generator for puzzle eb281b96.

Rule: vertical pingpong extension. Output height = 4*(h-1)+1. Each
row of output is taken from the input following the zigzag pattern:
input rows 0,1,...,h-1, h-2,...,1, 0, 1, ..., (period = 2*(h-1)).

Combinatorial axes (8):
  * grid_h / grid_w        — input dims (output 4*(h-1)+1 ≤ 30)
  * palette_size           — distinct fg colors
  * texture                — fill pattern (noise/sparse/blob/checker/...)
  * fg_density             — fraction of fg cells
  * row_distinctness       — strict (each row unique) / loose
  * vertical_asymmetric    — bool: ensure top != bottom (else pingpong invisible)
  * top_row_kind           — solid / striped / pattern_anchor (drives the
                             zigzag's visual signal)
  * caller-opt-in degenerates: ud_symmetric (output looks like simple
                              vertical tiling), monochrome, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "222de43cc4aa"
VERSION = "1.1.0"
TASK_ID = "222de43cc4aa"
SUMMARY = "Small grid; rule extends vertically with zigzag/pingpong reflection (out_h = 4*(h-1)+1)."

INVARIANTS = [
    "input height in [3, 8] (so 4*(h-1)+1 stays ≤ 29)",
    "input width ≤ 30",
    "≥2 distinct rows so the pingpong has visible variation",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
TOP_ROW_KINDS = ("solid", "striped", "pattern_anchor", "asymmetric_marker")
DEGENERATE_TEXTURES = ("ud_symmetric", "monochrome", "single_row")

AXES = {
    "grid_h":          {"type": "int",   "default": "rng 3..7", "valid": "3..8"},
    "grid_w":          {"type": "int",   "default": "rng 4..14", "valid": "3..16"},
    "palette_size":    {"type": "int",   "default": "rng 2..6", "valid": "1..10"},
    "texture":         {"type": "str",   "default": "rng helpful",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "fg_density":      {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "noise_overlay":   {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "top_row_kind":    {"type": "str",   "default": "rng helpful",
                        "valid": "|".join(TOP_ROW_KINDS)},
    "vertical_asymmetric": {"type": "bool", "default": "true", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 3, 4, 4, 8, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 6, 7, 11, 14, 5, 8
    else:
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 3, 7, 4, 14, 2, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    n_colors = ctx.draw_int("palette_size", c_lo, c_hi)
    palette = ctx.draw_distinct_colors("palette", n=n_colors)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, palette, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    g = fill_texture(texture, h, w, palette, rng)
    fill_d = float(overrides.get("fg_density",
                                 ctx.draw_rng("fg_density").uniform(0.3, 0.7)))
    if fill_d < 1.0:
        g = apply_bg_density(g, palette, rng, 1.0 - fill_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)
    top_row_kind = overrides.get("top_row_kind",
                                 ctx.draw_choice("top_row_kind", list(TOP_ROW_KINDS)))
    _shape_top_row(g, top_row_kind, palette, rng)
    if bool(overrides.get("vertical_asymmetric", True)) and _is_ud_sym(g):
        # Force at least one cell to break UD symmetry.
        g[0][0] = palette[1] if len(palette) > 1 else (g[0][0] + 1) % 10
    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _shape_top_row(g, kind, palette, rng):
    h = len(g); w = len(g[0])
    if kind == "solid":
        c0 = palette[0]
        for c in range(w):
            g[0][c] = c0
    elif kind == "striped":
        for c in range(w):
            g[0][c] = palette[c % len(palette)]
    elif kind == "pattern_anchor":
        # Single anchor at col 0 with distinct color
        g[0][0] = palette[0]
    elif kind == "asymmetric_marker":
        # Different markers at col 0 and col w-1 (forces asym)
        g[0][0] = palette[0]
        g[0][w - 1] = palette[1] if len(palette) > 1 else palette[0]


def _is_ud_sym(g):
    h = len(g); w = len(g[0])
    return all(g[r][c] == g[h - 1 - r][c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    g = full_grid(h, w, palette[0])
    if name == "ud_symmetric":
        for c in range(w):
            for r in range(h // 2):
                v = rng.choice(palette)
                g[r][c] = v
                g[h - 1 - r][c] = v
        return g
    if name == "monochrome":
        c0 = rng.choice(palette)
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "single_row":
        for c in range(w):
            g[0][c] = rng.choice(palette)
        for r in range(1, h):
            for c in range(w):
                g[r][c] = g[0][c]
        return g
    return g
