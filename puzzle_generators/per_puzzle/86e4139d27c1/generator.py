"""Generator for puzzle e9614598.

Rule: two blue(1) endpoints. Compute midpoint. Place a + (plus) of
green(3) at midpoint and 4 cardinal neighbors.

Combinatorial axes (8): grid_h/w, bg_color, endpoint_separation,
endpoint_orientation, position_bias, n_decoy_cells, decoy_palette_size,
edge_avoidance.
Degenerates: same_position, no_blues, three_blues.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "86e4139d27c1"
VERSION = "1.1.0"
TASK_ID = "86e4139d27c1"
SUMMARY = "Two blue endpoints; rule paints + (plus) at midpoint with 3."

INVARIANTS = [
    "bg != 3 and != 1",
    "exactly 2 blue(1) cells",
    "midpoint mr, mc has 4 cardinal neighbors all in-bounds",
    "no color 3 in input (rule writes 3 for output)",
]

ENDPOINT_ORIENTATIONS = ("same_row", "same_col", "diag", "anti_diag", "free")
POSITION_BIAS = ("center", "spread", "edge")
DEGENERATE_TEXTURES = ("same_position", "no_blues", "three_blues")
HELPFUL_TEXTURES = ENDPOINT_ORIENTATIONS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "grid_w":              {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "bg_color":            {"type": "color", "default": "rng (≠0,1,3)",
                            "valid": "0..9 (≠1,3)"},
    "endpoint_separation": {"type": "str", "default": "rng near|medium|far",
                            "valid": "near|medium|far"},
    "endpoint_orientation": {"type": "str", "default": "rng helpful",
                             "valid": "|".join(ENDPOINT_ORIENTATIONS)},
    "position_bias":       {"type": "str", "default": "rng center|spread|edge",
                            "valid": "center|spread|edge"},
    "n_decoy_cells":       {"type": "int", "default": "0", "valid": "0..3"},
    "edge_avoidance":      {"type": "bool", "default": "true",
                            "valid": "true|false"},
    "texture":             {"type": "str", "default": "alias for endpoint_orientation",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 6, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bgc = int(overrides.get("bg_color",
                            ctx.draw_color("bg_color", exclude={1, 3})))
    orient = (overrides.get("texture") or
              overrides.get("endpoint_orientation")
              or ctx.draw_choice("endpoint_orientation",
                                 list(ENDPOINT_ORIENTATIONS)))
    sep = overrides.get("endpoint_separation",
                        ctx.draw_choice("endpoint_separation",
                                        ["near", "medium", "far"]))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["center", "spread", "edge"]))
    edge_avoid = bool(overrides.get("edge_avoidance", True))
    inset = 1 if edge_avoid else 0
    rmin = inset; rmax = h - 1 - inset
    cmin = inset; cmax = w - 1 - inset
    g = full_grid(h, w, bgc)
    p1, p2 = _draw_endpoints(orient, sep, bias, rmin, rmax, cmin, cmax, rng)
    g[p1[0]][p1[1]] = 1
    g[p2[0]][p2[1]] = 1
    mr = (p1[0] + p2[0]) // 2
    mc = (p1[1] + p2[1]) // 2
    if not (0 < mr < h - 1 and 0 < mc < w - 1):
        # Force midpoint to have all 4 cardinal neighbors
        mr = max(1, min(h - 2, mr))
        mc = max(1, min(w - 2, mc))
        # Re-place endpoints: use simple horizontal pair around the midpoint
        g = full_grid(h, w, bgc)
        target_dist = max(2, min(w - 1, w - 2))
        c1 = max(0, mc - target_dist // 2)
        c2 = min(w - 1, mc + target_dist // 2)
        g[mr][c1] = 1
        g[mr][c2] = 1
    return g


def _draw_endpoints(orient, sep, bias, rmin, rmax, cmin, cmax, rng):
    target_dist = {"near": 4, "medium": 6, "far": 10}.get(sep, 4)
    if orient == "same_row":
        if bias == "center":
            r = (rmin + rmax) // 2
            c1 = max(cmin, (cmin + cmax - target_dist) // 2)
            c2 = min(cmax, c1 + target_dist)
            return (r, c1), (r, c2)
        r = rng.randint(rmin, rmax)
        c1 = rng.randint(cmin, max(cmin, cmax - target_dist))
        c2 = min(cmax, c1 + target_dist)
        return (r, c1), (r, c2)
    if orient == "same_col":
        c = rng.randint(cmin, cmax)
        r1 = rng.randint(rmin, max(rmin, rmax - target_dist))
        r2 = min(rmax, r1 + target_dist)
        return (r1, c), (r2, c)
    if orient == "diag":
        d = min(target_dist, rmax - rmin, cmax - cmin)
        r1 = rng.randint(rmin, max(rmin, rmax - d))
        c1 = rng.randint(cmin, max(cmin, cmax - d))
        return (r1, c1), (r1 + d, c1 + d)
    if orient == "anti_diag":
        d = min(target_dist, rmax - rmin, cmax - cmin)
        r1 = rng.randint(rmin, max(rmin, rmax - d))
        c1 = rng.randint(cmin + d, cmax)
        return (r1, c1), (r1 + d, c1 - d)
    for _ in range(20):
        p1 = (rng.randint(rmin, rmax), rng.randint(cmin, cmax))
        p2 = (rng.randint(rmin, rmax), rng.randint(cmin, cmax))
        mr = (p1[0] + p2[0]) // 2
        mc = (p1[1] + p2[1]) // 2
        if 0 < mr < rmax and 0 < mc < cmax and abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) >= 2:
            return p1, p2
    return ((rmin, cmin), (rmax, cmax))


def _draw_from_degenerate(name, h, w, rng):
    bgc = rng.choice([0, 2, 4, 5, 6, 7, 8, 9])
    g = full_grid(h, w, bgc)
    if name == "same_position":
        g[h // 2][w // 2] = 1
        return g
    if name == "no_blues":
        return g
    if name == "three_blues":
        g[1][1] = 1
        g[h - 2][1] = 1
        g[h - 2][w - 2] = 1
        return g
    return g
