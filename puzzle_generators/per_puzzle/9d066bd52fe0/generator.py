"""Generator for arc_puzzle_bank_21_set8:hard_h17.

Creates small geodesic Voronoi scenes: singleton colored seeds compete
through black space while gray walls block orthogonal movement.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9d066bd52fe0"
VERSION = "1.1.0"
TASK_ID = "9d066bd52fe0"

SUMMARY = "Singleton colored seeds fill reachable regions around gray walls."

INVARIANTS = [
    "background is 0",
    "gray 5 cells are walls",
    "all non-wall colors are singleton seeds",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w": {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "n_seeds": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_walls": {"type": "int", "default": "rng 1..2", "valid": "0..3"},
}


def _zero_cells(g):
    return [
        (r, c)
        for r, row in enumerate(g)
        for c, value in enumerate(row)
        if value == 0
    ]


def _add_wall(g, rng):
    h, w = len(g), len(g[0])
    vertical = rng.choice([True, False])
    if vertical and w >= 5:
        c = rng.randint(2, w - 3)
        gap_count = 1 if h <= 7 else rng.randint(1, 2)
        gaps = set(rng.sample(range(h), gap_count))
        for r in range(h):
            if r not in gaps:
                g[r][c] = 5
    elif h >= 5:
        r = rng.randint(2, h - 3)
        gap_count = 1 if w <= 8 else rng.randint(1, 2)
        gaps = set(rng.sample(range(w), gap_count))
        for c in range(w):
            if c not in gaps:
                g[r][c] = 5


def _far_enough(pos, chosen, min_gap):
    r, c = pos
    return all(abs(r - rr) + abs(c - cc) >= min_gap for rr, cc in chosen)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("grid_h", 7, 9)
    w = ctx.draw_int("grid_w", 8, 11)
    n_seeds = ctx.draw_int("n_seeds", 2, 3)
    n_walls = ctx.draw_int("n_walls", 1, 2)
    rng = ctx.draw_rng("layout")

    for _ in range(60):
        g = full_grid(h, w, 0)
        for _ in range(n_walls):
            _add_wall(g, rng)

        cells = _zero_cells(g)
        rng.shuffle(cells)
        chosen = []
        min_gap = max(3, min(h, w) // 2)
        for pos in cells:
            if _far_enough(pos, chosen, min_gap):
                chosen.append(pos)
                if len(chosen) == n_seeds:
                    break
        if len(chosen) < n_seeds:
            continue

        colors = rng.sample([2, 3, 4, 6, 7, 8, 9], n_seeds)
        for (r, c), color in zip(chosen, colors):
            g[r][c] = color
        return g

    raise ValueError("could not place geodesic seeds")
