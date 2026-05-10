"""Generator for arc_puzzle_bank_21_set19_bundle:hard_p01 — transform-by-marker-count.

Rule: (0, 0) is the key color. Row 0 contains color-9 markers; their count is
the transform code. Take all key-color cells outside row 0 as a shape; output
the shape transformed by code.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_markers, no_body_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "81fe15ffd672"
VERSION = "1.1.0"
TASK_ID = "81fe15ffd672"

SUMMARY = "Row 0: key color at (0,0) + 1-3 color-9 markers; body has key-colored shape."

INVARIANTS = [
    "background is 0",
    "(0, 0) holds a key color (non-{0, 9})",
    "row 0 has 1-3 color-9 markers at distinct columns",
    "body (rows 1..h-1) holds a connected shape in the key color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_markers", "no_body_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "key_at_origin_plus_9_markers_plus_body",
                       "valid": "key_at_origin_plus_9_markers_plus_body"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_markers = ctx.draw_int("n_markers", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n_markers = ctx.draw_int("n_markers", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n_markers = ctx.draw_int("n_markers", 1, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    key_color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    g[0][0] = key_color
    cols = rng.sample(range(1, w), n_markers)
    for c in cols:
        g[0][c] = 9
    # body shape (3-5 cells)
    cells = [(2, 2)]
    seen = {(2, 2)}
    target = rng.randint(3, 5)
    while len(cells) < target:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if 1 <= nr < h and 0 <= nc < w and (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    for r, c in cells:
        g[r][c] = key_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_key":
        # markers + body but no key at (0,0)
        for c in [3, 5]: g[0][c] = 9
        g[3][3] = 4; g[3][4] = 4
        return g
    if name == "no_markers":
        # key + body but no 9-markers (count=0 → no transform code)
        g[0][0] = 4
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        return g
    if name == "no_body_shape":
        # key + markers but no body
        g[0][0] = 4
        for c in [2, 4, 6]: g[0][c] = 9
        return g
    return g
