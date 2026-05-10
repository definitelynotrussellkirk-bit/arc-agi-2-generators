"""Generator for bdad9b1f.

Rule: find col with 8s and row with 2s. Output: full col with 8s,
full row with 2s, intersection cell = 4.

Combinatorial axes (8): grid_h/w, n_eights, n_twos, col8_position,
row2_position, position_bias, decoy_density, asymmetry.
Degenerates: no_eights, no_twos, all_intersection.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c99f630b7541"
VERSION = "1.1.0"
TASK_ID = "c99f630b7541"
SUMMARY = "Some 8s in one column, 2s in one row; rule paints the cross with 4 at intersection."

INVARIANTS = [
    "background is 0",
    "all 8-cells share one column",
    "all 2-cells share one row",
    ">=2 8-cells and >=2 2-cells (so the cross is non-trivial)",
    "no other non-bg cells",
    "no 4 in input (rule writes 4 for intersection)",
]

POSITION_BIAS = ("center", "spread", "edge")
DEGENERATE_TEXTURES = ("no_eights", "no_twos", "all_intersection")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 5..12", "valid": "4..16"},
    "grid_w":             {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "n_eights":           {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "n_twos":             {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "col8_position":      {"type": "str", "default": "rng helpful",
                           "valid": "|".join(POSITION_BIAS)},
    "row2_position":      {"type": "str", "default": "rng helpful",
                           "valid": "|".join(POSITION_BIAS)},
    "asymmetry":          {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "anchor_corner":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for col8_position",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 4, 6, 5, 8
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 16, 13, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 12, 6, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_eights = int(overrides.get("n_eights",
                                 ctx.draw_int("n_eights", 2, 4)))
    n_twos = int(overrides.get("n_twos",
                               ctx.draw_int("n_twos", 2, 4)))
    n_eights = max(2, min(h - 1, n_eights))
    n_twos = max(2, min(w - 1, n_twos))
    col8_pos = (overrides.get("texture") or
                overrides.get("col8_position")
                or ctx.draw_choice("col8_position", list(POSITION_BIAS)))
    row2_pos = overrides.get("row2_position",
                             ctx.draw_choice("row2_position",
                                             list(POSITION_BIAS)))
    col8 = _pick_col(col8_pos, w, rng)
    row2 = _pick_row(row2_pos, h, rng)
    g = full_grid(h, w, 0)
    rs = rng.sample([r for r in range(h) if r != row2],
                    min(n_eights, max(1, h - 1)))
    for r in rs:
        g[r][col8] = 8
    cs = rng.sample([c for c in range(w) if c != col8],
                    min(n_twos, max(1, w - 1)))
    for c in cs:
        g[row2][c] = 2
    return g


def _pick_col(bias, w, rng):
    if bias == "center":
        return w // 2
    if bias == "edge":
        return rng.choice([0, w - 1])
    return rng.randint(0, w - 1)


def _pick_row(bias, h, rng):
    if bias == "center":
        return h // 2
    if bias == "edge":
        return rng.choice([0, h - 1])
    return rng.randint(0, h - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    col8 = w // 2
    row2 = h // 2
    if name == "no_eights":
        for c in range(w):
            if c != col8:
                g[row2][c] = 2
        return g
    if name == "no_twos":
        for r in range(h):
            if r != row2:
                g[r][col8] = 8
        return g
    if name == "all_intersection":
        # col8 == row2's col → no clear cross
        for r in range(h):
            g[r][col8] = 8
        for c in range(w):
            g[row2][c] = 2
        return g
    return g
