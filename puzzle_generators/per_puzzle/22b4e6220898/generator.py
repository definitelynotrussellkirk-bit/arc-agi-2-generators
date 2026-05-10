"""Generator for arc_additional_puzzles_21_set21_bundle:H144 — path overlap.

Rule: for every color present (each appearing exactly twice), draw a fixed
horizontal-first L-path between the two terminals. Cells used by 2+ paths
become color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_pairs, texture.
Degenerates: no_pairs, single_endpoint, no_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22b4e6220898"
VERSION = "1.1.0"
TASK_ID = "22b4e6220898"

SUMMARY = "2-3 colored endpoint pairs that L-route along horizontal-first paths."

INVARIANTS = [
    "background is 0",
    "2-3 distinct non-{0, 8} colors, each appearing exactly twice as endpoints",
    "endpoints are not 4-adjacent and have non-trivial L-paths between them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_endpoint", "no_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "= n_pairs", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "scattered_l_route_pairs",
                       "valid": "scattered_l_route_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= n_pairs", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
        n_pairs = ctx.draw_int("n_pairs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([2, 3, 4, 5, 6, 7, 9], n_pairs)

    for outer in range(60):
        g = full_grid(h, w, 0)
        used = set()
        ok = True
        for color in palette:
            placed = False
            for _ in range(120):
                ar = rng.randint(0, h - 1); ac = rng.randint(0, w - 1)
                br = rng.randint(0, h - 1); bc = rng.randint(0, w - 1)
                if (ar, ac) in used or (br, bc) in used: continue
                if (ar, ac) == (br, bc): continue
                if abs(ar - br) < 2 or abs(ac - bc) < 2: continue
                g[ar][ac] = color
                g[br][bc] = color
                used.add((ar, ac)); used.add((br, bc))
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not place {0} L-route pairs in 60 attempts".format(n_pairs))


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no endpoint pairs to L-route.
        return g
    if name == "single_endpoint":
        # Color appears only once (no second endpoint) — rule's
        # "exactly twice" filter excludes; no path to draw.
        g[2][2] = 3
        return g
    if name == "no_overlap":
        # Two color pairs whose L-paths don't intersect — rule's
        # 8-overlay step has no cells to mark; output has no 8s.
        g[1][1] = 3; g[1][6] = 3
        g[6][1] = 4; g[6][8] = 4
        return g
    return g
