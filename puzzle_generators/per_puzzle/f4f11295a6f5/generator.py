"""Generator for ARC task 8f2ea7aa.

Rule: crop input to its non-bg bbox (= pattern of side N). Build N²×N²
output where each block (br, bc) shows the pattern if pattern[br][bc] is
non-bg, else all bg.

Combinatorial axes (8): pattern_size, fg_color, fg_density,
pattern_layout, padding_top, padding_left, decoy_density, edge_force.
Degenerates: empty_pattern, full_pattern, single_cell_pattern.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f4f11295a6f5"
VERSION = "1.1.0"
TASK_ID = "f4f11295a6f5"
SUMMARY = "A padded NxN binary pattern; cropped pattern controls self-tile."

INVARIANTS = [
    "background is 0",
    "foreground pattern has a stable bbox of side >=2",
    "cropped pattern contains both 0 and non-0 cells (so tile is non-trivial)",
    "padding around pattern is bg",
]

PATTERN_LAYOUTS = ("random", "diag", "anti_diag", "cross", "L_shape", "checker")
DEGENERATE_TEXTURES = ("empty_pattern", "full_pattern", "single_cell_pattern")
HELPFUL_TEXTURES = PATTERN_LAYOUTS

AXES = {
    "pattern_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "fg_color":       {"type": "color", "default": "rng", "valid": "1..9"},
    "fg_density":     {"type": "float", "default": "rng 0.35..0.7", "valid": "0..1"},
    "pattern_layout": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATTERN_LAYOUTS)},
    "padding_top":    {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "padding_left":   {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "decoy_density":  {"type": "float", "default": "0", "valid": "0..0.1"},
    "edge_force":     {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for pattern_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi = 2, 3
    elif difficulty == "hard":
        n_lo, n_hi = 4, 5
    else:
        n_lo, n_hi = 2, 4
    rng = ctx.draw_rng("pattern")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    n = int(overrides.get("pattern_size", ctx.draw_int("pattern_size", n_lo, n_hi)))
    n = max(2, min(5, n))
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    layout = (overrides.get("texture") or overrides.get("pattern_layout")
              or ctx.draw_choice("pattern_layout", list(PATTERN_LAYOUTS)))
    density = float(overrides.get("fg_density",
                                  ctx.draw_rng("fg_density").uniform(0.35, 0.7)))
    pad_t = int(overrides.get("padding_top", ctx.draw_int("padding_top", 1, 3)))
    pad_l = int(overrides.get("padding_left", ctx.draw_int("padding_left", 1, 3)))
    edge_force = bool(overrides.get("edge_force", True))
    h = pad_t + n + rng.randint(1, 3)
    w = pad_l + n + rng.randint(1, 3)
    g = full_grid(h, w, 0)
    pattern = _build_pattern(layout, n, density, edge_force, rng)
    for r in range(n):
        for c in range(n):
            if pattern[r][c]:
                g[pad_t + r][pad_l + c] = fg
    has_zero = any(0 == g[pad_t + r][pad_l + c]
                   for r in range(n) for c in range(n))
    has_fg = any(g[pad_t + r][pad_l + c] == fg
                 for r in range(n) for c in range(n))
    if not has_zero:
        g[pad_t][pad_l + n - 1] = 0
    if not has_fg:
        g[pad_t][pad_l] = fg
    return g


def _build_pattern(layout, n, density, edge_force, rng):
    p = [[0] * n for _ in range(n)]
    if layout == "diag":
        for i in range(n):
            p[i][i] = 1
    elif layout == "anti_diag":
        for i in range(n):
            p[i][n - 1 - i] = 1
    elif layout == "cross":
        m = n // 2
        for i in range(n):
            p[m][i] = 1
            p[i][m] = 1
    elif layout == "L_shape":
        for i in range(n):
            p[i][0] = 1
            p[n - 1][i] = 1
    elif layout == "checker":
        for r in range(n):
            for c in range(n):
                p[r][c] = 1 if (r + c) % 2 == 0 else 0
    else:  # random
        for r in range(n):
            for c in range(n):
                p[r][c] = 1 if rng.random() < density else 0
    if edge_force:
        p[0][0] = 1
        p[n - 1][n - 1] = 1
    return p


def _draw_from_degenerate(name, rng):
    if name == "empty_pattern":
        g = full_grid(7, 7, 0)
        fg = rng.choice([1, 3, 4, 6, 7, 8, 9])
        g[3][3] = fg
        return g
    if name == "full_pattern":
        g = full_grid(7, 7, 0)
        fg = rng.choice([1, 3, 4, 6, 7, 8, 9])
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = fg
        return g
    if name == "single_cell_pattern":
        g = full_grid(6, 6, 0)
        fg = rng.choice([1, 3, 4, 6, 7, 8, 9])
        g[2][2] = fg
        g[3][3] = fg
        return g
    return [[0]]
