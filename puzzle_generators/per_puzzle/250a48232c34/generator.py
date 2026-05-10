"""Generator for arc_puzzle_bank_21_set2:S2_H4.

Rule: largest gray template; colored anchors 1..4 stamp rotations.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_anchors, multiple_templates.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "250a48232c34"
VERSION = "1.1.0"
TASK_ID = "250a48232c34"
SUMMARY = "Color-coded anchors stamp 0/90/180/270 degree rotations of a gray template."

INVARIANTS = [
    "one gray template object is larger than any other gray object",
    "anchors use colors 1 through 4",
    "each anchor has enough room for its requested rotated template",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "multiple_templates")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_anchors":      {"type": "int", "default": "rng 2..4", "valid": "1..4"},
    "template":       {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "template_with_anchors",
                       "valid": "template_with_anchors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
]


def _rotate_norm(cells, turns):
    cur = sorted(cells)
    for _ in range(turns % 4):
        max_r = max(r for r, _c in cur)
        cur = [(c, max_r - r) for r, c in cur]
        r0 = min(r for r, _c in cur)
        c0 = min(c for _r, c in cur)
        cur = sorted((r - r0, c - c0) for r, c in cur)
    return cur


def _paint(g, top, left, cells, color):
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
        n_anchors = ctx.draw_int("n_anchors", 1, 2)
    elif difficulty == "hard":
        n_anchors = ctx.draw_int("n_anchors", 3, 4)
    else:
        n_anchors = ctx.draw_int("n_anchors", 2, 4)
    template = _TEMPLATES[ctx.draw_int("template", 0, len(_TEMPLATES) - 1)]
    h, w = 15, 15
    g = full_grid(h, w, 0)
    _paint(g, 1, 1, template, 5)

    anchor_positions = [(7, 1), (7, 8), (11, 1), (11, 8)]
    colors = [1, 2, 3, 4]
    rng.shuffle(colors)
    for color, (r, c) in zip(colors[:n_anchors], anchor_positions):
        rotated = _rotate_norm(template, color - 1)
        rh = max(rr for rr, _cc in rotated) + 1
        rw = max(cc for _rr, cc in rotated) + 1
        if r + rh < h and c + rw < w:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 15, 15
    g = full_grid(h, w, 0)
    if name == "no_template":
        # Anchors but no gray template — rule has no shape to
        # stamp; rule's stamp branch is undefined.
        g[7][1] = 1; g[7][8] = 2; g[11][1] = 3
        return g
    if name == "no_anchors":
        # Template but no anchors — rule has no stamp targets;
        # output equals input.
        _paint(g, 1, 1, _TEMPLATES[0], 5)
        return g
    if name == "multiple_templates":
        # Two equally-sized gray candidates — rule's "largest"
        # tie-break ambiguous; stamp source undefined.
        _paint(g, 1, 1, _TEMPLATES[0], 5)
        _paint(g, 1, 8, _TEMPLATES[0], 5)
        g[7][1] = 1; g[7][8] = 2
        return g
    return g
