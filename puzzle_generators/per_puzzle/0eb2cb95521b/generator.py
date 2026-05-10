"""Generator for puzzle 137f0df0.

Rule: 4 gray(5) cells form an axis-aligned rectangle (2 rows, 2 cols).
Output fills interior + edge gap regions with red/blue.

Combinatorial axes (8): grid_size, first_r, second_r, first_c, second_c,
gray_color, anchor_corner, asymmetry_force.
Degenerates: no_grays, single_gray, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0eb2cb95521b"
VERSION = "1.1.0"
TASK_ID = "0eb2cb95521b"
SUMMARY = "4 gray dots forming a rect; rule fills regions with red/blue."

INVARIANTS = [
    "background is 0",
    "exactly 4 gray(5) cells at corners of an axis-aligned rect",
    "rect interior >=1 cell wide AND tall",
    "rect doesn't touch grid edge",
]

POSITION_BIASES = ("scattered", "centered", "tight", "spread")
DEGENERATE_TEXTURES = ("no_grays", "single_gray", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_size":      {"type": "int", "default": "rng 7..14", "valid": "7..18"},
    "first_r":        {"type": "int", "default": "auto",
                       "valid": "1..size//2-1"},
    "second_r":       {"type": "int", "default": "auto",
                       "valid": "size//2+1..size-2"},
    "first_c":        {"type": "int", "default": "auto",
                       "valid": "1..size//2-1"},
    "second_c":       {"type": "int", "default": "auto",
                       "valid": "size//2+1..size-2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
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
    if difficulty == "easy":
        size_lo, size_hi = 7, 9
    elif difficulty == "hard":
        size_lo, size_hi = 12, 18
    else:
        size_lo, size_hi = 7, 14
    size = ctx.draw_int("grid_size", size_lo, size_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], size, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(size, size, 0)
    fr, sr, fc, sc = _pick_positions(bias, size, rng)
    if "first_r" in overrides:
        fr = max(1, min(size - 2, int(overrides["first_r"])))
    if "second_r" in overrides:
        sr = max(fr + 1, min(size - 2, int(overrides["second_r"])))
    if "first_c" in overrides:
        fc = max(1, min(size - 2, int(overrides["first_c"])))
    if "second_c" in overrides:
        sc = max(fc + 1, min(size - 2, int(overrides["second_c"])))
    for r in (fr, sr):
        for c in (fc, sc):
            g[r][c] = 5
    return g


def _pick_positions(bias, size, rng):
    if bias == "centered":
        center = size // 2
        return center - 1, center + 1, center - 1, center + 1
    if bias == "tight":
        fr = rng.randint(1, size // 2 - 1)
        sr = fr + 2
        fc = rng.randint(1, size // 2 - 1)
        sc = fc + 2
        if sr > size - 2:
            sr = size - 2
        if sc > size - 2:
            sc = size - 2
        return fr, sr, fc, sc
    if bias == "spread":
        return 1, size - 2, 1, size - 2
    fr = rng.randint(1, max(1, size // 2 - 1))
    sr = rng.randint(size // 2 + 1, max(size // 2 + 1, size - 2))
    fc = rng.randint(1, max(1, size // 2 - 1))
    sc = rng.randint(size // 2 + 1, max(size // 2 + 1, size - 2))
    return fr, sr, fc, sc


def _draw_from_degenerate(name, size, rng):
    g = full_grid(size, size, 0)
    if name == "no_grays":
        return g
    if name == "single_gray":
        g[size // 2][size // 2] = 5
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 5
        return g
    return g
