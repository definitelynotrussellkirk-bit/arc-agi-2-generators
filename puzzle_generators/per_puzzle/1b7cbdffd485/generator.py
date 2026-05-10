"""Generator for 4be741c5.

Rule: 3-4 horizontal bands of distinct colors stacked vertically; rule
extracts unique color order as 1xN row.

Combinatorial axes (8): grid_h/w, n_bands, palette_kind, density,
band_orientation, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_band, no_bands, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1b7cbdffd485"
VERSION = "1.1.0"
TASK_ID = "1b7cbdffd485"
SUMMARY = "3-4 horizontal bands of distinct colors stacked vertically."

INVARIANTS = [
    "3-4 distinct colors, each forming a horizontal band",
    "bands are stacked top-to-bottom",
    "bands have some 0/other-color mixing inside",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_band", "no_bands", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "n_bands":        {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "float", "default": "0.85", "valid": "0.6..1.0"},
    "band_orientation":{"type": "str", "default": "horizontal",
                       "valid": "horizontal"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        h_lo, h_hi, w_lo, w_hi = 6, 8, 5, 7
        nb_lo, nb_hi = 2, 3
        d_default = 0.95
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 9, 12
        nb_lo, nb_hi = 4, 5
        d_default = 0.7
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 11, 6, 9
        nb_lo, nb_hi = 3, 4
        d_default = 0.85
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    n_bands = int(overrides.get("n_bands",
                                ctx.draw_int("n_bands", nb_lo, nb_hi)))
    n_bands = max(2, min(min(h, 5), n_bands))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_bands, rng)
    density = float(overrides.get("density", d_default))
    density = max(0.5, min(1.0, density))
    band_h = h // n_bands
    for i, color in enumerate(palette):
        rs = i * band_h
        re = rs + band_h if i < n_bands - 1 else h
        for r in range(rs, re):
            for c in range(w):
                if rng.random() < density:
                    g[r][c] = color
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
    h, w = 9, 7
    g = full_grid(h, w, 0)
    if name == "same_band":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    if name == "no_bands":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 3 + 1
        return g
    return g
