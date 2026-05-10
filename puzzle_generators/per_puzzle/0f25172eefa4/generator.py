"""Generator for 9b:m59 — transform strip from key row.

Rule: the last row holds 1-N transform codes (non-bg cells). The
source = the body (rows 0..h-2) cropped to non-bg bbox. Output
hstacks the source under each key's transform with 1-col gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_keys, no_body, symmetric_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0f25172eefa4"
VERSION = "1.1.0"
TASK_ID = "0f25172eefa4"

SUMMARY = "1 body shape (rows 0..h-2) + 1-3 transform-code cells in the last row."

INVARIANTS = [
    "background is 0",
    "exactly one isolated multi-cell shape in rows 0..h-2",
    "1-3 non-bg cells in the last row, each a small transform code",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_keys", "no_body", "symmetric_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "body_with_key_row",
                       "valid": "body_with_key_row"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    body_color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    shape = rng.choice(_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    placed = False
    for _ in range(40):
        r0 = rng.randint(0, h - 2 - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = body_color
        placed = True; break
    if not placed:
        raise ValueError("could not place body shape")
    n_keys = rng.randint(1, 3)
    key_cols = rng.sample(range(0, w), n_keys)
    for c in key_cols:
        g[h - 1][c] = rng.randint(1, 5)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_keys":
        # Body but empty key row — rule has no transforms to apply;
        # output is empty strip.
        for r, c in [(2, 3), (3, 3), (3, 4), (4, 4)]: g[r][c] = 4
        return g
    if name == "no_body":
        # Key row but no body in rows 0..h-2 — rule has nothing
        # to transform.
        g[h - 1][2] = 1; g[h - 1][5] = 3
        return g
    if name == "symmetric_body":
        # Body shape symmetric — every transform key produces the
        # same shape; rule's output strip is uniform.
        for r, c in [(2, 4), (2, 5), (3, 4), (3, 5)]: g[r][c] = 4
        g[h - 1][2] = 1; g[h - 1][5] = 3
        return g
    return g
