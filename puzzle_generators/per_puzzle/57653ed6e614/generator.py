"""Generator for ARC task 29c11459.

Rule: for each row, lv = g[r][0], rv = g[r][w-1]. If both non-zero:
  c < mid → lv; c == mid → 5; c > mid → rv.
Else keep cell as-is. (mid = w/2 with integer division.)

Combinatorial axes: grid_h, grid_w (odd ≥ 3), left_color, right_color,
n_active_rows (rows with both edges non-zero), edge_distribution.
Degenerates: no_active_rows (rule no-op), all_rows_active,
single_color_edges (lv == rv).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "57653ed6e614"
VERSION = "1.1.0"
TASK_ID = "57653ed6e614"
SUMMARY = "Rows with non-zero left+right edges become left/right bands split by 5 in the middle."

INVARIANTS = [
    "grid width is odd ≥ 3 (so middle col is well-defined)",
    "≥1 row has both edges non-zero (rule has visible effect)",
    "left and right edge colors are distinct (else output looks like a fill)",
]

EDGE_DISTRIBUTIONS = ("all_active", "half_active", "few_active",
                     "alternating_inactive")
DEGENERATE_TEXTURES = ("no_active_rows", "single_color_edges", "single_active_row")
HELPFUL_TEXTURES = EDGE_DISTRIBUTIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 3..14", "valid": "1..18"},
    "grid_w":             {"type": "choice", "default": "rng odd 5..15", "valid": "5|7|9|11|13|15"},
    "left_color":         {"type": "color", "default": "rng (≠0,5)", "valid": "1..9 (≠5)"},
    "right_color":        {"type": "color", "default": "rng (≠0,5,left)", "valid": "1..9"},
    "edge_distribution":  {"type": "str", "default": "rng helpful",
                           "valid": "|".join(EDGE_DISTRIBUTIONS)},
    "interior_decoy_density": {"type": "float", "default": "rng 0..0.2", "valid": "0..0.5"},
    "texture":            {"type": "str", "default": "alias for edge_distribution",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_choices = 3, 6, [5, 7]
    elif difficulty == "hard":
        h_lo, h_hi, w_choices = 11, 14, [11, 13, 15]
    else:
        h_lo, h_hi, w_choices = 3, 14, [5, 7, 9, 11, 13, 15]
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_choice("grid_w", w_choices)
    rng = ctx.draw_rng("rows")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    left = int(overrides.get("left_color", ctx.draw_color("left_color", exclude={0, 5})))
    right = int(overrides.get("right_color", ctx.draw_color("right_color", exclude={0, 5, left})))
    distribution = (overrides.get("texture") or overrides.get("edge_distribution")
                    or ctx.draw_choice("edge_distribution", list(EDGE_DISTRIBUTIONS)))
    decoy_d = float(overrides.get("interior_decoy_density",
                                  ctx.draw_rng("interior_decoy_density").uniform(0.0, 0.2)))
    g = full_grid(h, w, 0)
    for r in range(h):
        active = _is_active(distribution, r, h, rng)
        if active:
            g[r][0] = left
            g[r][w - 1] = right
        if decoy_d > 0:
            for c in range(1, w - 1):
                if rng.random() < decoy_d:
                    g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # Force at least one active row.
    if not any(g[r][0] != 0 and g[r][w - 1] != 0 for r in range(h)):
        g[0][0] = left
        g[0][w - 1] = right
    return g


def _is_active(dist, r, h, rng):
    if dist == "all_active":
        return True
    if dist == "half_active":
        return r < h // 2
    if dist == "few_active":
        return rng.random() < 0.4
    if dist == "alternating_inactive":
        return r % 2 == 0
    return rng.random() < 0.6


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_active_rows":
        # No row has both edges non-zero — rule is identity.
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        return g
    if name == "single_color_edges":
        c0 = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        for r in range(h):
            g[r][0] = c0
            g[r][w - 1] = c0
        return g
    if name == "single_active_row":
        left = 1; right = 2
        g[0][0] = left
        g[0][w - 1] = right
        return g
    return g
