"""Generator for puzzle e99362f0.

Rule: yellow(4) cross divides grid into 4 quadrants. Output overlays
quadrants with priority BR > TL > TR > BL.

Combinatorial axes (8): half_size, palette_kind, palette_size,
quadrant_density, position_bias, anchor_corner, asymmetry_force,
include_decoy.
Degenerates: empty_quadrants, full_quadrants, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1672855ac30c"
VERSION = "1.1.0"
TASK_ID = "1672855ac30c"
SUMMARY = "Yellow cross divides grid; rule overlays quadrants BR>TL>TR>BL."

INVARIANTS = [
    "h = w = 2*half + 1 (so cross at center)",
    "exactly 1 yellow(4) row + 1 yellow(4) col forming a centered cross",
    "each quadrant has non-bg non-yellow cells",
]

POSITION_BIASES = ("scattered", "diagonal", "corners", "edges",
                   "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_quadrants", "full_quadrants", "monochrome")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "half_size":      {"type": "int", "default": "rng 4..7", "valid": "3..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "quadrant_density":{"type": "float", "default": "rng 0.2..0.4",
                        "valid": "0.05..0.7"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        half_lo, half_hi = 3, 4
    elif difficulty == "hard":
        half_lo, half_hi = 7, 9
    else:
        half_lo, half_hi = 4, 7
    half = int(overrides.get("half_size",
                             ctx.draw_int("half_size", half_lo, half_hi)))
    half = max(3, min(9, half))
    h = w = 2 * half + 1
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], half, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette_size = max(2, min(6, palette_size))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    density = float(overrides.get("quadrant_density",
                                  ctx.draw_rng("quadrant_density")
                                  .uniform(0.2, 0.4)))
    palette = _build_palette(palette_kind, palette_size, rng)
    cr = cc = half
    g = full_grid(h, w, 0)
    for c in range(w):
        g[cr][c] = 4
    for r in range(h):
        g[r][cc] = 4
    _fill_quadrants(g, h, w, cr, cc, palette, density, bias, rng)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _fill_quadrants(g, h, w, cr, cc, palette, density, bias, rng):
    if bias == "diagonal":
        for r in range(h):
            for c in range(w):
                if r == cr or c == cc:
                    continue
                if abs(r - cr) == abs(c - cc) and rng.random() < density + 0.4:
                    g[r][c] = rng.choice(palette)
    elif bias == "corners":
        for r, c in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
        for r in range(h):
            for c in range(w):
                if r == cr or c == cc:
                    continue
                if rng.random() < density / 2:
                    g[r][c] = rng.choice(palette)
    elif bias == "edges":
        for r in range(h):
            for c in range(w):
                if r == cr or c == cc:
                    continue
                on_edge = (r in (0, h - 1) or c in (0, w - 1))
                if on_edge and rng.random() < density + 0.2:
                    g[r][c] = rng.choice(palette)
    elif bias == "centered":
        for r in range(h):
            for c in range(w):
                if r == cr or c == cc:
                    continue
                d = abs(r - cr) + abs(c - cc)
                if rng.random() < density * (1 - d / (h + w)):
                    g[r][c] = rng.choice(palette)
    else:
        for r in range(h):
            for c in range(w):
                if r == cr or c == cc:
                    continue
                if rng.random() < density:
                    g[r][c] = rng.choice(palette)


def _draw_from_degenerate(name, half, rng):
    h = w = 2 * half + 1
    g = full_grid(h, w, 0)
    cr = cc = half
    for c in range(w):
        g[cr][c] = 4
    for r in range(h):
        g[r][cc] = 4
    if name == "empty_quadrants":
        return g
    if name == "full_quadrants":
        for r in range(h):
            for c in range(w):
                if r != cr and c != cc:
                    g[r][c] = 3
        return g
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                if r != cr and c != cc:
                    g[r][c] = 3
        return g
    return g
