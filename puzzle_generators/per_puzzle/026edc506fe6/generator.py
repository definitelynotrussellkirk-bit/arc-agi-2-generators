"""Generator for arc_additional_puzzle_bank_volume20:M134 — Translate color-1 cells by red→green vector.

Rule:
  - a = first red(2) cell, b = first green(3) cell
  - delta = b - a
  - Move every color-1 cell by delta, paint at the new positions with 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: zero_delta, no_shape, missing_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "026edc506fe6"
VERSION = "1.1.0"
TASK_ID = "026edc506fe6"
SUMMARY = "Red, green markers + a color-1 shape; translate the shape by red→green to color 4."

INVARIANTS = [
    "exactly one red(2) cell and one green(3) cell, both single-cell",
    "≥2 color-1 cells (form a shape)",
    "the translated positions of color-1 cells stay within the grid",
    "translated positions don't overlap existing non-bg cells",
    "delta between red and green is non-zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("zero_delta", "no_shape", "missing_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shape":        {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "shape_with_translation_markers",
                       "valid": "shape_with_translation_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        n_shape = ctx.draw_int("n_shape", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
        n_shape = ctx.draw_int("n_shape", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 10, 14)
        n_shape = ctx.draw_int("n_shape", 3, 5)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()

    shape = grow_blob(rng, h - 2, max(3, w // 3), used, n_shape)
    if shape is None:
        shape = {(1, 1)}
    shape_rs = [r for r, _ in shape]; shape_cs = [c for _, c in shape]
    sh = max(shape_rs) - min(shape_rs) + 1
    sw = max(shape_cs) - min(shape_cs) + 1
    sr_off = rng.randint(0, max(0, h - sh - 1))
    sc_off = rng.randint(0, max(0, max(1, w // 2) - sw - 1))
    shape = {(r - min(shape_rs) + sr_off, c - min(shape_cs) + sc_off)
             for r, c in shape}

    for r, c in shape:
        g[r][c] = 1
    used |= shape

    placed_red = False
    for _ in range(50):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if (r, c) in used: continue
        dr = rng.randint(-h // 2, h // 2)
        dc = rng.randint(0, max(1, w // 3))
        if dr == 0 and dc == 0: continue
        translated = {(rr + dr, cc + dc) for rr, cc in shape}
        if any(not (0 <= tr < h and 0 <= tc < w) for tr, tc in translated):
            continue
        if any((tr, tc) in used for tr, tc in translated):
            continue
        gr, gc = r + dr, c + dc
        if not (0 <= gr < h and 0 <= gc < w): continue
        if (gr, gc) in used: continue
        g[r][c] = 2
        g[gr][gc] = 3
        used.add((r, c)); used.add((gr, gc))
        placed_red = True
        break

    if not placed_red:
        for r in range(h):
            for c in range(w - 1):
                if (r, c) not in used and (r, c + 1) not in used:
                    g[r][c] = 2; g[r][c+1] = 3
                    return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "zero_delta":
        # red and green at the same position → delta is 0; translation is identity
        # (impossible to encode same cell with two colors, so place adjacent diagonal stand-in
        # where delta is the smallest possible; for true zero-delta we collapse markers)
        g[3][2] = 1; g[3][3] = 1; g[4][2] = 1   # color-1 shape
        g[5][6] = 2  # red — no green present means delta is undefined
        return g
    if name == "no_shape":
        # red, green markers but no color-1 shape → rule has nothing to translate
        g[2][3] = 2; g[2][6] = 3   # delta = (0, 3)
        return g
    if name == "missing_marker":
        # only red, no green → delta undefined; rule predicate fails
        g[3][2] = 1; g[3][3] = 1; g[4][2] = 1
        g[5][6] = 2
        return g
    return g
