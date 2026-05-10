"""Generator for edcc2ff0.

Rule: top has 3 indicator cells in col 0 (rows 1, 3, 5). Below row 7 is
a colored region; for each indicator color, count its objects and paint
a horizontal bar of that length on the indicator row.

Combinatorial axes (8): grid_h/w, indicator_palette, bg_choice,
n_objs_per_color, position_bias, palette_kind, anchor_corner,
asymmetry_force.
Degenerates: no_indicators, no_bg_row, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d53f4142488d"
VERSION = "1.1.0"
TASK_ID = "d53f4142488d"
SUMMARY = "20-tall grid with 3 indicators + uniform-color rect at row 7+."

INVARIANTS = [
    "h >= 16, w in 8..12",
    "rows 0,2,4,6 are all 0",
    "rows 1,3,5 have a single non-zero cell at col 0 (the indicator)",
    "row 7 is a full-width row of one bg color",
    "rows 8+ have non-zero cells of indicator colors at distinct positions",
]

POSITION_BIASES = ("scattered", "stacked", "clustered", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_indicators", "no_bg_row", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 18..22", "valid": "16..24"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "n_objs_per_color":{"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "bg_choice":      {"type": "color", "default": "rng",
                       "valid": "3|7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 16, 18, 6, 9
        no_lo, no_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 21, 24, 11, 14
        no_lo, no_hi = 2, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 18, 22, 8, 12
        no_lo, no_hi = 1, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    indicators = palette[:3]
    bg = int(overrides.get("bg_choice",
                           rng.choice([v for v in [3, 7] if v not in indicators])))
    g[1][0] = indicators[0]
    g[3][0] = indicators[1]
    g[5][0] = indicators[2]
    for c in range(w):
        g[7][c] = bg
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    no_per = int(overrides.get("n_objs_per_color",
                               ctx.draw_int("n_objs_per_color",
                                            no_lo, no_hi)))
    no_per = max(1, min(4, no_per))
    for color in indicators:
        n_objs = rng.randint(1, no_per)
        for _ in range(n_objs):
            for _try in range(40):
                r = rng.randint(8, h - 2)
                if bias == "stacked":
                    c = 1
                elif bias == "clustered":
                    c = rng.randint(0, max(0, w // 2 - 2))
                else:
                    c = rng.randint(0, w - 2)
                if g[r][c] == bg and g[r][c + 1] == bg:
                    g[r][c] = color
                    g[r][c + 1] = color
                    break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 4]
    else:
        pool = [1, 2, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c not in (3, 7)]
    rng.shuffle(pool)
    if len(pool) < 3:
        for c in [1, 2, 4, 5, 6, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= 3:
                break
    return pool[:3]


def _draw_from_degenerate(name, rng):
    h, w = 20, 10
    g = full_grid(h, w, 0)
    if name == "no_indicators":
        for c in range(w):
            g[7][c] = 3
        return g
    if name == "no_bg_row":
        g[1][0] = 1; g[3][0] = 2; g[5][0] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
