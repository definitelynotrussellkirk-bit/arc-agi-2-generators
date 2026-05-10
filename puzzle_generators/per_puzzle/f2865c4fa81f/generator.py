"""Generator for 770cc55f.

Rule: top + bot bars separated by a 2-row; rule fills wider bar's cols
toward sep, restricted to shared cols.

Combinatorial axes (8): grid_h/w, palette_kind, n_more, n_less,
top_wider, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_separator, no_bars, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f2865c4fa81f"
VERSION = "1.1.0"
TASK_ID = "f2865c4fa81f"
SUMMARY = "Tall narrow grid with all-2 sep + top/bot bars; narrower's cols subset of wider's."

INVARIANTS = [
    "exactly one all-2 separator row",
    "top half: exactly one row with a non-zero bar",
    "bot half: exactly one row with a non-zero bar",
    "narrower bar's non-zero cols are a subset of the wider bar's cols",
    "wider bar has strictly more cols than narrower",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separator", "no_bars", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "top_wider":      {"type": "bool", "default": "rng",
                       "valid": "true|false"},
    "n_more":         {"type": "int", "default": "rng 3..w-1", "valid": "2..w"},
    "n_less":         {"type": "int", "default": "rng 1..n_more-1",
                       "valid": "1..w-1"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 9, 11, 4, 5
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 15, 18, 7, 9
    else:
        h_lo, h_hi, w_lo, w_hi = 11, 15, 5, 7
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    sep = h // 2
    for c in range(w):
        g[sep][c] = 2
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    top_color, bot_color = pal[0], pal[1]
    top_wider_o = overrides.get("top_wider")
    if top_wider_o is None:
        top_wider = rng.choice([True, False])
    else:
        top_wider = bool(top_wider_o)
    if top_wider:
        n_more = rng.randint(3, w - 1)
        n_less = rng.randint(1, n_more - 1)
    else:
        n_less = rng.randint(1, w - 2)
        n_more = rng.randint(n_less + 1, w)
    if top_wider:
        top_cols = sorted(rng.sample(range(w), n_more))
        bot_cols = sorted(rng.sample(top_cols, n_less))
    else:
        bot_cols = sorted(rng.sample(range(w), n_more))
        top_cols = sorted(rng.sample(bot_cols, n_less))
    top_bar_row = rng.randint(0, max(0, sep - 2))
    bot_bar_row = rng.randint(min(sep + 2, h - 1), h - 1)
    for c in top_cols:
        g[top_bar_row][c] = top_color
    for c in bot_cols:
        g[bot_bar_row][c] = bot_color
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [1, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 2]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 13, 6
    g = full_grid(h, w, 0)
    if name == "no_separator":
        for c in range(3):
            g[2][c] = 1
            g[10][c + 2] = 3
        return g
    if name == "no_bars":
        for c in range(w):
            g[h // 2][c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
