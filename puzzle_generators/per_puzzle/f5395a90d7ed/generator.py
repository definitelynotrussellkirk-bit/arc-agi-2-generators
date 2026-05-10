"""Generator for puzzle d23f8c26.

Rule: `(rule! (lambda (g) (let ((mid (floor (/ (cols g) 2)))) (cellmap g (r c v) (if (= c mid) v 0)))))`.
Keep only the middle column; everything else → 0. Note: works with any
width because `floor` selects a single mid column.

Combinatorial axes:
  * grid_h               — outer canvas height
  * grid_wh              — (w-1)/2; total w = 2*grid_wh + 1 (odd)
  * texture              — pattern: noise/sparse/blob/stripes/checker/...
  * mid_col_kind         — what the middle column looks like:
                           mixed / two_colors / single_color / palette_col
  * decoy_density        — coverage of non-middle cells (irrelevant
                           to the rule — pure decoy)
  * caller-opt-in degenerates: monochrome, only_mid_filled,
                               middle_all_zero (output blank)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "f5395a90d7ed"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "f5395a90d7ed"
SUMMARY = "Odd-width colored grid; rule keeps only the middle column."

INVARIANTS = [
    "w is odd, w ≥ 3",
    "the middle column determines the entire output",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
MID_COL_KINDS = ("mixed", "two_colors", "single_color", "palette_col")
DEGENERATE_TEXTURES = ("monochrome", "only_mid_filled", "middle_all_zero")

AXES = {
    "grid_h":        {"type": "int",   "default": "rng 3..14", "valid": "2..18"},
    "grid_wh":       {"type": "int",   "default": "rng 1..7",  "valid": "1..14"},
    "texture":       {"type": "str",   "default": "rng helpful",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "mid_col_kind":  {"type": "str",   "default": "rng helpful",
                      "valid": "|".join(MID_COL_KINDS)},
    "bg_color":      {"type": "color", "default": "rng",       "valid": "0..9"},
    "decoy_density": {"type": "float", "default": "rng 0.4..0.85", "valid": "0..1"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, wh_lo, wh_hi = 3, 6, 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, wh_lo, wh_hi = 11, 14, 5, 7
    else:
        h_lo, h_hi, wh_lo, wh_hi = 3, 14, 1, 7

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    wh = ctx.draw_int("grid_wh", wh_lo, wh_hi)
    w = 2 * wh + 1
    rng = ctx.draw_rng("cells")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

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

    decoy_d = float(overrides.get(
        "decoy_density",
        ctx.draw_rng("decoy_density").uniform(0.4, 0.85)))
    if decoy_d < 1.0:
        g = apply_bg_density(g, full_palette, rng, 1.0 - decoy_d)

    mid = w // 2
    mid_kind = overrides.get(
        "mid_col_kind",
        ctx.draw_choice("mid_col_kind", list(MID_COL_KINDS)))
    _set_mid_column(g, mid, mid_kind, palette, rng)
    return g


def _set_mid_column(g, mid, kind, palette, rng):
    h = len(g)
    if not palette:
        palette = [1, 2]
    if kind == "mixed":
        for r in range(h):
            g[r][mid] = rng.choice(palette)
    elif kind == "two_colors":
        a = palette[0]; b = palette[1] if len(palette) > 1 else a
        for r in range(h):
            g[r][mid] = a if r % 2 == 0 else b
    elif kind == "single_color":
        c0 = palette[0]
        for r in range(h):
            g[r][mid] = c0
    elif kind == "palette_col":
        for r in range(h):
            g[r][mid] = palette[r % len(palette)]


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the keep-mid-column signal is hidden.

    monochrome       — uniform input → uniform 1-col output (visually trivial).
    only_mid_filled  — only the middle column has fg; rest is bg →
                        output looks "exactly like" the visible content.
    middle_all_zero  — middle column is all bg → output is blank
                        (rule's signal absent).
    """
    g = full_grid(h, w, 0)
    palette = list(range(1, 10))
    rng.shuffle(palette)
    mid = w // 2
    if name == "monochrome":
        c = palette[0]
        for r in range(h):
            for cc in range(w):
                g[r][cc] = c
        return g
    if name == "only_mid_filled":
        for r in range(h):
            g[r][mid] = palette[r % len(palette)]
        return g
    if name == "middle_all_zero":
        for r in range(h):
            for cc in range(w):
                if cc != mid:
                    g[r][cc] = rng.choice(palette[:3])
        return g
    return g
