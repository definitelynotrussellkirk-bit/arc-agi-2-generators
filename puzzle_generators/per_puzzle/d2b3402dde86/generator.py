"""Generator for puzzle 2013d3e2.

Rule: crop to non-bg content, then crop the result to its top-left
((h/2)-1) × ((w/2)-1) corner.

Combinatorial axes: grid_h/w, content_h/w (size of the inner block),
texture (pattern within content), padding_min, fg_palette.
Degenerates: fills_grid (no padding), single_cell, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.textures import (
    fill_texture, apply_bg_density, apply_noise_overlay,
)

GENERATOR_ID = "d2b3402dde86"
VERSION = "1.1.0"
TASK_ID = "d2b3402dde86"
SUMMARY = "Padded content block; rule crops to content then takes top-left ((h/2)-1)×((w/2)-1) corner."

INVARIANTS = [
    "background is 0",
    "non-bg content has bg padding so cropping shrinks",
    "content_h ≥ 4 and content_w ≥ 4 so output is non-trivial",
]

HELPFUL_TEXTURES = (
    "noise", "sparse", "blob", "stripes",
    "gradient", "checkerboard", "frame", "ring", "plus",
)
DEGENERATE_TEXTURES = ("fills_grid", "single_cell", "monochrome")

AXES = {
    "grid_h":          {"type": "int", "default": "rng 8..16", "valid": "5..20"},
    "grid_w":          {"type": "int", "default": "rng 8..16", "valid": "5..20"},
    "content_h":       {"type": "int", "default": "rng 4..min(grid_h-2, 10)",
                        "valid": "4..15"},
    "content_w":       {"type": "int", "default": "rng 4..min(grid_w-2, 10)",
                        "valid": "4..15"},
    "fg_palette_size": {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "texture":         {"type": "str", "default": "rng helpful",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
    "padding_min":     {"type": "int", "default": "rng 1..3", "valid": "1..5"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        g_lo, g_hi, c_lo, c_hi = 8, 10, 4, 5
    elif difficulty == "hard":
        g_lo, g_hi, c_lo, c_hi = 14, 16, 7, 10
    else:
        g_lo, g_hi, c_lo, c_hi = 8, 16, 4, 10
    h = ctx.draw_int("grid_h", g_lo, g_hi)
    w = ctx.draw_int("grid_w", g_lo, g_hi)
    rng = ctx.draw_rng("shape")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pad = int(overrides.get("padding_min",
                            ctx.draw_int("padding_min", 1, 3)))
    sh = ctx.draw_int("content_h", c_lo, max(c_lo, min(c_hi, h - 2 * pad)))
    sw = ctx.draw_int("content_w", c_lo, max(c_lo, min(c_hi, w - 2 * pad)))
    rr = ctx.draw_int("content_r", pad, max(pad, h - sh - pad))
    rc = ctx.draw_int("content_c", pad, max(pad, w - sw - pad))
    n_palette = int(overrides.get("fg_palette_size",
                                  ctx.draw_int("fg_palette_size", 1, 3)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0}))
    full_palette = [0, *palette]
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    inner = fill_texture(texture, sh, sw, full_palette, rng)
    g = full_grid(h, w, 0)
    for dr in range(sh):
        for dc in range(sw):
            g[rr + dr][rc + dc] = inner[dr][dc]
    # Pin corners so bbox extent is unambiguous.
    g[rr][rc] = palette[0]
    g[rr][rc + sw - 1] = palette[-1]
    g[rr + sh - 1][rc] = palette[0]
    g[rr + sh - 1][rc + sw - 1] = palette[-1]
    return g


def _draw_from_degenerate(name, h, w, rng):
    palette = list(range(1, 10))
    rng.shuffle(palette)
    g = full_grid(h, w, 0)
    if name == "fills_grid":
        fg = palette[0]
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.5:
                    g[r][c] = fg
        g[0][0] = fg; g[0][w - 1] = fg
        g[h - 1][0] = fg; g[h - 1][w - 1] = fg
        return g
    if name == "single_cell":
        # Need at least a 4x4 content for the rule to produce non-trivial output;
        # but degenerate "single cell" is intentionally below that — rule will
        # try to crop and may produce a 1x1 output.
        rr = rng.randint(2, h - 3); rc = rng.randint(2, w - 3)
        # Add 4 corners to ensure crop has some extent.
        for r, c in [(rr, rc), (rr, rc + 3), (rr + 3, rc), (rr + 3, rc + 3)]:
            g[r][c] = palette[0]
        return g
    if name == "monochrome":
        rr = rng.randint(2, h - 6); rc = rng.randint(2, w - 6)
        for r in range(rr, rr + 4):
            for c in range(rc, rc + 4):
                g[r][c] = palette[0]
        return g
    return g
