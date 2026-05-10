"""Generator for ARC task 3618c87e.

Rule: for each non-bottom-row cell with v == 1: → 0. For bottom-row
cell c: if any cell in column c equals 1, → 1, else keep.
Effect: color-1 falls to the bottom row.

Combinatorial axes (8): grid_h/w, n_ones, ones_layout, ones_row_bias,
bottom_row_decoy_density, decoy_palette_size, ones_column_distribution,
non_one_decoy_density.
Degenerates: no_ones, all_in_bottom_row, single_one.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "44d20451ce17"
VERSION = "1.1.0"
TASK_ID = "44d20451ce17"
SUMMARY = "Scattered 1-cells fall to the bottom row; non-1 cells unchanged."

INVARIANTS = [
    "background is 0",
    "≥1 color-1 cell above the bottom row",
]

ONES_LAYOUTS = ("random", "clustered", "row", "column", "diagonal", "scattered", "blob")
ROW_BIASES = ("top", "bottom", "mid", "spread")
COL_DISTRIBUTIONS = ("uniform", "sparse_cols", "all_cols", "one_col")
DEGENERATE_TEXTURES = ("no_ones", "all_in_bottom_row", "single_one")
HELPFUL_TEXTURES = ONES_LAYOUTS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "grid_w":              {"type": "int", "default": "rng 4..14", "valid": "3..18"},
    "n_ones":              {"type": "int", "default": "rng 2..h*w/4", "valid": "1..h*w/2"},
    "ones_layout":         {"type": "str", "default": "rng helpful",
                            "valid": "|".join(ONES_LAYOUTS)},
    "ones_row_bias":       {"type": "str", "default": "rng helpful",
                            "valid": "|".join(ROW_BIASES)},
    "ones_col_dist":       {"type": "str", "default": "rng helpful",
                            "valid": "|".join(COL_DISTRIBUTIONS)},
    "bottom_decoy_density": {"type": "float", "default": "rng 0..0.4", "valid": "0..0.95"},
    "non_one_decoy_density": {"type": "float", "default": "rng 0..0.15", "valid": "0..0.5"},
    "texture":             {"type": "str", "default": "alias for ones_layout",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 4, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_ones = int(overrides.get("n_ones",
                               ctx.draw_int("n_ones", 2, max(2, (h * w) // 4))))
    layout = (overrides.get("texture") or overrides.get("ones_layout")
              or ctx.draw_choice("ones_layout", list(ONES_LAYOUTS)))
    bias = overrides.get("ones_row_bias",
                         ctx.draw_choice("ones_row_bias", list(ROW_BIASES)))
    col_dist = overrides.get("ones_col_dist",
                             ctx.draw_choice("ones_col_dist", list(COL_DISTRIBUTIONS)))
    bot_d = float(overrides.get("bottom_decoy_density",
                                ctx.draw_rng("bottom_decoy_density").uniform(0.0, 0.4)))
    non_d = float(overrides.get("non_one_decoy_density",
                                ctx.draw_rng("non_one_decoy_density").uniform(0.0, 0.15)))
    g = full_grid(h, w, 0)
    candidates = _candidates(bias, col_dist, h, w, rng)
    for r, c in _layout_cells(layout, candidates, n_ones, rng):
        if 0 <= r < h - 1 and 0 <= c < w:
            g[r][c] = 1
    decoy_palette = [c for c in range(2, 10)]
    rng.shuffle(decoy_palette)
    for c in range(w):
        if rng.random() < bot_d:
            g[h - 1][c] = rng.choice(decoy_palette)
    for r in range(h - 1):
        for c in range(w):
            if g[r][c] == 0 and rng.random() < non_d:
                g[r][c] = rng.choice(decoy_palette[:3])
    if not any(g[r][c] == 1 for r in range(h - 1) for c in range(w)):
        g[0][0] = 1
    return g


def _candidates(bias, col_dist, h, w, rng):
    if bias == "top":
        rows = list(range(0, max(1, h // 2)))
    elif bias == "bottom":
        rows = list(range(max(0, h // 2), h - 1))
    elif bias == "mid":
        m = h // 2
        rows = list(range(max(0, m - 1), min(h - 1, m + 2)))
    else:
        rows = list(range(h - 1))
    if col_dist == "sparse_cols":
        cols = rng.sample(range(w), max(1, w // 3))
    elif col_dist == "all_cols":
        cols = list(range(w))
    elif col_dist == "one_col":
        cols = [rng.randint(0, w - 1)]
    else:
        cols = list(range(w))
    return [(r, c) for r in rows for c in cols]


def _layout_cells(layout, candidates, n, rng):
    if not candidates: return []
    n = min(n, len(candidates))
    if layout == "clustered":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return candidates[:n]
    if layout == "row":
        rs = sorted({r for r, _ in candidates})
        if not rs: return []
        r = rng.choice(rs)
        cells = [(r, c) for (rr, c) in candidates if rr == r]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "column":
        cs = sorted({c for _, c in candidates})
        if not cs: return []
        c = rng.choice(cs)
        cells = [(r, c) for (r, cc) in candidates if cc == c]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "diagonal":
        cset = set(candidates)
        return [(k, k) for k in range(25) if (k, k) in cset][:n]
    if layout == "scattered":
        scat = [(r, c) for (r, c) in candidates if (r + c) % 2 == 0]
        rng.shuffle(scat)
        return scat[:n]
    if layout == "blob":
        cr, cc = rng.choice(candidates)
        candidates = sorted(candidates, key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
        return candidates[:n]
    rng.shuffle(candidates)
    return candidates[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_ones":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.3:
                    g[r][c] = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        return g
    if name == "all_in_bottom_row":
        for c in range(w):
            if rng.random() < 0.5:
                g[h - 1][c] = 1
        # Need at least one 1 above bottom for invariant.
        g[0][0] = 1
        return g
    if name == "single_one":
        g[0][0] = 1
        return g
    return g
