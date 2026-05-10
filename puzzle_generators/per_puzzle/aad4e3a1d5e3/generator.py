"""Generator for arc_additional_puzzles_21_set8:H50.

A full vertical color-5 guide and horizontal color-6 guide define mirror axes.
The rule reflects the non-guide object into all four quadrants.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_guides, no_motif, motif_on_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aad4e3a1d5e3"
VERSION = "1.1.0"
TASK_ID = "aad4e3a1d5e3"
SUMMARY = "A colored motif appears in one guide-defined quadrant and mirrors across both guides."

INVARIANTS = [
    "one nearly full color-5 vertical guide",
    "one full color-6 horizontal guide",
    "all non-guide colored cells lie on one side of both guides",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guides", "no_motif", "motif_on_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15 odd", "valid": "9..19 odd"},
    "grid_w":         {"type": "int", "default": "rng 11..17 odd", "valid": "9..21 odd"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "5col_6row_guides_quadrant_motif",
                       "valid": "5col_6row_guides_quadrant_motif"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 11, 17)
    if h % 2 == 0:
        h += 1
    if w % 2 == 0:
        w += 1
    axis_r = h // 2
    axis_c = w // 2
    motif = _MOTIFS[ctx.draw_int("motif", 0, len(_MOTIFS) - 1)]
    mh = max(r for r, _c in motif) + 1
    mw = max(c for _r, c in motif) + 1

    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][axis_c] = 5
    for c in range(w):
        g[axis_r][c] = 6

    top = rng.randint(1, axis_r - mh - 1)
    left = rng.randint(1, axis_c - mw - 1)
    color = rng.choice([1, 2, 3, 4, 7, 8, 9])
    for r, c in motif:
        g[top + r][left + c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_guides":
        # motif but no 5/6 guide axes → no mirror axes defined
        for r, c in _MOTIFS[0]: g[1 + r][1 + c] = 4
        return g
    if name == "no_motif":
        # guides but no motif → nothing to reflect
        for r in range(h): g[r][w // 2] = 5
        for c in range(w): g[h // 2][c] = 6
        return g
    if name == "motif_on_axis":
        # motif lies on guide axis → reflection is identity
        for r in range(h): g[r][w // 2] = 5
        for c in range(w): g[h // 2][c] = 6
        # overwrite axis cells with motif color (also breaks invariant)
        g[2][w // 2] = 4; g[3][w // 2] = 4
        return g
    return g
