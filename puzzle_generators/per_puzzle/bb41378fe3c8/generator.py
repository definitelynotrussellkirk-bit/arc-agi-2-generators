"""Generator for additional_scaffolded:E6.

Rule: each color-2 cell casts a one-cell down-right shadow in color 5.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, markers_on_bottom_right, marker_blocked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bb41378fe3c8"
VERSION = "1.1.0"
TASK_ID = "bb41378fe3c8"
SUMMARY = "Each color-2 cell casts a one-cell down-right shadow in color 5."

INVARIANTS = [
    "background is 0",
    "input contains color-2 singleton markers",
    "most markers have an empty down-right cell inside the grid",
    "markers are separated so shadows do not overwrite other markers",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "markers_on_bottom_right", "marker_blocked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..11", "valid": "2..18"},
    "grid_w":         {"type": "int", "default": "rng 6..11", "valid": "2..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 3..7", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "scattered_avoid_br",
                       "valid": "scattered_avoid_br"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 8)
        n_markers = ctx.draw_int("n_markers", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
        n_markers = ctx.draw_int("n_markers", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 6, 11)
        w = ctx.draw_int("grid_w", 6, 11)
        n_markers = ctx.draw_int("n_markers", 3, 7)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    cells: list[tuple[int, int]] = []
    for _ in range(180):
        if len(cells) >= n_markers:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if any(abs(r - rr) <= 1 and abs(c - cc) <= 1 for rr, cc in cells):
            continue
        if g[r + 1][c + 1] != 0:
            continue
        cells.append((r, c))
        g[r][c] = 2
    if not cells:
        g[0][0] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # no color-2 cells → no shadows cast, output identity
        return g
    if name == "markers_on_bottom_right":
        # markers on bottom row or right column → down-right cell is out of bounds, rule no-op
        for c in [1, 3, 5]:
            g[h - 1][c] = 2
        for r in [2, 4]:
            g[r][w - 1] = 2
        return g
    if name == "marker_blocked":
        # down-right cell already non-bg → rule overwrites (shadow paints over) or no-op depending on impl
        for r, c in [(1, 1), (3, 3), (5, 5)]:
            g[r][c] = 2
            g[r + 1][c + 1] = 4  # blocked: down-right is non-bg color
        return g
    return g
