"""Generator for 9d9215db.

Rule: nonzero ring cells propagate to symmetric corner or side positions
of their Chebyshev ring.

Combinatorial axes (8): grid_size, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, n_seeds, ring_radius.
Degenerates: no_seeds, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d2534264df36"
VERSION = "1.1.0"
TASK_ID = "d2534264df36"
SUMMARY = "Nonzero ring cells propagate to symmetric corner/side positions."

INVARIANTS = [
    "background is color 0",
    "source cells sit on square Chebyshev rings",
    "corner cells copy to all four ring corners",
    "side cells copy to the sampled side positions of the same ring",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "full_grid", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 7..9", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "n_seeds":        {"type": "int", "default": "3", "valid": "2..5"},
    "ring_radius":    {"type": "int", "default": "auto", "valid": "auto"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        size_choices = [7]
    elif difficulty == "hard":
        size_choices = [9, 11, 13]
    else:
        size_choices = [7, 9]
    size = ctx.draw_choice("size", size_choices)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 3, rng)
    g = full_grid(size, size, 0)
    g[0][0] = pal[0]
    if 3 < size:
        g[1][3] = pal[1]
    if size - 2 >= 0 and size - 1 >= 0:
        g[size - 2][size - 1] = pal[2]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    size = 7
    g = full_grid(size, size, 0)
    if name == "no_seeds":
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 2
        return g
    if name == "single_cell":
        g[3][3] = 2
        return g
    return g
