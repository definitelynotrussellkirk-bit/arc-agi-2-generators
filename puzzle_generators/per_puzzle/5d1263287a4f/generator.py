"""Generator for puzzle 2dee498d.

Rule: `(rule! (lambda (g) (let ((pw (/ (cols g) 3))) (build-grid (rows g) pw (r c) (at g r c)))))`.
Output is the leftmost third of the input (h × w/3).

Combinatorial axes:
  * grid_h               — outer canvas height
  * grid_w_third         — w/3 (so total w = 3 × grid_w_third)
  * texture              — pattern: noise/sparse/blob/stripes/checker/...
  * left_third_kind      — what fills the leftmost third (controls
                           output): mixed / two_colors / one_color /
                           palette_left
  * mid_right_pattern    — what fills the middle and right thirds
                           (decoy that the rule discards):
                           same_as_left / different / random / blank
  * caller-opt-in degenerates: monochrome, periodic_thirds (input
                               looks like 3 copies → output = a third
                               looking the same), only_left_filled
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "5d1263287a4f"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "5d1263287a4f"
SUMMARY = "Width divisible by 3; rule outputs the leftmost third of the input."

INVARIANTS = [
    "w divisible by 3",
    "the leftmost w/3 columns determine the output",
    "the middle and right thirds are decoy (rule discards them)",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
LEFT_THIRD_KINDS = ("mixed", "two_colors", "one_color", "palette_left")
MID_RIGHT_PATTERNS = ("same_as_left", "different", "random", "blank")
DEGENERATE_TEXTURES = ("monochrome", "periodic_thirds", "only_left_filled")

AXES = {
    "grid_h":           {"type": "int",   "default": "rng 2..10", "valid": "2..15"},
    "grid_w_third":     {"type": "int",   "default": "rng 2..6",  "valid": "1..10"},
    "texture":          {"type": "str",   "default": "rng helpful",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "left_third_kind":  {"type": "str",   "default": "rng helpful",
                         "valid": "|".join(LEFT_THIRD_KINDS)},
    "mid_right_pattern": {"type": "str",  "default": "rng helpful",
                          "valid": "|".join(MID_RIGHT_PATTERNS)},
    "bg_color":         {"type": "color", "default": "rng",       "valid": "0..9"},
    "noise_overlay":    {"type": "float", "default": "rng 0..0.05", "valid": "0..0.3"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, t_lo, t_hi = 2, 5, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, t_lo, t_hi = 8, 10, 5, 6
    else:
        h_lo, h_hi, t_lo, t_hi = 2, 10, 2, 6

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    third = ctx.draw_int("grid_w_third", t_lo, t_hi)
    w = third * 3
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, third, rng)

    bg = int(overrides.get("bg_color", ctx.draw_color("bg_color")))
    palette = list(ctx.draw_distinct_colors("palette", n=5))
    if bg in palette:
        palette = [c for c in palette if c != bg] + \
                  [c for c in range(10) if c not in palette and c != bg][:1]

    texture = overrides.get(
        "texture",
        ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    full_palette = [bg, *palette]
    g = fill_texture(texture, h, w, full_palette, rng)

    no = float(overrides.get(
        "noise_overlay",
        ctx.draw_rng("noise_overlay").uniform(0.0, 0.05)))
    if no > 0.0:
        g = apply_noise_overlay(g, full_palette, rng, no)

    left_kind = overrides.get(
        "left_third_kind",
        ctx.draw_choice("left_third_kind", list(LEFT_THIRD_KINDS)))
    _set_left_third(g, third, left_kind, palette, rng)

    pattern = overrides.get(
        "mid_right_pattern",
        ctx.draw_choice("mid_right_pattern", list(MID_RIGHT_PATTERNS)))
    _set_mid_right(g, third, pattern, bg, palette, rng)
    return g


def _set_left_third(g, third, kind, palette, rng):
    h = len(g)
    if not palette:
        palette = [1, 2]
    if kind == "mixed":
        for r in range(h):
            for c in range(third):
                g[r][c] = rng.choice(palette)
    elif kind == "two_colors":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        for r in range(h):
            for c in range(third):
                g[r][c] = a if (r + c) % 2 == 0 else b
    elif kind == "one_color":
        c0 = palette[0]
        for r in range(h):
            for c in range(third):
                g[r][c] = c0
    elif kind == "palette_left":
        for r in range(h):
            for c in range(third):
                g[r][c] = palette[(r + c) % len(palette)]


def _set_mid_right(g, third, pattern, bg, palette, rng):
    h = len(g); w = len(g[0])
    if pattern == "same_as_left":
        for r in range(h):
            for c in range(third, w):
                g[r][c] = g[r][c % third]
    elif pattern == "different":
        # Force columns in mid/right to NOT equal the corresponding
        # left-third column (visually misleading: looks like 3 distinct panels).
        for r in range(h):
            for c in range(third, w):
                left_v = g[r][c % third]
                options = [v for v in palette if v != left_v]
                if not options:
                    options = palette
                g[r][c] = rng.choice(options)
    elif pattern == "random":
        for r in range(h):
            for c in range(third, w):
                g[r][c] = rng.choice([bg] + list(palette))
    elif pattern == "blank":
        for r in range(h):
            for c in range(third, w):
                g[r][c] = bg


def _draw_from_degenerate(name, h, w, third, rng):
    """Edge-case where the left-third extraction is hidden.

    monochrome         — uniform input → uniform output (third the width).
    periodic_thirds    — middle and right thirds = exact copies of left;
                          the cropping looks like "compress to 1/3."
    only_left_filled   — only the leftmost third has fg cells; right
                          two thirds are bg → output looks "exactly like"
                          the visible content.
    """
    bg = 0
    g = full_grid(h, w, bg)
    palette = list(range(1, 10))
    rng.shuffle(palette)
    if name == "monochrome":
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "periodic_thirds":
        for r in range(h):
            for c in range(third):
                g[r][c] = palette[(r + c) % len(palette)]
            for c in range(third, w):
                g[r][c] = g[r][c % third]
        return g
    if name == "only_left_filled":
        for r in range(h):
            for c in range(third):
                g[r][c] = palette[(r + c) % len(palette)]
        return g
    return g
