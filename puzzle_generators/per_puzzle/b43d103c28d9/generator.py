"""Generator for ARC task 3906de3d.

Rule: gravity-up by column. For each column c: collect non-zero values
in their original order, then place them in rows 0..n-1 of the output
column; the rest is 0.

Combinatorial axes: grid_h/w, palette_size, fg_density, fg_layout
(spread/clustered/sparse).
Degenerates: all_zero, all_filled (output equals input), single_column.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b43d103c28d9"
VERSION = "1.1.0"
TASK_ID = "b43d103c28d9"
SUMMARY = "Sparse columns; rule stacks each column's non-zero values at the top (gravity-up)."

INVARIANTS = [
    "background is 0",
    "≥1 non-zero cell so output is non-trivial",
]

FG_LAYOUTS = ("spread", "clustered_top", "clustered_bottom", "scattered", "blob")
DEGENERATE_TEXTURES = ("all_zero", "all_filled", "single_column")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "grid_w":          {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "palette_size":    {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "fg_density":      {"type": "float", "default": "rng 0.15..0.4", "valid": "0..0.9"},
    "fg_layout":       {"type": "str", "default": "rng helpful",
                        "valid": "|".join(FG_LAYOUTS)},
    "texture":         {"type": "str", "default": "alias for fg_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 4, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 5)))
    palette = list(ctx.draw_distinct_colors("palette", n=max(1, n_palette), exclude={0}))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.15, 0.4)))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    g = full_grid(h, w, 0)
    if layout == "spread":
        for r in range(h):
            for c in range(w):
                if rng.random() < density:
                    g[r][c] = rng.choice(palette)
    elif layout == "clustered_top":
        for r in range(h // 2):
            for c in range(w):
                if rng.random() < density * 1.5:
                    g[r][c] = rng.choice(palette)
    elif layout == "clustered_bottom":
        for r in range(h // 2, h):
            for c in range(w):
                if rng.random() < density * 1.5:
                    g[r][c] = rng.choice(palette)
    elif layout == "scattered":
        for r in range(0, h, 2):
            for c in range(0, w, 2):
                if rng.random() < density * 1.5:
                    g[r][c] = rng.choice(palette)
    elif layout == "blob":
        bh = max(1, int(h * density)); bw = max(1, int(w * density))
        r0 = rng.randint(0, h - bh); c0 = rng.randint(0, w - bw)
        for r in range(r0, r0 + bh):
            for c in range(c0, c0 + bw):
                g[r][c] = rng.choice(palette)
    if not any(g[r][c] != 0 for r in range(h) for c in range(w)):
        g[h - 1][0] = palette[0]
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "all_zero":
        g[h - 1][0] = fg
        return g
    if name == "all_filled":
        # Every cell non-zero; output equals input.
        for r in range(h):
            for c in range(w):
                g[r][c] = fg
        return g
    if name == "single_column":
        c = rng.randint(0, w - 1)
        for r in range(h):
            if rng.random() < 0.5:
                g[r][c] = fg
        g[h - 1][c] = fg
        return g
    return g
