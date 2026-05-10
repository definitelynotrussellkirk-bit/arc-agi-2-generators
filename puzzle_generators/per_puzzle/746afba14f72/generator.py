"""Generator for arc_puzzle_bank_seventeenth21:E117.

Rule: blank cells with all four cardinal neighbors of the same color get filled
with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cavities,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cavities, partial_arms, mismatched_arms.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "746afba14f72"
VERSION = "1.1.0"
TASK_ID = "746afba14f72"

SUMMARY = "Same-color cardinal neighbors surround blank cavity centers."

INVARIANTS = [
    "background is 0",
    "each active center is 0",
    "the four cardinal neighbors share one nonzero color",
    "motifs are separated to avoid accidental cavities",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cavities", "partial_arms", "mismatched_arms")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cavities":       {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_cardinal_arms",
                       "valid": "spaced_cardinal_arms"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_ARMS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("cavities", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("cavities", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("cavities", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        cells = {(r, c)} | {(r + dr, c + dc) for dr, dc in _ARMS}
        guard = {
            (rr, cc)
            for cr, cc0 in cells
            for rr in range(max(0, cr - 1), min(h, cr + 2))
            for cc in range(max(0, cc0 - 1), min(w, cc0 + 2))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for dr, dc in _ARMS:
            g[r + dr][c + dc] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_cavities":
        # blank → no cavity to fill, rule has no effect
        return g
    if name == "partial_arms":
        # only 3 of 4 cardinal arms present → predicate fails
        # cavity at (2,3) — top, left, right arms but missing bottom
        g[1][3] = 4; g[2][2] = 4; g[2][4] = 4
        return g
    if name == "mismatched_arms":
        # all 4 arms present but in different colors → predicate "all 4 same color" fails
        g[1][3] = 4; g[3][3] = 6; g[2][2] = 3; g[2][4] = 8
        return g
    return g
