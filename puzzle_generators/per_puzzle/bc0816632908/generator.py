"""Generator for 7447852a.

Rule: 2-bg grid with isolated 0-cells (each a separate 4-component).
Sort components by leftmost col; indices 0, 3, 6, ... recolor from 0 to 4.

Combinatorial axes (8): grid_h/w, n_zeros, zero_layout, min_zero_spacing,
column_distribution, decoy_palette_size, decoy_density, vertical_bias.
Degenerates: single_zero, no_zeros, all_zeros_one_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bc0816632908"
VERSION = "1.1.0"
TASK_ID = "bc0816632908"
SUMMARY = "2-bg grid with isolated 0-cells; rule recolors every 3rd by left-edge."

INVARIANTS = [
    "background is 2",
    "≥4 isolated 0-cells (each its own 4-component on 2-bg)",
    "no two 0-cells share a 4-edge (so each is a separate component)",
    "all components have distinct leftmost columns (sort is unambiguous)",
]

ZERO_LAYOUTS = ("scattered", "row_aligned", "diagonal", "ascending", "random")
DEGENERATE_TEXTURES = ("single_zero", "no_zeros", "all_zeros_one_col")
HELPFUL_TEXTURES = ZERO_LAYOUTS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 3..6", "valid": "3..10"},
    "grid_w":              {"type": "int", "default": "rng 12..18", "valid": "10..24"},
    "n_zeros":             {"type": "int", "default": "rng 4..8", "valid": "1..12"},
    "zero_layout":         {"type": "str", "default": "rng helpful",
                            "valid": "|".join(ZERO_LAYOUTS)},
    "min_zero_spacing":    {"type": "int", "default": "2", "valid": "1..3"},
    "column_distribution": {"type": "str", "default": "rng even|spread",
                            "valid": "even|spread"},
    "decoy_palette_size":  {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "decoy_density":       {"type": "float", "default": "rng 0..0.05",
                            "valid": "0..0.15"},
    "texture":             {"type": "str", "default": "alias for zero_layout",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 3, 4, 10, 13, 4, 5
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 5, 7, 16, 22, 7, 12
    else:
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 3, 6, 12, 18, 4, 8
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_zeros = int(overrides.get("n_zeros", ctx.draw_int("n_zeros", n_lo, n_hi)))
    n_zeros = max(4, min(12, n_zeros))
    layout = (overrides.get("texture") or overrides.get("zero_layout")
              or ctx.draw_choice("zero_layout", list(ZERO_LAYOUTS)))
    spacing = int(overrides.get("min_zero_spacing", 2))
    g = full_grid(h, w, 2)
    placed = _layout_zeros(layout, h, w, n_zeros, spacing, rng)
    for r, c in placed:
        g[r][c] = 0
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 2)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.05)))
    decoy_pool = [c for c in range(1, 10) if c not in (0, 2, 4)]
    rng.shuffle(decoy_pool)
    decoy_palette = decoy_pool[:max(0, n_decoy)]
    if decoy_palette and decoy_d > 0:
        for r in range(h):
            for c in range(w):
                if g[r][c] == 2 and rng.random() < decoy_d:
                    if not any(g[nr][nc] == 0
                               for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                               if 0 <= nr < h and 0 <= nc < w):
                        g[r][c] = rng.choice(decoy_palette)
    return g


def _layout_zeros(layout, h, w, n, spacing, rng):
    placed = []

    def ok(r, c):
        return all(abs(pr - r) + abs(pc - c) >= spacing for pr, pc in placed)

    if layout == "diagonal":
        for k in range(min(h, w)):
            if ok(k, k):
                placed.append((k, k))
            if len(placed) >= n:
                return placed
    if layout == "ascending":
        cols = sorted(rng.sample(range(w), min(n, w)))
        for c in cols:
            r = rng.randint(0, h - 1)
            for _ in range(20):
                if ok(r, c):
                    placed.append((r, c))
                    break
                r = (r + 1) % h
            if len(placed) >= n:
                return placed
    if layout == "row_aligned":
        cols = sorted(rng.sample(range(w), min(n, w)))
        r = rng.randint(0, h - 1)
        for c in cols:
            if ok(r, c):
                placed.append((r, c))
            if len(placed) >= n:
                return placed
    if layout == "scattered":
        cells = [(r, c) for r in range(0, h, 2) for c in range(0, w, 2)]
        rng.shuffle(cells)
        for r, c in cells:
            if ok(r, c):
                placed.append((r, c))
            if len(placed) >= n:
                return placed
    for _ in range(80):
        if len(placed) >= n:
            break
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if ok(r, c):
            placed.append((r, c))
    return placed


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 2)
    if name == "single_zero":
        g[h // 2][w // 2] = 0
        return g
    if name == "no_zeros":
        return g
    if name == "all_zeros_one_col":
        c = w // 2
        for r in range(0, h, 2):
            g[r][c] = 0
        return g
    return g
