"""Generator for 9b:m62 — frame color presence matrix.

Rule: row 0 is the legend (palette of distinct non-{0,9} colors).
Each 9-frame's interior holds some subset of legend colors. Output
is an NxL matrix (N frames, L legend colors): cell (i, j) = legend[j]
if color j is present in frame i's interior, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend (row 0 empty → rule has no palette to lift);
no_frames (legend present but no 9-frames → rule has no rows in
output); empty_interiors (frames present but interiors empty →
output is all-0).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3799ce10ce15"
VERSION = "1.1.0"
TASK_ID = "3799ce10ce15"

SUMMARY = "Top-row 3-color legend + 3 9-frames with varying interior color subsets."

INVARIANTS = [
    "background is 0",
    "row 0 holds 3 distinct non-{0,9} colors at distinct columns",
    "exactly 3 hollow 9-frames at distinct columns (sorted scan order)",
    "each frame's interior holds a non-empty distinct subset of legend colors (so output rows differ)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_frames", "empty_interiors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..18"},
    "grid_w":            {"type": "int", "default": "rng 19..21", "valid": "18..22"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "row0_legend_with_3_frames",
                          "valid": "row0_legend_with_3_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 19, 20)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 20, 21)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 19, 21)
    rng = ctx.draw_rng("layout")
    legend = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 3)
    fh = 6; fw = 5
    for outer in range(40):
        g = full_grid(h, w, 0)
        legend_cols = rng.sample(range(0, w), 3)
        for col, color in zip(legend_cols, legend):
            g[0][col] = color
        col_starts = [0, fw + 1, 2 * (fw + 1)]
        if col_starts[-1] + fw > w:
            continue
        r0 = rng.randint(2, h - fh)
        subset_codes = rng.sample(range(1, 8), 3)
        ok = True
        for c0, code in zip(col_starts, subset_codes):
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            interior = [(r, c) for r in range(r0 + 1, r0 + fh - 1)
                        for c in range(c0 + 1, c0 + fw - 1)]
            colors_present = [legend[i] for i in range(3) if (code >> i) & 1]
            slots = rng.sample(interior, len(colors_present))
            for (rr, cc), color in zip(slots, colors_present):
                g[rr][cc] = color
        if ok:
            return g
    raise ValueError("could not lay out legend + 3 frames + interior subsets")


def _draw_from_degenerate(name, rng):
    h, w = 12, 20
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Row 0 empty — rule has no palette to lift.
        for c0 in [0, 6, 12]:
            for c in range(c0, c0 + 5):
                g[3][c] = 9; g[8][c] = 9
            for r in range(3, 9):
                g[r][c0] = 9; g[r][c0 + 4] = 9
            g[5][c0 + 2] = 4
        return g
    if name == "no_frames":
        # Legend present but no frames.
        g[0][2] = 4; g[0][8] = 5; g[0][14] = 6
        return g
    if name == "empty_interiors":
        # Frames present but interiors empty.
        g[0][2] = 4; g[0][8] = 5; g[0][14] = 6
        for c0 in [0, 6, 12]:
            for c in range(c0, c0 + 5):
                g[3][c] = 9; g[8][c] = 9
            for r in range(3, 9):
                g[r][c0] = 9; g[r][c0 + 4] = 9
        return g
    return g
