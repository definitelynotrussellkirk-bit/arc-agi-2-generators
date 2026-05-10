"""Generator for 17b:m118 — connect pairs with monotone staircases.

Rule: for each color appearing exactly twice (cell-pair), paint a
monotone staircase between the two cells in that color.

Object-graph family: structural property "each color has exactly 2
cells" is enforced via validate-after-place. The generator raises
ValueError if it can't realize the constraint, so the runner records
generate.generator_raised rather than producing a weak input.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_marker, adjacent_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2b83f40cf6d9"
VERSION = "1.1.0"
TASK_ID = "2b83f40cf6d9"

SUMMARY = "2-3 colors, each with exactly 2 single cells (the pairs to connect)."

INVARIANTS = [
    "background is 0",
    "2-3 distinct non-bg colors are present",
    "each color appears in exactly 2 cells",
    "all 4-6 cells are pairwise non-adjacent (4-conn) so each is its own component",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_marker", "adjacent_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "non_adjacent_pairs",
                       "valid": "non_adjacent_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _too_close(g, r, c) -> bool:
    h, w = len(g), len(g[0])
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_colors)
    for outer in range(40):
        g = full_grid(h, w, 0)
        ok = True
        for color in palette:
            placed = 0
            for _ in range(60):
                if placed == 2: break
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0 or _too_close(g, r, c):
                    continue
                g[r][c] = color
                placed += 1
            if placed != 2:
                ok = False; break
        if not ok:
            continue
        from collections import Counter
        cnt = Counter(v for row in g for v in row if v != 0)
        if all(v == 2 for v in cnt.values()) and len(cnt) == n_colors:
            return g
    raise ValueError(
        f"could not place {n_colors} non-adjacent color-pairs in 40 outer attempts")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no pairs to connect.
        return g
    if name == "single_marker":
        # Color has only 1 cell — rule needs 2 for a staircase pair.
        g[3][3] = 4
        return g
    if name == "adjacent_cells":
        # Pair is 4-adjacent — staircase degenerates to no movement.
        g[3][3] = 4; g[3][4] = 4
        return g
    return g
