"""Generator for arc_puzzle_bank_21_set5_e:medium_e05.

Rule: color-1 and color-2 markers define a translation vector. A motif
made from other colors repeats by that vector until it would leave grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_motif, zero_vector.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dd47ca15f98a"
VERSION = "1.1.0"
TASK_ID = "dd47ca15f98a"

SUMMARY = "A motif repeats along the vector from the 1-marker to the 2-marker."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-1 marker and one color-2 marker",
    "all motif cells use colors other than 1 and 2",
    "at least two full translated motif copies fit in the grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_motif", "zero_vector")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "copy_count":     {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "marker_pair_with_motif",
                       "valid": "marker_pair_with_motif"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
]

_VECTORS = [(0, 2), (0, 3), (2, 0), (3, 0), (1, 2), (2, 1)]


def _stamp(g, cells, top, left, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    cells = list(rng.choice(_MOTIFS))
    dr, dc = rng.choice(_VECTORS)
    if difficulty == "easy":
        copies = ctx.draw_int("copy_count", 2, 2)
    elif difficulty == "hard":
        copies = ctx.draw_int("copy_count", 4, 5)
    else:
        copies = ctx.draw_int("copy_count", 2, 4)

    motif_h = max(r for r, _c in cells) + 1
    motif_w = max(c for _r, c in cells) + 1
    min_h = 4 + motif_h + (copies - 1) * dr
    min_w = 4 + motif_w + (copies - 1) * dc
    if difficulty == "easy":
        h = max(min_h, ctx.draw_int("grid_h", 9, 10))
        w = max(min_w, ctx.draw_int("grid_w", 9, 11))
    elif difficulty == "hard":
        h = max(min_h, ctx.draw_int("grid_h", 12, 16))
        w = max(min_w, ctx.draw_int("grid_w", 13, 17))
    else:
        h = max(min_h, ctx.draw_int("grid_h", 9, 12))
        w = max(min_w, ctx.draw_int("grid_w", 9, 14))

    g = full_grid(h, w, 0)
    g[0][0] = 1
    g[dr][dc] = 2

    max_top = h - motif_h - (copies - 1) * dr
    max_left = w - motif_w - (copies - 1) * dc
    top = rng.randint(3, max_top)
    left = rng.randint(1, max_left)
    color = rng.choice([3, 4, 5, 6, 7, 8, 9])
    _stamp(g, cells, top, left, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # Motif present but no 1/2 markers — rule's vector readout
        # fails; no copies generated.
        for r, c in [(4, 4), (4, 5), (5, 5), (6, 5)]: g[r][c] = 4
        return g
    if name == "no_motif":
        # Markers present but no motif cells — rule has nothing
        # to repeat along the vector.
        g[0][0] = 1
        g[2][2] = 2
        return g
    if name == "zero_vector":
        # Markers coincide (delta = 0,0) — rule's translation is
        # identity; motif never advances; rule's repeat invisible.
        g[0][0] = 1
        g[0][0] = 2
        for r, c in [(4, 4), (4, 5), (5, 5)]: g[r][c] = 4
        return g
    return g
