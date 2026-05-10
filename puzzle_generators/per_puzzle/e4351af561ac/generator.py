"""Generator for 3b:m21 — keep blobs matching template under rotation.

Rule: a 1-color template blob defines the shape. Blobs (in any color)
matching that shape under any rotation are kept; others dropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, all_match, no_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    L_TROMINO_NE, L_TROMINO_SE, T_TETROMINO,
)

GENERATOR_ID = "e4351af561ac"
VERSION = "1.1.0"
TASK_ID = "e4351af561ac"
SUMMARY = "1 color-1 L-template + 2-3 other-color L blobs (some rotation-matching, some different shape)."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 L-tromino (the template)",
    "≥1 other-color blob with same shape under rotation (kept)",
    "≥1 other-color blob with different shape (dropped)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "all_match", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "template_plus_blobs",
                       "valid": "template_plus_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _bbox(cells):
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _free(g, r0, c0, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        rr, cc = r0 + r, c0 + c
        if not (0 <= rr < h and 0 <= cc < w): return False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    placements = [
        (L_TROMINO_NE, 1),  # template
        (L_TROMINO_SE, palette[0]),  # rotation match (also L)
        (T_TETROMINO, palette[1]),  # different shape (T)
    ]
    rng.shuffle(placements)
    for shape, color in placements:
        sh, sw = _bbox(shape)
        for _ in range(40):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            if _free(g, r0, c0, shape):
                paint_at(g, r0, c0, shape, color)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_template":
        # No color-1 template — rule has no target shape.
        paint_at(g, 1, 1, L_TROMINO_SE, 4)
        paint_at(g, 1, 6, T_TETROMINO, 5)
        return g
    if name == "all_match":
        # All non-template blobs match the template under rotation — rule keeps everything.
        paint_at(g, 1, 1, L_TROMINO_NE, 1)
        paint_at(g, 5, 1, L_TROMINO_SE, 4)
        paint_at(g, 5, 6, L_TROMINO_NE, 5)
        return g
    if name == "no_match":
        # Template present but no rotation match anywhere — rule keeps only template.
        paint_at(g, 1, 1, L_TROMINO_NE, 1)
        paint_at(g, 5, 1, T_TETROMINO, 4)
        paint_at(g, 5, 6, T_TETROMINO, 5)
        return g
    return g
