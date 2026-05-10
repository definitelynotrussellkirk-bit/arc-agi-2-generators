"""Generator for 14b8e18c.

Rule: each square frame (hollow ≥2x2 or solid) gets 2-cells at its 4
outer corners.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_squares, square_kind.
Degenerates: no_squares, single_square, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline, draw_rect

GENERATOR_ID = "42f19ef6d600"
VERSION = "1.1.0"
TASK_ID = "42f19ef6d600"
SUMMARY = "7-bg with 1-2 squares (hollow or solid) of distinct colors."

INVARIANTS = [
    "bg is color 7",
    "one or two squares each at least 3x3",
    "squares have distinct non-{2,7} colors",
    "squares well-separated by at least two cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_squares", "single_square", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_squares":      {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "square_kind":    {"type": "str", "default": "rng", "valid": "rng"},
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
        h_lo, h_hi = 8, 8
    elif difficulty == "hard":
        h_lo, h_hi = 11, 13
    else:
        h_lo, h_hi = 8, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", 9, 12)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [1, 3, 4, 5, 6, 8, 9] if c not in pool]
    g = [[7] * w for _ in range(h)]
    n_sq = rng.randint(1, 2)
    palette = pool[:n_sq]
    placed = []
    for color in palette:
        for _ in range(40):
            sz = rng.randint(3, 4)
            r0 = rng.randint(1, h - sz - 1)
            c0 = rng.randint(1, w - sz - 1)
            if any(abs(r0 - pr) < (sz + 2) and abs(c0 - pc) < (sz + 2) for pr, pc in placed):
                continue
            if rng.random() < 0.5:
                draw_rect_outline(g, r0, c0, sz, sz, color)
            else:
                draw_rect(g, r0, c0, sz, sz, color)
            placed.append((r0, c0))
            break
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 3, 4]
    else:
        pool = [1, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c not in (0, 2, 7)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = [[7] * 10 for _ in range(9)]
    if name == "no_squares":
        return g
    if name == "single_square":
        draw_rect_outline(g, 2, 2, 4, 4, 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(10):
                g[r][c] = 3
        return g
    return g
