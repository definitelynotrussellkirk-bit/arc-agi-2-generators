"""Generator for 11b:m74 — scale smallest component and recolor.

Rule: a single-cell marker provides a target color. Among multi-cell
shapes, find the smallest. Crop, upscale 2x, recolor to marker color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker (no isolated single-cell marker → rule's
target-color selector returns nothing), tied_smallest (≥2 multi-cell
shapes share min size → "the smallest" is ambiguous, tie-break
decides), single_shape (only one multi-cell shape → no candidate
contrast for "smallest").
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "00f0de29a65c"
VERSION = "1.1.0"
TASK_ID = "00f0de29a65c"
SUMMARY = "1 single-cell marker + 2-3 multi-cell shapes with distinct sizes."

INVARIANTS = [
    "background is 0",
    "exactly one isolated single-cell marker",
    "2-3 multi-cell shapes, distinct colors, with strictly distinct cell counts",
    "marker color is distinct from all shape colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "tied_smallest", "single_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":            {"type": "int", "default": "rng 12..15", "valid": "11..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":     {"type": "str", "default": "marker_plus_distinct_size_shapes",
                          "valid": "marker_plus_distinct_size_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_SIZE = {
    3: [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2)],
    ],
    4: [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
    ],
    5: [
        [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)],
    ],
    6: [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
    ],
    7: [
        [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
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
        w = ctx.draw_int("grid_w", 12, 13)
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
        n_lo, n_hi = 3, 3
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 12, 15)
        n_lo, n_hi = 2, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_shapes = rng.randint(n_lo, n_hi)
    sizes = rng.sample([3, 4, 5, 6, 7], n_shapes)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_shapes + 1)
    marker_color = palette[0]
    shape_colors = palette[1:]
    for size, color in zip(sizes, shape_colors):
        _place(g, rng, rng.choice(_BY_SIZE[size]), color)
    for _ in range(60):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        bad = False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                    bad = True; break
            if bad: break
        if bad: continue
        g[r][c] = marker_color; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # No isolated single-cell marker — rule's target-color
        # selector returns nothing.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[6 + dr][7 + dc] = 6
        return g
    if name == "tied_smallest":
        # Two multi-cell shapes share min size — "the smallest" is
        # ambiguous; tie-break decides.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[6 + dr][8 + dc] = 6   # tied with prev
        g[10][1] = 7
        return g
    if name == "single_shape":
        # Only one multi-cell shape — no contrast for "smallest".
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[3 + dr][3 + dc] = 4
        g[10][9] = 7
        return g
    return g
