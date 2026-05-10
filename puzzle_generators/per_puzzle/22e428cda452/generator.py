"""Generator for fd02da9e.

Rule: bg=7. For each non-7 cell, project a small 4-cell or 3-cell
pattern diagonally based on which edge it's on. Original cell erased.

Combinatorial axes (8): n_cells, edge_kind, palette_kind, color,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: corner_only, no_cells, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22e428cda452"
VERSION = "1.1.0"
TASK_ID = "22e428cda452"
SUMMARY = "8x8 bg=7 grid with 1-3 colored cells on top edge or left edge."

INVARIANTS = [
    "h = w = 8",
    "bg = 7",
    "1-3 non-7 cells, each on the top row or left column",
    "if on top non-corner: c >= 2 (room for diagonal projection)",
    "if on left non-corner: r >= 3 (room for diagonal projection)",
]

EDGE_KINDS = ("top", "left", "mixed")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("corner_only", "no_cells", "full_grid")
HELPFUL_TEXTURES = EDGE_KINDS

AXES = {
    "n_cells":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "edge_kind":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(EDGE_KINDS)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "color":          {"type": "color", "default": "rng !7", "valid": "1..9 except 7"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "left_lean|right_lean|spread"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..3"},
    "texture":        {"type": "str", "default": "alias for edge_kind",
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
        nc_lo, nc_hi = 1, 1
    elif difficulty == "hard":
        nc_lo, nc_hi = 3, 4
    else:
        nc_lo, nc_hi = 1, 3
    h = w = 8
    g = full_grid(h, w, 7)
    edge_kind = (overrides.get("texture") or
                 overrides.get("edge_kind")
                 or ctx.draw_choice("edge_kind", list(EDGE_KINDS)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    n = int(overrides.get("n_cells",
                          ctx.draw_int("n_cells", nc_lo, nc_hi)))
    n = max(1, min(4, n))
    placed = 0
    attempts = 0
    while placed < n and attempts < 40:
        attempts += 1
        if edge_kind == "top":
            kind = "top"
        elif edge_kind == "left":
            kind = "left"
        else:
            kind = rng.choice(["top", "left"])
        if kind == "top":
            r = 0
            c = rng.choice([0] + list(range(2, w - 2)))
        else:
            c = 0
            r = rng.randint(3, h - 1)
        if g[r][c] == 7:
            color = int(overrides.get("color", rng.choice(pal)))
            g[r][c] = color
            placed += 1
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c != 7]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h = w = 8
    g = full_grid(h, w, 7)
    if name == "corner_only":
        g[0][0] = 2
        return g
    if name == "no_cells":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
