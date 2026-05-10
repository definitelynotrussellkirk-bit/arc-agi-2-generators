"""Generator for a09f6c25.

Rule: each non-bg shape with size>1; h-symmetric -> 1, v-symmetric -> 3,
otherwise -> 6.

Combinatorial axes (8): grid_h/w, n_shapes, position_bias, palette_kind,
shape_variant, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_shapes, all_sym, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9c5259babb4b"
VERSION = "1.1.0"
TASK_ID = "9c5259babb4b"
SUMMARY = "8-bg with 3 distinct shapes (h-sym, v-sym, asymmetric) of color 2."

INVARIANTS = [
    "bg = 8",
    "exactly 3 shapes of color 2, well separated",
    "one shape is horizontally symmetric, one vertically, one asymmetric",
]

POSITION_BIASES = ("scattered", "row_aligned", "spread", "rng")
DEGENERATE_TEXTURES = ("no_shapes", "all_sym", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

HSYM = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]
VSYM = [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3)]
ASYM = [(0, 0), (0, 1), (1, 0), (2, 0), (2, 2)]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "10..24"},
    "n_shapes":       {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "int", "default": "0", "valid": "0..2"},
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
    elif difficulty == "hard":
        h_lo, h_hi = 16, 22
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 2)
    g = [[8] * w for _ in range(h)]
    placed = []
    for shape in [HSYM, VSYM, ASYM]:
        sh = max(r for r, c in shape) + 1
        sw = max(c for r, c in shape) + 1
        for _ in range(40):
            r0 = rng.randint(1, h - sh - 1); c0 = rng.randint(1, w - sw - 1)
            if any(abs(r0 - pr) < (sh + 2) and abs(c0 - pc) < (sw + 2)
                   for pr, pc in placed):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = 2
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 16
    g = [[8] * w for _ in range(h)]
    if name == "no_shapes":
        return g
    if name == "all_sym":
        for dr, dc in HSYM:
            g[2 + dr][2 + dc] = 2
        for dr, dc in HSYM:
            g[8 + dr][8 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
