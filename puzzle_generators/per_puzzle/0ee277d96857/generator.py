"""Generator for ARC task 695367ec.

Rule: input is n × n. Output is 15 × 15: a periodic lattice with period
(n+1) — every (n+1)-th row and column is `g[0][0]` color, others 0.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0ee277d96857"
VERSION = "1.1.0"
TASK_ID = "0ee277d96857"
SUMMARY = "n × n solid tile; rule emits 15 × 15 with periodic lines (period n+1) in g[0][0]'s color."

INVARIANTS = [
    "input is square (n × n) with n in 2..5",
    "g[0][0] is non-zero (used as line color in output)",
    "input contents besides g[0][0] are decoy",
]

INPUT_DECORATIONS = ("solid", "noise_with_corner", "stripes_with_corner",
                     "checker_with_corner", "blob_with_corner")
DEGENERATE_TEXTURES = ("zero_corner", "all_zero", "all_solid_max_size")
HELPFUL_TEXTURES = INPUT_DECORATIONS

AXES = {
    "side":             {"type": "int", "default": "rng 2..5", "valid": "2..14"},
    "line_color":       {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "input_decoration": {"type": "str", "default": "rng helpful",
                         "valid": "|".join(INPUT_DECORATIONS)},
    "texture":          {"type": "str", "default": "alias for input_decoration",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        s_lo, s_hi = 2, 3
    elif difficulty == "hard":
        s_lo, s_hi = 4, 5
    else:
        s_lo, s_hi = 2, 5
    n = ctx.draw_int("side", s_lo, s_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, rng)
    line = int(overrides.get("line_color", ctx.draw_color("line_color", exclude={0})))
    decoration = (overrides.get("texture") or overrides.get("input_decoration")
                  or ctx.draw_choice("input_decoration", list(INPUT_DECORATIONS)))
    g = full_grid(n, n, line)
    if decoration == "solid":
        return g
    other = (line + 1) % 10
    if other == 0:
        other = 1
    if decoration == "noise_with_corner":
        for r in range(n):
            for c in range(n):
                if rng.random() < 0.5 and (r, c) != (0, 0):
                    g[r][c] = other
    elif decoration == "stripes_with_corner":
        for r in range(n):
            for c in range(n):
                if r % 2 == 1 and (r, c) != (0, 0):
                    g[r][c] = other
    elif decoration == "checker_with_corner":
        for r in range(n):
            for c in range(n):
                if (r + c) % 2 == 1 and (r, c) != (0, 0):
                    g[r][c] = other
    elif decoration == "blob_with_corner":
        # Lower-right block becomes other color.
        for r in range(n // 2, n):
            for c in range(n // 2, n):
                if (r, c) != (0, 0):
                    g[r][c] = other
    g[0][0] = line  # ensure g[0][0] is the line color
    return g


def _draw_from_degenerate(name, n, rng):
    if name == "zero_corner":
        # g[0][0] is 0 → output line color is 0 → output all-0.
        g = full_grid(n, n, rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        g[0][0] = 0
        return g
    if name == "all_zero":
        return full_grid(n, n, 0)
    if name == "all_solid_max_size":
        return full_grid(5, 5, rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    return full_grid(n, n, 1)
