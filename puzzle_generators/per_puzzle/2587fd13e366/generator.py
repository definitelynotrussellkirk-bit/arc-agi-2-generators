"""Generator for puzzle 516b51b7.

Rule: solid blue rectangles; rule fills each with concentric red/green
rings (center=blue, dist 1=red, dist 2=green, alternating).

Combinatorial axes (8): grid_h/w, n_rects, rect_size_kind,
position_bias, palette_size, decoy_density, inter_rect_margin,
asymmetry_force.
Degenerates: no_rects, single_small, all_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "2587fd13e366"
VERSION = "1.1.0"
TASK_ID = "2587fd13e366"
SUMMARY = "Solid blue rectangles; rule fills with concentric red/green rings."

INVARIANTS = [
    "background is 0",
    ">=1 solid blue(1) rectangle of dim >=4×4",
    "rectangles non-overlapping with margin >=1",
    "no colors 2 or 3 in input (rule writes them for output)",
]

RECT_SIZE_KINDS = ("small", "medium", "large", "wide", "tall")
DEGENERATE_TEXTURES = ("no_rects", "single_small", "all_overlap")
HELPFUL_TEXTURES = RECT_SIZE_KINDS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":             {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_rects":            {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "rect_size_kind":     {"type": "str", "default": "rng helpful",
                           "valid": "|".join(RECT_SIZE_KINDS)},
    "position_bias":      {"type": "str", "default": "rng spread|center|edge",
                           "valid": "spread|center|edge"},
    "palette_size":       {"type": "int", "default": "1", "valid": "1..3"},
    "inter_rect_margin":  {"type": "int", "default": "1", "valid": "1..3"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for rect_size_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 10, 13
    elif difficulty == "hard":
        h_lo, h_hi = 17, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
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
    g = full_grid(h, w, 0)
    placed = 0
    placed_boxes = []
    for _ in range(n_rects * 5):
        if placed >= n_rects:
            break
        rh, rw = _rect_dims(size_kind, h, w, rng)
        for _try in range(20):
            r0, c0 = _pick_pos(bias, h, w, rh, rw, rng)
            if r0 < 1 or c0 < 1 or r0 + rh > h - 1 or c0 + rw > w - 1:
                continue
            ok = all(not (r0 - margin <= obr2 and r0 + rh + margin >= obr1
                          and c0 - margin <= obc2 and c0 + rw + margin >= obc1)
                     for (obr1, obc1, obr2, obc2) in placed_boxes)
            if not ok:
                continue
            draw_rect(g, r0, c0, rh, rw, 1)
            placed_boxes.append((r0, c0, r0 + rh - 1, c0 + rw - 1))
            placed += 1
            break
    if placed == 0:
        if h >= 6 and w >= 6:
            draw_rect(g, 1, 1, 4, 4, 1)
    return g


def _rect_dims(kind, h, w, rng):
    max_h = max(4, h // 2)
    max_w = max(4, w // 2)
    if kind == "small":
        return 4, 4
    if kind == "medium":
        return rng.randint(4, 5), rng.randint(4, 5)
    if kind == "large":
        return rng.randint(5, 7), rng.randint(5, 7)
    if kind == "wide":
        return 4, rng.randint(5, max_w)
    if kind == "tall":
        return rng.randint(5, max_h), 4
    return rng.randint(4, max_h), rng.randint(4, max_w)


def _pick_pos(bias, h, w, rh, rw, rng):
    if bias == "center":
        return max(1, (h - rh) // 2), max(1, (w - rw) // 2)
    if bias == "edge":
        return 1, 1
    return rng.randint(1, h - rh - 1), rng.randint(1, w - rw - 1)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_rects":
        return g
    if name == "single_small":
        if h >= 4 and w >= 4:
            draw_rect(g, 1, 1, 3, 3, 1)
        return g
    if name == "all_overlap":
        if h >= 6 and w >= 6:
            draw_rect(g, 1, 1, 4, 4, 1)
            draw_rect(g, 2, 2, 4, 4, 1)
        return g
    return g
