"""Generator for puzzle 9c56f360.

Rule: per row, find the 3-cells (single cell at right). Slide left
until hitting an 8 (stop just past it) or to col 0.

Combinatorial axes (8): grid_h/w, n_threes, n_eights, eight_density,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_threes, no_eights, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "536de2f7591b"
VERSION = "1.1.0"
TASK_ID = "536de2f7591b"
SUMMARY = "3 at right + 8 obstacles; rule slides 3 left until hitting 8 or wall."

INVARIANTS = [
    "background is 0",
    "1-4 rows have a single 3-cell at col w-1",
    "scattered 8-cells across grid",
    "3-rows have 0-3 8-cells to their left",
]

POSITION_BIASES = ("scattered", "left_heavy", "right_heavy", "diagonal",
                   "centered")
DEGENERATE_TEXTURES = ("no_threes", "no_eights", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "n_threes":       {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "n_eights":       {"type": "int", "default": "rng h..h+h/2",
                       "valid": "1..h*w/2"},
    "eight_density":  {"type": "float", "default": "rng 0.15..0.3",
                       "valid": "0.05..0.5"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 16
    else:
        h_lo, h_hi = 6, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_threes = int(overrides.get("n_threes",
                                 ctx.draw_int("n_threes", 2, 4)))
    n_threes = max(1, min(min(h, 6), n_threes))
    eight_d = float(overrides.get("eight_density",
                                  ctx.draw_rng("eight_density")
                                  .uniform(0.15, 0.3)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    n_eights = int(overrides.get("n_eights",
                                  int(h * w * eight_d / 2)))
    n_eights = max(1, min(h * w // 2, n_eights))
    for _ in range(n_eights):
        r, c = _pick_eight_position(bias, h, w, rng)
        if g[r][c] == 0:
            g[r][c] = 8
    rows = rng.sample(range(h), n_threes)
    for r in rows:
        if g[r][w - 1] == 0:
            g[r][w - 1] = 3
    return g


def _pick_eight_position(bias, h, w, rng):
    if bias == "left_heavy":
        return rng.randint(0, h - 1), rng.randint(0, max(0, w // 3))
    if bias == "right_heavy":
        return rng.randint(0, h - 1), rng.randint(2 * w // 3, w - 2)
    if bias == "diagonal":
        i = rng.randint(0, min(h, w) - 1)
        return i, max(0, i - 1)
    if bias == "centered":
        return rng.randint(0, h - 1), max(0, w // 2 + rng.randint(-2, 2))
    return rng.randint(0, h - 1), rng.randint(0, w - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_threes":
        # Just 8s, no 3 at col w-1
        for _ in range(h):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 2)
            if g[r][c] == 0:
                g[r][c] = 8
        return g
    if name == "no_eights":
        for r in range(min(h, 3)):
            g[r][w - 1] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8 if (r + c) % 2 == 0 else 3
        return g
    return g
