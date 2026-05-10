"""Generator for arc_puzzle_bank_21_set9_e:medium_i14 — fill enclosed holes with frame color.

Rule: for each blob, fill its bbox-interior 0-cells with that blob's
color. Solid blobs unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, all_solid, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "56f043832ecb"
VERSION = "1.1.0"
TASK_ID = "56f043832ecb"
SUMMARY = "1-2 closed rect-frames in distinct colors, each with hollow interior."

INVARIANTS = [
    "background is 0",
    "≥1 closed rect-frame ≥3×3 with bbox-interior 0-cell",
    "frames don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "all_solid", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_frames",
                       "valid": "scattered_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
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
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Empty grid — no frame to fill.
        return g
    if name == "all_solid":
        # Solid filled blobs (no hollow bbox-interior) — rule is a no-op.
        for r in range(1, 4):
            for c in range(1, 4):
                g[r][c] = 4
        for r in range(1, 4):
            for c in range(6, 9):
                g[r][c] = 6
        return g
    if name == "single_frame":
        # Just one frame — minimal context.
        for c in range(1, 5):
            g[1][c] = 5; g[4][c] = 5
        for r in range(1, 5):
            g[r][1] = 5; g[r][4] = 5
        return g
    return g
