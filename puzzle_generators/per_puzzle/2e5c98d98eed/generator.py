"""Generator for arc_additional_puzzles_21_set20_bundle:E140 — Fill 8-frame interior with seed color.

Rule: 8 forms a closed rectangular frame; the interior contains a
single seed cell (non-0, non-8). Fill the interior with that seed
color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, multi_seed, broken_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "2e5c98d98eed"
VERSION = "1.1.0"
TASK_ID = "2e5c98d98eed"
SUMMARY = "Single closed 8-frame ≥4×4 with one seed cell of distinct color inside."

INVARIANTS = [
    "exactly 1 closed 8-frame, ≥4×4",
    "exactly 1 cell of distinct non-{0,8} color inside the frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "multi_seed", "broken_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_size":     {"type": "str", "default": "rng 4..5x4..6", "valid": "rng 4..5x4..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "centered_frame_with_seed",
                       "valid": "centered_frame_with_seed"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    fr = rng.randint(4, 5); fc = rng.randint(4, 6)
    r0 = rng.randint(1, h - fr - 1); c0 = rng.randint(1, w - fc - 1)
    draw_rect_outline(g, r0, c0, fr, fc, 8)
    seed_color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    seed_r = r0 + rng.randint(1, fr - 2); seed_c = c0 + rng.randint(1, fc - 2)
    g[seed_r][seed_c] = seed_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # frame but empty interior → seed color undefined, rule cannot fire
        draw_rect_outline(g, 1, 1, 5, 6, 8)
        return g
    if name == "multi_seed":
        # multiple seed colors inside → seed color ambiguous
        draw_rect_outline(g, 1, 1, 5, 6, 8)
        g[2][2] = 4
        g[3][4] = 6
        g[4][3] = 3
        return g
    if name == "broken_frame":
        # frame has a missing edge cell → not closed, "interior" undefined
        draw_rect_outline(g, 1, 1, 5, 6, 8)
        g[1][3] = 0   # gap in top edge
        g[3][3] = 4
        return g
    return g
