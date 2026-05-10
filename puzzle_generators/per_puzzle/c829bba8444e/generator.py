"""Generator for 11b:hard_71 — library lookup transform gallery.

Rule: 9-frames sorted by col define the library (each frame's
cropped interior is one entry). Rows 0 and 1 at the same column hold
(selector, transform-code) pairs: row 0 is the 1-indexed library
selector, row 1 is the transform code in {1..4}. Output hstacks the
picked entries, each transformed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, no_frames, selector_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c829bba8444e"
VERSION = "1.1.0"
TASK_ID = "c829bba8444e"

SUMMARY = "3 hollow 9-frames + 2-3 (selector, transform) pairs at top rows."

INVARIANTS = [
    "background is 0",
    "exactly 3 hollow 9-frames at distinct columns (in lower portion of grid)",
    "each frame's interior holds 2-4 non-bg cells in a single non-9 color",
    "rows 0 and 1 hold 2-3 (sel, tr) pairs at distinct columns; sel ∈ {1, 2, 3}, tr ∈ {1..4}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "no_frames", "selector_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 17..19", "valid": "16..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "top_pairs_3_frames_below",
                       "valid": "top_pairs_3_frames_below"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "balanced", "valid": "balanced"},
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 17, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 19, 21)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 17, 19)
    rng = ctx.draw_rng("layout")
    fh = 5; fw = 5
    g = full_grid(h, w, 0)
    col_starts = [0, 6, 12]
    if col_starts[-1] + fw > w:
        raise ValueError("grid too narrow")
    r0 = rng.randint(3, h - fh)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 3)
    for c0, color in zip(col_starts, palette):
        for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
        for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
        cells = [(r, c) for r in range(r0 + 1, r0 + fh - 1)
                 for c in range(c0 + 1, c0 + fw - 1)]
        n = rng.randint(2, 4)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    n_pairs = rng.randint(2, 3)
    pair_cols = rng.sample(range(0, w), n_pairs)
    for c in pair_cols:
        sel = rng.randint(1, 3)
        tr = rng.randint(1, 4)
        g[0][c] = sel
        g[1][c] = tr
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 17
    g = full_grid(h, w, 0)
    fh = 5; fw = 5
    r0 = 5
    palette = [3, 4, 6]
    if name == "no_pairs":
        # 3 frames in library but no (sel, tr) pairs in rows 0/1 —
        # rule has nothing to look up; output is empty hstack.
        for c0, color in zip([0, 6, 12], palette):
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            g[r0 + 1][c0 + 1] = color
        return g
    if name == "no_frames":
        # (sel, tr) pairs but no library frames — rule's selector
        # lookup has no entries.
        g[0][2] = 1; g[1][2] = 3
        g[0][8] = 2; g[1][8] = 4
        return g
    if name == "selector_oob":
        # Pairs reference selector index larger than the library size
        # — rule's lookup has no entry for those selectors.
        for c0, color in zip([0, 6, 12], palette):
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            g[r0 + 1][c0 + 1] = color
        g[0][2] = 5; g[1][2] = 2
        g[0][8] = 7; g[1][8] = 1
        return g
    return g
