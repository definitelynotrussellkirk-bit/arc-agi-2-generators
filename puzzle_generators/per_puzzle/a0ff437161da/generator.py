"""Generator for puzzle 4a1cacc2.

Rule: bg=8 with one non-8 cell. Find nearest corner; fill rectangle
from cell to that corner with cell's color.

Combinatorial axes (8): grid_h/w, color, cell_position, palette_kind,
quadrant_bias, anchor_corner, asymmetry_force, distance_kind.
Degenerates: cell_at_corner, no_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a0ff437161da"
VERSION = "1.1.0"
TASK_ID = "a0ff437161da"
SUMMARY = "8-bg with 1 non-8 cell; rule fills rect to nearest corner."

INVARIANTS = [
    "bg = 8",
    "exactly 1 non-8 cell",
    "cell not at a corner (rule's fill is non-trivial)",
]

QUADRANT_BIASES = ("upper_left", "upper_right", "lower_left",
                   "lower_right", "center", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("cell_at_corner", "no_cell", "full_grid")
HELPFUL_TEXTURES = QUADRANT_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..12", "valid": "4..16"},
    "color":          {"type": "color", "default": "rng (≠8)",
                       "valid": "1..9 (≠8)"},
    "quadrant_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(QUADRANT_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "distance_kind":  {"type": "str", "default": "rng",
                       "valid": "near|medium|far"},
    "texture":        {"type": "str", "default": "alias for quadrant_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 9, 14
    else:
        h_lo, h_hi = 5, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 2)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    color = int(overrides.get("color", palette[0]))
    if color == 8:
        color = next((c for c in palette if c != 8), 1)
    bias = (overrides.get("texture") or
            overrides.get("quadrant_bias")
            or ctx.draw_choice("quadrant_bias",
                               list(QUADRANT_BIASES)))
    r, c = _pick_position(bias, h, w, rng)
    g = [[8] * w for _ in range(h)]
    g[r][c] = color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    rng.shuffle(pool)
    return pool


def _pick_position(bias, h, w, rng):
    if bias == "upper_left":
        return rng.randint(1, max(1, h // 2 - 1)), \
               rng.randint(1, max(1, w // 2 - 1))
    if bias == "upper_right":
        return rng.randint(1, max(1, h // 2 - 1)), \
               rng.randint(w // 2, max(w // 2, w - 2))
    if bias == "lower_left":
        return rng.randint(h // 2, max(h // 2, h - 2)), \
               rng.randint(1, max(1, w // 2 - 1))
    if bias == "lower_right":
        return rng.randint(h // 2, max(h // 2, h - 2)), \
               rng.randint(w // 2, max(w // 2, w - 2))
    if bias == "center":
        return h // 2, w // 2
    return rng.randint(1, h - 2), rng.randint(1, w - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = [[8] * w for _ in range(h)]
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    if name == "cell_at_corner":
        g[0][0] = color
        return g
    if name == "no_cell":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
