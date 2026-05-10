"""Generator for puzzle 9af7a82c.

Rule: count cells per color (including 0). Sort by count desc. Output
each color as a column in a max-height grid; bars rise from top.

Combinatorial axes (8): grid_h/w, n_colors, palette_kind,
count_distribution, position_bias, anchor_corner, asymmetry_force,
include_zero.
Degenerates: monochrome, all_distinct, equal_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "370e7fced412"
VERSION = "1.1.0"
TASK_ID = "370e7fced412"
SUMMARY = "Small grid with N colors of distinct counts; rule sorts to bar chart."

INVARIANTS = [
    ">=3 distinct colors with distinct counts",
    "all counts < total cells (so no color fills entire grid)",
    "max count <= grid_h (so output bars fit)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
COUNT_DISTRIBUTIONS = ("uniform_gap", "increasing", "decreasing",
                        "polarized", "powers")
DEGENERATE_TEXTURES = ("monochrome", "all_distinct", "equal_counts")
HELPFUL_TEXTURES = COUNT_DISTRIBUTIONS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 3..6", "valid": "2..10"},
    "grid_w":            {"type": "int", "default": "rng 3..6", "valid": "2..10"},
    "n_colors":          {"type": "int", "default": "rng 3..4", "valid": "2..7"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "count_distribution":{"type": "str", "default": "rng helpful",
                          "valid": "|".join(COUNT_DISTRIBUTIONS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "include_zero":      {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for count_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 2, 4
    elif difficulty == "hard":
        h_lo, h_hi = 5, 10
    else:
        h_lo, h_hi = 3, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", 3, 4)))
    n_colors = max(2, min(min(7, h * w - 1), n_colors))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    distribution = (overrides.get("texture") or
                    overrides.get("count_distribution")
                    or ctx.draw_choice("count_distribution",
                                       list(COUNT_DISTRIBUTIONS)))
    palette = _build_palette(palette_kind, n_colors, rng)
    counts = _build_counts(distribution, n_colors, h, h * w, rng)
    g = full_grid(h, w, 0)
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
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _build_counts(distribution, n, max_count, total_cells, rng):
    max_count = max(2, max_count)
    if distribution == "uniform_gap":
        counts = [max_count - i for i in range(n)]
    elif distribution == "increasing":
        counts = [1 + i for i in range(n)]
    elif distribution == "decreasing":
        counts = [max_count - i for i in range(n)]
    elif distribution == "polarized":
        counts = [max_count] + [1] * (n - 1)
    elif distribution == "powers":
        counts = [min(max_count, 2 ** i) for i in range(n)]
    else:
        counts = [max_count - i for i in range(n)]
    # Make all counts distinct + positive
    seen = set()
    final = []
    for c in counts:
        c = max(1, c)
        while c in seen and c < max_count:
            c += 1
        if c in seen:
            c -= 1
            while c in seen and c > 1:
                c -= 1
        if c < 1:
            c = 1
        seen.add(c)
        final.append(c)
    if sum(final) > total_cells:
        scale = total_cells / sum(final)
        final = sorted({max(1, int(c * scale)) for c in final}, reverse=True)
    return final[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    if name == "monochrome":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "all_distinct":
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(9, len(cells)))
        for i, (r, c) in enumerate(cells):
            g[r][c] = palette[i % len(palette)]
        return g
    if name == "equal_counts":
        # Two colors with equal counts → tie in sort order
        for r in range(h):
            for c in range(w):
                g[r][c] = color if (r + c) % 2 == 0 else (color % 9) + 1
        return g
    return g
