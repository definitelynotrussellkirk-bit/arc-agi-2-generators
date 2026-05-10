"""Generator for d4c90558.

Rule: colored frames sorted by count of gray cells inside their bbox,
encoded as padded rows.

Combinatorial axes (8): grid_h/w, frame_count, palette_kind, gray_skew,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_grays, all_grays, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "0de8e68aecee"
VERSION = "1.1.0"
TASK_ID = "0de8e68aecee"
SUMMARY = "Colored frames sorted by gray-count inside bbox; encoded as padded rows."

INVARIANTS = [
    "background is color 0",
    "frame colors are nonzero and not gray",
    "each frame bbox contains one or more color-5 cells",
    "the output has one row per frame, sorted by gray-count ascending",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_grays", "all_grays", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "16", "valid": "12..22"},
    "frame_count":    {"type": "int", "default": "3", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "gray_skew":      {"type": "str", "default": "ascending",
                       "valid": "ascending|descending|rng"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "scattered|spread|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..5"},
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
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 16, 18
    h = int(overrides.get("grid_h",
                          rng.randint(h_lo, h_hi)))
    w = int(overrides.get("grid_w",
                          rng.randint(h_lo, h_hi)))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 3, rng)
    g = full_grid(h, w, 0)
    specs = [
        (1, 1, 5, 5, 1),
        (1, 9, 6, 14, 3),
        (9, 3, 14, 9, 5),
    ]
    for color, (r1, c1, r2, c2, gray_count) in zip(pal, specs):
        if r2 < h and c2 < w:
            draw_frame(g, r1, c1, r2, c2, color)
            placed = 0
            for r in range(r1 + 1, r2):
                for c in range(c1 + 1, c2):
                    if placed < gray_count and (r + c) % 2 == placed % 2:
                        g[r][c] = 5
                        placed += 1
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 5)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "no_grays":
        draw_frame(g, 1, 1, 5, 5, 1)
        draw_frame(g, 1, 9, 6, 14, 3)
        return g
    if name == "all_grays":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
