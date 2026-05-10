"""Generator for arc_additional_puzzle_bank_volume13:M91 — Voronoi 2 vs 3.

Rule: place 2-marker and 3-marker. For each empty cell, color by closer
marker (Manhattan): closer to 2→2, closer to 3→3, ties→0.
Non-zero cells keep their value.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_strays,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_2_marker, no_3_marker, markers_adjacent.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "554712910457"
VERSION = "1.1.0"
TASK_ID = "554712910457"
SUMMARY = "2-marker + 3-marker + 1-2 stray non-mapping colored cells; output Voronoi-fills empty cells by closer marker."

INVARIANTS = [
    "exactly one 2-marker and one 3-marker, far apart",
    "between 0 and 3 stray cells of other colors (4-9), placed in empty squares",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_2_marker", "no_3_marker", "markers_adjacent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_strays":       {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "two_markers_far_apart",
                       "valid": "two_markers_far_apart"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..7"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    # 2-marker upper area, 3-marker lower-right
    r2 = rng.randint(0, max(0, h // 2 - 1))
    c2 = rng.randint(0, max(0, w // 2 - 1))
    r3 = rng.randint(min(h - 1, h // 2 + 1), h - 1)
    c3 = rng.randint(min(w - 1, w // 2 + 1), w - 1)
    if (r2, c2) == (r3, c3):
        r3 = h - 1; c3 = w - 1
    g[r2][c2] = 2
    g[r3][c3] = 3
    used = {(r2, c2), (r3, c3)}
    # 1-2 stray cells (colors 4-9)
    n_strays = rng.randint(1, 2)
    placed = 0
    for _ in range(20):
        if placed >= n_strays: break
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if (r, c) in used: continue
        col = rng.choice([4, 5, 6, 7, 8, 9])
        g[r][c] = col; used.add((r, c)); placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_2_marker":
        # only 3-marker → no Voronoi competition, all empty cells go to 3
        g[5][7] = 3
        g[2][3] = 4
        return g
    if name == "no_3_marker":
        # only 2-marker → all empty cells go to 2
        g[1][1] = 2
        g[3][5] = 6
        return g
    if name == "markers_adjacent":
        # 2 and 3 markers next to each other → tie band dominates output
        g[2][3] = 2
        g[2][4] = 3
        return g
    return g
