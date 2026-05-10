"""Generator for 32597951.

Rule: bbox of 8-cells; for each 1-cell strictly inside (or in bbox),
recolor to 3.

Combinatorial axes (8): grid_h/w, ones_density, blob_size, blob_position,
palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_eights, blob_outside, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "113d9bb402d3"
VERSION = "1.1.0"
TASK_ID = "113d9bb402d3"
SUMMARY = "Many 1-cells scattered + a small 8-blob region marking a recolor zone."

INVARIANTS = [
    "many 1-cells (>=10) scattered throughout",
    ">=3 cells of color 8 with bbox covering some 1-cells",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
DEGENERATE_TEXTURES = ("no_eights", "blob_outside", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "10..20"},
    "ones_density":   {"type": "float", "default": "rng 0.4..0.6", "valid": "0.2..0.8"},
    "blob_size":      {"type": "int", "default": "rng 3..5", "valid": "3..8"},
    "blob_position":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "warm|cool|broad|primary"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for blob_position",
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
        h_lo, h_hi, w_lo, w_hi = 5, 6, 10, 13
        d_lo, d_hi = 0.30, 0.45
        b_lo, b_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 16, 20
        d_lo, d_hi = 0.50, 0.70
        b_lo, b_hi = 4, 7
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 8, 13, 16
        d_lo, d_hi = 0.40, 0.60
        b_lo, b_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    density = float(overrides.get("ones_density", rng.uniform(d_lo, d_hi)))
    n_ones = int(density * h * w)
    for _ in range(n_ones):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        g[r][c] = 1
    bias = (overrides.get("texture") or
            overrides.get("blob_position")
            or ctx.draw_choice("blob_position", list(POSITION_BIASES)))
    blob_size = int(overrides.get("blob_size",
                                  ctx.draw_int("blob_size", b_lo, b_hi)))
    blob_size = max(3, min(8, blob_size))
    r0, c0 = _pick_blob_pos(bias, h, w, rng)
    for _ in range(blob_size):
        dr = rng.randint(0, 2); dc = rng.randint(0, 3)
        rr = max(0, min(h - 1, r0 + dr))
        cc = max(0, min(w - 1, c0 + dc))
        g[rr][cc] = 8
    return g


def _pick_blob_pos(bias, h, w, rng):
    if bias == "centered":
        r0 = max(0, h // 2 - 1); c0 = max(0, w // 2 - 1)
    elif bias == "corner":
        r0 = rng.choice([0, max(0, h - 3)])
        c0 = rng.choice([0, max(0, w - 4)])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            r0 = rng.choice([0, max(0, h - 3)])
            c0 = rng.randint(0, max(0, w - 4))
        else:
            r0 = rng.randint(0, max(0, h - 3))
            c0 = rng.choice([0, max(0, w - 4)])
    else:
        r0 = rng.randint(0, max(0, h - 3))
        c0 = rng.randint(0, max(0, w - 4))
    return r0, c0


def _draw_from_degenerate(name, rng):
    h, w = 7, 14
    g = full_grid(h, w, 0)
    if name == "no_eights":
        for _ in range(int(0.4 * h * w)):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = 1
        return g
    if name == "blob_outside":
        for _ in range(int(0.4 * h * w)):
            r = rng.randint(0, h - 1); c = rng.randint(2, w - 1)
            g[r][c] = 1
        for r in range(2):
            g[r][0] = 8
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
