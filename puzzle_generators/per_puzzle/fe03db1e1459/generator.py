"""Generator for arc_additional_puzzle_bank_volume23:M155 — Translate 1s by 2→3 delta.

Rule: dr/dc = (3-marker - 2-marker). For each 1-cell, place 8 at
(r+dr, c+dc) if in bounds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_ones, zero_delta.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fe03db1e1459"
VERSION = "1.1.0"
TASK_ID = "fe03db1e1459"
SUMMARY = "Several 1-cells in upper area + one 2-marker + one 3-marker further away; output translates 1s by 2→3 delta as 8s."

INVARIANTS = [
    "between 3 and 6 1-cells in upper portion",
    "exactly one 2-marker and one 3-marker",
    "delta is non-zero so output differs from input",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_ones", "zero_delta")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "ones_upper_markers_below",
                       "valid": "ones_upper_markers_below"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_ones = rng.randint(3, 6)
    used = set()
    placed = 0
    for _ in range(n_ones * 4):
        if placed >= n_ones: break
        r = rng.randint(0, h // 2)
        c = rng.randint(0, w // 2 + 1)
        if (r, c) in used: continue
        used.add((r, c)); g[r][c] = 1; placed += 1
    for _ in range(20):
        r = rng.randint(0, h // 2 + 1)
        c = rng.randint(0, w // 2 + 1)
        if (r, c) in used: continue
        used.add((r, c)); g[r][c] = 2; mr2, mc2 = r, c; break
    for _ in range(40):
        r = rng.randint(mr2 + 1, h - 1)
        c = rng.randint(mc2 + 1, w - 1)
        if (r, c) in used: continue
        dr = r - mr2; dc = c - mc2
        any_in = any(0 <= or_ + dr < h and 0 <= oc + dc < w
                     for or_, oc in used if g[or_][oc] == 1)
        if not any_in: continue
        used.add((r, c)); g[r][c] = 3; return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # 1-cells but no 2/3 markers — rule has no delta vector to
        # compute.
        for r, c in [(1, 1), (1, 3), (2, 2)]: g[r][c] = 1
        return g
    if name == "no_ones":
        # Markers but no 1-cells — rule has nothing to translate.
        g[2][2] = 2; g[5][7] = 3
        return g
    if name == "zero_delta":
        # 2 and 3 markers at the same location is impossible — but
        # placing them adjacently with the 3 ON the same cell as a 1
        # makes the delta zero in any practical attempt; here we
        # simulate "delta 0" by an effectively-coincident pair, which
        # makes the translation a no-op.
        for r, c in [(1, 1), (1, 3)]: g[r][c] = 1
        g[3][3] = 2; g[3][3] = 3  # 3 overwrites 2; only 3 remains
        return g
    return g
