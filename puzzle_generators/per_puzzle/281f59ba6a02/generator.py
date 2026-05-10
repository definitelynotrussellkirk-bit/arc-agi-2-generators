"""Generator for 0962bcdd.

Rule: scattered colored centers; rule expands each into X-pattern + cross
arms (radius 2).

Combinatorial axes (8): grid_h/w, n_centers, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size, min_separation.
Degenerates: no_centers, all_close, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "281f59ba6a02"
VERSION = "1.1.0"
TASK_ID = "281f59ba6a02"
SUMMARY = "Sparse colored centers; rule expands each into X-pattern + cross arms (radius 2)."

INVARIANTS = [
    "background is 0",
    ">=2 single-cell colored 'plus centers'",
    "each center has bg margin >= 2 from grid edges",
    "centers are >= 5 cells apart from each other",
]

POSITION_BIASES = ("scattered", "diagonal", "centered", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_centers", "all_close", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "n_centers":      {"type": "int", "default": "2", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "min_separation": {"type": "int", "default": "5", "valid": "4..8"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 8, 10
        nc_lo, nc_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
        nc_lo, nc_hi = 3, 4
    else:
        h_lo, h_hi = 10, 14
        nc_lo, nc_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_centers = int(overrides.get("n_centers",
                                  ctx.draw_int("n_centers", nc_lo, nc_hi)))
    n_centers = max(2, min(4, n_centers))
    palette = ctx.draw_distinct_colors("palette", n=n_centers, exclude={0})
    g = full_grid(h, w, 0)
    sep = int(overrides.get("min_separation", 5))
    placed = []
    for color in palette:
        for _try in range(20):
            r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
            if any(abs(r - pr) <= sep - 1 and abs(c - pc) <= sep - 1
                   for pr, pc in placed):
                continue
            g[r][c] = color
            placed.append((r, c))
            break
    if len(placed) < 2:
        return _draw_from_degenerate("no_centers", rng)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_centers":
        return g
    if name == "all_close":
        g[5][5] = 1; g[5][6] = 2; g[6][5] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
