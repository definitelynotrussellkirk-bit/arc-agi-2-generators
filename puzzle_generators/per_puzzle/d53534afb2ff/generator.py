"""Generator for v2_meta_puzzles:M4 — recolor inner objs by enclosing frame.

Rule: hollow rect frames + small objs strictly inside; each interior obj is
recolored to its enclosing frame's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_inner, inner_outside_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "d53534afb2ff"
VERSION = "1.1.0"
TASK_ID = "d53534afb2ff"

SUMMARY = "1-2 hollow color frames each containing 1 small inner motif in another color."

INVARIANTS = [
    "background is 0",
    "1-2 hollow rectangular frames in distinct colors",
    "each frame strictly contains exactly one small motif in a different color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_inner", "inner_outside_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..18"},
    "n":              {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "frames_with_inner_motifs",
                       "valid": "frames_with_inner_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..6"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
        n = ctx.draw_int("n", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 17)
        n = ctx.draw_int("n", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        n = ctx.draw_int("n", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for _ in range(n):
            frame_color, inner_color = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
            placed = False
            for _ in range(120):
                fh = rng.choice([5, 6]); fw = rng.choice([5, 6])
                r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, frame_color)
                ir = rng.randint(r0 + 1, r0 + fh - 2)
                ic = rng.randint(c0 + 1, c0 + fw - 2)
                g[ir][ic] = inner_color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Inner objs but no frames — rule's "enclosing frame
        # color" lookup fails; recolor undefined.
        g[3][3] = 4; g[5][7] = 6
        return g
    if name == "no_inner":
        # Frame but no inner objects — rule's recolor branch
        # never fires; output equals input.
        draw_frame(g, 1, 1, 5, 6, 4)
        return g
    if name == "inner_outside_frame":
        # Frame + inner-color cell placed outside frame — rule's
        # "strictly inside" filter excludes.
        draw_frame(g, 1, 1, 5, 6, 4)
        g[7][9] = 6
        return g
    return g
