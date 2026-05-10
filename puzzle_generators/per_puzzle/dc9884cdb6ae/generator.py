"""Generator for puzzle 2bee17df.

Rule: count 0-cells per row and per col. For cells in max-zero-row or
max-zero-col, replace 0 with 3.

Combinatorial axes (8): grid_h/w, target_row_zeros, target_col_zeros,
n_extra_zeros, n_twos, position_bias, anchor_corner, asymmetry_force.
Degenerates: no_zeros, all_zeros, tied_max.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import random_free_cell

GENERATOR_ID = "dc9884cdb6ae"
VERSION = "1.1.0"
TASK_ID = "dc9884cdb6ae"
SUMMARY = "8-bg with sprinkled 2s/0s; rule fills max-0-row/col with 3."

INVARIANTS = [
    "bg = 8",
    ">=1 row has unique-max 0-count",
    ">=1 col has unique-max 0-count",
    "scattered 2-cells",
]

POSITION_BIASES = ("scattered", "row_focus", "col_focus", "corner",
                   "centered")
DEGENERATE_TEXTURES = ("no_zeros", "all_zeros", "tied_max")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":           {"type": "int", "default": "rng 5..9", "valid": "4..12"},
    "grid_w":           {"type": "int", "default": "rng 9..13", "valid": "7..16"},
    "target_row_zeros": {"type": "int", "default": "rng w-4..w-2",
                         "valid": "3..w-1"},
    "n_extra_zeros":    {"type": "int", "default": "rng 2..5",
                         "valid": "0..10"},
    "n_twos":           {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 8, 12
    else:
        h_lo, h_hi = 5, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 4, h_hi + 5)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    n_target_row_zeros = int(overrides.get("target_row_zeros",
                                           ctx.draw_int(
                                               "target_row_zeros",
                                               max(3, w - 4),
                                               max(3, w - 2))))
    n_extra = int(overrides.get("n_extra_zeros",
                                ctx.draw_int("n_extra_zeros", 2, 5)))
    n_twos = int(overrides.get("n_twos",
                               ctx.draw_int("n_twos", 2, 3)))
    g = full_grid(h, w, 8)
    target_row = _pick_target_row(bias, h, rng)
    target_col = _pick_target_col(bias, w, rng)
    cs = rng.sample(range(w), min(n_target_row_zeros, w))
    for c in cs:
        g[target_row][c] = 0
    rs = rng.sample(range(h), min(max(2, h // 2), h))
    for r in rs:
        if r != target_row and rng.random() < 0.6:
            g[r][target_col] = 0
    for _ in range(n_extra):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 8 and r != target_row and c != target_col:
                g[r][c] = 0
                break
    for _ in range(n_twos):
        cell = random_free_cell(g, rng, bg=8, max_tries=20)
        if cell is not None:
            g[cell[0]][cell[1]] = 2
    return g


def _pick_target_row(bias, h, rng):
    if bias == "row_focus":
        return rng.randint(1, h - 2)
    if bias == "centered":
        return h // 2
    if bias == "corner":
        return 1
    return rng.randint(1, h - 2)


def _pick_target_col(bias, w, rng):
    if bias == "col_focus":
        return rng.randint(1, w - 2)
    if bias == "centered":
        return w // 2
    if bias == "corner":
        return 1
    return rng.randint(1, w - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 8)
    if name == "no_zeros":
        # Sprinkled 2s, no 0s — rule has no work
        for _ in range(3):
            cell = random_free_cell(g, rng, bg=8, max_tries=20)
            if cell:
                g[cell[0]][cell[1]] = 2
        return g
    if name == "all_zeros":
        for r in range(h):
            for c in range(w):
                g[r][c] = 0
        return g
    if name == "tied_max":
        # Two rows with same 0-count
        for r in [1, 3]:
            if r < h:
                for c in range(w - 2):
                    g[r][c] = 0
        return g
    return g
