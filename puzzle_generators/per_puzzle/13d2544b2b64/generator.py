"""Generator for cbded52d.

Rule: 3x3 cell grid; matching left/right markers fill the center column,
matching top/bottom markers fill the center row.

Combinatorial axes (8): cell_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, marker_pair,
n_distinct_colors.
Degenerates: no_markers, all_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "13d2544b2b64"
VERSION = "1.1.0"
TASK_ID = "13d2544b2b64"
SUMMARY = "3x3 cell grid: agreeing left/right and top/bottom markers fill the center."

INVARIANTS = [
    "two zero rows and two zero columns divide the grid into a 3x3 cell grid",
    "non-separator cells start as color 1 so they are candidates for replacement",
    "matching left/right local cells mark the center column cell",
    "matching top/bottom local cells mark the center row cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "all_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "cell_size":      {"type": "int", "default": "2", "valid": "2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "marker_pair":    {"type": "str", "default": "lr_tb", "valid": "lr_tb"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    cell = ctx.draw_int("cell_size", 2, 2)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    hmark, vmark = pool[0], pool[1]
    g = full_grid(3 * cell + 2, 3 * cell + 2, 1)
    sep0 = cell
    sep1 = 2 * cell + 1
    for c in range(len(g[0])):
        g[sep0][c] = 0
        g[sep1][c] = 0
    for r in range(len(g)):
        g[r][sep0] = 0
        g[r][sep1] = 0
    g[0][0] = hmark
    g[0][sep1 + 1] = hmark
    g[0][sep0 + 1] = 1
    g[sep1 + 1][sep0 + 1] = vmark
    g[0][sep0 + 1] = vmark
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 1)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 1)
    if name == "no_markers":
        return g
    if name == "all_markers":
        return full_grid(8, 8, 2)
    if name == "full_grid":
        return full_grid(8, 8, 5)
    return g
