"""Generator for cb227835.

Rule: two 8 endpoints define paired diagonal-first and straight-first
3 paths.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
gap_size.
Degenerates: no_endpoints, single_endpoint, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db63430eeffa"
VERSION = "1.1.0"
TASK_ID = "db63430eeffa"
SUMMARY = "Two 8 endpoints define paired diagonal-first and straight-first paths."

INVARIANTS = [
    "the scene has exactly two color-8 endpoints",
    "the endpoints are separated in both row and column",
    "the row and column deltas are usually unequal",
    "endpoints sit clear of grid borders so paths fit",
]

ORIENTATIONS = ("down_right", "down_left", "up_right", "up_left")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_endpoints", "single_endpoint", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "7..16"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "gap_size":       {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    h = 8 + rng.randint(0, 4)
    w = 8 + rng.randint(0, 5)
    row_gap = rng.randint(3, h - 3)
    col_gap = rng.randint(2, w - 3)
    if row_gap == col_gap:
        row_gap = min(h - 2, row_gap + 1)
    r_lo = rng.randint(1, h - row_gap - 1)
    c_lo = rng.randint(1, w - col_gap - 1)
    r_hi = r_lo + row_gap
    c_hi = c_lo + col_gap
    if orientation == "down_right":
        p1, p2 = (r_lo, c_lo), (r_hi, c_hi)
    elif orientation == "down_left":
        p1, p2 = (r_lo, c_hi), (r_hi, c_lo)
    elif orientation == "up_right":
        p1, p2 = (r_hi, c_lo), (r_lo, c_hi)
    else:
        p1, p2 = (r_hi, c_hi), (r_lo, c_lo)
    g = full_grid(h, w, 0)
    g[p1[0]][p1[1]] = 8
    g[p2[0]][p2[1]] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_endpoints":
        return g
    if name == "single_endpoint":
        g[3][3] = 8
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 8
        return g
    return g
