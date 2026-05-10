"""Generator for puzzle 7ec998c9.

Rule: bg = corner color. Find single non-bg dot. If dot.r == dot.c
(diagonal), draw 1s on top + bottom anti-corner. Otherwise draw cross.

Combinatorial axes (8): grid_n, bg_color, dot_color, dot_position,
dot_quadrant, on_diagonal, anchor_corner, palette_kind.
Degenerates: no_dot, dot_on_edge, multiple_dots.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f1347e0836ec"
VERSION = "1.1.0"
TASK_ID = "f1347e0836ec"
SUMMARY = "Solid bg + 1 interior dot; rule draws cross or anti-corners."

INVARIANTS = [
    "h = w (square)",
    "all cells = bg except 1 dot",
    "dot is at interior position (1 <= r,c <= n-2)",
    "bg != dot_color",
]

DOT_POSITIONS = ("center", "diagonal", "anti_diagonal", "off_diagonal",
                 "near_edge", "near_corner")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dot", "dot_on_edge", "multiple_dots")
HELPFUL_TEXTURES = DOT_POSITIONS

AXES = {
    "grid_n":         {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "bg_color":       {"type": "color", "default": "rng (≠dot)",
                       "valid": "1..9"},
    "dot_color":      {"type": "color", "default": "rng (≠bg)",
                       "valid": "1..9"},
    "dot_position":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DOT_POSITIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "on_diagonal":    {"type": "bool", "default": "rng",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for dot_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi = 5, 7
    elif difficulty == "hard":
        n_lo, n_hi = 12, 16
    else:
        n_lo, n_hi = 6, 12
    n = int(ctx.draw_int("grid_n", n_lo, n_hi))
    n = max(5, min(16, n))
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    bg = int(overrides.get("bg_color", palette[0]))
    dot_color = int(overrides.get("dot_color",
                                  next((c for c in palette if c != bg),
                                       1)))
    if dot_color == bg:
        dot_color = next((c for c in palette if c != bg), 1)
    pos = (overrides.get("texture") or
           overrides.get("dot_position")
           or ctx.draw_choice("dot_position", list(DOT_POSITIONS)))
    g = [[bg] * n for _ in range(n)]
    r, c = _pick_dot(pos, n, rng)
    g[r][c] = dot_color
    return g


def _pick_dot(pos, n, rng):
    if pos == "center":
        return n // 2, n // 2
    if pos == "diagonal":
        i = rng.randint(1, n - 2)
        return i, i
    if pos == "anti_diagonal":
        i = rng.randint(1, n - 2)
        return i, n - 1 - i
    if pos == "off_diagonal":
        for _ in range(20):
            r = rng.randint(1, n - 2)
            c = rng.randint(1, n - 2)
            if r != c and r != n - 1 - c:
                return r, c
        return 1, 2
    if pos == "near_edge":
        side = rng.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return 1, rng.randint(1, n - 2)
        if side == "bottom":
            return n - 2, rng.randint(1, n - 2)
        if side == "left":
            return rng.randint(1, n - 2), 1
        return rng.randint(1, n - 2), n - 2
    if pos == "near_corner":
        return rng.choice([(1, 1), (1, n - 2), (n - 2, 1), (n - 2, n - 2)])
    return rng.randint(1, n - 2), rng.randint(1, n - 2)


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, n, rng):
    bg = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    g = [[bg] * n for _ in range(n)]
    dot_color = next((c for c in [2, 3, 4, 6, 7, 8, 9] if c != bg), 2)
    if name == "no_dot":
        return g
    if name == "dot_on_edge":
        g[0][n // 2] = dot_color
        return g
    if name == "multiple_dots":
        for r, c in [(1, 1), (n - 2, n - 2)]:
            g[r][c] = dot_color
        return g
    return g
