"""Generator for 9b:hard_63 — boolean gallery from two templates.

Rule: 2 hollow 9-frames sorted by column give two binary templates
(via interior crop + normalize). Bottom row holds 1-3 codes from
{4, 5, 6, 7} = {OR, AND, A−B, XOR}. Output hstacks the boolean op
result per code, painted with the code value.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes (bottom row empty → "for each code" loop is
empty, output undefined / collapses to width-0); identical_templates
(both frames have same interior support → AND==OR==A; A−B is empty;
XOR is empty); empty_template (one interior empty → AND/A−B
collapse).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1b46e014e17c"
VERSION = "1.1.0"
TASK_ID = "1b46e014e17c"

SUMMARY = "2 hollow 9-frames + 1-3 boolean op codes (4/5/6/7) in last row."

INVARIANTS = [
    "background is 0",
    "exactly 2 hollow 9-frames at distinct columns",
    "each frame's interior holds 3-6 non-bg, non-9 cells",
    "last row holds 1-3 codes in {4, 5, 6, 7} at distinct columns",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "identical_templates", "empty_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_frames_with_codes",
                       "valid": "two_frames_with_codes"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "fixed_two_frames", "valid": "fixed_two_frames"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_codes_lo, n_codes_hi = 1, 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 14, 16)
        n_codes_lo, n_codes_hi = 2, 3
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        n_codes_lo, n_codes_hi = 1, 3
    rng = ctx.draw_rng("layout")
    fh, fw = 5, 5
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 2)
    col_starts = [0, fw + 2]
    if col_starts[-1] + fw > w:
        raise ValueError("grid too narrow")
    r0 = rng.randint(0, h - fh - 2)
    for c0, color in zip(col_starts, palette):
        for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
        for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
        cells = [(r, c) for r in range(r0 + 1, r0 + fh - 1)
                 for c in range(c0 + 1, c0 + fw - 1)]
        n = rng.randint(3, 6)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    n_codes = rng.randint(n_codes_lo, n_codes_hi)
    code_cols = rng.sample(range(0, w), n_codes)
    for c in code_cols:
        g[h - 1][c] = rng.choice([4, 5, 6, 7])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    fh, fw = 5, 5
    g = full_grid(h, w, 0)
    palette = (1, 2)
    col_starts = [0, fw + 2]
    r0 = 1
    if name == "no_codes":
        # Bottom row has no codes — rule's "for each code" loop is
        # empty; output width is 0, formally undefined.
        for c0, color in zip(col_starts, palette):
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            for r, c in [(r0+1, c0+1), (r0+2, c0+2), (r0+3, c0+3)]:
                g[r][c] = color
        return g
    if name == "identical_templates":
        # Both interiors identical — AND==OR==A; A−B is empty;
        # XOR is empty; rule's 4 branches collapse.
        cells_pat = [(r0+1, 1), (r0+2, 2), (r0+3, 3)]
        for c0, color in zip(col_starts, palette):
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            for dr, _ in [(1, 1), (2, 2), (3, 3)]:
                g[r0 + dr][c0 + dr] = color
        g[h - 1][2] = 5; g[h - 1][7] = 6
        return g
    if name == "empty_template":
        # One frame's interior is empty — AND collapses to ∅,
        # A−B = A (or = ∅); rule's set ops give degenerate outputs.
        c0 = col_starts[0]; color = palette[0]
        for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
        for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
        for dr, dc in [(1, 1), (2, 2), (3, 3)]:
            g[r0 + dr][c0 + dc] = color
        c0 = col_starts[1]
        for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
        for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
        # interior left empty
        g[h - 1][2] = 4; g[h - 1][7] = 5; g[h - 1][12] = 7
        return g
    return g
