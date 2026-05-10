"""Generator for arc_puzzle_bank_21_set17_bundle:medium_p03 — flood framed rooms from seed.

Rule: each rect-frame contains exactly one non-frame seed; fill the
interior with the seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seed, multi_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3b75d3395ebb"
VERSION = "1.1.0"
TASK_ID = "3b75d3395ebb"
SUMMARY = "1-2 5-rect-frames each with one non-5 seed inside."

INVARIANTS = [
    "background is 0",
    "≥1 5-rect-frame ≥4×4 with exactly one non-5 seed inside",
    "frames don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seed", "multi_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "5_frame_with_seed",
                       "valid": "5_frame_with_seed"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    seed_palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n)
    for color in seed_palette:
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
                interior = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
                sr, sc = rng.choice(interior)
                g[sr][sc] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # Seed but no 5-frame — rule has no frame to flood.
        g[3][5] = 4
        return g
    if name == "no_seed":
        # 5-frame but interior is empty — rule's "fill with seed
        # color" has no color to use.
        for c in range(2, 9): g[2][c] = 5; g[6][c] = 5
        for r in range(2, 7): g[r][2] = 5; g[r][8] = 5
        return g
    if name == "multi_seeds":
        # 5-frame with multiple distinct seed colors inside — rule's
        # "exactly one seed" precondition fails; flood color ambiguous.
        for c in range(2, 9): g[2][c] = 5; g[6][c] = 5
        for r in range(2, 7): g[r][2] = 5; g[r][8] = 5
        g[3][4] = 3; g[5][7] = 6
        return g
    return g
