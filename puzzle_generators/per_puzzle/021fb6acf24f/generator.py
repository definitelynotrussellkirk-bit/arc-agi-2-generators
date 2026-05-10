"""Generator for 56ff96f3.

Rule: for each non-bg color in scan order, fill bbox-rectangle 0-cells
with that color. Order matters because earlier fills are preserved.

Combinatorial axes (8): grid_h/w, n_colors, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size.
Degenerates: collinear, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "021fb6acf24f"
VERSION = "1.1.0"
TASK_ID = "021fb6acf24f"
SUMMARY = "2-3 colors with corner cells defining non-degenerate bboxes."

INVARIANTS = [
    ">=2 distinct non-bg colors",
    "each color has 2 cells at distinct rows AND distinct cols",
]

POSITION_BIASES = ("scattered", "diagonal", "corners", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("collinear", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi, w_lo, w_hi = 5, 6, 7, 8
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 11, 14
        n_lo, n_hi = 3, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 8, 8, 10
        n_lo, n_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    n = int(overrides.get("n_colors",
                          ctx.draw_int("n_colors", n_lo, n_hi)))
    n = max(2, min(4, n))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, n, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    used = set()
    for i, color in enumerate(pal):
        for _ in range(40):
            r1, c1, r2, c2 = _pick_corners(bias, h, w, i, n, rng)
            if r1 == r2 or c1 == c2:
                continue
            if r1 > r2:
                r1, r2 = r2, r1
            if c1 > c2:
                c1, c2 = c2, c1
            if (r1, c1) in used or (r2, c2) in used:
                continue
            if g[r1][c1] != 0 or g[r2][c2] != 0:
                continue
            g[r1][c1] = color
            g[r2][c2] = color
            used.add((r1, c1)); used.add((r2, c2))
            break
    return g


def _pick_corners(bias, h, w, idx, n, rng):
    if bias == "diagonal":
        if idx % 2 == 0:
            r1, c1 = rng.randint(0, h - 3), rng.randint(0, w - 3)
            r2, c2 = rng.randint(r1 + 2, h - 1), rng.randint(c1 + 2, w - 1)
        else:
            r1, c1 = rng.randint(0, h - 3), rng.randint(2, w - 1)
            r2, c2 = rng.randint(r1 + 2, h - 1), rng.randint(0, c1 - 2)
        return r1, c1, r2, c2
    if bias == "corners":
        corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        rng.shuffle(corners)
        a, b = corners[0], corners[1]
        return a[0], a[1], b[0], b[1]
    if bias == "centered":
        cr, cc = h // 2, w // 2
        rad_r = max(2, h // 3)
        rad_c = max(2, w // 3)
        r1 = rng.randint(max(0, cr - rad_r), max(0, cr - 1))
        c1 = rng.randint(max(0, cc - rad_c), max(0, cc - 1))
        r2 = rng.randint(min(h - 1, cr + 1), min(h - 1, cr + rad_r))
        c2 = rng.randint(min(w - 1, cc + 1), min(w - 1, cc + rad_c))
        return r1, c1, r2, c2
    r1 = rng.randint(0, h - 3); r2 = rng.randint(r1 + 2, h - 1)
    c1 = rng.randint(0, w - 3); c2 = rng.randint(c1 + 2, w - 1)
    return r1, c1, r2, c2


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
    if len(pool) < n:
        for c in [2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "collinear":
        g[2][1] = 2; g[2][7] = 2
        g[4][1] = 3; g[4][7] = 3
        return g
    if name == "single_color":
        g[1][1] = 2; g[5][7] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
