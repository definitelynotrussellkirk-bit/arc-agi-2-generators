"""Generator for e048c9ed.

Rule: bars write a squared length code into the marker column.

Combinatorial axes (8): grid_h/w, marker_col, bar_color, palette_kind,
length_pattern, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_marker, no_bars, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9fe97c2dd8a4"
VERSION = "1.1.0"
TASK_ID = "9fe97c2dd8a4"
SUMMARY = "Bars write squared length code into marker column using duplicate non-marker lengths."

INVARIANTS = [
    "background is color 0",
    "one color-5 marker supplies the target output column",
    "each nonempty row contains a horizontal bar",
    "two non-marker rows share a duplicate bar length that anchors the unique-length adjustment",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marker", "no_bars", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..18"},
    "marker_col":     {"type": "int", "default": "rng 7..9", "valid": "1..29"},
    "bar_color":      {"type": "color", "default": "rng !{0,5}",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "length_pattern": {"type": "str", "default": "varied",
                       "valid": "varied|tight"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
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
        h_lo, h_hi = 6, 7
    elif difficulty == "hard":
        h_lo, h_hi = 8, 12
    else:
        h_lo, h_hi = 6, 8
    mc = ctx.draw_int("marker_col", 7, 9)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("bar_color",
                              rng.choice(pal) if pal else
                              ctx.draw_color("bar_color", exclude={0, 5})))
    h = rng.randint(h_lo, h_hi)
    w = max(mc + 2, 11)
    g = full_grid(h, w, 0)
    lengths = [3, 3, 5, 4, 2, 6, 4][:h]
    for r, length in enumerate(lengths):
        start = rng.randint(0, 1)
        for c in range(start, start + length):
            if c != mc and 0 <= c < w:
                g[r][c] = color
    marker_r = h - 1
    g[marker_r][mc] = 5
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
    h, w = 7, 12
    g = full_grid(h, w, 0)
    if name == "no_marker":
        for r in range(h):
            for c in range(min(4, w)):
                g[r][c] = 3
        return g
    if name == "no_bars":
        g[h - 1][8] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
