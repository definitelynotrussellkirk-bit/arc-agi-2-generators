"""Generator for puzzle 5587a8d0.

Rule: collect distinct non-7 colors; sort by frequency desc. Output is
(2n-1)x(2n-1) grid where each ring (Chebyshev distance from center)
uses one color from outermost (most frequent) inward.

Combinatorial axes (8): grid_h/w, n_colors, palette_kind,
count_distribution, position_bias, anchor_corner, asymmetry_force,
bg_color.
Degenerates: monochrome, equal_counts, no_non_bg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1189131c32a4"
VERSION = "1.1.0"
TASK_ID = "1189131c32a4"
SUMMARY = "7-bg with N colors of distinct counts; rule outputs concentric squares."

INVARIANTS = [
    "bg = 7",
    "2-4 distinct non-7 colors with strictly distinct counts",
    "max count <= h*w (so all cells fit)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
COUNT_DISTRIBUTIONS = ("uniform_gap", "polarized", "increasing",
                       "decreasing", "powers")
DEGENERATE_TEXTURES = ("monochrome", "equal_counts", "no_non_bg")
HELPFUL_TEXTURES = COUNT_DISTRIBUTIONS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "grid_w":            {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "n_colors":          {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "count_distribution":{"type": "str", "default": "rng helpful",
                          "valid": "|".join(COUNT_DISTRIBUTIONS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "bg_color":          {"type": "color", "default": "7", "valid": "7"},
    "texture":           {"type": "str", "default": "alias for count_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 7, 10
    else:
        h_lo, h_hi = 4, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 1)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", 2, 3)))
    n_colors = max(2, min(min(h * w - 1, 5), n_colors))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    distribution = (overrides.get("texture") or
                    overrides.get("count_distribution")
                    or ctx.draw_choice("count_distribution",
                                       list(COUNT_DISTRIBUTIONS)))
    palette = _build_palette(palette_kind, n_colors, rng)
    counts = _build_counts(distribution, n_colors, h * w, rng)
    g = full_grid(h, w, 7)
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    idx = 0
    for color, cnt in zip(palette, counts):
        for _ in range(cnt):
            if idx >= len(cells):
                break
            r, c = cells[idx]
            idx += 1
            g[r][c] = color
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _build_counts(distribution, n, total, rng):
    if distribution == "uniform_gap":
        base = max(2, total // (n + 1))
        counts = [max(1, base - i) for i in range(n)]
    elif distribution == "polarized":
        counts = [max(2, total // 2)] + [1] * (n - 1)
    elif distribution == "increasing":
        counts = [1 + i for i in range(n)]
    elif distribution == "decreasing":
        counts = [n - i for i in range(n)]
    elif distribution == "powers":
        counts = [min(total - 1, 2 ** i) for i in range(n)]
    else:
        counts = list(range(1, n + 1))
    seen = set()
    final = []
    for c in counts:
        c = max(1, c)
        while c in seen and c < total:
            c += 1
        seen.add(c)
        final.append(c)
    if sum(final) > total:
        scale = total / sum(final)
        final = [max(1, int(c * scale)) for c in final]
        seen = set()
        for i, c in enumerate(final):
            while c in seen and c < total:
                c += 1
            seen.add(c)
            final[i] = c
    return final[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 7)
    color = rng.choice([1, 2, 3, 4, 5, 6, 8, 9])
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "equal_counts":
        # Two colors with equal counts → tie
        c1, c2 = rng.sample([1, 2, 3, 4, 5, 6, 8, 9], 2)
        for r in range(h):
            for c in range(w):
                g[r][c] = c1 if (r + c) % 2 == 0 else c2
        return g
    if name == "no_non_bg":
        return g
    return g
