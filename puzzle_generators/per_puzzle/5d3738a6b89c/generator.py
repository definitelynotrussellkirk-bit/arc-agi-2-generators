"""Generator for arc_puzzle_bank_twelfth21:H80.

Combinatorial axes (8): grid_h, grid_w, palette_kind, layout,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototypes, no_keys, key_color_unmatched.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d3738a6b89c"
VERSION = "1.1.0"
TASK_ID = "5d3738a6b89c"
SUMMARY = "Stamp 3x3 prototype masks around matching key cells below a separator row."

INVARIANTS = [
    "three 3x3 prototype boxes sit above a full color-9 separator row",
    "prototype boxes are separated by full color-9 columns in the top section",
    "each prototype's center color is its key",
    "below the separator, singleton key cells receive their prototype mask stamped around them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototypes", "no_keys", "key_color_unmatched")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "layout":         {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "prototypes_plus_keys",
                       "valid": "prototypes_plus_keys"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MASKS = [
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
]
_KEY_LAYOUTS = [
    [(5, 2), (8, 7), (10, 4)],
    [(5, 8), (7, 2), (10, 9)],
    [(6, 3), (8, 9), (10, 6)],
]


def _paint_box(g, box_left, key, mask):
    for r, c in mask:
        g[r][box_left + c] = key
    g[1][box_left + 1] = key


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout_rng")
    layout = ctx.draw_int("layout", 0, len(_KEY_LAYOUTS) - 1)
    keys = rng.sample([2, 4, 6, 7, 8], 3)
    g = full_grid(11, 11, 0)
    for r in range(3):
        g[r][3] = 9
        g[r][7] = 9
    for c in range(11):
        g[3][c] = 9
    for box_left, key, mask in zip([0, 4, 8], keys, _MASKS):
        _paint_box(g, box_left, key, mask)
    for (r, c), key in zip(_KEY_LAYOUTS[layout], keys):
        g[r][c] = key
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    for r in range(3):
        g[r][3] = 9
        g[r][7] = 9
    for c in range(11):
        g[3][c] = 9
    if name == "no_prototypes":
        # divider + keys present but no prototypes → no masks to stamp
        for (r, c), key in zip(_KEY_LAYOUTS[0], [4, 6, 7]):
            g[r][c] = key
        return g
    if name == "no_keys":
        # prototypes present but no keys below → nothing to stamp around
        keys = [4, 6, 7]
        for box_left, key, mask in zip([0, 4, 8], keys, _MASKS):
            _paint_box(g, box_left, key, mask)
        return g
    if name == "key_color_unmatched":
        # keys below use colors not present in any prototype → no match
        keys = [4, 6, 7]
        for box_left, key, mask in zip([0, 4, 8], keys, _MASKS):
            _paint_box(g, box_left, key, mask)
        for (r, c) in _KEY_LAYOUTS[0]:
            g[r][c] = 5  # color 5 not used in any prototype
        return g
    return g
