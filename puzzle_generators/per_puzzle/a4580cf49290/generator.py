"""Generator for 17b:m113 — select object by legend and transform.

Rule: key color at (0,0), transform code at (0, w-1). Find shape with
matching key color; output is its crop transformed per code.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_match_shape, no_code.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a4580cf49290"
VERSION = "1.1.0"
TASK_ID = "a4580cf49290"
SUMMARY = "Key color at (0,0) + transform code at (0, w-1) + 2-3 shapes incl. one matching key."

INVARIANTS = [
    "background is 0",
    "cell (0,0) is the key color (some non-bg)",
    "cell (0, w-1) is a transform code (small integer)",
    "2-3 multi-cell shapes elsewhere; one is in the key color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_match_shape", "no_code")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "header_corners_shapes_below",
                       "valid": "header_corners_shapes_below"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(2, h - sh); c0 = rng.randint(1, w - sw - 1)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([3, 4, 6, 7, 8, 9], 3)
    key = palette[0]
    code = rng.choice([1, 2, 3, 4, 5])
    g[0][0] = key
    g[0][w - 1] = code
    for color in palette:
        _place(g, rng, rng.choice(_SHAPES), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_key":
        # No key color at (0,0) — rule has no shape selector.
        g[0][w - 1] = 2
        for r, c in [(2, 2), (3, 2), (4, 2)]: g[r][c] = 4
        for r, c in [(6, 6), (6, 7), (7, 7)]: g[r][c] = 5
        return g
    if name == "no_match_shape":
        # Key set but no shape in key color — rule selects nothing.
        g[0][0] = 4
        g[0][w - 1] = 2
        for r, c in [(2, 2), (3, 2), (4, 2)]: g[r][c] = 5
        for r, c in [(6, 6), (6, 7), (7, 7)]: g[r][c] = 6
        return g
    if name == "no_code":
        # Key set but no transform code — rule has no transformation to apply.
        g[0][0] = 4
        for r, c in [(2, 2), (3, 2), (4, 2)]: g[r][c] = 4
        for r, c in [(6, 6), (6, 7), (7, 7)]: g[r][c] = 5
        return g
    return g
