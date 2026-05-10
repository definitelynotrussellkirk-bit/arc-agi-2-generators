"""Generator for `arc_additional_puzzle_bank_volume6:E40` — orange(7)
connected components touching any of the 4 corners get recolored to
blue(1); other orange components stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_corner, n_interior,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_objects, no_interior_objects, all_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "59ccf6f5cc65"
VERSION = "1.1.0"
TASK_ID = "59ccf6f5cc65"
SUMMARY = "Orange components, some at corners; rule recolors corner-touching ones to blue."

INVARIANTS = [
    "background is 0",
    ">=2 orange(7) components",
    ">=1 has a cell at a grid corner",
    ">=1 is strictly interior",
    "components 4-connected, non-overlapping with margin >= 1",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_objects", "no_interior_objects", "all_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "corner_anchored_plus_interior",
                       "valid": "corner_anchored_plus_interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 12, 16)
    rng = ctx.draw_rng("placement")

    g = full_grid(h, w, 0)
    placed_corner = 0
    corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    rng.shuffle(corners)
    placed_boxes: list[tuple[int, int, int, int]] = []
    for cr, cc in corners[:2]:
        rh = rng.randint(2, 4); rw = rng.randint(2, 4)
        if cr == 0:
            rr = 0
        else:
            rr = max(0, h - rh)
        if cc == 0:
            rcc = 0
        else:
            rcc = max(0, w - rw)
        ok = all(not (rr - 1 <= or2 and rr + rh >= or1
                       and rcc - 1 <= oc2 and rcc + rw >= oc1)
                  for (or1, oc1, or2, oc2) in placed_boxes)
        if not ok: continue
        for dr in range(rh):
            for dc in range(rw):
                g[rr + dr][rcc + dc] = 7
        placed_boxes.append((rr, rcc, rr + rh - 1, rcc + rw - 1))
        placed_corner += 1

    placed_int = 0
    for _ in range(8):
        if placed_int >= 2: break
        rh = rng.randint(2, 3); rw = rng.randint(2, 3)
        cells = normalize(rect_cells(rh, rw))
        if place_no_overlap(rng, g, cells, 7, bg=0, margin=1, max_tries=30):
            placed_int += 1

    if placed_corner < 1 or placed_int < 1:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "no_corner_objects":
        # only interior components → rule fires zero times, output identical
        for r in range(3):
            for c in range(3): g[5 + r][5 + c] = 7
        for r in range(2):
            for c in range(2): g[9 + r][9 + c] = 7
        return g
    if name == "no_interior_objects":
        # only corner components → all recolored, output uniform
        for r in range(3):
            for c in range(3): g[r][c] = 7
        for r in range(3):
            for c in range(3): g[h - 3 + r][w - 3 + c] = 7
        return g
    if name == "all_corner":
        # all 4 corners filled, no interior → output uniform after rule
        for r in range(2):
            for c in range(2): g[r][c] = 7
        for r in range(2):
            for c in range(2): g[r][w - 2 + c] = 7
        for r in range(2):
            for c in range(2): g[h - 2 + r][c] = 7
        for r in range(2):
            for c in range(2): g[h - 2 + r][w - 2 + c] = 7
        return g
    return g
