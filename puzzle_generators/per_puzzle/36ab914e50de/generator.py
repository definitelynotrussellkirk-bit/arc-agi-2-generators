"""Generator for arc_puzzle_bank_21_set23_s:S23_H7.

Rule: 4 scrambled edge-coded tiles; rotate/permute to match by edge-center
connector colors; output the assembled lattice.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, no_tiles, edges_unmatched.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "36ab914e50de"
VERSION = "1.1.0"
TASK_ID = "36ab914e50de"
SUMMARY = "Scramble four edge-coded tiles; the rule searches rotations and positions to assemble a matching 2x2 lattice."

INVARIANTS = [
    "the input is a 2x2 lattice of 3x3 tiles separated by color-9 dividers",
    "four tiles have matching edge-center connector colors under one 2x2 arrangement",
    "tiles may be permuted and rotated in the input",
    "the output is the valid assembled lattice chosen by the solver's deterministic tie-break",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "no_tiles", "edges_unmatched")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "scramble":       {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "8", "valid": "8..8"},
    "position_bias":  {"type": "str", "default": "2x2_tile_lattice",
                       "valid": "2x2_tile_lattice"},
    "n_distinct_colors": {"type": "int", "default": "8", "valid": "8..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BASE_TILES = [
    [[0, 0, 0], [0, 2, 6], [0, 8, 0]],
    [[0, 0, 0], [6, 3, 0], [0, 1, 0]],
    [[0, 8, 0], [0, 4, 7], [0, 0, 0]],
    [[0, 1, 0], [7, 5, 0], [0, 0, 0]],
]

_SCRAMBLES = [
    [(2, 1), (0, 0), (3, 3), (1, 2)],
    [(1, 1), (3, 0), (0, 2), (2, 3)],
    [(3, 2), (2, 0), (1, 3), (0, 1)],
    [(0, 1), (2, 2), (1, 0), (3, 3)],
    [(2, 3), (1, 2), (3, 1), (0, 0)],
    [(1, 3), (0, 2), (2, 1), (3, 0)],
]


def _turn(tile):
    h = len(tile)
    return [[tile[h - 1 - r][c] for r in range(h)] for c in range(h)]


def _rot(tile, k):
    out = [row[:] for row in tile]
    for _ in range(k % 4):
        out = _turn(out)
    return out


def _paste_tile(g, tile, tile_index):
    tr = tile_index // 2
    tc = tile_index % 2
    top = tr * 4
    left = tc * 4
    for r in range(3):
        for c in range(3):
            g[top + r][left + c] = tile[r][c]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    scramble = (ctx.draw_int("scramble", 0, len(_SCRAMBLES) - 1) + sample_index) % len(_SCRAMBLES)
    g = full_grid(7, 7, 9)
    for r in (0, 1, 2, 4, 5, 6):
        for c in (0, 1, 2, 4, 5, 6):
            g[r][c] = 0
    for out_index, (tile_index, turns) in enumerate(_SCRAMBLES[scramble]):
        _paste_tile(g, _rot(_BASE_TILES[tile_index], turns), out_index)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 9)
    for r in (0, 1, 2, 4, 5, 6):
        for c in (0, 1, 2, 4, 5, 6): g[r][c] = 0
    if name == "no_separators":
        # No 9-dividers — rule's tile-lattice precondition fails;
        # tile boundaries undefined.
        h2 = full_grid(7, 7, 0)
        for out_index, (tile_index, turns) in enumerate(_SCRAMBLES[0]):
            _paste_tile(h2, _rot(_BASE_TILES[tile_index], turns), out_index)
        return h2
    if name == "no_tiles":
        # Separators but no tile content — rule has no edge codes
        # to match.
        return g
    if name == "edges_unmatched":
        # Edge codes that cannot be made consistent under any
        # rotation/permutation — rule's matching search fails.
        for out_index, (tile_index, turns) in enumerate(_SCRAMBLES[0]):
            _paste_tile(g, _BASE_TILES[tile_index], out_index)
        # Corrupt one tile's edge code so no global match exists
        g[0][1] = 9; g[1][2] = 9
        return g
    return g
