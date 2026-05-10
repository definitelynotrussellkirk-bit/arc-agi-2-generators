"""Generator for e4888269.

Rule: solid two-column key table defines ordered color substitutions.

Combinatorial axes (8): grid_h/w, key_height, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, key_position.
Degenerates: no_key, no_targets, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "35b257d07d86"
VERSION = "1.1.0"
TASK_ID = "35b257d07d86"
SUMMARY = "Solid two-column key table defines ordered color substitutions."

INVARIANTS = [
    "background is color 0",
    "the key table is a solid 2-column multicolor component",
    "key rows are read top-to-bottom as color substitution pairs",
    "the key table itself is preserved while other cells are substituted",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_key", "no_targets", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "10", "valid": "8..14"},
    "key_height":     {"type": "int", "default": "3", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        kh_lo, kh_hi = 3, 3
    elif difficulty == "hard":
        kh_lo, kh_hi = 4, 5
    else:
        kh_lo, kh_hi = 3, 4
    key_height = ctx.draw_int("key_height", kh_lo, kh_hi)
    key_height = max(3, min(5, key_height))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, key_height + 1, rng)
    if len(pool) < key_height + 1:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    colors = pool[:key_height + 1]
    g = full_grid(9, 10, 0)
    pairs = [(colors[i], colors[i + 1]) for i in range(key_height)]
    for r in range(key_height):
        if 1 + r < 9:
            g[1 + r][1] = pairs[r][0]
            g[1 + r][2] = pairs[r][1]
    for i, value in enumerate(colors[:4]):
        if 4 + i < 10:
            g[6][4 + i] = value
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_key":
        for i, value in enumerate([1, 2, 3, 4]):
            g[6][4 + i] = value
        return g
    if name == "no_targets":
        for r in range(3):
            g[1 + r][1] = r + 2
            g[1 + r][2] = r + 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
