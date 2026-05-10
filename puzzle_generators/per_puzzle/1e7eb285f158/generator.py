"""Generator for e88171ec.

Rule: find largest all-zero rectangle (>=3x3); fill its interior with 8.

Combinatorial axes (8): grid_h/w, rect_h, rect_w, noise_density,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_empty, all_empty, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e7eb285f158"
VERSION = "1.1.0"
TASK_ID = "1e7eb285f158"
SUMMARY = "Sparse 0/2 noise with one larger rectangular all-0 region."

INVARIANTS = [
    "grid is 0/2 only",
    ">=1 explicit empty rectangular region of size >=3x3 (the target)",
    "the rest of the grid has scattered 2-cells (not too dense)",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
DEGENERATE_TEXTURES = ("no_empty", "all_empty", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "rect_h":         {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "rect_w":         {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "noise_density":  {"type": "float", "default": "0.55", "valid": "0.3..0.8"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
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
        h_lo, h_hi = 10, 12
        d_default = 0.4
        rh_lo, rh_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        d_default = 0.65
        rh_lo, rh_hi = 4, 7
    else:
        h_lo, h_hi = 12, 16
        d_default = 0.55
        rh_lo, rh_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    density = float(overrides.get("noise_density", d_default))
    density = max(0.2, min(0.8, density))
    g = [[2 if rng.random() < density else 0 for _ in range(w)] for _ in range(h)]
    rh = int(overrides.get("rect_h",
                           rng.randint(rh_lo, rh_hi)))
    rw = int(overrides.get("rect_w",
                           rng.randint(rh_lo, rh_hi)))
    rh = max(3, min(rh, h - 2))
    rw = max(3, min(rw, w - 2))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        r0 = max(1, (h - rh) // 2)
        c0 = max(1, (w - rw) // 2)
    elif bias == "corner":
        r0 = rng.choice([1, max(1, h - rh - 1)])
        c0 = rng.choice([1, max(1, w - rw - 1)])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            r0 = rng.choice([1, max(1, h - rh - 1)])
            c0 = rng.randint(1, max(1, w - rw - 1))
        else:
            r0 = rng.randint(1, max(1, h - rh - 1))
            c0 = rng.choice([1, max(1, w - rw - 1)])
    else:
        r0 = rng.randint(1, max(1, h - rh - 1))
        c0 = rng.randint(1, max(1, w - rw - 1))
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            g[r][c] = 0
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    if name == "no_empty":
        g = [[2] * w for _ in range(h)]
        return g
    if name == "all_empty":
        g = full_grid(h, w, 0)
        return g
    if name == "full_grid":
        return [[2] * w for _ in range(h)]
    return full_grid(h, w, 0)
