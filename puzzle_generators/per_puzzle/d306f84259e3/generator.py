"""Generator for puzzle a5f85a15.

Rule: for each diagonal (constant r-c), every other non-bg cell along
the diagonal gets recolored to 4. Specifically: 1st, 3rd, 5th… non-bg
cells stay; 2nd, 4th, 6th… become 4.

Combinatorial axes (8): grid_h/w, base_color, n_diagonal_runs,
diag_run_length, diag_density, position_bias, palette_size,
asymmetry_force.
Degenerates: empty_grid, single_cell, full_grid_diag.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d306f84259e3"
VERSION = "1.1.0"
TASK_ID = "d306f84259e3"
SUMMARY = "Diagonal cells of one color; rule recolors every-other to 4."

INVARIANTS = [
    "background is 0",
    ">=2 non-bg cells",
    "non-bg cells use a single color != 4",
    "at least one diagonal has >=2 non-bg cells (so rule has effect)",
]

DIAG_PATTERNS = ("single_diag", "two_diags", "scattered_diag",
                 "dense_diag", "sparse", "broken_diag")
DEGENERATE_TEXTURES = ("empty_grid", "single_cell", "full_grid_diag")
HELPFUL_TEXTURES = DIAG_PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "6..16"},
    "base_color":     {"type": "color", "default": "rng (≠0,4)",
                       "valid": "1..9 (≠4)"},
    "n_diagonal_runs":{"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "diag_min_length":{"type": "int", "default": "2", "valid": "2..6"},
    "diag_max_length":{"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "diag_pattern":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIAG_PATTERNS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for diag_pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 6, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 1)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    color = int(overrides.get("base_color",
                              ctx.draw_color("base_color", exclude={0, 4})))
    n_runs = int(overrides.get("n_diagonal_runs",
                               ctx.draw_int("n_diagonal_runs", 1, 3)))
    n_runs = max(1, min(5, n_runs))
    d_min = int(overrides.get("diag_min_length", 2))
    d_max = int(overrides.get("diag_max_length",
                              ctx.draw_int("diag_max_length", 4, 6)))
    d_min = max(2, min(6, d_min))
    d_max = max(d_min, min(min(h, w), d_max))
    pattern = (overrides.get("texture") or
               overrides.get("diag_pattern")
               or ctx.draw_choice("diag_pattern", list(DIAG_PATTERNS)))
    g = full_grid(h, w, 0)
    if pattern == "single_diag":
        n_runs = 1
    elif pattern == "two_diags":
        n_runs = max(2, n_runs)
    for _ in range(n_runs):
        run_len = rng.randint(d_min, d_max)
        run_len = min(run_len, min(h, w))
        if pattern == "broken_diag":
            r0 = rng.randint(0, h - run_len)
            c0 = rng.randint(0, w - run_len)
            for i in range(run_len):
                if rng.random() > 0.25:
                    g[r0 + i][c0 + i] = color
        elif pattern == "sparse":
            for _ in range(rng.randint(2, 4)):
                rr = rng.randint(0, h - 1)
                cc = rng.randint(0, w - 1)
                if g[rr][cc] == 0:
                    g[rr][cc] = color
        elif pattern == "dense_diag":
            r0 = rng.randint(0, h - run_len)
            c0 = rng.randint(0, w - run_len)
            for i in range(run_len):
                g[r0 + i][c0 + i] = color
            # add extra near the diag
            for off in (-1, 1):
                for i in range(run_len):
                    rr = r0 + i; cc = c0 + i + off
                    if 0 <= cc < w and rng.random() < 0.3 and g[rr][cc] == 0:
                        g[rr][cc] = color
        elif pattern == "scattered_diag":
            r0 = rng.randint(0, h - run_len)
            c0 = rng.randint(0, w - run_len)
            for i in range(run_len):
                if rng.random() < 0.7:
                    g[r0 + i][c0 + i] = color
        else:
            r0 = rng.randint(0, h - run_len)
            c0 = rng.randint(0, w - run_len)
            for i in range(run_len):
                g[r0 + i][c0 + i] = color
    if bool(overrides.get("anchor_corner", False)):
        if g[0][0] == 0:
            g[0][0] = color
    n_nonbg = sum(1 for row in g for v in row if v != 0)
    if n_nonbg < 2:
        g[0][0] = color
        g[1][1 if w > 1 else 0] = color
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
    if name == "empty_grid":
        return g
    if name == "single_cell":
        g[h // 2][w // 2] = color
        return g
    if name == "full_grid_diag":
        for i in range(min(h, w)):
            g[i][i] = color
        return g
    return g
