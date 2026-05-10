"""Generator for arc_puzzle_bank_21_set19_bundle:hard_p07 — laser-bounce trail.

Rule: a source cell on the border (color in non-{0, 1, 2, 5}) emits a beam
inward. Mirror 1 is /, mirror 2 is \\, color 5 is wall. The beam paints 0-cells
along its path with the source color until it hits a wall or exits.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_mirrors, n_walls, texture.
Degenerates: no_source, no_mirrors, source_in_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e410357cf67e"
VERSION = "1.1.0"
TASK_ID = "e410357cf67e"

SUMMARY = "1 source on border + 1-3 mirrors (1 or 2) inside + optional walls."

INVARIANTS = [
    "background is 0",
    "exactly one source cell on the grid border in a non-{0, 1, 2, 5} color",
    "1-3 mirror cells (color 1 or 2) inside the grid (not on border)",
    "0-2 wall cells (color 5) sparsely placed",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_mirrors", "source_in_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_mirrors":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "n_walls":        {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "border_source_inner_mirrors",
                       "valid": "border_source_inner_mirrors"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_mirrors = ctx.draw_int("n_mirrors", 1, 1)
        n_walls = ctx.draw_int("n_walls", 0, 0)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        n_mirrors = ctx.draw_int("n_mirrors", 3, 4)
        n_walls = ctx.draw_int("n_walls", 1, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        n_mirrors = ctx.draw_int("n_mirrors", 1, 3)
        n_walls = ctx.draw_int("n_walls", 0, 2)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    source_color = rng.choice([3, 4, 6, 7, 8, 9])
    border = []
    for c in range(w): border.extend([(0, c), (h - 1, c)])
    for r in range(1, h - 1): border.extend([(r, 0), (r, w - 1)])
    sr, sc = rng.choice(border)
    g[sr][sc] = source_color
    for _ in range(n_mirrors):
        for _t in range(40):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice([1, 2])
            break
    for _ in range(n_walls):
        for _t in range(40):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = 5
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_source":
        # Mirrors and walls but no border source — rule has no beam
        # to launch.
        g[3][4] = 1; g[5][6] = 2
        g[7][3] = 5
        return g
    if name == "no_mirrors":
        # Source on border but no mirrors — beam travels straight;
        # rule's reflection step never fires.
        g[0][5] = 4
        g[5][3] = 5
        return g
    if name == "source_in_corner":
        # Source at a corner — beam direction is ambiguous (corner
        # has two valid inward directions).
        g[0][0] = 4
        g[3][3] = 1
        return g
    return g
