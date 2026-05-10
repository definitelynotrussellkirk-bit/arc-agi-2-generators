"""Generator for b6afb2da.

Rule: solid 5-block; cells get corner=1, edge=4, interior=2 by 5-neighbor count.

Combinatorial axes (8): grid_h/w, n_rects, rect_size_kind,
position_bias, n_decoys, decoy_palette_kind, inter_rect_margin,
asymmetry_force.
Degenerates: no_rects, single_2x2, all_5s.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "22d1f016cb3d"
VERSION = "1.1.0"
TASK_ID = "22d1f016cb3d"
SUMMARY = "Solid 5-rect ≥3×3; rule paints corner=1, edge=4, interior=2."

INVARIANTS = [
    "background is 0",
    ">=1 solid 5-rectangle of side >=3 (so all 3 zones exist)",
    "rectangles don't touch (4-conn separation)",
    "no colors 1, 2, 4 in input (rule writes them for output)",
]

RECT_SIZE_KINDS = ("small", "medium", "large", "wide", "tall")
DEGENERATE_TEXTURES = ("no_rects", "single_2x2", "all_5s")
HELPFUL_TEXTURES = RECT_SIZE_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 7..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "n_rects":            {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "rect_size_kind":     {"type": "str", "default": "rng helpful",
                           "valid": "|".join(RECT_SIZE_KINDS)},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "n_decoys":           {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "decoy_palette_kind": {"type": "str", "default": "rng warm|cool|broad",
                           "valid": "warm|cool|broad"},
    "inter_rect_margin":  {"type": "int", "default": "1", "valid": "1..3"},
    "texture":            {"type": "str", "default": "alias for rect_size_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 8, 6, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 17, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 7, 14, 8, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_rects = int(overrides.get("n_rects",
                                ctx.draw_int("n_rects", 1, 3)))
    n_rects = max(1, min(5, n_rects))
    size_kind = (overrides.get("texture") or
                 overrides.get("rect_size_kind")
                 or ctx.draw_choice("rect_size_kind",
                                    list(RECT_SIZE_KINDS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["spread", "center", "edge"]))
    margin = int(overrides.get("inter_rect_margin", 1))
    decoy_kind = overrides.get("decoy_palette_kind",
                               ctx.draw_choice("decoy_palette_kind",
                                               ["warm", "cool", "broad"]))
    if decoy_kind == "warm":
        decoy_pool = [3, 6, 9]
    elif decoy_kind == "cool":
        decoy_pool = [7, 8]
    else:
        decoy_pool = [3, 6, 7, 8, 9]
    g = full_grid(h, w, 0)
    placed = []
    for _ in range(n_rects * 5):
        if len(placed) >= n_rects:
            break
        rh, rw = _rect_dims(size_kind, h, w, rng)
        for _try in range(20):
            r0, c0 = _pick_pos(bias, h, w, rh, rw, rng)
            if r0 < 0 or c0 < 0 or r0 + rh > h or c0 + rw > w:
                continue
            ok = all(not _overlaps(r0, c0, rh, rw, pr, pc, prh, prw, margin)
                     for pr, pc, prh, prw in placed)
            if not ok:
                continue
            draw_rect(g, r0, c0, rh, rw, 5)
            placed.append((r0, c0, rh, rw))
            break
    if not placed:
        if h >= 4 and w >= 4:
            draw_rect(g, 1, 1, 3, 3, 5)
            placed.append((1, 1, 3, 3))
    n_decoys = int(overrides.get("n_decoys",
                                 ctx.draw_int("n_decoys", 1, 3)))
    placed_decoys = 0
    for _ in range(n_decoys * 4):
        if placed_decoys >= n_decoys:
            break
        dr = rng.randint(0, h - 1); dc = rng.randint(0, w - 1)
        if g[dr][dc] == 0:
            g[dr][dc] = rng.choice(decoy_pool)
            placed_decoys += 1
    return g


def _rect_dims(kind, h, w, rng):
    if kind == "small":
        return 3, 3
    if kind == "medium":
        return rng.randint(3, 4), rng.randint(3, 4)
    if kind == "large":
        return rng.randint(4, 6), rng.randint(4, 6)
    if kind == "wide":
        return 3, rng.randint(4, min(7, w - 2))
    if kind == "tall":
        return rng.randint(4, min(7, h - 2)), 3
    return rng.randint(3, 5), rng.randint(3, 5)


def _pick_pos(bias, h, w, rh, rw, rng):
    if bias == "center":
        return max(0, (h - rh) // 2), max(0, (w - rw) // 2)
    if bias == "edge":
        return 0, 0
    return rng.randint(0, h - rh), rng.randint(0, w - rw)


def _overlaps(r1, c1, h1, w1, r2, c2, h2, w2, margin):
    return not (r1 + h1 + margin <= r2 or r2 + h2 + margin <= r1
                or c1 + w1 + margin <= c2 or c2 + w2 + margin <= c1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_rects":
        for _ in range(3):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice([3, 6, 7, 8, 9])
        return g
    if name == "single_2x2":
        if h >= 3 and w >= 3:
            draw_rect(g, 1, 1, 2, 2, 5)
        return g
    if name == "all_5s":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
