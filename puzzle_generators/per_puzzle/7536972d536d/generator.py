"""Generator for arc_additional_puzzles_21_set13_bundle:E88 — Mirror non-{0,8} across full 8-row.

Rule: find full row or col of 8s; mirror each non-{0,8} cell across.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_content, content_on_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7536972d536d"
VERSION = "1.1.0"
TASK_ID = "7536972d536d"
SUMMARY = "Full-width 8-row divider in middle; left side has non-8 cells."

INVARIANTS = [
    "exactly 1 full-width row of 8s",
    "left side has 2-3 isolated non-{0,8} cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_content", "content_on_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "str", "default": "rng row|col", "valid": "row|col"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "8_divider_with_one_side_content",
                       "valid": "8_divider_with_one_side_content"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
    w = 9
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    if rng.random() < 0.5:
        gr = h // 2
        for c in range(w):
            g[gr][c] = 8
        palette = [1, 2, 3, 4, 5, 6, 7, 9]
        for _ in range(rng.randint(2, 3)):
            for _ in range(20):
                r = rng.randint(0, gr - 1); c = rng.randint(0, w - 1)
                if g[r][c] == 0:
                    g[r][c] = rng.choice(palette)
                    break
    else:
        gc = w // 2
        for r in range(h):
            g[r][gc] = 8
        palette = [1, 2, 3, 4, 5, 6, 7, 9]
        for _ in range(rng.randint(2, 3)):
            for _ in range(20):
                r = rng.randint(0, h - 1); c = rng.randint(0, gc - 1)
                if g[r][c] == 0:
                    g[r][c] = rng.choice(palette)
                    break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # content without 8-divider → no axis to mirror across
        g[1][2] = 4
        g[2][3] = 6
        return g
    if name == "no_content":
        # 8-divider alone → nothing to mirror
        for c in range(w):
            g[3][c] = 8
        return g
    if name == "content_on_both_sides":
        # divider with content on both sides → "one side only" precondition fails
        for c in range(w):
            g[3][c] = 8
        g[1][2] = 4
        g[5][6] = 6  # also on bottom side
        return g
    return g
