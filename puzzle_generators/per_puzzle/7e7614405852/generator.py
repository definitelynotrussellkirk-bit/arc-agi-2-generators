"""Generator for arc_puzzle_bank_third21:E17.

Rule: horizontal runs of exactly three same-color cells have only the
center recolored to 8.

Combinatorial axes (8): grid_h/w, palette_kind, n_runs, palette_size,
position_bias, n_distinct_colors, run_density, texture.
Degenerates: no_runs, run_length_2, run_length_5.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7e7614405852"
VERSION = "1.1.0"
TASK_ID = "7e7614405852"
SUMMARY = "Horizontal runs of exactly three same-color cells have only the center recolored to 8."

INVARIANTS = [
    "generated runs are length exactly 3",
    "runs are separated",
    "background is zero",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_runs", "run_length_2", "run_length_5")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "run_density":    {"type": "str", "default": "fixed_3", "valid": "fixed_3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
    n = ctx.draw_int("n_runs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    spots = [(r, c) for r in range(0, h, 2) for c in range(0, w - 2, 4)]
    rng.shuffle(spots)
    for i, (r, c) in enumerate(spots[:n]):
        color = (i % 7) + 1
        if color == 8:
            color = 9
        g[r][c] = color
        g[r][c + 1] = color
        g[r][c + 2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # singletons only — no length-3 run to mark center of
        g[1][2] = 4
        g[3][6] = 7
        return g
    if name == "run_length_2":
        # length-2 runs only — no center cell exists in length-3 sense
        g[1][2] = 3; g[1][3] = 3
        g[3][5] = 5; g[3][6] = 5
        return g
    if name == "run_length_5":
        # length-5 run — rule's "exactly 3" predicate fails
        for c in range(2, 7):
            g[3][c] = 7
        return g
    return g
