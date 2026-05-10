"""Generator for arc_puzzle_bank_eighteenth21:H124 — match prototype under dihedral.

Three prototype panels and one query panel are laid out horizontally. The query
matches one prototype up to a dihedral transform; the selected prototype is
recolored by the query color.

Combinatorial axes (8): match_index, palette_kind, n_protos, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_query, missing_separator, ambiguous_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3194379886a5"
VERSION = "1.1.0"
TASK_ID = "3194379886a5"
SUMMARY = "Choose the prototype whose support matches the query under symmetry."

INVARIANTS = [
    "the input has four equal-width horizontal panels",
    "the first three panels are prototype shapes",
    "the fourth query panel is a transformed copy of exactly one prototype",
    "the output is the matched prototype recolored by the query color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_query", "missing_separator", "ambiguous_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "match_index":    {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_protos":       {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "four_horizontal_panels",
                       "valid": "four_horizontal_panels"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PROTOS = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
]


def _place_panel(g, panel, cells, color):
    left = panel * 5
    for dr, dc in cells:
        g[1 + dr][left + 1 + dc] = color


def _turn(cells):
    raw = [(c, -r) for r, c in cells]
    min_r = min(r for r, _ in raw)
    min_c = min(c for _, c in raw)
    return [(r - min_r, c - min_c) for r, c in raw]


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
        match_index = ctx.draw_int("match_index", 0, 1)
    elif difficulty == "hard":
        match_index = ctx.draw_int("match_index", 0, 2)
    else:
        match_index = ctx.draw_int("match_index", 0, 2)
    proto_colors = rng.sample([1, 2, 3, 4, 5, 6, 7], 3)
    query_color = rng.choice([8, 9])
    g = full_grid(5, 19, 0)
    for sep in [4, 9, 14]:
        for r in range(5):
            g[r][sep] = 4
    for idx, cells in enumerate(_PROTOS):
        _place_panel(g, idx, cells, proto_colors[idx])
    _place_panel(g, 3, _turn(_PROTOS[match_index]), query_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 19, 0)
    if name == "no_query":
        # Three prototypes drawn but the query panel is empty — rule has no
        # query shape to match, so no selection can be made.
        for sep in [4, 9, 14]:
            for r in range(5):
                g[r][sep] = 4
        for idx, cells in enumerate(_PROTOS):
            _place_panel(g, idx, cells, [1, 2, 3][idx])
        return g
    if name == "missing_separator":
        # Separators absent; cells run together, panel boundaries undefined.
        for idx, cells in enumerate(_PROTOS):
            _place_panel(g, idx, cells, [1, 2, 3][idx])
        _place_panel(g, 3, _turn(_PROTOS[0]), 8)
        return g
    if name == "ambiguous_match":
        # All three prototypes are the same shape (= rotations of each
        # other); the query matches all of them, so the rule's choice is
        # ambiguous.
        for sep in [4, 9, 14]:
            for r in range(5):
                g[r][sep] = 4
        same_shape = _PROTOS[0]
        _place_panel(g, 0, same_shape, 1)
        _place_panel(g, 1, _turn(same_shape), 2)
        _place_panel(g, 2, _turn(_turn(same_shape)), 3)
        _place_panel(g, 3, same_shape, 8)
        return g
    return g
