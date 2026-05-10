"""Generator for arc_puzzle_bank_sixth21:E40.

Rule: centers of same-color three-cell diagonal lines are recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_triples,
palette_size, position_bias, n_distinct_colors, diag_dir, texture.
Degenerates: no_triples, isolated_pair, center_already_8.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "994f16f93144"
VERSION = "1.1.0"
TASK_ID = "994f16f93144"
SUMMARY = "Centers of same-color three-cell diagonal lines are recolored to 8."

INVARIANTS = [
    "each generated pattern is a diagonal triple",
    "triples are separated",
    "center color is not 8",
]

PALETTE_KINDS = ("default", "main_diag", "anti_diag", "mixed_diag")
DEGENERATE_TEXTURES = ("no_triples", "isolated_pair", "center_already_8")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_triples":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..7", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..7", "valid": "1..9"},
    "diag_dir":       {"type": "str", "default": "mixed", "valid": "mixed"},
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
        n = ctx.draw_int("n_triples", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n_triples", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        n = ctx.draw_int("n_triples", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    centers = [(r, c) for r in range(1, h - 1, 3) for c in range(1, w - 1, 3)]
    rng.shuffle(centers)
    for i, (r, c) in enumerate(centers[:n]):
        color = (i % 7) + 1
        dr, dc = rng.choice([(1, 1), (1, -1)])
        g[r - dr][c - dc] = color
        g[r][c] = color
        g[r + dr][c + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_triples":
        # empty grid — no diagonal triples to recolor
        return g
    if name == "isolated_pair":
        # two-cell diagonal (not three) → predicate "length-3 diag" fails
        g[2][2] = 4; g[3][3] = 4
        return g
    if name == "center_already_8":
        # diagonal triple whose center is already 8 — recolor is no-op / ambiguous
        g[2][2] = 8; g[3][3] = 8; g[4][4] = 8
        return g
    return g
