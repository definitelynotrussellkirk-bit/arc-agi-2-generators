"""Generator for arc_additional_puzzle_bank_volume18:H124 — Bouncing 8-ray.

Rule: source is the 2-cell at edge, direction inferred from edge.
Ray traces, painting 8s, bouncing off 7 (slash) or 6 (backslash) cells,
stops on 5 or out-of-bounds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_mirrors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_mirrors, source_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f5952ff1cee1"
VERSION = "1.1.0"
TASK_ID = "f5952ff1cee1"
SUMMARY = "2-source on top edge + 1-2 mirror cells (6 or 7) below."

INVARIANTS = [
    "exactly one 2-cell on row 0 (the source, going down)",
    "1-2 mirror cells (6 or 7) somewhere below",
    "rest of grid is 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_mirrors", "source_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_mirrors":      {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "top_2source_with_mirrors",
                       "valid": "top_2source_with_mirrors"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sc = rng.randint(1, w - 2)
    g[0][sc] = 2
    n_mirrors = rng.randint(1, 2)
    placed = 0
    for _ in range(40):
        if placed >= n_mirrors:
            break
        r = rng.randint(2, h - 2); c = rng.randint(1, w - 2)
        if g[r][c] == 0 and c != sc:
            g[r][c] = rng.choice([6, 7])
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_source":
        # mirrors but no 2-source → ray has no origin
        g[3][4] = 6; g[5][7] = 7
        return g
    if name == "no_mirrors":
        # source but no mirrors → ray goes straight to bottom edge
        g[0][4] = 2
        return g
    if name == "source_at_corner":
        # source at corner → direction inference clashes (top + left edge)
        g[0][0] = 2
        g[4][3] = 6
        return g
    return g
