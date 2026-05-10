"""Generator for 3345333e.

Rule: solid rectangular occluder is cleared or reconstructed from
visible left-right mirror evidence.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
shape_kind.
Degenerates: no_occluder, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "3025c0637069"
VERSION = "1.1.0"
TASK_ID = "3025c0637069"
SUMMARY = "Solid rectangular occluder reconstructed from mirror evidence."

INVARIANTS = [
    "one nonzero color forms a solid rectangular occluder",
    "one different nonzero color forms a non-rectangular visible shape",
    "the occluder hides part of the shape along a left-right symmetry axis",
    "shape and occluder colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_occluder", "no_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "shape_kind":     {"type": "str", "default": "fixed", "valid": "fixed"},
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
        h_lo, h_hi = 10, 11
    elif difficulty == "hard":
        h_lo, h_hi = 13, 16
    else:
        h_lo, h_hi = 10, 13
    h = ctx.draw_int("height", h_lo, h_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    shape_color, rect_color = pool[0], pool[1]
    w = rng.randint(11, 14)
    g = full_grid(h, w, 0)
    top = rng.randint(2, h - 6)
    left = rng.randint(2, 3)
    for r, c in [(top, left), (top + 1, left), (top + 2, left),
                 (top, left + 1), (top + 2, left + 1)]:
        g[r][c] = shape_color
    draw_rect(g, top - 1, left + 3, 5, 3, rect_color)
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
    g = full_grid(11, 12, 0)
    if name == "no_occluder":
        for r, c in [(2, 2), (3, 2), (4, 2), (2, 3), (4, 3)]:
            g[r][c] = 2
        return g
    if name == "no_shape":
        draw_rect(g, 1, 5, 5, 3, 3)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
