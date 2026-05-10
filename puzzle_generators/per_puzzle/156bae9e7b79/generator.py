"""Generator for puzzle bae5c565.

Rule: bg=5, row-0 keys + vertical cyan(8) line. Output expands each
key as triangle radiating from line-top, radius growing per row.

Combinatorial axes (8): grid_h/w, n_keys, palette_kind, line_col_bias,
line_height, anchor_corner, asymmetry_force, key_density.
Degenerates: no_keys, no_line, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "156bae9e7b79"
VERSION = "1.1.0"
TASK_ID = "156bae9e7b79"
SUMMARY = "bg=5 + row-0 keys + cyan line; rule expands keys as triangles."

INVARIANTS = [
    "background is 5",
    "row 0 contains varied non-{0,5,8} keys",
    "exactly 1 col has 8s extending vertically (the line)",
    "line col in middle 1/3 horizontally so triangles fit",
]

LINE_COL_BIASES = ("center", "left_third", "right_third", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_keys", "no_line", "full_grid")
HELPFUL_TEXTURES = LINE_COL_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "n_keys":         {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "line_col_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LINE_COL_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "key_density":    {"type": "float", "default": "rng 0.3..0.6",
                       "valid": "0.2..1"},
    "texture":        {"type": "str", "default": "alias for line_col_bias",
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
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_keys = int(overrides.get("n_keys",
                               ctx.draw_int("n_keys", 2, 4)))
    n_keys = max(2, min(6, n_keys))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_keys, rng)
    bias = (overrides.get("texture") or
            overrides.get("line_col_bias")
            or ctx.draw_choice("line_col_bias",
                               list(LINE_COL_BIASES)))
    density = float(overrides.get("key_density",
                                  ctx.draw_rng("key_density")
                                  .uniform(0.3, 0.6)))
    g = full_grid(h, w, 5)
    for c in range(w):
        if rng.random() < density:
            g[0][c] = rng.choice(palette)
    line_col = _pick_line_col(bias, w, rng)
    line_top = rng.randint(1, max(1, h // 3))
    line_bot = rng.randint(2 * h // 3, h - 1)
    for r in range(line_top, line_bot + 1):
        g[r][line_col] = 8
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 9]
    pool = [c for c in pool if c not in (5, 8)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 9]:
            if c not in pool and c not in (5, 8):
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _pick_line_col(bias, w, rng):
    if bias == "center":
        return w // 2
    if bias == "left_third":
        return rng.randint(w // 3, max(w // 3, w // 2 - 1))
    if bias == "right_third":
        return rng.randint(w // 2 + 1, max(w // 2 + 1, 2 * w // 3))
    return rng.randint(w // 3, max(w // 3, 2 * w // 3))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 5)
    if name == "no_keys":
        line_col = w // 2
        for r in range(1, h):
            g[r][line_col] = 8
        return g
    if name == "no_line":
        for c in range(0, w, 2):
            g[0][c] = rng.choice([2, 3, 4])
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
