"""Generator for ARC task b15fca0b.

Rule: two color-2 endpoints on an empty grid; rule fills the shortest
path between them with 4 (endpoints stay color 2).

Combinatorial axes (8): grid_h/w, endpoint_separation, endpoint_layout,
decoy_palette_size, decoy_density, edge_avoidance, manhattan_min,
manhattan_max.
Degenerates: adjacent_endpoints, same_row, same_column.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e78f94d8f5bc"
VERSION = "1.1.0"
TASK_ID = "e78f94d8f5bc"
SUMMARY = "Two color-2 endpoints; rule fills the shortest path between them with 4."

INVARIANTS = [
    "background is 0",
    "exactly two color-2 endpoints",
    "endpoints have Manhattan distance >= 3 (so path is visible)",
    "no other color-2 cells anywhere on the grid",
]

ENDPOINT_LAYOUTS = ("opposite_corners", "diagonal", "near_corners",
                    "spread", "random")
DEGENERATE_TEXTURES = ("adjacent_endpoints", "same_row", "same_column")
HELPFUL_TEXTURES = ENDPOINT_LAYOUTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 5..12", "valid": "3..16"},
    "grid_w":             {"type": "int", "default": "rng 5..12", "valid": "3..16"},
    "endpoint_separation": {"type": "str", "default": "rng near|medium|far",
                            "valid": "near|medium|far"},
    "endpoint_layout":    {"type": "str", "default": "rng helpful",
                           "valid": "|".join(ENDPOINT_LAYOUTS)},
    "edge_avoidance":     {"type": "bool", "default": "false", "valid": "true|false"},
    "decoy_palette_size": {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "decoy_density":      {"type": "float", "default": "rng 0..0.05",
                           "valid": "0..0.15"},
    "manhattan_min":      {"type": "int", "default": "rng 3..5", "valid": "3..10"},
    "texture":            {"type": "str", "default": "alias for endpoint_layout",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 5, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("points")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    layout = (overrides.get("texture") or overrides.get("endpoint_layout")
              or ctx.draw_choice("endpoint_layout", list(ENDPOINT_LAYOUTS)))
    sep = overrides.get("endpoint_separation",
                        ctx.draw_choice("endpoint_separation",
                                        ["near", "medium", "far"]))
    edge_avoid = bool(overrides.get("edge_avoidance", False))
    md_min = int(overrides.get("manhattan_min",
                               ctx.draw_int("manhattan_min", 3, 5)))
    md_min = max(3, min(h + w - 2, md_min))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 2)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.05)))
    g = full_grid(h, w, 0)
    p1, p2 = _draw_endpoints(layout, sep, h, w, md_min, edge_avoid, rng)
    g[p1[0]][p1[1]] = 2
    g[p2[0]][p2[1]] = 2
    decoy_pool = [c for c in range(1, 10) if c not in (0, 2, 4)]
    rng.shuffle(decoy_pool)
    decoy_palette = decoy_pool[:max(0, n_decoy)]
    if decoy_palette and decoy_d > 0:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 0 and rng.random() < decoy_d:
                    g[r][c] = rng.choice(decoy_palette)
    return g


def _draw_endpoints(layout, sep, h, w, md_min, edge_avoid, rng):
    inset = 1 if edge_avoid else 0
    rmin, rmax = inset, h - 1 - inset
    cmin, cmax = inset, w - 1 - inset
    if rmax <= rmin: rmin, rmax = 0, h - 1
    if cmax <= cmin: cmin, cmax = 0, w - 1
    if layout == "opposite_corners":
        return ((rmin, cmin), (rmax, cmax))
    if layout == "diagonal":
        return ((rmin, cmax), (rmax, cmin))
    if layout == "near_corners":
        choices = [(rmin, cmin), (rmin, cmax), (rmax, cmin), (rmax, cmax)]
        a, b = rng.sample(choices, 2)
        return (a, b)
    if layout == "spread":
        target = {"near": md_min,
                  "medium": (h + w) // 2,
                  "far": h + w - 2}.get(sep, md_min)
        for _ in range(80):
            p1 = (rng.randint(rmin, rmax), rng.randint(cmin, cmax))
            p2 = (rng.randint(rmin, rmax), rng.randint(cmin, cmax))
            if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) >= target:
                return p1, p2
    for _ in range(80):
        p1 = (rng.randint(rmin, rmax), rng.randint(cmin, cmax))
        p2 = (rng.randint(rmin, rmax), rng.randint(cmin, cmax))
        if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) >= md_min:
            return p1, p2
    return ((rmin, cmin), (rmax, cmax))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "adjacent_endpoints":
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 2)
        g[r][c] = 2; g[r][c + 1] = 2
        return g
    if name == "same_row":
        r = rng.randint(0, h - 1)
        g[r][0] = 2; g[r][w - 1] = 2
        return g
    if name == "same_column":
        c = rng.randint(0, w - 1)
        g[0][c] = 2; g[h - 1][c] = 2
        return g
    return g
