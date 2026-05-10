"""Generator for 13b:m91 — select LR-symmetric blob, recolor.

Rule: same as 12b:m83 — pick the unique LR-symmetric blob and recolor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, all_symmetric, all_asymmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    PLUS_5, T_TETROMINO, L_TROMINO_NE, L_TROMINO_SE,
)

GENERATOR_ID = "a78185b4bd20"
VERSION = "1.1.0"
TASK_ID = "a78185b4bd20"
SUMMARY = "1 LR-symmetric blob + 2 LR-asymmetric distractors."

INVARIANTS = [
    "background is 0",
    "exactly one LR-symmetric blob",
    "≥1 LR-asymmetric blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "all_symmetric", "all_asymmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "isolated_blobs",
                       "valid": "isolated_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
        if not (0 <= rr < h and 0 <= cc < w):
            return False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0:
                    return False
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
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sym = rng.choice([PLUS_5, T_TETROMINO])
    asym = rng.choice([L_TROMINO_NE, L_TROMINO_SE])
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    placements = [(sym, palette[0]), (asym, palette[1]), (asym, palette[2])]
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
    if name == "no_blobs":
        # Empty grid — rule has no blob to select.
        return g
    if name == "all_symmetric":
        # Every blob is LR-symmetric — "the unique symmetric one" is ambiguous.
        paint_at(g, 1, 1, PLUS_5, 4)
        paint_at(g, 1, 6, T_TETROMINO, 5)
        paint_at(g, 5, 1, PLUS_5, 6)
        return g
    if name == "all_asymmetric":
        # No symmetric blob — rule has no candidate to select.
        paint_at(g, 1, 1, L_TROMINO_NE, 4)
        paint_at(g, 1, 6, L_TROMINO_SE, 5)
        paint_at(g, 5, 1, L_TROMINO_NE, 6)
        return g
    return g
