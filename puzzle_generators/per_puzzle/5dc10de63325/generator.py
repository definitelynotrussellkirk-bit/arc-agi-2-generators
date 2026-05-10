"""Generator for puzzle b1fc8b8e.

Rule: count cyan(8) cells. Output is a 5x5 grid with 2x2 tiles in a
zero-cross arrangement, where count is divided by 4 per quadrant.

Combinatorial axes (8): grid_h/w, n_cyans, distribution, position_bias,
anchor_corner, asymmetry_force, palette_size, include_decoy.
Degenerates: no_cyans, full_grid, single_cyan.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5dc10de63325"
VERSION = "1.1.0"
TASK_ID = "5dc10de63325"
SUMMARY = "Cyan cells; rule outputs 5x5 with 2x2 tiles based on count // 4."

INVARIANTS = [
    "background is 0",
    "all non-bg cells are cyan(8)",
    ">=4 cyan cells (so output non-trivial)",
    "max cyan count <= 16 (so per-quad <=4 fits 2x2)",
]

DISTRIBUTIONS = ("scattered", "clustered", "corners", "row_aligned",
                 "diagonal", "checker")
DEGENERATE_TEXTURES = ("no_cyans", "full_grid", "single_cyan")
HELPFUL_TEXTURES = DISTRIBUTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..12", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 6..12", "valid": "5..18"},
    "n_cyans":        {"type": "int", "default": "rng 4..12", "valid": "4..16"},
    "distribution":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DISTRIBUTIONS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "force_div_4":    {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for distribution",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 6, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_cyans = int(overrides.get("n_cyans",
                                ctx.draw_int("n_cyans", 4, 12)))
    n_cyans = max(4, min(16, min(h * w - 1, n_cyans)))
    if bool(overrides.get("force_div_4", False)):
        n_cyans = (n_cyans // 4) * 4
        if n_cyans < 4:
            n_cyans = 4
    distribution = (overrides.get("texture") or
                    overrides.get("distribution")
                    or ctx.draw_choice("distribution",
                                       list(DISTRIBUTIONS)))
    g = full_grid(h, w, 0)
    positions = _pick_positions(distribution, h, w, n_cyans, rng)
    for r, c in positions[:n_cyans]:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = 8
    return g


def _pick_positions(distribution, h, w, n, rng):
    if distribution == "scattered":
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        return cells
    if distribution == "clustered":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(h) for c in range(w)]
        cells.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return cells
    if distribution == "corners":
        corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        rest = [(r, c) for r in range(h) for c in range(w)
                if (r, c) not in corners]
        rng.shuffle(rest)
        return corners + rest
    if distribution == "row_aligned":
        r = h // 2
        cells = [(r, c) for c in range(w)] + \
                [(r2, c) for r2 in range(h) if r2 != r for c in range(w)]
        return cells
    if distribution == "diagonal":
        diag = [(i, i) for i in range(min(h, w))]
        anti = [(i, min(h, w) - 1 - i) for i in range(min(h, w))]
        rest = [(r, c) for r in range(h) for c in range(w)
                if (r, c) not in diag and (r, c) not in anti]
        rng.shuffle(rest)
        return diag + anti + rest
    if distribution == "checker":
        cells = [(r, c) for r in range(h) for c in range(w)
                 if (r + c) % 2 == 0]
        rng.shuffle(cells)
        return cells
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_cyans":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    if name == "single_cyan":
        g[h // 2][w // 2] = 8
        return g
    return g
