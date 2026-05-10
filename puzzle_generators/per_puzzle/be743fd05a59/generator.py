"""Generator for arc_puzzle_bank_21_set3:S3_E6.

Rule: each maroon cell casts a gray echo one cell down-left if that target is empty.

Combinatorial axes (8): grid_h, grid_w, palette_kind, source_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_sources, sources_at_bl, sources_clustered.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "be743fd05a59"
VERSION = "1.1.0"
TASK_ID = "be743fd05a59"
SUMMARY = "Each maroon cell casts a gray echo one cell down-left if that target is empty."

INVARIANTS = [
    "background is 0",
    "maroon source cells are isolated",
    "down-left echo targets are inside the grid for most sources",
    "occupied echo targets block painting",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_sources", "sources_at_bl", "sources_clustered")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "source_count":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_avoid_bl",
                       "valid": "scattered_avoid_bl"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("source_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        count = ctx.draw_int("source_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        count = ctx.draw_int("source_count", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = []
    for _ in range(count):
        for _attempt in range(200):
            r = rng.randint(0, h - 2)
            c = rng.randint(1, w - 1)
            if g[r][c] == 0 and all(abs(r - rr) + abs(c - cc) >= 3 for rr, cc in placed):
                g[r][c] = 9
                placed.append((r, c))
                if rng.random() < 0.25:
                    g[r + 1][c - 1] = rng.choice([1, 4])
                break
        else:
            raise ValueError("could not place maroon source")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_sources":
        # no maroon cells → no echoes, rule no-op
        return g
    if name == "sources_at_bl":
        # maroon cells on bottom row or left column → down-left is out of bounds, rule no-op
        for c in [2, 4, 7]:
            g[h - 1][c] = 9
        for r in [2, 5]:
            g[r][0] = 9
        return g
    if name == "sources_clustered":
        # adjacent maroon cells → "isolated source" invariant violated, ambiguous component count
        for r, c in [(2, 4), (2, 5), (3, 4), (3, 5)]:
            g[r][c] = 9
        return g
    return g
