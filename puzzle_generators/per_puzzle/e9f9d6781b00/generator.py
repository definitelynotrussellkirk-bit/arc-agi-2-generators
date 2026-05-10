"""Generator for puzzle d13f3404.

Rule: non-bg cells on row 0 or col 0. Output is 2h × 2w; each non-bg
cell shoots SE diagonal trail of its color.

Combinatorial axes (8): grid_h/w, n_dots, palette_size, palette_kind,
position_layout, anchor_corner, edge_split, asymmetry_force.
Degenerates: no_dots, all_dots, dots_off_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e9f9d6781b00"
VERSION = "1.1.0"
TASK_ID = "e9f9d6781b00"
SUMMARY = "Top-row/left-col non-bg cells; rule shoots SE diagonals into 2h × 2w."

INVARIANTS = [
    "background is 0",
    "non-bg cells only on row 0 or column 0",
    "2*h <= 30 and 2*w <= 30",
    ">=1 non-bg cell",
]

POSITION_LAYOUTS = ("scattered", "row_only", "col_only", "balanced",
                    "corner_heavy")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("no_dots", "all_dots", "dots_off_edge")
HELPFUL_TEXTURES = POSITION_LAYOUTS

AXES = {
    "grid_h":          {"type": "int", "default": "rng 4..15", "valid": "3..15"},
    "grid_w":          {"type": "int", "default": "rng 4..15", "valid": "3..15"},
    "n_dots":          {"type": "int", "default": "rng 2..6", "valid": "1..15"},
    "palette_size":    {"type": "int", "default": "rng 2..5", "valid": "1..7"},
    "palette_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PALETTE_KINDS)},
    "position_layout": {"type": "str", "default": "rng helpful",
                        "valid": "|".join(POSITION_LAYOUTS)},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "edge_split":      {"type": "str", "default": "rng even|row_heavy|col_heavy",
                        "valid": "even|row_heavy|col_heavy"},
    "texture":         {"type": "str", "default": "alias for position_layout",
                        "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 6
    elif difficulty == "hard":
        h_lo, h_hi = 11, 15
    else:
        h_lo, h_hi = 4, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 2, 5)))
    palette = pool[:max(1, n_palette)]
    layout = (overrides.get("texture") or
              overrides.get("position_layout")
              or ctx.draw_choice("position_layout",
                                 list(POSITION_LAYOUTS)))
    edge_split = overrides.get("edge_split",
                               ctx.draw_choice("edge_split",
                                               ["even", "row_heavy", "col_heavy"]))
    g = full_grid(h, w, 0)
    edge_positions = _edge_positions(layout, h, w, edge_split, rng)
    n_dots = int(overrides.get("n_dots",
                               ctx.draw_int("n_dots", 2,
                                            min(len(edge_positions), 8))))
    n_dots = max(1, min(len(edge_positions), n_dots))
    chosen = rng.sample(edge_positions, n_dots)
    for r, c in chosen:
        g[r][c] = rng.choice(palette)
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = palette[0]
    return g


def _edge_positions(layout, h, w, split, rng):
    row_positions = [(0, c) for c in range(w)]
    col_positions = [(r, 0) for r in range(1, h)]
    if layout == "row_only":
        return row_positions
    if layout == "col_only":
        return col_positions
    if layout == "corner_heavy":
        positions = [(0, 0), (0, 1), (0, w - 1), (1, 0), (h - 1, 0)]
        return [p for p in positions if 0 <= p[0] < h and 0 <= p[1] < w]
    if layout == "balanced":
        return row_positions + col_positions
    if split == "row_heavy":
        return row_positions + col_positions[:len(col_positions) // 3]
    if split == "col_heavy":
        return row_positions[:len(row_positions) // 3] + col_positions
    return row_positions + col_positions


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_dots":
        return g
    if name == "all_dots":
        for c in range(w):
            g[0][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(1, h):
            g[r][0] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "dots_off_edge":
        g[h // 2][w // 2] = color
        return g
    return g
