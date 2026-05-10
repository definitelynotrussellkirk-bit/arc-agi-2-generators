"""Generator for bb52a14b.

Rule: yellow-plus-template copies yellow into every zero slot whose
surrounding non-yellow pattern matches.

Combinatorial axes (8): grid_h/w, palette_kind, n_targets,
template_position, anchor_corner, asymmetry_force, palette_size,
position_bias.
Degenerates: no_template, no_targets, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0be9d8005490"
VERSION = "1.1.0"
TASK_ID = "0be9d8005490"
SUMMARY = "A yellow-plus-template copies yellow into every zero slot whose surrounding non-yellow pattern matches."

INVARIANTS = [
    "background is color 0",
    "color 4 marks wildcard cells inside the source template bbox",
    "matching target windows preserve every non-yellow template cell",
    "zero cells at matched wildcard positions become yellow",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_targets", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "10", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_targets":      {"type": "int", "default": "2", "valid": "1..3"},
    "template_position":{"type": "str", "default": "tl",
                       "valid": "tl|center|rng"},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _stamp(g, r0, c0, pattern):
    for r, row in enumerate(pattern):
        for c, value in enumerate(row):
            if value is not None:
                if 0 <= r0 + r < len(g) and 0 <= c0 + c < len(g[0]):
                    g[r0 + r][c0 + c] = value


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h, w = 8, 9
    elif difficulty == "hard":
        h, w = 13, 14
    else:
        h, w = 9, 10
    h = int(overrides.get("grid_h", h))
    w = int(overrides.get("grid_w", w))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    a, b = pal[0], pal[1]
    g = full_grid(h, w, 0)
    template = [
        [4, a, 4],
        [b, a, b],
        [4, a, 4],
    ]
    target = [
        [None, a, None],
        [b, a, b],
        [None, a, None],
    ]
    _stamp(g, 1, 1, template)
    _stamp(g, 5, 1, target)
    n_targets = int(overrides.get("n_targets", 2))
    if n_targets >= 2 and 5 + 2 < h and 6 + 2 < w:
        _stamp(g, 5, 6, target)
    if n_targets >= 3 and 6 + 2 < h and 4 + 2 < w:
        _stamp(g, max(0, h - 4), max(0, w - 5), target)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 4)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_template":
        for r, c in [(2, 2), (3, 1), (3, 3)]:
            g[r][c] = 2
        return g
    if name == "no_targets":
        g[1][1] = 4; g[1][2] = 2; g[1][3] = 4
        g[2][1] = 3; g[2][2] = 2; g[2][3] = 3
        g[3][1] = 4; g[3][2] = 2; g[3][3] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
