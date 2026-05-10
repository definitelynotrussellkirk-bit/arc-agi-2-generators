"""Generator for puzzle 8403a5d5.

Rule: bg + 1 non-bg seed at bottom row. Output renders vertical
stripes from the seed col, alternating colors with 5-decoration.

Combinatorial axes (8): grid_h/w, bg_color, fg_color, seed_position,
seed_col_bias, anchor_corner, asymmetry_force, palette_kind.
Degenerates: no_seed, full_grid, multiple_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "24247834f3c9"
VERSION = "1.1.0"
TASK_ID = "24247834f3c9"
SUMMARY = "1 seed at bottom row; rule paints periodic vertical stripes."

INVARIANTS = [
    "bg != 5 and != fg",
    "exactly 1 non-bg seed at row h-1",
    "fg != 0 and != 5",
]

SEED_BIASES = ("center", "left_edge", "right_edge", "spread", "near_center")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "full_grid", "multiple_seeds")
HELPFUL_TEXTURES = SEED_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..15", "valid": "3..30"},
    "grid_w":         {"type": "int", "default": "rng 5..15", "valid": "3..30"},
    "bg_color":       {"type": "color", "default": "rng (≠5,fg)",
                       "valid": "0..9 (≠5)"},
    "fg_color":       {"type": "color", "default": "rng (≠5,bg)",
                       "valid": "0..9 (≠5,bg)"},
    "seed_col_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SEED_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for seed_col_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 6
    elif difficulty == "hard":
        h_lo, h_hi = 15, 28
    else:
        h_lo, h_hi = 5, 15
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    bgc = int(overrides.get("bg_color", palette[0]))
    fgc = int(overrides.get("fg_color", palette[1]))
    if bgc == 5: bgc = 0
    if fgc == 5 or fgc == bgc:
        fgc = next((c for c in [1, 2, 3, 4, 6, 7, 8, 9]
                    if c != bgc and c != 5), 1)
    bias = (overrides.get("texture") or
            overrides.get("seed_col_bias")
            or ctx.draw_choice("seed_col_bias", list(SEED_BIASES)))
    g = full_grid(h, w, bgc)
    locc = _pick_seed_col(bias, w, rng)
    g[h - 1][locc] = fgc
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [0, 1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c != 5]
    rng.shuffle(pool)
    while len(pool) < 2:
        for c in [0, 1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool and c != 5:
                pool.append(c)
    return pool[:2]


def _pick_seed_col(bias, w, rng):
    if bias == "center":
        return w // 2
    if bias == "left_edge":
        return 0
    if bias == "right_edge":
        return w - 1
    if bias == "near_center":
        return max(0, min(w - 1, w // 2 + rng.randint(-1, 1)))
    return rng.randint(0, w - 1)


def _draw_from_degenerate(name, h, w, rng):
    bgc = rng.choice([0, 1, 2, 3, 4, 6, 7, 8, 9])
    g = full_grid(h, w, bgc)
    fg = next((c for c in [1, 2, 3, 4, 6, 7, 8, 9]
               if c != bgc and c != 5), 1)
    if name == "no_seed":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = fg
        return g
    if name == "multiple_seeds":
        for c in range(0, w, 2):
            g[h - 1][c] = fg
        return g
    return g
