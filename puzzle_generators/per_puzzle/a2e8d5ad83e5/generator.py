"""Generator for puzzle e9bb6954.

Rule: multiple solid filled squares. Output draws row+col cross from
each square's center in that square's color; intersections of distinct
colors become 0.

Combinatorial axes (8): grid_h/w, n_squares, sq_size_min, sq_size_max,
palette_kind, position_bias, anchor_corner, asymmetry_force.
Degenerates: single_square, overlapping, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "a2e8d5ad83e5"
VERSION = "1.1.0"
TASK_ID = "a2e8d5ad83e5"
SUMMARY = "Filled squares; rule draws crosses from their centers."

INVARIANTS = [
    "background is 0",
    ">=2 solid filled squares",
    "squares use distinct colors",
    "squares non-overlapping with margin >=2",
]

POSITION_BIASES = ("scattered", "corners", "diagonal", "row_aligned",
                   "col_aligned")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_square", "overlapping", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "grid_w":         {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "n_squares":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "sq_size_min":    {"type": "int", "default": "2", "valid": "2..4"},
    "sq_size_max":    {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
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
        h_lo, h_hi = 12, 14
    elif difficulty == "hard":
        h_lo, h_hi = 18, 24
    else:
        h_lo, h_hi = 14, 20
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_squares = int(overrides.get("n_squares",
                                  ctx.draw_int("n_squares", 2, 3)))
    n_squares = max(2, min(4, n_squares))
    s_min = int(overrides.get("sq_size_min", 2))
    s_max = int(overrides.get("sq_size_max",
                              ctx.draw_int("sq_size_max", 3, 4)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    palette = _build_palette(palette_kind, n_squares, rng)
    g = full_grid(h, w, 0)
    placed = 0
    placed_boxes = []
    for color in palette:
        for _ in range(40):
            sz = rng.randint(s_min, s_max)
            rr, rc = _pick_position(bias, h, w, sz, placed, rng)
            if rr is None:
                continue
            ok = all(not (rr - 2 <= or2 and rr + sz + 1 >= or1
                          and rc - 2 <= oc2 and rc + sz + 1 >= oc1)
                     for (or1, oc1, or2, oc2) in placed_boxes)
            if not ok:
                continue
            draw_rect(g, rr, rc, sz, sz, color)
            placed_boxes.append((rr, rc, rr + sz - 1, rc + sz - 1))
            placed += 1
            break
    if placed < 2:
        # Fallback: place 2 in opposite corners
        if not placed_boxes:
            draw_rect(g, 2, 2, 2, 2, palette[0])
        draw_rect(g, h - 4, w - 4, 2, 2,
                  palette[1] if len(palette) > 1 else palette[0])
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
    while len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _pick_position(bias, h, w, sz, idx, rng):
    if h - sz - 2 < 2 or w - sz - 2 < 2:
        return None, None
    if bias == "corners":
        corners = [(2, 2), (2, w - sz - 2), (h - sz - 2, 2),
                   (h - sz - 2, w - sz - 2)]
        return corners[idx % 4]
    if bias == "diagonal":
        rr = 2 + idx * 4; rc = 2 + idx * 4
        if rr + sz > h - 2 or rc + sz > w - 2:
            return rng.randint(2, h - sz - 2), rng.randint(2, w - sz - 2)
        return rr, rc
    if bias == "row_aligned":
        rr = max(2, (h - sz) // 2)
        rc = 2 + idx * 4
        if rc + sz > w - 2:
            rc = rng.randint(2, w - sz - 2)
        return rr, rc
    if bias == "col_aligned":
        rr = 2 + idx * 4
        if rr + sz > h - 2:
            rr = rng.randint(2, h - sz - 2)
        return rr, max(2, (w - sz) // 2)
    return rng.randint(2, h - sz - 2), rng.randint(2, w - sz - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_square":
        draw_rect(g, h // 2, w // 2, 2, 2, 3)
        return g
    if name == "overlapping":
        draw_rect(g, 3, 3, 3, 3, 3)
        draw_rect(g, 4, 4, 3, 3, 4)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 4
        return g
    return g
