"""Generator for 30f42897.

Rule: edge cells colored consecutively; rule shifts colored block
forward along ring by 2N.

Combinatorial axes (8): grid_h/w, n_cells, color, side, palette_kind,
anchor_corner, asymmetry_force, palette_size.
Degenerates: no_cells, full_ring, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c18b572dbe0d"
VERSION = "1.1.0"
TASK_ID = "c18b572dbe0d"
SUMMARY = "8-bg with N consecutive colored cells along an edge of the perimeter ring."

INVARIANTS = [
    "bg = 8",
    "N=2-5 consecutive non-bg cells along one edge of the perimeter ring",
    "all colored cells share the same single color",
]

SIDES = ("top", "bottom", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cells", "full_ring", "full_grid")
HELPFUL_TEXTURES = SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "n_cells":        {"type": "int", "default": "rng 2..5", "valid": "1..6"},
    "color":          {"type": "color", "default": "rng !8",
                       "valid": "1..7|9"},
    "side":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SIDES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for side",
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
        h_lo, h_hi, w_lo, w_hi = 5, 7, 6, 8
        nc_lo, nc_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 12, 12, 14
        nc_lo, nc_hi = 4, 6
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 9, 8, 12
        nc_lo, nc_hi = 2, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = [[8] * w for _ in range(h)]
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("color",
                              rng.choice(pal) if pal else
                              rng.choice([1, 2, 3, 4, 5, 6, 7, 9])))
    n = ctx.draw_int("n_cells", nc_lo, nc_hi)
    n = max(1, min(min(min(h, w) - 1, 6), n))
    side = (overrides.get("texture") if overrides.get("texture") in SIDES else None) or \
           overrides.get("side") or \
           ctx.draw_choice("side", list(SIDES))
    if side == "top":
        c0 = rng.randint(0, w - n)
        for c in range(c0, c0 + n):
            g[0][c] = color
    elif side == "bottom":
        c0 = rng.randint(0, w - n)
        for c in range(c0, c0 + n):
            g[h - 1][c] = color
    elif side == "left":
        r0 = rng.randint(0, h - n)
        for r in range(r0, r0 + n):
            g[r][0] = color
    else:
        r0 = rng.randint(0, h - n)
        for r in range(r0, r0 + n):
            g[r][w - 1] = color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c != 8]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = [[8] * w for _ in range(h)]
    if name == "no_cells":
        return g
    if name == "full_ring":
        for c in range(w):
            g[0][c] = 2
            g[h - 1][c] = 2
        for r in range(h):
            g[r][0] = 2
            g[r][w - 1] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
