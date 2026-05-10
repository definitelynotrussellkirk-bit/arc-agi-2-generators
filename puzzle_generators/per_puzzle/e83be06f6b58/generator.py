"""Generator for puzzle 9968a131.

Rule: bg=7. Rows whose visible run starts with the larger color shift
right one cell; smaller-value rows stay fixed.

Combinatorial axes (8): row_count, grid_w, palette_kind, run_min,
run_max, start_min, start_max, anchor_corner.
Degenerates: empty_rows, all_same_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e83be06f6b58"
VERSION = "1.1.0"
TASK_ID = "e83be06f6b58"
SUMMARY = "bg=7 rows w/ alternating runs; rule shifts max-starting rows right."

INVARIANTS = [
    "background is 7",
    "rows have visible runs of 2 alternating colors",
    "runs starting with min color preserved; max-starting shift right",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_rows", "all_same_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "row_count":      {"type": "int", "default": "rng 4..7", "valid": "1..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_min":        {"type": "int", "default": "3", "valid": "2..5"},
    "run_max":        {"type": "int", "default": "5", "valid": "3..7"},
    "start_min":      {"type": "int", "default": "0", "valid": "0..3"},
    "start_max":      {"type": "int", "default": "2", "valid": "0..4"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        rc_lo, rc_hi = 1, 4
    elif difficulty == "hard":
        rc_lo, rc_hi = 7, 12
    else:
        rc_lo, rc_hi = 4, 7
    row_count = int(overrides.get("row_count",
                                  ctx.draw_int("row_count", rc_lo, rc_hi)))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    a, b = sorted(palette[:2])
    w = int(overrides.get("grid_w",
                          ctx.draw_int("grid_w", 8, 12)))
    run_min = int(overrides.get("run_min", 3))
    run_max = int(overrides.get("run_max", 5))
    start_min = int(overrides.get("start_min", 0))
    start_max = int(overrides.get("start_max", 2))
    g = full_grid(row_count, w, 7)
    for r in range(row_count):
        start = rng.randint(start_min, min(start_max, max(start_min, w - run_min - 1)))
        length = rng.randint(run_min, max(run_min, min(run_max, w - start - 1)))
        if r % 2 == 0:
            vals = [a if i % 2 == 0 else b for i in range(length)]
        else:
            vals = [b if i % 2 == 0 else a for i in range(length)]
        for i, v in enumerate(vals):
            if start + i < w:
                g[r][start + i] = v
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c != 7]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h = 5; w = 10
    g = full_grid(h, w, 7)
    if name == "empty_rows":
        return g
    if name == "all_same_color":
        c = rng.choice([1, 2, 3, 4, 5, 6, 8, 9])
        for r in range(h):
            for cc in range(2, 7):
                g[r][cc] = c
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = rng.choice([1, 2, 3])
        return g
    return g
