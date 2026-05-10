"""Generator for puzzle aaef0977.

Rule: bg = mode. Seed = first non-bg cell. Color every cell by
Manhattan distance from seed, using fixed 9-color cycle starting from
seed's color.

Combinatorial axes (8): grid_h/w, bg_color, seed_color, seed_position,
position_bias, n_decoy_pixels, edge_avoidance, anchor_corner.
Degenerates: no_seed, multiple_seeds, full_grid_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "891a82451a8a"
VERSION = "1.1.0"
TASK_ID = "891a82451a8a"
SUMMARY = "Single non-bg seed; rule colors by Manhattan distance via fixed cycle."

INVARIANTS = [
    "exactly one non-bg cell (the seed)",
    "bg is most-common color (mode)",
    "seed color is in the cycle {0, 5, 2, 8, 9, 6, 1, 3, 4}",
    "bg is in the same cycle (so start-index lookup is valid)",
]

POSITION_BIAS = ("center", "spread", "edge", "corners")
DEGENERATE_TEXTURES = ("no_seed", "multiple_seeds", "full_grid_seed")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "grid_w":           {"type": "int", "default": "rng 6..14", "valid": "4..18"},
    "bg_color":         {"type": "color", "default": "rng cycle",
                         "valid": "0,1,5,8"},
    "seed_color":       {"type": "color", "default": "rng cycle (≠bg)",
                         "valid": "cycle"},
    "seed_position_bias": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(POSITION_BIAS)},
    "edge_avoidance":   {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "include_decoy_seeds": {"type": "bool", "default": "false",
                            "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for seed_position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 6, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    cycle = [0, 5, 2, 8, 9, 6, 1, 3, 4]
    bg = int(overrides.get("bg_color", rng.choice([0, 1, 5, 8])))
    if bg not in cycle:
        bg = 0
    seed_options = [c for c in cycle if c != bg]
    seed_color = int(overrides.get("seed_color", rng.choice(seed_options)))
    if seed_color == bg or seed_color not in cycle:
        seed_color = seed_options[0]
    pos_bias = (overrides.get("texture") or
                overrides.get("seed_position_bias")
                or ctx.draw_choice("seed_position_bias",
                                   list(POSITION_BIAS)))
    edge_avoid = bool(overrides.get("edge_avoidance", False))
    inset = 1 if edge_avoid else 0
    rmin, rmax = inset, h - 1 - inset
    cmin, cmax = inset, w - 1 - inset
    if rmax < rmin: rmin, rmax = 0, h - 1
    if cmax < cmin: cmin, cmax = 0, w - 1
    g = full_grid(h, w, bg)
    if pos_bias == "center":
        sr, sc = (rmin + rmax) // 2, (cmin + cmax) // 2
    elif pos_bias == "edge":
        sr = rng.choice([rmin, rmax])
        sc = rng.randint(cmin, cmax)
    elif pos_bias == "corners":
        sr, sc = rng.choice([(rmin, cmin), (rmin, cmax),
                             (rmax, cmin), (rmax, cmax)])
    else:
        sr = rng.randint(rmin, rmax)
        sc = rng.randint(cmin, cmax)
    g[sr][sc] = seed_color
    return g


def _draw_from_degenerate(name, h, w, rng):
    bg = rng.choice([0, 1, 5, 8])
    cycle = [0, 5, 2, 8, 9, 6, 1, 3, 4]
    seed_color = rng.choice([c for c in cycle if c != bg])
    g = full_grid(h, w, bg)
    if name == "no_seed":
        return g
    if name == "multiple_seeds":
        g[1][1] = seed_color
        g[h - 2][w - 2] = seed_color
        return g
    if name == "full_grid_seed":
        for r in range(h):
            for c in range(w):
                g[r][c] = seed_color
        return g
    return g
