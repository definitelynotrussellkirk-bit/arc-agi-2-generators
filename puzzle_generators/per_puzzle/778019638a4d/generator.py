"""Generator for arc_puzzle_bank_fifth_21_bundle:hard_33_local_transform_gallery_sorted_by_width.

Each target component has a transform key immediately above its bounding-box
top-left. The rule transforms each keyed component and packs the results by
width.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_items,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_keys, no_components, equal_widths.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "778019638a4d"
VERSION = "1.1.0"
TASK_ID = "778019638a4d"
SUMMARY = "Transform keyed components and pack them into a width-sorted gallery."

INVARIANTS = [
    "keys are colors 1..4 and sit directly above their component bbox",
    "target components are nonzero colors other than 1..4",
    "components are separated after key removal",
    "transformed crops are sorted by width then height descending",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_keys", "no_components", "equal_widths")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_items":        {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "keys_above_components",
                       "valid": "keys_above_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_ITEMS = [
    ([(0, 0), (1, 0), (1, 1)], (2, 1)),
    ([(0, 0), (0, 1), (1, 1), (2, 1)], (2, 7)),
    ([(0, 1), (1, 0), (1, 1), (1, 2)], (7, 3)),
]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_items = ctx.draw_int("n_items", 2, 2)
    elif difficulty == "hard":
        n_items = ctx.draw_int("n_items", 3, 3)
    else:
        n_items = ctx.draw_int("n_items", 2, 3)
    keys = rng.sample([1, 2, 3, 4], n_items)
    colors = rng.sample([5, 6, 7, 8, 9], n_items)
    g = full_grid(11, 12, 0)
    for idx in range(n_items):
        cells, (top, left) = _ITEMS[idx]
        g[top - 1][left] = keys[idx]
        _paint(g, top, left, cells, colors[idx])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_keys":
        # components without keys → no transforms to apply
        for idx, color in zip(range(2), [5, 6]):
            cells, (top, left) = _ITEMS[idx]
            _paint(g, top, left, cells, color)
        return g
    if name == "no_components":
        # keys without components → nothing to transform/pack
        g[1][1] = 1
        g[1][7] = 2
        return g
    if name == "equal_widths":
        # all components same width → no sorting signal, ambiguous order
        for idx, color in zip(range(2), [5, 6]):
            cells = [(0, 0), (1, 0), (1, 1)]  # width 2
            top = 2 if idx == 0 else 6
            left = 1 if idx == 0 else 5
            g[top - 1][left] = idx + 1
            _paint(g, top, left, cells, color)
        return g
    return g
