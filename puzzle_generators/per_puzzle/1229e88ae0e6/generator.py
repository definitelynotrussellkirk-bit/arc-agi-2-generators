"""Generator for v0_original:medium_04 — center crop of nonzero region.

Rule: crop the input to its non-zero bbox, then paste centered on a blank grid
of the same dimensions.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, already_centered, motif_fills_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1229e88ae0e6"
VERSION = "1.1.0"
TASK_ID = "1229e88ae0e6"

SUMMARY = "A small connected motif positioned off-center."

INVARIANTS = [
    "background is 0",
    "exactly one connected motif (3-5 cells) in some non-zero color, NOT centered on the grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "already_centered", "motif_fills_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "off_center_motif",
                       "valid": "off_center_motif"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 6, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 8)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    cells = _build_motif(rng, rng.randint(3, 5))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
    r0 = rng.choice([0, h - sh])
    c0 = rng.choice([0, w - sw])
    for r, c in cells:
        g[r0 + r - min(rs)][c0 + c - min(cs)] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_motif":
        # blank → no nonzero region to center
        return g
    if name == "already_centered":
        # motif already centered → rule is identity (no signal)
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3)]:
            g[r][c] = 4
        return g
    if name == "motif_fills_grid":
        # motif fills entire grid → centering is identity
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
