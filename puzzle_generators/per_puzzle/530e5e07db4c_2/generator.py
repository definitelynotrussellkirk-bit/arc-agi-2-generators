"""Generator for fc5d964d.

Rule: BFS from 2-seed through cells {2,3,5}; if 3-seed in component,
recolor reached 5-cells to 4. (Same rule as 468bcf25.)

Combinatorial axes (8): grid_h/w, path_orientation, n_isolated_stubs,
seed_2_position, seed_3_position, palette_kind, anchor_corner,
asymmetry_force.
Degenerates: no_path, no_seeds, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "530e5e07db4c_2"
VERSION = "1.1.0"
TASK_ID = "530e5e07db4c_2"
SUMMARY = "5-path connecting 2-seed to 3-seed + isolated 5-stubs."

INVARIANTS = [
    "exactly one 2-seed and one 3-seed",
    "5-cells form a connected path between them",
    "1-2 isolated 5-stubs",
]

PATH_ORIENTATIONS = ("horizontal", "vertical", "L_shape", "diagonal")
DEGENERATE_TEXTURES = ("no_path", "no_seeds", "full_grid")
HELPFUL_TEXTURES = PATH_ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "path_orientation":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATH_ORIENTATIONS)},
    "n_isolated_stubs":{"type": "int", "default": "rng 1..2", "valid": "0..4"},
    "seed_2_position":{"type": "str", "default": "rng",
                       "valid": "tl|tr|bl|br|left|right"},
    "seed_3_position":{"type": "str", "default": "rng",
                       "valid": "tl|tr|bl|br|left|right"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for path_orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 6, 7, 9
        ns_lo, ns_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 12, 14
        ns_lo, ns_hi = 2, 4
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 8, 9, 11
        ns_lo, ns_hi = 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    orient = (overrides.get("texture") or
              overrides.get("path_orientation")
              or ctx.draw_choice("path_orientation",
                                 list(PATH_ORIENTATIONS)))
    if orient == "horizontal":
        r = rng.randint(1, h - 2)
        g[r][1] = 2
        for c in range(2, w - 2):
            g[r][c] = 5
        g[r][w - 2] = 3
    elif orient == "vertical":
        c = rng.randint(1, w - 2)
        g[1][c] = 2
        for r in range(2, h - 2):
            g[r][c] = 5
        g[h - 2][c] = 3
    elif orient == "L_shape":
        r1 = 1; r2 = h - 2; c1 = 1; c2 = w - 2
        g[r1][c1] = 2
        for c in range(c1 + 1, c2):
            g[r1][c] = 5
        for r in range(r1, r2):
            g[r][c2] = 5
        g[r2][c2] = 3
    else:
        r1 = 1; c1 = 1
        steps = min(h, w) - 2
        g[r1][c1] = 2
        cr, cc = r1, c1
        for _ in range(steps - 1):
            cr += 1; cc += 1
            if cr < h - 1 and cc < w - 1:
                g[cr][cc] = 5
        g[h - 2][w - 2] = 3
    n_stubs = int(overrides.get("n_isolated_stubs",
                                ctx.draw_int("n_isolated_stubs",
                                             ns_lo, ns_hi)))
    n_stubs = max(0, min(4, n_stubs))
    for _ in range(n_stubs):
        for _try in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = 5
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_path":
        g[1][1] = 2
        g[1][w - 2] = 3
        return g
    if name == "no_seeds":
        for c in range(2, w - 2):
            g[3][c] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
