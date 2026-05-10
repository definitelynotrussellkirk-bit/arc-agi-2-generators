"""Generator for puzzle 1a2e2828.

Rule: find a row uniformly one non-zero color → output 1x1 of that
color. Otherwise find row with single anomaly and output that.

Combinatorial axes (8): grid_h/w, clean_color, clean_row,
n_distract_rows, distract_density, palette_kind, anchor_corner,
asymmetry_force.
Degenerates: no_clean_row, all_clean, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7b0cb3b9a618"
VERSION = "1.1.0"
TASK_ID = "7b0cb3b9a618"
SUMMARY = "Rows w/ 1 clean row; rule outputs 1x1 of clean color."

INVARIANTS = [
    "background is 0",
    "exactly 1 row is uniform non-zero (the clean row)",
    "other rows have mixed content",
]

ROW_POSITIONS = ("top", "middle", "bottom", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_clean_row", "all_clean", "monochrome")
HELPFUL_TEXTURES = ROW_POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "clean_color":    {"type": "color", "default": "rng (≠0)",
                       "valid": "1..9"},
    "clean_row_pos":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ROW_POSITIONS)},
    "n_distract_rows":{"type": "int", "default": "rng 2..5",
                       "valid": "1..8"},
    "distract_density":{"type": "float", "default": "rng 0.5..0.8",
                        "valid": "0.3..1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for clean_row_pos",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    clean_color = int(overrides.get("clean_color", palette[0]))
    if clean_color == 0:
        clean_color = palette[0] if palette[0] != 0 else 1
    pos = (overrides.get("texture") or
           overrides.get("clean_row_pos")
           or ctx.draw_choice("clean_row_pos",
                              list(ROW_POSITIONS)))
    if pos == "top":
        clean_row = rng.randint(0, max(0, h // 3))
    elif pos == "middle":
        clean_row = h // 2
    elif pos == "bottom":
        clean_row = rng.randint(2 * h // 3, h - 1)
    else:
        clean_row = rng.randint(2, h - 2)
    n_distract = int(overrides.get("n_distract_rows",
                                   ctx.draw_int("n_distract_rows", 2, 5)))
    n_distract = max(1, min(8, n_distract))
    density = float(overrides.get("distract_density",
                                  ctx.draw_rng("distract_density")
                                  .uniform(0.5, 0.8)))
    g = full_grid(h, w, 0)
    for c in range(w):
        g[clean_row][c] = clean_color
    other = [v for v in palette if v != clean_color]
    for _ in range(n_distract):
        r = rng.randint(0, h - 1)
        if r == clean_row:
            continue
        v = rng.choice(other)
        for c in range(w):
            if rng.random() < density:
                g[r][c] = v
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_clean_row":
        for r in range(h):
            for c in range(w):
                if rng.random() < 0.4:
                    g[r][c] = rng.choice([1, 2, 3, 4])
        return g
    if name == "all_clean":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    if name == "monochrome":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(h):
            for cc in range(w):
                g[r][cc] = c
        return g
    return g
