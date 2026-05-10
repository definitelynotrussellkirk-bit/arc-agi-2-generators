"""Generator for arc_additional_puzzles_21_set6:H37 — dihedral exemplar transform.

Two color-2 exemplar objects define a dihedral transform. A color-3 query
object is transformed the same way by the rule.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identity_transform (exemplars identical → 8 valid ops fix
A; rule cannot infer which transform), symmetric_base (base is point-
symmetric → multiple transforms map A→B; rule's inference is ambiguous),
no_query (no color-3 component → rule has nothing to transform).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5eab486dd6f3"
VERSION = "1.1.0"
TASK_ID = "5eab486dd6f3"
SUMMARY = "Two color-2 exemplars show a symmetry transform applied to a color-3 query."

INVARIANTS = [
    "exactly two separated color-2 exemplar components",
    "exactly one color-3 query component",
    "the exemplar components differ by one rotation/reflection transform",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identity_transform", "symmetric_base", "no_query")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "int", "default": "rng 1..7", "valid": "1..7"},
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "query_shape":    {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_exemplars_one_query",
                       "valid": "two_exemplars_one_query"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (3, 0)],
]


def _normalize(cells):
    r0 = min(r for r, _c in cells)
    c0 = min(c for _r, c in cells)
    return sorted((r - r0, c - c0) for r, c in cells)


def _transform(cells, code):
    raw = []
    for r, c in cells:
        if code == 1:
            raw.append((c, -r))
        elif code == 2:
            raw.append((-r, -c))
        elif code == 3:
            raw.append((-c, r))
        elif code == 4:
            raw.append((r, -c))
        elif code == 5:
            raw.append((-r, c))
        elif code == 6:
            raw.append((c, r))
        elif code == 7:
            raw.append((-c, -r))
        else:
            raw.append((r, c))
    return _normalize(raw)


def _stamp(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        code = ctx.draw_int("transform", 1, 4)
    else:
        code = ctx.draw_int("transform", 1, 7)
    base = list(_SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)])
    query = list(_SHAPES[ctx.draw_int("query_shape", 0, len(_SHAPES) - 1)])
    rng.shuffle(query)
    query = _normalize(query)

    exemplar_b = _transform(base, code)
    h, w = 14, 20
    g = full_grid(h, w, 0)
    _stamp(g, 2, 1, _normalize(base), 2)
    _stamp(g, 2, 8, exemplar_b, 2)
    _stamp(g, 8, rng.randint(1, 12), query, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 20
    g = full_grid(h, w, 0)
    if name == "identity_transform":
        # Exemplars are identical — 8 valid ops fix A; rule's
        # transform-inference cannot pick a unique op.
        base = _normalize(_SHAPES[0])
        _stamp(g, 2, 1, base, 2)
        _stamp(g, 2, 8, base, 2)
        _stamp(g, 8, 5, _normalize(_SHAPES[1]), 3)
        return g
    if name == "symmetric_base":
        # Base is its own 180° rotation (a 2x2 square works);
        # multiple transforms map A→B identically.
        sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
        _stamp(g, 2, 1, sq, 2)
        _stamp(g, 2, 8, sq, 2)
        _stamp(g, 8, 5, _normalize(_SHAPES[1]), 3)
        return g
    if name == "no_query":
        # No color-3 query — rule has nothing to transform; output
        # equals input.
        base = _normalize(_SHAPES[0])
        _stamp(g, 2, 1, base, 2)
        _stamp(g, 2, 8, _transform(base, 2), 2)
        return g
    return g
