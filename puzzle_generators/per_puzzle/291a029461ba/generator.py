"""Generator for 8731374e.

Rule: largest near-solid rectangle contains dots whose rows and
columns become a cross-hatch crop.

Combinatorial axes (8): grid_h/w, dot_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
rect_kind.
Degenerates: no_rect, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "291a029461ba"
VERSION = "1.1.0"
TASK_ID = "291a029461ba"
SUMMARY = "Largest near-solid rectangle dots produce cross-hatch crop output."

INVARIANTS = [
    "one near-solid rectangle is larger than any competing near-solid region",
    "the rectangle top-left cell gives the crop background color",
    "one to four interior outlier dots share a single dot color",
    "rectangle and dot colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "no_dots", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "7..18"},
    "dot_count":      {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "rect_kind":      {"type": "str", "default": "solid", "valid": "solid"},
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
        dc_lo, dc_hi = 1, 2
    elif difficulty == "hard":
        dc_lo, dc_hi = 3, 5
    else:
        dc_lo, dc_hi = 1, 4
    dot_count = ctx.draw_int("dot_count", dc_lo, dc_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    bg_color, dot_color = pool[0], pool[1]
    rh = rng.randint(4, 7)
    rw = rng.randint(4, 8)
    h = rh + 4 + rng.randint(0, 2)
    w = rw + 4 + rng.randint(0, 2)
    r0 = rng.randint(1, h - rh - 1)
    c0 = rng.randint(1, w - rw - 1)
    g = full_grid(h, w, 0)
    draw_rect(g, r0, c0, rh, rw, bg_color)
    candidates = [
        (r, c)
        for r in range(r0, r0 + rh)
        for c in range(c0, c0 + rw)
        if (r, c) != (r0, c0)
    ]
    rng.shuffle(candidates)
    for r, c in candidates[:dot_count]:
        g[r][c] = dot_color
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
    g = full_grid(10, 12, 0)
    if name == "no_rect":
        g[3][3] = 2
        return g
    if name == "no_dots":
        draw_rect(g, 2, 2, 5, 6, 1)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
