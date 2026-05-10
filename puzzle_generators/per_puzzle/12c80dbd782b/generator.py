"""Generator for v3_rich_schema:easy_02_frame_2x2_blocks — outline 2x2 color-3 blocks.

Rule: each 2x2 solid color-3 block has its surrounding ring (1 cell
out) filled with color 5 in the bg cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blocks, wrong_shape, wrong_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "12c80dbd782b"
VERSION = "1.1.0"
TASK_ID = "12c80dbd782b"

SUMMARY = "1-2 solid 2x2 color-3 blocks with bg margin around them."

INVARIANTS = [
    "background is 0",
    "1-2 disjoint 2x2 solid color-3 blocks with at least 1 cell of bg margin around each",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blocks", "wrong_shape", "wrong_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n":              {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1 (color 3)", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered_2x2_with_margin",
                       "valid": "scattered_2x2_with_margin"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 2), min(h, r2 + 3)):
        for c in range(max(0, c1 - 2), min(w, c2 + 3)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        n = ctx.draw_int("n", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for _ in range(n):
            placed = False
            for _ in range(80):
                r = rng.randint(1, h - 3); c = rng.randint(1, w - 3)
                if not _free(g, r, c, r + 1, c + 1): continue
                for dr in range(2):
                    for dc in range(2):
                        g[r + dr][c + dc] = 3
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_blocks":
        # Empty grid — rule has no 2x2 to ring.
        return g
    if name == "wrong_shape":
        # 1x4 line and 3x3 square — neither is a 2x2 block, so the
        # rule's match never fires.
        for dc in range(4):
            g[2][1 + dc] = 3
        for dr in range(3):
            for dc in range(3):
                g[4 + dr][3 + dc] = 3
        return g
    if name == "wrong_color":
        # 2x2 block but in color 5 (not 3) — the rule's color-3 filter
        # doesn't match it.
        for dr in range(2):
            for dc in range(2):
                g[2 + dr][2 + dc] = 5
        return g
    return g
