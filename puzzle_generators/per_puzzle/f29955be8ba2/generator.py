"""Generator for arc_puzzle_bank_sixth21:H37.

Rule: use the first-column header to permute three horizontal row blocks.

Combinatorial axes (8): grid_h, grid_w, palette_kind, permutation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: identity_perm, missing_header, duplicate_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f29955be8ba2"
VERSION = "1.1.0"
TASK_ID = "f29955be8ba2"
SUMMARY = "Use the first-column header to permute three horizontal row blocks."

INVARIANTS = [
    "the grid has three equal-height row blocks",
    "the first three cells in column 0 encode a permutation of 1,2,3",
    "the remaining columns contain three visually distinct blocks",
    "the output omits the header column and orders blocks by the header",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identity_perm", "missing_header", "duplicate_blocks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "8", "valid": "8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "permutation":    {"type": "enum", "default": "rng",
                       "valid": "123|132|213|231|312|321"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "header_plus_blocks",
                       "valid": "header_plus_blocks"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "framed", "valid": "framed"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PERMS = ["123", "132", "213", "231", "312", "321"]
_BLOCKS = [
    [[1, 1, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0]],
    [[0, 0, 0, 2, 2, 0, 0], [0, 0, 2, 2, 0, 0, 0], [0, 2, 2, 0, 0, 0, 0]],
    [[3, 3, 3, 0, 0, 0, 0], [0, 3, 0, 0, 3, 0, 0], [0, 0, 3, 3, 3, 0, 0]],
]


def _recolor(block, color):
    return [[color if v else 0 for v in row] for row in block]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        perm = ctx.draw_choice("permutation", ["123", "213", "132"])
    elif difficulty == "hard":
        perm = ctx.draw_choice("permutation", ["231", "312", "321"])
    else:
        perm = ctx.draw_choice("permutation", _PERMS)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)

    g = full_grid(9, 8, 0)
    for r, value in enumerate(int(ch) for ch in perm):
        g[r][0] = value
    for block_idx, block in enumerate(_BLOCKS):
        painted = _recolor(block, colors[block_idx])
        for r, row in enumerate(painted):
            for c, value in enumerate(row):
                g[block_idx * 3 + r][1 + c] = value
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 8, 0)
    if name == "identity_perm":
        # header = "123" → permutation is identity, output blocks in original order, no rule effect
        for r, value in enumerate([1, 2, 3]):
            g[r][0] = value
        for block_idx, block in enumerate(_BLOCKS):
            painted = _recolor(block, [4, 6, 8][block_idx])
            for r, row in enumerate(painted):
                for c, value in enumerate(row):
                    g[block_idx * 3 + r][1 + c] = value
        return g
    if name == "missing_header":
        # no header in column 0 → permutation undefined
        for block_idx, block in enumerate(_BLOCKS):
            painted = _recolor(block, [4, 6, 8][block_idx])
            for r, row in enumerate(painted):
                for c, value in enumerate(row):
                    g[block_idx * 3 + r][1 + c] = value
        return g
    if name == "duplicate_blocks":
        # all 3 blocks identical → permutation has no visible effect, output equals identity
        for r, value in enumerate([3, 1, 2]):
            g[r][0] = value
        for block_idx in range(3):
            painted = _recolor(_BLOCKS[0], 4)   # all use block 0 in color 4
            for r, row in enumerate(painted):
                for c, value in enumerate(row):
                    g[block_idx * 3 + r][1 + c] = value
        return g
    return g
