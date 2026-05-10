"""Generator for 33b52de3.

Rule: colored key tile replaces periodically spaced gray cells by
tile index.

Combinatorial axes (8): rows, cols, palette_kind, anchor_corner,
asymmetry_force, palette_size, period_r, period_c.
Degenerates: no_grays, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "19c55a8731b1"
VERSION = "1.1.0"
TASK_ID = "19c55a8731b1"
SUMMARY = "Colored key tile replaces periodically spaced gray cells by tile index."

INVARIANTS = [
    "the key tile uses nonzero colors other than 5",
    "gray cells form at least two periodic row starts and column starts",
    "key tile sits anchored away from the gray cells",
    "key tile colors are distinct so each gray maps to a unique replacement",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_grays", "no_key", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "rows":           {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "cols":           {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "2..8"},
    "period_r":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "period_c":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        r_lo, r_hi, c_lo, c_hi = 2, 2, 2, 2
    elif difficulty == "hard":
        r_lo, r_hi, c_lo, c_hi = 3, 4, 3, 4
    else:
        r_lo, r_hi, c_lo, c_hi = 2, 3, 2, 3
    rows = ctx.draw_int("rows", r_lo, r_hi)
    cols = ctx.draw_int("cols", c_lo, c_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < rows * cols:
        pool = pool + [c for c in [1, 2, 3, 4, 6, 7, 8, 9] if c not in pool]
    colors = pool[:max(rows * cols, 1)]
    period_r = rng.randint(2, 3)
    period_c = rng.randint(2, 3)
    gr0 = 5
    gc0 = 1
    h = gr0 + (rows - 1) * period_r + 2
    w = gc0 + (cols - 1) * period_c + 2
    g = full_grid(h, w, 0)
    for r in range(rows):
        for c in range(cols):
            g[1 + r][1 + c] = colors[(r * cols + c) % len(colors)]
            g[gr0 + r * period_r][gc0 + c * period_c] = 5
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 5)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_grays":
        g[1][1] = 1
        g[1][2] = 2
        return g
    if name == "no_key":
        g[5][1] = 5
        g[7][3] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
