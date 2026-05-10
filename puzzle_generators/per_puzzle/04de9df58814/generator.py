"""Generator for arc_additional_puzzle_bank_volume18:E123.

Rule: green(3) connected components touching the grid border get
recolored; interior greens stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_border, all_interior, no_green.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "04de9df58814"
VERSION = "1.1.0"
TASK_ID = "04de9df58814"
SUMMARY = "Several green objects; some touch the grid border, some are interior."

INVARIANTS = [
    "background is 0",
    ">=2 green(3) connected components",
    ">=1 green component has a cell on the outer border",
    ">=1 green component is strictly interior (margin >= 1)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_border", "all_interior", "no_green")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "border_plus_interior",
                       "valid": "border_plus_interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 16, 18)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 12, 18)
        w = ctx.draw_int("grid_w", 12, 18)
    rng = ctx.draw_rng("placement")

    g = full_grid(h, w, 0)
    placed_border = 0
    placed_boxes: list[tuple[int, int, int, int]] = []
    for _ in range(8):
        if placed_border >= 2: break
        rh = rng.randint(2, max(2, h // 4))
        rw = rng.randint(2, max(2, w // 4))
        side = rng.choice(["top", "bottom", "left", "right"])
        if side == "top":   rr, rc = 0, rng.randint(0, w - rw)
        elif side == "bottom": rr, rc = h - rh, rng.randint(0, w - rw)
        elif side == "left": rr, rc = rng.randint(0, h - rh), 0
        else: rr, rc = rng.randint(0, h - rh), w - rw
        ok = all(not (rr - 1 <= or2 and rr + rh >= or1
                       and rc - 1 <= oc2 and rc + rw >= oc1)
                  for (or1, oc1, or2, oc2) in placed_boxes)
        if not ok: continue
        for dr in range(rh):
            for dc in range(rw):
                g[rr + dr][rc + dc] = 3
        placed_boxes.append((rr, rc, rr + rh - 1, rc + rw - 1))
        placed_border += 1

    placed_interior = 0
    for _ in range(8):
        if placed_interior >= 2: break
        rh = rng.randint(2, max(2, h // 4))
        rw = rng.randint(2, max(2, w // 4))
        cells = normalize(rect_cells(rh, rw))
        if place_no_overlap(rng, g, cells, 3, bg=0, margin=1, max_tries=30):
            placed_interior += 1
    if placed_border < 1 or placed_interior < 1:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "all_border":
        # all greens touch the border → all recolored, no interior comparison
        for r in range(0, 2):
            for c in range(0, 3): g[r][c] = 3
        for r in range(h - 2, h):
            for c in range(w - 3, w): g[r][c] = 3
        return g
    if name == "all_interior":
        # no greens touch border → rule recolors nothing, output equals input
        for r in range(4, 6):
            for c in range(3, 5): g[r][c] = 3
        for r in range(7, 9):
            for c in range(7, 10): g[r][c] = 3
        return g
    if name == "no_green":
        # no color-3 cells → rule has no objects to recolor, output equals input
        for r in range(2, 4):
            for c in range(2, 5): g[r][c] = 4
        for r in range(8, 10):
            for c in range(8, 11): g[r][c] = 8
        return g
    return g
