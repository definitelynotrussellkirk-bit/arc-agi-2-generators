"""Generator for arc_additional_puzzles_21_set12_bundle:M84 — 2x2 grid of motif transform variants.

Rule: the 4 corner cells encode transforms (1=rot-cw, 2=rot-180,
3=flip-lr, 4=flip-ud). The non-corner non-zero cells form a "motif"
(cropped to bbox). Output is a 2x2 packing of (motif transformed by
each corner's code), placed top-left, top-right, bottom-left,
bottom-right respectively.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_codes, no_motif, symmetric_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "d01b33f4a589"
VERSION = "1.1.0"
TASK_ID = "d01b33f4a589"
SUMMARY = "4 corner transform codes (1..4) + a small motif in the middle."

INVARIANTS = [
    "background is 0",
    "the 4 corner cells each carry a transform code in {1, 2, 3, 4}",
    "exactly one connected motif (1-2 colors) sits strictly between the corners",
    "motif uses no value in {1, 2, 3, 4} and avoids the corner cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_codes", "no_motif", "symmetric_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "corner_codes_motif_inside",
                       "valid": "corner_codes_motif_inside"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    codes = [1, 2, 3, 4]
    rng.shuffle(codes)
    g[0][0] = codes[0]
    g[0][w - 1] = codes[1]
    g[h - 1][0] = codes[2]
    g[h - 1][w - 1] = codes[3]
    motif_color = rng.choice(list(random_palette(rng, 1, exclude={1, 2, 3, 4})))
    motif = rng.choice(_MOTIFS)
    sh = max(c[0] for c in motif) + 1
    sw = max(c[1] for c in motif) + 1
    r0 = rng.randint(2, h - sh - 2)
    c0 = rng.randint(2, w - sw - 2)
    paint_at(g, r0, c0, motif, motif_color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    motif = [(0, 0), (1, 0), (1, 1)]
    if name == "no_corner_codes":
        # Motif in middle but corners are empty — rule has no per-cell
        # transform codes to apply to its 2x2 packing.
        paint_at(g, 4, 4, motif, 6)
        return g
    if name == "no_motif":
        # Corner codes but no motif — rule's 2x2 packing has nothing
        # to transform.
        g[0][0] = 1; g[0][w - 1] = 2
        g[h - 1][0] = 3; g[h - 1][w - 1] = 4
        return g
    if name == "symmetric_motif":
        # Motif is fully rotation-and-flip symmetric (e.g., 2x2 square)
        # — every transform yields the same shape, rule's 4 variants
        # collapse to the same output.
        g[0][0] = 1; g[0][w - 1] = 2
        g[h - 1][0] = 3; g[h - 1][w - 1] = 4
        for r, c in [(4, 4), (4, 5), (5, 4), (5, 5)]: g[r][c] = 6
        return g
    return g
