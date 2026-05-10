"""Generator for 19b:m131 — connect color pairs with clear elbows
(over an 8-marker obstacle field).

Rule: for each color appearing exactly twice (excluding 8), paint an
elbow path that doesn't cross any 8-cell. The 8-cells act as walls.

Object-graph family: validate-after-place ensures (a) each color has
2 isolated cells, (b) at least one elbow per pair avoids both 8-cells
and other pair-cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: single_pair (only 1 color pair → no graph effect);
no_walls (no color-8 walls → rule's wall-avoidance becomes trivial,
both elbows of every pair are clear); walls_block_all_pairs (every
pair has both elbows blocked by walls → rule's clear-elbow
precondition fails for every pair).
"""
from __future__ import annotations

from collections import Counter

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "76e0bd03e098"
VERSION = "1.1.0"
TASK_ID = "76e0bd03e098"

SUMMARY = "2-3 color pairs + 2-3 isolated 8-walls; pairs have at least one clear elbow."

INVARIANTS = [
    "background is 0",
    "2-3 distinct non-{0,8} colors, each appearing exactly 2 cells",
    "2-3 isolated 8-marker cells (walls)",
    "all cells pairwise non-adjacent (4-conn)",
    "for each pair, at least one of two L-elbow paths is clear of 8s and other pair-cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_pair", "no_walls", "walls_block_all_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "pairs_with_walls",
                          "valid": "pairs_with_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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


def _line(p, q):
    if p[0] == q[0]:
        c1, c2 = sorted([p[1], q[1]])
        return [(p[0], c) for c in range(c1, c2 + 1)]
    if p[1] == q[1]:
        r1, r2 = sorted([p[0], q[0]])
        return [(r, p[1]) for r in range(r1, r2 + 1)]
    return []


def _elbow_clear(a, b, blockers) -> bool:
    for e in [(a[0], b[1]), (b[0], a[1])]:
        path = set(_line(a, e)) | set(_line(e, b))
        middle = path - {a, b}
        if all(p not in blockers for p in middle):
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 3)
    n_walls = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n_colors)
    for _ in range(60):
        g = full_grid(h, w, 0)
        wall_cells = []
        for _ in range(60):
            if len(wall_cells) == n_walls: break
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0 or _too_close(g, r, c):
                continue
            g[r][c] = 8
            wall_cells.append((r, c))
        if len(wall_cells) < n_walls:
            continue
        cells_by_color: dict = {}
        ok = True
        for color in palette:
            placed = []
            for _ in range(80):
                if len(placed) == 2: break
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0 or _too_close(g, r, c):
                    continue
                if placed and (placed[0][0] == r or placed[0][1] == c):
                    continue
                g[r][c] = color
                placed.append((r, c))
            if len(placed) != 2:
                ok = False; break
            cells_by_color[color] = placed
        if not ok:
            continue
        wall_set = set(wall_cells)
        all_pair_cells = {p for pair in cells_by_color.values() for p in pair}
        good = True
        for color, pair in cells_by_color.items():
            blockers = wall_set | (all_pair_cells - set(pair))
            if not _elbow_clear(pair[0], pair[1], blockers):
                good = False; break
        if good:
            cnt = Counter(v for row in g for v in row if v != 0)
            if cnt.get(8, 0) == n_walls and \
               all(v == 2 for k, v in cnt.items() if k != 8) and \
               len([k for k in cnt if k != 8]) == n_colors:
                return g
    raise ValueError(
        f"could not realize {n_colors} pairs + {n_walls} walls with clear elbows")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "single_pair":
        # Only 1 color pair — no graph effect.
        g[2][2] = 1; g[6][7] = 1
        g[3][5] = 8; g[5][2] = 8
        return g
    if name == "no_walls":
        # No color-8 walls — wall-avoidance becomes trivial, no contrast.
        g[2][2] = 1; g[6][8] = 1
        g[2][8] = 2; g[6][2] = 2
        return g
    if name == "walls_block_all_pairs":
        # Walls form a complete diagonal blocking every elbow.
        g[2][2] = 1; g[6][8] = 1
        for k in range(min(h, w)):
            if 0 <= k < h and 0 <= k < w and g[k][k] == 0:
                g[k][k] = 8
        return g
    return g
