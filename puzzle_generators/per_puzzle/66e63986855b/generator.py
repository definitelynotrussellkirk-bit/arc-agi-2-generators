"""Generator for puzzle bf32578f.

Rule: C-shape: top + bottom rows full, middle rows partial. Output
extends middle rows from their rightmost cell across to col 2*maxc-rc.

Combinatorial axes (8): grid_h/w, color, box_h, box_w, palette_kind,
middle_rc_distribution, anchor_corner, asymmetry_force.
Degenerates: no_shape, full_box, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "66e63986855b"
VERSION = "1.1.0"
TASK_ID = "66e63986855b"
SUMMARY = "C-shape; rule mirrors middle rows across rightmost col."

INVARIANTS = [
    "background is 0",
    "single color forming C/U-shape",
    "top + bottom rows of bbox are full width",
    "middle rows have varying widths starting at col 0",
    "global maxc < w / 2 so output mirror fits",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
MIDDLE_DISTRIBUTIONS = ("uniform", "increasing", "decreasing",
                       "centered_peak", "alternating")
DEGENERATE_TEXTURES = ("no_shape", "full_box", "single_row")
HELPFUL_TEXTURES = MIDDLE_DISTRIBUTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..14", "valid": "6..18"},
    "color":          {"type": "color", "default": "rng (≠0)",
                       "valid": "1..9"},
    "box_h":          {"type": "int", "default": "rng 4..h-1", "valid": "3..h-1"},
    "box_w":          {"type": "int", "default": "rng 3..min(w/2,6)",
                       "valid": "3..w/2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "middle_distribution":{"type": "str", "default": "rng helpful",
                          "valid": "|".join(MIDDLE_DISTRIBUTIONS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for middle_distribution",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 9, 14
    else:
        h_lo, h_hi = 5, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    color = int(overrides.get("color", palette[0]))
    box_h = int(overrides.get("box_h",
                              ctx.draw_int("box_h", 4, max(4, h - 1))))
    box_w = int(overrides.get("box_w",
                              ctx.draw_int("box_w", 3,
                                           min(w // 2, 6))))
    box_h = max(3, min(h - 1, box_h))
    box_w = max(3, min(w // 2, box_w))
    distribution = (overrides.get("texture") or
                    overrides.get("middle_distribution")
                    or ctx.draw_choice("middle_distribution",
                                       list(MIDDLE_DISTRIBUTIONS)))
    g = full_grid(h, w, 0)
    box_r = 0
    box_c = 0
    for c in range(box_c, box_c + box_w):
        g[box_r][c] = color
        g[box_r + box_h - 1][c] = color
    middle_rs = list(range(box_r + 1, box_r + box_h - 1))
    rcs = _build_middle_rcs(distribution, middle_rs, box_w, rng)
    for r, rc in zip(middle_rs, rcs):
        for c in range(box_c, box_c + rc + 1):
            g[r][c] = color
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
    rng.shuffle(pool)
    return pool


def _build_middle_rcs(distribution, middle_rs, box_w, rng):
    n = len(middle_rs)
    if n == 0:
        return []
    if distribution == "uniform":
        return [rng.randint(0, box_w - 2) for _ in range(n)]
    if distribution == "increasing":
        return [min(box_w - 2, i) for i in range(n)]
    if distribution == "decreasing":
        return [max(0, n - 1 - i) for i in range(n)]
    if distribution == "centered_peak":
        center = n // 2
        return [max(0, min(box_w - 2, center - abs(i - center) + 1))
                for i in range(n)]
    if distribution == "alternating":
        return [box_w - 2 if i % 2 == 0 else 0 for i in range(n)]
    return [rng.randint(0, box_w - 2) for _ in range(n)]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_shape":
        return g
    if name == "full_box":
        for r in range(h):
            for c in range(min(4, w)):
                g[r][c] = color
        return g
    if name == "single_row":
        for c in range(min(4, w)):
            g[h // 2][c] = color
        return g
    return g
