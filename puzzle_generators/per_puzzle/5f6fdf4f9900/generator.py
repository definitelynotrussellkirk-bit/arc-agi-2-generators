"""Generator for 469497ad.

Rule: small sparse grid has 2-3 foreground colors, forcing color-count
upscaling.

Combinatorial axes (8): grid_size, n_colors, palette_kind, motif_variant,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_colors, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "5f6fdf4f9900"
VERSION = "1.1.0"
TASK_ID = "5f6fdf4f9900"
SUMMARY = "A small sparse grid has 2-3 foreground colors, forcing color-count upscaling."

INVARIANTS = [
    "background is 0",
    "there are at least two nonzero colors",
    "foreground cells form small separated motifs with black concave corners nearby",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
POSITION_BIASES = ("scattered", "diagonal", "corners", "centered")
DEGENERATE_TEXTURES = ("no_colors", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

_MOTIFS = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
]

AXES = {
    "grid_size":      {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_variant":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        size_lo, size_hi = 3, 4
        nc_lo, nc_hi = 2, 2
    elif difficulty == "hard":
        size_lo, size_hi = 5, 6
        nc_lo, nc_hi = 3, 4
    else:
        size_lo, size_hi = 4, 5
        nc_lo, nc_hi = 2, 3
    size = ctx.draw_int("grid_size", size_lo, size_hi)
    n_colors = ctx.draw_int("n_colors", nc_lo, nc_hi)
    n_colors = max(2, min(4, n_colors))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    colors = _build_palette(palette_kind, n_colors, rng)
    g = full_grid(size, size, 0)
    anchors = [(0, 0), (size - 2, size - 2), (0, size - 2)]
    rng.shuffle(anchors)
    for color, (r, c), motif in zip(colors, anchors, _MOTIFS):
        if r + 1 < size and c + 1 < size:
            paint_at(g, r, c, motif, color)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [1, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 2)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    size = 4
    g = full_grid(size, size, 0)
    if name == "no_colors":
        return g
    if name == "single_color":
        g[0][0] = 3; g[1][0] = 3; g[1][1] = 3
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 3
        return g
    return g
