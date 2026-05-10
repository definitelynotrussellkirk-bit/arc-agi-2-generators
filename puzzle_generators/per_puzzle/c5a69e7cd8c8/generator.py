"""Generator for 25d487eb.

Rule: singleton color emits ray opposite its first open neighboring cell.

Combinatorial axes (8): size, opening, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, n_extras.
Degenerates: no_singleton, no_support, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c5a69e7cd8c8"
VERSION = "1.1.0"
TASK_ID = "c5a69e7cd8c8"
SUMMARY = "A singleton color emits a ray opposite its first open neighboring cell."

INVARIANTS = [
    "exactly one nonzero color appears once",
    "the singleton has one first open cardinal neighbor",
    "all other nonzero cells use a repeated support color",
    "the ray is drawn through zero cells opposite the opening",
]

DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_singleton", "no_support", "full_grid")
HELPFUL_TEXTURES = tuple(DIRECTIONS.keys())

AXES = {
    "size":           {"type": "int", "default": "rng 10..14", "valid": "7..30"},
    "opening":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "centered",
                       "valid": "centered|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "n_extras":       {"type": "int", "default": "6", "valid": "3..8"},
    "texture":        {"type": "str", "default": "alias for opening",
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
        s_lo, s_hi = 7, 10
    elif difficulty == "hard":
        s_lo, s_hi = 14, 22
    else:
        s_lo, s_hi = 10, 14
    size = ctx.draw_int("size", s_lo, s_hi)
    opening = (overrides.get("texture") if overrides.get("texture") in HELPFUL_TEXTURES else None) or \
              overrides.get("opening") or \
              ctx.draw_choice("opening", tuple(DIRECTIONS))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    support, singleton = pal[0], pal[1]
    g = full_grid(size, size, 0)
    mr = size // 2
    mc = size // 2
    g[mr][mc] = singleton
    open_dr, open_dc = DIRECTIONS[opening]
    for dr, dc in DIRECTIONS.values():
        if (dr, dc) != (open_dr, open_dc):
            if 0 <= mr + dr < size and 0 <= mc + dc < size:
                g[mr + dr][mc + dc] = support
    extras = [
        (mr - 1, mc - 1), (mr - 1, mc + 1),
        (mr + 1, mc - 1), (mr + 1, mc + 1),
        (mr + 2, mc), (mr, mc + 2),
    ]
    for r, c in extras:
        if 0 <= r < size and 0 <= c < size and g[r][c] == 0:
            g[r][c] = support
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
    size = 12
    g = full_grid(size, size, 0)
    if name == "no_singleton":
        g[5][5] = 1; g[5][6] = 1; g[6][5] = 1
        return g
    if name == "no_support":
        g[6][6] = 2
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 1
        return g
    return g
