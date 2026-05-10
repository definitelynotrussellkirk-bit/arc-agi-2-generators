"""Generator for 12b:m80 — connect pairs with clear elbow path.

Rule: for each color appearing in exactly 2 cells, draw an elbow path
between them — but only if at least one of the two L-shaped routes is
clear of the OTHER pair-cells.

Object-graph family: validate-after-place ensures (a) each color has
exactly 2 cells, AND (b) for each pair, at least one elbow corner
yields a path that doesn't cross another pair's cells. Raises on
persistent failure.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: single_marker (some color has only 1 marker → rule's
"connect 2" branch finds no second endpoint), colinear_pair (both
markers on same row/col → no elbow needed; rule's elbow-path is
degenerate straight line), blocked_elbows (both elbows for some pair
cross other pair-cells → rule's "clear elbow" condition fails).
"""
from __future__ import annotations

from collections import Counter

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c7c9b61d5a51"
VERSION = "1.1.0"
TASK_ID = "c7c9b61d5a51"

SUMMARY = "2-3 color pairs (single cells); at least one elbow per pair is clear of other pairs."

INVARIANTS = [
    "background is 0",
    "2-3 distinct non-bg colors are present",
    "each color appears in exactly 2 cells",
    "all 4-6 cells are pairwise non-adjacent (4-conn)",
    "for each pair, at least one of the two L-shaped elbow paths is clear of other pair-cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_marker", "colinear_pair", "blocked_elbows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "color_pairs_for_elbow",
                          "valid": "color_pairs_for_elbow"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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


def _elbow_clear(g, a, b, others) -> bool:
    elbows = [(a[0], b[1]), (b[0], a[1])]
    for e in elbows:
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
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
        all_others = {p for color, pair in cells_by_color.items() for p in pair}
        good = True
        for color, pair in cells_by_color.items():
            others = all_others - set(pair)
            if not _elbow_clear(g, pair[0], pair[1], others):
                good = False; break
        if good:
            cnt = Counter(v for row in g for v in row if v != 0)
            if all(v == 2 for v in cnt.values()) and len(cnt) == n_colors:
                return g
    raise ValueError(
        f"could not place {n_colors} non-colinear color-pairs with clear elbows in 60 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "single_marker":
        # Some color has only 1 marker — rule's "connect 2" branch
        # finds no second endpoint.
        g[2][2] = 4
        g[5][6] = 6; g[6][8] = 6
        return g
    if name == "colinear_pair":
        # Both markers on same row — elbow path is degenerate straight line.
        g[3][2] = 4; g[3][7] = 4
        g[6][2] = 6; g[6][7] = 6
        return g
    if name == "blocked_elbows":
        # Both elbows for one pair are blocked by another pair's cells.
        g[2][2] = 4; g[6][8] = 4
        g[2][8] = 6; g[6][2] = 6   # both elbow corners blocked
        return g
    return g
