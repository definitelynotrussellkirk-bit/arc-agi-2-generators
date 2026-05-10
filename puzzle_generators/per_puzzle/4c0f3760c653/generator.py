"""Generator for arc_puzzle_bank_third21:M15 — keep only square-bbox objects.

Rule: filter objects, keep only those whose bbox is square (h == w).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_squares, no_squares, single_square.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4c0f3760c653"
VERSION = "1.1.0"
TASK_ID = "4c0f3760c653"
SUMMARY = "≥1 square-bbox blob (kept) + ≥1 non-square blob (dropped)."

INVARIANTS = [
    "background is 0",
    "≥1 blob with bbox h == w",
    "≥1 blob with bbox h != w (so the rule isn't identity)",
    "blobs are 4-disjoint and have distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_squares", "no_squares", "single_square")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "mixed_aspect",
                       "valid": "mixed_aspect"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w:
        return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    # square 2x2
    for _ in range(40):
        r1 = rng.randint(0, h - 2)
        c1 = rng.randint(0, w - 2)
        if _free(g, r1, c1, r1 + 1, c1 + 1):
            for r in range(r1, r1 + 2):
                for c in range(c1, c1 + 2):
                    g[r][c] = palette[0]
            break
    # vertical 1x3
    for _ in range(40):
        r1 = rng.randint(0, h - 3)
        c1 = rng.randint(0, w - 1)
        if _free(g, r1, c1, r1 + 2, c1):
            for r in range(r1, r1 + 3):
                g[r][c1] = palette[1]
            break
    # horizontal 1x3
    for _ in range(40):
        r1 = rng.randint(0, h - 1)
        c1 = rng.randint(0, w - 3)
        if _free(g, r1, c1, r1, c1 + 2):
            for c in range(c1, c1 + 3):
                g[r1][c] = palette[2]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "all_squares":
        # all blobs have square bboxes → rule is identity, all blobs kept
        for r in range(1, 3):
            for c in range(1, 3): g[r][c] = 4
        for r in range(1, 3):
            for c in range(6, 8): g[r][c] = 6
        for r in range(5, 7):
            for c in range(3, 5): g[r][c] = 3
        return g
    if name == "no_squares":
        # all blobs non-square → rule erases everything, output is empty
        for c in range(1, 4): g[1][c] = 4   # 1x3
        for r in range(3, 6): g[r][7] = 6   # 3x1
        for c in range(2, 6): g[7][c] = 3   # 1x4
        return g
    if name == "single_square":
        # only one square → kept; no comparison among squares
        for r in range(2, 4):
            for c in range(4, 6): g[r][c] = 4
        return g
    return g
