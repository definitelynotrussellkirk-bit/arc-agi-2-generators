"""Generator for arc_additional_puzzles_21_set6:M42 — L-shape connect 2 markers per color via cmd.

Rule: cell (0,0) is a command. For each non-cmd color with exactly 2
markers a, b, paint an L-segment connecting them (cmd=1: horizontal
at a's row + vertical at b's col; else: vertical at a's col +
horizontal at b's row).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, single_marker, collinear_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "819daf7d9f91"
VERSION = "1.1.0"
TASK_ID = "819daf7d9f91"
SUMMARY = "Cmd at (0,0) + 1-3 endpoint-color pairs forming L-segments via bend rule."

INVARIANTS = [
    "cell (0,0) holds the command (1 or 2)",
    "each endpoint color has exactly 2 markers, on different rows AND different columns",
    "endpoints don't overlap (0,0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "single_marker", "collinear_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "cmd_topleft_pairs_anywhere",
                       "valid": "cmd_topleft_pairs_anywhere"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        n = ctx.draw_int("n_pairs", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_pairs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
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
        # No command at (0,0) — bend direction is undefined.
        g[2][2] = 3; g[5][6] = 3
        return g
    if name == "single_marker":
        # Color has only 1 marker — rule has no second endpoint to connect to.
        g[0][0] = 1
        g[3][4] = 3
        return g
    if name == "collinear_pair":
        # Pair on same row — L-segment degenerates to a straight line.
        g[0][0] = 1
        g[3][2] = 3; g[3][6] = 3
        return g
    return g
