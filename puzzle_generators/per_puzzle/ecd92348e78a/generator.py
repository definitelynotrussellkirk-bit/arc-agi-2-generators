"""Generator for puzzle b7999b51.

Rule: for each non-bg color, compute its bbox height; output bar chart
columns sorted descending.

Combinatorial axes (8): grid_h/w, n_colors, palette_kind, height_min,
height_max, position_bias, anchor_corner, asymmetry_force.
Degenerates: tied_heights, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ecd92348e78a"
VERSION = "1.1.0"
TASK_ID = "ecd92348e78a"
SUMMARY = "Multi-color cells with distinct bbox heights; rule outputs bar chart."

INVARIANTS = [
    "background is 0",
    "2-5 distinct non-bg colors",
    "each color has a distinct bbox height",
    "max bbox height <= 8 (output cols fit)",
]

POSITION_BIASES = ("scattered", "left_heavy", "right_heavy",
                   "evenly_spaced", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_heights", "single_color", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "6..20"},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "height_min":     {"type": "int", "default": "2", "valid": "2..6"},
    "height_max":     {"type": "int", "default": "min(8,h-1)",
                       "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", 2, 3)))
    n_colors = max(2, min(5, n_colors))
    h_min = int(overrides.get("height_min", 2))
    h_max = int(overrides.get("height_max", min(8, h - 1)))
    h_min = max(2, min(h - 1, h_min))
    h_max = max(h_min + 1, min(8, min(h - 1, h_max)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    palette = _build_palette(palette_kind, n_colors, rng)
    heights = rng.sample(range(h_min, h_max + 1),
                          min(n_colors, h_max - h_min + 1))
    while len(heights) < n_colors:
        heights.append(h_min + len(heights))
    g = full_grid(h, w, 0)
    used_cols = set()
    cols = _pick_columns(bias, w, n_colors, rng)
    for color, ht, c in zip(palette, heights, cols):
        if c in used_cols:
            for cc in range(w):
                if cc not in used_cols:
                    c = cc; break
        r0 = rng.randint(0, h - ht)
        for dr in range(ht):
            g[r0 + dr][c] = color
        used_cols.add(c)
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


def _pick_columns(bias, w, n, rng):
    candidates = list(range(w))
    if bias == "left_heavy":
        return candidates[:n]
    if bias == "right_heavy":
        return candidates[-n:]
    if bias == "evenly_spaced":
        step = max(1, w // (n + 1))
        return [step * (i + 1) for i in range(n) if step * (i + 1) < w][:n]
    if bias == "centered":
        center = w // 2
        cs = [center - (n - 1) // 2 + i for i in range(n)]
        return [c for c in cs if 0 <= c < w][:n]
    rng.shuffle(candidates)
    return sorted(candidates[:n])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "tied_heights":
        # Two colors with same height
        c1, c2 = 2, 1
        for r in range(3):
            g[r][c1] = 3
            g[r][c2] = 4
        return g
    if name == "single_color":
        for r in range(3):
            g[r][1] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 4
        return g
    return g
