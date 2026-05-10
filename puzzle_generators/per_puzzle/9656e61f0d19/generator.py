"""Generator for 9f5f939b.

Rule: cyan center becomes yellow only when equidistant rays hit
correctly oriented blue bars.

Combinatorial axes (8): distance, palette_kind, position_bias,
anchor_corner, asymmetry_force, palette_size, n_centers, bar_orientation.
Degenerates: no_bars, no_center, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9656e61f0d19"
VERSION = "1.1.0"
TASK_ID = "9656e61f0d19"
SUMMARY = "Cyan center becomes yellow only when equidistant rays hit oriented blue bars."

INVARIANTS = [
    "background is color 0",
    "candidate centers use color 8",
    "blue bars use color 1",
    "vertical rays must hit vertical bars and horizontal rays must hit horizontal bars at the same distance",
]

DEGENERATE_TEXTURES = ("no_bars", "no_center", "full_grid")
HELPFUL_TEXTURES = ("close", "mid", "far")

AXES = {
    "distance":       {"type": "int", "default": "rng 2..3", "valid": "2..8"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "centered|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "n_centers":      {"type": "int", "default": "1", "valid": "1"},
    "bar_orientation":{"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for distance",
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
        d_lo, d_hi = 2, 3
    elif difficulty == "hard":
        d_lo, d_hi = 4, 8
    else:
        d_lo, d_hi = 2, 5
    if overrides.get("texture") == "close":
        dist = 2
    elif overrides.get("texture") == "mid":
        dist = 3
    elif overrides.get("texture") == "far":
        dist = rng.randint(5, 7)
    else:
        dist = ctx.draw_int("distance", d_lo, d_hi)
    dist = max(2, min(8, dist))
    h = 2 * dist + 7
    w = 2 * dist + 7
    r = dist + 3 + rng.randint(0, 1)
    c = dist + 3 + rng.randint(0, 1)
    g = full_grid(h, w, 0)
    g[r][c] = 8
    g[r - dist][c] = 1
    g[r - dist - 1][c] = 1
    g[r + dist][c] = 1
    g[r + dist + 1][c] = 1
    g[r][c - dist] = 1
    g[r][c - dist - 1] = 1
    g[r][c + dist] = 1
    g[r][c + dist + 1] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "no_bars":
        g[6][6] = 8
        return g
    if name == "no_center":
        g[3][6] = 1; g[9][6] = 1
        g[6][3] = 1; g[6][9] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
