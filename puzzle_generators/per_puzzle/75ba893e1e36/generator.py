"""Generator for ARC task 59341089.

Rule: output is h × 4w. For each output col c with phase = c mod 2w:
  if phase < w → output = g[r][w-1-phase]   (LR-mirror)
  else         → output = g[r][phase-w]     (input)
Effectively: 4 horizontal tiles in pattern: mirror|input|mirror|input.

Combinatorial axes (8):
  * grid_h / grid_w        — input dims (output 4w must fit ≤ 30)
  * palette_size           — distinct fg colors
  * texture                — noise/sparse/blob/stripes/...
  * fg_density             — coverage
  * lr_asymmetric          — bool: ensure LR != input
  * left_edge_kind         — what's special at col 0 (anchor visible in mirror)
  * row_pattern            — random / per_row / banded / row_distinct
  * caller-opt-in degenerates: lr_symmetric (output is just 4 copies),
                              monochrome (uniform), single_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "75ba893e1e36"
VERSION = "1.1.0"
TASK_ID = "75ba893e1e36"
SUMMARY = "Tile; rule extends 4 horizontal phases (mirror|input|mirror|input), output h × 4w."

INVARIANTS = [
    "4 × w ≤ 30 so output fits",
    "input width ≤ 7",
    "≥2 distinct colors so the mirror is visible",
    "input is not LR-symmetric (else mirror has no effect)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
LEFT_EDGE_KINDS = ("anchor", "stripe", "blank", "matching")
ROW_PATTERNS = ("random", "per_row", "banded", "row_distinct")
DEGENERATE_TEXTURES = ("lr_symmetric", "monochrome", "single_col")

AXES = {
    "grid_h":         {"type": "int",   "default": "rng 2..14", "valid": "1..15"},
    "grid_w":         {"type": "int",   "default": "rng 2..7", "valid": "1..7"},
    "palette_size":   {"type": "int",   "default": "rng 2..6", "valid": "1..10"},
    "texture":        {"type": "str",   "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "bg_density":     {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "noise_overlay":  {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
    "left_edge_kind": {"type": "str",   "default": "rng helpful",
                       "valid": "|".join(LEFT_EDGE_KINDS)},
    "row_pattern":    {"type": "str",   "default": "rng helpful",
                       "valid": "|".join(ROW_PATTERNS)},
    "lr_asymmetric":  {"type": "bool",  "default": "true", "valid": "true|false"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 5, 2, 4, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 11, 14, 5, 7, 5, 8
    else:
        h_lo, h_hi, w_lo, w_hi, c_lo, c_hi = 2, 14, 2, 7, 2, 6
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
    bg_d = float(overrides.get("bg_density",
                               ctx.draw_rng("bg_density").uniform(0.0, 0.4)))
    if bg_d > 0.0:
        g = apply_bg_density(g, palette, rng, bg_d)
    no = float(overrides.get("noise_overlay",
                             ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, palette, rng, no)
    edge = overrides.get("left_edge_kind",
                         ctx.draw_choice("left_edge_kind", list(LEFT_EDGE_KINDS)))
    _shape_left_edge(g, edge, palette, rng)
    row_pat = overrides.get("row_pattern",
                            ctx.draw_choice("row_pattern", list(ROW_PATTERNS)))
    _apply_row_pattern(g, row_pat, palette, rng)
    if bool(overrides.get("lr_asymmetric", True)) and _is_lr_sym(g):
        g[0][0] = palette[1] if len(palette) > 1 else (g[0][0] + 1) % 10
    if len({v for row in g for v in row}) < 2:
        g[0][0] = palette[0]
        g[-1][-1] = palette[1] if len(palette) > 1 else (palette[0] + 1) % 10
    return g


def _shape_left_edge(g, kind, palette, rng):
    h = len(g)
    if kind == "anchor":
        g[0][0] = palette[0]
    elif kind == "stripe":
        for r in range(h):
            g[r][0] = palette[r % len(palette)]
    elif kind == "matching":
        # Make col 0 same as col w-1 (will produce mirror palindrome)
        w = len(g[0])
        for r in range(h):
            g[r][0] = g[r][w - 1]


def _apply_row_pattern(g, pat, palette, rng):
    h = len(g); w = len(g[0])
    if pat == "per_row":
        for r in range(h):
            color = palette[r % len(palette)]
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = color
    elif pat == "banded":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[(r + c) % len(palette)]
    elif pat == "row_distinct":
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0:
                    g[r][c] = palette[r % len(palette)]


def _is_lr_sym(g):
    h = len(g); w = len(g[0])
    return all(g[r][c] == g[r][w - 1 - c] for r in range(h) for c in range(w))


def _draw_from_degenerate(name, h, w, palette, rng):
    g = full_grid(h, w, palette[0])
    if name == "lr_symmetric":
        for r in range(h):
            for c in range(w // 2):
                v = rng.choice(palette)
                g[r][c] = v
                g[r][w - 1 - c] = v
        return g
    if name == "monochrome":
        c0 = rng.choice(palette)
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "single_col":
        for r in range(h):
            v = rng.choice(palette)
            for c in range(w):
                g[r][c] = v
        return g
    return g
