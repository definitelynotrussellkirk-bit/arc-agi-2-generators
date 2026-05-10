"""Generator for 22806e14.

Rule: 2 colors on 7-bg: marker (least cells) and block (most cells);
output decision based on majority shape parity.

Combinatorial axes (8): grid_h/w, palette_kind, n_crosses, n_squares,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: only_crosses, only_blocks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "a2d9d069c7d5"
VERSION = "1.1.0"
TASK_ID = "a2d9d069c7d5"
SUMMARY = "7-bg + 1-2 cross-shapes (color C1) + 1 solid square (color C2)."

INVARIANTS = [
    "bg = 7",
    "1-2 plus-shapes of color C1",
    "1 solid square of color C2 (>=3x3)",
    "C1 != C2, both not 7",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("only_crosses", "only_blocks", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_crosses":      {"type": "int", "default": "1", "valid": "1..3"},
    "n_squares":      {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered|spread|rng"},
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
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = [[7] * w for _ in range(h)]
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    cross_color = pal[0]
    block_color = pal[1] if len(pal) > 1 else 4
    n_crosses = int(overrides.get("n_crosses", 1))
    for _ in range(n_crosses):
        for _try in range(40):
            r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
            if all(g[r + dr][c + dc] == 7
                   for dr in [-1, 0, 1] for dc in [-1, 0, 1]):
                for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                    g[r + dr][c + dc] = cross_color
                break
    n_squares = int(overrides.get("n_squares", 1))
    for _ in range(n_squares):
        for _try in range(40):
            sz = rng.randint(3, 4)
            r0 = rng.randint(1, h - sz - 1); c0 = rng.randint(1, w - sz - 1)
            if all(g[r0 + dr][c0 + dc] == 7
                   for dr in range(-1, sz + 1)
                   for dc in range(-1, sz + 1)
                   if 0 <= r0 + dr < h and 0 <= c0 + dc < w):
                draw_rect(g, r0, c0, sz, sz, block_color)
                break
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c != 7]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = [[7] * w for _ in range(h)]
    if name == "only_crosses":
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            g[7 + dr][7 + dc] = 2
        return g
    if name == "only_blocks":
        draw_rect(g, 4, 4, 3, 3, 3)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 7
        return g
    return g
