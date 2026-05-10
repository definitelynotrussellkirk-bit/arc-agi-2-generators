"""Generator for puzzle 1190e5a7.

Rule: find separator color (full row of one color != bg). Count
separator rows R and cols C. Output is (R+1) x (C+1) filled with bg.

Combinatorial axes (8): grid_h/w, n_sep_rows, n_sep_cols, bg_color,
sep_color, position_bias, anchor_corner, asymmetry_force.
Degenerates: no_separator, all_separator, asymmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1c1ef857c9e2"
VERSION = "1.1.0"
TASK_ID = "1c1ef857c9e2"
SUMMARY = "bg-filled grid divided by full sep rows + cols; rule outputs cell grid."

INVARIANTS = [
    "1-3 full rows of sep_color",
    "1-3 full cols of sep_color",
    "all other cells are bg",
    "bg != sep_color",
]

POSITION_BIASES = ("evenly_spaced", "centered", "edge_heavy",
                   "alternating", "scattered")
DEGENERATE_TEXTURES = ("no_separator", "all_separator", "asymmetric")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..16", "valid": "7..20"},
    "grid_w":         {"type": "int", "default": "rng 9..16", "valid": "7..20"},
    "n_sep_rows":     {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "n_sep_cols":     {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "bg_color":       {"type": "color", "default": "rng (≠sep)",
                       "valid": "1..9"},
    "sep_color":      {"type": "color", "default": "rng (≠bg)",
                       "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 10
    elif difficulty == "hard":
        h_lo, h_hi = 14, 20
    else:
        h_lo, h_hi = 9, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bg = int(overrides.get("bg_color",
                           ctx.draw_color("bg_color", exclude={0})))
    sep = int(overrides.get("sep_color",
                            ctx.draw_color("sep_color",
                                           exclude={0, bg})))
    if sep == bg:
        sep = next((c for c in [1, 2, 3, 4, 6, 7, 8, 9] if c != bg), 1)
    n_sep_rows = int(overrides.get("n_sep_rows",
                                   ctx.draw_int("n_sep_rows", 1, 3)))
    n_sep_cols = int(overrides.get("n_sep_cols",
                                   ctx.draw_int("n_sep_cols", 1, 3)))
    n_sep_rows = max(1, min(min(h - 2, 5), n_sep_rows))
    n_sep_cols = max(1, min(min(w - 2, 5), n_sep_cols))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    g = full_grid(h, w, bg)
    sep_rows = _pick_lines(bias, h, n_sep_rows, rng)
    sep_cols = _pick_lines(bias, w, n_sep_cols, rng)
    for r in sep_rows:
        for c in range(w):
            g[r][c] = sep
    for c in sep_cols:
        for r in range(h):
            g[r][c] = sep
    return g


def _pick_lines(bias, dim, n, rng):
    if bias == "evenly_spaced":
        step = max(1, dim // (n + 1))
        rs = [step * (i + 1) for i in range(n)]
        return sorted({r for r in rs if 1 <= r < dim - 1})[:n]
    if bias == "centered":
        center = dim // 2
        rs = [center - (n - 1) // 2 + i for i in range(n)]
        return sorted({r for r in rs if 1 <= r < dim - 1})[:n]
    if bias == "edge_heavy":
        rs = []
        if 1 < dim:
            rs.append(1)
        if dim - 2 > 1:
            rs.append(dim - 2)
        rs.extend(rng.sample(range(2, dim - 2), min(n - len(rs),
                                                      max(0, dim - 4))))
        return sorted(set(rs))[:n]
    if bias == "alternating":
        rs = [i for i in range(1, dim - 1) if i % 2 == 1]
        return rs[:n]
    return sorted(rng.sample(range(1, dim - 1), min(n, dim - 2)))


def _draw_from_degenerate(name, h, w, rng):
    bg, sep = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    g = full_grid(h, w, bg)
    if name == "no_separator":
        # No full row/col of sep color
        return g
    if name == "all_separator":
        # Every row and col is sep
        for r in range(h):
            for c in range(w):
                g[r][c] = sep
        return g
    if name == "asymmetric":
        # Many rows but no cols (or vice versa)
        for r in range(1, h - 1, 2):
            for c in range(w):
                g[r][c] = sep
        return g
    return g
