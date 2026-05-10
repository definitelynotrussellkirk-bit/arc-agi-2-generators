"""Generator for 12b:m84 — project 2x2 blocks to mini grid.

Rule: detect 2x2 single-color blocks. Project them to a mini grid:
  - rows of mini grid = sorted unique block-top-row positions
  - cols of mini grid = sorted unique block-top-col positions
  - cell (r, c) = block color if a block sits at that (top_row, top_col)

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blocks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, blocks_share_row, blocks_share_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b2d893865427"
VERSION = "1.1.0"
TASK_ID = "b2d893865427"

SUMMARY = "3-4 distinct-color 2x2 blocks at distinct (row, col) positions."

INVARIANTS = [
    "background is 0",
    "3-4 solid 2x2 blocks, each in a distinct non-bg color",
    "each block's top-left position is at strictly distinct rows AND strictly distinct cols across all blocks",
    "blocks don't touch each other (≥1 bg gap between bboxes)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "blocks_share_row", "blocks_share_col")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blocks":       {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "distinct_rows_and_cols",
                       "valid": "distinct_rows_and_cols"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")
    n_blocks = rng.randint(3, 4)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_blocks)
    for _ in range(40):
        g = full_grid(h, w, 0)
        rows = rng.sample(range(0, h - 1), n_blocks)
        cols = rng.sample(range(0, w - 1), n_blocks)
        rng.shuffle(rows); rng.shuffle(cols)
        ok = True
        for color, r0, c0 in zip(palette, rows, cols):
            if not _free(g, r0, c0, r0 + 1, c0 + 1):
                ok = False; break
            for dr in (0, 1):
                for dc in (0, 1):
                    g[r0 + dr][c0 + dc] = color
        if ok:
            return g
    raise ValueError(f"could not place {n_blocks} 2x2 blocks at distinct rows+cols")


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # Empty grid — rule has no 2x2 blocks to project.
        return g
    if name == "blocks_share_row":
        # Two blocks share a top-row — projection collapses them onto same row.
        for dr in (0, 1):
            for dc in (0, 1): g[1 + dr][1 + dc] = 4
        for dr in (0, 1):
            for dc in (0, 1): g[1 + dr][7 + dc] = 5
        return g
    if name == "blocks_share_col":
        # Two blocks share a top-col — projection collapses them onto same col.
        for dr in (0, 1):
            for dc in (0, 1): g[1 + dr][3 + dc] = 4
        for dr in (0, 1):
            for dc in (0, 1): g[7 + dr][3 + dc] = 5
        return g
    return g
