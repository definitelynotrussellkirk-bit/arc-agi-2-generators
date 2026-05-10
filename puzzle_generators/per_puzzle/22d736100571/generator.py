"""Generator for arc_additional_puzzle_bank_volume20:E135.

Red line spans with exactly one missing cell have that gap filled red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_spans,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_spans, no_gap, multiple_gaps.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22d736100571"
VERSION = "1.1.0"
TASK_ID = "22d736100571"
SUMMARY = "Red line spans with exactly one missing cell have that gap filled red."

INVARIANTS = [
    "background is 0",
    "each active row contains one red span with exactly one zero gap",
    "span endpoints and other cells in the span are red",
    "active rows use distinct columns to avoid accidental vertical spans",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_spans", "no_gap", "multiple_gaps")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_spans":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "rows_with_one_gap",
                       "valid": "rows_with_one_gap"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_spans = ctx.draw_int("n_spans", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        n_spans = ctx.draw_int("n_spans", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 14)
        n_spans = ctx.draw_int("n_spans", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), min(n_spans, h))
    used_cols: set[int] = set()
    for r in rows:
        length = rng.randint(4, min(6, w))
        starts = [c for c in range(w - length + 1) if all((c + i) not in used_cols for i in range(length))]
        if not starts:
            continue
        c0 = rng.choice(starts)
        gap = rng.randint(1, length - 2)
        for dc in range(length):
            if dc != gap:
                g[r][c0 + dc] = 2
        used_cols.update(range(c0, c0 + length))
    if not used_cols:
        g[1][1] = 2
        g[1][2] = 2
        g[1][4] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_spans":
        # blank → no spans with gaps to fill
        return g
    if name == "no_gap":
        # solid red span (no gap) → no missing cell, rule is identity
        for c in range(2, 7): g[3][c] = 2
        return g
    if name == "multiple_gaps":
        # span with 2 gaps → "exactly one" precondition fails
        for c in [2, 4, 7]: g[3][c] = 2  # gaps at 3, 5, 6
        return g
    return g
