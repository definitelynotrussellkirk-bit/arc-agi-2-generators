"""Generator for v0_original:medium_07 — fill hollow rectangle frame interior with same color.

Rule: each hollow rectangle frame ≥3×3 has its bg-cell interior
filled with its own border color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_extra,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, solid_frame, frame_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "524410ebe7b7"
VERSION = "1.1.0"
TASK_ID = "524410ebe7b7"
SUMMARY = "1 hollow rectangle frame + 1-2 distinct-color small shapes nearby."

INVARIANTS = [
    "background is 0",
    "exactly one rectangle frame (full perimeter, ≥3×3) of one non-bg color",
    "1-2 small shapes (1-2 cells each) of distinct other colors elsewhere",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "solid_frame", "frame_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_extra":        {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "frame_with_distractors",
                       "valid": "frame_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SMALL = [
    [(0, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        n_extra = ctx.draw_int("n_extra", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
        n_extra = ctx.draw_int("n_extra", 1, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 10)
        n_extra = ctx.draw_int("n_extra", 0, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 1 + n_extra))
    rh = rng.randint(3, min(5, h - 1))
    rw = rng.randint(3, min(5, w - 1))
    r1 = rng.randint(0, h - rh)
    c1 = rng.randint(0, w - rw)
    r2 = r1 + rh - 1
    c2 = c1 + rw - 1
    draw_frame(g, r1, c1, r2, c2, palette[0])
    placed: list[tuple[int, int, int, int]] = [(r1 - 1, c1 - 1, r2 + 1, c2 + 1)]
    for color in palette[1:]:
        small = rng.choice(_SMALL)
        sh = max(c[0] for c in small) + 1
        sw = max(c[1] for c in small) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, small, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # No hollow frame — rule has no interior to fill.
        g[1][1] = 4; g[5][6] = 5
        return g
    if name == "solid_frame":
        # Solid block, not hollow — rule expects perimeter only, has no interior gap.
        for r in range(1, 5):
            for c in range(1, 5): g[r][c] = 4
        return g
    if name == "frame_already_filled":
        # Frame's interior already filled with the border color — rule is no-op.
        for r in range(1, 5):
            for c in range(1, 5): g[r][c] = 4
        return g
    return g
