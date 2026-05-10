"""Generator for puzzle a2fd1cf0.

Rule: 1 red(2) cell + 1 green(3) cell at distinct rows/cols. Output
draws an L-path of 8s connecting them.

Combinatorial axes (8): grid_h/w, distance_kind, quadrant_bias,
red_position, green_position, anchor_corner, asymmetry_force,
include_decoy.
Degenerates: same_row, same_col, same_position.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "563e1df172df"
VERSION = "1.1.0"
TASK_ID = "563e1df172df"
SUMMARY = "Red + green at distinct rows/cols; rule draws L-path of 8s."

INVARIANTS = [
    "background is 0",
    "exactly 1 red(2) cell, 1 green(3) cell",
    "red and green at different rows AND different cols",
    "no other non-bg cells (rule writes 8 for path)",
]

DISTANCE_KINDS = ("near", "medium", "far", "diagonal", "knight")
QUADRANT_BIASES = ("opposite", "same_corner", "spread", "edges")
DEGENERATE_TEXTURES = ("same_row", "same_col", "same_position")
HELPFUL_TEXTURES = DISTANCE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "distance_kind":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DISTANCE_KINDS)},
    "quadrant_bias":  {"type": "str", "default": "rng",
                       "valid": "|".join(QUADRANT_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "min_dist":       {"type": "int", "default": "2", "valid": "1..6"},
    "max_dist":       {"type": "int", "default": "min(h,w)-2",
                       "valid": "2..max"},
    "texture":        {"type": "str", "default": "alias for distance_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    distance = (overrides.get("texture") or
                overrides.get("distance_kind")
                or ctx.draw_choice("distance_kind",
                                   list(DISTANCE_KINDS)))
    quadrant = overrides.get("quadrant_bias",
                             ctx.draw_choice("quadrant_bias",
                                             list(QUADRANT_BIASES)))
    g = full_grid(h, w, 0)
    rr, rc, gr, gc = _pick_endpoints(distance, quadrant, h, w, rng)
    g[rr][rc] = 2
    g[gr][gc] = 3
    return g


def _pick_endpoints(distance, quadrant, h, w, rng):
    if quadrant == "opposite":
        rr = rng.randint(0, h // 2 - 1) if h > 2 else 0
        rc = rng.randint(0, w // 2 - 1) if w > 2 else 0
        gr = rng.randint(h // 2, h - 1)
        gc = rng.randint(w // 2, w - 1)
        return rr, rc, gr, gc
    if quadrant == "same_corner":
        rr = rng.randint(0, h // 3) if h > 3 else 0
        rc = rng.randint(0, w // 3) if w > 3 else 0
        for _ in range(20):
            gr = rng.randint(0, h // 2)
            gc = rng.randint(0, w // 2)
            if gr != rr and gc != rc:
                return rr, rc, gr, gc
    if quadrant == "edges":
        rr = rng.choice([0, h - 1])
        rc = rng.randint(1, max(1, w - 2))
        for _ in range(20):
            gr = rng.choice([0, h - 1])
            gc = rng.randint(1, max(1, w - 2))
            if gr != rr and gc != rc:
                return rr, rc, gr, gc
    target = {"near": 3, "medium": 5, "far": 8,
              "diagonal": min(h, w) - 1, "knight": 2}.get(distance, 4)
    for _ in range(40):
        rr = rng.randint(0, h - 1); rc = rng.randint(0, w - 1)
        gr = rng.randint(0, h - 1); gc = rng.randint(0, w - 1)
        if gr == rr or gc == rc:
            continue
        d = abs(gr - rr) + abs(gc - rc)
        if abs(d - target) <= 2:
            return rr, rc, gr, gc
    return 0, 0, h - 1, w - 1


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_row":
        r = h // 2
        c1 = rng.randint(0, w // 2 - 1)
        c2 = rng.randint(w // 2, w - 1)
        g[r][c1] = 2
        g[r][c2] = 3
        return g
    if name == "same_col":
        c = w // 2
        r1 = rng.randint(0, h // 2 - 1)
        r2 = rng.randint(h // 2, h - 1)
        g[r1][c] = 2
        g[r2][c] = 3
        return g
    if name == "same_position":
        # Only one cell can be one color
        g[h // 2][w // 2] = 2
        return g
    return g
