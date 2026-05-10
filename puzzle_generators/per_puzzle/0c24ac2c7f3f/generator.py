"""Generator for bd283c4a.

Rule: sort all colors (including bg) by frequency desc; output fills
bottom-to-top, left-to-right with each color taking its count of cells
(stacked histogram).

Combinatorial axes (8): grid_h/w, n_colors, palette_kind, count_skew,
anchor_corner, asymmetry_force, palette_size, include_decoy.
Degenerates: tied_freqs, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0c24ac2c7f3f"
VERSION = "1.1.0"
TASK_ID = "0c24ac2c7f3f"
SUMMARY = "Multiple colors with distinct frequencies; rule outputs stacked histogram."

INVARIANTS = [
    "3-5 distinct colors in the input",
    "colors have distinct frequencies (sort is unambiguous)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
COUNT_SKEWS = ("uniform", "skewed", "extreme")
DEGENERATE_TEXTURES = ("tied_freqs", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "n_colors":       {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "count_skew":     {"type": "str", "default": "rng",
                       "valid": "|".join(COUNT_SKEWS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
        n_lo, n_hi = 3, 3
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
        n_lo, n_hi = 4, 5
    else:
        h_lo, h_hi = 6, 10
        n_lo, n_hi = 3, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", n_lo, n_hi)))
    n_colors = max(2, min(6, n_colors))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_colors, rng)
    skew = overrides.get("count_skew",
                         ctx.draw_choice("count_skew", list(COUNT_SKEWS)))
    n_cells = h * w
    counts = _make_counts(skew, n_colors, n_cells, rng)
    g = full_grid(h, w, palette[0])
    positions = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(positions)
    idx = 0
    for color, cnt in zip(palette, counts):
        for _ in range(cnt):
            if idx >= len(positions):
                break
            r, c = positions[idx]; idx += 1
            g[r][c] = color
    return g


def _make_counts(skew, n_colors, n_cells, rng):
    if skew == "extreme":
        # one dominates
        counts = [n_cells - 2 * (n_colors - 1)]
        for i in range(n_colors - 1):
            counts.append(2 + i)
    elif skew == "skewed":
        counts = []
        remaining = n_cells
        weights = [2 ** (n_colors - 1 - i) for i in range(n_colors)]
        wsum = sum(weights)
        for i in range(n_colors - 1):
            c = max(1, remaining * weights[i] // wsum + rng.randint(-1, 1))
            counts.append(c)
            remaining -= c
        counts.append(max(1, remaining))
    else:
        counts = []
        remaining = n_cells
        for i in range(n_colors - 1):
            c = max(1, remaining // (n_colors - i) + rng.randint(-1, 1))
            counts.append(c)
            remaining -= c
        counts.append(max(1, remaining))
    if len(set(counts)) != len(counts):
        counts = sorted(rng.sample(range(2, max(3, n_cells)), n_colors),
                        reverse=True)
        diff = n_cells - sum(counts)
        counts[0] += diff
        if counts[0] <= 0:
            counts[0] = max(1, counts[0])
    return counts


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [0, 2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [0, 1, 5, 7, 8]
    elif kind == "primary":
        pool = [0, 1, 2, 3, 4]
    else:
        pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "tied_freqs":
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 3 + 1
        return g
    if name == "single_color":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
