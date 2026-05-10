"""Generator for puzzle 705a3229.

Rule: scattered non-bg pixels emit a vertical+horizontal ray toward
the closer edge (above if top-half, else below; same for left/right).

Combinatorial axes (8): grid_h/w, n_pixels, palette_kind, palette_size,
position_bias, min_separation, anchor_corner, asymmetry_force.
Degenerates: single_pixel, no_pixels, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e3be2a9d8ce2"
VERSION = "1.1.0"
TASK_ID = "e3be2a9d8ce2"
SUMMARY = "Pixels emit perpendicular rays toward closer edge."

INVARIANTS = [
    "background is 0",
    ">=2 non-bg pixels",
    "pixels >=2 cells apart (Manhattan)",
]

POSITION_BIASES = ("scattered", "corners", "diagonal", "row_aligned",
                   "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_pixel", "no_pixels", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_pixels":       {"type": "int", "default": "rng 3..6", "valid": "2..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "min_separation": {"type": "int", "default": "3", "valid": "2..6"},
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
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_pixels = int(overrides.get("n_pixels",
                                 ctx.draw_int("n_pixels", 3, 6)))
    n_pixels = max(2, min(8, n_pixels))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette = _build_palette(palette_kind, max(1, min(6, palette_size)),
                              rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    min_sep = int(overrides.get("min_separation", 3))
    g = full_grid(h, w, 0)
    placed = []
    candidates = _candidates(bias, h, w, rng)
    for r, c in candidates:
        if len(placed) >= n_pixels:
            break
        if not (1 <= r <= h - 2 and 1 <= c <= w - 2):
            continue
        if any(abs(r - pr) + abs(c - pc) < min_sep for pr, pc in placed):
            continue
        g[r][c] = rng.choice(palette)
        placed.append((r, c))
    if len(placed) < 2:
        for r, c in [(1, 1), (h - 2, w - 2)]:
            if g[r][c] == 0:
                g[r][c] = palette[0]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _candidates(bias, h, w, rng):
    if bias == "corners":
        return [(2, 2), (2, w - 3), (h - 3, 2), (h - 3, w - 3)]
    if bias == "diagonal":
        return [(i, i) for i in range(2, min(h, w) - 2, 3)]
    if bias == "row_aligned":
        r = h // 2
        return [(r, c) for c in range(2, w - 2, 4)]
    if bias == "centered":
        cr, cc = h // 2, w // 2
        cells = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
        cells.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return cells
    cells = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_pixel":
        g[h // 2][w // 2] = 3
        return g
    if name == "no_pixels":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
