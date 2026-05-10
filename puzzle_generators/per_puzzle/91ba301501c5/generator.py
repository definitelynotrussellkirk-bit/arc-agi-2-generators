"""Generator for 8d510a79.

Rule: horizontal gray(5) line + blue(1) and red(2) cells; rule extends
blue away from the line vertically, red toward it (until hit).

Combinatorial axes (8): grid_h/w, line_position, n_blue, n_red,
side_balance, palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_line, no_marks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "91ba301501c5"
VERSION = "1.1.0"
TASK_ID = "91ba301501c5"
SUMMARY = "Horizontal gray line + blue/red cells; rule extends blue away, red toward the line."

INVARIANTS = [
    "exactly one row entirely gray(5)",
    "gray line is interior (not at row 0 or h-1)",
    ">=2 blue(1) cells",
    ">=2 red(2) cells",
    "blue and red cells are not on the gray line itself",
]

LINE_POSITIONS = ("center", "upper", "lower", "rng")
SIDE_BALANCES = ("balanced", "above_only", "below_only", "skewed")
DEGENERATE_TEXTURES = ("no_line", "no_marks", "full_grid")
HELPFUL_TEXTURES = LINE_POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "line_position":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LINE_POSITIONS)},
    "n_blue":         {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "n_red":          {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "side_balance":   {"type": "str", "default": "rng",
                       "valid": "|".join(SIDE_BALANCES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for line_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 7, 9, 6, 8
        nb_lo, nb_hi, nr_lo, nr_hi = 2, 2, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 12, 16
        nb_lo, nb_hi, nr_lo, nr_hi = 3, 6, 3, 6
    else:
        h_lo, h_hi, w_lo, w_hi = 9, 14, 8, 12
        nb_lo, nb_hi, nr_lo, nr_hi = 2, 4, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    line_pos = (overrides.get("texture") or
                overrides.get("line_position")
                or ctx.draw_choice("line_position", list(LINE_POSITIONS)))
    if line_pos == "center":
        line_r = h // 2
    elif line_pos == "upper":
        line_r = max(2, h // 3)
    elif line_pos == "lower":
        line_r = min(h - 3, 2 * h // 3)
    else:
        line_r = rng.randint(2, h - 3)
    line_r = max(2, min(line_r, h - 3))
    g = full_grid(h, w, 0)
    for c in range(w):
        g[line_r][c] = 5
    n_blue = int(overrides.get("n_blue",
                               ctx.draw_int("n_blue", nb_lo, nb_hi)))
    n_red = int(overrides.get("n_red",
                              ctx.draw_int("n_red", nr_lo, nr_hi)))
    n_blue = max(2, min(8, n_blue))
    n_red = max(2, min(8, n_red))
    balance = overrides.get("side_balance",
                            ctx.draw_choice("side_balance",
                                            list(SIDE_BALANCES)))
    _place_marks(g, n_blue, 1, balance, line_r, h, w, rng)
    _place_marks(g, n_red, 2, balance, line_r, h, w, rng)
    return g


def _place_marks(g, n, color, balance, line_r, h, w, rng):
    placed = 0
    for _ in range(n * 8):
        if placed >= n:
            break
        if balance == "above_only":
            r = rng.randint(0, line_r - 1)
        elif balance == "below_only":
            r = rng.randint(line_r + 1, h - 1)
        elif balance == "skewed":
            r = rng.randint(0, line_r - 1) if rng.random() < 0.7 else rng.randint(line_r + 1, h - 1)
        else:
            r = rng.choice([rng.randint(0, line_r - 1),
                            rng.randint(line_r + 1, h - 1)])
        c = rng.randint(0, w - 1)
        if r != line_r and g[r][c] == 0:
            g[r][c] = color
            placed += 1


def _draw_from_degenerate(name, rng):
    h, w = 11, 9
    g = full_grid(h, w, 0)
    if name == "no_line":
        g[2][2] = 1
        g[6][6] = 2
        return g
    if name == "no_marks":
        for c in range(w):
            g[5][c] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
