"""Generator for puzzle 363442ee.

Rule: 3x3 template at TL + 5-col divider + 1-cells in the right region.
Output: stamps the TL template centered on each 1-cell.

Combinatorial axes (8): grid_h/w, n_dots, palette_kind, palette_size,
template_density, position_bias, anchor_corner, asymmetry_force.
Degenerates: no_dots, no_template, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28423cdf02cc"
VERSION = "1.1.0"
TASK_ID = "28423cdf02cc"
SUMMARY = "3x3 template + 5-divider + 1-cells; rule stamps template at each 1."

INVARIANTS = [
    "rows 0-2, cols 0-2 contain a 3x3 colored template",
    "col 3 is full-height 5-divider",
    "cols 4..w-1, rows 3+ have 2-4 single 1-cells",
    "1-cells at interior positions so stamp fits",
]

POSITION_BIASES = ("scattered", "row_aligned", "col_aligned", "diagonal",
                   "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "no_template", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "n_dots":         {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..6"},
    "template_density":{"type": "float", "default": "rng 0.5..0.9",
                        "valid": "0.3..1"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 7, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 4, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_dots = int(overrides.get("n_dots",
                               ctx.draw_int("n_dots", 2, 4)))
    n_dots = max(1, min(6, n_dots))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size", 3))
    palette = _build_palette(palette_kind,
                             max(2, min(6, palette_size)),
                             rng)
    density = float(overrides.get("template_density",
                                  ctx.draw_rng("template_density")
                                  .uniform(0.5, 0.9)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    for r in range(3):
        for c in range(3):
            if rng.random() < density:
                g[r][c] = rng.choice(palette)
    # Ensure template not all-bg
    if not any(g[r][c] != 0 for r in range(3) for c in range(3)):
        g[1][1] = palette[0]
    for r in range(h):
        g[r][3] = 5
    candidates = _candidates(bias, h, w, rng)
    placed = 0
    seen = []
    for r, c in candidates:
        if placed >= n_dots:
            break
        if not (2 <= r <= h - 2 and 5 <= c <= w - 2):
            continue
        if any(abs(r - pr) + abs(c - pc) < 5 for pr, pc in seen):
            continue
        if g[r][c] == 0:
            g[r][c] = 1
            seen.append((r, c))
            placed += 1
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _candidates(bias, h, w, rng):
    if bias == "row_aligned":
        r = h // 2
        return [(r, c) for c in range(5, w - 1, 4)]
    if bias == "col_aligned":
        c = (w + 5) // 2
        return [(r, c) for r in range(2, h - 1, 3)]
    if bias == "diagonal":
        return [(2 + i, 5 + i) for i in range(min(h - 4, w - 6))]
    if bias == "centered":
        cr, cc = h // 2, (w + 5) // 2
        cells = [(r, c) for r in range(2, h - 1) for c in range(5, w - 1)]
        cells.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return cells
    cells = [(r, c) for r in range(2, h - 1) for c in range(5, w - 1)]
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][3] = 5
    if name == "no_dots":
        for r in range(3):
            for c in range(3):
                g[r][c] = rng.choice([2, 3, 4])
        return g
    if name == "no_template":
        g[h // 2][8] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
