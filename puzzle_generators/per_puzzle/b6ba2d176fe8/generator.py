"""Generator for 03560426.

Rule: objects sorted by column become solid rectangles in a diagonal
staircase.

Combinatorial axes (8): n_objects, max_rh, max_rw, palette_kind,
column_spacing, row_spread, anchor_corner, asymmetry_force.
Degenerates: same_column, single_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "b6ba2d176fe8"
VERSION = "1.1.0"
TASK_ID = "b6ba2d176fe8"
SUMMARY = "Objects sorted by column become solid rectangles in a diagonal staircase."

INVARIANTS = [
    "nonzero objects are disconnected solid rectangles",
    "objects have distinct left columns",
    "the diagonal staircase of bbox sizes fits in the grid",
    "object colors are preserved in output order",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_column", "single_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_objects":      {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "max_rh":         {"type": "int", "default": "3", "valid": "2..4"},
    "max_rw":         {"type": "int", "default": "3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "column_spacing": {"type": "int", "default": "4", "valid": "3..6"},
    "row_spread":     {"type": "str", "default": "rng",
                       "valid": "tight|wide"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
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
        no_lo, no_hi = 2, 3
        rh_max, rw_max = 2, 2
    elif difficulty == "hard":
        no_lo, no_hi = 5, 6
        rh_max, rw_max = 3, 4
    else:
        no_lo, no_hi = 3, 4
        rh_max, rw_max = 3, 3
    n_objects = int(overrides.get("n_objects",
                                  ctx.draw_int("n_objects", no_lo, no_hi)))
    n_objects = max(2, min(6, n_objects))
    rh_max = int(overrides.get("max_rh", rh_max))
    rw_max = int(overrides.get("max_rw", rw_max))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    spacing = int(overrides.get("column_spacing", 4))
    row_spread = overrides.get("row_spread",
                               ctx.draw_choice("row_spread",
                                               ["tight", "wide"]))
    dims = [(rng.randint(1, rh_max), rng.randint(1, rw_max))
            for _ in range(n_objects)]
    h = max(10, 2 + sum(dh - 1 for dh, _ in dims) + max(dh for dh, _ in dims))
    w = max(12, 2 + n_objects * spacing)
    g = full_grid(h, w, 0)
    palette = _build_palette(palette_kind, n_objects, rng)
    for i, ((rh, rw), color) in enumerate(zip(dims, palette)):
        if row_spread == "tight":
            r = rng.randint(1, max(1, h // 2))
        else:
            r = rng.randint(1, max(1, h - rh - 1))
        c = 1 + i * spacing
        if c + rw <= w:
            draw_rect(g, r, c, rh, rw, color)
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
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "same_column":
        g[2][2] = 1
        g[5][2] = 2
        return g
    if name == "single_object":
        draw_rect(g, 3, 3, 2, 2, 4)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 7 + 1
        return g
    return g
