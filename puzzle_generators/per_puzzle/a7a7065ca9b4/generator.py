"""Generator for puzzle 62b74c02.

Rule: input has a non-bg pattern in left pw cols; col pw is the first
all-bg column. Rule copies the pattern to the right edge and fills the
middle columns with col-0's row color.

Combinatorial axes (8): grid_h/w, pattern_w, palette_size,
pattern_density, col0_uniqueness, pattern_layout, decoy_density,
right_pad_size.
Degenerates: empty_pattern_columns, single_color_pattern, full_pattern.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a7a7065ca9b4"
VERSION = "1.1.0"
TASK_ID = "a7a7065ca9b4"
SUMMARY = "Left pattern + col-0 row colors; rule copies pattern right and fills middle."

INVARIANTS = [
    "background is 0",
    "left pw columns (pw in [2, 4]) contain a non-bg pattern",
    "column pw is entirely bg (the divider)",
    "remaining grid right of col pw is bg in the input",
    "col 0 has a non-bg color in every row (fill source)",
    "right side has >=pw bg columns (room for the copy)",
]

PATTERN_LAYOUTS = ("sparse", "dense", "rows_uniform", "diag", "stripes")
DEGENERATE_TEXTURES = ("empty_pattern_columns", "single_color_pattern", "full_pattern")
HELPFUL_TEXTURES = PATTERN_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":          {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "pattern_w":       {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_size":    {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "pattern_density": {"type": "float", "default": "rng 0.3..0.7", "valid": "0..1"},
    "pattern_layout":  {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PATTERN_LAYOUTS)},
    "col0_uniqueness": {"type": "str", "default": "rng all_distinct|repeating|random",
                        "valid": "all_distinct|repeating|random"},
    "right_pad_size":  {"type": "int", "default": "= w - pw - 1", "valid": "auto"},
    "texture":         {"type": "str", "default": "alias for pattern_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, pw_lo, pw_hi = 4, 6, 8, 10, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, pw_lo, pw_hi = 9, 12, 13, 18, 3, 4
    else:
        h_lo, h_hi, w_lo, w_hi, pw_lo, pw_hi = 6, 10, 10, 14, 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    pw = int(overrides.get("pattern_w", ctx.draw_int("pattern_w", pw_lo, pw_hi)))
    pw = max(2, min(4, pw))
    if pw + 2 > w:
        pw = max(2, w - 2)
    n_palette = int(overrides.get("palette_size", ctx.draw_int("palette_size", 2, 4)))
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=max(2, n_palette), exclude={0}))
    layout = (overrides.get("texture") or overrides.get("pattern_layout")
              or ctx.draw_choice("pattern_layout", list(PATTERN_LAYOUTS)))
    density = float(overrides.get("pattern_density",
                                  ctx.draw_rng("pattern_density").uniform(0.3, 0.7)))
    col0_unique = overrides.get("col0_uniqueness",
                                ctx.draw_choice("col0_uniqueness",
                                                ["all_distinct", "repeating", "random"]))
    g = full_grid(h, w, 0)
    if col0_unique == "all_distinct" and len(palette) >= h:
        col0_colors = list(rng.sample(palette, h))
    elif col0_unique == "repeating":
        block = rng.choice(palette)
        col0_colors = [block] * h
        if len(palette) > 1:
            other = [p for p in palette if p != block]
            col0_colors[h // 2] = rng.choice(other)
    else:
        col0_colors = [rng.choice(palette) for _ in range(h)]
    for r in range(h):
        g[r][0] = col0_colors[r]
    _fill_pattern(g, layout, h, pw, palette, density, rng)
    for r in range(h):
        g[r][pw] = 0
    for r in range(h):
        for c in range(pw + 1, w):
            g[r][c] = 0
    return g


def _fill_pattern(g, layout, h, pw, palette, density, rng):
    if layout == "sparse":
        for r in range(h):
            for c in range(1, pw):
                if rng.random() < density * 0.5:
                    g[r][c] = rng.choice(palette)
    elif layout == "dense":
        for r in range(h):
            for c in range(1, pw):
                if rng.random() < density:
                    g[r][c] = rng.choice(palette)
    elif layout == "rows_uniform":
        for r in range(h):
            color = rng.choice(palette)
            for c in range(1, pw):
                if rng.random() < density:
                    g[r][c] = color
    elif layout == "diag":
        for r in range(h):
            c = 1 + (r % max(1, pw - 1))
            if c < pw:
                g[r][c] = rng.choice(palette)
    elif layout == "stripes":
        for c in range(1, pw):
            color = rng.choice(palette)
            for r in range(h):
                if rng.random() < density:
                    g[r][c] = color


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(palette)
    if name == "empty_pattern_columns":
        for r in range(h):
            g[r][0] = rng.choice(palette[:3])
        return g
    if name == "single_color_pattern":
        color = palette[0]
        for r in range(h):
            g[r][0] = color
        for r in range(h):
            for c in range(1, 3):
                if rng.random() < 0.5:
                    g[r][c] = color
        return g
    if name == "full_pattern":
        for r in range(h):
            g[r][0] = rng.choice(palette[:3])
            for c in range(1, 3):
                g[r][c] = rng.choice(palette[:3])
        return g
    return g
