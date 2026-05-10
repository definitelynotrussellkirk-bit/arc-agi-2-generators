"""Generator for puzzle 95a58926.

Rule: rows/cols with > w/2 (resp h/2) cells of color 5 are "lines".
Output: empty grid; intersections of these lines = marker color (first
non-{0,5} color in input); rest of these lines = 5.

Combinatorial axes (8): grid_h/w, n_5_rows, n_5_cols, marker_color,
five_density, distractor_density, position_bias, anchor_corner.
Degenerates: no_lines, all_lines, no_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import random_free_cell

GENERATOR_ID = "661dffbdf39a"
VERSION = "1.1.0"
TASK_ID = "661dffbdf39a"
SUMMARY = "Mostly-5 rows + cols + scattered marker; rule outputs cross."

INVARIANTS = [
    "background is 0",
    ">=1 row with > w/2 cells of 5",
    ">=1 col with > h/2 cells of 5",
    "exactly one marker color (non-0, non-5) in scattered cells",
]

POSITION_BIASES = ("spread", "centered", "edge", "diagonal")
DEGENERATE_TEXTURES = ("no_lines", "all_lines", "no_marker")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "grid_w":            {"type": "int", "default": "rng 12..18", "valid": "9..22"},
    "n_5_rows":          {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "n_5_cols":          {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "marker_color":      {"type": "color", "default": "rng (≠0,5)",
                          "valid": "1..9 (≠5)"},
    "five_density":      {"type": "float", "default": "rng 0.6..0.8",
                          "valid": "0.5..1"},
    "distractor_density":{"type": "float", "default": "rng 0.05..0.15",
                          "valid": "0..0.3"},
    "position_bias":     {"type": "str", "default": "rng helpful",
                          "valid": "|".join(POSITION_BIASES)},
    "texture":           {"type": "str", "default": "alias for position_bias",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 7, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 4, h_hi + 6)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rows = int(overrides.get("n_5_rows",
                               ctx.draw_int("n_5_rows", 1, 3)))
    n_cols = int(overrides.get("n_5_cols",
                               ctx.draw_int("n_5_cols", 1, 3)))
    n_rows = max(1, min(min(h - 1, 4), n_rows))
    n_cols = max(1, min(min(w - 1, 4), n_cols))
    marker = int(overrides.get("marker_color",
                               ctx.draw_color("marker_color",
                                              exclude={0, 5})))
    five_d = float(overrides.get("five_density",
                                 ctx.draw_rng("five_density")
                                 .uniform(0.6, 0.8)))
    distractor_d = float(overrides.get("distractor_density",
                                       ctx.draw_rng("distractor_density")
                                       .uniform(0.05, 0.15)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    rs = _pick_lines(bias, h, n_rows, rng)
    cs = _pick_lines(bias, w, n_cols, rng)
    for r in rs:
        for c in range(w):
            g[r][c] = 5 if rng.random() < five_d else marker
    for c in cs:
        for r in range(h):
            if g[r][c] == 0:
                g[r][c] = 5 if rng.random() < five_d else marker
    # Stray marker cells
    for _ in range(int(h * w * distractor_d / 4)):
        cell = random_free_cell(g, rng, max_tries=20)
        if cell is not None:
            g[cell[0]][cell[1]] = marker
    return g


def _pick_lines(bias, dim, n, rng):
    if bias == "centered":
        center = dim // 2
        rs = [center - (n - 1) // 2 + i for i in range(n)]
        return [r for r in rs if 0 <= r < dim][:n]
    if bias == "edge":
        edges = [0, dim - 1]
        rs = list(edges)
        if n > 2:
            rs += rng.sample(range(1, dim - 1), min(n - 2, dim - 2))
        return rs[:n]
    if bias == "diagonal":
        return [i * (dim // (n + 1)) + 1 for i in range(n)
                if i * (dim // (n + 1)) + 1 < dim][:n]
    return rng.sample(range(dim), n)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    marker = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "no_lines":
        # Sparse 5s — no row/col has > 50% 5s
        for _ in range(h * w // 10):
            cell = random_free_cell(g, rng, max_tries=20)
            if cell is not None:
                g[cell[0]][cell[1]] = 5
        for _ in range(2):
            cell = random_free_cell(g, rng, max_tries=10)
            if cell is not None:
                g[cell[0]][cell[1]] = marker
        return g
    if name == "all_lines":
        # Every row + col is mostly 5 → output is large cross
        for r in range(h):
            for c in range(w):
                g[r][c] = 5 if rng.random() < 0.85 else marker
        return g
    if name == "no_marker":
        # Lines exist but no non-5 marker
        r = h // 2; c = w // 2
        for cc in range(w):
            g[r][cc] = 5
        for rr in range(h):
            if g[rr][c] == 0:
                g[rr][c] = 5
        return g
    return g
