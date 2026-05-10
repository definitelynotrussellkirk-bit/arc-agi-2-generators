"""Generator for arc_puzzle_bank_twelfth_21_bundle:hard_80_select_object_by_holes_and_symmetry_scale2.

Combinatorial axes (8): holes, symmetry, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_header, no_objects, ambiguous_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8f49fe4fdfa8"
VERSION = "1.1.0"
TASK_ID = "8f49fe4fdfa8"
SUMMARY = "Select the object matching requested hole count and vertical symmetry, then scale and recolor it."

INVARIANTS = [
    "row 0 encodes hole count as count-of-ones minus one",
    "row 0 column 4 encodes whether vertical symmetry is required",
    "row 0 column 6 gives the output color",
    "the body contains candidate objects spanning the hole/symmetry feature combinations",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_header", "no_objects", "ambiguous_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "holes":          {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "symmetry":       {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "header_row0_objects_below",
                       "valid": "header_row0_objects_below"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "4..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OBJECTS = {
    (0, 1): [(0, 1), (1, 1), (2, 1)],
    (0, 0): [(0, 0), (1, 0), (2, 0), (2, 1)],
    (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    (1, 0): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
}

_POSITIONS = {
    (0, 1): (2, 1),
    (0, 0): (2, 6),
    (1, 1): (7, 1),
    (1, 0): (7, 7),
}


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    holes = ctx.draw_int("holes", 0, 1)
    symmetry = ctx.draw_int("symmetry", 0, 1)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8], 4)
    target_color = rng.choice([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in colors])

    g = full_grid(12, 13, 0)
    for c in range(holes + 1):
        g[0][c] = 1
    g[0][4] = 2 if symmetry else 3
    g[0][6] = target_color

    for color, key in zip(colors, _OBJECTS):
        top, left = _POSITIONS[key]
        _paint(g, top, left, _OBJECTS[key], color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 13, 0)
    if name == "no_header":
        # Row 0 empty — no spec for which object to select.
        for color, key in zip([2, 3, 4, 5], _OBJECTS):
            top, left = _POSITIONS[key]
            _paint(g, top, left, _OBJECTS[key], color)
        return g
    if name == "no_objects":
        # Header present but body has no candidate objects — nothing to select.
        g[0][0] = 1
        g[0][4] = 2
        g[0][6] = 9
        return g
    if name == "ambiguous_match":
        # All four objects share the same (holes, symmetry) — match is non-unique.
        g[0][0] = 1
        g[0][4] = 2
        g[0][6] = 9
        same = [(0, 1), (1, 1), (2, 1)]
        _paint(g, 2, 1, same, 2)
        _paint(g, 2, 6, same, 3)
        _paint(g, 7, 1, same, 4)
        _paint(g, 7, 7, same, 5)
        return g
    return g
