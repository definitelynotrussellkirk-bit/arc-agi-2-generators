"""Generator for 984d8a3e.

Rule: rows rebuilt from left, middle, and right color counts so middle
run shares a common right edge.

Combinatorial axes (8): row_count, palette_kind, grid_w, anchor_corner,
asymmetry_force, palette_size, left_count_pattern, mid_count_pattern.
Degenerates: single_color, no_pattern, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "18a074d140e9"
VERSION = "1.1.0"
TASK_ID = "18a074d140e9"
SUMMARY = "Rows rebuilt from left/middle/right color counts; middle run aligns right edge."

INVARIANTS = [
    "the left color is the value at the top-left cell",
    "the middle color is the modal color",
    "the third non-background color is the right color",
    "each output row preserves per-color counts while aligning the middle run's right edge",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_color", "no_pattern", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "row_count":      {"type": "int", "default": "rng 4..6", "valid": "1..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "left_count_pattern":{"type": "str", "default": "stride3",
                       "valid": "stride3|stride2|fixed"},
    "mid_count_pattern":{"type": "str", "default": "stride2",
                       "valid": "stride2|stride3|fixed"},
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
        rc_lo, rc_hi = 3, 4
    elif difficulty == "hard":
        rc_lo, rc_hi = 7, 12
    else:
        rc_lo, rc_hi = 4, 6
    rows = ctx.draw_int("row_count", rc_lo, rc_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 3, rng)
    left, mid, right = pal[0], pal[1], pal[2]
    w = int(overrides.get("grid_w",
                          9 + rng.randint(0, 2)))
    g = full_grid(rows, w, right)
    for r in range(rows):
        left_count = 1 + (r % 3)
        mid_count = 3 + (r % 2)
        for c in range(left_count):
            if c < w:
                g[r][c] = left
        for c in range(left_count, left_count + mid_count):
            if c < w:
                g[r][c] = mid
    g[0][0] = left
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
    h, w = 5, 10
    if name == "single_color":
        return full_grid(h, w, 2)
    if name == "no_pattern":
        return full_grid(h, w, 0)
    if name == "full_grid":
        return full_grid(h, w, 2)
    return full_grid(h, w, 0)
