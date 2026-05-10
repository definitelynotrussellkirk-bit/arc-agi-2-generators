"""Generator for 2037f2c7.

Rule: two aligned large figures compared row-wise, marking
zero/nonzero disagreements.

Combinatorial axes (8): figure_h, figure_w, gap, palette_kind,
n_holes, position_bias, anchor_corner, asymmetry_force.
Degenerates: no_holes, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f4a707214fb5"
VERSION = "1.1.0"
TASK_ID = "f4a707214fb5"
SUMMARY = "Two aligned large figures compared row-wise; rule marks disagreements."

INVARIANTS = [
    "there are two large 8-connected multicolor objects",
    "the two objects have the same bounding-box dimensions",
    "the upper object sorts before the lower object",
    "rows with zero/nonzero disagreements become the compact output rows",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "figure_height":  {"type": "int", "default": "rng 3..5", "valid": "3..8"},
    "figure_width":   {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "gap":            {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_holes":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "centered|spread|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
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
        fh_lo, fh_hi = 3, 4
        fw_lo, fw_hi = 3, 4
        nh_lo, nh_hi = 1, 2
    elif difficulty == "hard":
        fh_lo, fh_hi = 5, 8
        fw_lo, fw_hi = 5, 8
        nh_lo, nh_hi = 3, 6
    else:
        fh_lo, fh_hi = 3, 5
        fw_lo, fw_hi = 4, 6
        nh_lo, nh_hi = 2, 4
    fh = ctx.draw_int("figure_height", fh_lo, fh_hi)
    fw = ctx.draw_int("figure_width", fw_lo, fw_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    color_a, color_b = pal[0], pal[1]
    gap = ctx.draw_int("gap", 2, 3)
    h = 2 * fh + gap + 2
    w = fw + rng.randint(3, 6)
    c0 = rng.randint(1, max(1, w - fw - 1))
    r1 = 1
    r2 = r1 + fh + gap
    g = full_grid(h, w, 0)
    for r in range(fh):
        for c in range(fw):
            g[r1 + r][c0 + c] = color_a
            g[r2 + r][c0 + c] = color_b
    hole_candidates = [
        (r, c)
        for r in range(fh)
        for c in range(fw)
        if 0 < r < fh - 1 or 0 < c < fw - 1
    ]
    rng.shuffle(hole_candidates)
    n_h = int(overrides.get("n_holes",
                            rng.randint(nh_lo, min(nh_hi, len(hole_candidates)))))
    n_h = max(1, min(len(hole_candidates), n_h))
    for r, c in hole_candidates[:n_h]:
        g[r2 + r][c0 + c] = 0
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 8)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 12, 10
    g = full_grid(h, w, 0)
    if name == "no_holes":
        for r in range(3):
            for c in range(4):
                g[1 + r][3 + c] = 2
                g[7 + r][3 + c] = 3
        return g
    if name == "all_holes":
        for r in range(3):
            for c in range(4):
                g[1 + r][3 + c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
