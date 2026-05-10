"""Generator for arc_puzzle_bank_21_set12_bundle:hard_l16 — blocked geodesic Voronoi.

Rule: color-5 cells are walls; other non-zero cells are seeds. Every 0-cell
takes the color of its unique nearest seed (BFS shortest path through non-walls).
Ties remain 0. Walls and seeds preserved.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls (no color-5 → BFS becomes unblocked Manhattan
Voronoi); no_seeds (walls present but no seeds → output identical
to input, no fill); single_seed (only 1 seed → all reachable cells
take that color, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "d3633a9fb1cd"
VERSION = "1.1.0"
TASK_ID = "d3633a9fb1cd"

SUMMARY = "Color-5 outer wall + 2-3 seeds inside; output is the geodesic Voronoi fill."

INVARIANTS = [
    "background is 0",
    "an outer rectangular color-5 wall (full perimeter) plus optional interior wall column/row",
    "2-3 seed cells in distinct non-{0, 5} colors strictly inside the walled region",
    "seeds are reachable from each other (no isolated chambers)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "n_seeds":           {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "walled_region_with_seeds",
                          "valid": "walled_region_with_seeds"},
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
        w = ctx.draw_int("grid_w", 11, 12)
        n_seeds = ctx.draw_int("n_seeds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n_seeds = ctx.draw_int("n_seeds", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    rng = ctx.draw_rng("layout")

    seed_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_seeds)

    for outer in range(40):
        g = full_grid(h, w, 0)
        wall_r1 = 1
        wall_c1 = 1
        wall_r2 = h - 2
        wall_c2 = w - 2
        draw_frame(g, wall_r1, wall_c1, wall_r2, wall_c2, 5)
        interior = [(r, c) for r in range(wall_r1 + 1, wall_r2)
                            for c in range(wall_c1 + 1, wall_c2)]
        if len(interior) < n_seeds * 4:
            continue
        chosen = []
        for color in seed_colors:
            placed = False
            for _ in range(120):
                cand = rng.choice(interior)
                if cand in chosen:
                    continue
                if any(abs(cand[0] - r) + abs(cand[1] - c) < 3 for r, c in chosen):
                    continue
                chosen.append(cand)
                g[cand[0]][cand[1]] = color
                placed = True
                break
            if not placed:
                break
        if len(chosen) == n_seeds:
            return g
    raise ValueError("could not realize Voronoi layout in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # No color-5 wall — BFS becomes unblocked Manhattan Voronoi.
        g[3][3] = 4
        g[6][8] = 6
        return g
    if name == "no_seeds":
        # Walls present but no seeds — output identical to input.
        draw_frame(g, 1, 1, h - 2, w - 2, 5)
        return g
    if name == "single_seed":
        # Only 1 seed — all reachable cells get that color, no contrast.
        draw_frame(g, 1, 1, h - 2, w - 2, 5)
        g[5][6] = 4
        return g
    return g
