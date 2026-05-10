"""Generator for arc_puzzle_bank_21_set15_bundle:easy_o06.

Each 2x2 motif has exactly three same-color cells and one empty corner.

Combinatorial axes (8): grid_h, grid_w, palette_kind, block_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, complete_2x2, two_corners_missing.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f16508733f0a"
VERSION = "1.1.0"
TASK_ID = "f16508733f0a"
SUMMARY = "Separated incomplete 2x2 same-color blocks."

INVARIANTS = [
    "background is 0",
    "each motif is a 2x2 block with three cells of one color and one zero",
    "motifs are separated to avoid accidental adjacent 2x2 completions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "complete_2x2", "two_corners_missing")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "block_count":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "incomplete_2x2_motifs",
                       "valid": "incomplete_2x2_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _area(r, c):
    return {(rr, cc) for rr in range(r - 1, r + 3) for cc in range(c - 1, c + 3)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        block_count = ctx.draw_int("block_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        block_count = ctx.draw_int("block_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        block_count = ctx.draw_int("block_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=block_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            r = rng.randint(0, h - 2)
            c = rng.randint(0, w - 2)
            zone = _area(r, c)
            if not (zone & occupied):
                cells = [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
                missing = rng.randrange(4)
                for i, (rr, cc) in enumerate(cells):
                    if i != missing:
                        g[rr][cc] = color
                occupied |= zone
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # blank → no 2x2 motifs to complete
        return g
    if name == "complete_2x2":
        # 2x2 already complete → no missing corner to fill
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 4
                g[4 + dr][5 + dc] = 6
        return g
    if name == "two_corners_missing":
        # two missing corners per motif → ambiguous which corner to complete
        g[1][1] = 4; g[2][2] = 4
        g[4][5] = 6; g[5][6] = 6
        return g
    return g
