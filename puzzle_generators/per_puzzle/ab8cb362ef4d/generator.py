"""Generator for 17b:m116 — apply gravity inside each box.

Rule: each 5-rect-frame contains scattered non-5 cells inside.
Gravity-down each column within the frame: non-5 cells fall to the
bottom of the frame interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_pebbles, all_at_bottom.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ab8cb362ef4d"
VERSION = "1.1.0"
TASK_ID = "ab8cb362ef4d"
SUMMARY = "1-2 5-frames each with 2-3 scattered non-5 cells inside (above the floor)."

INVARIANTS = [
    "background is 0",
    "≥1 5-rect-frame ≥4×4 with scattered non-5 cells in upper interior rows",
    "non-5 cells aren't already at the bottom interior row (so gravity moves them)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_pebbles", "all_at_bottom")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "5_frame_with_floating_pebbles",
                       "valid": "5_frame_with_floating_pebbles"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(40):
        fh = rng.randint(4, 5); fw = rng.randint(4, 5)
        r1 = rng.randint(0, h - fh)
        c1 = rng.randint(0, w - fw)
        r2 = r1 + fh - 1; c2 = c1 + fw - 1
        if _free(g, r1, c1, r2, c2):
            for c in range(c1, c2 + 1):
                g[r1][c] = 5; g[r2][c] = 5
            for r in range(r1, r2 + 1):
                g[r][c1] = 5; g[r][c2] = 5
            interior_upper = [(r, c) for r in range(r1 + 1, r2 - 1) for c in range(c1 + 1, c2)]
            n = rng.randint(2, 3)
            for r, c in rng.sample(interior_upper, min(n, len(interior_upper))):
                g[r][c] = rng.choice([2, 3, 4, 6, 7, 8, 9])
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # Pebbles but no 5-frame — chamber boundary undefined.
        g[3][3] = 4; g[5][7] = 6
        return g
    if name == "no_pebbles":
        # 5-frame but no pebbles inside — rule has nothing to drop.
        for c in range(2, 9): g[2][c] = 5; g[7][c] = 5
        for r in range(2, 8): g[r][2] = 5; g[r][8] = 5
        return g
    if name == "all_at_bottom":
        # Pebbles already on the bottom interior row — gravity is
        # no-op, output equals input.
        for c in range(2, 9): g[2][c] = 5; g[7][c] = 5
        for r in range(2, 8): g[r][2] = 5; g[r][8] = 5
        g[6][4] = 4; g[6][6] = 6; g[6][7] = 7
        return g
    return g
