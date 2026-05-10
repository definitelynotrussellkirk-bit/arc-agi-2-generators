"""Generator for arc_additional_puzzle_bank_volume17:E115 — connect red endpoints with cyan.

Rule: aligned red marker pairs with clear interiors are connected by
cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, single_endpoint_per_row, span_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "00ed2544a15e"
VERSION = "1.1.0"
TASK_ID = "00ed2544a15e"
SUMMARY = "Aligned red marker pairs with clear interiors are connected by cyan."

INVARIANTS = [
    "background is 0",
    "active rows contain exactly two red markers",
    "interiors between paired markers are empty",
    "red endpoint columns are unique across rows to avoid extra vertical pairs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "single_endpoint_per_row", "span_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "row_endpoint_pairs",
                       "valid": "row_endpoint_pairs"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n_pairs = ctx.draw_int("n_pairs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 8, 14)
        n_pairs = ctx.draw_int("n_pairs", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), min(n_pairs, h))
    used_cols: set[int] = set()
    for r in rows:
        choices = [c for c in range(w) if c not in used_cols]
        if len(choices) < 2:
            break
        c1, c2 = sorted(rng.sample(choices, 2))
        if c2 - c1 < 2:
            continue
        g[r][c1] = 2
        g[r][c2] = 2
        used_cols.update((c1, c2))
    if not used_cols:
        g[1][1] = 2
        g[1][4] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # blank → no red endpoints to bridge
        return g
    if name == "single_endpoint_per_row":
        # rows have 1 red cell → can't define an endpoint pair
        g[1][2] = 2
        g[3][5] = 2
        g[5][8] = 2
        return g
    if name == "span_already_filled":
        # endpoints + everything between already painted → rule has nothing
        for c in range(1, 7): g[1][c] = 2
        for c in range(2, 6): g[3][c] = 2
        return g
    return g
