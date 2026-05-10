"""Generator for 78e78cff.

Rule: singleton fill color expands by scanline intervals determined
from marker gaps around its column.

Combinatorial axes (8): width, height, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, marker_kind.
Degenerates: no_seed, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "30d3af94d21e"
VERSION = "1.1.0"
TASK_ID = "30d3af94d21e"
SUMMARY = "Singleton fill color expands by scanline intervals from marker gaps."

INVARIANTS = [
    "background is the modal color",
    "one non-background color appears exactly once and is the fill seed",
    "another non-background color supplies row interval markers",
    "marker rows differ from seed row so the rule has work to do",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "width":          {"type": "int", "default": "rng 9..11", "valid": "5..14"},
    "height":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "marker_kind":    {"type": "str", "default": "rng", "valid": "rng"},
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
        w_lo, w_hi = 9, 9
    elif difficulty == "hard":
        w_lo, w_hi = 11, 13
    else:
        w_lo, w_hi = 9, 11
    w = ctx.draw_int("width", w_lo, w_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    bg, fill, mark = pool[0], pool[1], pool[2]
    h = 8 + rng.randint(0, 2)
    g = full_grid(h, w, bg)
    cc = w // 2
    g[h // 2][cc] = fill
    for c in (1, w - 2):
        g[1][c] = mark
    for c in (2, w - 3):
        g[h - 2][c] = mark
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 5)
    if name == "no_seed":
        g[1][1] = 2
        g[8][8] = 2
        return g
    if name == "no_markers":
        g[5][5] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
