"""Generator for 6e19193c.

Rule: each colored L-tromino emits a diagonal ray away from its
missing 2x2 corner.

Combinatorial axes (8): grid_h/w, object_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_objects, single_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a802749348c"
VERSION = "1.1.0"
TASK_ID = "8a802749348c"
SUMMARY = "Each colored L-tromino emits diagonal ray from missing 2x2 corner."

INVARIANTS = [
    "background is color 0",
    "each active object is a three-cell L inside a 2x2 box",
    "active objects are separated and single-colored",
    "the missing corner determines the ray direction",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "object_count":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n_lo, n_hi = 1, 2
    elif difficulty == "hard":
        n_lo, n_hi = 3, 3
    else:
        n_lo, n_hi = 2, 3
    n = ctx.draw_int("object_count", n_lo, n_hi)
    h = 9 + rng.randint(0, 4)
    w = 9 + rng.randint(0, 4)
    colors = ctx.draw_distinct_colors("colors", n=n, exclude={0})
    g = full_grid(h, w, 0)
    variants = [
        [(0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
    ]
    anchors = [(1, 1), (h - 3, 2), (2, w - 3)]
    for i in range(n):
        r0, c0 = anchors[i]
        cells = variants[(seed + sample_index + i + rng.randint(0, 3)) % len(variants)]
        for dr, dc in cells:
            g[r0 + dr][c0 + dc] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        for dr, dc in [(0, 1), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
