"""Generator for arc_additional_puzzles_21_set13_bundle:H90 — route pairs around the wall.

Rule: color 8 is impassable wall. For each non-{0, 8} color appearing exactly
twice, BFS shortest path between the two endpoints avoiding walls and any
already-painted other-colored paths. Paint that path with the same color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_wall (no color-8 → BFS becomes unblocked, no
routing challenge); no_pairs (wall but no endpoint pairs → rule
has nothing to route); single_pair (only 1 pair → no other-colored
paths to avoid, simpler routing).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b5f36515995c"
VERSION = "1.1.0"
TASK_ID = "b5f36515995c"

SUMMARY = "Vertical wall + 2-3 colored endpoint pairs to route around it."

INVARIANTS = [
    "background is 0",
    "exactly one full-height color-8 vertical wall column with a 1-cell gap",
    "2-3 distinct non-{0,8} colors each appear exactly twice as endpoints",
    "endpoints are reachable through the wall gap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_wall", "no_pairs", "single_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "n_pairs":           {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "wall_with_routing_pairs",
                          "valid": "wall_with_routing_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_pairs = ctx.draw_int("n_pairs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("layout")

    wall_col = w // 2
    gap_row = rng.choice([0, 1, 2, h - 1, h - 2, h - 3])
    palette = rng.sample([2, 3, 4, 5, 6, 7, 9], n_pairs)

    for outer in range(40):
        g = full_grid(h, w, 0)
        for r in range(h):
            if r != gap_row:
                g[r][wall_col] = 8

        used = set()
        ok = True
        for color in palette:
            placed = False
            for _ in range(120):
                ar = rng.randint(0, h - 1); ac = rng.randint(0, wall_col - 1)
                br = rng.randint(0, h - 1); bc = rng.randint(wall_col + 1, w - 1)
                if (ar, ac) in used or (br, bc) in used:
                    continue
                if g[ar][ac] != 0 or g[br][bc] != 0:
                    continue
                if abs(ar - gap_row) < 1 and ac == wall_col:
                    continue
                if abs(ar - br) + abs(ac - bc) < 4:
                    continue
                g[ar][ac] = color
                g[br][bc] = color
                used.add((ar, ac))
                used.add((br, bc))
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not place {0} routed pairs in 40 attempts".format(n_pairs))


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_wall":
        # No wall — BFS becomes unblocked, no routing challenge.
        g[2][2] = 4; g[6][8] = 4
        g[3][7] = 6; g[7][2] = 6
        return g
    if name == "no_pairs":
        # Wall present but no endpoint pairs — nothing to route.
        for r in range(h):
            if r != 4: g[r][5] = 8
        return g
    if name == "single_pair":
        # Only 1 pair — no other-colored paths to avoid.
        for r in range(h):
            if r != 4: g[r][5] = 8
        g[2][2] = 4; g[6][8] = 4
        return g
    return g
