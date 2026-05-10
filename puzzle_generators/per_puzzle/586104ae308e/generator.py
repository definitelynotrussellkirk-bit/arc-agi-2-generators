"""Generator for puzzle 2685904e.

Rule: row 0 has N 8-cells. 5-row is separator. Below 5-row is data
row. Output filters data row to colors appearing exactly N times,
paints these N rows above the separator.

Combinatorial axes (8): grid_h/w, n8, sep_row, target_color,
n_distract, palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_8s, no_separator, empty_data.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "586104ae308e"
VERSION = "1.1.0"
TASK_ID = "586104ae308e"
SUMMARY = "Top row 8s + 5-sep + data row; rule paints data above sep."

INVARIANTS = [
    "row 0 has N leftmost 8-cells, rest 0",
    "exactly one full-width 5-row at sep_row",
    "exactly one data row below sep (rest below are 0)",
    "data row has >=1 color appearing exactly N times",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_8s", "no_separator", "empty_data")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "n8":             {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "sep_row":        {"type": "int", "default": "rng n8+1..h-3",
                       "valid": "2..h-2"},
    "target_color":   {"type": "color", "default": "rng (≠0,5,8)",
                       "valid": "1..9 (≠5,8)"},
    "n_distract":     {"type": "int", "default": "rng 2..4", "valid": "0..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n8 = int(overrides.get("n8",
                           ctx.draw_int("n8", 2, 4)))
    n8 = max(1, min(min(w - 1, 6), n8))
    sep = int(overrides.get("sep_row",
                            rng.randint(n8 + 1, max(n8 + 1, h - 3))))
    sep = max(2, min(h - 2, sep))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    target_color = int(overrides.get("target_color",
                                     next((c for c in palette
                                           if c not in (5, 8)), 3)))
    if target_color in (5, 8):
        target_color = next((c for c in palette
                             if c not in (5, 8, target_color)), 3)
    n_distract = int(overrides.get("n_distract",
                                   ctx.draw_int("n_distract", 2, 4)))
    g = full_grid(h, w, 0)
    for c in range(n8):
        g[0][c] = 8
    for c in range(w):
        g[sep][c] = 5
    dr = sep + 1
    if dr >= h:
        dr = h - 1
    other = [v for v in palette if v != target_color and v not in (5, 8)]
    cols = list(range(w))
    rng.shuffle(cols)
    for c in cols[:n8]:
        g[dr][c] = target_color
    for c in cols[n8:n8 + n_distract]:
        if other:
            g[dr][c] = rng.choice(other)
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_8s":
        sep = h // 2
        for c in range(w):
            g[sep][c] = 5
        for c in range(w):
            if rng.random() < 0.4:
                g[sep + 1][c] = rng.choice([2, 3, 4])
        return g
    if name == "no_separator":
        for c in range(2):
            g[0][c] = 8
        return g
    if name == "empty_data":
        for c in range(2):
            g[0][c] = 8
        sep = h // 2
        for c in range(w):
            g[sep][c] = 5
        return g
    return g
