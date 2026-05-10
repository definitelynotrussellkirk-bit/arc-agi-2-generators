"""Generator for puzzle 73182012.

Rule: extract the top-left quadrant of non-bg shape's bbox.

Combinatorial axes (8): grid_h/w, shape_dim, palette_size,
position_bias, fill_density, palette_kind, anchor_corners,
quadrant_distribution.
Degenerates: empty_grid, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ba1bd4c08c37"
VERSION = "1.1.0"
TASK_ID = "ba1bd4c08c37"
SUMMARY = "Symmetric shape with bbox; rule extracts top-left quadrant of bbox."

INVARIANTS = [
    "background is 0",
    ">=1 non-bg cell with bg padding around content",
    "non-bg shape's bbox has even dimensions in [4, 8]",
    "all 4 corners of bbox painted (so bbox extent is exact)",
]

QUADRANT_DISTS = ("balanced", "tl_heavy", "scattered", "diag_emphasis")
PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("empty_grid", "single_cell", "full_grid")
HELPFUL_TEXTURES = QUADRANT_DISTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":             {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "shape_dim":          {"type": "int", "default": "rng 4..6 even",
                           "valid": "4..8 even"},
    "palette_size":       {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "fill_density":       {"type": "float", "default": "rng 0.2..0.5",
                           "valid": "0.1..0.8"},
    "palette_kind":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PALETTE_KINDS)},
    "quadrant_distribution": {"type": "str", "default": "rng helpful",
                              "valid": "|".join(QUADRANT_DISTS)},
    "texture":            {"type": "str", "default": "alias for quadrant_distribution",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, dims = 8, 11, [4]
    elif difficulty == "hard":
        h_lo, h_hi, dims = 14, 20, [6, 8]
    else:
        h_lo, h_hi, dims = 10, 16, [4, 6, 8]
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("dim")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    shape_dim = int(overrides.get("shape_dim", rng.choice(dims)))
    if shape_dim % 2 == 1: shape_dim += 1
    shape_dim = max(4, min(8, shape_dim))
    if shape_dim + 4 > min(h, w):
        shape_dim = min(h, w) - 4
        if shape_dim % 2 == 1: shape_dim -= 1
        shape_dim = max(4, shape_dim)
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
                                  ctx.draw_int("palette_size", 2, 4)))
    palette = pool[:max(2, n_palette)]
    quad_dist = (overrides.get("texture") or
                 overrides.get("quadrant_distribution")
                 or ctx.draw_choice("quadrant_distribution",
                                    list(QUADRANT_DISTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    if bias == "center":
        rr = (h - shape_dim) // 2
        rc = (w - shape_dim) // 2
    elif bias == "edge":
        rr = 2; rc = 2
    else:
        rr = rng.randint(2, h - shape_dim - 2)
        rc = rng.randint(2, w - shape_dim - 2)
    g = full_grid(h, w, 0)
    rng2 = ctx.draw_rng("cells")
    half = shape_dim // 2
    quadrants = [
        [(rr + dr, rc + dc) for dr in range(half) for dc in range(half)],
        [(rr + dr, rc + dc) for dr in range(half) for dc in range(half, shape_dim)],
        [(rr + dr, rc + dc) for dr in range(half, shape_dim) for dc in range(half)],
        [(rr + dr, rc + dc) for dr in range(half, shape_dim)
         for dc in range(half, shape_dim)],
    ]
    g[rr][rc] = palette[0]
    g[rr][rc + shape_dim - 1] = palette[0]
    g[rr + shape_dim - 1][rc] = palette[0]
    g[rr + shape_dim - 1][rc + shape_dim - 1] = palette[0]
    weights = _quadrant_weights(quad_dist)
    for q_idx, q_cells in enumerate(quadrants):
        rng2.shuffle(q_cells)
        n_paint = rng2.randint(weights[q_idx], weights[q_idx] + 2)
        for r, c in q_cells[:n_paint]:
            if g[r][c] == 0:
                g[r][c] = rng2.choice(palette)
    return g


def _quadrant_weights(dist):
    if dist == "tl_heavy":
        return [3, 1, 1, 1]
    if dist == "diag_emphasis":
        return [2, 1, 1, 2]
    if dist == "scattered":
        return [1, 1, 1, 1]
    return [2, 1, 1, 1]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "empty_grid":
        return g
    if name == "single_cell":
        g[h // 2][w // 2] = color
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    return g
