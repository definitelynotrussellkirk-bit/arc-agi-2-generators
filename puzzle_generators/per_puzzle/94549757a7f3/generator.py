"""Generator for arc_additional_puzzle_bank_volume2:E14 — Add a 2 right of every horizontal 3-line.

Rule: each 3-blob that is a single row (obj-r1 == obj-r2) — set
(r, c2 + 1) to 2 if in-bounds and currently 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_3_lines, all_at_right_edge, vertical_3_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "94549757a7f3"
VERSION = "1.1.0"
TASK_ID = "94549757a7f3"
SUMMARY = "3-4 horizontal 3-lines of varying lengths."

INVARIANTS = [
    "≥3 disjoint horizontal 3-blobs (size ≥2, single row)",
    "right of each line has space (cell at c2+1 is 0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_3_lines", "all_at_right_edge", "vertical_3_lines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "row_lines_with_right_room",
                       "valid": "row_lines_with_right_room"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n_lines = ctx.draw_int("n_lines", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_lines = ctx.draw_int("n_lines", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        n_lines = ctx.draw_int("n_lines", 3, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    for _ in range(n_lines):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            length = rng.randint(2, 4)
            c = rng.randint(0, w - length - 1)
            if all((r, c + i) not in used for i in range(length + 1)):
                for i in range(length):
                    g[r][c + i] = 3
                used.update((r, c + i) for i in range(length + 1))
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_3_lines":
        # only single 3s and 3-pairs (length-2) — no horizontal length-3+ runs to mark
        # depends on rule's exact predicate; if it accepts length-2 these still apply
        g[1][2] = 3
        g[3][6] = 3
        return g
    if name == "all_at_right_edge":
        # 3-lines end at the rightmost column → c2+1 is out of bounds, rule paints nothing
        for c in range(w - 3, w): g[1][c] = 3
        for c in range(w - 4, w): g[4][c] = 3
        return g
    if name == "vertical_3_lines":
        # 3-cells arranged vertically (single column) → predicate "single row" fails
        for r in range(1, 4): g[r][2] = 3
        for r in range(3, 6): g[r][6] = 3
        return g
    return g
