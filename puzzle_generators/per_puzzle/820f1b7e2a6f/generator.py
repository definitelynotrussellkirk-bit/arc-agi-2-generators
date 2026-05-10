"""Generator for arc_additional_puzzle_bank_volume16:E110 — diagonal magenta endpoints recolor.

Rule: each diagonal magenta segment has its two endpoints recolored
blue.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_segments,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_segments, axis_aligned, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "820f1b7e2a6f"
VERSION = "1.1.0"
TASK_ID = "820f1b7e2a6f"
SUMMARY = "Endpoints of 8-connected diagonal magenta segments are recolored blue."

INVARIANTS = [
    "background is 0",
    "magenta components are diagonal line segments",
    "diagonal segments have length at least three",
    "segments are separated so 8-connected components do not merge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_segments", "axis_aligned", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_segments":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1 (magenta)", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "diagonal_segments",
                       "valid": "diagonal_segments"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_segments = ctx.draw_int("n_segments", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 18)
        w = ctx.draw_int("grid_w", 14, 18)
        n_segments = ctx.draw_int("n_segments", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 9, 14)
        n_segments = ctx.draw_int("n_segments", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    occupied: set[tuple[int, int]] = set()
    for _ in range(240):
        if len(occupied) >= n_segments * 3:
            break
        length = rng.randint(3, min(5, h, w))
        slope = rng.choice([-1, 1])
        r0 = rng.randint(1, h - length - 1)
        c0 = rng.randint(length, w - 2) if slope == -1 else rng.randint(1, w - length - 1)
        cells = [(r0 + i, c0 + slope * i) for i in range(length)]
        if any(abs(r - rr) <= 1 and abs(c - cc) <= 1 for r, c in cells for rr, cc in occupied):
            continue
        for cell in cells:
            occupied.add(cell)
            g[cell[0]][cell[1]] = 6
        if sum(1 for _, _, v in [(r, c, g[r][c]) for r in range(h) for c in range(w)] if v == 6) >= n_segments * 3:
            break
    if not occupied:
        for i in range(3):
            g[1 + i][1 + i] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_segments":
        # Empty grid — no diagonal magenta to recolor.
        return g
    if name == "axis_aligned":
        # Horizontal and vertical magenta segments — neither is a
        # diagonal, so the rule's diagonal-segment match never fires.
        for dc in range(4):
            g[2][2 + dc] = 6
        for dr in range(4):
            g[5 + dr][7] = 6
        return g
    if name == "single_cell":
        # Single magenta cells (length 1) — too short for the rule's
        # length-3+ filter, no endpoints to identify.
        g[2][2] = 6; g[5][7] = 6; g[8][3] = 6
        return g
    return g
