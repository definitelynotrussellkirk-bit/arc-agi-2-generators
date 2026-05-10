"""Generator for arc_additional_puzzles_21_set13_bundle:H85 — priority sprouts.

Rule: row 0 holds priority colors in column order (ignoring zeros, lower index =
higher priority). Body cells grow a plus of radius 1. When sprouts overlap,
the higher-priority color wins. Output drops row 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_priority, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_priority, no_seeds, single_priority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a3a85fedfec1"
VERSION = "1.1.0"
TASK_ID = "a3a85fedfec1"

SUMMARY = "Top-row priority colors + body seeds; each seed grows a + and overlaps resolve by priority."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-3 distinct non-zero priority colors at distinct columns",
    "body (rows 1..h-1) has 3-5 isolated seed cells colored from the priority list",
    "seeds are not adjacent in body (so individual plus shapes are distinguishable in output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_priority", "no_seeds", "single_priority")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_priority":     {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "n_seeds":        {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "row0_priority_seeds_below",
                       "valid": "row0_priority_seeds_below"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_priority = ctx.draw_int("n_priority", 2, 2)
        n_seeds = ctx.draw_int("n_seeds", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
        n_priority = ctx.draw_int("n_priority", 3, 3)
        n_seeds = ctx.draw_int("n_seeds", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n_priority = ctx.draw_int("n_priority", 2, 3)
        n_seeds = ctx.draw_int("n_seeds", 3, 5)
    rng = ctx.draw_rng("layout")
    priority = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_priority)

    for outer in range(40):
        g = full_grid(h, w, 0)
        cols0 = rng.sample(range(w), n_priority)
        cols0.sort()
        for col, color in zip(cols0, priority):
            g[0][col] = color

        placed = []
        ok = True
        for _ in range(n_seeds):
            inner_placed = False
            for _ in range(80):
                r = rng.randint(1, h - 1)
                c = rng.randint(0, w - 1)
                if g[r][c] != 0:
                    continue
                adj_clash = False
                for sr, sc in placed:
                    if abs(sr - r) + abs(sc - c) <= 1:
                        adj_clash = True
                        break
                if adj_clash:
                    continue
                color = rng.choice(priority)
                g[r][c] = color
                placed.append((r, c))
                inner_placed = True
                break
            if not inner_placed:
                ok = False
                break
        if ok and len(placed) == n_seeds:
            return g
    raise ValueError("could not place seeds in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_priority":
        # Row 0 empty — rule has no priority order.
        g[3][3] = 4; g[5][6] = 5
        return g
    if name == "no_seeds":
        # Priority but no body seeds — rule has no plus-shapes to grow.
        g[0][2] = 4; g[0][6] = 5
        return g
    if name == "single_priority":
        # Only one priority color — rule's priority resolution is trivial.
        g[0][2] = 4
        g[3][3] = 4; g[5][6] = 4
        return g
    return g
