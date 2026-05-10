"""Generator for 18b:m124 — connect color pairs with clear elbows.

Rule: for each color appearing exactly twice, paint the elbow path
between them — provided at least one of the two L-shaped routes
doesn't cross another pair's cells.

Object-graph family: same validate-after-place tactic as m80.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: single_pair (only 1 pair → rule paints just one
elbow, no graph effect); colinear_pair (pair endpoints share row
or column → "elbow" degenerates to a straight line, both routes
identical); no_clear_elbow (every pair's both elbows pass through
another pair's cells → rule's clear-elbow precondition fails).
"""
from __future__ import annotations

from collections import Counter

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0fc84838e274"
VERSION = "1.1.0"
TASK_ID = "0fc84838e274"

SUMMARY = "2-3 color pairs (single cells); at least one elbow per pair is clear of other pairs."

INVARIANTS = [
    "background is 0",
    "2-3 distinct non-bg colors are present",
    "each color appears in exactly 2 cells",
    "all cells pairwise non-adjacent (4-conn)",
    "for each pair, at least one of two L-elbow paths is clear of other pair-cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_pair", "colinear_pair", "no_clear_elbow")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":     {"type": "str", "default": "non_colinear_pairs",
                          "valid": "non_colinear_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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


def _elbow_clear(a, b, others) -> bool:
    for e in [(a[0], b[1]), (b[0], a[1])]:
        path = set(_line(a, e)) | set(_line(e, b))
        if all(p not in others for p in path):
            return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_colors)
    for _ in range(60):
        g = full_grid(h, w, 0)
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
        all_others = {p for pair in cells_by_color.values() for p in pair}
        good = True
        for color, pair in cells_by_color.items():
            if not _elbow_clear(pair[0], pair[1], all_others - set(pair)):
                good = False; break
        if good:
            cnt = Counter(v for row in g for v in row if v != 0)
            if all(v == 2 for v in cnt.values()) and len(cnt) == n_colors:
                return g
    raise ValueError(
        f"could not place {n_colors} non-colinear color-pairs with clear elbows in 60 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "single_pair":
        # Only 1 color pair — graph effect collapses to a single elbow.
        g[2][2] = 1; g[7][8] = 1
        return g
    if name == "colinear_pair":
        # Pair endpoints share a row — "elbow" is a straight line, no L bend.
        g[3][1] = 1; g[3][9] = 1
        g[6][2] = 2; g[8][8] = 2
        return g
    if name == "no_clear_elbow":
        # Both elbows of each pair pass through another pair's cell.
        g[2][2] = 1; g[8][8] = 1
        g[2][8] = 2; g[8][2] = 2
        return g
    return g
