"""Generator for 21f83797.

Rule: 2 cells of color 2. Output paints full rows r1, r2 and cols c1,
c2 in 2; cells strictly inside the rectangle become 1.

Combinatorial axes (8): grid_h/w, dot_separation, dot_orientation,
position_bias, n_decoys, decoy_palette_size, anchor_corners,
edge_avoidance.
Degenerates: same_row, same_col, single_dot.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "01023c69fe3c"
VERSION = "1.1.0"
TASK_ID = "01023c69fe3c"
SUMMARY = "Two 2-cells; rule paints cross + fills bbox interior with 1."

INVARIANTS = [
    "background is 0",
    "exactly 2 cells of color 2",
    "the 2 cells have distinct rows AND distinct cols",
    "no color 1 in input (rule writes 1 for output)",
]

DOT_ORIENTATIONS = ("diagonal", "anti_diagonal", "spread", "near_corners")
POSITION_BIAS = ("center", "spread", "edge")
DEGENERATE_TEXTURES = ("same_row", "same_col", "single_dot")
HELPFUL_TEXTURES = DOT_ORIENTATIONS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "grid_w":           {"type": "int", "default": "rng 8..16", "valid": "6..20"},
    "dot_orientation":  {"type": "str", "default": "rng helpful",
                         "valid": "|".join(DOT_ORIENTATIONS)},
    "dot_separation":   {"type": "str", "default": "rng near|medium|far",
                         "valid": "near|medium|far"},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIAS)},
    "edge_avoidance":   {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "anchor_corners":   {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "min_distance":     {"type": "int", "default": "2", "valid": "1..h"},
    "texture":          {"type": "str", "default": "alias for dot_orientation",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 8, 6, 10
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 13, 18, 14, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 14, 8, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    orient = (overrides.get("texture") or
              overrides.get("dot_orientation")
              or ctx.draw_choice("dot_orientation",
                                 list(DOT_ORIENTATIONS)))
    sep = overrides.get("dot_separation",
                        ctx.draw_choice("dot_separation",
                                        ["near", "medium", "far"]))
    edge_avoid = bool(overrides.get("edge_avoidance", False))
    inset = 1 if edge_avoid else 0
    rmin, rmax = inset, h - 1 - inset
    cmin, cmax = inset, w - 1 - inset
    if rmax < rmin: rmin, rmax = 0, h - 1
    if cmax < cmin: cmin, cmax = 0, w - 1
    target_dist = {"near": 3, "medium": (h + w) // 3,
                   "far": h + w - 4}.get(sep, 3)
    g = full_grid(h, w, 0)
    if orient == "diagonal":
        d = max(2, min(target_dist, min(rmax - rmin, cmax - cmin)))
        r1 = rng.randint(rmin, max(rmin, rmax - d))
        c1 = rng.randint(cmin, max(cmin, cmax - d))
        g[r1][c1] = 2
        g[r1 + d][c1 + d] = 2
    elif orient == "anti_diagonal":
        d = max(2, min(target_dist, min(rmax - rmin, cmax - cmin)))
        r1 = rng.randint(rmin, max(rmin, rmax - d))
        c1 = rng.randint(cmin + d, cmax)
        g[r1][c1] = 2
        g[r1 + d][c1 - d] = 2
    elif orient == "near_corners":
        choices = [((rmin, cmin), (rmax, cmax)),
                   ((rmin, cmax), (rmax, cmin)),
                   ((rmin + 1, cmin + 1), (rmax - 1, cmax - 1))]
        (r1, c1), (r2, c2) = rng.choice(choices)
        g[r1][c1] = 2
        g[r2][c2] = 2
    else:  # spread
        for _ in range(40):
            r1, r2 = rng.sample(range(rmin, rmax + 1), 2)
            c1, c2 = rng.sample(range(cmin, cmax + 1), 2)
            if abs(r1 - r2) + abs(c1 - c2) >= 2:
                g[r1][c1] = 2
                g[r2][c2] = 2
                break
        else:
            g[rmin][cmin] = 2
            g[rmax][cmax] = 2
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_row":
        r = h // 2
        g[r][1] = 2
        g[r][w - 2] = 2
        return g
    if name == "same_col":
        c = w // 2
        g[1][c] = 2
        g[h - 2][c] = 2
        return g
    if name == "single_dot":
        g[h // 2][w // 2] = 2
        return g
    return g
