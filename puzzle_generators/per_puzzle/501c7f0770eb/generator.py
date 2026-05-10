"""Generator for 5b:hard_29 — local rays in chambers.

Rule: each rectangular 5-frame is a chamber. Inside the chamber,
color-1 cells emit vertical rays (color 7), color-2 cells emit
horizontal rays. Rays stop at any color-4 or color-5 cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_chambers (no color-5 frames → rule has no chambers
to fire rays in); no_seeds (chambers but no color-1/2 seeds → no
rays emitted); only_one_seed_color (chambers with only color-1 OR
only color-2 → only one ray direction is exercised).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "501c7f0770eb"
VERSION = "1.1.0"
TASK_ID = "501c7f0770eb"

SUMMARY = "1-2 hollow 5-frames + 1-2 color-1 + 1-2 color-2 seeds inside each."

INVARIANTS = [
    "background is 0",
    "1-2 hollow 5-rectangular frames",
    "each frame's interior holds 1-2 color-1 seeds and 1-2 color-2 seeds",
    "no seed sits adjacent to another seed (so rays start cleanly)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_chambers", "no_seeds", "only_one_seed_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 12..14", "valid": "11..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "frames_with_seeds_inside",
                          "valid": "frames_with_seeds_inside"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_frames = rng.randint(1, 2)
    placed_frames = []
    for _ in range(n_frames):
        for _ in range(40):
            fh = rng.randint(5, 6); fw = rng.randint(5, 6)
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            for c in range(c0, c0 + fw): g[r0][c] = 5; g[r0 + fh - 1][c] = 5
            for r in range(r0, r0 + fh): g[r][c0] = 5; g[r][c0 + fw - 1] = 5
            placed_frames.append((r0, c0, fh, fw))
            break
    for r0, c0, fh, fw in placed_frames:
        for color, n in ((1, rng.randint(1, 2)), (2, rng.randint(1, 2))):
            placed = 0; attempts = 0
            while placed < n and attempts < 40:
                attempts += 1
                r = rng.randint(r0 + 1, r0 + fh - 2)
                c = rng.randint(c0 + 1, c0 + fw - 2)
                if g[r][c] != 0 or _too_close(g, r, c): continue
                g[r][c] = color
                placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_chambers":
        # No 5-frames — rule has no chambers.
        g[3][4] = 1; g[5][8] = 2
        return g
    if name == "no_seeds":
        # Frames but no seeds — no rays emitted.
        for c in range(2, 7): g[2][c] = 5; g[7][c] = 5
        for r in range(2, 8): g[r][2] = 5; g[r][6] = 5
        return g
    if name == "only_one_seed_color":
        # Frame with only color-1 seeds — only vertical rays exercised.
        for c in range(2, 7): g[2][c] = 5; g[7][c] = 5
        for r in range(2, 8): g[r][2] = 5; g[r][6] = 5
        g[4][4] = 1; g[6][5] = 1
        return g
    return g
