"""Generator for puzzle f341894c.

Rule: 7-marker looks through gray(8) corridor; visible adjacent 1/6
pair is rewritten to ordered 6,1 in viewing direction.

Combinatorial axes (8): grid_h/w, ray_direction, gap_min, gap_max,
n_corridors, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_corridor, no_pair, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b2f49898372a"
VERSION = "1.1.0"
TASK_ID = "b2f49898372a"
SUMMARY = "7 marker + 8 corridor + 1/6 pair; rule reorders 1/6 in viewing direction."

INVARIANTS = [
    "background is 0",
    "exactly 1 marker (7), 1 corridor of 8s, 1 1/6 pair",
    "marker + corridor + pair aligned in chosen direction",
]

DIRECTIONS = ("right", "left", "down", "up")
DEGENERATE_TEXTURES = ("no_corridor", "no_pair", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "ray_direction":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "gap_min":        {"type": "int", "default": "1", "valid": "1..3"},
    "gap_max":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "n_corridors":    {"type": "int", "default": "1", "valid": "1..2"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for ray_direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_DIR_DELTAS = {
    "right": (0, 1),
    "left": (0, -1),
    "down": (1, 0),
    "up": (-1, 0),
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 7, 9
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
    else:
        h_lo, h_hi = 9, 14
    h = h_lo + rng.randint(0, h_hi - h_lo)
    w = h_lo + rng.randint(0, h_hi - h_lo)
    direction = (overrides.get("texture") or
                 overrides.get("ray_direction")
                 or ctx.draw_choice("ray_direction",
                                    list(DIRECTIONS)))
    if direction not in _DIR_DELTAS:
        direction = "right"
    gap_min = int(overrides.get("gap_min", 1))
    gap_max = int(overrides.get("gap_max",
                                ctx.draw_int("gap_max", 2, 3)))
    gap_min = max(1, min(3, gap_min))
    gap_max = max(gap_min, min(5, gap_max))
    g = full_grid(h, w, 0)
    dr, dc = _DIR_DELTAS[direction]
    if direction == "right":
        mr = rng.randint(h // 3, max(h // 3, 2 * h // 3)); mc = 1
    elif direction == "left":
        mr = rng.randint(h // 3, max(h // 3, 2 * h // 3)); mc = w - 2
    elif direction == "down":
        mr = 1; mc = rng.randint(w // 3, max(w // 3, 2 * w // 3))
    else:
        mr = h - 2; mc = rng.randint(w // 3, max(w // 3, 2 * w // 3))
    g[mr][mc] = 7
    gap = rng.randint(gap_min, gap_max)
    for i in range(1, gap + 1):
        rr, cc = mr + dr * i, mc + dc * i
        if 0 <= rr < h and 0 <= cc < w:
            g[rr][cc] = 8
    a_r, a_c = mr + dr * (gap + 1), mc + dc * (gap + 1)
    b_r, b_c = mr + dr * (gap + 2), mc + dc * (gap + 2)
    if not (0 <= a_r < h and 0 <= a_c < w and
            0 <= b_r < h and 0 <= b_c < w):
        # Adjust to fit
        gap = 1
        for i in range(1, gap + 1):
            rr, cc = mr + dr * i, mc + dc * i
            if 0 <= rr < h and 0 <= cc < w:
                g[rr][cc] = 8
        a_r, a_c = mr + dr * (gap + 1), mc + dc * (gap + 1)
        b_r, b_c = mr + dr * (gap + 2), mc + dc * (gap + 2)
    if 0 <= a_r < h and 0 <= a_c < w:
        g[a_r][a_c] = 1
    if 0 <= b_r < h and 0 <= b_c < w:
        g[b_r][b_c] = 6
    return g


def _draw_from_degenerate(name, rng):
    h = w = 11
    g = full_grid(h, w, 0)
    if name == "no_corridor":
        g[h // 2][1] = 7
        g[h // 2][3] = 1
        g[h // 2][4] = 6
        return g
    if name == "no_pair":
        g[h // 2][1] = 7
        for c in range(2, 5):
            g[h // 2][c] = 8
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
