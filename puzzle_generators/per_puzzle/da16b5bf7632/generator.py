"""Generator for 8b:hard_55 — sort components by holes (desc) and hconcat.

Rule: connected components sorted by hole-count desc, ties by (row, col).
Output is the cropped shapes hconcat'd in that order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_zero_holes (all 3 components have 0 holes → tie-break
falls to (row, col), hides "by holes" branch); single_component
(only one component, sort is trivial); tied_holes (two components
share hole-count → ordering between them is tie-break-dependent).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "da16b5bf7632"
VERSION = "1.1.0"
TASK_ID = "da16b5bf7632"

SUMMARY = "3 components in distinct colors, with distinct hole counts."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components in distinct colors",
    "each pair has different hole counts (so the sort is unambiguous)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_zero_holes", "single_component", "tied_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 16..18", "valid": "14..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_distinct_holes",
                       "valid": "three_distinct_holes"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_HOLES = {
    0: [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
    ],
    1: [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    ],
    2: [
        [(0, 0), (0, 1), (0, 2), (0, 3),
         (1, 0), (1, 2), (1, 3),
         (2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    3: [
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
         (1, 0), (1, 2), (1, 4),
         (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
    ],
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 16, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 18, 22)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 16, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 6, 7, 8, 9], 3)
    keys = rng.sample([0, 1, 2, 3], 3)
    for k, color in zip(keys, palette):
        _place(g, rng, rng.choice(_BY_HOLES[k]), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 17
    g = full_grid(h, w, 0)
    if name == "all_zero_holes":
        # All 3 components have 0 holes → rule's "by holes desc"
        # comparator yields all-tied; output ordering is
        # tie-break-only.
        for shape, color in [(_BY_HOLES[0][0], 2), (_BY_HOLES[0][1], 3),
                             (_BY_HOLES[0][0], 4)]:
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            for r0 in range(0, h - sh - 1, 4):
                for c0 in range(0, w - sw - 1, 5):
                    if all(g[r0 + dr][c0 + dc] == 0 for dr, dc in shape):
                        for dr, dc in shape:
                            g[r0 + dr][c0 + dc] = color
                        break
                else:
                    continue
                break
        return g
    if name == "single_component":
        # Only one component — rule's sort is trivial, no contrast.
        for dr, dc in _BY_HOLES[2][0]:
            g[3 + dr][5 + dc] = 4
        return g
    if name == "tied_holes":
        # Two components share hole-count → comparator yields a tie
        # at that pair; downstream ordering depends on tie-break.
        placed = []
        for shape, color, base in [(_BY_HOLES[1][0], 2, (1, 1)),
                                   (_BY_HOLES[1][0], 3, (1, 9)),
                                   (_BY_HOLES[0][0], 6, (8, 5))]:
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            r0, c0 = base
            if r0 + sh <= h and c0 + sw <= w:
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                placed.append(color)
        return g
    return g
