"""Generator for puzzle 5521c0d9.

Rule: bar chart at bottom; each bar jumps up by its own height.

Combinatorial axes (8): grid_h/w, n_bars, bar_height_distribution,
bar_width_distribution, bar_position_bias, palette_size,
inter_bar_spacing, anchor_bottom.
Degenerates: single_bar, no_bars, equal_height_bars.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fdd447a064fe"
VERSION = "1.1.0"
TASK_ID = "fdd447a064fe"
SUMMARY = "Bar chart at bottom; rule jumps each bar up by its own height."

INVARIANTS = [
    "background is 0",
    ">=2 rectangular bars at bottom",
    "each bar height h_b satisfies 2*h_b <= grid_h",
    "bars don't overlap horizontally",
    "bars use distinct colors",
]

HEIGHT_DISTS = ("ascending", "wide_spread", "tight_spread", "shuffled")
WIDTH_DISTS = ("uniform_1", "uniform_2", "mixed", "all_2")
DEGENERATE_TEXTURES = ("single_bar", "no_bars", "equal_height_bars")
HELPFUL_TEXTURES = HEIGHT_DISTS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 10..18", "valid": "8..22"},
    "grid_w":             {"type": "int", "default": "rng 10..16", "valid": "8..20"},
    "n_bars":             {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "bar_height_distribution": {"type": "str", "default": "rng helpful",
                                "valid": "|".join(HEIGHT_DISTS)},
    "bar_width_distribution": {"type": "str", "default": "rng helpful",
                               "valid": "|".join(WIDTH_DISTS)},
    "bar_position_bias":  {"type": "str", "default": "rng spread|left|center",
                           "valid": "spread|left|center"},
    "inter_bar_spacing":  {"type": "int", "default": "rng 0..2",
                           "valid": "0..3"},
    "anchor_bottom":      {"type": "bool", "default": "true",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for bar_height_distribution",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 8, 12, 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 16, 22, 5, 7
    else:
        h_lo, h_hi, n_lo, n_hi = 10, 18, 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_bars = int(overrides.get("n_bars",
                               ctx.draw_int("n_bars", n_lo, n_hi)))
    n_bars = max(2, min(7, n_bars))
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=n_bars, exclude={0}))
    while len(palette) < n_bars:
        palette.append(palette[0])
    height_dist = (overrides.get("texture") or
                   overrides.get("bar_height_distribution")
                   or ctx.draw_choice("bar_height_distribution",
                                      list(HEIGHT_DISTS)))
    width_dist = overrides.get("bar_width_distribution",
                               ctx.draw_choice("bar_width_distribution",
                                               list(WIDTH_DISTS)))
    bias = overrides.get("bar_position_bias",
                         ctx.draw_choice("bar_position_bias",
                                         ["spread", "left", "center"]))
    spacing = int(overrides.get("inter_bar_spacing",
                                ctx.draw_int("inter_bar_spacing", 0, 2)))
    g = full_grid(h, w, 0)
    heights = _draw_heights(height_dist, n_bars, h, rng)
    widths = _draw_widths(width_dist, n_bars, rng)
    positions = _draw_positions(bias, w, n_bars, widths, spacing, rng)
    placed = 0
    for i, (start_c, bw, bh) in enumerate(zip(positions, widths, heights)):
        if start_c is None:
            continue
        if 2 * bh >= h or start_c + bw > w:
            continue
        for dr in range(bh):
            for dc in range(bw):
                if 0 <= h - 1 - dr < h and 0 <= start_c + dc < w:
                    g[h - 1 - dr][start_c + dc] = palette[i]
        placed += 1
    if placed < 2:
        # Fallback: simple 2-bar placement
        g = full_grid(h, w, 0)
        g[h - 1][1] = palette[0]
        g[h - 1][3] = palette[1] if len(palette) > 1 else palette[0]
        g[h - 2][3] = palette[1] if len(palette) > 1 else palette[0]
    return g


def _draw_heights(dist, n, h, rng):
    max_h = h // 2 - 1
    if max_h < 1:
        return [1] * n
    if dist == "ascending":
        return [min(max_h, 1 + i) for i in range(n)]
    if dist == "tight_spread":
        base = rng.randint(1, max(1, max_h - n + 1))
        return [min(max_h, base + i) for i in range(n)]
    if dist == "wide_spread":
        return sorted([rng.randint(1, max_h) for _ in range(n)])
    return [rng.randint(1, max_h) for _ in range(n)]


def _draw_widths(dist, n, rng):
    if dist == "uniform_1":
        return [1] * n
    if dist == "uniform_2":
        return [2] * n
    if dist == "all_2":
        return [2] * n
    return [rng.choice([1, 2]) for _ in range(n)]


def _draw_positions(bias, w, n, widths, spacing, rng):
    total_width = sum(widths) + (n - 1) * spacing
    if total_width > w:
        return [None] * n
    if bias == "left":
        positions = []
        c = 0
        for bw in widths:
            positions.append(c)
            c += bw + spacing
        return positions
    if bias == "center":
        positions = []
        c = max(0, (w - total_width) // 2)
        for bw in widths:
            positions.append(c)
            c += bw + spacing
        return positions
    free = w - total_width
    gap = max(spacing, free // (n + 1))
    positions = []
    c = gap
    for bw in widths:
        positions.append(c)
        c += bw + max(spacing, gap)
    return positions


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "single_bar":
        for dr in range(min(3, h - 1)):
            g[h - 1 - dr][w // 2] = color
        return g
    if name == "no_bars":
        return g
    if name == "equal_height_bars":
        bh = 2
        for i, c0 in enumerate([1, 4, 7]):
            if c0 + 1 < w and i < 3:
                color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
                for dr in range(bh):
                    g[h - 1 - dr][c0] = color
        return g
    return g
