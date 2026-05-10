"""Generator for arc_additional_puzzles_21_set14_bundle:H95 — Recolor non-bg cells by nesting depth.

Rule: count enclosing rect-frames around each non-bg cell. Recolor
to (1 + count). Nested frames get progressively higher numbers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, single_frame, no_nesting.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "938fbbaf1437"
VERSION = "1.1.0"
TASK_ID = "938fbbaf1437"
SUMMARY = "2 nested 1-frames forming concentric rectangles."

INVARIANTS = [
    "outer 1-frame ≥6×6",
    "inner 1-frame strictly inside outer, ≥3×3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "no_nesting")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "nested_concentric_frames",
                       "valid": "nested_concentric_frames"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    fr = h; fc = w
    draw_rect_outline(g, 0, 0, fr, fc, 1)
    inner_h = rng.randint(3, h - 4); inner_w = rng.randint(3, w - 4)
    r0 = rng.randint(2, h - inner_h - 2); c0 = rng.randint(2, w - inner_w - 2)
    draw_rect_outline(g, r0, c0, inner_h, inner_w, 1)
    for _ in range(rng.randint(1, 2)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = 1
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # blank → no nesting depth to count
        return g
    if name == "single_frame":
        # only one frame → all cells have nesting depth 0 or 1, no progression
        draw_rect_outline(g, 0, 0, h, w, 1)
        return g
    if name == "no_nesting":
        # two frames placed side-by-side, no nesting → max depth still 1
        draw_rect_outline(g, 1, 1, 4, 4, 1)
        draw_rect_outline(g, 1, 5, 4, 4, 1)
        return g
    return g
