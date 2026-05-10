"""Generator for arc_puzzle_bank_21_set6_s:S6_M4 — seeded checker fill.

Rule: a single rect-frame contains one seed cell of a different color.
Fill the frame interior with a checker pattern matching the seed's
parity (cells with (r+c) parity == seed parity become seed-color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seed, multiple_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f245a7809423"
VERSION = "1.1.0"
TASK_ID = "f245a7809423"
SUMMARY = "One rect-frame (≥4×5) with a single seed inside (different color)."

INVARIANTS = [
    "background is 0",
    "exactly one rect-frame, color != seed color",
    "frame interior has exactly one seed cell",
    "frame interior has ≥3 cells of opposite parity (so checker fill is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seed", "multiple_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "rng 4..5", "valid": "4..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "frame_with_seed",
                       "valid": "frame_with_seed"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    fc, sc = palette
    fh = rng.randint(4, 5)
    fw = rng.randint(5, 7)
    r1 = rng.randint(0, h - fh)
    c1 = rng.randint(0, w - fw)
    r2 = r1 + fh - 1
    c2 = c1 + fw - 1
    for c in range(c1, c2 + 1):
        g[r1][c] = fc; g[r2][c] = fc
    for r in range(r1, r2 + 1):
        g[r][c1] = fc; g[r][c2] = fc
    inner = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    sr, sk = rng.choice(inner)
    g[sr][sk] = sc
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # seed without frame → no boundary to fill within
        g[3][4] = 6
        return g
    if name == "no_seed":
        # frame without seed → no parity color to checker with
        for c in range(1, 8):
            g[1][c] = 4; g[5][c] = 4
        for r in range(1, 6):
            g[r][1] = 4; g[r][7] = 4
        return g
    if name == "multiple_seeds":
        # frame with 2 seeds → "exactly one seed" precondition fails
        for c in range(1, 8):
            g[1][c] = 4; g[5][c] = 4
        for r in range(1, 6):
            g[r][1] = 4; g[r][7] = 4
        g[2][3] = 6
        g[3][5] = 7  # second seed (different color too)
        return g
    return g
