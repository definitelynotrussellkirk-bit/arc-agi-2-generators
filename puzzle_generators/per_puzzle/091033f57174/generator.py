"""Generator for arc_additional_puzzles_21_set11_bundle:M71 — L-shape draw between 2 markers per color.

Rule: cell (0,0) is the command (1 or 2). For each other color with
exactly 2 markers a, b, draw an L-shape connecting them:
  cmd=1: horizontal segment at a's row, vertical at b's col (bend at (a.r, b.c))
  cmd=2: vertical segment at a's col, horizontal at b's row (bend at (b.r, a.c))

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_pairs, texture.
Degenerates: no_cmd, no_pairs, aligned_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "091033f57174"
VERSION = "1.1.0"
TASK_ID = "091033f57174"
SUMMARY = "Command at (0,0) plus 1-3 endpoint-color pairs forming L-shapes via bend rule."

INVARIANTS = [
    "cell (0,0) holds the command color (1 or 2)",
    "each endpoint color has exactly 2 markers",
    "every endpoint pair is on different rows and different columns (so the L is non-degenerate)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_pairs", "aligned_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_pairs+1", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered_endpoint_pairs",
                       "valid": "scattered_endpoint_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= n_pairs+1", "valid": "2..5"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        n = ctx.draw_int("n_pairs", 1, 3)
    rng = ctx.draw_rng("layout")
    cmd = rng.choice([1, 2])
    g = full_grid(h, w, 0)
    g[0][0] = cmd
    palette = list(random_palette(rng, n, exclude={cmd}))
    used: set[tuple[int, int]] = {(0, 0)}
    for color in palette:
        for _ in range(50):
            r1 = rng.randint(0, h - 1); c1 = rng.randint(0, w - 1)
            r2 = rng.randint(0, h - 1); c2 = rng.randint(0, w - 1)
            if (r1, c1) in used or (r2, c2) in used: continue
            if r1 == r2 or c1 == c2: continue
            g[r1][c1] = color
            g[r2][c2] = color
            used.add((r1, c1)); used.add((r2, c2))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # No command color at (0,0) — rule has no L-orientation to apply.
        g[2][3] = 4; g[5][6] = 4
        return g
    if name == "no_pairs":
        # Command present but no endpoint pairs — rule has no L to draw.
        g[0][0] = 1
        return g
    if name == "aligned_pair":
        # Pair shares row (or column) — bend collapses; L degenerates to
        # a straight segment, ambiguous under the bend rule.
        g[0][0] = 1
        g[3][2] = 4; g[3][6] = 4
        return g
    return g
