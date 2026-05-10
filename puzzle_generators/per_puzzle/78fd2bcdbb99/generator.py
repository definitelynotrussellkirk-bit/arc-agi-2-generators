"""Generator for ce0c6312.

Rule: count LR/UD mismatches; use axis with fewer; for each empty cell
with non-zero mirror, copy.

Combinatorial axes (8): grid_h/w, color, density, palette_kind,
n_missing, anchor_corner, asymmetry_force, palette_size.
Degenerates: full_symmetric, no_pattern, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "78fd2bcdbb99"
VERSION = "1.1.0"
TASK_ID = "78fd2bcdbb99"
SUMMARY = "Mostly lr-symmetric pattern with one missing cell that has a non-zero mirror."

INVARIANTS = [
    "pattern is approximately lr-symmetric",
    "at least one empty cell has a non-zero lr-mirror",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("full_symmetric", "no_pattern", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "color":          {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "density":        {"type": "float", "default": "0.4", "valid": "0.2..0.6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_missing":      {"type": "int", "default": "1", "valid": "1..3"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
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
        h_lo, h_hi, w_lo, w_hi = 4, 5, 5, 7
        d_default = 0.3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 8, 10, 11, 14
        d_default = 0.5
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 7, 7, 9
        d_default = 0.4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("color",
                              rng.choice(pal) if pal else
                              rng.choice([2, 3, 4, 5])))
    density = float(overrides.get("density", d_default))
    density = max(0.1, min(0.7, density))
    for r in range(1, h - 1):
        for c in range(1, w // 2):
            if rng.random() < density:
                g[r][c] = color
                g[r][w - 1 - c] = color
    n_missing = int(overrides.get("n_missing",
                                  ctx.draw_int("n_missing", 1, 2)))
    n_missing = max(1, min(3, n_missing))
    for _ in range(n_missing):
        for _ in range(20):
            r = rng.randint(1, h - 2); c = rng.randint(1, max(1, w // 2 - 1))
            if g[r][c] == color:
                g[r][w - 1 - c] = 0
                break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4, 5]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "full_symmetric":
        for r in range(1, h - 1):
            for c in range(1, w // 2):
                g[r][c] = 3
                g[r][w - 1 - c] = 3
        return g
    if name == "no_pattern":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
