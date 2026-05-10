"""Generator for arc_puzzle_bank_21_set24_bundle:medium_p04 — fill frame interior by side-seed.

Rule: 1-2 hollow color-5 frames. Each frame has a colored seed at its
vertical midpoint, just left of c0 (or just right of c1 if left is empty).
The seed's color fills the frame's interior.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-5 frames → rule has nothing to fill),
no_seeds (frames present but no side-seeds → rule's fill-color is
undefined), seed_at_both_sides (frame has seeds on both sides → rule's
"left or right" tie-break decides which color fills).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "4b326abc33f4"
VERSION = "1.1.0"
TASK_ID = "4b326abc33f4"

SUMMARY = "1-2 color-5 frames + a colored seed cell adjacent to each frame's left or right side at mid-height."

INVARIANTS = [
    "background is 0",
    "1-2 hollow color-5 frames at distinct positions",
    "each frame has a single colored seed cell adjacent to its left or right edge at the vertical midpoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_seeds", "seed_at_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "n_frames":          {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "frames_with_side_seeds",
                          "valid": "frames_with_side_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 14, 15)
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 16, 17)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 14, 17)
        n_frames = ctx.draw_int("n_frames", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for i in range(n_frames):
            fh = rng.choice([5, 6])
            fw = rng.choice([5, 6])
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - fh); c0 = rng.randint(2, w - fw - 1)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 5)
                mid_r = (r0 + r0 + fh - 1) // 2
                use_left = rng.choice([True, False])
                if use_left and c0 - 1 >= 0 and g[mid_r][c0 - 1] == 0:
                    g[mid_r][c0 - 1] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
                elif c0 + fw <= w - 1 and g[mid_r][c0 + fw] == 0:
                    g[mid_r][c0 + fw] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
                else:
                    continue
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize set24 medium_p04 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 16
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No color-5 frames — rule has nothing to fill.
        g[3][3] = 4
        g[6][9] = 6
        return g
    if name == "no_seeds":
        # Frames present but no side-seeds.
        draw_frame(g, 1, 3, 5, 7, 5)
        draw_frame(g, 4, 9, 8, 13, 5)
        return g
    if name == "seed_at_both_sides":
        # Frame has seeds on both sides — tie-break decides fill color.
        draw_frame(g, 2, 5, 6, 9, 5)
        g[4][4] = 4   # left seed
        g[4][10] = 6  # right seed
        return g
    return g
