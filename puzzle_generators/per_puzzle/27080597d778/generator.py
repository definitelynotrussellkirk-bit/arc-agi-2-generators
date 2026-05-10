"""Generator for bbb1b8b6.

Rule: input is h × 9. Cols 0-3 = left, col 4 = 5s, cols 5-8 = right.
Where left and right are XOR-complementary, output combines them; else
returns left.

Combinatorial axes (8): grid_h, color_left, color_right,
fill_distribution, fill_layout, palette_kind, balance, decoy_density.
Degenerates: empty_halves, full_left, full_right.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "27080597d778"
VERSION = "1.1.0"
TASK_ID = "27080597d778"
SUMMARY = "h × 9 with complementary halves separated by 5-col; rule combines them."

INVARIANTS = [
    "h in [3, 8], w = 9",
    "col 4 is all 5s",
    "for every (r, c) with c in 0..3: exactly one of left[r][c] or right[r][c] is non-zero",
    "left uses one color, right uses one (possibly same) color",
]

FILL_LAYOUTS = ("scattered", "alternating", "left_heavy",
                "right_heavy", "diag", "checker")
DEGENERATE_TEXTURES = ("empty_halves", "full_left", "full_right")
HELPFUL_TEXTURES = FILL_LAYOUTS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 4..8", "valid": "3..10"},
    "color_left":        {"type": "color", "default": "rng (≠0,5)",
                          "valid": "1..9 (≠5)"},
    "color_right":       {"type": "color", "default": "rng (≠0,5)",
                          "valid": "1..9 (≠5)"},
    "fill_layout":       {"type": "str", "default": "rng helpful",
                          "valid": "|".join(FILL_LAYOUTS)},
    "balance":           {"type": "str", "default": "rng even|left|right",
                          "valid": "even|left|right"},
    "palette_kind":      {"type": "str", "default": "distinct",
                          "valid": "distinct|same"},
    "anchor_endpoints":  {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for fill_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 7, 10
    else:
        h_lo, h_hi = 4, 8
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = 9
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 ["distinct", "same"]))
    pool = [c for c in range(1, 10) if c != 5]
    rng.shuffle(pool)
    if palette_kind == "same":
        color_left = color_right = pool[0]
    else:
        color_left = int(overrides.get("color_left", pool[0]))
        color_right = int(overrides.get("color_right", pool[1]))
    layout = (overrides.get("texture") or overrides.get("fill_layout")
              or ctx.draw_choice("fill_layout", list(FILL_LAYOUTS)))
    balance = overrides.get("balance",
                            ctx.draw_choice("balance",
                                            ["even", "left", "right"]))
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(4):
            left_choice = _pick_left(layout, balance, r, c, h, rng)
            if left_choice:
                g[r][c] = color_left
            else:
                g[r][c + 5] = color_right
        g[r][4] = 5
    return g


def _pick_left(layout, balance, r, c, h, rng):
    if layout == "left_heavy":
        return True
    if layout == "right_heavy":
        return False
    if layout == "alternating":
        return (r + c) % 2 == 0
    if layout == "diag":
        return r >= c
    if layout == "checker":
        return (r + c) % 2 == 0
    if balance == "left":
        return rng.random() < 0.7
    if balance == "right":
        return rng.random() < 0.3
    return rng.random() < 0.5


def _draw_from_degenerate(name, h, rng):
    g = full_grid(h, 9, 0)
    color_left = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    color_right = rng.choice([c for c in [1, 2, 3, 4, 6, 7, 8, 9]
                              if c != color_left])
    for r in range(h):
        g[r][4] = 5
    if name == "empty_halves":
        return g
    if name == "full_left":
        for r in range(h):
            for c in range(4):
                g[r][c] = color_left
        return g
    if name == "full_right":
        for r in range(h):
            for c in range(4):
                g[r][c + 5] = color_right
        return g
    return g
