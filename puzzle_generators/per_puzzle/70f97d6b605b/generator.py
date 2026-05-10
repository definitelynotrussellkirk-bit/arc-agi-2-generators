"""Generator for v2_meta_puzzles:E1 — recolor 5-cell X-pentomino color-3 to 2.

Rule: each color-3 X-pentomino (5 cells: 4 corners + center of a 3x3) is
recolored to color 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_x, wrong_shape, wrong_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "70f97d6b605b"
VERSION = "1.1.0"
TASK_ID = "70f97d6b605b"

SUMMARY = "1-2 X-pentominoes (corners + center of 3x3) in color 3."

INVARIANTS = [
    "background is 0",
    "1-2 X-pentominoes (5 color-3 cells in 3x3 X-pattern: 4 corners + center)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_x", "wrong_shape", "wrong_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n":              {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1 (color 3)", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered_x_pentominoes",
                       "valid": "scattered_x_pentominoes"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 11)
        n = ctx.draw_int("n", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for _ in range(n):
            placed = False
            for _ in range(80):
                r0 = rng.randint(0, h - 3); c0 = rng.randint(0, w - 3)
                if not _free(g, r0, c0, r0 + 2, c0 + 2): continue
                for dr, dc in [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]:
                    g[r0 + dr][c0 + dc] = 3
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize E1 layout")


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_x":
        # Empty grid — no X-pentomino to recolor.
        return g
    if name == "wrong_shape":
        # 5-cell plus (X's structural cousin) and a 5-cell line — neither
        # is the corners+center X pattern, so the rule's match never fires.
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]:
            g[1 + dr][1 + dc] = 3
        for dc in range(5):
            g[5][2 + dc] = 3
        return g
    if name == "wrong_color":
        # The X-pentomino is drawn but in a non-color-3 palette — the
        # rule's color filter never matches it.
        for dr, dc in [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]:
            g[2 + dr][2 + dc] = 5
        return g
    return g
