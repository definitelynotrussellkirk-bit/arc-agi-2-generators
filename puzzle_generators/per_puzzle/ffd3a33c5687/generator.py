"""Generator for puzzle 411bd042.

Rule: LR mirror-completion. For each cell (r, c), pair with mirror
(r, w-1-c). If either is non-zero, output that value (left priority).

Combinatorial axes (8): grid_h/w, n_cells, palette_kind, palette_size,
position_bias, anchor_corner, asymmetry_force, side_bias.
Degenerates: full_symmetry, no_cells, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ffd3a33c5687"
VERSION = "1.1.0"
TASK_ID = "ffd3a33c5687"
SUMMARY = "Asymmetric cells; rule mirrors LR + merges."

INVARIANTS = [
    "background is 0",
    "between 3-8 colored cells",
    ">=1 cell whose mirror is empty",
]

POSITION_BIASES = ("scattered", "left_heavy", "right_heavy",
                   "diagonal", "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("full_symmetry", "no_cells", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "n_cells":        {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
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
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 9, 12
    else:
        h_lo, h_hi = 5, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_cells = int(overrides.get("n_cells",
                                ctx.draw_int("n_cells", 4, 7)))
    n_cells = max(3, min(10, n_cells))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 2, 4)))
    palette = _build_palette(palette_kind,
                             max(1, min(6, palette_size)),
                             rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    g = full_grid(h, w, 0)
    candidates = _candidates(bias, h, w, rng)
    placed = 0
    for r, c in candidates:
        if placed >= n_cells:
            break
        if g[r][c] == 0:
            g[r][c] = rng.choice(palette)
            placed += 1
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
    return pool[:n]


def _candidates(bias, h, w, rng):
    cells = [(r, c) for r in range(h) for c in range(w)]
    if bias == "left_heavy":
        cells = [p for p in cells if p[1] < w // 2]
        rng.shuffle(cells)
        return cells
    if bias == "right_heavy":
        cells = [p for p in cells if p[1] >= w // 2]
        rng.shuffle(cells)
        return cells
    if bias == "diagonal":
        return [(i, i) for i in range(min(h, w))] + cells
    if bias == "centered":
        cr, cc = h // 2, w // 2
        cells.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return cells
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "full_symmetry":
        # Symmetric LR pattern → rule has no asymmetry to merge
        c = rng.choice([2, 3, 4])
        g[h // 2][0] = c
        g[h // 2][w - 1] = c
        return g
    if name == "no_cells":
        return g
    if name == "full_grid":
        for r in range(h):
            for cc in range(w):
                g[r][cc] = rng.choice([2, 3, 4])
        return g
    return g
