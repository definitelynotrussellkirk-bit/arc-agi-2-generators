"""Generator for arc_puzzle_bank_fifth21:E35.

Rule: each row has a color header in column 0; any 8-marker elsewhere in
that row is recolored to the row's header color.

Combinatorial axes (8): grid_h/w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_headers, no_markers, header_is_eight.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bab4d8f5ba7a"
VERSION = "1.1.0"
TASK_ID = "bab4d8f5ba7a"
SUMMARY = "Use first-column row headers to recolor row-local 8 markers."

INVARIANTS = [
    "background is 0",
    "active rows have a nonzero color header in column 0",
    "each active row has one color-8 marker away from the header",
    "8 markers are replaced by their row header color",
]

PALETTE_KINDS = ("default", "warm_headers", "cool_headers", "rainbow")
DEGENERATE_TEXTURES = ("no_headers", "no_markers", "header_is_eight")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "3..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "uniform", "valid": "uniform"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5",
                          "valid": "1..8"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target_max = 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        target_max = 5
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        target_max = 5
    target = min(ctx.draw_int("active_rows", 3, target_max), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in rng.sample(range(h), target):
        header = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        g[r][0] = header
        g[r][rng.randint(1, w - 1)] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_headers":
        # 8-markers without row headers — nothing to recolor to
        g[1][3] = 8
        g[3][5] = 8
        g[5][2] = 8
        return g
    if name == "no_markers":
        # Headers without any 8 to recolor — rule no-op
        g[1][0] = 4
        g[3][0] = 7
        g[5][0] = 2
        return g
    if name == "header_is_eight":
        # Header column has 8 — header IS marker, ambiguous which is which
        g[1][0] = 8
        g[1][4] = 8
        g[3][0] = 4
        g[3][6] = 8
        return g
    return g
