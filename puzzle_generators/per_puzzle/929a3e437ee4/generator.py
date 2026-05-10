"""Generator for a3325580.

Rule: find color(s) with max cell count. Sort tied colors by leftmost
column. Output mx (max count) tall x k wide.

Combinatorial axes (8): grid_h/w, n_tied, target_count, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_tie, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "929a3e437ee4"
VERSION = "1.1.0"
TASK_ID = "929a3e437ee4"
SUMMARY = "Several scattered cells; 2-3 colors tied for max count."

INVARIANTS = [
    "2-3 colors all having the same maximum cell count",
    "each tied color appears in a distinct column-region",
    "other colors (if any) have strictly smaller count",
]

POSITION_BIASES = ("scattered", "centered", "row_aligned", "col_aligned")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_tie", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "n_tied":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "target_count":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        h_lo, h_hi = 8, 9
        nt_lo, nt_hi = 2, 2
        tc_lo, tc_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi = 12, 14
        nt_lo, nt_hi = 3, 4
        tc_lo, tc_hi = 3, 5
    else:
        h_lo, h_hi = 9, 12
        nt_lo, nt_hi = 2, 3
        tc_lo, tc_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    n_tied = int(overrides.get("n_tied",
                               ctx.draw_int("n_tied", nt_lo, nt_hi)))
    n_tied = max(2, min(4, n_tied))
    target_count = int(overrides.get("target_count",
                                     ctx.draw_int("target_count",
                                                  tc_lo, tc_hi)))
    target_count = max(2, min(5, target_count))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_tied, rng)
    zone_w = max(1, w // n_tied)
    for i, color in enumerate(palette):
        zone_start = i * zone_w
        zone_end = (i + 1) * zone_w if i < n_tied - 1 else w
        placed = 0
        for _ in range(60):
            if placed >= target_count:
                break
            r = rng.randint(0, h - 1)
            c = rng.randint(zone_start, max(zone_start, zone_end - 1))
            if g[r][c] == 0:
                g[r][c] = color
                placed += 1
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_tie":
        for i in range(5):
            g[i][1] = 2
        for i in range(3):
            g[i][6] = 3
        return g
    if name == "single_color":
        for i in range(4):
            g[i][3] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 3 + 1
        return g
    return g
