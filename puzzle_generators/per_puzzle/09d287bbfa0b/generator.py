"""Generator for 60d73be6.

Rule: cross separator (one full row + one full col, non-bg) + colored
pixels in one quadrant; rule reflects pixels into all 4 quadrants.

Combinatorial axes (8): grid_h/w, sep_color, cross_position, n_pixels,
quadrant, palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_cross, multiple_quadrants, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "09d287bbfa0b"
VERSION = "1.1.0"
TASK_ID = "09d287bbfa0b"
SUMMARY = "Cross separator + pixels in one quadrant; rule reflects into all 4 quadrants."

INVARIANTS = [
    "background is 7",
    "exactly one row entirely non-bg (horizontal separator)",
    "exactly one column entirely non-bg (vertical separator)",
    ">=2 colored pixels in one quadrant",
]

CROSS_POSITIONS = ("center", "off_center", "near_corner", "rng")
QUADRANTS = ("nw", "ne", "sw", "se")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cross", "multiple_quadrants", "full_grid")
HELPFUL_TEXTURES = CROSS_POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "sep_color":      {"type": "color", "default": "rng",
                       "valid": "1..6"},
    "cross_position": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CROSS_POSITIONS)},
    "n_pixels":       {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "quadrant":       {"type": "str", "default": "nw",
                       "valid": "|".join(QUADRANTS)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "texture":        {"type": "str", "default": "alias for cross_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 7, 9
        np_lo, np_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
        np_lo, np_hi = 4, 6
    else:
        h_lo, h_hi = 9, 13
        np_lo, np_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    sep_color = int(overrides.get("sep_color",
                                  rng.choice([1, 2, 3, 4, 5, 6])))
    cross_pos = (overrides.get("texture") or
                 overrides.get("cross_position")
                 or ctx.draw_choice("cross_position",
                                    list(CROSS_POSITIONS)))
    if cross_pos == "center":
        cr = h // 2
        cc = w // 2
    elif cross_pos == "off_center":
        cr = max(2, h // 2 - 1)
        cc = max(2, w // 2 - 1)
    elif cross_pos == "near_corner":
        cr = rng.randint(2, max(2, h // 3))
        cc = rng.randint(2, max(2, w // 3))
    else:
        cr = rng.randint(2, h - 3)
        cc = rng.randint(2, w - 3)
    cr = max(2, min(cr, h - 3))
    cc = max(2, min(cc, w - 3))
    g = full_grid(h, w, 7)
    for c in range(w):
        g[cr][c] = sep_color
    for r in range(h):
        g[r][cc] = sep_color
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, sep_color, rng)
    quadrant = overrides.get("quadrant",
                             ctx.draw_choice("quadrant", list(QUADRANTS)))
    n_pix = int(overrides.get("n_pixels",
                              ctx.draw_int("n_pixels", np_lo, np_hi)))
    n_pix = max(2, min(8, n_pix))
    for _ in range(n_pix):
        for _try in range(20):
            if quadrant == "nw":
                r = rng.randint(0, cr - 1); c = rng.randint(0, cc - 1)
            elif quadrant == "ne":
                r = rng.randint(0, cr - 1); c = rng.randint(cc + 1, w - 1)
            elif quadrant == "sw":
                r = rng.randint(cr + 1, h - 1); c = rng.randint(0, cc - 1)
            else:
                r = rng.randint(cr + 1, h - 1); c = rng.randint(cc + 1, w - 1)
            if g[r][c] == 7:
                g[r][c] = rng.choice(palette)
                break
    return g


def _build_palette(kind, sep_color, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c not in (7, sep_color)]
    if not pool:
        pool = [c for c in [1, 2, 3, 4, 5, 6, 8, 9] if c not in (7, sep_color)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 7)
    if name == "no_cross":
        g[2][2] = 1; g[3][3] = 2
        return g
    if name == "multiple_quadrants":
        cr, cc = 5, 5
        for c in range(w):
            g[cr][c] = 4
        for r in range(h):
            g[r][cc] = 4
        g[2][2] = 1; g[2][8] = 1; g[8][2] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
