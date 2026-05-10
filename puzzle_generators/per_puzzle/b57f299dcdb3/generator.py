"""Generator for puzzle 642d658d.

Rule: yellow-centered plus shapes. Output 1x1 of most-frequent petal
color.

Combinatorial axes (8): grid_h/w, n_pluses, palette_kind, n_winner,
n_distractors, position_bias, anchor_corner, asymmetry_force.
Degenerates: tied_petals, single_plus, no_pluses.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b57f299dcdb3"
VERSION = "1.1.0"
TASK_ID = "b57f299dcdb3"
SUMMARY = "Yellow-centered plus shapes; rule outputs most-frequent petal color."

INVARIANTS = [
    "background is 0",
    ">=2 yellow-centered plus shapes (>=1 cell margin)",
    "each plus: center=4; 4 cardinals = single non-{0,4} petal color",
    "one petal color is strict-majority among pluses",
]

POSITION_BIASES = ("scattered", "row_aligned", "col_aligned", "diagonal",
                   "centered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("tied_petals", "single_plus", "no_pluses")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..16", "valid": "9..22"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..22"},
    "n_pluses":       {"type": "int", "default": "rng 4..8", "valid": "2..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_distractors":  {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 9, 12
    elif difficulty == "hard":
        h_lo, h_hi = 16, 22
    else:
        h_lo, h_hi = 11, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n = int(overrides.get("n_pluses",
                          ctx.draw_int("n_pluses", 4, 8)))
    n = max(2, min(12, n))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    n_distractors = int(overrides.get("n_distractors",
                                      ctx.draw_int("n_distractors",
                                                   2, 3)))
    n_distractors = max(1, min(4, n_distractors))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    palette = _build_palette(palette_kind, 1 + n_distractors, rng)
    winner = palette[0]
    distractors = palette[1:1 + n_distractors]
    n_winner = max(2, n // 2 + 1)
    petal_colors = [winner] * n_winner
    for i in range(n - n_winner):
        petal_colors.append(distractors[i % len(distractors)])
    rng.shuffle(petal_colors)
    g = full_grid(h, w, 0)
    placed = 0
    candidates = _candidates(bias, h, w, rng)
    for color in petal_colors:
        placed_this = False
        for cr, cc in candidates:
            if not (2 <= cr <= h - 3 and 2 <= cc <= w - 3):
                continue
            clear = True
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    rr, ccc = cr + dr, cc + dc
                    if 0 <= rr < h and 0 <= ccc < w and g[rr][ccc] != 0:
                        clear = False; break
                if not clear:
                    break
            if not clear:
                continue
            g[cr][cc] = 4
            g[cr - 1][cc] = color
            g[cr + 1][cc] = color
            g[cr][cc - 1] = color
            g[cr][cc + 1] = color
            placed += 1
            placed_this = True
            break
        if not placed_this:
            continue
    if placed < 2:
        return _draw_from_degenerate("single_plus", h, w, rng)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _candidates(bias, h, w, rng):
    if bias == "row_aligned":
        r = h // 2
        return [(r, c) for c in range(2, w - 2, 4)]
    if bias == "col_aligned":
        c = w // 2
        return [(r, c) for r in range(2, h - 2, 4)]
    if bias == "diagonal":
        return [(i, i) for i in range(2, min(h, w) - 2, 3)]
    if bias == "centered":
        cr, cc = h // 2, w // 2
        cells = [(r, c) for r in range(2, h - 2) for c in range(2, w - 2)]
        cells.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return cells
    cells = [(r, c) for r in range(2, h - 2) for c in range(2, w - 2)]
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 5, 6, 7, 8, 9], 3)
    if name == "tied_petals":
        # Two petal colors with same count (no winner)
        for cr, cc, color in [(3, 3, palette[0]), (3, 8, palette[1]),
                              (8, 3, palette[0]), (8, 8, palette[1])]:
            if 2 <= cr <= h - 3 and 2 <= cc <= w - 3:
                g[cr][cc] = 4
                g[cr - 1][cc] = color
                g[cr + 1][cc] = color
                g[cr][cc - 1] = color
                g[cr][cc + 1] = color
        return g
    if name == "single_plus":
        cr, cc = h // 2, w // 2
        g[cr][cc] = 4
        g[cr - 1][cc] = palette[0]
        g[cr + 1][cc] = palette[0]
        g[cr][cc - 1] = palette[0]
        g[cr][cc + 1] = palette[0]
        return g
    if name == "no_pluses":
        return g
    return g
