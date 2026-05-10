"""Generator for arc_puzzle_bank_21_set11_s:S11_E5 — Stamp boundary at anchor offset.

Rule: anchor is the 1-cell. Largest non-1 component's boundary is
moved to start at the anchor's position (relative to its top-left).

Combinatorial axes (8): grid_h, grid_w, palette_kind, rect_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_rect, multiple_anchors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "023f0cc17b52"
VERSION = "1.1.0"
TASK_ID = "023f0cc17b52"
SUMMARY = "Solid filled rectangle of color C ≠ 1 + a single 1-cell anchor elsewhere."

INVARIANTS = [
    "exactly one 1-cell (the anchor)",
    "exactly one solid rectangle of one non-1 color, ≥3×3",
    "anchor is in a separate region from the rectangle",
    "the boundary stamp at anchor offset stays in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_rect", "multiple_anchors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "rect_plus_anchor",
                       "valid": "rect_plus_anchor"},
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
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    rh = rng.randint(3, 4); rw = rng.randint(3, 4)
    # Place rectangle in the upper-left half so the anchor offset moves boundary in-bounds
    r0 = rng.randint(0, max(1, h // 2 - rh + 1))
    c0 = rng.randint(0, max(1, w // 2 - rw + 1))
    color = rng.choice([2, 3, 4, 6, 7, 8, 9])
    draw_rect(g, r0, c0, rh, rw, color)
    # Anchor at position offset from rect top-left, ensuring stamp stays in bounds
    # We need anchor at (ar, ac) such that ar+rh-1 < h and ac+rw-1 < w
    for _ in range(40):
        ar = rng.randint(r0 + rh, h - rh)
        ac = rng.randint(0, w - rw)
        if g[ar][ac] == 0:
            g[ar][ac] = 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # rectangle but no 1-anchor → no offset to stamp at, identity
        draw_rect(g, 0, 0, 3, 3, 4)
        return g
    if name == "no_rect":
        # anchor but no rectangle → no boundary to stamp
        g[5][5] = 1
        return g
    if name == "multiple_anchors":
        # multiple 1-cells → ambiguous which is the anchor
        draw_rect(g, 0, 0, 3, 3, 4)
        g[5][2] = 1
        g[6][7] = 1
        return g
    return g
