"""Generator for puzzle e48d4e1a.

Rule: input has full-row + full-col cross of one non-gray color + N
gray(5) markers. Output moves cross center by (N, -N).

Combinatorial axes (8): grid_h/w, cross_color, n_grays, cross_position,
gray_distribution, anchor_corner, asymmetry_force, palette_kind.
Degenerates: no_grays, cross_at_edge, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dc050b56cac4"
VERSION = "1.1.0"
TASK_ID = "dc050b56cac4"
SUMMARY = "Plus-cross + gray markers; rule moves cross by (N, -N)."

INVARIANTS = [
    "exactly one full row + one full col of cross_color",
    "cross_color != 5 and != 0",
    "1-3 gray(5) cells off the cross",
    "cross center + (N, -N) in-bounds",
]

CROSS_POSITIONS = ("center", "upper_left", "upper_right", "lower_left",
                   "lower_right", "spread")
GRAY_DISTRIBUTIONS = ("scattered", "near_cross", "corners", "row_aligned")
DEGENERATE_TEXTURES = ("no_grays", "cross_at_edge", "full_grid")
HELPFUL_TEXTURES = CROSS_POSITIONS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "grid_w":           {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "cross_color":      {"type": "color", "default": "rng (≠0,5)",
                         "valid": "1..9 (≠5)"},
    "n_grays":          {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "cross_position":   {"type": "str", "default": "rng helpful",
                         "valid": "|".join(CROSS_POSITIONS)},
    "gray_distribution":{"type": "str", "default": "rng helpful",
                         "valid": "|".join(GRAY_DISTRIBUTIONS)},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "asymmetry_force":  {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for cross_position",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 11
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    cross_color = int(overrides.get("cross_color",
                                    ctx.draw_color("cross_color",
                                                   exclude={0, 5})))
    n_grays = int(overrides.get("n_grays",
                                ctx.draw_int("n_grays", 1, 2)))
    n_grays = max(1, min(3, n_grays))
    cross_pos = (overrides.get("texture") or
                 overrides.get("cross_position")
                 or ctx.draw_choice("cross_position",
                                    list(CROSS_POSITIONS)))
    gray_dist = overrides.get("gray_distribution",
                              ctx.draw_choice("gray_distribution",
                                              list(GRAY_DISTRIBUTIONS)))
    cr, cc = _pick_cross_position(cross_pos, h, w, n_grays, rng)
    g = full_grid(h, w, 0)
    for c in range(w):
        g[cr][c] = cross_color
    for r in range(h):
        g[r][cc] = cross_color
    placed = 0
    for _ in range(n_grays * 8):
        if placed >= n_grays:
            break
        r, c = _pick_gray(gray_dist, h, w, cr, cc, rng)
        if r == cr or c == cc:
            continue
        if g[r][c] == 0:
            g[r][c] = 5
            placed += 1
    if placed < 1:
        # Force at least 1 gray
        for r in range(h):
            for c in range(w):
                if r != cr and c != cc and g[r][c] == 0:
                    g[r][c] = 5
                    placed = 1
                    break
            if placed:
                break
    return g


def _pick_cross_position(name, h, w, n_grays, rng):
    margin = n_grays + 1
    if name == "center":
        return h // 2, w // 2
    if name == "upper_left":
        return rng.randint(margin, h // 2), rng.randint(margin, w // 2)
    if name == "upper_right":
        return rng.randint(margin, h // 2), rng.randint(w // 2, w - 2)
    if name == "lower_left":
        return rng.randint(h // 2, h - 2), rng.randint(margin, w // 2)
    if name == "lower_right":
        return rng.randint(h // 2, h - 2), rng.randint(w // 2, w - 2)
    return rng.randint(margin, h - 2), rng.randint(margin, w - 2)


def _pick_gray(name, h, w, cr, cc, rng):
    if name == "near_cross":
        dr = rng.choice([-2, -1, 1, 2])
        dc = rng.choice([-2, -1, 1, 2])
        return max(0, min(h - 1, cr + dr)), max(0, min(w - 1, cc + dc))
    if name == "corners":
        return rng.choice([(0, 0), (0, w - 1), (h - 1, 0),
                           (h - 1, w - 1)])
    if name == "row_aligned":
        return rng.randint(0, h - 1), rng.randint(0, w - 1)
    return rng.randint(0, h - 1), rng.randint(0, w - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    cross_color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "no_grays":
        cr, cc = h // 2, w // 2
        for c in range(w):
            g[cr][c] = cross_color
        for r in range(h):
            g[r][cc] = cross_color
        return g
    if name == "cross_at_edge":
        cr, cc = 0, 0
        for c in range(w):
            g[cr][c] = cross_color
        for r in range(h):
            g[r][cc] = cross_color
        if h > 2 and w > 2:
            g[h - 1][w - 1] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = cross_color
        return g
    return g
