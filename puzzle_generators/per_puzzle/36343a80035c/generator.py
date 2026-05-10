"""Generator for arc_puzzle_bank_21_set5_e:medium_e03 — output enclosed holes.

Rule: each blob has bbox-interior 0-cells fully enclosed. Output: 8s
at every such enclosed-hole cell, in an otherwise empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, all_solid, frame_open.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "36343a80035c"
VERSION = "1.1.0"
TASK_ID = "36343a80035c"
SUMMARY = "1-2 closed rect-frames in distinct colors, each with an interior hole."

INVARIANTS = [
    "background is 0",
    "≥1 closed rect-frame ≥3×3 with at least one bbox-interior 0-cell",
    "frames don't 4-touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "all_solid", "frame_open")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "= n_frames", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_frames",
                       "valid": "scattered_frames"},
    "n_distinct_colors": {"type": "int", "default": "= n_frames", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            fh = rng.randint(3, 4); fw = rng.randint(3, 4)
            r1 = rng.randint(0, h - fh)
            c1 = rng.randint(0, w - fw)
            r2 = r1 + fh - 1; c2 = c1 + fw - 1
            if _free(g, r1, c1, r2, c2):
                for c in range(c1, c2 + 1):
                    g[r1][c] = color; g[r2][c] = color
                for r in range(r1, r2 + 1):
                    g[r][c1] = color; g[r][c2] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Empty grid — no enclosed hole to extract.
        return g
    if name == "all_solid":
        # Solid blobs — no interior 0-cells, output should be all-zero.
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 4
        return g
    if name == "frame_open":
        # Frame missing a wall cell — interior reaches background, so
        # there's no enclosed hole to output.
        for c in range(2, 6):
            g[1][c] = 4; g[5][c] = 4
        for r in range(1, 6):
            g[r][2] = 4; g[r][5] = 4
        g[3][2] = 0
        return g
    return g
