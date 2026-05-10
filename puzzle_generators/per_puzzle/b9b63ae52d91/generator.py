"""Generator for puzzle a8610ef7.

Rule: `(rule! (lambda (g) (cellmap g (r c v) (if (= v 8) (if (= (at g (- (- h 1) r) c) 8) 2 5) 0))))`.
For each cyan(8) cell: if its vertical mirror (h-1-r, c) is also 8,
output 2 (red); else output 5 (gray). Non-8 cells become 0.

Combinatorial axes:
  * grid_h / grid_w     — outer canvas size
  * n_pairs             — vertically-symmetric cyan pairs
  * n_solo              — asymmetric cyans (no UD-mirror partner)
  * pair_layout         — random / cluster / row / column / diagonal
  * solo_layout         — random / cluster / row / column / diagonal
  * caller-opt-in degenerates: all_pairs (output all 2s + 0s),
                               all_solo (output all 5s + 0s),
                               only_axis_cyans (cells on horizontal
                               axis are trivially symmetric)
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9b63ae52d91"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "b9b63ae52d91"
SUMMARY = "Cyan cells; rule paints UD-symmetric pairs red, asymmetric cyans gray, others 0."

INVARIANTS = [
    "background is 0",
    "all non-bg cells are cyan(8)",
    "≥1 vertically-symmetric pair (r, c) ↔ (h-1-r, c)",
    "≥1 asymmetric cyan (no UD mirror partner)",
]

LAYOUTS = ("random", "cluster", "row", "column", "diagonal")
DEGENERATE_TEXTURES = ("all_pairs", "all_solo", "only_axis_cyans")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":      {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "grid_w":      {"type": "int", "default": "rng 6..14", "valid": "5..18"},
    "n_pairs":     {"type": "int", "default": "rng 2..5",  "valid": "1..8"},
    "n_solo":      {"type": "int", "default": "rng 2..5",  "valid": "1..8"},
    "pair_layout": {"type": "str", "default": "rng helpful",
                    "valid": "|".join(LAYOUTS)},
    "solo_layout": {"type": "str", "default": "rng helpful",
                    "valid": "|".join(LAYOUTS)},
    "texture":     {"type": "str", "default": "alias for pair_layout",
                    "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, p_lo, p_hi = 6, 8, 1, 2
    elif difficulty == "hard":
        h_lo, h_hi, p_lo, p_hi = 11, 14, 4, 6
    else:
        h_lo, h_hi, p_lo, p_hi = 6, 14, 2, 5

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

    n_pairs = int(overrides.get("n_pairs",
                                ctx.draw_int("n_pairs", p_lo, p_hi)))
    n_solo = int(overrides.get("n_solo",
                               ctx.draw_int("n_solo", p_lo, p_hi)))
    pair_layout = (overrides.get("texture")
                   or overrides.get("pair_layout")
                   or ctx.draw_choice("pair_layout", list(LAYOUTS)))
    solo_layout = overrides.get(
        "solo_layout",
        ctx.draw_choice("solo_layout", list(LAYOUTS)))

    g = full_grid(h, w, 0)
    pair_candidates = _layout_for(pair_layout, h, w, rng, half_h=True)
    placed_pairs = 0
    for (r, c) in pair_candidates:
        if placed_pairs >= n_pairs:
            break
        mirror_r = h - 1 - r
        if r == mirror_r:
            continue
        if g[r][c] != 0 or g[mirror_r][c] != 0:
            continue
        g[r][c] = 8; g[mirror_r][c] = 8
        placed_pairs += 1

    solo_candidates = _layout_for(solo_layout, h, w, rng, half_h=False)
    placed_solo = 0
    for (r, c) in solo_candidates:
        if placed_solo >= n_solo:
            break
        mirror_r = h - 1 - r
        if r == mirror_r:
            continue
        if g[r][c] != 0 or g[mirror_r][c] != 0:
            continue
        g[r][c] = 8
        placed_solo += 1

    if placed_pairs < 1:
        for r in range(h // 2):
            for c in range(w):
                mr = h - 1 - r
                if g[r][c] == 0 and g[mr][c] == 0 and r != mr:
                    g[r][c] = 8; g[mr][c] = 8
                    break
            else:
                continue
            break
    if placed_solo < 1:
        for r in range(h):
            for c in range(w):
                mr = h - 1 - r
                if g[r][c] == 0 and g[mr][c] == 0 and r != mr:
                    g[r][c] = 8
                    return g
    return g


def _layout_for(layout, h, w, rng, half_h):
    rmax = h // 2 if half_h else h
    cells = [(r, c) for r in range(rmax) for c in range(w)]
    if layout == "cluster":
        cr = rng.randint(0, max(0, rmax - 1)); cc = rng.randint(0, w - 1)
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
    elif layout == "row":
        r = rng.randint(0, max(0, rmax - 1))
        cells = [(r, c) for c in range(w)]
        rng.shuffle(cells)
    elif layout == "column":
        c = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(rmax)]
        rng.shuffle(cells)
    elif layout == "diagonal":
        cells = [(k, k) for k in range(min(rmax, w))]
        rng.shuffle(cells)
    else:
        rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the UD-symmetry signal collapses.

    all_pairs        — every cyan has a UD-mirror; output: 2s and 0s only.
    all_solo         — no UD-symmetric pair; output: 5s and 0s only.
    only_axis_cyans  — cyans only on the central row (its own mirror);
                        these are trivially "symmetric" — visually subtle.
    """
    g = full_grid(h, w, 0)
    if name == "all_pairs":
        for c in range(w):
            for r in range(h // 2):
                if rng.random() < 0.4:
                    g[r][c] = 8
                    g[h - 1 - r][c] = 8
        return g
    if name == "all_solo":
        for r in range(h):
            for c in range(w):
                mr = h - 1 - r
                if r == mr: continue
                if rng.random() < 0.20 and g[r][c] == 0 and g[mr][c] == 0:
                    g[r][c] = 8
        return g
    if name == "only_axis_cyans":
        if h % 2 == 0:
            return g
        axis = h // 2
        for c in range(w):
            if rng.random() < 0.5:
                g[axis][c] = 8
        return g
    return g
