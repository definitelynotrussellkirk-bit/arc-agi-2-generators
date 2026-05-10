"""Generator for puzzle 45bbe264.

Rule: for each non-bg pixel, draw a horizontal+vertical cross through
it. Cells where crosses of DIFFERENT colors meet become red(2).

Combinatorial axes (8): grid_h/w, n_pixels, palette_kind, palette_size,
position_bias, anchor_corner, asymmetry_force, share_axes.
Degenerates: single_pixel, all_same_axis, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "959992fc8fa9"
VERSION = "1.1.0"
TASK_ID = "959992fc8fa9"
SUMMARY = "Sparse pixels; rule draws crosses; different-color crossings → red."

INVARIANTS = [
    "background is 0",
    ">=2 non-bg pixels of distinct non-bg, non-2 colors",
    ">=1 pair shares neither row nor col",
    "no pixel uses color 2 (rule writes 2 for crossings)",
]

POSITION_BIASES = ("spread", "corners", "diagonal", "edges", "clustered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_pixel", "all_same_axis", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "n_pixels":       {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "share_axes":     {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_pix = int(overrides.get("n_pixels",
                              ctx.draw_int("n_pixels", 3, 5)))
    n_pix = max(2, min(7, n_pix))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    palette = _build_palette(palette_kind,
                             min(n_pix, 4), rng)
    g = full_grid(h, w, 0)
    positions = _pick_positions(bias, h, w, n_pix, rng)
    placed_pos = []
    for r, c in positions:
        if any(pr == r or pc == c for pr, pc in placed_pos):
            continue
        if g[r][c] != 0:
            continue
        g[r][c] = palette[len(placed_pos) % len(palette)]
        placed_pos.append((r, c))
        if len(placed_pos) >= n_pix:
            break
    if len(placed_pos) < 2:
        # Fallback: just place 2 at corners
        if g[0][0] == 0:
            g[0][0] = palette[0]
        if g[h - 1][w - 1] == 0:
            g[h - 1][w - 1] = palette[1] if len(palette) > 1 \
                              else (palette[0] + 1) % 10
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
    rng.shuffle(pool)
    while len(pool) < n:
        for c in [1, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return pool[:n]


def _pick_positions(bias, h, w, n, rng):
    if bias == "corners":
        positions = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        rng.shuffle(positions)
        return positions
    if bias == "diagonal":
        diag = [(i, i) for i in range(min(h, w))]
        anti = [(i, min(h, w) - 1 - i) for i in range(min(h, w))]
        rng.shuffle(diag)
        rng.shuffle(anti)
        return diag + anti
    if bias == "edges":
        edges = [(0, c) for c in range(w)] + [(h - 1, c) for c in range(w)] \
              + [(r, 0) for r in range(h)] + [(r, w - 1) for r in range(h)]
        rng.shuffle(edges)
        return edges
    if bias == "clustered":
        cr, cc = rng.randint(0, h - 1), rng.randint(0, w - 1)
        positions = [(r, c) for r in range(h) for c in range(w)]
        positions.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return positions
    positions = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(positions)
    return positions


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_pixel":
        g[h // 2][w // 2] = 3
        return g
    if name == "all_same_axis":
        # All pixels in same row → no different-color intersection
        r = h // 2
        cs = rng.sample(range(w), min(3, w))
        for i, c in enumerate(cs):
            g[r][c] = [3, 4, 6][i % 3]
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                if (r + c) % 2 == 0:
                    g[r][c] = 3
        return g
    return g
