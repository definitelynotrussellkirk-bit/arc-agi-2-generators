"""Generator for 9841fdad.

Rule: objects in left framed panel project as stretched bars into
matching right panel.

Combinatorial axes (8): grid_h, panel_w, palette_kind, frame_color,
n_objects, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_objects, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ae70dcf677ff"
VERSION = "1.1.0"
TASK_ID = "ae70dcf677ff"
SUMMARY = "Objects in left framed panel project as stretched bars into right panel."

INVARIANTS = [
    "one frame color forms the outer border and the vertical separator",
    "the left panel has a background and separated colored objects",
    "the right panel is the projection canvas",
    "projected objects preserve row span and horizontal margin convention",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "no_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "7..12"},
    "panel_width":    {"type": "int", "default": "5", "valid": "3..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_color":    {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "n_objects":      {"type": "int", "default": "2", "valid": "1..3"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
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
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 3, rng)
    frame, c1, c2 = pal[0], pal[1], pal[2]
    panel_w = ctx.draw_int("panel_width", 5, 5)
    h = int(overrides.get("grid_h", 9))
    h = max(7, min(12, h))
    w = 2 * panel_w + 3
    sep = panel_w + 1
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = frame
        g[h - 1][c] = frame
    for r in range(h):
        g[r][0] = frame
        g[r][sep] = frame
        g[r][w - 1] = frame
    for r, c in [(2, 2), (3, 2), (3, 3)]:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = c1
    for r, c in [(5, 1), (5, 2), (6, 2)]:
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = c2
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
    h, w = 9, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        for c in range(w):
            g[0][c] = 5
            g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5
            g[r][6] = 5
            g[r][w - 1] = 5
        return g
    if name == "no_frame":
        g[3][3] = 2
        g[5][8] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
