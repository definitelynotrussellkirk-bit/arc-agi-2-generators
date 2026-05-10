"""Generator for puzzle 070dd51e.

Rule: for each color, find pairs of same-color cells in row/col; fill
between them with that color.

Combinatorial axes (8): grid_h/w, n_pairs, palette_kind, orientation,
gap_min, gap_max, anchor_corner, asymmetry_force.
Degenerates: no_pairs, all_same_position, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "615b0cf22405"
VERSION = "1.1.0"
TASK_ID = "615b0cf22405"
SUMMARY = "Same-color pairs aligned in row/col; rule fills between them."

INVARIANTS = [
    "background is 0",
    ">=1 color pair aligned in row OR col, >=3 cells apart",
]

ORIENTATIONS = ("row", "col", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pairs", "all_same_position", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "n_pairs":        {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "gap_min":        {"type": "int", "default": "3", "valid": "2..6"},
    "gap_max":        {"type": "int", "default": "rng 4..7",
                       "valid": "3..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for orientation",
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
    w = ctx.draw_int("grid_w", h_lo + 3, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_pairs = int(overrides.get("n_pairs",
                                ctx.draw_int("n_pairs", 1, 2)))
    n_pairs = max(1, min(4, n_pairs))
    orientation = (overrides.get("texture") or
                   overrides.get("orientation")
                   or ctx.draw_choice("orientation",
                                      list(ORIENTATIONS)))
    gap_min = int(overrides.get("gap_min", 3))
    gap_max = int(overrides.get("gap_max",
                                ctx.draw_int("gap_max", 4, 7)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_pairs, rng)
    g = full_grid(h, w, 0)
    for color in palette[:n_pairs]:
        for _ in range(20):
            ori = orientation if orientation != "rng" \
                  else rng.choice(["row", "col"])
            if ori == "row":
                r = rng.randint(0, h - 1)
                if w < gap_min + 1:
                    continue
                gap = rng.randint(gap_min, min(gap_max, w - 1))
                c0 = rng.randint(0, w - gap - 1)
                c1 = c0 + gap
                if g[r][c0] == 0 and g[r][c1] == 0:
                    g[r][c0] = color
                    g[r][c1] = color
                    break
            else:
                if h < gap_min + 1:
                    continue
                c = rng.randint(0, w - 1)
                gap = rng.randint(gap_min, min(gap_max, h - 1))
                r0 = rng.randint(0, h - gap - 1)
                r1 = r0 + gap
                if g[r0][c] == 0 and g[r1][c] == 0:
                    g[r0][c] = color
                    g[r1][c] = color
                    break
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


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Single cells, no pair
        g[1][1] = 3
        g[h - 2][w - 2] = 4
        return g
    if name == "all_same_position":
        # 2 cells too close to each other
        g[1][1] = 3
        g[1][2] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 4
        return g
    return g
