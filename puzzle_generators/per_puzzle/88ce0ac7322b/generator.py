"""Generator for arc_puzzle_bank_21_set23_s:S23_M6 — sort tiles by occupancy.

Combinatorial axes (8): grid_h, grid_w, palette_kind, tile_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_tile, tied_counts, already_sorted.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "88ce0ac7322b"
VERSION = "1.1.0"
TASK_ID = "88ce0ac7322b"

SUMMARY = "A one-row tile strip whose tiles have distinct nonzero cell counts."

INVARIANTS = [
    "tiles are 3x3 and separated by full 9 columns",
    "all tile occupancy counts are distinct",
    "the input order is not already sorted by occupancy count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_tile", "tied_counts", "already_sorted")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "3..3"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..23"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "tile_count":     {"type": "int", "default": "rng 4..5", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "rng 4..5", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "9col_separated_tiles",
                       "valid": "9col_separated_tiles"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


PATTERNS = {
    1: [(1, 1)],
    2: [(1, 0), (1, 1)],
    4: [(0, 0), (0, 1), (1, 0), (1, 1)],
    5: [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    6: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)],
}


def _tile(cells, color):
    tile = [[0, 0, 0] for _ in range(3)]
    for r, c in cells:
        tile[r][c] = color
    return tile


def _assemble(tiles):
    h = 3
    w = len(tiles) * 3 + len(tiles) - 1
    g = full_grid(h, w, 9)
    for i, tile in enumerate(tiles):
        c0 = i * 4
        for r in range(3):
            for c in range(3):
                g[r][c0 + c] = tile[r][c]
    return g


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("tile_count", 4, 4)
    elif difficulty == "hard":
        n = ctx.draw_int("tile_count", 5, 5)
    else:
        n = ctx.draw_int("tile_count", 4, 5)
    rng = ctx.draw_rng("layout")
    counts = list(PATTERNS)[:n]
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], n)
    pairs = list(zip(counts, colors))
    rng.shuffle(pairs)
    if [count for count, _ in pairs] == sorted(counts):
        pairs = pairs[1:] + pairs[:1]
    return _assemble([_tile(PATTERNS[count], color) for count, color in pairs])


def _draw_from_degenerate(name, rng):
    if name == "single_tile":
        # one tile only → trivially sorted, no permutation to learn
        return _assemble([_tile(PATTERNS[2], 4)])
    if name == "tied_counts":
        # 2 tiles with same count → "distinct counts" precondition fails
        return _assemble([
            _tile(PATTERNS[2], 4),
            _tile(PATTERNS[2], 6),  # tied with first
            _tile(PATTERNS[5], 7),
        ])
    if name == "already_sorted":
        # input already in ascending order → output equals input
        return _assemble([
            _tile(PATTERNS[1], 4),
            _tile(PATTERNS[2], 6),
            _tile(PATTERNS[4], 7),
            _tile(PATTERNS[5], 8),
        ])
    return _assemble([_tile(PATTERNS[2], 4)])
