"""Generator for c3202e5a.

Rule: full sep-rows + full sep-cols divide the grid; output the unique
color of pure single-color blocks, else 0.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_pure, density.
Degenerates: all_pure, no_pure, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4d5bb3c0250b"
VERSION = "1.1.0"
TASK_ID = "4d5bb3c0250b"
SUMMARY = "23x23 grid with sep-rows/cols of color 3 dividing into 5x5 blocks."

INVARIANTS = [
    "h equals 23 and w equals 23",
    "three full sep-rows and three full sep-cols of color 3",
    "at least one block is pure with a single non-bg color",
    "most other blocks contain two distinct non-bg colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("all_pure", "no_pure", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "23", "valid": "23"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_pure":         {"type": "int", "default": "1", "valid": "1..4"},
    "density":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
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
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    h = w = 23
    g = full_grid(h, w, 0)
    sep_color = 3
    sep_rows = [5, 11, 17]
    sep_cols = [5, 11, 17]
    for r in sep_rows:
        for c in range(w):
            g[r][c] = sep_color
    for c in sep_cols:
        for r in range(h):
            g[r][c] = sep_color
    block_starts = [(r0, c0) for r0 in [0, 6, 12, 18] for c0 in [0, 6, 12, 18]]
    pure_idx = rng.randint(0, len(block_starts) - 1)
    for i, (r0, c0) in enumerate(block_starts):
        if i == pure_idx:
            color = rng.choice(palette)
            n_cells = rng.randint(2, 4)
            for _ in range(n_cells):
                r = rng.randint(r0, r0 + 4)
                c = rng.randint(c0, c0 + 4)
                g[r][c] = color
        else:
            cs = rng.sample(palette, 2)
            n_cells = rng.randint(2, 4)
            for _ in range(n_cells):
                r = rng.randint(r0, r0 + 4)
                c = rng.randint(c0, c0 + 4)
                g[r][c] = rng.choice(cs)
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 4]
    else:
        pool = [1, 2, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 3)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h = w = 23
    g = full_grid(h, w, 0)
    sep_rows = [5, 11, 17]
    sep_cols = [5, 11, 17]
    for r in sep_rows:
        for c in range(w):
            g[r][c] = 3
    for c in sep_cols:
        for r in range(h):
            g[r][c] = 3
    if name == "no_pure":
        return g
    if name == "all_pure":
        for r0 in [0, 6, 12, 18]:
            for c0 in [0, 6, 12, 18]:
                g[r0][c0] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
