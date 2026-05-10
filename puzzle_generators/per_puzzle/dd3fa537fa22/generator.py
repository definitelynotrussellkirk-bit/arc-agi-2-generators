"""Generator for arc_puzzle_bank_21_set11_bundle:hard_k15 — match frame interior to filled insert.

Rule: hollow color-8 rectangular frames + solid filled rectangles in other colors.
For each frame, find the filled insert whose bbox matches the interior dims;
fill the frame's interior with the insert's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no color-8 frames → rule has nothing to
fill); no_inserts (frames present but no solid inserts → rule's
matcher returns nothing); tied_sizes (two frames have the same
interior dims, two inserts share the same dims → matcher
ambiguous, color choice undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "dd3fa537fa22"
VERSION = "1.1.0"
TASK_ID = "dd3fa537fa22"

SUMMARY = "2 hollow 8-frames with distinct interior sizes + 2 solid-rect inserts whose bboxes match."

INVARIANTS = [
    "background is 0",
    "exactly 2 hollow color-8 rectangular frames with distinct interior dims",
    "exactly 2 solid-filled rectangles in non-{0, 8} colors, each whose bbox matches a frame's interior",
    "frames + inserts are 4-conn isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_inserts", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":            {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "frames_plus_inserts",
                          "valid": "frames_plus_inserts"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 14, 17)
    rng = ctx.draw_rng("layout")

    sizes = rng.sample([(2, 2), (2, 3), (3, 2), (3, 3), (2, 4), (4, 2)], 2)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 2)

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for ih, iw in sizes:
            fh, fw = ih + 2, iw + 2
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1):
                    continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, 8)
                placed = True
                break
            if not placed:
                ok = False; break
        if not ok:
            continue
        for (ih, iw), color in zip(sizes, colors):
            placed = False
            for _ in range(120):
                r0 = rng.randint(0, h - ih); c0 = rng.randint(0, w - iw)
                if not _free(g, r0, c0, r0 + ih - 1, c0 + iw - 1):
                    continue
                for r in range(ih):
                    for c in range(iw):
                        g[r0 + r][c0 + c] = color
                placed = True
                break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize hard_k15 layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No color-8 frames — rule has no interiors to fill.
        for r in range(2):
            for c in range(2):
                g[3 + r][3 + c] = 1
        for r in range(3):
            for c in range(3):
                g[7 + r][9 + c] = 2
        return g
    if name == "no_inserts":
        # Frames present, but no solid inserts to read color from.
        draw_frame(g, 1, 1, 4, 4, 8)
        draw_frame(g, 7, 8, 11, 13, 8)
        return g
    if name == "tied_sizes":
        # Two frames with same interior dims (3x3) + two inserts with same dims.
        # Matcher cannot decide which insert goes with which frame.
        draw_frame(g, 1, 1, 4, 4, 8)        # interior 2x2
        draw_frame(g, 1, 8, 4, 11, 8)        # interior 2x2 (same)
        for r in range(2):
            for c in range(2):
                g[7 + r][1 + c] = 1
        for r in range(2):
            for c in range(2):
                g[7 + r][8 + c] = 2
        return g
    return g
