"""Generator for arc_additional_puzzle_bank_volume18:E120 — odd-length blue middle recolor.

Rule: odd-length blue segments have only their middle cell recolored
red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_segments,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_segments, even_length, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bedf1922195c"
VERSION = "1.1.0"
TASK_ID = "bedf1922195c"
SUMMARY = "Odd-length blue segments have only their middle cell recolored red."

INVARIANTS = [
    "background is 0",
    "blue components are straight odd-length segments",
    "segments have length at least three",
    "segments are separated so components do not merge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_segments", "even_length", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_segments":     {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1 (blue)", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "axis_aligned_odd_length",
                       "valid": "axis_aligned_odd_length"},
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
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        n_segments = ctx.draw_int("n_segments", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 13, 18)
        n_segments = ctx.draw_int("n_segments", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_segments = ctx.draw_int("n_segments", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    horizontal = rng.choice([False, True])
    used: set[int] = set()
    made = 0
    for _ in range(200):
        if made >= n_segments:
            break
        length = rng.choice([3, 5])
        if horizontal:
            choices = [r for r in range(h) if all(abs(r - rr) > 1 for rr in used)]
            if not choices:
                break
            r = rng.choice(choices)
            c = rng.randint(0, w - length)
            for dc in range(length):
                g[r][c + dc] = 1
            used.add(r)
        else:
            choices = [c for c in range(w) if all(abs(c - cc) > 1 for cc in used)]
            if not choices:
                break
            c = rng.choice(choices)
            r = rng.randint(0, h - length)
            for dr in range(length):
                g[r + dr][c] = 1
            used.add(c)
        made += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_segments":
        # Empty grid — no blue segment to recolor.
        return g
    if name == "even_length":
        # Blue segments of length 2 and 4 — no integer middle cell,
        # so the rule's middle-recolor never fires.
        for dc in range(2):
            g[1][1 + dc] = 1
        for dc in range(4):
            g[5][2 + dc] = 1
        for dr in range(4):
            g[3 + dr][8] = 1
        return g
    if name == "single_cell":
        # Length-1 segments — too short for the rule's length-3+ filter,
        # no middle cell to recolor.
        g[1][1] = 1; g[3][5] = 1; g[7][2] = 1
        return g
    return g
