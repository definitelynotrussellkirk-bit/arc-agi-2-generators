"""Generator for ARC task c9f8e694.

Rule: for each cell with v==5, replace with the first non-5 in same
row (if any); else keep.

Combinatorial axes: grid_h/w, row_palette, n_non5_per_row,
five_density, row_color_distribution.
Degenerates: all_fives, no_fives, single_non5_per_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9da02d5e3ac0"
VERSION = "1.1.0"
TASK_ID = "9da02d5e3ac0"
SUMMARY = "Rows have non-5 markers and 5 cells; rule replaces 5s with the row's first non-5 value."

INVARIANTS = [
    "each row has ≥1 non-5 value (else 5s stay)",
    "≥1 5 cell exists somewhere",
    "row palette uses distinct non-5 colors",
]

ROW_DISTRIBUTIONS = ("uniform_per_row", "all_distinct", "biased")
DEGENERATE_TEXTURES = ("all_fives", "no_fives", "single_non5_per_row")
HELPFUL_TEXTURES = ROW_DISTRIBUTIONS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":            {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "row_palette_size":  {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "five_density":      {"type": "float", "default": "rng 0.5..0.85", "valid": "0..1"},
    "row_distribution":  {"type": "str", "default": "rng helpful",
                          "valid": "|".join(ROW_DISTRIBUTIONS)},
    "texture":           {"type": "str", "default": "alias for row_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("rows")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_palette = int(overrides.get("row_palette_size",
                                  ctx.draw_int("row_palette_size", 2, 6)))
    palette = list(ctx.draw_distinct_colors("row_colors", n=max(1, n_palette), exclude={5}))
    density = float(overrides.get("five_density",
                                  ctx.draw_rng("five_density").uniform(0.5, 0.85)))
    distribution = (overrides.get("texture") or overrides.get("row_distribution")
                    or ctx.draw_choice("row_distribution", list(ROW_DISTRIBUTIONS)))
    g = full_grid(h, w, 5)
    for r in range(h):
        if distribution == "uniform_per_row":
            color = palette[r % len(palette)]
        elif distribution == "all_distinct":
            color = palette[r % len(palette)]
        elif distribution == "biased":
            color = rng.choices(palette,
                                weights=[3] + [1] * (len(palette) - 1))[0]
        else:
            color = rng.choice(palette)
        # Place ≥1 non-5 in row.
        n_color = max(1, int(w * (1 - density)))
        positions = list(range(w))
        rng.shuffle(positions)
        for c in positions[:n_color]:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, h, w, rng):
    palette = [c for c in range(1, 10) if c != 5]
    rng.shuffle(palette)
    g = full_grid(h, w, 5)
    if name == "all_fives":
        return g
    if name == "no_fives":
        # No 5 cells; rule has nothing to replace.
        c0 = palette[0]
        for r in range(h):
            for c in range(w):
                g[r][c] = c0
        return g
    if name == "single_non5_per_row":
        for r in range(h):
            c = rng.randint(0, w - 1)
            g[r][c] = palette[r % len(palette)]
        return g
    return g
