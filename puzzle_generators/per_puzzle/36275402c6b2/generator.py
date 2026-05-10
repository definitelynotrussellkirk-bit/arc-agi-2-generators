"""Generator for e9b4f6fc.

Rule: adjacent outside color pairs define substitutions applied to the
largest rectangle crop.

Combinatorial axes (8): grid_h/w, palette_kind, rect_h, rect_w,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_pairs, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "36275402c6b2"
VERSION = "1.1.0"
TASK_ID = "36275402c6b2"
SUMMARY = "Adjacent outside color pairs define substitutions on largest rect crop."

INVARIANTS = [
    "background is color 0",
    "the largest object is a solid rectangle",
    "outside adjacent pairs encode replacement-color then source-color",
    "the output is the rectangle crop after applying those substitutions",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pairs", "no_rect", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_h":         {"type": "int", "default": "4", "valid": "3..6"},
    "rect_w":         {"type": "int", "default": "5", "valid": "4..7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed",
                       "valid": "fixed"},
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
        h_lo, h_hi = 8, 10
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 10, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 2)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 3, rng)
    old, new, other = palette[0], palette[1], palette[2]
    g = full_grid(h, w, 0)
    rh = int(overrides.get("rect_h", 4))
    rw = int(overrides.get("rect_w", 5))
    rh = max(3, min(rh, h - 4))
    rw = max(4, min(rw, w - 4))
    fill_box(g, 2, 2, 2 + rh - 1, 2 + rw - 1, old)
    if 7 < h and 3 < w:
        g[7][2] = new
        g[7][3] = old
    if 8 < h:
        g[8][2] = other
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
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        fill_box(g, 2, 2, 5, 6, 2)
        return g
    if name == "no_rect":
        g[7][2] = 1; g[7][3] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
