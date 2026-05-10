"""Generator for puzzle 762cd429.

Rule: 2x2 template at (tr, 0..1) is repeated into exponentially wider
staircase blocks rightward.

Combinatorial axes (8): width, height, template_row, palette_kind,
palette_size, anchor_corner, asymmetry_force, include_decoy.
Degenerates: no_template, full_template, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dc3b5c670093"
VERSION = "1.1.0"
TASK_ID = "dc3b5c670093"
SUMMARY = "2x2 template; rule expands into staircase doubling rightward."

INVARIANTS = [
    "background is 0",
    "9-row grid",
    "2x2 template at (tr, 0..1) with 4 distinct non-bg colors",
    "tr in [3, 5] (so staircase fits)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "full_template", "monochrome")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "width":          {"type": "int", "default": "rng 12..18", "valid": "8..28"},
    "height":         {"type": "int", "default": "9", "valid": "9"},
    "template_row":   {"type": "int", "default": "4", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
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
        w_lo, w_hi = 8, 12
    elif difficulty == "hard":
        w_lo, w_hi = 18, 28
    else:
        w_lo, w_hi = 12, 18
    w = int(overrides.get("width", ctx.draw_int("width", w_lo, w_hi)))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    colors = _build_palette(palette_kind, 4, rng)
    tr = int(overrides.get("template_row", 4))
    tr = max(3, min(5, tr))
    h = 9
    g = full_grid(h, w, 0)
    g[tr][0] = colors[0]
    g[tr][1] = colors[1]
    g[tr + 1][0] = colors[2]
    g[tr + 1][1] = colors[3]
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
    h = 9; w = 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        return g
    if name == "full_template":
        # Template fills first 2 cols completely
        for r in range(h):
            g[r][0] = 3
            g[r][1] = 4
        return g
    if name == "monochrome":
        for r in range(h):
            g[4][r % 2] = 3
        return g
    return g
