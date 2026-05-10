"""Generator for 4b:hard_28 — select by marker count, scale, recolor.

Rule: count K = number of 9-marker cells. Pick the K-th smallest
color-1 component (1-indexed). Scale it 2x, recolor to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers (K = 0 → rule's "K-th smallest" with K=0 has
no valid index, no component selected), out_of_range_K (K > number
of components → rule's K-th lookup is out of bounds), tied_sizes
(≥2 components share size → "K-th smallest" rank is ambiguous,
tie-break decides).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b7ff231aab1a"
VERSION = "1.1.0"
TASK_ID = "b7ff231aab1a"
SUMMARY = "K isolated 9-markers + 3 color-1 components with strictly distinct sizes."

INVARIANTS = [
    "background is 0",
    "1-3 isolated 9-marker cells",
    "exactly 3 color-1 components with strictly distinct cell counts",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "out_of_range_K", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "markers_plus_distinct_size_components",
                          "valid": "markers_plus_distinct_size_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_SIZE = {
    3: [[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (1, 1)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 0)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        m_lo, m_hi = 1, 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 13)
        w = ctx.draw_int("grid_w", 15, 15)
        m_lo, m_hi = 2, 3
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        m_lo, m_hi = 1, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sizes = rng.sample([3, 4, 5, 6], 3)
    for size in sizes:
        _place(g, rng, rng.choice(_BY_SIZE[size]), 1)
    n_markers = rng.randint(m_lo, m_hi)
    placed = 0; attempts = 0
    while placed < n_markers and attempts < 60:
        attempts += 1
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
        g[r][c] = 9; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # K = 0 — rule's "K-th smallest" has no valid index;
        # no component selected.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[5 + dr][5 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]:
            g[8 + dr][9 + dc] = 1
        return g
    if name == "out_of_range_K":
        # K = 5 markers but only 3 components — rule's K-th lookup
        # is out of bounds.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[5 + dr][5 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (0, 2)]:
            g[8 + dr][9 + dc] = 1
        for r, c in [(0, 12), (4, 13), (7, 12), (10, 0), (10, 6)]:
            g[r][c] = 9
        return g
    if name == "tied_sizes":
        # Two components share min size — "K-th smallest" is ambiguous.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][5 + dc] = 1   # tied with prev
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]:
            g[8 + dr][9 + dc] = 1
        g[3][12] = 9
        return g
    return g
