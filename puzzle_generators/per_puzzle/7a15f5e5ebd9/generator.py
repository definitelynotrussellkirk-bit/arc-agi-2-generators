"""Generator for arc_additional_puzzles_21_set18_bundle:E120 — Stamp 4-shape at 2-anchor.

Rule: 9-cell anchors a 4-shape; 2-cells are stamp anchors. For each
2-anchor, draw 4-cells at the same offsets relative to the 2-anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_anchors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_2_anchor, no_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7a15f5e5ebd9"
VERSION = "1.1.0"
TASK_ID = "7a15f5e5ebd9"
SUMMARY = "9-anchor + 4-shape (2-3 cells) + 1-2 single 2-anchors at distant positions."

INVARIANTS = [
    "exactly one 9-cell (template anchor)",
    "2-3 4-cells forming a connected shape next to the 9",
    "1-2 single 2-cells, far from 9 (so stamp stays in-bounds)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_2_anchor", "no_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "1", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "9_topleft_2_bottomright",
                       "valid": "9_topleft_2_bottomright"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = [
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (0, 2), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
    [(0, 1), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape = rng.choice(SHAPES)
    sh = max(r for r, c in shape) + 1
    sw = max(c for r, c in shape) + 1
    r9 = rng.randint(1, max(1, h // 3))
    c9 = rng.randint(1, max(1, w // 3))
    g[r9][c9] = 9
    for dr, dc in shape:
        if 0 <= r9 + dr < h and 0 <= c9 + dc < w:
            g[r9 + dr][c9 + dc] = 4
    for _ in range(40):
        ar = rng.randint(h // 2 + 1, h - 1)
        ac = rng.randint(w // 2 + 1, w - 2)
        if g[ar][ac] == 0:
            g[ar][ac] = 2
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # No 9-cell template anchor — rule has no offsets to read.
        for dr, dc in SHAPES[0]:
            g[1 + dr][1 + dc] = 4
        g[6][8] = 2
        return g
    if name == "no_2_anchor":
        # 9-anchor + shape but no 2-anchors — rule has nowhere to
        # stamp the offsets to.
        g[1][1] = 9
        for dr, dc in SHAPES[0]:
            if 0 <= 1 + dr < h and 0 <= 1 + dc < w:
                g[1 + dr][1 + dc] = 4
        return g
    if name == "no_shape":
        # 9-anchor and 2-anchor present but no 4-shape — rule's
        # offset list is empty, so the stamp is a no-op.
        g[1][1] = 9
        g[6][8] = 2
        return g
    return g
