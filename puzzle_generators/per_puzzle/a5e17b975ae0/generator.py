"""Generator for 11b:hard_74 — fill keyed chambers inside frames.

Rule: walls are color 5 or 9. Any other non-bg cell is a seed. From
each seed, BFS through 0-cells (blocked by 5/9), painting all reached
cells with the seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_seeds, no_chamber_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a5e17b975ae0"
VERSION = "1.1.0"
TASK_ID = "a5e17b975ae0"

SUMMARY = "1-2 hollow 9-frames; each interior holds 1-2 seed cells (non-{0,5,9} colors)."

INVARIANTS = [
    "background is 0",
    "1-2 hollow 9-rectangular frames (walls)",
    "each frame's interior holds 1-2 seed cells in non-{0,5,9} colors",
    "seeds are isolated (no 4-neighbor non-bg)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_seeds", "no_chamber_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "frames_with_seeds_inside",
                       "valid": "frames_with_seeds_inside"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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


def _too_close(g, r, c) -> bool:
    h, w = len(g), len(g[0])
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 15, 19)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 13, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_frames = rng.randint(1, 2)
    frames = []
    for _ in range(n_frames):
        for _ in range(40):
            fh = rng.randint(5, 7); fw = rng.randint(5, 7)
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            frames.append((r0, c0, fh, fw))
            break
    for r0, c0, fh, fw in frames:
        n_seeds = rng.randint(1, 2)
        seed_palette = rng.sample([1, 2, 3, 4, 6, 7, 8], n_seeds)
        for color in seed_palette:
            for _ in range(40):
                r = rng.randint(r0 + 1, r0 + fh - 2)
                c = rng.randint(c0 + 1, c0 + fw - 2)
                if g[r][c] != 0 or _too_close(g, r, c): continue
                g[r][c] = color; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No 9-frames — rule has no chambers (BFS spreads to whole grid).
        g[3][3] = 4; g[6][8] = 5
        return g
    if name == "no_seeds":
        # Frames present but no seeds — rule has nothing to flood.
        for c in range(2, 8): g[2][c] = 9; g[7][c] = 9
        for r in range(2, 8): g[r][2] = 9; g[r][7] = 9
        return g
    if name == "no_chamber_room":
        # Frame is 3x3 — interior is a single cell, BFS region is trivial.
        for c in range(2, 5): g[2][c] = 9; g[4][c] = 9
        for r in range(2, 5): g[r][2] = 9; g[r][4] = 9
        g[3][3] = 4
        return g
    return g
