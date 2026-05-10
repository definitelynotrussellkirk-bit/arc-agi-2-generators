"""Generator for v2_meta_puzzles:E7 — recolor color-6 by orientation.

Rule: each color-6 connected component is recolored: 8 if horizontal-only
(rmin == rmax), 2 otherwise.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_horizontal, only_vertical, no_color_6.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "852e47529f18"
VERSION = "1.1.0"
TASK_ID = "852e47529f18"
SUMMARY = "1 horizontal color-6 line + 1 vertical or rectangular color-6 motif."

INVARIANTS = [
    "background is 0",
    "exactly two color-6 motifs at distinct positions",
    "one motif is a horizontal line (single-row, length ≥3)",
    "the other motif spans multiple rows",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_horizontal", "only_vertical", "no_color_6")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motifs":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "horizontal_plus_vertical",
                       "valid": "horizontal_plus_vertical"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        # horizontal line
        length = rng.randint(3, 5)
        for _ in range(80):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - length)
            if not _free(g, r, c, r, c + length - 1): continue
            for cc in range(c, c + length):
                g[r][cc] = 6
            break
        else:
            continue
        # vertical line or rect
        ph = rng.randint(2, 3); pw = rng.randint(1, 2)
        for _ in range(80):
            r0 = rng.randint(0, h - ph); c0 = rng.randint(0, w - pw)
            if not _free(g, r0, c0, r0 + ph - 1, c0 + pw - 1): continue
            for dr in range(ph):
                for dc in range(pw):
                    g[r0 + dr][c0 + dc] = 6
            break
        else:
            continue
        return g
    raise ValueError("could not realize E7 layout")


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "only_horizontal":
        # all 6-motifs are horizontal-only → only the rmin==rmax → 8 branch fires
        for c in range(2, 5): g[1][c] = 6
        for c in range(4, 7): g[4][c] = 6
        return g
    if name == "only_vertical":
        # all 6-motifs span multiple rows → only the else → 2 branch fires
        for r in range(1, 4): g[r][2] = 6
        for r in range(3, 6): g[r][7] = 6
        return g
    if name == "no_color_6":
        # no color-6 cells → rule has no components to recolor
        g[2][3] = 4; g[4][6] = 8
        return g
    return g
