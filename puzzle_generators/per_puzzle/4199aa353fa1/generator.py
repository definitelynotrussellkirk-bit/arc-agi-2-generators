"""Generator for `arc_additional_puzzle_bank_volume21:M144` — input
has a control marker (one cell of color 2/3/4/5/6) selecting a rotation
direction, plus a blue(1) template shape. Rule rotates the template
based on the control marker color.

Concept membership: 2 puzzles share this rule.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, marker, texture.
Degenerates: no_marker, no_template, multiple_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4199aa353fa1"
VERSION = "1.1.0"
TASK_ID = "4199aa353fa1"
SUMMARY = "Control marker + blue template; rule rotates the template based on marker color."

INVARIANTS = [
    "background is 0",
    "exactly one control marker cell, color in {2, 3, 4, 5, 6}",
    ">=2 blue(1) cells in a contiguous L/J/T-shape",
    "template is asymmetric",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_template", "multiple_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker":         {"type": "color", "default": "rng of {2,3,4,5,6}",
                       "valid": "{2,3,4,5,6}"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "marker_then_blue_template",
                       "valid": "marker_then_blue_template"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 17)
        w = ctx.draw_int("grid_w", 14, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
    marker = ctx.draw_choice("marker", [2, 3, 4, 5, 6])
    rng = ctx.draw_rng("placement")

    g = full_grid(h, w, 0)
    mr = rng.randint(1, h - 2); mc = rng.randint(1, w - 2)
    g[mr][mc] = marker
    for _try in range(15):
        br = rng.randint(2, h - 4); bc = rng.randint(2, w - 4)
        if abs(br - mr) <= 2 and abs(bc - mc) <= 2: continue
        if all(g[br + dr][bc + dc] == 0 for dr in range(3) for dc in range(2)):
            g[br][bc] = 1
            g[br + 1][bc] = 1
            g[br + 2][bc] = 1
            g[br + 2][bc + 1] = 1
            return g
    return [[0]]


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # Blue template but no control marker — rule has no
        # rotation-direction code to read.
        g[3][3] = 1; g[4][3] = 1; g[5][3] = 1; g[5][4] = 1
        return g
    if name == "no_template":
        # Marker but no blue template — rule has nothing to rotate.
        g[5][5] = 3
        return g
    if name == "multiple_markers":
        # Two control markers in different colors — rule's
        # exactly-one-control precondition fails; rotation lookup
        # is ambiguous.
        g[2][2] = 3
        g[8][8] = 5
        g[5][5] = 1; g[6][5] = 1; g[7][5] = 1; g[7][6] = 1
        return g
    return g
