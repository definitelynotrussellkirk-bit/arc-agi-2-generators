"""Generator for arc_puzzle_bank_21_set23_bundle:easy_p07.

Rule: aligned same-color 2x2 blocks define a filled barbell rectangle.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_block, off_axis_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3e2b303f4cf7"
VERSION = "1.1.0"
TASK_ID = "3e2b303f4cf7"
SUMMARY = "Aligned same-color 2x2 blocks define a filled barbell rectangle."

INVARIANTS = [
    "background is 0",
    "each active color appears as exactly two aligned 2x2 blocks",
    "block pairs are separated by at least one blank row or column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_block", "off_axis_blocks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "6..20"},
    "pair_count":     {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "aligned_block_pairs",
                       "valid": "aligned_block_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _blocked(cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return {(r, c)
            for r in range(min(rs) - 1, max(rs) + 2)
            for c in range(min(cs) - 1, max(cs) + 2)}


def _block_cells(r: int, c: int) -> set[tuple[int, int]]:
    return {(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        pair_count = ctx.draw_int("pair_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 17)
        w = ctx.draw_int("grid_w", 14, 19)
        pair_count = ctx.draw_int("pair_count", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
        pair_count = ctx.draw_int("pair_count", 2, 3)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(pair_count, 9))
    occupied: set[tuple[int, int]] = set()
    candidates: list[tuple[set[tuple[int, int]], str]] = []

    for r in range(1, h - 2):
        for c1 in range(1, w - 4):
            for c2 in range(c1 + 3, w - 1):
                cells = _block_cells(r, c1) | _block_cells(r, c2)
                candidates.append((cells, "h"))
    for c in range(1, w - 2):
        for r1 in range(1, h - 4):
            for r2 in range(r1 + 3, h - 1):
                cells = _block_cells(r1, c) | _block_cells(r2, c)
                candidates.append((cells, "v"))
    rng.shuffle(candidates)

    placed = 0
    for cells, _orientation in candidates:
        blocked = _blocked(cells)
        if blocked & occupied:
            continue
        color = colors[placed % len(colors)]
        for r, c in cells:
            grid[r][c] = color
        occupied |= blocked
        placed += 1
        if placed >= pair_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no barbells to fill.
        return g
    if name == "single_block":
        # Color appears as only one 2x2 block — rule's "exactly
        # two aligned blocks" precondition fails.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        return g
    if name == "off_axis_blocks":
        # Two same-color 2x2 blocks not aligned (different rows
        # AND different cols) — rule's "axis-aligned barbell"
        # filter excludes; fill undefined.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(6, 8):
            for c in range(8, 10): g[r][c] = 4
        return g
    return g
