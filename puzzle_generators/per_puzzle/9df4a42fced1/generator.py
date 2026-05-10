"""Generator for arc_puzzle_bank_21_set17_bundle:medium_p06 — frame center label.

Rule: each rect-frame containing exactly one seed inside → output
single dot at frame's bbox center, in the seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_seeds, multi_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9df4a42fced1"
VERSION = "1.1.0"
TASK_ID = "9df4a42fced1"
SUMMARY = "1-2 rect-frames in distinct colors, each with one differently-colored seed inside."

INVARIANTS = [
    "background is 0",
    "≥1 rect-frame ≥5×5 with exactly one non-frame seed inside",
    "frames don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_seeds", "multi_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "non_overlapping_frames",
                       "valid": "non_overlapping_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2 * n)
    for i in range(n):
        for _ in range(40):
            fh = 5; fw = 5
            r1 = rng.randint(0, h - fh)
            c1 = rng.randint(0, w - fw)
            r2 = r1 + fh - 1; c2 = c1 + fw - 1
            if _free(g, r1, c1, r2, c2):
                fc = palette[2 * i]
                sc = palette[2 * i + 1]
                for c in range(c1, c2 + 1):
                    g[r1][c] = fc; g[r2][c] = fc
                for r in range(r1, r2 + 1):
                    g[r][c1] = fc; g[r][c2] = fc
                interior = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
                sr, sk = rng.choice(interior)
                g[sr][sk] = sc
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Loose seeds, no frames — rule has no center to label.
        g[3][4] = 5; g[6][8] = 6
        return g
    if name == "no_seeds":
        # Frame present but interior empty — rule has no seed color to use.
        for c in range(2, 7): g[2][c] = 4; g[6][c] = 4
        for r in range(2, 7): g[r][2] = 4; g[r][6] = 4
        return g
    if name == "multi_seeds":
        # Frame interior has 2 seeds — "the seed" is ambiguous.
        for c in range(2, 7): g[2][c] = 4; g[6][c] = 4
        for r in range(2, 7): g[r][2] = 4; g[r][6] = 4
        g[3][3] = 5; g[5][5] = 6
        return g
    return g
