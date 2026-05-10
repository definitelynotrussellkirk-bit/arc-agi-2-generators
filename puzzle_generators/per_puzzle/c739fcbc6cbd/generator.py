"""Generator for 0a938d79.

Rule: 2 edge-cell markers; rule paints periodic perpendicular lines.

Combinatorial axes (8): grid_h/w, palette_kind, rotation, position_bias,
gap_min, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_position, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import (
    full_grid, paint_cells, rot180, rot90_ccw,
)

GENERATOR_ID = "c739fcbc6cbd"
VERSION = "1.1.0"
TASK_ID = "c739fcbc6cbd"
SUMMARY = "Two edge-cell markers; rule paints periodic perpendicular lines."

INVARIANTS = [
    "bg=0",
    "2 cells of distinct non-bg colors at top/bottom edges",
    "column gap >= 2 between them",
]

ROTATIONS = ("none", "180", "270")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_position", "no_markers", "full_grid")
HELPFUL_TEXTURES = ROTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..29", "valid": "4..29"},
    "grid_w":         {"type": "int", "default": "rng h+1..30", "valid": "5..30"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "rotation":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ROTATIONS)},
    "gap_min":        {"type": "int", "default": "2", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "centered|spread|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for rotation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 18, 29
    else:
        h_lo, h_hi = 4, 29
    h = ctx.draw_int_diff("grid_h", h_lo, h_hi)
    w_min = h + 1
    w = ctx.draw_int_diff("grid_w", w_min, 30)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    cola, colb = pal[0], pal[1]
    g = full_grid(h, w, 0)
    gap_min = int(overrides.get("gap_min", 2))
    gap_min = max(2, min(6, gap_min))
    loc_ja = rng.randint(3, w - 2)
    loc_jb = rng.randint(1, max(1, loc_ja - gap_min))
    loc_ia = rng.choice([0, h - 1])
    loc_ib = rng.choice([0, h - 1])
    paint_cells(g, [(loc_ia, loc_ja)], cola)
    paint_cells(g, [(loc_ib, loc_jb)], colb)
    rot = (overrides.get("texture") if overrides.get("texture") in ROTATIONS else None) or \
          overrides.get("rotation") or \
          ctx.draw_choice("rotation", list(ROTATIONS))
    if rot == "180":
        g = rot180(g)
    elif rot == "270":
        g = rot90_ccw(g)
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
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "same_position":
        g[0][3] = 2
        return g
    if name == "no_markers":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
