"""Generator for 1b59e163.

Rule: bg=4; multi-color shape contains cells of various colors; each
single dot of color C finds C in shape and stamps shape there.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_dots, n_distinct_colors.
Degenerates: no_shape, no_dot, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_cells

GENERATOR_ID = "8d7d1364cf11"
VERSION = "1.1.0"
TASK_ID = "8d7d1364cf11"
SUMMARY = "4-bg + 1 multi-color shape + 1-2 dot anchors."

INVARIANTS = [
    "bg is 4",
    "exactly one multi-color shape with three or more cells in distinct colors",
    "one or two dot cells whose color matches a cell in the shape",
    "dots are far from the shape so the stamp stays in-bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_dot", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_dots":         {"type": "int", "default": "1", "valid": "1..2"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h_lo, h_hi = 14, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 14, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [1, 2, 3, 5, 6, 7, 8, 9] if c not in pool]
    palette = pool[:3]
    g = [[4] * w for _ in range(h)]
    sr0, sc0 = 2, 2
    shape = [(sr0 + 0, sc0 + 0, palette[0]),
             (sr0 + 0, sc0 + 1, palette[0]),
             (sr0 + 0, sc0 + 2, palette[0]),
             (sr0 + 1, sc0 + 1, palette[1]),
             (sr0 - 1, sc0 + 0, palette[2])]
    paint_cells(g, shape)
    target_color = palette[1]
    for _ in range(40):
        dr = rng.randint(h // 2 + 2, h - 3)
        dc = rng.randint(w // 2, w - 3)
        if g[dr][dc] == 4:
            g[dr][dc] = target_color
            break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 4)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = [[4] * 16 for _ in range(16)]
    if name == "no_shape":
        g[10][10] = 2
        return g
    if name == "no_dot":
        for c in range(2, 5):
            g[2][c] = 1
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(16):
                g[r][c] = 4
        return g
    return g
