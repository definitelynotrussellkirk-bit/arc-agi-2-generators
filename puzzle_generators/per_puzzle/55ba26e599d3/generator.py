"""Generator for bcb3040b.

Rule: 2 endpoints of color 2; rule draws line via DDA. 0-cells become
2; 1-cells become 3.

Combinatorial axes (8): grid_h/w, density_1, endpoint_position,
n_distractors, palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_endpoint, no_endpoints, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "55ba26e599d3"
VERSION = "1.1.0"
TASK_ID = "55ba26e599d3"
SUMMARY = "2 endpoint cells of color 2 + scattered 1-cells."

INVARIANTS = [
    "exactly 2 cells of color 2",
    "scattered 1-cells throughout (some on the line path)",
]

POSITION_BIASES = ("opposite", "diagonal", "row_aligned", "rng")
DEGENERATE_TEXTURES = ("same_endpoint", "no_endpoints", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "density_1":      {"type": "float", "default": "0.4", "valid": "0.2..0.6"},
    "endpoint_position":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "n_distractors":  {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for endpoint_position",
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
        h_lo, h_hi, w_lo, w_hi = 3, 4, 10, 12
        d_default = 0.3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 7, 10, 16, 20
        d_default = 0.5
    else:
        h_lo, h_hi, w_lo, w_hi = 4, 6, 12, 16
        d_default = 0.4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    density = float(overrides.get("density_1", d_default))
    density = max(0.1, min(0.7, density))
    n_ones = int(density * h * w)
    for _ in range(n_ones):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        g[r][c] = 1
    bias = (overrides.get("texture") or
            overrides.get("endpoint_position")
            or ctx.draw_choice("endpoint_position", list(POSITION_BIASES)))
    for _try in range(40):
        if bias == "opposite":
            r1 = 0; c1 = 0; r2 = h - 1; c2 = w - 1
        elif bias == "diagonal":
            r1 = rng.randint(0, max(0, h // 2 - 1)); c1 = rng.randint(0, 2)
            r2 = rng.randint(min(h - 1, h // 2), h - 1); c2 = rng.randint(w - 4, w - 1)
        elif bias == "row_aligned":
            r1 = r2 = rng.randint(0, h - 1)
            c1 = rng.randint(0, 2); c2 = rng.randint(w - 4, w - 1)
        else:
            r1 = rng.randint(0, h - 1); c1 = rng.randint(0, 2)
            r2 = rng.randint(0, h - 1); c2 = rng.randint(w - 4, w - 1)
        if (r1, c1) != (r2, c2):
            g[r1][c1] = 2
            g[r2][c2] = 2
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 14
    g = full_grid(h, w, 0)
    if name == "same_endpoint":
        g[2][7] = 2
        return g
    if name == "no_endpoints":
        for _ in range(int(0.3 * h * w)):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
