"""Generator for arc_puzzle_bank_21_set21_bundle:medium_p04 — symmetry signature recolor.

Rule: each blob is recolored by the symmetry of its mask:
  HV-symmetric → 2, H-only → 3, V-only → 4, asymmetric → 6.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_hv (all blobs HV-sym → output recolors everything to
2, hides per-class branches); all_asym (no HV/H/V exemplars → hides
those branches); single_blob (only one shape → no contrast across
classes).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    SQUARE_2X2, PLUS_5, L_TROMINO_NE, L_TROMINO_SE, H_LINE_3, V_LINE_3,
)

GENERATOR_ID = "5a40ab695e6e"
VERSION = "1.1.0"
TASK_ID = "5a40ab695e6e"

SUMMARY = "3-4 fixed-shape blobs spanning HV-sym, H-sym, V-sym, asymmetric."

INVARIANTS = [
    "background is 0",
    "blobs include at least one HV-sym (square/plus), one V-sym (h-line), one asymmetric (L)",
    "blobs are all distinct colors and don't touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_hv", "all_asym", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "symmetry_class_blobs",
                       "valid": "symmetry_class_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    SQUARE_2X2,        # HV-sym
    PLUS_5,            # HV-sym
    H_LINE_3,          # V-sym (mirror across horizontal axis)
    V_LINE_3,          # H-sym (mirror across vertical axis)
    L_TROMINO_NE,      # asymmetric
    L_TROMINO_SE,      # asymmetric
]
_HV_ONLY = [SQUARE_2X2, PLUS_5]
_ASYM_ONLY = [L_TROMINO_NE, L_TROMINO_SE]


def _bbox_dims(cells):
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _free_at(g, r0, c0, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        rr, cc = r0 + r, c0 + c
        if not (0 <= rr < h and 0 <= cc < w):
            return False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0:
                    return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh, sw = _bbox_dims(shape)
    for _ in range(40):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        if _free_at(g, r0, c0, shape):
            paint_at(g, r0, c0, shape, color)
            return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        n = 3
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 16)
        n = 4
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n = None
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if n is None:
        n = rng.randint(3, 4)
    palette = rng.sample([1, 5, 6, 7, 8, 9, 2], n)
    shapes = rng.sample(_SHAPES, n)
    for shape, color in zip(shapes, palette):
        _place(g, rng, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "all_hv":
        # Every blob is HV-symmetric → rule's branches for H-only,
        # V-only, asymmetric never fire; output recolors everything
        # uniformly to 2.
        for shape, color, base in [(SQUARE_2X2, 1, (1, 1)),
                                   (PLUS_5, 5, (5, 7)),
                                   (SQUARE_2X2, 7, (7, 2))]:
            sh, sw = _bbox_dims(shape)
            r0, c0 = base
            if r0 + sh <= h and c0 + sw <= w:
                paint_at(g, r0, c0, shape, color)
        return g
    if name == "all_asym":
        # Every blob is asymmetric → only the "→6" branch fires.
        for shape, color, base in [(L_TROMINO_NE, 1, (1, 1)),
                                   (L_TROMINO_SE, 5, (5, 6)),
                                   (L_TROMINO_NE, 7, (7, 2))]:
            sh, sw = _bbox_dims(shape)
            r0, c0 = base
            if r0 + sh <= h and c0 + sw <= w:
                paint_at(g, r0, c0, shape, color)
        return g
    if name == "single_blob":
        # Only one blob — rule technically still applies, but no
        # contrast across symmetry classes.
        paint_at(g, 3, 4, PLUS_5, 6)
        return g
    return g
