"""Generator for arc_additional_puzzles_21_set15_bundle:M99 — Flood compartments by max-color marker.

Rule: 5-walls divide grid. For each chamber, find max non-{0,5} value;
flood-fill chamber with that color.

Combinatorial axes (8): n_rows, n_cols, palette_kind, marker_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, empty_chamber, single_marker_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "10ae3d33166b"
VERSION = "1.1.0"
TASK_ID = "10ae3d33166b"
SUMMARY = "5-walls divide grid into 4-6 compartments; each has 1-2 markers of varied colors."

INVARIANTS = [
    "5-walls form a regular grid",
    "each compartment has 1-2 marker cells of distinct non-{0,5} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "empty_chamber", "single_marker_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_rows":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "n_cols":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_count":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "compartment_grid",
                       "valid": "compartment_grid"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n_rows = ctx.draw_int("n_rows", 2, 2)
        n_cols = ctx.draw_int("n_cols", 2, 2)
    elif difficulty == "hard":
        n_rows = ctx.draw_int("n_rows", 3, 3)
        n_cols = ctx.draw_int("n_cols", 3, 3)
    else:
        n_rows = ctx.draw_int("n_rows", 2, 3)
        n_cols = ctx.draw_int("n_cols", 2, 3)
    cell_h = 3; cell_w = 4
    h = n_rows * cell_h + (n_rows + 1)
    w = n_cols * cell_w + (n_cols + 1)
    g = full_grid(h, w, 5)
    rng = ctx.draw_rng("layout")
    for ri in range(n_rows):
        for ci in range(n_cols):
            r0 = 1 + ri * (cell_h + 1)
            c0 = 1 + ci * (cell_w + 1)
            for r in range(r0, r0 + cell_h):
                for c in range(c0, c0 + cell_w):
                    g[r][c] = 0
            n_markers = rng.randint(1, 2)
            palette = [2, 3, 4, 6, 7, 8, 9]; rng.shuffle(palette)
            for i in range(n_markers):
                while True:
                    sr = rng.randint(r0, r0 + cell_h - 1)
                    sc = rng.randint(c0, c0 + cell_w - 1)
                    if g[sr][sc] == 0:
                        g[sr][sc] = palette[i]; break
    return g


def _draw_from_degenerate(name, rng):
    n_rows, n_cols = 2, 2
    cell_h, cell_w = 3, 4
    h = n_rows * cell_h + (n_rows + 1)
    w = n_cols * cell_w + (n_cols + 1)
    g = full_grid(h, w, 5)
    # carve chambers (default chambers used by all degenerates)
    chamber_origins = []
    for ri in range(n_rows):
        for ci in range(n_cols):
            r0 = 1 + ri * (cell_h + 1)
            c0 = 1 + ci * (cell_w + 1)
            chamber_origins.append((r0, c0))
            for r in range(r0, r0 + cell_h):
                for c in range(c0, c0 + cell_w):
                    g[r][c] = 0
    if name == "no_walls":
        # blank grid, no 5-walls → no chambers to flood
        return full_grid(h, w, 0)
    if name == "empty_chamber":
        # one chamber has no marker → no fill color defined for it
        r0, c0 = chamber_origins[0]
        g[r0][c0] = 4
        # other chambers left empty
        return g
    if name == "single_marker_color":
        # all chambers share one marker color → no per-chamber distinction
        for r0, c0 in chamber_origins:
            g[r0 + 1][c0 + 1] = 4
        return g
    return g
