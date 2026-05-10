"""Generator for arc_puzzle_bank_21_set3:S3_M2 — frame cross from inner dot.

Rule: each frame contains exactly one red dot strictly inside it. The
output draws a cross through that dot up to the frame walls.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_dot, dot_on_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "1594f141732b"
VERSION = "1.1.0"
TASK_ID = "1594f141732b"

SUMMARY = "One or two rectangular frames, each with a red dot well inside the frame."

INVARIANTS = [
    "background is 0",
    "each non-red frame is an exact rectangular outline",
    "each frame contains exactly one singleton red dot strictly inside it",
    "the red dot is separated from the frame border by at least one blank cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_dot", "dot_on_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "grid_w":         {"type": "int", "default": "rng 15..19", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "frame_with_inner_dot",
                       "valid": "frame_with_inner_dot"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r1, c1, r2, c2) -> bool:
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
        h = ctx.draw_int("grid_h", 14, 14)
        w = ctx.draw_int("grid_w", 15, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 17, 19)
        w = ctx.draw_int("grid_w", 19, 21)
    else:
        h = ctx.draw_int("grid_h", 14, 17)
        w = ctx.draw_int("grid_w", 15, 19)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 3, 4, 5, 6, 7, 8, 9], rng.randint(1, 2))

    for color in colors:
        placed = False
        for _ in range(80):
            rh = rng.randint(7, min(9, h - 2))
            rw = rng.randint(7, min(10, w - 2))
            r1 = rng.randint(1, h - rh - 1)
            c1 = rng.randint(1, w - rw - 1)
            r2 = r1 + rh - 1
            c2 = c1 + rw - 1
            if not _clear(g, r1, c1, r2, c2):
                continue
            draw_frame(g, r1, c1, r2, c2, color)
            g[rng.randint(r1 + 2, r2 - 2)][rng.randint(c1 + 2, c2 - 2)] = 2
            placed = True
            break
        if not placed:
            raise ValueError("could not place a separated frame")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 15
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # Red dots but no frame — rule has no boundary to draw cross
        # through; cross extent is undefined.
        g[5][7] = 2
        return g
    if name == "no_dot":
        # Frame but no inner dot — rule has no cross center.
        draw_frame(g, 2, 2, 8, 12, 4)
        return g
    if name == "dot_on_frame":
        # Frame + red dot but the dot is ON the frame wall (not strictly
        # inside) — rule's "inside the frame" precondition fails.
        draw_frame(g, 2, 2, 8, 12, 4)
        g[2][7] = 2
        return g
    return g
