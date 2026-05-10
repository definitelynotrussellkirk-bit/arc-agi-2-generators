"""Generator for arc_puzzle_bank_fourteenth21:M93 — flood frame interior from seed.

Rule: a 2-rect-frame contains exactly one non-2 seed inside. Fill the
interior with the seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seed, multiple_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cb3541dd8827"
VERSION = "1.1.0"
TASK_ID = "cb3541dd8827"
SUMMARY = "One 2-rect-frame ≥4×4 with exactly one non-2 seed inside."

INVARIANTS = [
    "background is 0",
    "exactly one 2-rect-frame, ≥4x4 with empty interior",
    "exactly one non-2 seed inside; interior has ≥3 0-cells (so fill is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seed", "multiple_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "rng 4..5", "valid": "4..6"},
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
    fh = rng.randint(4, 5)
    fw = rng.randint(5, 7)
    r1 = rng.randint(0, h - fh)
    c1 = rng.randint(0, w - fw)
    r2 = r1 + fh - 1
    c2 = c1 + fw - 1
    for c in range(c1, c2 + 1):
        g[r1][c] = 2; g[r2][c] = 2
    for r in range(r1, r2 + 1):
        g[r][c1] = 2; g[r][c2] = 2
    seed_color = rng.choice([3, 4, 5, 6, 7, 8, 9])
    interior = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    sr, sc = rng.choice(interior)
    g[sr][sc] = seed_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # seed but no 2-frame → no interior to flood
        g[3][4] = 6
        return g
    if name == "no_seed":
        # frame but no seed → no color to fill interior with
        for c in range(2, 8): g[1][c] = 2; g[6][c] = 2
        for r in range(1, 7): g[r][2] = 2; g[r][7] = 2
        return g
    if name == "multiple_seeds":
        # two seeds inside frame → ambiguous fill color
        for c in range(2, 8): g[1][c] = 2; g[6][c] = 2
        for r in range(1, 7): g[r][2] = 2; g[r][7] = 2
        g[3][4] = 4; g[4][6] = 6
        return g
    return g
