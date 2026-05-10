"""Generator for arc_additional_puzzles_21_set6:H42 — Voronoi-fill 1-frame interior.

Rule: 1-frame; seed cells inside; fill each interior cell with the
nearest-seed-color (Manhattan).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seeds, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "9ea9f1e62275"
VERSION = "1.1.0"
TASK_ID = "9ea9f1e62275"
SUMMARY = "Single 1-frame ≥6×8 with 3-4 distinct seed colors inside (1 cell each)."

INVARIANTS = [
    "exactly one 1-frame, ≥6 tall and ≥8 wide",
    "3-4 single-cell seeds inside, distinct non-{0,1} colors",
    "seeds are at distinct positions (not on border)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seeds", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "frame_with_interior_seeds",
                       "valid": "frame_with_interior_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "2..9"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    fh = h - 2; fw = w - 2
    draw_rect_outline(g, 1, 1, fh, fw, 1)
    n_seeds = rng.randint(3, 4)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_seeds)
    placed = []
    for color in palette:
        for _ in range(40):
            r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
            if g[r][c] == 0 and all(abs(r - pr) + abs(c - pc) >= 3 for pr, pc in placed):
                g[r][c] = color
                placed.append((r, c))
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # seeds but no 1-frame → no interior to Voronoi-partition
        g[3][3] = 4
        g[5][8] = 6
        return g
    if name == "no_seeds":
        # frame but no seeds → no Voronoi partition possible
        draw_rect_outline(g, 1, 1, h - 2, w - 2, 1)
        return g
    if name == "single_seed":
        # only one seed → entire interior is "nearest" to that seed (no contrast)
        draw_rect_outline(g, 1, 1, h - 2, w - 2, 1)
        g[4][5] = 4
        return g
    return g
