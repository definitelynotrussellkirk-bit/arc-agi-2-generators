"""Generator for puzzle 5751f35e.

Rule: for each color, expand bbox to square (max of h, w). Sort by
area asc; paint each square. Smaller squares overwrite larger.

Combinatorial axes (8): grid_h/w, n_colors, palette_kind,
density_a, density_b, position_bias, anchor_corner, asymmetry_force.
Degenerates: tied_areas, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1bf52c06eae6"
VERSION = "1.1.0"
TASK_ID = "1bf52c06eae6"
SUMMARY = "Scattered cells; rule paints each color's bbox as square, smallest last."

INVARIANTS = [
    "background is 0",
    ">=2 distinct non-bg colors",
    "their bboxes have distinct areas (winner unambiguous)",
]

POSITION_BIASES = ("scattered", "centered_inside", "corners",
                   "spread", "diagonal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_areas", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "n_colors":       {"type": "int", "default": "2", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density_a":      {"type": "float", "default": "rng 0.35..0.55",
                       "valid": "0.2..0.7"},
    "density_b":      {"type": "float", "default": "rng 0.45..0.65",
                       "valid": "0.2..0.8"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 7, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 3, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, 2, rng)
    density_a = float(overrides.get("density_a",
                                    ctx.draw_rng("density_a")
                                    .uniform(0.35, 0.55)))
    density_b = float(overrides.get("density_b",
                                    ctx.draw_rng("density_b")
                                    .uniform(0.45, 0.65)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            if rng.random() < density_a:
                g[r][c] = palette[0]
    if bias == "centered_inside":
        cr, cc = h // 2, w // 2
        r1, r2 = cr - 2, cr + 1
        c1, c2 = cc - 2, cc + 1
    elif bias == "corners":
        r1, r2 = 1, max(2, h // 2)
        c1, c2 = 1, max(2, w // 2)
    elif bias == "diagonal":
        r1 = rng.randint(2, max(2, h - 4))
        r2 = r1 + rng.randint(1, 2)
        c1 = r1; c2 = r2
    else:
        r1 = rng.randint(2, max(2, h - 4))
        r2 = rng.randint(r1 + 1, max(r1 + 1, h - 2))
        c1 = rng.randint(2, max(2, w - 5))
        c2 = rng.randint(c1 + 1, max(c1 + 1, w - 3))
    r1 = max(0, min(h - 1, r1))
    r2 = max(r1, min(h - 1, r2))
    c1 = max(0, min(w - 1, c1))
    c2 = max(c1, min(w - 1, c2))
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            if rng.random() < density_b:
                g[r][c] = palette[1]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    if name == "tied_areas":
        for r in range(2, 5):
            for c in range(2, 5):
                if rng.random() < 0.6:
                    g[r][c] = palette[0]
        for r in range(2, 5):
            for c in range(w - 5, w - 2):
                if rng.random() < 0.6:
                    g[r][c] = palette[1]
        return g
    if name == "single_color":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = palette[0]
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[0]
        return g
    return g
