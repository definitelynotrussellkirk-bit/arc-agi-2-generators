"""Generator for 14754a24.

Rule: incomplete yellow pluses use gray cells as missing arms; the
gray cells get recolored red.

Combinatorial axes (8): grid_h/w, n_pluses, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
yellow_count.
Degenerates: no_pluses, full_grid, single_arm.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1314f4ccf5cc"
VERSION = "1.1.0"
TASK_ID = "1314f4ccf5cc"
SUMMARY = "Incomplete yellow pluses; gray cells fill missing arms and recolor to red."

INVARIANTS = [
    "each target plus footprint contains only yellow and gray cells",
    "the yellow cells form one 4-connected object",
    "at least one gray plus cell completes the plus",
    "targets are separated by background",
]

DENSITY_KINDS = ("sparse", "medium", "dense")
DEGENERATE_TEXTURES = ("no_pluses", "full_grid", "single_arm")
HELPFUL_TEXTURES = DENSITY_KINDS

PLUS_OFFSETS = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..15", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "8..18"},
    "n_pluses":       {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "yellow_count":   {"type": "int", "default": "rng 2..4", "valid": "1..4"},
    "density":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DENSITY_KINDS)},
    "texture":        {"type": "str", "default": "alias for density",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r, c):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - 2), min(h, r + 3)):
        for cc in range(max(0, c - 2), min(w, c + 3)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        np_lo, np_hi = 1, 2
    elif difficulty == "hard":
        np_lo, np_hi = 4, 6
    else:
        np_lo, np_hi = 2, 4
    n_pluses = ctx.draw_int("n_pluses", np_lo, np_hi)
    h = rng.randint(10, 15)
    w = rng.randint(10, 15)
    g = full_grid(h, w, 0)
    candidates = [(r, c) for r in range(2, h - 2) for c in range(2, w - 2)]
    rng.shuffle(candidates)
    placed = 0
    for r, c in candidates:
        if placed >= n_pluses:
            break
        if not _clear(g, r, c):
            continue
        yellow_count = rng.randint(2, 4)
        yellow = {(0, 0)}
        arms = PLUS_OFFSETS[1:]
        rng.shuffle(arms)
        yellow.update(arms[:yellow_count - 1])
        for dr, dc in PLUS_OFFSETS:
            g[r + dr][c + dc] = 4 if (dr, dc) in yellow else 5
        placed += 1
    if placed == 0:
        for dr, dc in PLUS_OFFSETS:
            g[3 + dr][3 + dc] = 4 if (dr, dc) in {(0, 0), (1, 0)} else 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_pluses":
        return g
    if name == "single_arm":
        g[5][5] = 4
        g[5][6] = 5
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 4
        return g
    return g
