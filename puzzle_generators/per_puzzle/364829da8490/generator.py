"""Generator for arc_puzzle_bank_21_set19_bundle:medium_p07 — fill enclosed holes.

Rule: for every 0-region that is enclosed (does NOT touch the border)
and bordered by exactly one color, fill the region with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, frame_open, frame_at_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "364829da8490"
VERSION = "1.1.0"
TASK_ID = "364829da8490"
SUMMARY = "1-2 closed rect outlines (different colors) with hollow interiors."

INVARIANTS = [
    "background is 0",
    "every frame is a single color, fully closed (no holes in the wall)",
    "frame interiors are 0 and don't touch the grid border",
    "different frames don't 4-touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "frame_open", "frame_at_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_closed_frames",
                       "valid": "scattered_closed_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _frame_free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 1 or c1 < 1 or r2 >= h - 1 or c2 >= w - 1:
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            fh = rng.randint(4, 5)
            fw = rng.randint(4, 5)
            r1 = rng.randint(1, h - fh - 1)
            c1 = rng.randint(1, w - fw - 1)
            r2 = r1 + fh - 1
            c2 = c1 + fw - 1
            if not _frame_free(g, r1, c1, r2, c2):
                continue
            for c in range(c1, c2 + 1):
                g[r1][c] = color; g[r2][c] = color
            for r in range(r1, r2 + 1):
                g[r][c1] = color; g[r][c2] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Empty grid — rule has no enclosed regions to fill.
        return g
    if name == "frame_open":
        # Frame is broken (one wall cell missing) — region leaks to
        # border, not enclosed; rule's fill condition fails.
        for c in range(2, 9): g[2][c] = 4; g[7][c] = 4
        for r in range(2, 8): g[r][2] = 4
        for r in range(2, 8):
            if r != 5: g[r][8] = 4
        return g
    if name == "frame_at_border":
        # Frame uses the grid border as one of its walls — the
        # interior 0-region touches the border via the missing
        # outer wall path; rule's "enclosed" condition fails.
        for c in range(0, 7): g[0][c] = 4; g[5][c] = 4
        for r in range(0, 6): g[r][0] = 4; g[r][6] = 4
        return g
    return g
