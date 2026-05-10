"""Generator for arc_puzzle_bank_thirteenth21:E86.

Rule: blank cells with all four cardinal arms of the same color are filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pluses,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, partial_arms, mismatched_arms.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f9dd4cf0f344"
VERSION = "1.1.0"
TASK_ID = "f9dd4cf0f344"

SUMMARY = "Four same-color cardinal arms around a zero center fill that center."

INVARIANTS = [
    "background is 0",
    "plus centers are zero in the input",
    "all four cardinal neighbors around a center share one nonzero color",
    "plus patterns are spaced apart",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pluses", "partial_arms", "mismatched_arms")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pluses":         {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_pluses",
                       "valid": "spaced_pluses"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far(center, centers):
    r, c = center
    return all(abs(r - rr) + abs(c - cc) >= 4 for rr, cc in centers)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("pluses", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("pluses", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pluses", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    centers = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(centers)
    used = []
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(9, target))
    for r, c in centers:
        if len(used) >= target:
            break
        if not _far((r, c), used):
            continue
        color = colors[len(used) % len(colors)]
        used.append((r, c))
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            g[r + dr][c + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # blank → no plus centers, rule has no effect
        return g
    if name == "partial_arms":
        # only 3 of 4 cardinal arms → predicate "all 4 same color" fails
        g[1][3] = 4; g[2][2] = 4; g[2][4] = 4  # missing bottom arm
        g[5][6] = 6; g[5][8] = 6; g[6][7] = 6  # missing top arm (bottom row)
        return g
    if name == "mismatched_arms":
        # all 4 arms present but in different colors → predicate fails
        g[1][3] = 4; g[3][3] = 6; g[2][2] = 3; g[2][4] = 8
        return g
    return g
