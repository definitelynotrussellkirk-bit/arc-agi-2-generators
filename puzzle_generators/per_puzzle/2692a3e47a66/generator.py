"""Generator for 22208ba4.

Rule: bg = mode color. For each color appearing in >=2 objects, clear
those cells and reflect each by its bbox size (move toward center).

Combinatorial axes (8): grid_h/w, color, n_corners, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_corner, all_corners, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2692a3e47a66"
VERSION = "1.1.0"
TASK_ID = "2692a3e47a66"
SUMMARY = "Mostly bg=7 grid with 2 same-color cells at opposite corners."

INVARIANTS = [
    "bg = 7",
    "exactly 2 cells of one color (!=7) at distinct corners (different rows AND cols)",
    "the cells are at the outer-most rows/cols (so reflection moves inward)",
]

POSITION_BIASES = ("opposite", "adjacent", "diagonal", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_corner", "all_corners", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "color":          {"type": "color", "default": "rng !7", "valid": "1..9 except 7"},
    "n_corners":      {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
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
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = [[7] * w for _ in range(h)]
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("color", rng.choice(pal)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    if bias == "opposite":
        a, b = rng.choice([((0, 0), (h - 1, w - 1)),
                            ((0, w - 1), (h - 1, 0))])
    elif bias == "adjacent":
        edges = [((0, 0), (0, w - 1)), ((0, 0), (h - 1, 0)),
                 ((h - 1, 0), (h - 1, w - 1)),
                 ((0, w - 1), (h - 1, w - 1))]
        a, b = rng.choice(edges)
    elif bias == "diagonal":
        a, b = rng.choice([((0, 0), (h - 1, w - 1)),
                            ((0, w - 1), (h - 1, 0))])
    else:
        a, b = rng.sample(corners, 2)
    g[a[0]][a[1]] = color
    g[b[0]][b[1]] = color
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
    h, w = 13, 13
    g = [[7] * w for _ in range(h)]
    if name == "same_corner":
        g[0][0] = 2
        return g
    if name == "all_corners":
        for r, c in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
            g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
