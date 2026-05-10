"""Generator for puzzle 623ea044.

Rule: bg=0; sparse non-bg cells. Output shoots diagonals from every
non-bg cell along all 4 diagonals, keeping the cell's color.

Combinatorial axes (8): grid_h/w, n_dots, fgc, position_bias,
density_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_dots, full_grid, single_dot.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_cells
from puzzle_generators.helpers.indices import all_indices

GENERATOR_ID = "9ce2dcf587b8"
VERSION = "1.1.0"
TASK_ID = "9ce2dcf587b8"
SUMMARY = "Sparse dots; rule shoots 4 diagonals from each in dot's color."

INVARIANTS = [
    "background is 0",
    ">=1 non-bg cells, all same color",
]

DENSITY_KINDS = ("sparse", "medium", "dense", "checker", "diagonal",
                 "corners", "stripes")
DEGENERATE_TEXTURES = ("no_dots", "full_grid", "single_dot")
HELPFUL_TEXTURES = DENSITY_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..14", "valid": "3..30"},
    "grid_w":         {"type": "int", "default": "rng 5..14", "valid": "3..30"},
    "fgc":            {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "n_dots":         {"type": "int", "default": "rng 2..(h*w)/8",
                       "valid": "1..(h*w)"},
    "density_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DENSITY_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..3"},
    "texture":        {"type": "str", "default": "alias for density_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 7
    elif difficulty == "hard":
        h_lo, h_hi = 14, 25
    else:
        h_lo, h_hi = 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fgc = int(overrides.get("fgc",
                            ctx.draw_color("fgc", exclude={0})))
    if fgc == 0:
        fgc = 3
    density = (overrides.get("texture") or
               overrides.get("density_kind")
               or ctx.draw_choice("density_kind",
                                  list(DENSITY_KINDS)))
    g = full_grid(h, w, 0)
    if density == "sparse":
        n = max(1, (h * w) // 16)
    elif density == "medium":
        n = max(1, (h * w) // 8)
    elif density == "dense":
        n = max(1, (h * w) // 4)
    else:
        n = int(overrides.get("n_dots",
                              ctx.draw_int("n_dots", 2, max(2, h * w // 8))))
    if density == "checker":
        for r in range(h):
            for c in range(w):
                if (r + c) % 2 == 0 and rng.random() < 0.5:
                    g[r][c] = fgc
    elif density == "diagonal":
        for i in range(min(h, w)):
            g[i][i] = fgc
    elif density == "corners":
        for r, c in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
            g[r][c] = fgc
    elif density == "stripes":
        for r in range(0, h, 2):
            for c in range(0, w, 3):
                g[r][c] = fgc
    else:
        n = max(1, min(h * w - 1, n))
        locs = rng.sample(list(all_indices(h, w)), n)
        paint_cells(g, locs, fgc)
    if not any(v != 0 for row in g for v in row):
        g[0][0] = fgc
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fgc = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_dots":
        # Force 1 dot since rule needs something to shoot
        g[h // 2][w // 2] = fgc
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = fgc
        return g
    if name == "single_dot":
        g[h // 2][w // 2] = fgc
        return g
    return g
