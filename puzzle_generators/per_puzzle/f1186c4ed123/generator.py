"""Generator for 12997ef3.

Rule: blue template recolored once for each singleton color dot.

Combinatorial axes (8): grid_h/w, n_dots, template_variant, orientation,
palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_template, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f1186c4ed123"
VERSION = "1.1.0"
TASK_ID = "f1186c4ed123"
SUMMARY = "A blue template is recolored once for each singleton color dot."

INVARIANTS = [
    "the blue cells form one bounded template",
    "each non-blue color dot appears exactly once",
    "dots in one column request a vertical stack",
    "dots in multiple columns request horizontal concatenation",
]

ORIENTATIONS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_dots", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

TEMPLATES = [
    [[1, 0, 1], [1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0], [1, 1], [0, 1]],
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "6..20"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..20"},
    "n_dots":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "template_variant":{"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "texture":        {"type": "str", "default": "alias for orientation",
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
        h_lo, h_hi = 6, 9
        nd_lo, nd_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 13, 20
        nd_lo, nd_hi = 4, 6
    else:
        h_lo, h_hi = 9, 13
        nd_lo, nd_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_dots = ctx.draw_int("n_dots", nd_lo, nd_hi)
    n_dots = max(1, min(min(min(h, w) - 2, 6), n_dots))
    g = full_grid(h, w, 0)
    tv = int(overrides.get("template_variant",
                           ctx.draw_int("template_variant",
                                        0, len(TEMPLATES) - 1)))
    tv = max(0, min(len(TEMPLATES) - 1, tv))
    tmpl = TEMPLATES[tv]
    th, tw = len(tmpl), len(tmpl[0])
    tr = rng.randint(1, max(1, h - th - 3))
    tc = rng.randint(1, max(1, w - tw - 4))
    for dr, row in enumerate(tmpl):
        for dc, v in enumerate(row):
            if v:
                g[tr + dr][tc + dc] = 1
    colors = list(ctx.draw_distinct_colors("dot_colors", n=n_dots,
                                           exclude={0, 1}))
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    if orientation == "vertical":
        c = w - 2
        rows = sorted(rng.sample(range(h), n_dots))
        for color, r in zip(colors, rows):
            g[r][c] = color
    else:
        r = h - 2
        cols = sorted(rng.sample(range(w), n_dots))
        for color, c in zip(colors, cols):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_template":
        g[h - 2][2] = 2; g[h - 2][5] = 3
        return g
    if name == "no_dots":
        for dr, row in enumerate(TEMPLATES[0]):
            for dc, v in enumerate(row):
                if v:
                    g[2 + dr][2 + dc] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
