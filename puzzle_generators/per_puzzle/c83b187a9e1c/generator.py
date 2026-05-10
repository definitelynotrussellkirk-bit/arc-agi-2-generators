"""Generator for arc_puzzle_bank_21_set9_e:hard_i20.

A color-1 template is shown with several colored candidates. Exactly one
candidate has the same binary shape under a dihedral transform; the rule crops
that candidate and recolors its nonzero cells to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (no color-1 → rule has nothing to match);
no_match (template + distractors but no candidate matches dihedral
class → selector returns nothing); tied_match (two candidates both
match → selector's "exactly one" precondition fails).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c83b187a9e1c"
VERSION = "1.1.0"
TASK_ID = "c83b187a9e1c"
SUMMARY = "Select the non-1 candidate matching the template up to dihedral symmetry."

INVARIANTS = [
    "there is exactly one color-1 template object",
    "candidate objects are single-color non-1 objects",
    "exactly one candidate is a dihedral transform of the template shape",
    "the output is the matching candidate crop recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_match", "tied_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "variant":           {"type": "int", "default": "rng 0..7", "valid": "0..7"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "10..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "template_plus_dihedral_match",
                          "valid": "template_plus_dihedral_match"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BASE = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]
_DISTRACTORS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
]


def _norm(cells):
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return sorted((r - min_r, c - min_c) for r, c in cells)


def _xform(cells, code):
    raw = []
    for r, c in cells:
        if code == 0:
            raw.append((r, c))
        elif code == 1:
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
        else:
            raw.append((-c, -r))
    return _norm(raw)


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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        w = ctx.draw_int("grid_w", 13, 15)
    variant = ctx.draw_int("variant", 0, 7)
    candidate_color, d1_color, d2_color = rng.sample([2, 3, 4, 5, 6, 7, 9], 3)
    g = full_grid(10, w, 0)

    _paint(g, 1, 1, _BASE, 1)
    match = _xform(_BASE, variant)
    match_left = min(w - 4, 6 + rng.randint(0, 1))
    _paint(g, 1, match_left, match, candidate_color)
    _paint(g, 6, 2, _DISTRACTORS[rng.randrange(len(_DISTRACTORS))], d1_color)
    _paint(g, 5, w - 5, _DISTRACTORS[(variant + 1) % len(_DISTRACTORS)], d2_color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        # No color-1 template — rule has nothing to match.
        _paint(g, 1, 1, _BASE, 4)
        _paint(g, 6, 8, _DISTRACTORS[0], 6)
        return g
    if name == "no_match":
        # Template (L-pentomino) but distractors all 2x2 squares (different class).
        _paint(g, 1, 1, _BASE, 1)
        _paint(g, 1, 8, _DISTRACTORS[0], 4)
        _paint(g, 6, 1, _DISTRACTORS[0], 6)
        _paint(g, 6, 8, _DISTRACTORS[0], 7)
        return g
    if name == "tied_match":
        # Two candidates both match the template's dihedral class.
        _paint(g, 1, 1, _BASE, 1)
        _paint(g, 1, 8, _xform(_BASE, 0), 4)   # match 1: identity
        _paint(g, 6, 8, _xform(_BASE, 2), 6)   # match 2: 180
        return g
    return g
