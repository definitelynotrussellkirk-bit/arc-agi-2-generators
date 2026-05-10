"""Generator for 0ca9ddb6.

Rule: 0-cell adjacent (cardinally) to 1 -> 1. 0-cell adjacent
(diagonally) to 2 -> 2.

Combinatorial axes (8): grid_h/w, n_ones, n_twos, min_separation,
position_bias, palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_markers, all_adjacent, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3cf7be88b563"
VERSION = "1.1.0"
TASK_ID = "3cf7be88b563"
SUMMARY = "1-2 isolated 1-cells and 1-2 isolated 2-cells."

INVARIANTS = [
    "1-2 isolated 1-cells",
    "1-2 isolated 2-cells",
    "no two markers within Manhattan distance 3",
]

POSITION_BIASES = ("scattered", "spread", "centered", "corners")
DEGENERATE_TEXTURES = ("no_markers", "all_adjacent", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "n_ones":         {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_twos":         {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "min_separation": {"type": "int", "default": "3", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
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
        h_lo, h_hi, w_lo, w_hi = 5, 6, 7, 8
        no_lo, no_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 12, 11, 14
        no_lo, no_hi = 2, 3
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 8, 8, 10
        no_lo, no_hi = 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    sep = int(overrides.get("min_separation", 3))
    n_ones = int(overrides.get("n_ones",
                               ctx.draw_int("n_ones", no_lo, no_hi)))
    n_twos = int(overrides.get("n_twos",
                               ctx.draw_int("n_twos", no_lo, no_hi)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    placed = []
    for color, count in [(1, n_ones), (2, n_twos)]:
        for _ in range(count):
            for _ in range(40):
                r, c = _pick_cell(bias, h, w, rng)
                if all(abs(r - pr) + abs(c - pc) > sep for pr, pc in placed):
                    g[r][c] = color
                    placed.append((r, c))
                    break
    return g


def _pick_cell(bias, h, w, rng):
    if bias == "centered":
        r = rng.randint(max(1, h // 3), min(h - 2, 2 * h // 3))
        c = rng.randint(max(1, w // 3), min(w - 2, 2 * w // 3))
    elif bias == "corners":
        r = rng.choice([1, h - 2])
        c = rng.choice([1, w - 2])
    elif bias == "spread":
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
    else:
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
    return r, c


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        return g
    if name == "all_adjacent":
        g[3][3] = 1; g[3][4] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
