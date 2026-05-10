"""Generator for arc_additional_puzzles_21_set22_bundle:M151 — move payload by 2-to-3 vector.

Rule: the 2 and 3 markers define a vector; all other colored payload
cells move by that vector.

Combinatorial axes (8): grid_h, grid_w, palette_kind, vector,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_payload, payload_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "10599ac9904a"
VERSION = "1.1.0"
TASK_ID = "10599ac9904a"
SUMMARY = "The last 2 and last 3 markers define a vector; all other colored payload cells move by that vector."

INVARIANTS = [
    "markers 2 and 3 define a small in-bounds translation",
    "payload colors exclude 2 and 3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_payload", "payload_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "vector":         {"type": "str", "default": "rng vec",
                       "valid": "(1,2)|(2,1)|(-1,2)|(2,-1)"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "markers_with_payload",
                       "valid": "markers_with_payload"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    dr, dc = rng.choice([(1, 2), (2, 1), (-1, 2), (2, -1)])
    g = full_grid(h, w, 0)
    mr = 1 if dr >= 0 else 3
    mc = 1 if dc >= 0 else w - 3
    g[mr][mc] = 2
    g[mr + dr][mc + dc] = 3
    colors = list(ctx.draw_distinct_colors("payload", n=3, exclude=[0, 2, 3]))
    occupied = {(mr, mc), (mr + dr, mc + dc)}
    candidates = [
        (r, c)
        for r in range(1, h - 1)
        for c in range(1, w - 1)
        if (r, c) not in occupied
        and (r + dr, c + dc) not in occupied
        and 0 <= r + dr < h
        and 0 <= c + dc < w
    ]
    rng.shuffle(candidates)
    for color, (r, c) in zip(colors, candidates[:3]):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # payload but no 2/3 markers → no translation vector defined
        g[3][3] = 4
        g[5][6] = 6
        g[7][2] = 7
        return g
    if name == "no_payload":
        # markers define vector but no payload to translate
        g[1][1] = 2
        g[3][3] = 3
        return g
    if name == "payload_at_edge":
        # payload too close to edge → translation lands out of bounds
        g[1][1] = 2; g[3][3] = 3   # vector (2,2)
        g[h - 1][w - 1] = 4   # destination would be (h+1, w+1) - off grid
        g[h - 2][w - 2] = 6
        return g
    return g
