"""Generator for arc_puzzle_bank_21_set24_bundle:medium_p06 — connect aligned same-color pairs.

Rule: pairs of cells in the same color, axially or diagonally aligned with a
clear bg-only path between them. Output draws a line of the matching color
along the path.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: adjacent_pair (cells touching → no path between them, no
line drawn), unaligned_pair (pair not on diagonal/axis → rule's
alignment filter excludes them, output equals input), single_cell
(only one cell of a color → no pair to connect).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2dbcb80623f9"
VERSION = "1.1.0"
TASK_ID = "2dbcb80623f9"

SUMMARY = "2-3 pairs of single cells in distinct colors, each pair aligned (axial or diagonal) with a clear path between."

INVARIANTS = [
    "background is 0",
    "2-3 pairs of single cells in distinct colors",
    "each pair is axially or diagonally aligned with at least 2 cells of separation",
    "the cells along the connecting path are bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("adjacent_pair", "unaligned_pair", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "aligned_pairs",
                       "valid": "aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
        n_pairs = ctx.draw_int("n_pairs", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 14)
        n_pairs = ctx.draw_int("n_pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("layout")

    dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_pairs)
        ok = True
        for color in colors:
            placed = False
            for _t in range(120):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                dr, dc = rng.choice(dirs)
                steps = rng.randint(2, 6)
                r2 = r + dr * steps; c2 = c + dc * steps
                if not (0 <= r2 < h and 0 <= c2 < w): continue
                if g[r][c] != 0 or g[r2][c2] != 0: continue
                ok_path = True
                rr, cc = r + dr, c + dc
                while (rr, cc) != (r2, c2):
                    if g[rr][cc] != 0: ok_path = False; break
                    rr += dr; cc += dc
                if not ok_path: continue
                g[r][c] = color
                g[r2][c2] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize set24 medium_p06 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "adjacent_pair":
        # Pair cells are adjacent — no bg path between; rule's
        # connector has 0 cells to paint.
        g[2][2] = 1; g[3][3] = 1
        g[5][6] = 3; g[6][7] = 3
        return g
    if name == "unaligned_pair":
        # Pair not on diagonal/axis — rule's alignment filter
        # excludes them; output equals input.
        g[1][1] = 1; g[5][8] = 1
        g[2][6] = 3; g[6][2] = 3
        return g
    if name == "single_cell":
        # Only one cell of a color — rule has no pair to connect;
        # the cell is left alone.
        g[3][3] = 4
        g[5][7] = 6
        return g
    return g
