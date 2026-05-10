"""Generator for v2_meta_puzzles:E6 — recolor yellow plus centers.

Rule: for each yellow plus, recolor only its center cell to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pluses,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, partial_arms, wrong_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b018768ee9e2"
VERSION = "1.1.0"
TASK_ID = "b018768ee9e2"

SUMMARY = "1-2 plus-shaped color-4 patterns with yellow centers."

INVARIANTS = [
    "background is 0",
    "1-2 plus-shaped patterns: center and four cardinal cells are color 4",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pluses", "partial_arms", "wrong_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pluses":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_yellow_pluses",
                       "valid": "spaced_yellow_pluses"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 7)
        n = ctx.draw_int("n_pluses", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_pluses", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n_pluses", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for _ in range(n):
            placed = False
            for _ in range(80):
                r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
                if not _free(g, r - 1, c - 1, r + 1, c + 1): continue
                g[r][c] = 4
                g[r - 1][c] = 4
                g[r + 1][c] = 4
                g[r][c - 1] = 4
                g[r][c + 1] = 4
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize E6 layout")


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # blank → no plus shapes, rule has no centers to recolor
        return g
    if name == "partial_arms":
        # 4-cell partial pluses (missing one arm) → predicate "exact plus" fails
        g[2][3] = 4; g[1][3] = 4; g[3][3] = 4; g[2][2] = 4  # missing right arm
        return g
    if name == "wrong_color":
        # exact pluses but in color 6 (red→magenta), not 4 (yellow) → predicate fails
        g[2][3] = 6; g[1][3] = 6; g[3][3] = 6; g[2][2] = 6; g[2][4] = 6
        return g
    return g
