"""Generator for arc_additional_puzzles_21_set7:M44 — checkerboard fill of frame interior with 2 seed colors.

Rule: a single rectangle frame's strict interior contains 2 seed
cells of distinct non-bg colors a, b. Fill the entire interior with a
checkerboard of (a, b) using ((r-1)+(c-1))%2 to pick a vs b.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seeds, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "78cc0b96bc87"
VERSION = "1.1.0"
TASK_ID = "78cc0b96bc87"
SUMMARY = "1 rectangle frame with 2 seed cells of distinct colors in its strict interior."

INVARIANTS = [
    "background is 0",
    "exactly one full-perimeter rectangle frame ≥4×4",
    "strict interior holds exactly 2 seed cells, in distinct colors a and b (different from frame color)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seeds", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_size":     {"type": "int", "default": "rng 5..7", "valid": "4..8"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "single_frame_anywhere",
                       "valid": "single_frame_anywhere"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rh = rng.randint(5, 7)
    rw = rng.randint(5, 8)
    rh = min(rh, h - 1)
    rw = min(rw, w - 1)
    r1 = rng.randint(0, h - rh)
    c1 = rng.randint(0, w - rw)
    r2 = r1 + rh - 1
    c2 = c1 + rw - 1
    frame_color = rng.choice([1, 5])
    palette = list(random_palette(rng, 3, exclude={frame_color}))
    a, b = palette[0], palette[1]
    draw_frame(g, r1, c1, r2, c2, frame_color)
    interior_cells = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    rng.shuffle(interior_cells)
    g[interior_cells[0][0]][interior_cells[0][1]] = a
    g[interior_cells[1][0]][interior_cells[1][1]] = b
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # Two seed colors but no frame — rule has no interior to fill.
        g[3][3] = 2; g[5][6] = 4
        return g
    if name == "no_seeds":
        # Frame present but no seed cells inside — rule has nothing to extend.
        draw_frame(g, 1, 1, 6, 8, 1)
        return g
    if name == "single_seed":
        # Frame present but only one seed color — rule needs two for checkerboard.
        draw_frame(g, 1, 1, 6, 8, 1)
        g[3][3] = 4
        return g
    return g
